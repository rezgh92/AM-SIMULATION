# Materials-data dossier: Paper 3 (Cu co-fired with a cordierite-type glass-ceramic by multi-material VPP)

**Compiled:** 2026-09-24. **Scope:** numbers needed to parameterise a simulation-only paper on co-firing copper with an IBM-lineage cordierite-type glass-ceramic.

## How to read this file

Every number below was read in a source during this session. Nothing was recalled from memory. Each DOI was resolved against the Crossref REST API (`api.crossref.org/works/<DOI>`) on 2026-09-24, and title, journal, volume and pages match Crossref. Patents were read in full text on Google Patents. Datasheets were read as PDFs. When a number could not be found in a source that was actually read, it is marked **NOT FOUND**.

**Verification levels** (last-but-one column of each table):

| Code | Meaning |
|---|---|
| **FT** | DOI verified in Crossref; value read in the open-access full text (PDF or HTML). |
| **AB** | DOI verified in Crossref; value read in the abstract (from Crossref or the IBM Research publication page). |
| **PT** | Patent full text (Google Patents HTML). No DOI; the patent number was checked by reading the patent. |
| **DS** | Manufacturer datasheet or web page, read directly. No DOI. |
| **SN** | DOI verified, but the value comes only from a search-engine rendering of the publisher abstract. The page itself was blocked (IEEE Xplore, ScienceDirect, Wiley). **Weak. Re-check before citing a number.** |
| **D** | Derived in this dossier from a sourced equation or constant (arithmetic only). The source equation is cited; the derived number is not in the source. |

Quotes are verbatim from the extracted text. Patent and PDF text extraction damages some notation. For example, "10 -4" means 10⁻⁴, "H 2 /H 2 O" means H₂/H₂O, "×10 7 /°C." in US 4,301,324 means ×10⁻⁷/°C (the minus sign was lost), and "⬚C" in the IBM JRD PDF means °C. Where a quote carries such an artefact, the correct reading is given in the "value" column.

---

## 1. Cordierite-type (MgO–Al₂O₃–SiO₂ ± B₂O₃/P₂O₅) glass powders

### 1.1 Compositions and particle size (the IBM glasses)

| Parameter | Value (units) | Conditions | Source | Verif. | Exact quote |
|---|---|---|---|---|---|
| IBM "Glass #12" composition | SiO₂ 52.5, MgO 22.0, Al₂O₃ 22.0, P₂O₅ 1.5, B₂O₃ 0.5, ZrO₂ 1.5 (wt%) | Glass used in the Cu co-fire examples | Herron, Master, Tummala, US 4,234,367 (1980) | PT | "Composition (by weight percent) of Glass Formulation #12: … SiO.sub.2 52.5 P.sub.2 O.sub.5 1.5 MgO 22.0 B.sub.2 O.sub.3 0.5 Al.sub.2 O.sub.3 22.0 ZrO.sub.2 1.5" |
| Cordierite-type composition range | SiO₂ 48–55, Al₂O₃ 18–23, MgO 18–25, ZnO 0–2, Li₂O 0–1, B₂O₃ 0–3, P₂O₅ 0–3, TiO₂ 0–2.5 (wt%); SnO₂ + ZrO₂ limits in the table | Patent Table I | Kumar, McMillan, Tummala, US 4,301,324 (1981) | PT | "COMPOSITION RANGES (WEIGHT PERCENTAGES) β-Spodumene Type Cordierite Type … SiO.sub.2 65 to 75 48 to 55 Al.sub.2 O.sub.3 12 to 17 18 to 23 MgO 0 to 2 18 to 25 …" |
| Alternative IBM glass | SiO₂ 55.00, MgO 20.00, Al₂O₃ 21.23, P₂O₅ 2.77, B₂O₃ 1.00 (wt%) | Glass used in the flattening patent | Dubetsky, Herron, Master, US 4,340,436 (1982) | PT | "SiO 2 --55.00 MgO--20.00 Al 2 O 3 --21.23 P 2 O 5 --2.77 B 2 O 3 --1.00" |
| Stoichiometric cordierite glass (reference) | SiO₂ 51.3, Al₂O₃ 34.9, MgO 13.8 (wt%) | Glass for which the VFT fit in §1.3 holds | Reinsch, Nascimento, Müller, Zanotto 2008, *J. Non-Cryst. Solids* 354, 5386–5394, doi:10.1016/j.jnoncrysol.2008.09.007 | FT | "nominal composition of cordierite (in wt%): 51.3 SiO2, 34.9 Al2O3 and 13.8 MgO" |
| Glass powder mean particle size | 2–7 µm | Tape-cast green sheets | US 4,301,324 | PT | "The average particle size for the glass powder should be in the range of 2 to 7 μm for good sintering and strength." |

**Caution.** IBM Glass #12 is MgO-rich and Al₂O₃-poor compared with stoichiometric cordierite (22/22/52.5 against 13.8/34.9/51.3 wt% MgO/Al₂O₃/SiO₂). Viscosity and Tg for stoichiometric glass (§1.2–1.3) are therefore stand-ins, not IBM-glass data.

### 1.2 Glass transition, softening and coalescence temperatures

| Parameter | Value (units) | Conditions | Source | Verif. | Exact quote |
|---|---|---|---|---|---|
| Tg, stoichiometric cordierite glass | 1083 K (≈810 °C) | Table value, "measured by DSC or … Sciglass database" | Fokin, Nascimento, Zanotto 2005, *J. Non-Cryst. Solids* 351, 789–794, doi:10.1016/j.jnoncrysol.2005.02.005 (Table 1, citing Reinsch's 2001 thesis) | FT (checked on the page image) | Table 1 row: "Cordierite (2MgO·2Al2O3·5SiO2) 1083 1643 0.659 9 × 10⁻⁶ 1523 [19]" (columns: Tg (K), Tm (K), Tg/Tm, Umax (m/s), T at Umax (K)) |
| Tg definition used in the VFT fit | η(Tg) = 10^12.3 Pa s; dilatometric Tg at 5 K/min | Stoichiometric cordierite glass | Reinsch et al. 2008 | FT | "Tg was determined by a horizontal dilatometer (heating rate 5 K/min, Netzsch 402 E)"; "at their respective Tg (10^12.3 Pa s)" |
| Tg of a near-cordierite MAS glass (perlite tailings, 1.24 wt% Na₂O) | 806.6 °C | DSC. Table 3 is taken from Fig. 1, which is at **30 °C/min**; the methods section says Tg was found at 10 °C/min, so the rate is ambiguous | Wang et al. 2026, *Materials* 19, 1348, doi:10.3390/ma19071348 | FT | Table 3: "x = 0.0 \| 806.6 \| 948.8 \| 970.1 \| 1031.6" (Tg, To, Tp1, Tp2 in °C) |
| Tg of a tuff-derived MAS glass | ≈909 °C (909.76, 908.39, 909.43) | DSC at 10 °C/min in N₂ | Yu et al. 2022, *Materials* 15, 8758, doi:10.3390/ma15248758 | FT | "The Tg of the three basic glasses was substantially the same, about 909 °C." **Flag:** the same paper sinters to 2.62 g/cm³ at 875–900 °C, below this "Tg". Treat as doubtful. |
| Tg, IBM Glass #12 | **NOT FOUND** | — | — | — | — |
| Bounds for the IBM glass | annealing point < 785 ± 10 °C < softening point | Burnout hold is placed "between the anneal and softening points" | US 4,234,367, claim 1; US 4,340,436 | PT | "a burn-out temperature in the range between the anneal and softening points of said glass" |
| Dilatometric softening point, IBM glass | **NOT FOUND** (only the bound above) | — | — | — | — |
| Coalescence (onset of densification) of the IBM glass powder | ≈800–875 °C | Cu-compatible cordierite glasses | US 4,234,367 | PT | "the maximum temperature for binder removal is much lower due to the coalescence of the glass particulate at about 800° C.-875° C." |
| Onset of sintering required for a Cu-compatible glass | ≈800 °C | — | Herron, Kumar, Master, US 4,627,160 (1986) | PT | "The temperature limits imposed by the use of copper requires glass ceramics that begin to sinter at or near 800° C." |

### 1.3 Viscosity

| Parameter | Value (units) | Conditions | Source | Verif. | Exact quote |
|---|---|---|---|---|---|
| **VFT(H) fit, stoichiometric cordierite glass** | log₁₀(η/Pa s) = −3.97 + 5316 K / (T − 762 K) | Combined data: beam bending 10^12.3–10^9 Pa s, rotation < 10^5 Pa s, plus Giess & Knickerbocker (900 and 920 °C) and Yuritsyn | Reinsch et al. 2008, Eq. (1a) | FT (sign checked on the page image) | "log10(η/(Pa s)) = −3.97 + 5316 K/(T − 762 K) (cordierite)" |
| VFT-derived η at process temperatures | 800 °C: 1.3×10¹³; 825 °C: 7.0×10¹¹; 850 °C: 5.6×10¹⁰; 875 °C: 6.3×10⁹; 900 °C: 9.1×10⁸; 950 °C: 3.6×10⁷ Pa s. η = 10^12.3 Pa s at 816 °C | From Eq. (1a) | Reinsch 2008 Eq. (1a) | **D** | — |
| Temperature sensitivity, IBM cordierite-type glass | ≈1 decade of η per 40 °C (Fulcher form) | 800–860 °C isothermal sintering, air | Giess, Fletcher, Herron 1984, *J. Am. Ceram. Soc.* 67, 549–552, doi:10.1111/j.1151-2916.1984.tb19168.x | AB | "The temperature dependence of sintering followed that of the solid glass viscosity, which is described by the Fulcher equation using independently measured viscosity data. Viscosity decreased approximately an order of magnitude for every 40°C temperature increase." |
| Viscosity of MgO–Al₂O₃–SiO₂–B₂O₃–P₂O₅ cordierite-type glasses (IBM data) | **Values NOT READ.** The source exists and is the likely IBM-glass VFT source. | Parallel-plate viscometer, 900 and 920 °C (per Reinsch 2008) | Giess & Knickerbocker 1985, *J. Mater. Sci. Lett.* 4, 835–837, doi:10.1007/bf00720516 (Crossref spells the author "Geiss") | DOI only | — |
| Viscosity window that is too fluid for buried conductors | 10⁵–10⁸ poise (10⁴–10⁷ Pa s) at the sintering temperature | Reason IBM needed crystallising glasses | US 4,301,324 | PT | "the relatively high fluidity (viscosity of 10 5 to 10 8 poises) at the sintering temperature would result in excessive movement of the buried conductor patterns" |
| Crystallisation Ea compared with viscous-flow Ea | E_cryst ≈ ½ E_viscous | Powdered high-cordierite glass, DTA | Watanabe & Giess 1985, *J. Am. Ceram. Soc.* 68, doi:10.1111/j.1151-2916.1985.tb15307.x | AB | "The apparent activation energy for crystallization obtained from the DTA experiments was about half that for viscous flow estimated from the viscosity. Crystallization in such a system is believed to be controlled by a surface nucleation mechanism." |
| Fragility index m | **NOT FOUND** as a stated value. It can be computed from the VFT constants above (flag **D** if used). | — | — | — | — |

### 1.4 Sintering (densification) data

| Parameter | Value (units) | Conditions | Source | Verif. | Exact quote |
|---|---|---|---|---|---|
| Isothermal sintering temperatures; total linear shrinkage | 800, 820, 840, 860 °C; axial 0.12, diametral 0.17 | Uniaxially pressed pellets of crushed cordierite-type glass, air | Giess et al. 1984 | AB | "sintered in air at 800°, 820°, 840°, and 860°C … The total fractional shrinkage along axes was only 0.12, whereas that of diameters was 0.17." |
| Model fit | Frenkel fits until near full density; Mackenzie–Shuttleworth shows departure from ideality; an Avrami-type empirical fit covers the whole range | same | Giess et al. 1984 | AB | "Linear shrinkage obeyed the Frenkel viscous flow sintering model well, until complete densification was approached … A simple Avrami‐type equation permits an empirical fit of data for the entire sintering range" |
| Shrinkage anisotropy (axial/diametral) | 0.3 → ≈0.7 as density rises | Cylindrical pressed compacts | Exner & Giess 1988, *J. Mater. Res.* 3, 122–125, doi:10.1557/jmr.1988.0122 | AB | "the axial-to-diametral shrinkage ratio increases from a value of 0.3 to approximately 0.7 with increasing density" |
| Anisotropy for spheroidised powder | ≈0.7; spheroidising reduced the shrinkage rate | Isothermal, air | Giess, Guerci, Walker, Wen 1985, *J. Am. Ceram. Soc.* 68, doi:10.1111/j.1151-2916.1985.tb10136.x | AB | "Both jagged‐ and spheroidized‐particle compacts showed about the same 0.7 anisotropy of the ratio of axial to diametral shrinkage, but spheroidizing reduced the shrinkage rate." |
| Dense sintering before crystallising (IBM glass #10) | Negligible porosity at 850 °C with little crystallinity; satisfactory range 870–950 °C | Patent laminates | US 4,301,324 | PT | "composition #10 can be sintered to negligible porosity at a temperature of 850° C. but examination of the material fired to this temperature shows very little crystallinity in it." / "composition #10 can be satisfactorily sintered at temperatures within the range of 870° C. to 950° C." |
| Optimum sintering temperature, Glass #12 (and #10) | 950 °C (#12); 925 °C (#10) | Table III; hold 2 h (1–5 h allowed) | US 4,301,324 | PT | Table III "Sintering Temp. (°C.) 1050 960 925 925 950 967 …" (glasses #8, #9, #10, #11, #12, …); "The optimum holding time at the sintering temperature was two hours" |
| Heating and cooling limits | Heat ≤ 2 °C/min (1–2 °C/min for binder removal); cool ≤ 4 °C/min to 400 °C | Multilayer firing | US 4,301,324 | PT | "the heating rate should be low, not greater than 2° C./minute; faster heating rates resulted in incomplete binder burnout" / "A slow heating rate of 1° C. to 2° C. is essential" / "cooled at a conrolled rate not to exceed 4° C./minute to at least about 400° C." |
| Mechanism (single stage) | Glass-to-glass coalescence first, then surface crystallisation arrests viscous flow | Cordierite type | US 4,301,324 | PT | "(iv) the onset of surface crystallization following soon after the completion of densification providing a crystallized network that prevents further viscous deformation." |
| Onset of crystallisation (IBM glass, laminate) | ≈900 °C; full crystallisation hold ≈960 °C | US 4,340,436 glass | US 4,340,436 | PT | "between the end of the H 2 /H 2 O burn-out hold (e.g. about 780° C.) and before crystallization begins (about 900° C.)" |
| Race between sintering and crystallisation, stoichiometric cordierite glass | At 12 K/min only particles < 1 µm reach full density. Surface crystallisation starts at ≈1150 K and is complete at ≈1250 K, when densification stops. Radii tested: 1, 6.8, 8, 11 µm | Non-isothermal, narrow-sized jagged powder; Müller's data with Clusters-model simulation | Prado & Zanotto 2002, *C. R. Chimie* 5, 773–786, doi:10.1016/s1631-0748(02)01447-9 | FT | "at a heating rate of 12 K min–1, only particles smaller than 1 μm sintered to full density." / "Under these conditions, crystallization begins at ∼1150 K and is completed at ∼1250 K. At this point, densification is completely arrested." |
| Clusters model (sintering with concurrent surface crystallisation) | dρc/dt = (dρ/dt)(1 − αs), with αs = 1 − exp(−π Ns U² t²) (isothermal) | Input: η(T), γ, particle-size distribution, Ns, U(T), green density | Prado & Zanotto 2002 (Eqs. 6–7) | FT | "the JMAK 〚12〛 theory predicts the crystallized surface fraction, αs: αs = 1 − e^(−π Ns U(T)² t²)" … "dρc/dt = dρ/dt (1 − αs)" |

### 1.5 Crystallisation: DSC/DTA peaks, activation energy, Avrami exponent, phases

| Parameter | Value (units) | Conditions | Source | Verif. | Exact quote |
|---|---|---|---|---|---|
| **Overall crystallisation Ea, IBM-type high-cordierite glass with P₂O₅ + B₂O₃** | 303.5 kJ/mol (Marseglia/DTA); 301.9 kJ/mol (JMA from XRD) | Powdered glass, DTA at several heating rates | Watanabe & Giess 1994, *J. Non-Cryst. Solids* 169, 306–310, doi:10.1016/0022-3093(94)90327-1 | AB (IBM Research publication page) | "The overall activation energy of crystallization, 303.5 kJ/mol, of high-cordierite was computed by using Marseglia's equation based on DTA traces taken at different heating rates. This result is in fair agreement with that (301.9 kJ/mol) calculated using the Johnson-Mehl-Avrami equation" |
| Phase sequence (IBM-type glass) | Metastable high-quartz ss first, then high (α-) cordierite, then forsterite and protoenstatite at higher T | same | Watanabe & Giess 1994 | AB | "Metastable high-quartz, which has a structure similar to high-cordierite, appeared first. In addition to the main phase of high-cordierite, two other phases (forsterite and protoenstatite) appear with an increase in temperature." |
| Avrami exponent n, IBM glass | **NOT FOUND** (1994 abstract gives only Ea and the mechanism: surface nucleation, then volume-diffusion control) | — | — | — | "The rate-determining step … is concluded to be a volume diffusion process governed by the thin boundary layer produced at a glass-crystal interface following surface nucleation." |
| Crystallisation Ea, P₂O₅-modified cordierite-type glass | 469 kJ/mol | Static "thermal marking" experiments | Rudolph, Pannhorst, Petzow 1993, *J. Non-Cryst. Solids* 155, 273–281, doi:10.1016/0022-3093(93)91262-2 | **SN** | (search-engine rendering of the abstract: "an apparent activation energy of 469 kJ mol⁻¹ was obtained") |
| Kissinger Ek, B₂O₃-doped MAS glasses | 330.56 (S, stoichiometric); 332.06 (NS1); 412.12 (NS2); 417.86 (NS3) kJ/mol | DTA at 5, 10, 15, 20 °C/min; powder d₅₀ ≈ 5.9 µm | Sun et al. 2022, *J. Inorg. Mater.* 37, 1351, doi:10.15541/jim20220179 | FT | Table 2: "S 330.56 4.39×10^12 … NS1 332.06 3.54×10^12 … NS2 412.12 4.68×10^15 … NS3 417.86 8.05×10^15" |
| Kissinger and Ozawa E (α-cordierite peak); Avrami n (Matusita–Sakka) | E_K = 411.66, 403.36, 437.08, 326.81 kJ/mol; E_Ozawa = 432.86, 424.55, 458.00, 348.31 kJ/mol; n_avg = 3.16, 3.61, 3.71, 2.83 | x = 0, 0.3, 0.6, 1.1 wt% added Na₂O; DSC at 5, 10, 20, 30 °C/min | Wang et al. 2026 | FT | "the average Avrami exponent values (nave) for samples with varying Na2O additions are 3.16, 3.61, 3.71, and 2.83, respectively"; Table 4 "x = 0.0 \| 411.66 \| 432.86" |
| DSC peaks: μ- then α-cordierite | To 948.8, Tp1(μ) 970.1, Tp2(α) 1031.6 °C | x = 0; see the rate caveat in §1.2 | Wang et al. 2026 | FT | "the first exothermic peak corresponds to the crystallization of the metastable μ-cordierite phase, while the second exothermic peak corresponds to the crystallization of α-cordierite." |
| DSC Tp (tuff-derived) | 1006.22 / 1020.30 / 1028.33 °C | 10 °C/min | Yu et al. 2022 | FT | Table 3 "Tp (°C) \| 1006.22 \| 1020.30 \| 1028.33" |
| Width of the usable sintering window (IBM) | 80–100 °C, the span of the DTA exotherm | — | US 4,301,324 | PT | "satisfactory materials can be produced at sintering temperatures spanning 80°-100° C. covered by the exothermic peak in the thermograms of the corresponding glasses." |
| Crystal growth: maximum and shoulder | u(T) peaks at ≈1250 °C; shoulder at ≈970 °C (≈1.2 Tg) for μ-cordierite | Stoichiometric glass, 800–1350 °C | Reinsch et al. 2008 | FT | "The maximum of u(T) occurs at about 1250 °C for both systems. A smooth shoulder is observed around 970 °C for μ-cordierite." |
| Effect of water (relevant to steam burnout) | u at 945 °C rises from 0.2 to 0.6 µm/min as the dew point goes from −60 to +25 °C | μ-cordierite surface crystallisation | Reinsch et al. 2008 | FT | "u at 945 °C increased from 0.2 to 0.6 μm min⁻¹ for increasing air humidity (dew points between −60 and +25 °C)." |
| Umax; liquidus | 9×10⁻⁶ m/s at 1523 K; Tm 1643 K | Stoichiometric glass | Fokin et al. 2005 Table 1 | FT | see the Tg row in §1.2 |
| Growth maximum, bulk IBM-type glass | ≈1250 °C; morphology hexagonal-prismatic | Bulk glass with B₂O₃ + P₂O₅, 888–1363 °C | Watanabe, Giess, Shafer 1985, *J. Mater. Sci.* 20, 508–515, doi:10.1007/bf01026520 | AB (IBM Research page) | "The growth rate increased with temperature, and the maximum rate occurred at about 1250° C." |
| Phase selection in IBM glasses (μ vs α) | #9 (1 % Li₂O): μ only. #10 (2 % B₂O₃): α only. #12: α major plus clinoenstatite minor. ZrO₂ above a critical level promotes μ | US 4,301,324 Table III glasses | US 4,301,324 | PT | "Composition #9 contains μ-cordierite as the only crystalline phase." / "Composition #10 contains only α-cordierite due, it is believed, to the presence of boric oxide" / "Composition #12 … develops α-cordierite as the major crystal phase together with clinoenstatite as a minor phase." |
| Crystalline fraction after firing | > 80 vol% | IBM glass-ceramics | US 4,301,324 | PT | "the crystalline phases formed occupy greater than 80% of the body by volume." |
| Microstructure scale | Crystal network at the prior-particle scale (2–5 µm) with 1–2 µm secondary crystals | — | US 4,301,324 | PT | "a cellular network of crystals on the scale of the prior glass particle dimensions (2-5 μm), forming the first level within which are formed discrete crystals of sub-micron to 1-2 μm size" |

### 1.6 Fired glass-ceramic properties

| Parameter | Value (units) | Conditions | Source | Verif. | Exact quote |
|---|---|---|---|---|---|
| CTE design target | 20–40 ×10⁻⁷/°C, preferably ≈30 ×10⁻⁷/°C (20–300 °C) | Patent requirement | US 4,301,324 | PT | "the thermal expansion coefficient, measured in the temperature range of 20°-300° C., of the glass-ceramic to be in the range of 20 to 40×10 -7 /°C. and preferably to be close to 30×10 -7 /°C." |
| CTE, Glass #12 (air-fired) | 23–24 ×10⁻⁷/°C | Sintered 915–970 °C | US 4,301,324 | PT | "For sintering temperatures between 915° C. and 970° C., the expansion coefficient only varied for 23×10 7 /°C. to 24×10 7 /°C." (read ×10⁻⁷) |
| CTE, Glass #12 (H₂/H₂O-fired) | 18 ×10⁻⁷/°C | After the Cu co-fire cycle | US 4,234,367 | PT | "TCE (Thermal coefficient or expansion)=18×10 -7 /° C." |
| **CTE, production HPGC substrate** | **3.0 ppm/°C** (Si: 2.6 ppm/°C) | IBM p690 "Regatta" MCM | Knickerbocker et al. 2002, *IBM J. Res. Dev.* 46, 779–804, doi:10.1147/rd.466.0779 | FT (archived IBM PDF) | "(CTE of HPGC substrate = 3.0 ppm/°C)"; "[coefficient of thermal expansion (CTE) of 2.6 ppm/°C]" |
| CTE, ES/9000 substrate | 30 ×10⁻⁷/°C | 1992 IBM JRD abstract | Tummala et al. 1992, *IBM J. Res. Dev.* 36, 889–904, doi:10.1147/rd.365.0889 | **SN** | "The thermal expansion of the new substrate (30 ×10⁻⁷°C⁻¹) is matched with that of the silicon chips" |
| **Dielectric constant** | 5.0 at 1 kHz (Glass #12, H₂/H₂O-fired); 5.1 (2002 HPGC); 5.0 vs 9.4 for alumina (1992) | — | US 4,234,367; Knickerbocker 2002; Tummala 1992 | PT; FT; SN | "K Dielectric Constant=5.0 (at 1000 Hz)"; "low dielectric constant of 5.1 compared to that of alumina, which is about 9.8" |
| **Flexural strength (MOR)** | 210 MN/m² = 210 MPa (Glass #12, H₂/H₂O-fired); 82,300 psi ≈ 567 MPa (Glass #12, air-fired, patent Table III, 3-point bend, mean of 10) | — | US 4,234,367; US 4,301,324 | PT | "Modulus of Rupture=210MN/m 2"; Table III "Modulus of Rupture (psi) 30,500 42,300 29,000 42,300 82,300 …" (5th entry = #12). **Flag:** the two patents differ by 2.7×. Use 210 MPa for the Cu-co-fired material. |
| Permittivity, Table III of US 4,301,324 | 5.3–5.7 (1 MHz) | Row has only 9 values for 12 glasses, so values cannot be assigned to glasses reliably | US 4,301,324 | PT | "Permittivity (k) 5.6* 5.7** 5.3* 5.4* 5.7* 5.6* 5.6* 5.7* 5.5*" |
| **Young's modulus, IBM glass-ceramic** | **NOT FOUND** | — | — | — | — |
| **Poisson's ratio, IBM glass-ceramic** | **NOT FOUND** | — | — | — | — |
| **Density, IBM glass-ceramic** | **NOT FOUND** | — | — | — | — |
| Analogue: dense α-cordierite GC (tuff) | ρ 2.62 g/cm³; σ_f 136 MPa; ε 5.12 (10 MHz); CTE 3.89 ×10⁻⁶/K | Sintered 900 °C, 6 h | Yu et al. 2022 | FT | "high densify (2.62 g∙cm−3), applicable flexural strength (136 MPa), … low dielectric constant (5.12, at 10 MHz …), and suitable coefficients of thermal expansion (CTE, 3.89 × 10−6 K−1)." |
| Analogue: porous α-cordierite GC | E 34.0 ± 2.9 GPa; σ_f 42.4 MPa; ρ 1.53 g/cm³ (**40.9 % apparent porosity**) | Not representative of dense substrates | Sun et al. 2022 | FT | "(42.4±3.0) MPa, (34.0±2.9) GPa, (0.7±0.15) MPa·m1/2, and 1.53 g/cm 3" |
| Analogue: commercial Cu-co-fired LTCC (Kyocera GL570) | E 128 GPa; σ_f 200 MPa; CTE 3.4 ppm/K (RT–400 °C); ε 5.6 (1 MHz), 5.7 (2 GHz); k 2.8 W/m·K; co-fired conductor Cu | Web table, "representative values" | Kyocera "Material Properties" page (global.kyocera.com/prdct/semicon/material/), read 2026-09-24 | DS | Table columns GL570/GL580/GL773: "5.6 \| 6.2 \| 5.7" (ε, 1 MHz); "3.4 \| 10.4 \| 11.7" (CTE); "200 \| 270 \| 280" (flexural, MPa); "128 \| 103 \| 95" (Young's, GPa); "Cu \| Cu \| Cu" |

---

## 2. IBM glass-ceramic/copper multilayer substrate: process conditions

| Parameter | Value (units) | Conditions | Source | Verif. | Exact quote |
|---|---|---|---|---|---|
| **Burnout ramp, atmosphere, hold** | 1–3 °C/min in H₂/H₂O to 785 ± 10 °C; hold 3–5 h; then N₂ with a 0.5 h hold to drive off H₂O | Glass #12 laminates with Cu paste | US 4,234,367 | PT | "heating a laminated assembly of green glass-ceramic layers, with an internal copper forming pattern in a H 2 /H 2 O ambient at a rate of 1° to 3° C. per minute to a burn-out temperature of 785±10° C., holding for 3-5 hours to burn out the polymeric material, followed by changing the ambient to nitrogen, N 2 , with about a 0.5 hour hold to remove entrapped or dissolved water" |
| **H₂/H₂O ratio** | Ramped from 10⁻⁶ at 400 °C to 10⁻⁴ at the burnout temperature (claims: 10^-6.5 to 10^-4), or held at 10⁻⁴ in the simplified cycle | — | US 4,234,367 | PT | "the H 2 /H 2 O ratios of the ambient are changed continuously from 10 -6 at 400° C. to 10 -4 at the burn-out temperature." / "This requires that only one specific ratio (e.g. 10 -4 ) of the H 2 /H 2 O be used at a firing temperature of 785±10° C." |
| **Sintering / crystallisation** | N₂, 1–3 °C/min to 930–970 °C, 2 h hold | — | US 4,234,367 | PT | "with subsequent heating in nitrogen at a rate of 1°-3° C./min. to a sintering temperature of about 930° to about 970° C. with a 2 hour hold at this temperature." |
| Full worked schedule (Glass #12) | N₂ at 2.15 °C/min to 200 °C → H₂/H₂O 10^-6.5 → 450 °C → 2.9 °C/min to 780 °C → ≈6 h hold (ratio raised to 10⁻⁴) → N₂ 0.5 h → 2.1 °C/min to ≈960 °C, 2 h → cool ≈3.8 °C/min | — | US 4,234,367 | PT | "the green-laminate is preheated at a rate of 2.15° C./min. in a nitrogen ambient … to a temperature of about 200° C. At this point the nitrogen is replaced with a H 2 /H 2 O ambient in a volume ratio 10 -6 .5. … After about 6 hours at the 780° C. hold temperature, the H 2 /H 2 O ambient is switched to a nitrogen ambient … heating is again elevated at a rate of 2.1° C./min. to the crystallization temperature of the glass, (e.g. about 960° C. for the Glass #12 ), which temperature is held for about 2 hours, after which the temperature is reduced to ambient at a rate of about 3.8° C./min." |
| Why the hold is at 785 °C, not 750 or 830 °C | 750 °C: carbon removal too slow. 830 °C: pores close and trap water and residue | Glass #12 | US 4,234,367 | PT | "too low a temperature (e.g. 750° C.) would take prohibitively excessive amounts of time for carbon removal, whereas too high a hold temperature (e.g. 830° C.) will trap water and binder residue when the glass pores close." |
| **Why burnout must finish before glass sintering** | Carbon trapped after coalescence reacts with water rejected during crystallisation; the part bloats or bursts | — | US 4,234,367 | PT | "after the glass has coalesced, any remaining binder residue will become entrapped in the glassy body." / "As the dissolved water is being rejected during glass-crystal growth, (after pore closure), it will subsequently oxidize retained carbon to form carbon oxides and hydrogen causing the substrate to expand or, in the worst case, burst." |
| Same rule, restated | — | — | US 4,627,160; US 4,301,324 | PT | "If the sintering phase, which reduces porosity, begins before the binder resin is completely removed, carbonaceous residues will be trapped in the substrate." / "the binder removal is essentially complete before appreciable glass-to-glass sintering has occurred." |
| PVB in inert gas | Not fully removed below 1150 °C | — | US 4,234,367 | PT | "the polyvinylbutyral binder has been found as not being easily burnt-out completely in a non-oxidizing ambient below 1150° C." |
| Binder loss in N₂ | Mostly complete by 700–800 °C (TGA and hot stage) | PVB | US 4,234,367 | PT | "in nitrogen, most of the binder degradation and/or removal occurs by about 700° to 800° C." |
| Glass crystallisation vs Cu melting point | Crystallisation 100–150 °C below the Cu melting point | Design rule | US 4,234,367 | PT | "wherein the temperature of crystallization of the glass is about 100° to 150° C. below the melting point of copper." |
| Lower-coalescence glass #10 | Burnout at 720 ± 10 °C | — | US 4,234,367 | PT | "which can be heated to 720°±10° C., for binder burn-out, due to its lower temperature of coalescence." |
| Cu resistivity after the H₂/H₂O cycle | 2.0 ± 0.2 µΩ·cm | ESL #2310 paste | US 4,234,367 | PT | "The resistivity obtained after firing in the H 2 /H 2 O ambient, was measured at 2.0±0.2 microhm-cm." |
| **Shrinkage anisotropy (Z vs X-Y)** | Unconstrained H₂/H₂O firing: Z ≈ ½ of X-Y | — | US 4,340,436 | PT | "Z direction (vertical) shrinkage for glass-ceramic substrates which is only about one half of the X-Y lateral directional shrinkage when fired in a H 2 /H 2 O ambient" |
| Z shrinkage under platen load | 10.96–14.77 % | Platen 0.8–4.0 g/cm² applied after an 825–875 °C abort | US 4,340,436 | PT | "% Z … 1V … 10.96 3V … 12.52 4V … 12.71 5V … 14.16 6V … 14.77 8V … 11.67 16V … 11.01" |
| **X-Y shrinkage, IBM glass-ceramic (number)** | **NOT FOUND** (given only in figures of US 4,340,436) | — | — | — | — |
| Share of shrinkage that happens during burnout | 33–50 % of total fired shrinkage | IBM MLC | Flaitz et al., US 5,130,067 (1992) | PT | "a good percentage (33-50%) of the total fired shrinkage and accompanying distortion, camber and via bulge, occurs during the binder burn-off step" |
| Zero-X-Y-shrinkage restraint pressure | 1–200 psi | Conformal co-sintering | US 5,130,067 | PT | "The restraining pressure applied is preferably in the range of 1-200 psi for MLC substrates" |
| Post-fire flattening | Crystallised cordierite GC (≈960 °C) does not flatten below 1100 °C, which is above the Cu melting point | — | US 4,340,436 | PT | "cordierite glass-ceramic substrates which crystallize at about 960° C. have shown little or no flattening below 1100° C." |
| Production scale | 63 layers (ES/9000, 1992); 70 layers, 85 mm MCM, TSM camber < 75 µm (2002) | — | Tummala 1992 (SN); Knickerbocker 2002 (FT) | SN; FT | "Generally, each of the 70 layers that make up the MCM substrate has a unique pattern."; Table 3 "TSM camber ⬍75 m" (read "< 75 µm") |
| Steam sintering described | Binder burnt off in steam (H₂O + H₂), then N₂ | — | Master, Herron, Tummala 1991, *IEEE Trans. CHMT* 14, 780–783, doi:10.1109/33.105133 | **SN** | (search rendering: "A steam sintering process based on sound theoretical principles has been developed") |
| Review article | No numbers in the abstract | — | Tummala 1991, *J. Am. Ceram. Soc.* 74, 895–908, doi:10.1111/j.1151-2916.1991.tb04320.x | AB | "Glass‐ceramic/copper substrate technology is discussed as an example of high‐performance ceramic packaging for use in 1990s." |

---

## 3. Commercial and Cu-compatible LTCC

| Parameter | Value (units) | Conditions | Source | Verif. | Exact quote |
|---|---|---|---|---|---|
| **DuPont 951: X,Y / Z shrinkage** | 12.7 ± 0.3 % (PT, P2, PX); 13.0 ± 0.2 % (C2) / 15 ± 0.5 % | Datasheet MCM951 (7/2011) | DuPont GreenTape 951 TDS | DS | "X, Y Shrinkage (%) … 12.7 ± 0.3 (951 PT, P2, PX) 13.0 ± 0.2 (951C2) … Z Shrinkage (%) … 15 ± 0.5" |
| DuPont 951: other properties | TCE 5.8 ppm/°C (25–300 °C); ρ 3.1 g/cm³; σ_f 230 MPa (4-pt); E 120 GPa; k 3.3 W/m·K; ε 7.8 (3 GHz) | — | same | DS | "TCE(25 to 300°C), ppm/ºC 5.8 Density (g/cm³) 3.1 … Flexural Strength, MPa (1) 230 Young's Modulus, GPa 120" |
| DuPont 951: lamination | 3000 psi, 70 °C, 10 min | — | same | DS | "Recommended parameters for lamination are 3000 psi at 70°C for 10 minutes." |
| **DuPont 951: belt firing profile (air)** | 25→60 °C at 2.5 °C/min; 60→400 at 19.2; 400→435 at 1.4; 435→850 at 7.0; 850 °C for 17 min; 850→40 at 17.3 °C/min | 3.5 h total | Wang, Hang, Needes, US 7,068,492 B2 (2006) | PT | "A typical LTCC belt furnace profile for 951 GREEN TAPE™ … includes: (1) 25° C. to 60° C. at 2.5° C./min, (2) 60° C. to 400° C. at 19.2° C./min, (3) 400° C. to 435° C. at 1.4° C./min, (4) 435° C. to 850° C. at 7.0° C./min, (5) dwell at 850° C. for 17 min, (6) 850° C. to 40° C. at 17.3° C./min" |
| **Ferro A6M/A6M-E** | X,Y 15.8 ± 0.3 %, Z 26.0 %; CTE 7.0 ppm/°C; ρ > 2.4 g/cc; σ_f 170 MPa; E 92 GPa; ε 5.7 (10 GHz); burnout RT→450 °C at < 2 °C/min, 2 h hold; fire 450→850 °C at 6–8 °C/min, 10–15 min hold, in air | Datasheet Nov 2015 | Ferro A6M/A6M-E TDS | DS | "Tape Shrinkage 15.8 ± 0.3 % X,Y 26.0 %Z"; "Binder Burn-out: Room temperature to 450oC at < 2oC/min, with 2 hour hold"; "Firing: 450 to 850oC @ 6-8oC/min, with 10-15 minute hold at peak" |
| Generic LTCC shrinkage | 10–15+ % in X-Y; ≈20 % in Z | Unconstrained | Girardi et al. 2009, *J. Microelectron. Electron. Packag.* 6, 114–118, doi:10.4071/1551-4897-6.2.114 | FT | "Standard, unconstrained LTCC firing shrinkage ranges from 10-15+% in the x and y directions to 20% in the z direction" |
| 951 shrinkage regression (PX tape, Au metal) | % shrinkage = 13.6269 − 0.005025 × (% metal loading) − 0.000344595 × (pressure) | DOE, isostatic lamination at 70 °C; pressure presumably in psi | Girardi 2009 | FT | "% firing shrinkage = 13.6269 −(0.00502500 · % metal loading) −(0.000344595 · pressure)" |
| ESL 41111-G data (for bilayer validation) | Green ρ 2020 kg/m³; sintered 2240 kg/m³; cycle 723 K for 3600 s in air, then 1123 K for 600 s at 0.083 K/s. At the start of the dwell, relative density 0.63 (constrained, simulated) vs 0.89 (free). Thickness shrinkage 28 % vs 21 %. η_uniaxial ≈ 8.7×10⁶ Pa s at 1023 K. Maximum camber 100.3 m⁻¹ at 1095 K | Bilayer of porous LTCC on dense LTCC | Chrétien et al. 2022, *Materials* 15, 6405, doi:10.3390/ma15186405 | FT | "A green density of 2020 ± 10 kg·m−3 and a bulk density of 2240 ± 10 kg·m−3"; "relative density at the beginning of the dwell at 1123 K of 0.63 vs. 0.89"; "The uniaxial viscosity (η) … is then 8.7 × 106 Pa·s"; "the camber reaches a maximum value of 100.3 m−1 at 1095 K" |
| **Cu-compatible glass-ceramic fired in N₂ + H₂O (Fujitsu)** | Burnout in N₂ with pH₂O 0.005–0.3 atm at 550–650 °C (example: 0.07 atm, 650 °C, 3 h), then dry N₂ at 900 °C for 1 h. Powder: Al₂O₃ 50.5, SiO₂ 35.0, B₂O₃ 13.0 wt% (+ alkali). ε 5.6; bending strength 2000 kg/cm² (≈196 MPa); PMMA binder | — | Kamehara, Kurihara, Niwa, US 4,504,339 (1985) | PT | "fired in an atmosphere of nitrogen containing water, the partial pressure of which was 0.07 atm, at 650° C. for 3 hours … the temperature was raised up to 900° C., which was maintained for 1 hour." / "a dielectric constant of the insulator layer of 5.6; and a bending strength of the substrate of 2000 kg/cm 2" |
| pH₂O window rationale | < 0.005 atm: incomplete burnout, porosity. > 0.3 atm: Cu oxidises. Implied H₂/H₂O (thermal decomposition at pH₂O = 0.3 atm): ≈10^-8.3 at 550 °C, ≈10^-7.2 at 650 °C | — | US 4,504,339 | PT | "If the partial pressure of water is higher than 0.3 atmosphere, the copper particles begin to oxidize"; "about 10 -8 .3 at 550° C., and about 10 -7 .2 at 650° C." |
| Shrinkage of a commercial Cu-in-N₂ LTCC | **NOT FOUND** (Kyocera GL570 gives properties but no shrinkage or firing data) | — | — | — | — |

---

## 4. Glass surface energy

| Parameter | Value (units) | Conditions | Source | Verif. | Exact quote |
|---|---|---|---|---|---|
| Surface tension, cordierite-type (IBM) glass | 0.36 N/m | Calculated from additive molar coefficients | Giess et al. 1984 | AB | "Surface tension calculated from published coefficients for the molar constituents was 0.36 N/m." |
| Surface tension, soda-lime-silica glass; effect of water | 0.315 J/m² (dry), falling to 0.205 J/m² at pH₂O = 16 mm Hg | 500–700 °C, fibre-elongation method | Parikh 1958, *J. Am. Ceram. Soc.* 41, 18–22, doi:10.1111/j.1151-2916.1958.tb13497.x | AB | "Water vapor was found to exhibit the most pronounced effect, causing a lowering from 315 to 205 dynes cm.−1 for a vapor pressure of 16 mm. Hg." |

**Note for the model.** The IBM burnout runs in steam. Parikh's result suggests the effective γ during a humid hold may sit 30–35 % below the dry value. That is an inference from a soda-lime glass and should not be stated as a cordierite measurement.

---

## 5. Copper thermomechanical data

| Parameter | Value (units) | Conditions | Source | Verif. | Exact quote |
|---|---|---|---|---|---|
| **Linear expansivity α(T)** | 10.3 (100 K), 15.2 (200 K), 16.5 (293 K), 18.3 (500 K), 20.3 (800 K), 23.7 (1100 K) ×10⁻⁶ K⁻¹ | Instantaneous expansivity (1/L)(dL/dT), not the mean | Kaye & Laby Online, §2.3.5 Thermal expansion, NPL (v1.1, 2010), archived at web.archive.org 2019-05-12 | DS (web table, no DOI) | Row "Copper \| 10.3 \| 15.2 \| 16.5 \| 18.3 \| 20.3 \| 23.7 \| –" under "α/(10−6 K−1) \| 100 K \| 200 K \| 293 K \| 500 K \| 800 K \| 1100 K \| 1500 K"; "In this section, expansivity data only are given." |
| RT CTE, E, melting point (OF Cu C10200) | CTE 17.6 ×10⁻⁶/K (at 20 °C); E 117 GPa; T_m 1083 °C; ρ 8.90 g/cm³ | Aurubis datasheet C10200 (18 08 US) | Aurubis | DS | "1083 8.90 0.394 58 391 117 17.6" (melting point °C, density, c_p, σ MS/m, k W/m·K, E GPa, CTE 10⁻⁶/K) |
| RT yield, soft (annealed) OF Cu | Rp0.2 nominal 69 MPa (10 ksi); Rm 179–262 MPa; elongation 35 % | Temper "Soft" | Aurubis C10200 | DS | "Soft … 26-38 [ksi] 10 [ksi] … 179-262 [MPa] 69 [MPa]" |
| **Shear modulus μ(T)** | μ(T) = μ₀ − D/(exp(T₀/T) − 1), with μ₀ = 51.3 GPa, D = 3.0 GPa, T₀ = 165 K | Varshni/MTS form fitted to Overton & Gaffney (1955) and Nadal & Le Poac (2003) data up to T/T_m ≈ 1 (Fig. 4a) | Banerjee 2005, arXiv:cond-mat/0512466 (no DOI) | FT (arXiv) | Table 3: "MTS shear modulus model … µ0 (GPa) D (GPa) T0 (K) … 51.3 3.0 165"; "The parameters for the MTS model have been chosen to fit the experimental data." |
| E(T) estimate | 117 (20 °C), 109 (200), 100 (400), 91 (600), 82 (800), 78 (900 °C) GPa | Assumes E/E_RT = μ/μ_RT, i.e. constant Poisson ratio | Aurubis E_RT × Banerjee μ(T) | **D** | — |
| Recommended E(T) and ν(T) (NIST) | **Values NOT READ.** srd.nist.gov returned HTTP 503 all session. | — | Ledbetter & Naimon 1974, *J. Phys. Chem. Ref. Data* 3, 897–935, doi:10.1063/1.3253150 | DOI only | — |
| Single-crystal C_ij above RT | **Values NOT READ** | 300–800 K | Chang & Himmel 1966, *J. Appl. Phys.* 37, 3567–3572, doi:10.1063/1.1708903 | DOI only | — |
| **Yield / flow stress vs T (model)** | Johnson–Cook: σ_y = [A + Bε_pⁿ][1 + C ln ε̇*][1 − T*^m], with A = 90 MPa, B = 292 MPa, C = 0.025, n = 0.31, m = 1.09, ε̇₀ = 1 s⁻¹, T₀ = 294 K, T_m = 1356 K | Annealed OFHC Cu, from Johnson & Cook 1985 | Banerjee 2005 (Table 4), citing Johnson & Cook 1985, *Eng. Fract. Mech.* 21, 31–48, doi:10.1016/0013-7944(85)90052-9 | FT (arXiv table); J&C paper not read | "Table 4: Parameters used in the Johnson-Cook model for copper (Johnson and Cook (1985)). A (MPa) B (MPa) C n m ˙ǫp0 (/s) T0 (K) Tm (K) 90 292 0.025 0.31 1.09 1.0 294 1356" |
| JC initial yield (ε_p = 0, 1 s⁻¹) | 90 (21 °C), 77 (200), 61 (400), 44 (600), 26 (800), 17 (900 °C), 8 MPa (1000 °C) | JC extrapolation | Johnson–Cook constants above | **D** | — |
| Warning on JC at low strain rate | JC overestimates quasi-static RT yield and under-predicts rate sensitivity at high T | — | Banerjee 2005 | FT | "The Johnson-Cook model overestimates the initial yield stress for the quasistatic (0.1/s strain-rate), room temperature (296 K), test." / "The strain-rate dependence of the yield stress is underestimated at high temperature (see the data at 1173 K in Figure 5(a))." |
| High-rate flow stress vs T (data) | (77 K, 380 MPa); (496 K, 300); (696 K, 230); (896 K, 180); (1096 K, 130 MPa); slope −0.25 MPa/K | 4000 s⁻¹, true strain 0.2 (Hopkinson-bar data); not a quasi-static yield | Banerjee 2005 | FT | "we get the following values of temperature and yield stress for a strain-rate of 4000/s: (77 K, 380 MPa); (496 K, 300 MPa); (696 K, 230 MPa); (896 K, 180 MPa); (1096 K, 130 MPa)." |
| **Quasi-static yield of annealed Cu at 600–900 °C (measured)** | **NOT FOUND** in an open primary source (see Gaps) | — | — | — | — |

---

## 6. Sintering, co-sintering and kinetics theory references

All DOIs below were verified in Crossref. "Content read" means the abstract (or full text) was read this session.

| Reference | DOI | Content read? | Key content (quote where read) |
|---|---|---|---|
| Frenkel 1945, *J. Phys. (USSR)* 9(5), 385 | none | Bibliographic data only, from Prado & Zanotto 2002 ref. [1] | Two-particle viscous coalescence. The linear-shrinkage form ΔL/L₀ = 3γt/(8ηr) is used in Prado & Zanotto 2002 (their C = 3γ/8r). |
| Mackenzie & Shuttleworth 1949, *Proc. Phys. Soc. B* 62, 833–852 | 10.1088/0370-1301/62/12/310 | Via Prado & Zanotto 2002 | Closed-pore stage: dρ/dt = (3γ/2a₀η)(1 − ρ) (simplified form, Prado & Zanotto Eq. 2a) |
| Scherer 1977 I–III, *J. Am. Ceram. Soc.* 60, 236–239 / 239–243 / 243–246 | 10.1111/j.1151-2916.1977.tb14114.x; …tb14115.x; …tb14116.x | I: AB | "An analysis is presented which describes the rate at which a cubic array of cylinders densifies by viscous flow driven by surface energy reduction." |
| Olevsky 1998, *Mater. Sci. Eng. R* 23, 41–100 | 10.1016/s0927-796x(98)00009-6 | No | Continuum theory of sintering |
| Bordia & Scherer 1988 I, II, III, *Acta Metall.* 36, 2393–2397; 2399–2409; 2411–2416 | 10.1016/0001-6160(88)90189-7; …90190-3; …90191-5 | No | Constitutive model, comparison of models, rigid inclusions |
| Bordia & Raj 1985, *J. Am. Ceram. Soc.* 68, 287–292 | 10.1111/j.1151-2916.1985.tb15227.x | AB | "the incompatibility stress is time dependent and reaches its maximum value during the initial stages of sintering" |
| Scherer & Garino 1985, *J. Am. Ceram. Soc.* 68, 216–220 | 10.1111/j.1151-2916.1985.tb15300.x | AB | Viscous sintering of a glass layer on a rigid substrate; "the effects of microstructural anisotropy (pore orientation) are likely to be small" |
| Cai, Green & Messing 1997 I, *J. Am. Ceram. Soc.* 80, 1929–1939 | 10.1111/j.1151-2916.1997.tb03075.x | AB | "The sintering mismatch stresses were estimated from the degree of curling in asymmetric laminates and from layer viscosities that were obtained by cyclic loading dilatometry." |
| Cai, Green & Messing 1997 II, *J. Am. Ceram. Soc.* 80, 1940–1948 | 10.1111/j.1151-2916.1997.tb03076.x | AB | "with the exception of the initial heating period, the viscoelastic stress is identical to the viscous stress that is calculated solely from the strain rate mismatch." |
| **Cai viscous bilayer curvature-rate formula** | — | **NOT VERIFIED.** The closed-form expression was not found in any open source read this session. Do not typeset it from memory; check it against Cai et al. 1997 Part I. A verified alternative is the normalised curvature-rate solution, Eq. (30) on thesis p. 37 of T. T. Molla, *Modeling Macroscopic Shape Distortions during Sintering of Multi-layers*, PhD thesis, DTU (2014), OA at backend.orbit.dtu.dk (portal file 102421296). Its symbols are defined in the thesis §3.4 (not transcribed here). | — |
| Kanters, Eisele & Rödel 2001, *J. Am. Ceram. Soc.* 84, 2757–2763 | 10.1111/j.1151-2916.2001.tb01091.x | AB | Cosintering of undoped / 3Y-TZP nanocrystalline zirconia laminates; densification and curvature fitted by a continuum model over "various relative layer thicknesses and heating rates" |
| Ni et al. 2013 (online 2012), *J. Am. Ceram. Soc.* 96, 972–978 | 10.1111/jace.12113 | AB | In-situ camber of CGO / LSM-CGO bilayers; uniaxial viscosities from vertical sintering; "The camber evolution … was found to correspond well with the one predicted by the theoretical model." |
| Molla et al. 2014, *J. Am. Ceram. Soc.* 97, 2965–2972 | 10.1111/jace.13025 | No | FE modelling of bilayer camber |
| Prado, Zanotto & Müller 2001, *J. Non-Cryst. Solids* 279, 169–178 | 10.1016/s0022-3093(00)00399-9 | Via Prado & Zanotto 2002 | Clusters model (Frenkel up to ρ = 0.8, then M–S) |
| Prado & Zanotto 2002, *C. R. Chimie* 5, 773–786 | 10.1016/s1631-0748(02)01447-9 | FT | See §1.4 (Clusters model with surface crystallisation; cordierite case) |
| Müller, Zanotto & Fokin 2000, *J. Non-Cryst. Solids* 274, 208–231 | 10.1016/s0022-3093(00)00214-3 | No | Surface nucleation sites and kinetics |
| Kissinger 1957, *Anal. Chem.* 29, 1702–1706 | 10.1021/ac60131a045 | Form as used in Sun 2022 and Wang 2026 | ln(β/Tp²) = ln(AR/Ek) − Ek/(RTp) (Sun 2022, Eq. 1) |
| Kissinger 1956, *J. Res. NBS* 57, 217 | 10.6028/jres.057.026 | No | (cited by Wang 2026) |
| Matusita, Komatsu & Yokota 1984, *J. Mater. Sci.* 19, 291–296 | 10.1007/BF02403137 | No | Non-isothermal Avrami n (used by Wang 2026) |
| Avrami 1939, 1940, 1941, *J. Chem. Phys.* 7, 1103–1112; 8, 212–224; 9, 177–184 | 10.1063/1.1750380; 10.1063/1.1750631; 10.1063/1.1750872 | No | JMAK kinetics |
| Vogel 1921, *Phys. Z.* 22, 645 | none | Bibliographic data from de.wikipedia (secondary) | VFT equation |
| Fulcher 1925, *J. Am. Ceram. Soc.* 8, 339–355 | 10.1111/j.1151-2916.1925.tb16731.x | No | VFT equation |
| Tammann & Hesse 1926, *Z. anorg. allg. Chem.* 156, 245–257 | 10.1002/zaac.19261560121 | No | VFT equation |
| Krieger & Dougherty 1959, *Trans. Soc. Rheol.* 3, 137–152 | 10.1122/1.548848 | No | Suspension viscosity model (formula not read this session) |

---

## 7. Gaps and uncertainties

1. **IBM glass Tg, dilatometric softening point and VFT constants: NOT FOUND.** Stand-ins are the stoichiometric-cordierite VFT fit of Reinsch 2008 (Tg ≈ 816 °C by η = 10^12.3 Pa s) and the IBM bound (anneal point < 785 °C < softening point; coalescence 800–875 °C). Giess & Knickerbocker 1985 (doi:10.1007/bf00720516) is the likely source of IBM-glass VFT data, but it is paywalled and was not read.
2. **Avrami exponent for the IBM glass: NOT FOUND.** Only E ≈ 302–304 kJ/mol and a surface-nucleation mechanism are verified. Values of n = 2.8–3.7 come from a different (perlite-derived, Na₂O-bearing) MAS glass.
3. **Young's modulus, Poisson's ratio and density of the IBM glass-ceramic: NOT FOUND.** The closest verified analogue is Kyocera GL570 (Cu-co-fired, CTE 3.4 ppm/K, E = 128 GPa). No ν was found for any cordierite GC.
4. **Strength conflict.** For Glass #12, US 4,301,324 gives 82,300 psi (≈567 MPa) and US 4,234,367 gives 210 MPa. Use 210 MPa for the H₂/H₂O / Cu-fired body.
5. **X-Y shrinkage of the IBM substrate: NOT FOUND** as a number. Verified facts are Z ≈ ½ X-Y (unconstrained, H₂/H₂O), 33–50 % of shrinkage during burnout, and Z = 11–15 % under light platen load.
6. **Tummala 1992 IBM JRD abstract (ε = 5.0, CTE 30 ×10⁻⁷/°C, 63 layers) and Master 1991 (steam sintering)** are SN level only; the IEEE Xplore pages were blocked. The CTE (3.0 ppm/°C) and ε (5.1) from the 2002 IBM JRD full text are FT and should be preferred.
7. **Cu E(T), ν(T) (Ledbetter & Naimon, NIST JPCRD):** srd.nist.gov returned HTTP 503 all session. E(T) here is a derived estimate. Retry https://srd.nist.gov/jpcrdreprint/1.3253150.pdf.
8. **Quasi-static yield of annealed Cu from 600 to 900 °C: NOT FOUND** in an open primary source. The JC extrapolation (D) is calibrated to high strain rates and overestimates quasi-static RT yield (90 vs 69 MPa). Candidates for follow-up are Li & Zinkle, "Physical and Mechanical Properties of Copper and Copper Alloys", *Comprehensive Nuclear Materials* 4.20 (2012) (UNT digital library copy blocked by a JS challenge), and NASA CR-134806 (1975, NTRS; OFHC Cu tensile and modulus vs T to 811 K, graphical only).
9. **Rudolph 1993 (469 kJ/mol)** is SN level only.
10. **Yu 2022 "Tg ≈ 909 °C"** conflicts with that paper's own 875–900 °C densification. Do not use it.
11. **Commercial Cu-in-N₂ LTCC shrinkage/firing datasheet: NOT FOUND.** The Fujitsu patent (US 4,504,339) gives a full N₂ + H₂O cycle but no shrinkage.
12. Kanters et al.: the requested reference was taken to be the 2001 J. Am. Ceram. Soc. cosintering paper. The same group also published *Adv. Eng. Mater.* 3 (2001) 158 (doi:10.1002/1527-2648(200103)3:3<158::aid-adem158>3.0.co;2-s), which was not read.

---

## BibTeX

DOI entries were generated from the Crossref records. Entries without a DOI (patents, datasheets, web tables, arXiv, thesis, Frenkel 1945, Vogel 1921) carry a `note`. The key `ni2013camber` matches `context_dossier.md`; its Crossref issued date is 2012 (online).

```bibtex
@article{tummala1991ceramic,
  author = {Tummala, Rao R.},
  title = {Ceramic and Glass-Ceramic Packaging in the 1990s},
  year = {1991},
  doi = {10.1111/j.1151-2916.1991.tb04320.x},
  journal = {Journal of the American Ceramic Society},
  volume = {74},
  number = {5},
  pages = {895--908}
}

@article{tummala1992highperformance,
  author = {Tummala, R. R. and Knickerbocker, J. U. and Knickerbocker, S. H. and Herron, L. W. and Nufer, R. W. and Master, R. N. and Neisser, M. O. and Kellner, B. M. and Perry, C. H. and Humenik, J. N. and Redmond, T. F.},
  title = {High-performance glass-ceramic/copper multilayer substrate with thin-film redistribution},
  year = {1992},
  doi = {10.1147/rd.365.0889},
  journal = {IBM Journal of Research and Development},
  volume = {36},
  number = {5},
  pages = {889--904}
}

@article{knickerbocker2002advanced,
  author = {Knickerbocker, J. U. and Pompeo, F. L. and Tai, A. F. and Thomas, D. L. and Weekly, R. D. and Nealon, M. G. and Hamel, H. C. and Haridass, A. and Humenik, J. N. and Shelleman, R. A. and Reddy, S. N. and Prettyman, K. M. and Fasano, B. V. and Ray, S. K. and Lombardi, T. E. and Marston, K. C. and Coico, P. A. and Brofman, P. J. and Goldmann, L. S. and Edwards, D. L. and Zitz, J. A. and Iruvanti, S. and Shinde, S. L. and Longworth, H. P.},
  title = {An advanced multichip module (MCM) for high-performance UNIX servers},
  year = {2002},
  doi = {10.1147/rd.466.0779},
  journal = {IBM Journal of Research and Development},
  volume = {46},
  number = {6},
  pages = {779--804}
}

@article{master1991cosintering,
  author = {Master, R.N. and Herron, L.W. and Tummala, R.R.},
  title = {Cosintering process for glass-ceramic/copper multilayer ceramic substrate},
  year = {1991},
  doi = {10.1109/33.105133},
  journal = {IEEE Transactions on Components, Hybrids, and Manufacturing Technology},
  volume = {14},
  number = {4},
  pages = {780--783}
}

@inproceedings{master1991cofiring,
  author = {Master, R.N. and Herron, L.W. and Tummala, R.R.},
  title = {Cofiring process for glass-Ceramic/copper multilayer ceramic substrate},
  year = {1991},
  doi = {10.1109/ectc.1991.163843},
  note = {Crossref record has no issued date; year from the conference title},
  booktitle = {1991 Proceedings 41st Electronic Components & Technology Conference},
  pages = {5--9}
}

@article{kumar1992past,
  author = {Kumar, Ananda H. and Tummala, Rao R.},
  title = {The past, present, and future of multilayer ceramic multichip modules in electronic packaging},
  year = {1992},
  doi = {10.1007/bf03222269},
  journal = {JOM},
  volume = {44},
  number = {7},
  pages = {10--14}
}

@article{giess1984isothermal,
  author = {GIESS, EDWARD A. and FLETCHER, JOSEPH P. and HERRON, L. WYNN},
  title = {Isothermal Sintering of Cordierite-Type Glass Powders},
  year = {1984},
  doi = {10.1111/j.1151-2916.1984.tb19168.x},
  journal = {Journal of the American Ceramic Society},
  volume = {67},
  number = {8},
  pages = {549--552}
}

@article{giess1985isothermal,
  author = {Giess, Edward A. and Guerci, Carl F. and Walker, George F. and Wen, Sheree H.},
  title = {Isothermal Sintering of Spheroidized Cordierite-Type Glass Powders},
  year = {1985},
  doi = {10.1111/j.1151-2916.1985.tb10136.x},
  journal = {Journal of the American Ceramic Society},
  volume = {68},
  number = {12}
}

@article{giess1985viscosity,
  author = {Geiss, Edward A. and Knickerbocker, Sarah H.},
  title = {Viscosity of MgO-Al2O3-SiO2-B2O3-P2O5 cordierite-type glasses},
  year = {1985},
  doi = {10.1007/bf00720516},
  journal = {Journal of Materials Science Letters},
  volume = {4},
  number = {7},
  pages = {835--837}
}

@article{exner1988anisotropic,
  author = {Exner, Hans Eckart and Giess, Edward A.},
  title = {Anisotropic shrinkage of cordierite-type glass powder cylindrical compacts},
  year = {1988},
  doi = {10.1557/jmr.1988.0122},
  journal = {Journal of Materials Research},
  volume = {3},
  number = {1},
  pages = {122--125}
}

@article{watanabe1985coalescence,
  author = {Watanabe, Koichi and Giess, Edward A.},
  title = {Coalescence and Crystallization in Powdered High-Cordierite (2MgO·2Al 2 O 3 ·5SiO 2 ) Glass},
  year = {1985},
  doi = {10.1111/j.1151-2916.1985.tb15307.x},
  journal = {Journal of the American Ceramic Society},
  volume = {68},
  number = {4}
}

@article{watanabe1985crystallization,
  author = {Watanabe, Koichi and Giess, Edward A. and Shafer, Merrill W.},
  title = {The crystallization mechanism of high-cordierite glass},
  year = {1985},
  doi = {10.1007/bf01026520},
  journal = {Journal of Materials Science},
  volume = {20},
  number = {2},
  pages = {508--515}
}

@article{watanabe1994crystallization,
  author = {Watanabe, Koichi and Giess, Edward A.},
  title = {Crystallization kinetics of high-cordierite glass},
  year = {1994},
  doi = {10.1016/0022-3093(94)90327-1},
  journal = {Journal of Non-Crystalline Solids},
  volume = {169},
  number = {3},
  pages = {306--310}
}

@article{rudolph1993determination,
  author = {Rudolph, Thomas and Pannhorst, Wolfgang and Petzow, Günter},
  title = {Determination of activation energies for the crystallization of a cordierite-type glass},
  year = {1993},
  doi = {10.1016/0022-3093(93)91262-2},
  journal = {Journal of Non-Crystalline Solids},
  volume = {155},
  number = {3},
  pages = {273--281}
}

@article{reinsch2008crystal,
  author = {Reinsch, Stefan and Nascimento, Marcio Luis Ferreira and Müller, Ralf and Zanotto, Edgar Dutra},
  title = {Crystal growth kinetics in cordierite and diopside glasses in wide temperature ranges},
  year = {2008},
  doi = {10.1016/j.jnoncrysol.2008.09.007},
  journal = {Journal of Non-Crystalline Solids},
  volume = {354},
  number = {52-54},
  pages = {5386--5394}
}

@article{fokin2005correlation,
  author = {Fokin, Vladimir M. and Nascimento, Marcio L.F. and Zanotto, Edgar D.},
  title = {Correlation between maximum crystal growth rate and glass transition temperature of silicate glasses},
  year = {2005},
  doi = {10.1016/j.jnoncrysol.2005.02.005},
  journal = {Journal of Non-Crystalline Solids},
  volume = {351},
  number = {10-11},
  pages = {789--794}
}

@article{sun2022crystallization,
  author = {SUN, Yangshan and YANG, Zhihua and CAI, Delong and ZHANG, Zhengyi and LIU, Qi and FANG, Shuqing and FENG, Liang and SHI, Lifen and WANG, Youle and JIA, Dechang},
  title = {Crystallization Kinetics, Properties of α -cordierite Based Glass-ceramics Prepared by Glass Powder Sintering},
  year = {2022},
  doi = {10.15541/jim20220179},
  journal = {Journal of Inorganic Materials},
  volume = {37},
  number = {12},
  pages = {1351}
}

@article{wang2026effect,
  author = {Wang, Saibo and Yu, Yongsheng and Zhao, Yunxiao and Wang, Pengzhen and Wang, Jinghan and Yan, Zhaoli and Jing, Qiangshan},
  title = {Effect of Na2O on the Low-Temperature Densification, Crystallization Behavior, and Dielectric Properties of Perlite Tailings-Derived α-Cordierite Glass-Ceramics},
  year = {2026},
  doi = {10.3390/ma19071348},
  journal = {Materials},
  volume = {19},
  number = {7},
  pages = {1348}
}

@article{yu2022synthesis,
  author = {Yu, Yongsheng and Wang, Jinghan and Yu, Yuanyuan and Yan, Zhaoli and Du, Yanyan and Chu, Pengfei and Jing, Qiangshan and Liu, Peng},
  title = {Synthesis and Characterization of Single-Phase α-Cordierite Glass-Ceramics for LTCC Substrates from Tuff},
  year = {2022},
  doi = {10.3390/ma15248758},
  journal = {Materials},
  volume = {15},
  number = {24},
  pages = {8758}
}

@article{prado2002glass,
  author = {Prado, Miguel Oscar and Zanotto, Edgar Dutra},
  title = {Glass sintering with concurrent crystallization},
  year = {2002},
  doi = {10.1016/s1631-0748(02)01447-9},
  journal = {Comptes Rendus. Chimie},
  volume = {5},
  number = {11},
  pages = {773--786}
}

@article{prado2001model,
  author = {Oscar Prado, Miguel and Dutra Zanotto, Edgar and Müller, Ralf},
  title = {Model for sintering polydispersed glass particles},
  year = {2001},
  doi = {10.1016/s0022-3093(00)00399-9},
  journal = {Journal of Non-Crystalline Solids},
  volume = {279},
  number = {2-3},
  pages = {169--178}
}

@article{muller2000surface,
  author = {Müller, R. and Zanotto, E.D. and Fokin, V.M.},
  title = {Surface crystallization of silicate glasses: nucleation sites and kinetics},
  year = {2000},
  doi = {10.1016/s0022-3093(00)00214-3},
  journal = {Journal of Non-Crystalline Solids},
  volume = {274},
  number = {1-3},
  pages = {208--231}
}

@article{girardi2009response,
  author = {Girardi, Michael and Barner, Gregg and Lopez, Cristie and Duncan, Brent and Zawicki, Larry},
  title = {Response Predicting LTCC Firing Shrinkage: A Response Surface Analysis Study},
  year = {2009},
  doi = {10.4071/1551-4897-6.2.114},
  journal = {Journal of Microelectronics and Electronic Packaging},
  volume = {6},
  number = {2},
  pages = {114--118}
}

@article{chretien2022distortion,
  author = {Chrétien, Lucie and Heux, Adrien and Antou, Guy and Pradeilles, Nicolas and Delhote, Nicolas and Maître, Alexandre},
  title = {Distortion of an LTCC Bilayer during Constrained Sintering: Comparison between Ombroscopic Imaging and Modeling},
  year = {2022},
  doi = {10.3390/ma15186405},
  journal = {Materials},
  volume = {15},
  number = {18},
  pages = {6405}
}

@article{parikh1958effect,
  author = {PARIKH, N. M.},
  title = {Effect of Atmosphere on Surface Tension of Glass},
  year = {1958},
  doi = {10.1111/j.1151-2916.1958.tb13497.x},
  journal = {Journal of the American Ceramic Society},
  volume = {41},
  number = {1},
  pages = {18--22}
}

@article{ledbetter1974elastic,
  author = {Ledbetter, H. M. and Naimon, E. R.},
  title = {Elastic Properties of Metals and Alloys. II. Copper},
  year = {1974},
  doi = {10.1063/1.3253150},
  journal = {Journal of Physical and Chemical Reference Data},
  volume = {3},
  number = {4},
  pages = {897--935}
}

@article{chang1966temperature,
  author = {Chang, Y. A. and Himmel, L.},
  title = {Temperature Dependence of the Elastic Constants of Cu, Ag, and Au above Room Temperature},
  year = {1966},
  doi = {10.1063/1.1708903},
  journal = {Journal of Applied Physics},
  volume = {37},
  number = {9},
  pages = {3567--3572}
}

@article{nix1941thermal,
  author = {Nix, F. C. and MacNair, D.},
  title = {The Thermal Expansion of Pure Metals: Copper, Gold, Aluminum, Nickel, and Iron},
  year = {1941},
  doi = {10.1103/physrev.60.597},
  journal = {Physical Review},
  volume = {60},
  number = {8},
  pages = {597--605}
}

@article{johnson1985fracture,
  author = {Johnson, Gordon R. and Cook, William H.},
  title = {Fracture characteristics of three metals subjected to various strains, strain rates, temperatures and pressures},
  year = {1985},
  doi = {10.1016/0013-7944(85)90052-9},
  journal = {Engineering Fracture Mechanics},
  volume = {21},
  number = {1},
  pages = {31--48}
}

@article{mackenzie1949phenomenological,
  author = {Mackenzie, J K and Shuttleworth, R},
  title = {A Phenomenological Theory of Sintering},
  year = {1949},
  doi = {10.1088/0370-1301/62/12/310},
  journal = {Proceedings of the Physical Society. Section B},
  volume = {62},
  number = {12},
  pages = {833--852}
}

@article{scherer1977sinteringI,
  author = {SCHERER, GEORGE W.},
  title = {Sintering of Low-Density Glasses: I, Theory},
  year = {1977},
  doi = {10.1111/j.1151-2916.1977.tb14114.x},
  journal = {Journal of the American Ceramic Society},
  volume = {60},
  number = {5-6},
  pages = {236--239}
}

@article{scherer1977sinteringII,
  author = {SCHERER, GEORGE W. and BACHMAN, DAVID L.},
  title = {Sintering of Low-Density Glasses: II, Experimental Study},
  year = {1977},
  doi = {10.1111/j.1151-2916.1977.tb14115.x},
  journal = {Journal of the American Ceramic Society},
  volume = {60},
  number = {5-6},
  pages = {239--243}
}

@article{scherer1977sinteringIII,
  author = {SCHERER, GEORGE W.},
  title = {Sintering of Low-Density Glasses: III, Effect of a Distribution of Pore Sizes},
  year = {1977},
  doi = {10.1111/j.1151-2916.1977.tb14116.x},
  journal = {Journal of the American Ceramic Society},
  volume = {60},
  number = {5-6},
  pages = {243--246}
}

@article{olevsky1998theory,
  author = {Olevsky, Eugene A.},
  title = {Theory of sintering: from discrete to continuum},
  year = {1998},
  doi = {10.1016/s0927-796x(98)00009-6},
  journal = {Materials Science and Engineering: R: Reports},
  volume = {23},
  number = {2},
  pages = {41--100}
}

@article{bordia1988constrained,
  author = {Bordia, R.K. and Scherer, G.W.},
  title = {On constrained sintering—I. Constitutive model for a sintering body},
  year = {1988},
  doi = {10.1016/0001-6160(88)90189-7},
  journal = {Acta Metallurgica},
  volume = {36},
  number = {9},
  pages = {2393--2397}
}

@article{bordia1988constrainedII,
  author = {Bordia, R.K. and Scherer, G.W.},
  title = {On constrained sintering—II. Comparison of constitutive models},
  year = {1988},
  doi = {10.1016/0001-6160(88)90190-3},
  journal = {Acta Metallurgica},
  volume = {36},
  number = {9},
  pages = {2399--2409}
}

@article{bordia1988constrainedIII,
  author = {Bordia, R.K. and Scherer, G.W.},
  title = {On constrained sintering—III. Rigid inclusions},
  year = {1988},
  doi = {10.1016/0001-6160(88)90191-5},
  journal = {Acta Metallurgica},
  volume = {36},
  number = {9},
  pages = {2411--2416}
}

@article{bordia1985sintering,
  author = {BORDIA, R.K. and RAJ, R.},
  title = {Sintering Behavior of Ceramic Films Constrained by a Rigid Substrate},
  year = {1985},
  doi = {10.1111/j.1151-2916.1985.tb15227.x},
  journal = {Journal of the American Ceramic Society},
  volume = {68},
  number = {6},
  pages = {287--292}
}

@article{scherer1985viscous,
  author = {SCHERER, GEORGE W. and GARINO, TERRY},
  title = {Viscous Sintering on a Rigid Substrate},
  year = {1985},
  doi = {10.1111/j.1151-2916.1985.tb15300.x},
  journal = {Journal of the American Ceramic Society},
  volume = {68},
  number = {4},
  pages = {216--220}
}

@article{cai1997constrainedI,
  author = {Cai, Peter Z. and Green, David J. and Messing, Gary L.},
  title = {Constrained Densification of Alumina/Zirconia Hybrid Laminates, I: Experimental Observations of Processing Defects},
  year = {1997},
  doi = {10.1111/j.1151-2916.1997.tb03075.x},
  journal = {Journal of the American Ceramic Society},
  volume = {80},
  number = {8},
  pages = {1929--1939}
}

@article{cai1997constrainedII,
  author = {Cai, Peter Z. and Green, David J. and Messing, Gary L.},
  title = {Constrained Densification of Alumina/Zirconia Hybrid Laminates, II: Viscoelastic Stress Computation},
  year = {1997},
  doi = {10.1111/j.1151-2916.1997.tb03076.x},
  journal = {Journal of the American Ceramic Society},
  volume = {80},
  number = {8},
  pages = {1940--1948}
}

@article{kanters2001cosintering,
  author = {Kanters, Johannes and Eisele, Ulrich and Rödel, Jürgen},
  title = {Cosintering Simulation and Experimentation: Case Study of Nanocrystalline Zirconia},
  year = {2001},
  doi = {10.1111/j.1151-2916.2001.tb01091.x},
  journal = {Journal of the American Ceramic Society},
  volume = {84},
  number = {12},
  pages = {2757--2763}
}

@article{ni2013camber,
  author = {Ni, De-Wei and Esposito, Vincenzo and Schmidt, Cristine Grings and Molla, Tesfaye Tadesse and Andersen, Kjeld Bøhm and Kaiser, Andreas and Ramousse, Severine and Pryds, Nini},
  title = {Camber Evolution and Stress Development of Porous Ceramic Bilayers During Co-Firing},
  year = {2013},
  doi = {10.1111/jace.12113},
  note = {Crossref issued date 2012-12-06 (online); volume 96 is the 2013 volume},
  journal = {Journal of the American Ceramic Society},
  volume = {96},
  number = {3},
  pages = {972--978}
}

@article{molla2014finite,
  author = {Molla, Tesfaye Tadesse and Ni, De Wei and Bulatova, Regina and Bjørk, Rasmus and Bahl, Christian and Pryds, Nini and Frandsen, Henrik Lund},
  title = {Finite Element Modeling of Camber Evolution During Sintering of Bilayer Structures},
  year = {2014},
  doi = {10.1111/jace.13025},
  journal = {Journal of the American Ceramic Society},
  volume = {97},
  number = {9},
  pages = {2965--2972}
}

@article{kissinger1957reaction,
  author = {Kissinger, H. E.},
  title = {Reaction Kinetics in Differential Thermal Analysis},
  year = {1957},
  doi = {10.1021/ac60131a045},
  journal = {Analytical Chemistry},
  volume = {29},
  number = {11},
  pages = {1702--1706}
}

@article{kissinger1956variation,
  author = {Kissinger, Homer E.},
  title = {Variation of peak temperature with heating rate in differential thermal analysis},
  year = {1956},
  doi = {10.6028/jres.057.026},
  journal = {Journal of Research of the National Bureau of Standards},
  volume = {57},
  number = {4},
  pages = {217}
}

@article{matusita1984kinetics,
  author = {Matusita, Kazumasa and Komatsu, Takayuki and Yokota, Ryosuke},
  title = {Kinetics of non-isothermal crystallization process and activation energy for crystal growth in amorphous materials},
  year = {1984},
  doi = {10.1007/bf02403137},
  journal = {Journal of Materials Science},
  volume = {19},
  number = {1},
  pages = {291--296}
}

@article{avrami1939kinetics,
  author = {Avrami, Melvin},
  title = {Kinetics of Phase Change. I General Theory},
  year = {1939},
  doi = {10.1063/1.1750380},
  journal = {The Journal of Chemical Physics},
  volume = {7},
  number = {12},
  pages = {1103--1112}
}

@article{avrami1940kinetics,
  author = {Avrami, Melvin},
  title = {Kinetics of Phase Change. II Transformation-Time Relations for Random Distribution of Nuclei},
  year = {1940},
  doi = {10.1063/1.1750631},
  journal = {The Journal of Chemical Physics},
  volume = {8},
  number = {2},
  pages = {212--224}
}

@article{avrami1941granulation,
  author = {Avrami, Melvin},
  title = {Granulation, Phase Change, and Microstructure Kinetics of Phase Change. III},
  year = {1941},
  doi = {10.1063/1.1750872},
  journal = {The Journal of Chemical Physics},
  volume = {9},
  number = {2},
  pages = {177--184}
}

@article{fulcher1925analysis,
  author = {Fulcher, Gordon S.},
  title = {ANALYSIS OF RECENT MEASUREMENTS OF THE VISCOSITY OF GLASSES},
  year = {1925},
  doi = {10.1111/j.1151-2916.1925.tb16731.x},
  journal = {Journal of the American Ceramic Society},
  volume = {8},
  number = {6},
  pages = {339--355}
}

@article{tammann1926abhangigkeit,
  author = {Tammann, G. and Hesse, W.},
  title = {Die Abhängigkeit der Viscosität von der Temperatur bie unterkühlten Flüssigkeiten},
  year = {1926},
  doi = {10.1002/zaac.19261560121},
  journal = {Zeitschrift für anorganische und allgemeine Chemie},
  volume = {156},
  number = {1},
  pages = {245--257}
}

@article{krieger1959mechanism,
  author = {Krieger, Irvin M. and Dougherty, Thomas J.},
  title = {A Mechanism for Non-Newtonian Flow in Suspensions of Rigid Spheres},
  year = {1959},
  doi = {10.1122/1.548848},
  journal = {Transactions of the Society of Rheology},
  volume = {3},
  number = {1},
  pages = {137--152}
}

@misc{frenkel1945viscous,
  author = {Frenkel, J.},
  title = {Viscous flow of crystalline bodies under the action of surface tension},
  year = {1945},
  howpublished = {J. Phys. (USSR) 9(5), 385},
  note = {No DOI. Bibliographic data as cited in Prado and Zanotto 2002 (ref. 1); title not verified against the original}
}

@misc{vogel1921temperaturabhangigkeitsgesetz,
  author = {Vogel, H.},
  title = {Das Temperaturabh{\"a}ngigkeitsgesetz der Viskosit{\"a}t von Fl{\"u}ssigkeiten},
  year = {1921},
  howpublished = {Physikalische Zeitschrift 22, 645},
  note = {No DOI. Bibliographic data from a secondary source (de.wikipedia, Vogel-Fulcher-Tammann-Gleichung)}
}

@misc{kumar1981glassceramic,
  author = {Kumar, Ananda H. and McMillan, Peter W. and Tummala, Rao R.},
  title = {Glass-ceramic structures and sintered multilayer substrates thereof with circuit patterns of gold, silver or copper},
  year = {1981},
  howpublished = {US Patent 4,301,324, issued 1981-11-17, assigned to IBM},
  note = {Full text read on Google Patents (US4301324A)}
}

@misc{herron1980method,
  author = {Herron, Lester W. and Master, Raj N. and Tummala, Rao R.},
  title = {Method of making multilayered glass-ceramic structures having an internal distribution of copper-based conductors},
  year = {1980},
  howpublished = {US Patent 4,234,367, issued 1980-11-18, assigned to IBM},
  note = {Full text read on Google Patents (US4234367A)}
}

@misc{dubetsky1982process,
  author = {Dubetsky, Derry J. and Herron, Lester W. and Master, Raj N.},
  title = {Process for flattening glass-ceramic substrates},
  year = {1982},
  howpublished = {US Patent 4,340,436, issued 1982-07-20, assigned to IBM},
  note = {Full text read on Google Patents (US4340436A)}
}

@misc{herron1986method,
  author = {Herron, Lester W. and Kumar, Ananda H. and Master, Raj N.},
  title = {Method for removal of carbonaceous residues from ceramic structures having internal metallurgy},
  year = {1986},
  howpublished = {US Patent 4,627,160, issued 1986-12-09, assigned to IBM},
  note = {Full text read on Google Patents (US4627160A)}
}

@misc{flaitz1992method,
  author = {Flaitz, Philip L. and Flanagan, Arlyne M. and Harvilchuck, Joseph M. and others},
  title = {Method and means for co-sintering ceramic/metal {MLC} substrates},
  year = {1992},
  howpublished = {US Patent 5,130,067, issued 1992-07-14, assigned to IBM},
  note = {Full text read on Google Patents (US5130067A)}
}

@misc{kamehara1985method,
  author = {Kamehara, Nobuo and Kurihara, Kazuaki and Niwa, Koichi},
  title = {Method for producing multilayered glass-ceramic structure with copper-based conductors therein},
  year = {1985},
  howpublished = {US Patent 4,504,339, issued 1985-03-12, assigned to Fujitsu Ltd},
  note = {Full text read on Google Patents (US4504339A)}
}

@misc{wang2006process,
  author = {Wang, Carl B. and Hang, Kenneth Warren and Needes, Christopher R.},
  title = {Process for the constrained sintering of a pseudo-symmetrically configured low temperature cofired ceramic structure},
  year = {2006},
  howpublished = {US Patent 7,068,492 B2, issued 2006-06-27},
  note = {Full text read on Google Patents; source of the DuPont 951 belt-furnace profile}
}

@misc{dupont951tds,
  author = {{DuPont Microcircuit Materials}},
  title = {DuPont GreenTape 951 Low Temperature Ceramic System, Technical Data Sheet (MCM951, 7/2011)},
  year = {2011},
  howpublished = {PDF, https://www.etsmtl.ca/uploads/Dupont_951.pdf},
  note = {Datasheet; read 2026-09-24}
}

@misc{ferroa6mtds,
  author = {{Ferro Corporation}},
  title = {A6M/A6M-E High Frequency LTCC Tape System, datasheet},
  year = {2015},
  howpublished = {PDF, https://www.etsmtl.ca/uploads/Ferro_A6M.pdf},
  note = {Datasheet dated November 2015; read 2026-09-24}
}

@misc{kyocera2026material,
  author = {{Kyocera Corporation}},
  title = {Material Properties: Ceramic Packages / Ceramic Substrates (GL570, GL580, GL773 LTCC)},
  year = {2026},
  howpublished = {Web page, https://global.kyocera.com/prdct/semicon/material/},
  note = {Representative values; read 2026-09-24}
}

@misc{aurubisc10200,
  author = {{Aurubis}},
  title = {Technical Datasheet C10200 (Cu-OF), 18 08 US},
  year = {2018},
  howpublished = {PDF, https://www.aurubis.com/en/dam/jcr:90029b00-b968-486e-bde0-ce56f16022cd/c10200-cu-of-us.pdf},
  note = {Datasheet; read 2026-09-24}
}

@misc{kayelaby235,
  author = {{National Physical Laboratory}},
  title = {Kaye and Laby Tables of Physical and Chemical Constants, Section 2.3.5 Thermal expansion (Version 1.1)},
  year = {2010},
  howpublished = {Archived web page, https://web.archive.org/web/20190512035127/http://www.kayelaby.npl.co.uk/general_physics/2_3/2_3_5.html},
  note = {Instantaneous expansivity table; read 2026-09-24}
}

@misc{banerjee2005evaluation,
  author = {Banerjee, Biswajit},
  title = {An evaluation of plastic flow stress models for the simulation of high-temperature and high-strain-rate deformation of metals},
  year = {2005},
  howpublished = {arXiv:cond-mat/0512466},
  note = {No DOI; full text read (arXiv v1)}
}

@phdthesis{molla2014modeling,
  author = {Molla, Tesfaye Tadesse},
  title = {Modeling Macroscopic Shape Distortions during Sintering of Multi-layers},
  school = {Technical University of Denmark (DTU)},
  year = {2014},
  note = {No DOI; open access at https://backend.orbit.dtu.dk/ws/portalfiles/portal/102421296/Modeling_Macroscopic_Shape_Distortions.pdf; Eq. (30), p. 37 read}
}
```
