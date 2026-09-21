- **summary**: **Scope: reverse-engineering an unknown Lithoz R&D copper photopolymer slurry — chemistry, content, and the analytical chain that closes the mass/volume balance.**

**1. What the binder almost certainly is.** Lithoz/TU-Wien have published the architecture even though the recipe is proprietary. Stampfl, Schwentenwein, Homa & Prinz (MRS Commun. 13:786, 2023) state that LCM binders comprise: (i) a **low-viscosity NON-REACTIVE solvent**, (ii) **reactive (meth)acrylate monomers of mixed functionality** (mono/di/tri), (iii) a visible-light **photoinitiator at <1 wt%**, (iv) **dispersants** (polarity compatibilisers), and (v) **dyes/absorbers** to moderate light penetration. Ożóg et al. (J. Ceram. Sci. Technol., 2019) independently confirm for LithaLox HP500: "(meth)acrylate monomers as reactive binder … proprietary non-reactive solvent, the dispersant and photoinitiators." The non-reactive solvent is the single most important structural fact for you: it dictates a long low-temperature **drying** stage (evaporation, not pyrolysis) that opens percolation channels before pyrolysis, and it produces a distinct sub-200 °C TGA event you must not confuse with binder decomposition. Published Lithoz-class debinding schedules spend the majority of their hours here (reported LithaLox profile: 25→75 °C/4 h + 18 h hold, →115 °C/4 h + 66 h hold, →205 °C/4 h + 22 h hold, →430 °C/10 h, →900 °C/12 h; ~156 h total). Comparable published LCM/DLP formulations use HDDA, TMPTA, PPTTA, ACMO, HEA, DEGDA, EBADA/EBADMA, urethane/polyester/amine-modified-polyether acrylates (SR238, SR355, CN509, CN371EU, Diacryl 101), TPO/BAPO (Omnirad 819) at 1–5 wt% of the organic fraction, and Solsperse 41000 / BYK-111 / Disperbyk-type phosphate-ester or polyether dispersants at ~3 wt% on powder.

**2. Copper-specific trap.** Roumanie et al. (SN Appl. Sci. 3:55, 2021) showed that **BAPO-derived phosphorus is a metallurgical poison in copper**: P from the photoinitiator plus DHP powder pushed sintered P to 0.035 wt% and collapsed thermal conductivity to ~160–250 W m⁻¹ K⁻¹ vs 250–270 for a BAPO-free formulation. So your ICP-OES for P is not book-keeping — it is a first-order property predictor. Likewise dispersant heteroatoms (P, S, Si, Zn, N) must be quantified because copper forms no carbides and cannot getter residual C; carbon leaves only as CO/CO₂/CH₄.

**3. Solids loading.** Lithoz's own datasheet gives the design window: LithaLox HP500/350 = **49 vol%**, LithaCon 3Y 210 = 48, LithaBone TCP 300 = 47, HA 400 = 46, LithaNit 770 = 40, LithaCore 450 = 63 vol%. The MRS review gives 45–60 vol% as typical, >45 vol% as mandatory for densification. Assume 45–60 vol% Cu. **Critical consequence:** because ρ_Cu/ρ_binder ≈ 8.1 (vs 3.6 for alumina), the ORGANIC MASS FRACTION of a copper green body is only **6–13 wt%** (13.1 at 45 vol%, 10.9 at 50, 9.1 at 55, 7.6 at 60) versus 22.6 wt% for LithaLox HP500. Your entire binder-content determination therefore hinges on a ~10 % mass-loss signal, which forces large TGA samples (>50 mg), buoyancy-corrected blank subtraction, and tight crucible-mass control.

**4. The algebra that closes it.** Measure the LIQUID slurry density ρ_sl (oscillating U-tube or liquid pycnometer), then burn out to metal and weigh. w_s = m_metal/m_green (Ar to 600 °C, then Ar–H₂ to gasify the ~7 wt% char Roumanie found in inert TGA). Then ρ_b = (1−w_s)/(1/ρ_sl − w_s/ρ_s) and φ_s = (w_s/ρ_s)/(w_s/ρ_s+(1−w_s)/ρ_b). Validating against LithaLox (ρ_sl = 2.52 g cm⁻³, 49 vol%, ρ_Al₂O₃ = 3.98) returns **ρ_b = 1.117 g cm⁻³** — a textbook multifunctional-acrylate density, which proves the method self-consistent. Sensitivity at φ=0.5 for Cu: ∂φ/∂w_s = 2.57, so 0.5 wt% error in w_s → 1.3 vol% in φ; ∂φ/∂ρ_b = 0.227 (g cm⁻³)⁻¹ → 0.02 g cm⁻³ error gives only 0.45 vol%.

**5. Never use air TGA for binder content on copper.** Oxidation adds mass: Cu→Cu₂O = +12.6 wt%, Cu→CuO = +25.2 wt%. Roumanie measured +8 / +14.4 / +16.8 wt% at 400/600/800 °C in air. The air trace is a convolution −w_b(1−χ) + w_s·g(T). Run inert first for the true organic budget; run air/reducing only to design the cycle.

**6. Speciation toolbox, ranked by information/effort.** SDS Section 3 (legally forces ≥1 wt% hazardous components with CAS) > Py-GC/MS at 750 °C/15 s (Belbakra, Polymers 13:4349 — m/z 99+55 = acrylate, 113+69 = methacrylate, 213 = bisphenol-A backbone) > TGA-FTIR/TGA-MS on the DTG peaks > ATR-FTIR of extractables (1720 C=O ester, 1636/1620 and 810 cm⁻¹ residual acrylate C=C, 3330 N–H + 1530 amide II for urethane, 1250 P=O / 1000–1050 P–O–C for phosphate esters) > Soxhlet/scCO₂ extraction to split sol/gel (scCO₂ removes ~90 wt% of the dissolvable fraction in 2 h and creates 21 vol% nanoporosity in ceramic prints) > ¹H/¹³C solution NMR on the sol, ¹³C CP-MAS on the gel > ICP-OES for P/S/Si/Zn/Na > CHNS + LECO C/O/N on green, brown and sintered states.
- **key_facts**:
  -
    - **fact**: Lithoz/TU-Wien state that LCM binders consist of a low-viscosity NON-REACTIVE solvent, reactive acrylate/methacrylate monomers of different functionality, a photoinitiator active at the LED wavelength at <1 wt%, dispersants, and dyes to moderate light penetration. The non-reactive solvent mandates a separate drying step before pyrolysis, which opens microscopic channels for decomposition products.
    - **source**: Stampfl J., Schwentenwein M., Homa J., Prinz F.B., 'Lithography-based additive manufacturing of ceramics: Materials, applications and perspectives', MRS Communications 13 (2023) 786-794, DOI 10.1557/s43579-023-00444-0 — https://doi.org/10.1557/s43579-023-00444-0
    - **confidence**: high
  -
    - **fact**: LithaLox HP500 is confirmed independently as 49 vol% high-purity alumina with a slurry density of 2.52 g/cm3, (meth)acrylate reactive binder, plus proprietary non-reactive solvent, dispersant and photoinitiators. This is the closest published analogue to an unlabelled Lithoz R&D slurry.
    - **source**: Ożóg P., Blugan G., Kata D., Graule T., 'Influence of the Printing Parameters on the Quality of Alumina Ceramics Shaped by UV-LCM Technology', J. Ceram. Sci. Technol. (2019), DOI 10.4416/JCST2019-00023 — https://www.ceramic-science.com/php/article_pdf.php?article_id=100699&hash=c6be80294a
    - **confidence**: high
  -
    - **fact**: Lithoz's own material datasheet gives slurry solids loading for its commercial grades: LithaLox HP500 and 350 = 49 vol%, LithaCon 3Y 210 (zirconia) = 48 vol%, LithaBone TCP 300 = 47 vol%, LithaBone HA 400 = 46 vol%, LithaNit 770 (Si3N4) = 40 vol%, LithaCore 450 (silica) = 63 vol%. This is the design envelope Lithoz works in.
    - **source**: Lithoz GmbH, 'Material Overview — LCM Technology', 2021/2 — https://lithoz.com/wp-content/uploads/2022/08/LITHOZ_Material_Folder_EN.pdf
    - **confidence**: high
  -
    - **fact**: Typical LCM solid loadings are 45-60 vol%; >45 vol% is required to ensure proper densification on sintering. Thermal processing (drying + debinding) typically takes 8-72 h, and wall thicknesses beyond 15-20 mm are difficult because solvent/decomposition-product removal is diffusion controlled.
    - **source**: Stampfl et al., MRS Communications 13 (2023) 786-794, DOI 10.1557/s43579-023-00444-0
    - **confidence**: high
  -
    - **fact**: Because copper is 8.1x denser than a typical acrylate binder, a copper green body at 45-60 vol% solids contains only 6-13 wt% organics, versus 22.6 wt% for LithaLox HP500 alumina at 49 vol%. All binder-content determination must be designed around a ~10 wt% mass-loss signal.
    - **source**: Derived arithmetic from rho_Cu = 8.96 g/cm3 and rho_binder = 1.117 g/cm3 (the latter back-calculated from the LithaLox HP500 datasheet values 49 vol% / 2.52 g/cm3 / rho_Al2O3 = 3.98)
    - **confidence**: high
  -
    - **fact**: Phosphorus originating from the BAPO photoinitiator (phenylbis(2,4,6-trimethylbenzoyl)phosphine oxide) is retained in sintered copper and severely degrades thermal conductivity. A BAPO-free formulation (DMPA) recovered reference-level conductivity. This makes ICP-OES for P a first-order property predictor, not just bookkeeping.
    - **source**: Roumanie M. et al., 'Influence of debinding and sintering conditions on the composition and thermal conductivity of copper parts printed from highly loaded photocurable formulations', SN Applied Sciences 3:55 (2021), DOI 10.1007/s42452-020-04049-3
    - **confidence**: high
  -
    - **fact**: Copper oxidises substantially during air debinding: mass gain of roughly +8, +14.4 and +16.8 wt% at 400, 600 and 800 C. Therefore an air TGA trace on a Cu-filled green body is a convolution of binder loss and metal oxidation and CANNOT be used to compute binder content.
    - **source**: Roumanie et al., SN Applied Sciences 3:55 (2021), DOI 10.1007/s42452-020-04049-3
    - **confidence**: medium
  -
    - **fact**: Pyrolysis of the same copper acrylate formulation in argon leaves ~7 wt% char residue, whereas burnout in air is complete. Any inert-atmosphere TGA therefore under-reports the organic fraction unless the char is subsequently gasified (H2 or O2 switch).
    - **source**: Roumanie et al., SN Applied Sciences 3:55 (2021), DOI 10.1007/s42452-020-04049-3
    - **confidence**: medium
  -
    - **fact**: Debinding atmosphere strongly controls residual carbon in copper: air at 400 C/4 h followed by H2 sintering gave 0.018 wt% C (equal to the raw powder); hydrogen debinding gave 0.25 wt% C; argon, vacuum, 600 ppm O2 and 5% O2/Ar all gave ~0.36 wt% C.
    - **source**: Roumanie et al., SN Applied Sciences 3:55 (2021), DOI 10.1007/s42452-020-04049-3
    - **confidence**: medium
  -
    - **fact**: Py-GC/MS at 750 C for 15 s cleanly discriminates acrylate from methacrylate networks: methacrylates depolymerise ('unzip') and regenerate their monomer (base peak m/z 113, methacryloyl m/z 69), while acrylates undergo beta-scission and yield no recoverable monomer (acrylate fragment m/z 99, acryloyl m/z 55). Bisphenol-A backbones give m/z 213.
    - **source**: Belbakra Z., Napoli A., Cherkaoui Z.M., Allonas X., 'Analysis of Acrylic and Methacrylic Networks through Pyrolysis-GC/MS', Polymers 13 (2021) 4349, DOI 10.3390/polym13244349 — https://pmc.ncbi.nlm.nih.gov/articles/PMC8708672/
    - **confidence**: high
  -
    - **fact**: A published copper DLP formulation (closest open analogue to the Lithoz copper slurry) used 60 vol% Cu with HDDA (SR238) + tetrafunctional oligoacrylate (SR355) + amine-modified polyether acrylate (CN509), variants with polyester acrylate CN371EU and ethoxylated bisphenol-A dimethacrylate (Diacryl 101), and MMMP + BAPO photoinitiators at 5 wt% of the photocurable fraction.
    - **source**: Roumanie et al., SN Applied Sciences 3:55 (2021), DOI 10.1007/s42452-020-04049-3
    - **confidence**: high
  -
    - **fact**: Representative ceramic VPP slurry formulations for comparison and spectral library building: (a) HEA/HDDA/PPTTA blends with Omnirad 819 (BAPO) 1 wt% and Solsperse 41000 dispersant 3 wt% at 40 vol% solids; (b) ACMO 56.7 / DEGDA 2.7 / TMPTA 40.6 wt% with TPO 3 wt% and BYK-111 3 wt% at 52 vol% AlN. These are the monomer/PI/dispersant classes you should pre-load into your GC-MS and FTIR libraries.
    - **source**: Zhang et al., Materials 18 (2025) 4004, DOI 10.3390/ma18174004; Kuang N., Zhao W., Wu J., Polymers 17 (2025) 2769, DOI 10.3390/polym17202769
    - **confidence**: high
  -
    - **fact**: Supercritical CO2 extraction of ceramic VPP prints removes ~90 wt% of the dissolvable (non-crosslinked) resin fraction in 2 h and creates ~21 vol% nanoporosity in ceramic/polymer prints (33 vol% in pure polymer prints); 15 h scCO2 + 18 h thermal debinding matched a 101 h reference thermal cycle. This is simultaneously an analytical separation of the sol fraction and a debinding accelerator.
    - **source**: Nurmi N.N., Frankberg E.J., Rinne M.M.A., Sandblom T., Konnunaho P., Levänen E.R., 'Enabling fast debinding of ceramic vat photopolymerization prints with supercritical carbon dioxide as a solvent' — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4647233 and https://www.sciencedirect.com/science/article/pii/S2214860424001891 (DOI unverified)
    - **confidence**: medium
  -
    - **fact**: A published Lithoz-class (LithaLox) thermal debinding profile runs 25->75 C over 4 h + 18 h hold; ->115 C over 4 h + 66 h hold; ->205 C over 4 h + 22 h hold; ->430 C over 10 h; ->900 C over 12 h; cool to 600 C over 8 h then to 25 C over 8 h; total ~156 h. The 66 h hold at 115 C is solvent removal, not binder pyrolysis.
    - **source**: unverified (recovered only as a search-result summary; wording consistent with the scCO2 debinding literature of Nurmi et al. — must be confirmed against the primary paper or the Lithoz datasheet before use)
    - **confidence**: low
  -
    - **fact**: Lithoz LCM parts are debound in air to a maximum of 900 C (alumina), followed by sintering at 1600 C for 2 h in air, using temperature programs supplied by Lithoz in the material datasheet. For copper, the 900 C air step is categorically forbidden (bulk oxidation, melting margin).
    - **source**: Ożóg et al., J. Ceram. Sci. Technol. (2019), DOI 10.4416/JCST2019-00023
    - **confidence**: high
  -
    - **fact**: Incus LMM (the metal analogue of LCM) uses a feedstock that is SOLID at room temperature with a sharp solid-to-liquid transition between 35 and 60 C, decaking at 40-80 C, and MIM-grade gas-atomised powder of 0-25 um. If your Lithoz copper slurry is liquid at RT it is an LCM-type (vat) slurry, not an LMM-type feedstock, and the binder architecture differs accordingly.
    - **source**: Harakaly G., Cano Cano S., Bosters J., Sperling C., Moedder D., Mitteramskogler G., J. Jpn. Soc. Powder Powder Metall. 72 (2025) S1227-S1231, DOI 10.2497/jjspm.16C-T11-08 — https://www.jstage.jst.go.jp/article/jjspm/72/Supplement/72_16C-T11-08/_pdf
    - **confidence**: high
  -
    - **fact**: In copper-filled photopolymer suspensions, UV transmission drops dramatically above 20 vol% loading and cure depth depends on the OXIDATION STATE of the copper particles (oxidised powders scatter less). Measuring the surface oxide of your as-received slurry powder is therefore part of both the print-parameter and the debinding design.
    - **source**: 'Lithography based Metal Manufacturing (LMM): Influence of particle size and composition of copper powder on UV light penetration', Materials Today Communications (2023) — https://www.sciencedirect.com/science/article/abs/pii/S2352492823002854
    - **confidence**: medium
  -
    - **fact**: There is an active, named research line on exactly your problem: Euro PM2024 paper M50, 'Recent Advances Of Lithography-based Metal Manufacturing Of Copper', Cano Cano S., Peritsch P., Bosters J. (Incus GmbH), Anand A., Gierl-Mayer C. (TU Wien), Harakaly G. It benchmarks copper powders from different suppliers through LMM feedstock, printing and sintering. These are the people to cite and to contact.
    - **source**: Euro PM2024 Group 3 Materials Abstracts Book, Malmö, 29 Sep - 2 Oct 2024, Paper M50, ID 6281350 — https://europm2024.com/wp-content/uploads/2024/02/Euro-PM2024-GROUP-3-MATERIALS-Abstracts-Book.pdf
    - **confidence**: high
  -
    - **fact**: Photoinitiator loading in vat photopolymerization resins is generally 0.01-10 wt%, commonly 0.5-1 wt%; Lithoz specifically states <1 wt% for LCM. TPO is now classified as a Class 1B reprotoxin, with TPO-L and BAPO expected to follow, which creates commercial pressure for Lithoz to substitute — relevant if you are trying to date/identify the formulation.
    - **source**: RadTech proceedings, Sehnal P., 'Novel Phosphine Oxide Photoinitiators' — https://radtech.org/proceedings/2014/papers/Photoinitiator/Sehnal%20-%20Novel%20Phosphine%20Oxide%20Photoinitiators.pdf ; Lithoz <1 wt% figure from MRS Communications 13 (2023) 786
    - **confidence**: medium
  -
    - **fact**: Non-reactive diluents used in ceramic VPP for exactly the reason Lithoz uses one (crack-free debinding) include PEG-200/400, PPG-400, benzyl alcohol, isopropyl alcohol and poly(oxyethylene) types; PPG decomposes BEFORE the main resin and forms interconnected escape porosity. These are the first candidates to look for in your GC-MS of the extractable fraction.
    - **source**: 'Effect of non-reactive diluent on defect-free debinding process of 3D printed ceramics', Additive Manufacturing (2023) — https://www.sciencedirect.com/science/article/pii/S221486042300088X ; and Si3N4 slurry work using 20 wt% ACMO / 30 wt% POE / 50 wt% HDDA — https://www.sciencedirect.com/science/article/abs/pii/S0272884220336701
    - **confidence**: medium
  -
    - **fact**: Standards to anchor the measurements: ASTM B923 (metal powder skeletal density by He or N2 pycnometry), ISO 13320 (laser diffraction PSD), ASTM E1019 (C, S, N, O by combustion and inert gas fusion — nominally steel/iron/nickel/cobalt, so its applicability to copper must be confirmed with the lab; ASTM E1941 covers C in refractory/reactive metals).
    - **source**: ASTM B923 https://www.astm.org/Standards/B923.htm ; ISO 13320:2020 https://www.iso.org/standard/69111.html ; ASTM E1019 https://www.astm.org/Standards/E1019.htm
    - **confidence**: medium
- **numbers**:
  -
    - **quantity**: LCM slurry solids loading, typical range
    - **value**: 45-60
    - **units**: vol%
    - **context**: All Lithoz/TU-Wien LCM ceramic slurries; >45 vol% stated as necessary for densification. Use as the prior for the copper slurry.
    - **source**: Stampfl et al., MRS Commun. 13 (2023) 786, DOI 10.1557/s43579-023-00444-0
  -
    - **quantity**: LithaLox HP500 / LithaLox 350 solids loading
    - **value**: 49
    - **units**: vol%
    - **context**: Lithoz commercial alumina slurry, from the manufacturer datasheet
    - **source**: Lithoz Material Overview folder 2021/2
  -
    - **quantity**: LithaCon 3Y 210 solids loading
    - **value**: 48
    - **units**: vol%
    - **context**: Lithoz 3 mol% yttria-stabilised zirconia slurry; viscosity 15 Pa.s at 50 1/s, 20 C
    - **source**: Lithoz Material Overview folder 2021/2
  -
    - **quantity**: LithaNit 770 solids loading
    - **value**: 40
    - **units**: vol%
    - **context**: Lithoz silicon nitride slurry — the LOW end of the Lithoz envelope (dark, absorbing ceramic)
    - **source**: Lithoz Material Overview folder 2021/2
  -
    - **quantity**: LithaCore 450 solids loading
    - **value**: 63
    - **units**: vol%
    - **context**: Lithoz silica-based casting-core slurry — the HIGH end; viscosity 45 Pa.s
    - **source**: Lithoz Material Overview folder 2021/2
  -
    - **quantity**: LithaBone TCP 300 / HA 400 solids loading
    - **value**: 47 / 46
    - **units**: vol%
    - **context**: Lithoz calcium-phosphate slurries
    - **source**: Lithoz Material Overview folder 2021/2
  -
    - **quantity**: LithaLox HP500 slurry density
    - **value**: 2.52
    - **units**: g/cm3
    - **context**: Measured slurry density at 49 vol% alumina; the key datum enabling back-calculation of the binder density
    - **source**: Ożóg et al., J. Ceram. Sci. Technol. (2019), DOI 10.4416/JCST2019-00023 (citing the Lithoz slurry datasheet)
  -
    - **quantity**: Back-calculated LCM organic-phase (binder+solvent+additives) density
    - **value**: 1.117
    - **units**: g/cm3
    - **context**: rho_b = (rho_slurry - phi*rho_Al2O3)/(1-phi) with rho_slurry=2.52, phi=0.49, rho_Al2O3=3.98. Consistent with multifunctional acrylate + glycol-ether solvent. Use 1.10-1.15 g/cm3 as the prior for the copper slurry binder.
    - **source**: Derived from Lithoz datasheet + Ożóg et al. (2019)
  -
    - **quantity**: Organic mass fraction of LithaLox HP500 green/slurry
    - **value**: 22.6
    - **units**: wt%
    - **context**: (1-phi)*rho_b/rho_slurry at 49 vol% alumina. The alumina benchmark against which the copper case must be scaled.
    - **source**: Derived from Lithoz datasheet + Ożóg et al. (2019)
  -
    - **quantity**: Organic mass fraction of a Cu green body at 45 / 50 / 55 / 60 / 65 vol% Cu
    - **value**: 13.05 / 10.93 / 9.13 / 7.57 / 6.20
    - **units**: wt%
    - **context**: rho_Cu = 8.96, rho_binder = 1.10 g/cm3. Corresponding green-body densities 4.64 / 5.03 / 5.42 / 5.82 / 6.21 g/cm3. THIS is your expected TGA mass loss.
    - **source**: Derived arithmetic (rho_Cu from standard reference; rho_binder from the LithaLox back-calculation)
  -
    - **quantity**: Sensitivity of solids volume fraction to solids mass fraction, d(phi)/d(w_s)
    - **value**: 2.57
    - **units**: dimensionless
    - **context**: At phi=0.5 for Cu with rho_b=1.10. A 0.5 wt% absolute error in the TGA-derived w_s propagates to 1.3 vol% error in phi_s. TGA repeatability of 0.1-0.2 wt% gives 0.26-0.51 vol%.
    - **source**: Derived analytically: d(phi)/d(w) = (b/rho_s + a/rho_b)/(a+b)^2 with a=w/rho_s, b=(1-w)/rho_b
  -
    - **quantity**: Sensitivity of solids volume fraction to binder density, d(phi)/d(rho_b)
    - **value**: 0.227
    - **units**: per (g/cm3)
    - **context**: At phi=0.5 for Cu. A 0.02 g/cm3 uncertainty in rho_b gives only 0.45 vol% in phi — so binder density is the LESS critical unknown; spend the effort on the mass balance.
    - **source**: Derived analytically: d(phi)/d(rho_b) = phi*b/(rho_b*(a+b))
  -
    - **quantity**: Copper oxidation mass-gain factors
    - **value**: +12.59 (Cu -> Cu2O), +25.18 (Cu -> CuO)
    - **units**: wt% of the copper mass
    - **context**: Stoichiometric. These are the terms that corrupt any air-atmosphere TGA of a copper green body.
    - **source**: Stoichiometry from atomic masses (Cu 63.546, O 15.999)
  -
    - **quantity**: Measured copper mass gain in air
    - **value**: +8, +14.4, +16.8
    - **units**: wt%
    - **context**: At 400, 600 and 800 C respectively for the copper powder used in a 60 vol% DLP formulation. Confirms the oxidation term is comparable in magnitude to the whole organic budget.
    - **source**: Roumanie et al., SN Appl. Sci. 3:55 (2021), DOI 10.1007/s42452-020-04049-3
  -
    - **quantity**: Char residue of a copper acrylate formulation pyrolysed in argon to 600 C
    - **value**: ~7
    - **units**: wt% (of the organic fraction)
    - **context**: Inert TGA does NOT fully volatilise the organics; complete burnout only in air. Design a two-stage TGA (Ar then H2 or O2) to capture the full budget.
    - **source**: Roumanie et al., SN Appl. Sci. 3:55 (2021), DOI 10.1007/s42452-020-04049-3
  -
    - **quantity**: Residual resin after 400 C / 4 h in air
    - **value**: 10-19
    - **units**: wt% of the original resin
    - **context**: i.e. isothermal air debinding at 400 C for 4 h is NOT complete; the remainder is burned off during ramp to sintering.
    - **source**: Roumanie et al., SN Appl. Sci. 3:55 (2021), DOI 10.1007/s42452-020-04049-3
  -
    - **quantity**: Residual carbon in sintered copper vs debinding atmosphere
    - **value**: air 400C: 0.018; H2: 0.25; Ar / vacuum / 600 ppm O2 / 5% O2-Ar: ~0.36
    - **units**: wt% C
    - **context**: After sintering in H2 at 1050 C. Raw ECKA copper powder reference = 0.018 wt% C. Air debinding is the only route that returned to powder-level carbon.
    - **source**: Roumanie et al., SN Appl. Sci. 3:55 (2021), DOI 10.1007/s42452-020-04049-3
  -
    - **quantity**: Phosphorus in the copper powder / in the sintered part
    - **value**: 0.02-0.025 (powder, DHP grade) ; 0.035 (sintered, BAPO formulation)
    - **units**: wt% P
    - **context**: The BAPO photoinitiator ADDED ~0.01 wt% P. Thermal conductivity fell from 250-270 to ~160-180 W/m/K. Quantify P by ICP-OES on BOTH the recovered powder and the sintered part to separate powder-borne from binder-borne phosphorus.
    - **source**: Roumanie et al., SN Appl. Sci. 3:55 (2021), DOI 10.1007/s42452-020-04049-3
  -
    - **quantity**: Copper powder used in the reference DLP copper work
    - **value**: d50 = 22, d90 = 42
    - **units**: um
    - **context**: ECKA Granules DHP (deoxidised high phosphorus) copper. Your Lithoz 2M30 slurry at ~30 um pixel will almost certainly use a FINER powder (likely d50 < 10 um) — measure it.
    - **source**: Roumanie et al., SN Appl. Sci. 3:55 (2021), DOI 10.1007/s42452-020-04049-3
  -
    - **quantity**: Incus LMM standard metal powder size range
    - **value**: 0-25
    - **units**: um
    - **context**: MIM-grade gas-atomised spherical powder; the metal-photopolymer AM benchmark
    - **source**: Harakaly et al., J. Jpn. Soc. Powder Powder Metall. 72 (2025) S1227, DOI 10.2497/jjspm.16C-T11-08
  -
    - **quantity**: Linear sintering shrinkage of DLP copper
    - **value**: ~19
    - **units**: %
    - **context**: Reference copper DLP parts. Back-solving 1-(phi_green/D_f)^(1/3) = 0.19 with D_f = 0.94 gives phi_green = 0.50, i.e. the green body had ~17% porosity relative to its 60 vol% slurry loading — a useful consistency check for your own measurements.
    - **source**: Roumanie et al., SN Appl. Sci. 3:55 (2021), DOI 10.1007/s42452-020-04049-3; back-calculation derived here
  -
    - **quantity**: Predicted linear shrinkage for a pore-free Cu green body
    - **value**: 17.2 (phi=0.55, D_f=0.97) / 15.8 (phi=0.58, D_f=0.97) / 15.4 (phi=0.60, D_f=0.99)
    - **units**: % linear
    - **context**: Isotropic, eps = 1 - (phi_green/D_f)^(1/3). Volumetric equivalents 43.3 / 40.2 / 39.4 %. Use as the sanity bound on your dilatometry.
    - **source**: Derived arithmetic
  -
    - **quantity**: Photoinitiator content in LCM slurries
    - **value**: <1
    - **units**: wt%
    - **context**: Stated by Lithoz/TU-Wien for LCM. Wider VPP literature: 0.01-10 wt%, commonly 0.5-1 wt%; the copper DLP reference used 5 wt% of the photocurable fraction (MMMP + BAPO).
    - **source**: Stampfl et al., MRS Commun. 13 (2023) 786; Roumanie et al. SN Appl. Sci. 3:55 (2021)
  -
    - **quantity**: Dispersant loading in comparable ceramic VPP slurries
    - **value**: 3
    - **units**: wt% on powder
    - **context**: Solsperse 41000 at 3 wt% on ceramic powder; BYK-111 at 3 wt% on modified AlN powder. Expect 1-5 wt% on powder for the Lithoz copper slurry.
    - **source**: Zhang et al., Materials 18 (2025) 4004, DOI 10.3390/ma18174004; Kuang et al., Polymers 17 (2025) 2769, DOI 10.3390/polym17202769
  -
    - **quantity**: Py-GC/MS diagnostic ions
    - **value**: acrylate m/z 99 (base) and 55 (acryloyl); methacrylate m/z 113 (base) and 69 (methacryloyl); bisphenol-A m/z 213
    - **units**: m/z
    - **context**: Pyrolysis at 750 C, 15 s, 20000 C/s, ZB-1HT 30 m x 0.25 mm x 0.10 um, He 20 psig, injector 300 C, split 1:50, EI 70 eV, scan 45-650. Methacrylates regenerate monomer (unzipping); acrylates do not (beta-scission) — absence of monomer is itself diagnostic.
    - **source**: Belbakra et al., Polymers 13 (2021) 4349, DOI 10.3390/polym13244349
  -
    - **quantity**: ATR-FTIR diagnostic bands for the binder classes
    - **value**: 1720 (ester C=O); 1636/1620 and 810 (residual acrylate C=C); 1408 (acrylate CH2 twist); 3330-3400 (urethane N-H); ~1530 and 1240 (urethane amide II / amide III); 1250 (P=O); 1000-1050 (P-O-C); 940-1100 (phosphate P-O)
    - **units**: cm-1
    - **context**: Use to fingerprint the extractable sol fraction and the crosslinked gel separately; the 1636/810 pair also gives double-bond conversion by internal-standard ratioing against 1720.
    - **source**: Compiled from the urethane-acrylate FTIR literature (e.g. Prog. Org. Coat. study of waterborne UV-curable polyurethane acrylates, https://www.sciencedirect.com/science/article/abs/pii/S0300944016302843) and phosphate-band assignments; acrylate 1635/812 cm-1 assignment widely reported
  -
    - **quantity**: Kinetic parameters for an HDDA/HEA/PPTTA ceramic VPP resin (3-component DAEM)
    - **value**: E0 = 62.1/215.3/233.1 kJ/mol with sigma = 0.73/2.66/29.03 and log10 A = 8/17/19, mass fractions 0.03/0.64/0.34 (HEA-HDDA); E0 = 102.5/128.1/238.3 with sigma 8.26/150.14/6.63 and fractions 0.11/0.04/0.85 (HDDA-PPTTA)
    - **units**: kJ/mol; log10(1/s); fraction
    - **context**: TGA at 5 K/min, N2 50 mL/min, 8 mg, 35-650 C, TGA/DSC3+. R^2 > 0.9999. Gives you a literature prior for the binder pyrolysis activation energies before you measure your own.
    - **source**: Zhang et al., Materials 18 (2025) 4004, DOI 10.3390/ma18174004
  -
    - **quantity**: Safe debinding heating rate for a 52 vol% AlN VPP green body
    - **value**: 0.5
    - **units**: C/min
    - **context**: To 550 C, 3 h dwell, vacuum. Rates of 1-5 C/min produced progressive cracking from trapped decomposition gases. A lower bound to anchor your copper cycle design.
    - **source**: Kuang N., Zhao W., Wu J., Polymers 17 (2025) 2769, DOI 10.3390/polym17202769
  -
    - **quantity**: scCO2 extractable fraction of a ceramic VPP print
    - **value**: ~90 wt% of the dissolvable resin fraction in 2 h; creates 21 vol% nanoporosity (ceramic/polymer) or 33 vol% (pure polymer)
    - **units**: wt% / vol%
    - **context**: Quantifies the NON-CROSSLINKED (sol) portion of a Lithoz-class green body — directly the non-reactive solvent + unreacted monomer + dispersant + photoinitiator you want to identify.
    - **source**: Nurmi et al., SSRN 4647233 / Additive Manufacturing (2024) — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4647233 (DOI unverified)
  -
    - **quantity**: LCM cure-depth criterion
    - **value**: cure depth >= 2 x layer thickness
    - **units**: dimensionless
    - **context**: Required for adequate interlayer bonding; insufficient bonding causes delamination during debinding. Layer thickness 25-50 um is typical for load-bearing LCM parts.
    - **source**: Stampfl et al., MRS Commun. 13 (2023) 786, DOI 10.1557/s43579-023-00444-0
  -
    - **quantity**: Copper UV transmission cut-off vs loading
    - **value**: >20
    - **units**: vol% Cu
    - **context**: Above ~20 vol% copper loading, transmission through the suspension drops dramatically, but photopolymerisation remains efficient within the cured layer; cure depth depends on the particle oxidation state.
    - **source**: Materials Today Communications (2023), https://www.sciencedirect.com/science/article/abs/pii/S2352492823002854
- **models_or_methods**:
  -
    - **name**: Closed mass/volume balance: slurry density + reduce-and-weigh burnout -> binder density, solids loading, green porosity
    - **formulation**: Let rho_s = metal skeletal density (He pycnometry on the recovered powder, ASTM B923; Cu = 8.96 g/cm3), rho_b = organic-phase density (unknown), rho_sl = LIQUID slurry density (oscillating U-tube or liquid pycnometer, 20 C, degassed), w_s = solids mass fraction.

(1) Burnout: w_s = m_metal,final / m_green,initial
    run TGA/muffle: Ar to 600 C (pyrolysis), then switch to Ar-5%H2 at 600-700 C and hold to constant mass (gasify the ~7 wt% char), cool in Ar. Verify residue is metallic by XRD + LECO O.
(2) Binder density:  rho_b = (1 - w_s) / ( 1/rho_sl - w_s/rho_s )
(3) Solids volume fraction:  phi_s = (w_s/rho_s) / ( w_s/rho_s + (1-w_s)/rho_b )
(4) Organic volume fraction:  phi_b = 1 - phi_s ;  organic mass fraction w_b = 1 - w_s
(5) Theoretical (pore-free) green density: rho_th = 1 / ( w_s/rho_s + (1-w_s)/rho_b )
(6) Green porosity from measured bulk density rho_bulk (geometric on a printed prism, or Archimedes with a wax/paraffin seal, or micro-CT):
    P_green = 1 - rho_bulk/rho_th
(7) Metal volume fraction actually present in the green body:
    phi_Cu,green = rho_bulk * w_s / rho_s
(8) Predicted isotropic linear sintering shrinkage to final relative density D_f:
    eps_L = 1 - (phi_Cu,green / D_f)^(1/3) ;  eps_V = 1 - phi_Cu,green/D_f

CONSISTENCY CHECK (do this first, on LithaLox numbers, to validate your lab): rho_sl = 2.52, phi = 0.49, rho_Al2O3 = 3.98 -> rho_b = 1.117 g/cm3, w_b = 22.6 wt%.
    - **when_to_use**: This is the backbone determination. Do it before any spectroscopy. It gives solids loading, binder content, binder density and green porosity — the four numbers your thermal/densification simulation needs — without knowing a single chemical name.
    - **inputs_needed**: Liquid slurry (>=5 mL, homogenised, degassed) for rho_sl; >=5 printed+cleaned green specimens (>=50 mg each, preferably >200 mg for muffle burnout) for w_s; recovered powder for He pycnometry and laser diffraction; a balance with >=0.01 mg readability; Ar and Ar-H2 supply; TGA with reactive-gas capability (or a tube furnace + analytical balance for the large-sample variant).
    - **limitations**: (a) Assumes all organics volatilise and no metal oxidises — you MUST use inert/reducing, never air. (b) The non-reactive solvent partially evaporates during printing, cleaning and storage, so w_s of the GREEN BODY != w_s of the SLURRY; measure both and report the difference as the solvent delta. (c) Archimedes on a green body requires sealing (wax or thin parylene) or the liquid infiltrates the open porosity; mercury pycnometry is the classical benchmark but is a hazard. (d) rho_s of the as-received powder may be depressed by a surface oxide; He pycnometry on virgin vs recovered powder quantifies this.
    - **source**: Derived; validated against Lithoz Material Overview 2021/2 + Ożóg et al. J. Ceram. Sci. Technol. (2019) DOI 10.4416/JCST2019-00023; ASTM B923 for skeletal density
  -
    - **name**: Error propagation for the solids-loading determination
    - **formulation**: With a = w_s/rho_s and b = (1-w_s)/rho_b, S = a + b, phi = a/S:

  d(phi)/d(w_s)   = ( b/rho_s + a/rho_b ) / S^2
  d(phi)/d(rho_b) = phi * b / ( rho_b * S )
  d(phi)/d(rho_s) = -( w_s/rho_s^2 ) * b / S^2

  sigma_phi^2 = (d(phi)/d(w_s))^2 sigma_ws^2 + (d(phi)/d(rho_b))^2 sigma_rhob^2 + (d(phi)/d(rho_s))^2 sigma_rhos^2

Evaluated for Cu at phi = 0.50 (w_s = 0.8907, rho_b = 1.10):
  d(phi)/d(w_s)   = 2.567      -> sigma_ws = 0.005 gives sigma_phi = 0.0128 (1.3 vol%)
  d(phi)/d(rho_b) = 0.227      -> sigma_rhob = 0.02 gives sigma_phi = 0.0045 (0.45 vol%)
  d(phi)/d(rho_s) = -0.028     -> negligible

For rho_b itself, propagate from (2):
  d(rho_b)/d(rho_sl) = (1-w_s) / ( rho_sl^2 (1/rho_sl - w_s/rho_s)^2 )
  d(rho_b)/d(w_s)    = [ -(1/rho_sl - w_s/rho_s) + (1-w_s)/rho_s ] / (1/rho_sl - w_s/rho_s)^2
    - **when_to_use**: To set the measurement budget. It tells you that the TGA/burnout mass fraction dominates the error and that chasing rho_b to three decimals is wasted effort.
    - **inputs_needed**: Replicate statistics: >=5 burnout specimens, >=3 slurry density measurements, balance calibration certificate, TGA buoyancy blank run under identical gas/rate.
    - **limitations**: Assumes uncorrelated errors. In practice w_s and rho_b are correlated through the shared solvent-evaporation systematic; report a sensitivity band rather than a single sigma if the solvent delta is large.
    - **source**: Derived analytically
  -
    - **name**: Atmosphere-resolved TGA/DTG/DSC triplet for a metal-filled green body
    - **formulation**: Run the SAME specimen mass and heating rate in three atmospheres and subtract:

  Inert (Ar or N2, >=50 mL/min):   dm/m0 = -w_b * (1 - chi_char)
  Reducing (Ar-5%H2 or 3%H2-N2):   dm/m0 = -w_b * (1 - chi_char') - w_ox * f_red   (f_red = 0.1259 for Cu2O, 0.2518 for CuO reduction, referenced to the metal)
  Oxidising (air or 20%O2-N2):     dm/m0 = -w_b + w_s * g(T),  g = 0.1259 (Cu->Cu2O) or 0.2518 (Cu->CuO)

The DIFFERENCE (air - inert) at any T isolates the metal oxidation term and hence the accessible specific surface of the powder.
The DIFFERENCE (reducing - inert) at T < 300 C quantifies the pre-existing surface oxide on the as-received powder (gives w_ox independently of LECO).

Multi-rate protocol: beta = 1, 2, 5, 10, 20 K/min in inert, for isoconversional kinetics.
Heating rates must be low enough that the Biot/gas-transport regime is not rate limiting: copper's very high k (~400 W/m/K) makes the green body near-isothermal, so unlike ceramics the rate limit is GAS PERMEATION, not heat conduction.
    - **when_to_use**: Immediately after the mass balance. The inert run gives the organic budget; the air run gives the oxidation penalty; the reducing run gives the starting oxide and the char-gasification window.
    - **inputs_needed**: TGA-DSC (simultaneous) with reactive-gas/H2-safe hardware (e.g. NETZSCH H2 SecureBox class), 3 atmospheres, matched crucibles (alumina, NOT platinum — Pt catalyses acrylate oxidation and is attacked by reduced Cu), blank buoyancy runs, 50-200 mg specimens to get adequate signal on a 7-13 wt% organic fraction.
    - **limitations**: (a) Copper alloys with Pt/Rh crucibles above ~600 C. (b) H2 + Cu2O at temperature is exactly the hydrogen-embrittlement (steam-void) reaction — do the H2 runs only on specimens you can sacrifice, and keep dew point controlled. (c) Small specimen TGA does not reproduce the gas-transport limitation of a real thick part; scale with a thermogravimetric run on a full-size part in a furnace on a load cell if possible.
    - **source**: Roumanie et al., SN Appl. Sci. 3:55 (2021) DOI 10.1007/s42452-020-04049-3 (oxidation gains, char yield, atmosphere-dependent carbon); NETZSCH application notes on CuO/Cu redox TGA under H2 (https://analyzing-testing.netzsch.com/en/application-literature/thermogravimetric-analysis-of-redox-reaction-of-cuo-and-cu-by-means-of-the-h2secure-box)
  -
    - **name**: Distributed Activation Energy Model (DAEM) / multi-pseudo-component pyrolysis kinetics
    - **formulation**: Gaussian activation-energy distribution per pseudo-component i:

  f_i(E) = 1/(sigma_i sqrt(2 pi)) * exp( -(E - E0_i)^2 / (2 sigma_i^2) )

  alpha_i(T) = 1 - Integral_0^inf exp( - Integral_T0^T (A_i/beta) exp(-E/(R T')) dT' ) f_i(E) dE

  m_cal(T) = m0 + Sum_i c_i alpha_i(T),   Sum_i c_i = total volatile fraction

Fit {E0_i, sigma_i, A_i, c_i} simultaneously to TGA curves at several beta. Literature priors for an acrylate ceramic VPP resin (3 components): E0 = 62 / 215 / 233 kJ/mol, sigma = 0.7 / 2.7 / 29, log10 A = 8 / 17 / 19.

Cross-check with model-free isoconversional methods on the multi-rate data:
  Friedman (differential):  ln( beta d(alpha)/dT ) = ln( A f(alpha) ) - E_alpha/(R T)
  KAS:                      ln( beta / T^2 )       = const - E_alpha/(R T)
  OFW (Doyle):              ln( beta )             = const - 1.052 E_alpha/(R T)
Agreement between Friedman/KAS/OFW E_alpha(alpha) and the DAEM E0_i validates the deconvolution.
    - **when_to_use**: To convert TGA into the source term for the debinding simulation: local volatile generation rate feeds the Darcy/Knudsen gas-pressure model that predicts cracking. Also the natural place to encode the solvent (low-E component) separately from the crosslinked network (high-E components).
    - **inputs_needed**: TGA at >=4 heating rates in inert, high-resolution DTG, and a nonlinear least-squares/global optimiser. Separate runs on (a) the full green body, (b) the scCO2- or Soxhlet-extracted green body (gel only), and (c) the recovered extract (sol only) to assign pseudo-components to real chemistry.
    - **limitations**: (a) Pseudo-components are mathematical, not chemical, unless anchored by extraction or TGA-MS. (b) First-order kinetics is assumed; autocatalysis by Cu (a strong oxidation catalyst) is not captured. (c) Copper surfaces catalyse acrylate decomposition, so kinetics fitted on the NEAT binder will not transfer to the filled system — always fit on the filled green body. (d) Fitted A and E are strongly correlated (compensation effect); do not interpret single parameters physically.
    - **source**: Zhang et al., Materials 18 (2025) 4004, DOI 10.3390/ma18174004; McAleer et al., 'Predicting photopolymer resin pyrolysis kinetics in ceramic vat photopolymerization additive manufacturing', J. Am. Ceram. Soc. (2025), DOI 10.1111/jace.20470
  -
    - **name**: Sol/gel separation by Soxhlet or supercritical CO2, then speciation of each fraction
    - **formulation**: Gel fraction:  G = m_dry,after_extraction / m_dry,before  (on the ORGANIC basis, i.e. correct for the metal):

  G_org = ( m_after - m_metal ) / ( m_before - m_metal ),  with m_metal = w_s * m_before

Soxhlet: acetone or THF (acrylate networks), 6-24 h, reflux; or scCO2 at ~40-60 C, 20-30 MPa, 2-15 h (non-destructive, no delamination reported, ~90 wt% of the dissolvable fraction in 2 h).
The EXTRACT (sol) = non-reactive solvent + unreacted monomer + dispersant + photoinitiator + photoproducts + dye. Concentrate under N2 and analyse by GC-MS (volatiles, solvent, monomers), LC-UV/MS (photoinitiator and its phosphine-oxide photoproducts, dye), 1H/13C solution NMR (monomer structure, ester/ether ratios), ATR-FTIR (functional-group confirmation).
The RESIDUE (gel) = crosslinked network + metal. Analyse by 13C CP-MAS ssNMR (backbone carbons, quaternary alpha-carbon presence distinguishes methacrylate from acrylate), Py-GC/MS at 750 C, and TGA.
    - **when_to_use**: This is the single highest-information experiment for identifying an unknown Lithoz binder, because Lithoz explicitly uses a non-reactive solvent that is NOT bound into the network and therefore extracts quantitatively.
    - **inputs_needed**: Printed+cleaned green specimens (multiple, >=1 g total organic basis), acetone/THF or a scCO2 rig, rotary evaporator/N2 blowdown, GC-MS, LC-MS, 400+ MHz NMR (solution and CP-MAS probe), ATR-FTIR.
    - **limitations**: (a) Copper catalyses acetone/THF peroxide chemistry and can leach into the extract — run a metal-free control (the same resin cured without powder, if Lithoz will supply it, or a blank slurry). (b) Extraction swells and can crack the green body; scCO2 avoids this. (c) Dispersants chemisorbed on the copper surface will NOT extract and will be under-reported — this is exactly the fraction that leaves residual C and heteroatoms; recover it by acid-digesting the powder after extraction and analysing the organic phase. (d) Quantifying the extract requires an internal standard added before extraction.
    - **source**: Nurmi et al., scCO2 debinding of ceramic VPP prints (SSRN 4647233 / ScienceDirect S2214860424001891); gel-fraction methodology from the Soxhlet crosslinking literature (e.g. Solar Energy Mater. Sol. Cells study of EVA crosslinking by Soxhlet, https://www.sciencedirect.com/science/article/abs/pii/S0927024815003827)
  -
    - **name**: Py-GC/MS fingerprinting of the crosslinked network
    - **formulation**: Conditions (validated): pyrolysis 750 C for 15 s at 20000 C/s, 10-100 ug sample; ZB-1HT (100% dimethylpolysiloxane) 30 m x 0.25 mm x 0.10 um; He at 20 psig; injector 300 C, split 1:50; EI 70 eV; scan m/z 45-650. No derivatisation.

Interpretation rules:
  - Methacrylate network -> depolymerisation ('unzipping'), strong regenerated monomer peaks; base fragment m/z 113, methacryloyl m/z 69.
  - Acrylate network -> beta-scission, NO recoverable monomer; fragments m/z 99 (acrylate) and 55 (acryloyl); dimers/trimers too heavy to elute.
  - Bisphenol-A-containing oligomer -> m/z 213 base peak.
  - Add to the target list: HDDA (M 226), TMPTA (M 296), TPGDA (M 300), PEGDA (M variable), ACMO (M 141, N-containing -> also flags in CHNS as N), HEA (M 116), NVP (M 111).
  - Photoinitiators: TPO (M 348) and BAPO/Irgacure 819 (M 418) both give 2,4,6-trimethylbenzoyl fragments and are better seen by LC-MS than Py-GC/MS.

Run in parallel: (i) the green body, (ii) the Soxhlet/scCO2 residue, (iii) the extract. Difference spectra assign peaks to bound vs free.
    - **when_to_use**: To name the monomers. Combine with the sol-fraction GC-MS: free monomer in the sol is directly identifiable; the network is identified by its fragment pattern.
    - **inputs_needed**: Pyrolyser-GC/MS, NIST library plus a custom library built from authentic standards of HDDA, TMPTA, TPGDA, PEGDA, ACMO, HEA, IBOA, urethane acrylates (e.g. CN series), TPO, BAPO, and the candidate dispersants.
    - **limitations**: (a) Acrylate networks are the HARD case: the absence of monomer means you infer composition from minor fragments, so authentic-standard cured films are essential for comparison. (b) Copper in the pyrolysis cup catalyses secondary reactions — pyrolyse the extracted/decalcified organic where possible, or accept a metal-catalysed fingerprint and match against a Cu-loaded standard. (c) Heavy oligomers (urethane acrylates) do not elute; detect these instead by ssNMR (urethane carbonyl ~157 ppm) and FTIR (N-H, amide II).
    - **source**: Belbakra Z., Napoli A., Cherkaoui Z.M., Allonas X., Polymers 13 (2021) 4349, DOI 10.3390/polym13244349
  -
    - **name**: Heteroatom accounting: ICP-OES + CHNS + inert-gas-fusion/combustion (LECO)
    - **formulation**: Measure the SAME element budget at four states: (0) virgin/recovered powder, (1) green body, (2) brown (debound) body, (3) sintered part.

Mass balance for element X (e.g. P):
  m_X,green = m_X,powder + m_X,binder
  -> binder-borne X per gram of green body:  x_binder = ( C_X,green - w_s * C_X,powder ) / (1 - w_s)

This converts a bulk ICP-OES number into the CONCENTRATION OF X IN THE BINDER, which is what identifies the additive.
Expected tracers: P -> acylphosphine-oxide photoinitiator (TPO/BAPO) and/or phosphate-ester dispersant; N -> amine synergist, ACMO/NVP, urethane, or a polyamide-type dispersant; S -> thiol/thioether or a sulfonate dispersant; Si -> siloxane defoamer/hybrid binder; Na/K -> polyacrylate salt dispersant; Zn/Ca -> carboxylate salts.

Carbon: CHNS combustion on the green body gives total organic C and the C/H/N/S ratio -> an elemental formula for the binder, e.g. C_x H_y O_z N_n. Combine with the TGA organic mass fraction:
  w_C,green = w_b * (12x / M_binder)
for a cross-check on w_b that is INDEPENDENT of the TGA.
Carbon/oxygen in the metal states: combustion-IR for C, inert-gas fusion for O (LECO). Track O in particular: it rises through debinding (oxidation) and must fall through H2 sintering.
    - **when_to_use**: Continuously, as the primary quantitative bridge between 'unknown binder' and 'property of the sintered copper'. The P measurement in particular is a direct predictor of final thermal/electrical conductivity.
    - **inputs_needed**: ICP-OES with microwave acid digestion (HNO3, optionally HNO3/H2SO4 or HNO3/HClO4 for complete organic destruction); CHNS analyser; combustion-IR carbon analyser and inert-gas-fusion oxygen/nitrogen analyser; matrix-matched copper CRMs.
    - **limitations**: (a) Standards mapping: ASTM E1019 covers C/S/N/O in steel, iron, nickel and cobalt alloys — its formal applicability to copper must be confirmed with the lab (ASTM E1941 covers C in refractory/reactive metals). Mark this as a lab-qualification item. (b) Organic P and N can be lost during open digestion; use closed-vessel microwave digestion. (c) CHNS oxygen is usually by difference and is unreliable for a metal-containing matrix — analyse the extracted organic fraction, not the green body, for the O determination. (d) Spectral interference of Cu on P lines in ICP-OES; use matrix-matched calibration.
    - **source**: ASTM E1019 (https://www.astm.org/Standards/E1019.htm); ASTM B923 (https://www.astm.org/Standards/B923.htm); P-in-copper conductivity effect from Roumanie et al., SN Appl. Sci. 3:55 (2021) DOI 10.1007/s42452-020-04049-3
  -
    - **name**: Powder recovery and re-characterisation (PSD, morphology, surface oxide)
    - **formulation**: Recover the metal from the green body WITHOUT sintering it:
  Ar to 450-500 C (pyrolysis) -> Ar-5%H2 at 250-350 C, hold (reduce surface oxide, well below any sintering onset) -> cool in Ar.
Then:
  - Laser diffraction per ISO 13320: disperse in IPA + 0.5-1 wt% of a known dispersant, sonicate 2 min; report d10/d50/d90 and compare to virgin powder. A shift to larger sizes = necking (recovery temperature too high) or agglomeration.
  - SEM/EDS: particle shape (gas-atomised spherical vs water-atomised irregular vs dendritic electrolytic), satellite fraction, surface films; EDS maps for P, O, and dispersant heteroatoms on the particle surface.
  - He pycnometry (ASTM B923): skeletal density; a value below 8.96 indicates retained oxide or closed porosity.
  - XPS or XRD on the as-received powder: Cu vs Cu2O vs CuO surface fraction (this also sets the cure depth per the LMM UV-penetration work).
  - BET specific surface area: sets both the oxidation rate in air debinding and the sintering driving force.
  - Micro-CT of the green body: bulk density, closed/open porosity, layer-interface defects — the boundary condition for the debinding gas-transport model.
    - **when_to_use**: In parallel with the mass balance. You cannot simulate sintering without the PSD, and you cannot design the debinding atmosphere without the surface oxide and BET area.
    - **inputs_needed**: Tube furnace with Ar and Ar-H2, laser diffractometer, SEM-EDS, He pycnometer, BET, XRD/XPS, micro-CT with ~3-10 um voxel.
    - **limitations**: (a) Copper at 350 C in H2 already shows measurable surface diffusion — verify by comparing d50 of recovered vs a directly ashed sample. (b) Laser diffraction assumes sphericity (Mie/Fraunhofer); for irregular powder cross-check with dynamic image analysis. (c) Micro-CT attenuation contrast between Cu and the organic phase is very high, which is good for porosity but causes beam hardening — use a Cu/Sn filter and a phantom.
    - **source**: ISO 13320:2020 (https://www.iso.org/standard/69111.html); ASTM B923; oxidation-state/cure-depth coupling from Materials Today Communications (2023) https://www.sciencedirect.com/science/article/abs/pii/S2352492823002854; micro-CT of VPP ceramics, e.g. https://www.sciencedirect.com/science/article/abs/pii/S1005030222001384
  -
    - **name**: Non-destructive first move: obtain and mine the Safety Data Sheet
    - **formulation**: Under EU CLP/REACH (Regulation 1907/2006 Annex II) and the GHS-aligned OSHA HazCom, Section 3 of an SDS must disclose hazardous components with identity and CAS number above concentration thresholds (generally 1 wt%, 0.1 wt% for CMR/sensitisers). Acrylates are skin sensitisers (Cat. 1) and TPO is now a Cat. 1B reprotoxin, so they are disclosable at or below 1 wt% and typically appear with a concentration RANGE.

Procedure: request the SDS for the R&D copper slurry directly from Lithoz (they are legally obliged to supply one for a supplied chemical product), plus the SDS for a commercial analogue (e.g. LithaLox, LithaCon) as a control. Cross-reference every CAS against the target list. Then use the SDS ranges as PRIORS and the analytics above to fix the values within them.
    - **when_to_use**: Day one, before any lab work. It is legally obtainable, free, and often narrows the monomer/photoinitiator identity to two or three CAS numbers.
    - **inputs_needed**: A formal request to Lithoz; an NDA if needed. Also ask explicitly for: the recommended thermal post-processing program (even as a 'starting point'), the powder supplier/grade, and the nominal solids loading in vol% — these are often disclosable even when the binder is not.
    - **limitations**: Non-hazardous components (many oligomers, some dispersants, the non-reactive solvent if non-hazardous) need not be disclosed; concentration ranges are broad; an R&D material may ship with a minimal or generic SDS. It never gives you the oligomer molecular weight or the dispersant architecture.
    - **source**: EU REACH Annex II SDS requirements and GHS Section 3 practice (https://www.chemsafetypro.com/Topics/GHS/GHS_safety_data_sheets.html); TPO reprotoxin reclassification noted in RadTech proceedings (https://radtech.org/proceedings/2014/papers/Photoinitiator/Sehnal%20-%20Novel%20Phosphine%20Oxide%20Photoinitiators.pdf)
- **open_questions**:
  - Is the Lithoz copper material an LCM-type LIQUID vat slurry (as the 2M30 implies) or an LMM-type feedstock that is solid at room temperature and melts at 35-60 C? This changes the binder architecture completely (non-reactive solvent + acrylate vs wax/solidification-agent + acrylate) and therefore the entire debinding strategy. Determine by DSC on the as-received material between 0 and 80 C and by simple rheometry at 20 C.
  - What is the identity and mass fraction of the non-reactive solvent? Lithoz confirms one exists in LCM slurries but names no chemistry. Candidates from the open literature are PEG-200/400, PPG-400, poly(oxyethylene) types, benzyl alcohol. Its boiling point and vapour pressure set the entire low-temperature stage of the cycle (the published LithaLox-class profile spends 66 h at 115 C). Resolve by headspace GC-MS on the fresh slurry plus TGA-MS below 250 C.
  - Does the copper slurry use BAPO/TPO (phosphorus-bearing) or a phosphorus-free photoinitiator? Roumanie et al. showed BAPO-derived P adds ~0.01 wt% P and can halve the thermal conductivity of sintered copper. If Lithoz has used BAPO, the achievable conductivity is capped regardless of how good the cycle is. Resolve by LC-MS of the extract plus ICP-OES for P on green vs powder.
  - Is the dispersant a phosphate ester (adds P), a polyacrylic acid / polyacrylate salt (adds Na/K), a polyether (BYK/Disperbyk/Solsperse polyether class, adds only C/H/O/N), or a thiol? Chemisorbed dispersant does not Soxhlet-extract and is a principal source of residual carbon on copper, which cannot form carbides. Resolve by XPS of the recovered powder surface plus ICP-OES/CHNS mass balance.
  - What is the actual solids loading of THIS slurry? The Lithoz commercial envelope is 40-63 vol% for ceramics, but copper's density, optical absorption and the >20 vol% transmission cut-off may have forced a different value. This is the single most important unknown and is resolvable in one week by the slurry-density + reduce-and-weigh route.
  - Is the copper powder DHP (phosphorus-deoxidised, ~0.02-0.05 wt% P) or OFHC/oxygen-free? DHP copper has intrinsically depressed conductivity independent of the binder. Resolve by ICP-OES on the virgin powder before blaming the photoinitiator.
  - What is the pre-existing surface oxide fraction on the as-received copper powder, and is it Cu2O or CuO? It controls cure depth (via scattering), the safe H2 exposure window (Cu2O + H2 at temperature is the hydrogen-embrittlement steam-void reaction), and the reducing-TGA baseline. Resolve by XRD/XPS + reducing TGA below 400 C.
  - What is the true char yield of this specific binder on a copper surface? Roumanie found ~7 wt% char in argon for a different acrylate system, but copper is a strong oxidation/decomposition catalyst and the value is formulation- and filler-specific. It determines whether an inert or slightly oxidising debinding step is required, which for copper is a direct trade against oxidation.
  - Does the green body contain residual unreacted monomer (a low double-bond conversion gradient through each layer, which Lithoz explicitly flags as a source of interlaminar cracking)? Quantify by FTIR 1636/810 vs 1720 cm-1 ratioing through the layer thickness, DSC residual exotherm, and the sol fraction from extraction.
  - What is the green-body bulk density and open-pore network geometry after drying? This sets the Darcy permeability that limits the safe heating rate during pyrolysis. Micro-CT plus Hg or gas porosimetry on dried green bodies; there is no published value for a copper LCM green body.
  - Can Lithoz be persuaded to release even a nominal starting thermal program, the powder grade, or the nominal solids loading under NDA? These are frequently disclosable even when the binder chemistry is not, and would collapse weeks of work.
  - Do the Incus/TU Wien copper results (Euro PM2024 paper M50, Cano Cano, Peritsch, Bosters, Anand, Gierl-Mayer, Harakaly) contain the sintered oxygen/carbon numbers and the debinding atmosphere? The abstract promises exactly this. Obtaining the full proceedings paper (EPMA) is a high-value, low-cost action.
  - What standard is formally appropriate for combustion carbon and inert-gas-fusion oxygen in COPPER? ASTM E1019 is written for steel/iron/nickel/cobalt; the correct copper-matrix method and the availability of matrix-matched CRMs need confirming with the analytical lab before the numbers can be defended in a paper.
- **references**:
  -
    - **citation**: Stampfl J., Schwentenwein M., Homa J., Prinz F.B., 'Lithography-based additive manufacturing of ceramics: Materials, applications and perspectives', MRS Communications 13 (2023) 786-794. DOI 10.1557/s43579-023-00444-0
    - **url**: https://doi.org/10.1557/s43579-023-00444-0
    - **why**: THE primary source on Lithoz binder architecture, written by Lithoz's own CTO/CEO and the TU Wien originator. Gives 45-60 vol% solids loading, PI <1 wt%, the existence of the non-reactive solvent, dyes as absorbers, 8-72 h thermal processing, 15-20 mm wall-thickness limit, the cure-depth >= 2x layer criterion, and the Dp = (2/3)(d50/(Q*phi)) scattering relation. Start here.
  -
    - **citation**: Lithoz GmbH, 'Material Overview — LCM Technology', company material folder, 2021/2
    - **url**: https://lithoz.com/wp-content/uploads/2022/08/LITHOZ_Material_Folder_EN.pdf
    - **why**: Manufacturer datasheet giving the actual solids loading of every Lithoz commercial slurry (40-63 vol%) plus slurry viscosities. This is the design envelope your unknown copper slurry sits inside, from the manufacturer's own hand.
  -
    - **citation**: Ożóg P., Blugan G., Kata D., Graule T., 'Influence of the Printing Parameters on the Quality of Alumina Ceramics Shaped by UV-LCM Technology', J. Ceram. Sci. Technol. (2019). DOI 10.4416/JCST2019-00023
    - **url**: https://www.ceramic-science.com/php/article_pdf.php?article_id=100699&hash=c6be80294a
    - **why**: Independent third-party confirmation of the LithaLox HP500 composition (49 vol%, 2.52 g/cm3, (meth)acrylate reactive binder + proprietary non-reactive solvent + dispersant + photoinitiators) and of the Lithoz-supplied debinding (to 900 C in air) and sintering (1600 C/2 h) programs. The 2.52 g/cm3 slurry density is what lets you back-calculate the binder density to 1.117 g/cm3.
  -
    - **citation**: Roumanie M. et al., 'Influence of debinding and sintering conditions on the composition and thermal conductivity of copper parts printed from highly loaded photocurable formulations', SN Applied Sciences 3:55 (2021). DOI 10.1007/s42452-020-04049-3
    - **url**: https://doi.org/10.1007/s42452-020-04049-3
    - **why**: The closest published analogue to your exact problem: 60 vol% copper in a named acrylate formulation, four resin variants, a systematic debinding-atmosphere study (air / H2 / Ar / vacuum / 600 ppm O2 / 5% O2-Ar), H2 sintering at 1050 C, and the C/O/P and thermal-conductivity outcomes. It also supplies the copper oxidation mass gains (+8/+14.4/+16.8 wt%) and the 7 wt% inert char yield you need to interpret your own TGA. Open-access PDF also at https://cea.hal.science/cea-03790772.
  -
    - **citation**: Belbakra Z., Napoli A., Cherkaoui Z.M., Allonas X., 'Analysis of Acrylic and Methacrylic Networks through Pyrolysis-GC/MS', Polymers 13 (2021) 4349. DOI 10.3390/polym13244349
    - **url**: https://pmc.ncbi.nlm.nih.gov/articles/PMC8708672/
    - **why**: The methodological reference for Py-GC/MS of crosslinked (meth)acrylate networks: exact pyrolysis/GC/MS conditions, the acrylate-vs-methacrylate discrimination rule, and the diagnostic ions (99/55 vs 113/69, 213 for bisphenol-A). This is how you name the monomers in a network that will not depolymerise.
  -
    - **citation**: Zhang et al., 'Pyrolysis Kinetics-Driven Resin Optimization for Enhanced Reliability in Ceramic Vat Photopolymerization Manufacturing', Materials 18 (2025) 4004. DOI 10.3390/ma18174004
    - **url**: https://pmc.ncbi.nlm.nih.gov/articles/PMC12429858/
    - **why**: Full worked multi-DAEM pyrolysis kinetics for HEA/HDDA/PPTTA ceramic VPP resins with a complete parameter table (E0, sigma, log A, c per pseudo-component) and the internal gas-pressure consequence. Gives you both the model formulation and literature priors before you have your own TGA data, plus a realistic slurry recipe (Omnirad 819 1 wt%, Solsperse 41000 3 wt%, 40 vol%).
  -
    - **citation**: McAleer et al., 'Predicting photopolymer resin pyrolysis kinetics in ceramic vat photopolymerization additive manufacturing', Journal of the American Ceramic Society (2025). DOI 10.1111/jace.20470
    - **url**: https://ceramics.onlinelibrary.wiley.com/doi/10.1111/jace.20470
    - **why**: State-of-the-art on predicting rather than merely fitting VPP resin pyrolysis kinetics — the natural citation for the kinetics chapter of your paper. Not retrievable in full here (paywalled); obtain via your library.
  -
    - **citation**: Harakaly G., Cano Cano S., Bosters J., Sperling C., Moedder D., Mitteramskogler G., 'Recent Advances in the Biomedical Field with the Lithography-based Metal Manufacturing Process', J. Jpn. Soc. Powder Powder Metall. 72 (2025) S1227-S1231. DOI 10.2497/jjspm.16C-T11-08
    - **url**: https://www.jstage.jst.go.jp/article/jjspm/72/Supplement/72_16C-T11-08/_pdf
    - **why**: Open-access description of the LMM metal-photopolymer process from Incus: feedstock solid at RT melting 35-60 C, decaking 40-80 C, 0-25 um MIM-grade powder, binder designated BMP18, MIM-equivalent debinding/sintering. Use it to decide whether your Lithoz copper material is an LCM slurry or an LMM feedstock — a fork that changes everything downstream.
  -
    - **citation**: Cano Cano S., Peritsch P., Bosters J., Anand A., Gierl-Mayer C., Harakaly G., 'Recent Advances Of Lithography-based Metal Manufacturing Of Copper', Euro PM2024, Malmö, Paper M50, ID 6281350 (Incus GmbH + TU Wien)
    - **url**: https://europm2024.com/wp-content/uploads/2024/02/Euro-PM2024-GROUP-3-MATERIALS-Abstracts-Book.pdf
    - **why**: The directly competing/adjacent work on copper in lithography-based metal AM, with named authors at Incus and TU Wien. Essential for the related-work section, for benchmarking, and as the obvious collaboration/contact route. Obtain the full proceedings paper from EPMA.
  -
    - **citation**: 'Lithography based Metal Manufacturing (LMM): Influence of particle size and composition of copper powder on UV light penetration', Materials Today Communications (2023)
    - **url**: https://www.sciencedirect.com/science/article/abs/pii/S2352492823002854
    - **why**: Establishes that copper suspension transmission collapses above ~20 vol% loading and that cure depth depends on the particle OXIDATION STATE. This couples your powder-surface characterisation to both the print parameters and the debinding design, and is a non-obvious result you should not rediscover.
  -
    - **citation**: Kuang N., Zhao W., Wu J., 'Effect of Debinding Process on Aluminum Nitride Ceramics Fabrication via Digital Light Processing 3D Printing', Polymers 17 (2025) 2769. DOI 10.3390/polym17202769
    - **url**: https://pmc.ncbi.nlm.nih.gov/articles/PMC12567068/
    - **why**: A complete, open, quantitative recipe-to-cycle example: named monomers with wt% (ACMO 56.7 / DEGDA 2.7 / TMPTA 40.6), TPO 3 wt%, BYK-111 3 wt%, 52 vol% solids, and a systematic heating-rate study showing 0.5 C/min is required to avoid cracking. Use as the template for your own debinding-rate DOE and as a library entry for FTIR/GC-MS.
  -
    - **citation**: Nurmi N.N., Frankberg E.J., Rinne M.M.A., Sandblom T., Konnunaho P., Levänen E.R., 'Enabling fast debinding of ceramic vat photopolymerization prints with supercritical carbon dioxide as a solvent' (SSRN preprint 4647233; published in Additive Manufacturing, 2024)
    - **url**: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4647233
    - **why**: Quantifies the DISSOLVABLE (sol) fraction of a ceramic VPP green body and shows ~90 wt% of it is removable in 2 h by scCO2 with 21 vol% nanoporosity created, cutting a 101 h thermal cycle to 15 h scCO2 + 18 h thermal. This is simultaneously the cleanest analytical separation of the non-crosslinked binder components and a legitimate process innovation for your paper. DOI not verified here.
  -
    - **citation**: US 10,538,460 B2, 'Ceramic slurries for additive manufacturing techniques', General Electric Co.
    - **url**: https://patents.google.com/patent/US10538460B2/en
    - **why**: Not Lithoz, but the most explicit public patent disclosure of a highly-filled photopolymerisable ceramic slurry: named monomers (ethoxylated TMPTA, tricyclodecane dimethanol diacrylate, diurethane dimethacrylate, isobornyl acrylate, bisphenol-A ethoxylate diacrylate, multifunctional thiols), named photoinitiators (HMPP, BAPO, 1-hydroxycyclohexyl phenyl ketone), a worked 53 vol% example (46/20/34 parts + 2 parts BAPO) and a 45-75 vol% claimed range. Use it to build your candidate list and your GC-MS/FTIR standard library. Related family: US 11,390,563; US 11,572,313; US 10,023,500 (hybrid siloxane binders).
  -
    - **citation**: ASTM B923, 'Standard Test Method for Metal Powder Skeletal Density by Helium or Nitrogen Pycnometry'
    - **url**: https://www.astm.org/Standards/B923.htm
    - **why**: The standard that makes your He-pycnometry number defensible, including the outgassing procedures that matter when the powder surface carries adsorbed dispersant and solvent.
  -
    - **citation**: ASTM E1019, 'Standard Test Methods for Determination of Carbon, Sulfur, Nitrogen, and Oxygen in Steel, Iron, Nickel, and Cobalt Alloys by Various Combustion and Inert Gas Fusion Techniques'
    - **url**: https://www.astm.org/Standards/E1019.htm
    - **why**: The combustion/inert-gas-fusion (LECO) reference for the C/O/N budget. NOTE the matrix caveat: it is written for ferrous/Ni/Co alloys, so confirm the correct method and CRMs for a copper matrix with your lab (ASTM E1941 covers C in refractory/reactive metals) before publishing numbers.
  -
    - **citation**: ISO 13320:2020, 'Particle size analysis — Laser diffraction methods'
    - **url**: https://www.iso.org/standard/69111.html
    - **why**: Required for a defensible d10/d50/d90 on the powder recovered from the green body, and for the virgin-vs-recovered comparison that detects necking during your recovery step.
  -
    - **citation**: NETZSCH application note, 'Thermogravimetric Analysis of Redox Reaction of CuO and Cu by Means of the H2SecureBox'
    - **url**: https://analyzing-testing.netzsch.com/en/application-literature/thermogravimetric-analysis-of-redox-reaction-of-cuo-and-cu-by-means-of-the-h2secure-box
    - **why**: Practical instrumentation reference for running TGA on copper under hydrogen (the only way to get a clean organic mass balance on a Cu-filled green body), including the reference CuO->Cu mass loss of 20.1% (theoretical 20.11%) with a peak rate at 316 C that you can use as an instrument validation run.
  -
    - **citation**: 'Effect of non-reactive diluent on defect-free debinding process of 3D printed ceramics', Additive Manufacturing (2023)
    - **url**: https://www.sciencedirect.com/science/article/pii/S221486042300088X
    - **why**: Explains WHY Lithoz puts a non-reactive solvent in the slurry and what it does thermally: PPG-type diluents decompose before the main resin and form interconnected escape porosity. Directly informs how you should interpret and exploit the low-temperature TGA event in your material.
  -
    - **citation**: Sehnal P., 'Novel Phosphine Oxide Photoinitiators', RadTech proceedings (2014)
    - **url**: https://radtech.org/proceedings/2014/papers/Photoinitiator/Sehnal%20-%20Novel%20Phosphine%20Oxide%20Photoinitiators.pdf
    - **why**: Background on TPO/BAPO acylphosphine-oxide chemistry, typical use levels, and the regulatory reclassification pressure (TPO as Cat. 1B reprotoxin). Relevant both to identifying the photoinitiator and to anticipating that Lithoz may have substituted it — which matters because the substitute may or may not carry phosphorus.
  -
    - **citation**: 'Study of thermal degradation mechanism of binders for ceramic injection molding by TGA-FTIR'
    - **url**: https://www.researchgate.net/publication/331283133_Study_of_thermal_degradation_mechanism_of_binders_for_ceramic_injection_molding_by_TGA-FTIR
    - **why**: Methodological template for coupling TGA to FTIR on a filled binder system, and a reminder of a result that will bite you: oxide/metal powder surfaces retard binder degradation early and accelerate it in the later exothermic stage, so neat-binder kinetics do not transfer to the filled system.