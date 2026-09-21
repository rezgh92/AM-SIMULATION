# CUPOLA — Copper Unknown-binder Process Optimisation, Learning and Analysis

**An architecture for simulating debinding and sintering of the Lithoz R&D copper slurry, and for deriving an optimum thermal cycle without knowing the binder.**

Status: proposal for discussion. Nothing implemented yet.
Evidence base: `docs/research/` — 27 agent reports from a 10-dimension literature and data sweep, three competing architectures, three adversarial design reviews, one completeness critique.

---

## 0. The short version

Three things came out of the research that change the shape of the project.

**1. You mostly do not need to know the binder.** Oxidative debinding of a metal-filled photopolymer is not kinetics-limited. It is limited by oxygen delivery and heat removal. In that regime the binder's pre-exponential factor has no leverage on the part-scale answer, and the minimum debinding time follows a parameter-free law. This is the central bet of the whole proposal, it is checkable in week 1, and it is the reason this project is tractable at all.

**2. The real problem is an ordering problem, not a temperature problem.** Copper forms no carbide, so carbon leaves only by gasification. Once porosity closes at ~92 % relative density, residual carbon and any reduction steam are sealed in permanently. Carbon and oxygen must be below spec *before* that moment. That "before" is an interior-point event constraint, and it is what makes this genuine optimal control rather than curve fitting.

**3. There is a reaction that every one of the three independent designs missed, and it is central.** `Cu₂O + C → 2Cu + CO` has ΔG = 55 200 − 158.3·T J/mol from the standard Ellingham fits — spontaneous above **76 °C**. Carbon and copper oxide cannot coexist. It is simultaneously the real carbon sink in any oxidise-then-reduce route and the real blistering source, because CO is insoluble in copper and is generated inside a body whose porosity is closing.

The recommended architecture is a **fail-fast execution spine with an uncertainty-native core**: a furnace-executable cycle in week 1, real parts in week 4, and a chance-constrained optimal-control model that grows out of the measurement campaign rather than preceding it.

**Answer to "can we actually simulate this?" — yes, with a specific and honest caveat.** Shrinkage factors, safe ramp rates, cycle-time scaling with section thickness, the ordering of chemical events, and *relative* comparisons between cycles will be predicted well. Absolute final density to better than ~2 percentage points, and absolute probability of cracking on a specific geometry, will not — those depend on flaw populations and on binder chemistry details that no amount of inference recovers. The deliverable is therefore a cycle **with a credible interval and a chance constraint**, not a single trajectory presented as truth.

---

## 1. What the research actually established

The numbers below are the load-bearing ones. Each was independently recomputed by at least one adversarial reviewer; where reviewers disagreed with the original claim, the corrected value is given. Full provenance in `docs/research/`.

### 1.1 The machine and the material

| Quantity | Value | Note |
|---|---|---|
| CeraFab Multi 2M30 pixel pitch | **35 µm**, 2194 × 1234 px, 76.79 × 43.19 mm | The datasheet's "635 dpi" is a copy-paste artefact from the S65/L30 (those are genuinely 40 µm). The "30" in 2M30 is not the pixel size. Verified by arithmetic closure in a Lithoz-coauthored paper using this exact machine. |
| Light engine | **450 nm, 50 mW/cm² max** | Not 460 nm / 83 mW/cm² — those are CeraFab 7500 values. ~40 % less peak intensity than the 7500, which matters because copper doses will be large. |
| Reference dose (LithaLox 350, 49 vol% alumina) | 130–180 mJ/cm², 25 µm layers, 20–30 s settle | A copper slurry will need far more. |
| Lithoz LCM organic-phase density | **1.13 ± 0.03 g/cm³** | Derived two independent ways (LithaLox HP500 slurry density inversion; LithaNit 720 TGA inversion) — they agree. |
| **Solids-loading inversion** | **φ = (ρ_slurry − 1.13) / 7.83** | One pycnometer measurement on the as-received slurry gives φ to ≈ ±1 vol%. ρ = 4.65 → 45 vol%; 5.04 → 50 %; 5.44 → 55 %. |
| Expected φ | 0.45–0.58 | Lithoz ceramics are 39–49 vol%; published copper DLP/LMM is 50–60 vol% (Incus 52–58, CEA 60). |
| Binder mass fraction vs φ | 15.9 wt% @ φ=0.40; 13.4 @ 0.45; 11.2 @ 0.50; **9.4 @ 0.55**; 7.8 @ 0.60 | Low wt% does *not* mean easy: gas generated per cm³ is the same as for alumina. |

### 1.2 The trap that makes naive characterisation useless

Copper **gains** mass by oxidation while the binder loses it, and the gain is comparable to or larger than the signal:

| Temperature | Cu mass gain in air |
|---|---|
| 400 °C | +8.0 wt% |
| 600 °C | +14.4 wt% |
| 800 °C | +16.8 wt% |

Against a binder inventory of 7.3–13.6 wt%. **A raw air-TGA of a filled sample can return a negative binder content.** This single fact invalidates the standard burn-off method and dictates the characterisation strategy in §3.

### 1.3 The regime claim — why the binder is largely irrelevant

Frank-Kamenetskii number for a slab, δ = Q·ρ_b·A·E·L²/(k_eff·R·T²)·exp(−E/RT), with Q = 25 MJ/kg, ρ_b = 550 kg/m³, E = 150 kJ/mol, A = 10¹³ s⁻¹, k_eff = 1 W/mK, against a slab-critical δ_c = 0.88:

| Geometry | δ | vs critical |
|---|---|---|
| 1 mm half-thickness, 250 °C | 9.5 | 11× supercritical |
| 5 mm, 250 °C | 239 | 270× |
| 10 mm, 350 °C | 1.7 × 10⁵ | 190 000× |

Supercritical by one to five decades at every geometry the 2M30 can print. A reaction that far supercritical is **never kinetics-limited**; `d(ln t_burn)/d(ln A) → 0`. Two independent reviewers reproduced this table to within 2 %.

The consequence is a **zero-parameter design law**:

> **t_min = ΔH_c · ρ_b · (V/A) / (h · ΔT_crit)**

= **47.7 h** for a 5 mm half-thickness at h = 20 W/m²K and ΔT_crit = 20 K; 95.5 h at 10 mm; **9.5 h** at 5 mm if h is raised to 100 W/m²K.

This reproduces Fraunhofer IFAM's 63 h / 250 °C cabinet hold and CEA-LITEN's multi-day cycle with **no fitted parameters**. Three consequences a human schedule-writer will not reach:

- The optimal debind is **near-isothermal with pO₂ as the throttle**, not a temperature staircase. Ramping T buys nothing and only risks runaway.
- Time scales **linearly** with half-thickness, not quadratically.
- **The real lever is h, the gas-side heat transfer coefficient.** A baffle and higher flow — order 1 k€ — compresses a 5 mm part from 47.7 h to 9.5 h at identical thermal risk. This is the single highest-return change in the project.

**The caveat that decides the claim.** All of this is at k_eff = 1 W/mK. At k_eff = 10 W/mK — plausible if the copper particles percolate, and the Maxwell-Eucken polymer-continuous closure is likely wrong for a 50–60 vol% green body whose particles are in contact — δ = 0.95 at 1 mm, i.e. marginal, not supercritical. The claim then degrades to "binder kinetics are irrelevant above roughly 2 mm section." **Laser-flash k_eff on a cured coupon is therefore the single most consequential week-1 measurement in the project.**

### 1.4 Constraints that turn out to be slack — and one that is not

Three constraints that intuition says should dominate are, on the numbers, inactive. Two of the three competing designs built major machinery around them anyway; one design's headline result was wrong by 4.8 decades on this exact point.

| Constraint | Verdict | Numbers |
|---|---|---|
| **Internal gas pressure (Darcy)** | **Slack by 1.5–4 decades** | Compressible Darcy slab, Kozeny-Carman K = ε³d²/180(1−ε)²: 1.70 bar at ε=0.02, 0.17 at ε=0.05, 0.021 at ε=0.10 for 16 µm powder, 5 mm half-thickness, 10 %/h binder loss — against **100–230 bar** green strength. *Gated re-enable: at d50 = 4 µm the same calculation gives 38 bar at 2 % porosity, which is green strength.* |
| **Ellingham / Cu-Cu₂O oxidation** | **Slack by ~9 decades** at practical setpoints | Boundary pH₂O/pH₂ = 1.29×10⁵ at 700 °C, 1.26×10⁴ at 1000 °C. At 1000 ppm H₂ and +20 °C dew point the reducing margin is 2222× at 800 °C, 546× at 1000 °C. Atmosphere control during the carbon hold is **not** about protecting the copper. |
| **Steam efflux as a Darcy problem** | **Wrong mechanism** | Reducing an 8 wt% oxygen pickup releases 22 400 mol H₂O/m³; over 4 h that is a 75 Pa centre overpressure. Five decades slack. But the swelling is real — it is *intraparticle*, at the particle radius, not the part half-thickness. |

**The one that is not slack** is the exotherm/heat-removal budget of §1.3, which is active throughout the entire pyrolysis phase and is the binding constraint on cycle time.

### 1.5 Physics that must be added — the corrections

These are the substantive fixes the adversarial review produced. All three independent architectures got at least some of them wrong.

**(a) The carbothermic channel.** `Cu₂O + C → 2Cu + CO`, ΔG = 55 200 − 158.3·T J/mol, negative above **349 K (76 °C)**. Equilibrium p_CO = 1.5×10² atm at 200 °C, 9.7×10³ atm at 400 °C. Carbon and copper oxide cannot coexist — this is why copper is smelted with carbon. Consequences: the widely-repeated "carbon cannot be removed below ~700 °C" story is **wrong for an air-debound part**, whose internal oxide gasifies the char at 400 °C; and CO, being insoluble in Cu, is a blistering source. Detectable signature: a CO spike at 300–500 °C under inert gas.

**(b) The eutectic ceiling is against the solidus, not the eutectic composition.** All three designs wrote "T ≤ 1066 °C whenever [O] > 0.39 wt%". But 0.39 wt% is the *eutectic composition*; the **solid solubility of oxygen in copper at 1066 °C is ~0.008 wt% (≈80 ppm)**. Any part above ~100 ppm O begins to melt at the eutectic temperature. Against terminal specs of 200–3000 ppm O, **1066 °C is a near-permanent ceiling until deoxidation is complete** — which removes the 1066–1085 °C window where copper densifies fastest.

**(c) Pore-gas back-pressure is the terminal-density limiter, and nobody had it.** σ_s,eff = 2γ/r_pore − p_gas. At γ = 1.5 J/m², only **30 bar** of trapped gas at r = 1 µm halts densification entirely (15 bar at 2 µm). Closed-pore gas in an air-debound copper part is H₂O/CO/CO₂ — all insoluble in Cu, unlike H₂, which is precisely why hydrogen sintering works. This is the standard limiter in the 92→99 % window that is the whole target. It is also the mechanistic justification for the 200 ppm carbon spec, which cannot be about surface poisoning: 200 ppm C on 16 µm Cu powder is already 6–13 monolayer equivalents.

**(d) Hydrogen embrittlement is not a Darcy problem.** It is lattice diffusion of dissolved H to *internal* Cu₂O inclusions, producing H₂O that is insoluble and immobile in copper and nucleates high-pressure voids at grain boundaries. Intraparticle, sub-continuum. A Darcy efflux constraint will certify parts that embrittle. The correct control is the **ordering constraint**: complete reduction while porosity is still open.

**(e) Phosphorus.** At 450 nm only BAPO-class acylphosphine oxides and acylgermanes are practical photoinitiators, and many LCM dispersants are phosphate esters. The **Cu–Cu₃P eutectic is at 714 °C** — far below any sintering temperature, so trace P gives liquid phase, local slumping and embrittlement in the middle of what you thought was solid-state debinding. At BAPO 0.5–2 wt% of the organic fraction the all-retained P budget is 30–182 ppm, costing 2.2–13 %IACS. Assay for **P, Ge, Sn, S** — not P alone.

**(f) Frank-Kamenetskii δ < 0.88 must never be a hard path constraint.** Two of the three designs imposed it. Solving δ(T) = 0.88 gives T_crit = 214 °C at 1 mm, 173 °C at 5 mm, **158 °C at 10 mm**. Nothing decomposes at those temperatures, so the constraint is mutually infeasible with binder removal and the optimiser returns infeasible. FK criticality is derived for a non-depleting, zeroth-order, oxidant-unlimited reactant — not for a pO₂-throttled burn. Keep δ as a **regime diagnostic**; carry thermal safety entirely on the transient excess-temperature constraint.

---

## 2. Architecture

Five tiers plus an instrument. Each tier is independently testable, and each has a written numeric trigger for when the tier above it gets built.

### T0 — Thermochemical feasibility layer
*No fitted parameter ever lives here.*

- Cu–C–O–H predominance diagram as a design tool; Ellingham lines for Cu/Cu₂O, H₂/H₂O, C/CO, C/CO₂, **and the carbothermic line**.
- Arden Buck dew-point ↔ pH₂O actuator map; water-gas-shift equilibrium; pO₂ from any gas blend.
- Reducing margin m(T), gasification driving force, **solidus-based eutectic ceiling T_max([O])**.
- **Implementation:** pure Python/JAX, `cantera` + hand-coded Gibbs fits. Traceable, so it composes into the optimiser.
- **Verification (day one, in CI):** must reproduce IBM's 785 °C / H₂:H₂O = 10⁻⁴ production setpoint as sitting 5.8× on the reducing side.

### T1 — The digital coupon (0-D / 1-D reduced-order model)
*The workhorse. Everything the optimiser and the sampler see.*

- State vector (13–15): `T_part, S_solvent, α₁..α₃, X_ox, X_red, C_char, ρ_rel, G, ε_open, n_O, n_C, p_pore, y_gas`.
- Physics: lumped/1-D thermal with radiation; N-component Šesták-Berggren binder decomposition; parabolic Cu→Cu₂O oxidation with PBR = 1.68 eigenstrain; **JMAK-with-incubation** oxide reduction (not first-order Arrhenius — this materially changes blistering risk); **carbothermic Cu₂O + C**; C + H₂O gasification with product inhibition; Darcy + Klinkenberg **plus a pre-percolation free-volume branch** below ε_c (Kozeny-Carman diverges as ε→0, and that is exactly where cracking happens); SOVS densification with **pore-gas back-pressure in the sintering stress**.
- **Implementation:** a NumPy reference *and* a CasADi graph, CI-tested to agree to 1e-8. Milliseconds per solve.
- Olevsky's seven closure constants are held **fixed at their theoretical values**. They are continuum-mechanics results, not free fits; fitting them is how the identifiability problem gets manufactured.

### T2 — Retort model
CSTR tanks-in-series oxygen balance, measured h, radiative lag, MFC/bubbler actuator map with slew limits. Its job is to make pO₂, pH₂, pH₂O at the *part surface* algebraic states computed from setpoints — so the optimiser physically cannot propose an atmosphere the rig can't make.

### T3 — Identification, triage and uncertainty
- **Triage before spending.** Morris screening → Sobol → profile likelihood → active subspace, producing an `IDENTIFIED / MARGINALISED / IRRELEVANT` verdict for every parameter, versioned in `docs/triage_table.md`. An experiment that sharpens an IRRELEVANT parameter must visibly score zero. Time-boxed to two weeks on the existing T1 graph — not a standalone three-month phase.
- **Isokinetic reparameterisation**, mandatory on every Arrhenius term: `k(T) = exp(κ − (E/R)(1/T − 1/T_iso))`. The raw (lnA, E) Jacobian columns over a 200–500 °C window correlate at **−0.9999**; this one-line change orthogonalises them and is worth more than extra data. (Centre T_iso on the sensitivity-weighted harmonic-mean temperature of the reaction window, ≈ 610–625 K — not on E/(R·lnA), which is the k = 1 temperature.)
- Bayesian inference in NumPyro/PyMC with **hierarchical lot-level random effects**, so a second drum of R&D slurry re-uses the population prior instead of forcing full recalibration.
- **Kennedy-O'Hagan discrepancy applied to constraint margins**, not raw TGA curves — and disabled by a CI guard until the residual passes a whiteness test. *No discrepancy term can absorb a missing source term.*

### T4 — Chance-constrained multi-phase optimal control
The deliverable layer. See §4 for the full programme.
CasADi + IPOPT, Radau IIA collocation, free phase-switching times, **outer enumeration over atmosphere topologies {OX, WGS, HYBRID}**. Compiles to a Eurotherm nanodac / Nabertherm segment program with the **active-constraint timeline attached**, so an operator and a referee can both see which physical limit the cycle is riding at each instant.

### T5 — 3-D thermo-chemo-mechanical (escalation only)
MOOSE + NEML2, built on upstream `idaholab/moose`. Anisotropic sintering stress (P_lR, P_lZ), gravity, setter friction, large deformation, inverse shrinkage compensation. **Built only when a numeric trigger fires** (shrinkage anisotropy > 1.5 percentage points).
*Day-one unit test before any 3-D work:* NEML2's sintering stress uses `3γφ²/r` where the classical Olevsky form is `3γρ²/r`. The ratio is **132× at ρ=0.92, 361× at 0.95, 2401× at 0.98** — the driving force vanishes precisely in the window that separates "another 90 %-dense copper part" from a result. Make all three forms selectable and unit-tested. Cost: one day.

### The instrument — exhaust-gas observer
**Zirconia pO₂ sensor + dew-point meter + NDIR CO₂ (or a small RGA) on the retort outlet.** All three adversarial reviewers independently named this the single best idea in the set.

It measures, in real time and **without knowing anything about the binder**, exactly the two quantities every ordering constraint is written on: how much carbon is actually leaving, and the realised oxygen potential. It converts a large slice of irreducible binder uncertainty from a marginalisation problem into a feedback problem — which is strictly better. It is the only proposed instrument that would detect the carbothermic CO burst. And it turns every furnace run into a calibration dataset instead of a pass/fail.

Buy it in week 1, alongside the bubbler and heated line.

---

## 3. The unknown-binder strategy

Seven steps, in execution order. The principle: **do not try to discover the chemistry — make it mostly irrelevant, and quantify the residue.**

**(1) Architectural decoupling.** The binder never appears in the code as a chemistry. It appears as a measured inventory — `{S_solvent, α₁..α_N network pseudo-components, C_char, ash}` plus a heteroatom vector `{P, Ge, Sn, S, Si, Na, Cl}` in ppm. Identifying the monomers is interesting for a paper and irrelevant to the cycle; identifying binder content, char yield and exotherm is what the cycle depends on. This is what lets work start before the chemistry is known.

**(2) The mass-balance closer — LOI-then-reduce.** One day, ~200 €, and the single highest-value experiment in the project.
Cured, washed, vacuum-dried coupon m₀ (2–5 g) → muffle 600 °C air 4 h → m₁ → tube furnace 4 %H₂/Ar 400 °C → m₂. Then **m_binder = m₀ − m₂**, and the copper's oxygen pickup cancels identically. This is the direct answer to the §1.2 trap.
**With the guards the reviewers demanded, which are non-negotiable:** crush the oxide cake before reduction; **reduce to constant mass** (re-weigh, re-reduce, require stability to 0.05 wt% on a second cycle) rather than a fixed 2 h; run a **bare-recovered-powder control** through the identical sequence to prove mass return; and **LECO C and O on the reduced residue m₂** to detect the two one-sided biases (incomplete bulk-Cu₂O reduction, and char encapsulated inside a sintered oxide shell). Quote accuracy of **±0.2–0.5 wt%** on a 7–14 wt% quantity — that is the real figure. The ±0.005 wt% that appears in the naive version is balance resolution, not accuracy.

**(3) Triangulate three independent routes.** LOI-then-reduce, He pycnometry + wax-sealed Archimedes, and the switched TGA of step 4. They must agree to 0.5 wt% or the feedstock state card is rejected by schema validation. Three routes agreeing is a far stronger methods figure than any single route.

**(4) The corrected TGA protocol.** Ramp in argon to 600 °C to capture network scission and residual char, then **switch to air isothermally at 600 °C** within the same run to combust the char and close the balance — an inert-only TGA under-reports binder by the ~7 wt% char that acrylates leave in argon but not in air. Run a **matched bare-Cu-powder blank** at the same d50, crucible, ramp and atmosphere sequence, and subtract.
The ingestion layer **refuses at runtime** to compute conversion from a raw air-TGA of a filled sample with no linked blank. One guard, and it protects the entire downstream analysis.
Then the ICTAC-2020 stack: Friedman → Vyazovkin advanced integral → KAS/OFW (auto-disabled when E(α) varies by more than 15 % over α ∈ [0.1, 0.9]); model selection over N = 2..4 parallel Šesták-Berggren reactions by BIC/PSIS-LOO; unit-tested against the **numerically integrated Simha-Wall random-scission solution** rather than a published table whose column headers conflict between sources. Minimum four heating rates (1, 2, 5, 10 K/min) and **blind prediction of a fifth rate not used in the fit**.
Critical: run TGA on **printed, cured green material**, never neat resin — copper and Cu₂O catalyse polymer decomposition.

**(5) The binder-agnostic worst-case envelope — what runs in week 1.** Take the union of worst cases over the plausible binder family {LCM acrylate + non-reactive solvent; Incus-type wax thermoplastic; plain HDDA/oligomer}: earliest onset 70 °C, latest completion 500 °C, highest char yield 7 wt% of organics, highest exotherm 30 MJ/kg, highest loading 13.6 wt%, lowest green conductivity 0.80 W/mK. Run T1 at each corner, take the pointwise-slowest T(t) and pointwise-lowest pO₂(t). Conservative by construction, defensible as *worst-case-envelope cycle synthesis under binder uncertainty*, and it narrows automatically as measurements land. The code reports the **wall-clock hours saved by each measurement** — which is how the next experiment gets funded.

**(6) State the irreducible unknowns and price them.**
- *Photoinitiator heteroatom* — structural risk, not incidental (§1.5e). ICP-OES/MS on digested green vs recovered powder settles it in a day. Nasty coupling: driving oxygen to zero makes the phosphorus penalty **worse**, because phosphates otherwise getter P out of solid solution.
- *The light-absorbing dye.* Lithoz LCM slurries contain dyes to moderate cure depth; aromatic dyes are prime char precursors; and **none of the published copper vat-photopolymerisation studies (Roumanie, IFAM, Resch) used one.** Their encouraging residual-carbon results may be systematically optimistic for this specific material. This is the single largest threat to external validity in the project. Detectable in one Py-GC-MS run at 620 °C, and stating it up front is how the paper survives the referee who has actually printed with LCM slurries.
- *Physical form of residual carbon on copper* (amorphous vs graphitic vs adsorbed) — unmeasured anywhere in the literature. Raman D/G on interrupted coupons. Since 200 ppm is already 6–13 monolayer equivalents, **speciation is the physically meaningful variable, not ppm**.

**(7) Ask Lithoz. Do not let pride add three weeks.** Under NDA, request: organic volume fraction; copper powder supplier, grade, D10/50/90, morphology, BET, **and as-received LECO oxygen in ppm**; any powder surface passivation (stearate, benzotriazole — that is carbon and nitrogen you will otherwise have to account for); whether the photoinitiator is acylphosphine-oxide or acylgermane class (yes/no is enough); dispersant chemistry; whether a dye is present; and **any internal recommended thermal envelope for this slurry, even flagged unvalidated** — that last item is the highest-value single unknown in the project. Also demand the safety data sheet (they are obliged to supply one even for R&D material, and its hazard classifications alone constrain the chemistry).
Run the full campaign anyway — you need the measurements for the paper regardless.

**Two commercial items with weeks of lead time, so start them now:**
- **Confirm in writing that all material supplied is from a single batch, and retain a sealed reserve sample.** If a second lot with different binder arrives mid-project, every kinetic parameter you identified is void.
- **Negotiate publication and IP terms before the first experiment.** Using a partner's undisclosed material creates a specific failure mode: you generate results you are contractually unable to describe. Agree a right to publish, a 30–60 day review window, what may be redacted, and ideally **Lithoz co-authorship** — a co-author both solves the disclosure problem and makes the paper stronger.

---

## 4. The optimal control problem

A multi-phase, chance-constrained hybrid OCP, solved on T1 and verified on the 1-D and 3-D models.

**Phases** — four, with free durations and free switching times, plus an outer enumeration over atmosphere topology {OX, WGS, HYBRID}. The enumeration is essential: every published copper success used an atmosphere *switch*, and a purely continuous T(t) optimiser will never discover that structure. It also converts the topology from an assumption into a finding, which is the difference between a result and a claim a referee will strike.

- P1 Dry (25–250 °C, evaporation-limited)
- P2 Pyrolyse (200–500 °C, **exotherm-limited — this is the binding phase**)
- P3 Carbon + reduce (450–900 °C, gasification- and SSA-limited)
- P4 Densify (900–1066 °C, SOVS)

**Decision variables** — actuator-space, so the answer is executable:
`T_furnace(t)` ∈ [20, 1066] °C with |dT/dt| ≤ 5 K/min and a slew bound; `x_O2,in` ∈ [0, 0.21]; `x_H2,in` ∈ [0, 0.04] (hard cap for lab safety below the 4.1 % LFL and for the steam-embrittlement limit); `T_dewpoint` ∈ [−60, +60] °C; `P_tot` ∈ [50, 1000] mbar; total flow ∈ [0.5, 10] slpm. Plus switching times τ₁..τ₃ and terminal time t_f.

**Objective** — `min t_f`. Furnace hours are the binding resource, and a scalarised quality-plus-time objective just hides the trade-off inside an arbitrary weight. Quality enters as constraints. Run as an **ε-constraint sweep over the carbon spec to produce a genuine Pareto front** (cycle time vs residual C vs P[success]) — that front, not a single cycle, is the real deliverable.

**Constraints.**

*Hard, deterministic, from T0 (no uncertainty, so no chance level):*
- pH₂O/pH₂ ≤ boundary(T) with margin — inactive at practical setpoints, kept as a guard.
- **T ≤ 1066 °C wherever local [O] > ~80 ppm** (solidus, §1.5b), relaxing only as the oxygen *field* falls. Spatially local, not a bulk scalar.
- Complementarity `y_O2 · y_H2 ≤ ε`, relaxed homotopically from 1e-2 to 1e-8 — correct physics over a combustion-catalytic metal, and a safety constraint.

*Interior-point event constraints — the heart of the problem:*
Define `t_close(x)` as the first time ρ(x,t) crosses ρ_close. Then
- `P[ C(x, t_close) ≤ 200 ppm ] ≥ 0.95`
- `P[ O(x, t_close) ≤ 300 ppm ] ≥ 0.95`
- `χ_reduction(x, t_close) = 1`

This is the mathematically correct statement of an ordering requirement, and it is what gives the optimiser a positive reason to *slow* the approach to 800–900 °C. Terminal-time or integral-penalty surrogates do not express it.
*Deeper version:* track **specific surface area**, not density — gasification is area-proportional and SSA collapses well before open porosity closes at ~92 %. The SSA-collapse clock is the real deadline.

*Chance constraints over the posterior predictive:*
- `P[ max_t (T_part − T_furnace) ≤ ΔT_crit ] ≥ 0.99` — **but only evaluated on a model with spatial resolution**, because a lumped temperature field is structurally incapable of producing the runaway it would certify against. Escalate T1 to 1-D whenever the optimiser enters the un-throttled branch.
- `P[ σ_max / σ_t(T, α, orientation) ≤ 1 ] ≥ 0.99` with a measured anisotropic green-strength surface and a separate interlayer cohesive check.

*Diagnostics, not constraints:* Frank-Kamenetskii δ (§1.5f); Darcy overpressure (§1.4, with the d50 < 6 µm re-enable trigger).

**Chance-constraint handling.** Sparse PCE (degree 3, hyperbolic truncation q = 0.7) over the triaged uncertain parameters gives analytic mean and variance of each constraint residual. Report **both** the distribution-free Cantelli tightening (κ = 4.36 at ε = 0.05) **and** the Gaussian (κ = 1.645), and say plainly that the first is conservative by construction — it inflates every margin 2.65× and the resulting "optimum" is a bound-optimum. Then **verify post-hoc with a 10⁴-sample Monte Carlo of the full posterior predictive** and quote the empirical satisfaction rate. Cheap in the loop, expensive in verification — never the reverse.

**Solver.** CasADi + IPOPT (HSL MA57/MA97), Radau IIA degree 3, ~60 finite elements per phase. Typical solve 2–15 min on a laptop. Multi-start from 20 perturbed guesses; report the spread, because a single local optimum presented as global is dishonest.

**Warm start / validation gate.** Both published industrial cycles are free, validated feasible points — **require the constraint set to admit them as feasible before the optimiser's own recommendation is trusted**:
- CEA-LITEN: 400 °C/4 h air + 1050 °C/4 h H₂ at 400 mbar
- Fraunhofer IFAM: acetone solvent debind 24 h; air 24 h/120 °C + 63 h/250 °C; 2 h/1050 °C in 99.999 % H₂ → 95.3 % density at 52 vol% loading

That yields a clean referee-facing sentence: *"the constraint set admits both industrially validated cycles as feasible points, and strictly dominates them in time."*

---

## 5. The baseline cycle — runnable next week

This is the binder-agnostic worst-case envelope, with the §1.5 corrections applied. It exists so that the furnace is not idle while the model is being built, and so that Gate 0 has **in-house anchor data with known loading, gas velocity and thermocouple placement** — strictly better evidence than either published cycle.

**Design intent, which is where it differs from the naive version:** throttle oxygen hard throughout rather than debinding in air. That is the lever the regime analysis identifies anyway, and it has a second benefit — it prevents the bulk oxidation (up to 63 % conversion to Cu₂O, +43 vol%) that creates the entire steam-reduction and blistering problem downstream. Accept more char, then gasify it in wet H₂ at 700–850 °C where C + H₂O is kinetically viable and porosity is still open.

| Segment | Ramp | Hold | Atmosphere | Rationale |
|---|---|---|---|---|
| 25 → 80 °C | 0.5 K/min | 4 h | N₂ | Solvent removal. Resch measured a 70–140 °C event. |
| 80 → 150 °C | 0.1 K/min | 12 h | N₂ | Non-reactive solvent; evaporation-limited. |
| 150 → 205 °C | 0.1 K/min | 8 h | N₂ | Onset of network scission. |
| 205 → 300 °C | 0.05 K/min | 6 h | N₂ + 2000 ppm O₂ | **Exotherm-limited.** O₂ throttled to hold ΔT < 20 K, not ramp-limited. |
| 300 → 400 °C | 0.05 K/min | 4 h | N₂ + 2000 ppm O₂ | Same. Deliberately *not* 2 vol% — oxygen budget, not just heat budget. |
| 400 → 450 °C | 0.2 K/min | 1 h purge | N₂ | Complete pyrolysis; purge before any H₂. |
| 450 → 800 °C | 2 K/min | **8 h** | N₂ + 0.1 % H₂, **dew point +40 °C** | Wet-H₂ carbon gasification *and* slow oxide reduction, concurrently, while porosity is fully open. Low pH₂ deliberately keeps the reduction front slow. |
| 800 → 1040 °C | 3 K/min | 3 h | dry 4 %H₂/Ar | Densification. **Ceiling 1040 °C, 26 K below the 1066 °C eutectic** — not 1050, and never above 1066 until [O] is verified sub-100 ppm. |
| 1040 → 600 °C | 3 K/min | — | 4 %H₂/Ar | Reducing on cooldown. |
| 600 → 25 °C | 5 K/min | — | N₂ | Below the H₂ re-oxidation window. |

**Total = 146 h** (ramps 68.4 h + holds 78.0 h), of which the 205–400 °C pyrolysis window alone is **75 h**.

> **Note on a corrected number.** The underlying research report quoted "~78 h" for this segment
> list. That is wrong — the segments sum to 146.4 h, and the 0.05 K/min ramps through 205–400 °C
> account for 65 h of it on their own. The corrected figure changes the reading in a useful way:
> **v0 offers essentially no time advantage over Lithoz's 156 h alumina debind.** It is not
> supposed to. It is a worst-case envelope whose job is to be safe and to generate anchor data.
> The interesting comparison is against the design law of §1.3, which puts the exotherm-limited
> floor for a 5 mm part at 47.7 h — so v0's pyrolysis window is **1.57× the floor**, which is
> about right for an envelope built on the union of worst cases. **Closing that 1.57× gap, and
> then attacking the floor itself by raising h, is the optimiser's entire job.**

Everything except the temperatures is literature-anchored; **the temperatures themselves are an educated envelope and should be treated as such.** Run it on coupons, not on anything you care about, with the exhaust-gas observer recording.

**Run one deliberate control alongside it:** Lithoz's ceramic-style cycle applied as-is. It is cheap, it is almost always skipped, and it establishes the failure mode you are actually fixing.

---

## 6. Experimental campaign

Ordered by information per euro. The **slurry, not the furnace, is the binding constraint** — compute grams per coupon × number of coupons against what was actually delivered, hold a reserve for the final demonstrator, and keep a sealed retained sample.

**Decouple from the printer.** There is no vat parameter set for this slurry, the 450 nm working curve for a copper slurry is unpublished, and 8.96 g/cm³ particles sediment over a long build. Run the feedstock campaign (E0, E1, LOI closure) on **flood-cured slurry cast in silicone moulds**. This removes an unbounded schedule risk from the critical path; printing is derisked in parallel.

| # | Experiment | Instrument | Identifies | Priority |
|---|---|---|---|---|
| E0 | Slurry density + He pycnometry + LOI-then-reduce (with all §3.2 guards) + ICP for P/Ge/Sn/S | Pycnometer, muffle + tube furnace, ICP-OES | φ, binder content, heteroatom budget | **Critical** |
| E1 | Multi-rate TGA (1/2/5/10 K/min), Ar→air switched, matched Cu blank; + 5th rate held out | STA | Binder kinetics, char yield | **Critical** |
| E2 | **Laser-flash k_eff on cured coupon** | LFA | Decides the entire flux-limited thesis (§1.3) | **Critical** |
| E3 | Bomb calorimetry / DSC for ΔH_c | Bomb cal., DSC | The design law scales linearly with it; 25 MJ/kg is currently an assumption | **Critical** |
| E4 | **Embedded-thermocouple thickness ladder, 2/5/10 mm** | Retort + TCs | Directly tests t_min = ΔH_c·ρ_b·(V/A)/(h·ΔT_crit); measures h | **Critical** |
| E5 | **Two-arm fork: oxidise-then-reduce vs never-oxidise-and-gasify** | Retort ×2 runs | A genuine binary unknown with no measured rate constants anywhere. Three weeks of furnace time instead of eighteen months of inference. | **Critical** |
| E6 | Interrupted-quench ladder at 600/700/800/900/950/1000 °C → LECO C+O, XRD phase, Archimedes + He pycnometry for open/closed porosity split | LECO, XRD | **Locates pore closure and proves the ordering race is won.** If carbon remains when open porosity vanishes, the cycle is unrecoverable. | **Critical** |
| E7 | σ_t(T, α) hot green strength on interrupted-debinding coupons, RT/100/200/300 °C, three build orientations | Environmental-chamber UTM | The **denominator of every mechanical constraint**. Does not exist for any metal-filled photopolymer. Publishable alone. | High |
| E8 | Multi-rate dilatometry + **gravity-loaded overhang bar** | Optical dilatometer | Densification kinetics **and** the deviatoric probe that breaks the σ_s0/η0 degeneracy | High |
| E9 | Three-axis shrinkage + green density vs build-plate position and build height | CMM / structured light | Anisotropy and sedimentation gradient. Single-axis push-rod dilatometry **hides this entirely**. | High |
| E10 | Raman D/G speciation of residual carbon on interrupted coupons | Raman | What 200 ppm physically means | Medium |
| E11 | Permeability rig on partially debound discs | Custom | Validates Kozeny-Carman prefactor and K_z/K_xy | Medium (gated) |
| E12 | Blind validation part — geometry and thickness not used in calibration | CT / CMM | The actual validation | **Critical** |

**Reference-material control (do this first, it substantially derisks both project and paper):** run the entire pipeline on a well-documented system — a commercial copper MIM feedstock, or an alumina LCM slurry with a published Lithoz cycle — before pointing it at a material whose binder you cannot see.

**Statistics:** n ≥ 3 replicates for any claimed number. Single specimens are not results. Randomised position map with furnace position as a recorded factor, because uniformity is not perfect.

---

## 7. Roadmap and gates

| Phase | Weeks | Deliverable | Gate |
|---|---|---|---|
| **P0 Baseline** | 0–1 | Cycle Card v0 in the furnace; T0 + T1 screener end-to-end; verification suite in CI; exhaust-gas observer ordered; NDA ask-list sent | T1 reproduces (a) CEA's mass-loss trace within 25 %, (b) IFAM's 87 h air debind as a solution of the ΔT < 20 K constraint, (c) IBM's 785 °C setpoint at 5.8× reducing margin. **Hard check: can the furnace actually make humidified low-H₂ gas?** If not, buy bubbler + heated line + premixed cylinder now (~8 k€, cheapest capability purchase in the project). |
| **P1 Fingerprint & fork** | 1–4 | Populated feedstock state card; k_eff and ΔH_c measured; both fork arms run; blank-corrected kinetics; h measured; **real parts out of the furnace** | ≥1 topology gives crack-free ≥5 mm coupons at >88 % density and <500 ppm C. Three binder-content routes agree to 0.5 wt%. *Fallback: run the IFAM recipe verbatim as a control and diagnose the difference — that comparison is itself a result.* |
| **P2 Calibrate & optimise** | 4–12 | Dilatometry + deviatoric probe; identifiability report; 1-D model validated on the thickness ladder; chance-constrained Cycle Card v2 + Pareto front | v2 beats v1 on real parts across (time, density, C, O) with no new defect mode, at <60 % of baseline time. **The optimiser's active-constraint story must match what the metrology says nearly failed.** If they disagree, fix the model — do not add a discrepancy term. CI enforces this. |
| **P3 Distortion & geometry** | 12–22 | MOOSE+NEML2 3-D; three-orientation shrinkage factors; compensated STL for one real component | Shrinkage within 0.5 pp on each axis; distortion RMS within 100 µm on a 40 mm part the model never saw. Verification suite still passes unchanged. |
| **P4 Robustness & publication** | 22–34 | Scenario-based re-solve; retort loading study; two papers submitted | — |

**If the E6 interrupted ladder shows carbon still present at pore closure, the project pivots** to a reformulation conversation with Lithoz rather than continuing to optimise a cycle that cannot exist. That is the one gate that changes the project rather than the parameters.

---

## 8. Software stack

| Need | Choice | Why |
|---|---|---|
| ROM + optimiser | **CasADi 3.6 + IPOPT (HSL MA57)** | Exact 1st/2nd derivatives on the same graph the sampler uses; multi-phase collocation is native |
| Inference | **NumPyro** (or PyMC) + ArviZ | NUTS on a stiff DAE; hierarchical lot effects |
| Sensitivity / triage | **SALib** (Morris, Sobol) + active subspace | Runs before furnace hours are spent |
| Surrogates / chance constraints | **ChaosPy** sparse PCE; **BoTorch/Ax** for OED | Analytic constraint moments in-loop |
| Thermochemistry | **Cantera** + hand-coded Gibbs fits; `pycalphad` if CALPHAD needed | JAX/CasADi-traceable so it composes into T0 |
| 3-D FEM | **MOOSE** (upstream `idaholab/moose`) + **NEML2** | Only mature open stack with a sintering constitutive path; `pyzag` for adjoint calibration |
| TGA kinetics | **pkynetics** + our own Simha-Wall reference | ICTAC-compliant isoconversional; the reference is the CI test |
| Meshing / geometry | gmsh, PyVista, trimesh | Compensation loop |
| Data / provenance | **pydantic v2 + pint + DVC**, HDF5 | Every field is (value, σ, provenance) |
| Verification | pytest + closed-form Sandia SOVS free-sintering and sinter-forge solutions, bilayer bar | In CI from day one, before any calibration |

**Reference codebases already cloned and inspected during the research:** `hpsint`, `refrasin`, MALAMUTE, NEML2, `pyzag`, `pkynetics`, PUMA. None is adopted wholesale — MOOSE upstream plus vendored NEML2 is the recommendation, with PUMA kernels lifted as *patterns*, not as a dependency.

**Two governance mechanisms that are cheap and disproportionately valuable:**

- **`docs/provenance_policy.md`** — every parameter tagged MEASURED / ANALOGUE / DERIVED / GUESS, with a `verified: yes|no` flag. Unverified literature numbers are **automatically promoted to wide priors** rather than entering as fixed constants. CI fails if a GUESS-tagged parameter appears in the top-5 Sobol indices of an active constraint. This makes epistemic honesty machine-checkable instead of aspirational — and it matters here, because several numbers the whole field relies on are single-sourced.
- **`docs/escalation_policy.md`** — numeric, **pre-registered** triggers for when a demoted term comes back: `d50 < 6 µm` re-enables the Darcy branch; measured `ΔT_core−surface > 30 K` escalates lumped → 1-D; shrinkage anisotropy > 1.5 pp escalates to 3-D; `P_tot < 200 mbar` switches transport off Darcy+Klinkenberg (Kn = 0.48 at 50 mbar — firmly transitional, so the vacuum branch of a naive optimiser runs on an invalid transport law); any exhaust CO above baseline under inert gas re-enables the carbothermic channel.
  Pre-registering **model complexity**, not just acceptance criteria, is what turns a modelling paper from a post-hoc story into a test — and it is the answer to the referee who asks "why did you delete that term?"

---

## 9. Risk register

| Risk | Severity | Mitigation |
|---|---|---|
| **Carbon still present at pore closure** — the cycle cannot exist | Fatal | E6 interrupted ladder, week 6. Pivot to reformulation with Lithoz rather than optimising an impossible cycle. |
| **k_eff is 10 W/mK, not 1** — the flux-limited thesis degrades to "above ~2 mm" | High | E2 laser flash, week 1. Cheap, decisive, and the claim is stated conditionally until it lands. |
| **Phosphorus from BAPO initiator** — Cu–Cu₃P eutectic at 714 °C, liquid phase mid-debind | High | ICP for P, Ge, Sn, S in E0. If P present it becomes a hard cycle constraint and possibly grounds to request a reformulated initiator. |
| **Aromatic dye as char precursor** — published copper VPP results may not transfer | High | Py-GC-MS at 620 °C. State the caveat in the paper up front. |
| **Hydrogen embrittlement / blistering** | High | Ordering constraint (reduce while open-porous), not a Darcy constraint. Throttle pO₂ during debind so bulk oxide never forms. Cap x_H2 at 4 %. |
| **Incipient melting at the 1066 °C eutectic** with incompletely deoxidised copper | High | Solidus-based ceiling (§1.5b). Verified sub-100 ppm O gate before exceeding 1000 °C. Baseline caps at 1040 °C. |
| **De-densification / bloating** from late CO or H₂O in closed pores | High | Pore-gas back-pressure in σ_s,eff. Look for the shrinkage plateau or reversal in dilatometry rather than smoothing it away. |
| **Second slurry lot with different binder** voids every identified parameter | High | Single-batch confirmation in writing + sealed retained sample + hierarchical lot random effect in the model. |
| **Printing not derisked** — no vat parameter set, no 450 nm working curve, Cu sedimentation | High | Flood-cured silicone-mould coupons decouple the feedstock campaign from the printer entirely. |
| **Copper vapour contaminating the furnace** | Medium | **Reject vacuum sintering** — Cu vapour pressure near 1080 °C gives µm/h free-surface recession and condensation onto elements and insulation. Use inert/reducing backfill at ≥ a few mbar. Prefer a separate debinding furnace. |
| **Brown-body pyrophoricity** — fine porous Cu with high SSA can self-heat on first air exposure | Medium | Inert transfer, or a controlled low-pO₂ passivation step before opening the furnace. |
| **Oxygen pickup between steps** as an unexplained scatter source | Medium | Enforced inert transfer/storage, logged exposure time per sample, and a deliberate exposure-time experiment to quantify the rate. |
| **Binder tar destroying elements and insulation** | Medium | Cold/tar trap. Binder tar plus hydrogen is a genuine deposit hazard. |
| **NDA blocks publication late** | Medium | Negotiate terms before the first experiment. Method-plus-case-study framing survives redaction. |

**Safety — not a line item, a plan with lead time.**
Hydrogen requires DSEAR/ATEX-equivalent assessment, gas detection, purge interlocks and a burn-off stack. **Binder pyrolysis produces carbon monoxide — odourless and lethal — so CO detection in the furnace room is mandatory.** Uncured slurry contains skin-sensitising acrylates and photoinitiators requiring specific PPE and waste routes. Brown-body pyrophoricity as above. None of this is optional for institutional approval.

---

## 10. The paper

**The contribution is the modelling and identification methodology, with this slurry as the case study.** That framing survives redaction, and it is also the honest description of what is new. "We sintered copper by vat photopolymerisation" is not a contribution — Incus and CEA-LITEN have published that.

**Paper 1 — process/method.** *Coupled oxygen-in / oxygen-out optimal control of debinding and sintering for lithography-based copper.* Core claims, all falsifiable and all registered in advance:
1. Oxidative debinding of metal-filled photopolymers is heat-removal and O₂-flux limited, not kinetics limited — with the zero-parameter design law and the thickness-ladder data that tests it.
2. Consequently the optimal debind is near-isothermal with pO₂ as the throttle, and the staircase of isothermal holds currently shipped is provably suboptimal — quantified against the 156 h reference.
3. The atmosphere topology is a *finding* from the outer enumeration, not an assumption.

**Paper 2 — data/materials.** σ_t(T, α) hot green strength with build-orientation anisotropy for a metal-filled photopolymer (does not exist); the 450 nm working curve for a copper slurry; the first master sintering curve for pure copper from this route; core-vs-surface temperature during pyrolysis; and the residual C/O → %IACS correlation. **Include the conductivity endpoint** — that correlation is the result a reader actually wants, and it converts a process study into a materials paper.

**Possible Paper 3 — model-predictive debinding from real-time evolved-gas analysis.** Genuinely unpublished for any AM metal system, and probably the strongest methods paper the project could produce.

**A named, reusable protocol worth publishing on its own:** the two-stage Ar→air-switched TGA with a matched bare-metal blank, plus the code-level guard that refuses to compute conversion from an unpaired air-TGA of an oxidisable filled feedstock. Small, real, and highly citable.

**What a referee will demand, minimum:** multi-rate isoconversional analysis with a blind held-out rate; an identifiability statement (**never report a standalone σ_s0** — free-sintering dilatometry identifies only the ratio σ_s0/η0, condition number ~10¹⁴–10¹⁶); blind validation on a geometry not used in calibration; uncertainty quantification on every predicted quantity; and full deposition of data, code and identified parameters in a citable repository.

Targets: *Additive Manufacturing*, *Journal of Materials Processing Technology*, *Journal of the European Ceramic Society*, *Thermochimica Acta* (for the protocol note).

---

## 11. Decisions needed before anything is built

1. **Furnace capability — audit before planning.** Do you have (a) an H₂-rated retort with interlocks, (b) **dew-point control hardware: a bubbler and a dew-point meter**, (c) 1100 °C with ±5 °C uniformity across the load *measured by survey, not trusted*, (d) a tar trap, (e) ideally a separate debinding furnace? If (b) is missing, nothing in §4's atmosphere optimisation is executable and it should be bought in week 1 (~8 k€). Is the dilatometer atmosphere-capable and H₂-rated? Note that typical push-rod loads of 20–50 cN will creep a weak brown body and produce false shrinkage — **contactless optical dilatometry is strongly preferred** for the debound state.

2. **Scope: cycle, or cycle + distortion compensation?** The T5 3-D layer roughly doubles the project. If dimensional accuracy on real geometry is a deliverable it must be in from the start (it changes the experiment matrix — E9, three-axis shrinkage, blind validation part). If the goal is dense, crack-free copper, T0–T4 suffices and the roadmap ends around week 12.

3. **How hard do we push Lithoz?** The NDA ask-list costs nothing scientifically and could remove months. Is there an existing agreement, and who owns that conversation? Related: are publication terms already settled?

4. **How much slurry is there, and is it one batch?** This is the binding resource. The campaign in §6 needs to be sized against the actual quantity, with a reserve held for the demonstrator and a sealed retained sample.

5. **Powder D50 — do we know it, and can we get it from Lithoz?** It flips one architectural decision outright: at 16 µm the Darcy pressure branch is deleted; below 6 µm it is re-enabled and the model gets meaningfully more expensive.

6. **Who builds what?** T0–T4 is a strong Python engineer plus a materials scientist. T5 needs someone who can write MOOSE/NEML2 constitutive models — that is a distinct and scarce skill. Who is hydrogen-trained? Where is LECO run and what is the turnaround?

7. **Is a reference-material control acceptable?** Running the full pipeline first on a commercial Cu MIM feedstock or an alumina LCM slurry with a published cycle costs perhaps three weeks and substantially derisks both the project and the paper. I recommend it.

---

## Appendix — what this proposal is built on

`docs/research/` contains 27 verbatim agent reports:

- **10 recon + 10 deep-dive** reports across Lithoz hardware and copper LMM, binder reverse-engineering, TGA kinetics, debinding transport and defects, Cu–O–C–H thermochemistry, sintering constitutive models, copper sintering data, inverse/UQ/optimal control, software stack, and validation/publication landscape.
- **3 competing architectures**, written to deliberately opposed design biases (physics-first multiscale; inverse-problem-first uncertainty-native; pragmatic time-to-first-part).
- **3 adversarial design reviews** under physical-correctness, feasibility and novelty lenses. These reviewers independently recomputed the load-bearing numbers and caught, among other things, a 4.8-decade error in one architecture's headline pressure result, an infeasible path constraint shared by two of them, and the missing carbothermic reaction shared by all three.
- **1 completeness critique**.

Scores: physics lens 6.5 / 5.5 / 4.5; feasibility 7 / 5 / 2; novelty 7 / 5 / 3.5. The synthesis takes the pragmatic architecture's execution spine, the inverse-first architecture's intellectual core, the physics-first architecture's exhaust-gas observer and event-constraint formulation, and repairs every fatal flaw the reviewers identified.

Where this document and a research report disagree, this document is the corrected version — the reports are preserved verbatim, errors included, because the disagreements are themselves informative.
