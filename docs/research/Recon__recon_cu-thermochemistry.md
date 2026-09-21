- **summary**: **The single most important result: copper cannot be oxidised by H2/H2O at any attainable dew point.** This inverts the usual PM atmosphere problem and defines the whole process strategy.

Cu2O is an exceptionally weak oxide. The Cu/Cu2O equilibrium oxygen pressure is pO2_eq = 3.2e-19 atm at 400 C, 3.1e-11 at 700 C, 5.0e-7 at 1000 C, 1.7e-6 at 1050 C (computed from 4Cu+O2=2Cu2O, dG = -333,400 + 141.3T J/mol-O2; validated against the published Cu2O dissociation pressure of ~1e-8 atm at 900 C, my value 3.4e-8). Converting to a hydrogen buffer, the H2O/H2 ratio required to *oxidise* copper is 1.0e7 at 400 C, 1.3e5 at 700 C and 1.26e4 at 1000 C. That is 99.99% steam. Only ~79 ppm H2 in otherwise pure superheated steam keeps copper reduced at 1000 C. Expressed as critical dew point, the limit is above +120 C for every practical H2 fraction from 100% down to 0.1% across 300-1050 C. Linde's industrial Table 5 independently reports the Cu2O limit as ~0.5 vol% O2 / dew point +100 C in 100% H2 at 850 and 1120 C — i.e. off the practical scale, exactly as computed. **Consequence: for a copper feedstock you may humidify the atmosphere freely to gasify carbon; there is no oxidation penalty. The classic pO2-vs-T "window" that dominates Cr/Mn/Si steels does not bind here.**

The real binding constraints are three, and none of them is copper oxidation.

**(1) Inert gas is oxidising; only a reductant is safe.** With no H2, pO2 is fixed by H2O dissociation, pO2 = (pH2O/2K)^(2/3). N2 or Ar at dew point -40 C gives pO2 = 2.3e-14 atm at 400 C and 2.0e-10 at 700 C — five to nine orders of magnitude above pO2_eq. My model reproduces SKB's published value for N2+2.9%H2O at 580 C to within 5% (4.20e-10 vs 4e-10 atm). Even 1 ppm residual O2 oxidises copper below 1028 C; 5 ppm oxidises it at every solid-state temperature. Debinding copper in "inert" nitrogen or argon therefore oxidises the part.

**(2) Hydrogen + internal oxide = catastrophic blistering, not embrittlement in the classical sense.** Hydrogen permeates copper fast (Reiter 1993, valid 470-1200 K: D = 6.60e-7 exp(-37.4 kJ/RT) m2/s, giving 3.4 mm/h penetration at 400 C) but dissolves negligibly (0.01 wt-ppm at 1 bar, 400 C). It reduces Cu2O in situ to H2O, which cannot diffuse out. Reducing a Cu2O inclusion liberates 9.66 cm3/mol of free volume, so the steam pressure is 580 MPa at 400 C and 1095 MPa at 1000 C — one to two orders of magnitude above copper's flow stress. Hwang's dilatometry (Mater. Trans. 51, 2010) shows the onset at 673-723 K and up to 20% linear expansion at 1133 K in H2 for powder with 0.471 mass% O. Harper showed tough-pitch copper (>200 ppm O) embrittles in H2 up to 400 C, accelerating above 374 C (the critical temperature of water), and that OF copper (<1 ppm O) cannot be embrittled at all.

**(3) Carbon is the actual hard constraint, and it is kinetic, not thermodynamic.** Copper forms no carbide, so carbon must leave as gas. Thermodynamically every route is open: Cu2O + C -> 2Cu + CO has dG = -52 kJ/mol at 400 C falling to -155 kJ/mol at 1050 C (equilibrium pCO ~1e5 atm at 1000 C — this is the internal CO-bloating mechanism). C + H2O -> CO + H2 crosses zero at ~673 C, C + CO2 -> 2CO at ~695 C, and C + 2H2 -> CH4 is favourable *below* ~650 C. The problem is that copper is a poor methanation and poor steam-reforming catalyst, so graphitised binder char is kinetically stranded. Steam gasification becomes practically viable only above ~700-750 C, by which point copper surface diffusion has already begun closing porosity. This is the crux: **carbon must be gone before pore closure, and the only thermodynamically clean lever is deliberate water vapour addition, which costs nothing in oxidation terms.**

Targets: OFE C10100 <=5 ppm O (>=101% IACS), OF C10200 <=10 ppm O, ETP C11000 200-400 ppm O. Oxygen is a weak conductivity poison (-0.126 %IACS per 0.01 wt% O) and actually getters other impurities, so the O limit is set by blistering, not conductivity. Phosphorus is the dominant poison (-0.73 %IACS per 10 ppm), which is why the only published copper VPP study (Roumanie 2021, 60 vol% Cu DLP, air debind 400 C + H2 sinter, C = 0.018 wt%) reached only 250 W/m.K and blamed phosphorus from the BAPO photoinitiator. Given Lithoz slurries are almost certainly BAPO/TPO-cured, **residual phosphorus is a first-order risk for this project.** Finally, Cu vapour pressure is 2.7e-2 Pa at 1050 C, so hard vacuum sintering causes free evaporation; a >=100 Pa inert backfill is required.
- **key_facts**:
  -
    - **fact**: Copper cannot be oxidised by any practically attainable H2/H2O ratio. The critical dew point for Cu2O formation exceeds +120 C for H2 fractions from 100% down to 0.1% over the entire 300-1050 C range. Only ~79 ppm H2 in pure steam is enough to keep Cu reduced at 1000 C.
    - **source**: Computed this session from standard Ellingham fits; independently corroborated by Linde, 'Furnace atmospheres no. 6: Sintering of steels', Table 5, which gives the Cu2O limit as ~0.5 vol% O2 / dew point +100 C in 100% H2 at 850 and 1120 C. https://static.prd.echannel.linde.com/wcsstore/REN_Industrial_Gas_Store/Sintering-of-steels-brochure-EN.pdf
    - **confidence**: high
  -
    - **fact**: Conversely, inert gas WITHOUT a reductant is oxidising to copper. N2/Ar at dew point -40 C yields pO2 = 2.3e-14 atm at 400 C vs pO2_eq = 3.2e-19 atm — five orders of magnitude oxidising. Debinding copper in pure N2 or Ar will oxidise it.
    - **source**: Computed; validated against SKB R-15-06 Table 3-1 (N2+2.9%H2O at 580 C -> pO2 = 4e-10 atm; my model gives 4.20e-10 atm). https://skb.se/publikation/2485262/R-15-06.pdf
    - **confidence**: high
  -
    - **fact**: Copper forms no stable carbide; residual binder carbon can only leave as CO, CO2 or CH4. Cu2O + C -> 2Cu + CO is spontaneous from below 100 C and reaches dG = -155 kJ/mol at 1050 C, with equilibrium pCO ~1e5 atm at 1000 C. This is the internal CO-bloating mechanism when carbon and oxide coexist in a closed pore.
    - **source**: Computed this session from Ellingham fits for Cu2O and CO
    - **confidence**: high
  -
    - **fact**: Hydrogen + internal Cu2O produces steam at 580 MPa (400 C) to 1095 MPa (1000 C) in the free volume created by reduction (9.66 cm3 per mol H2O), one to two orders of magnitude above copper's flow stress. Blistering is thermodynamically unavoidable if oxide survives into the H2 exposure.
    - **source**: Computed from Cu2O density 6.0 g/cm3, Cu 8.96 g/cm3, ideal gas
    - **confidence**: high
  -
    - **fact**: Measured swelling onset in copper powder in H2 is 673-723 K (400-450 C), with up to 20% linear expansion peaking at ~1133 K for coarse powder containing 0.471 mass% O. Onset is lower (673 K) for fine powder due to shorter H diffusion distance.
    - **source**: Materials Transactions 51(12) 2010, 2251-2258, 'Swelling of Copper Powders during Sintering of Heat Pipes in Hydrogen-Containing Atmospheres'. https://www.jstage.jst.go.jp/article/matertrans/51/12/51_M2010151/_article
    - **confidence**: high
  -
    - **fact**: That study's recommendation: use copper powder with oxygen below 0.2 mass% and an atmosphere with LESS THAN 5 vol% H2 to minimise swelling. This directly contradicts the instinct to use pure H2.
    - **source**: Materials Transactions 51(12) 2010, 2251-2258
    - **confidence**: high
  -
    - **fact**: Tough-pitch copper (>200 ppm O) is embrittled by H2 heat treatment at temperatures up to 400 C, with the rate increasing sharply above ~374 C (the critical temperature of water, above which the product steam cannot condense). The embrittling reaction CANNOT be induced in oxygen-free copper (<1 ppm O).
    - **source**: Harper, as reviewed in SKI Report 99:44, 'The Effects of Impurities on the Properties of Copper', section 2.4. https://www.osti.gov/etdeweb/servlets/purl/20066161
    - **confidence**: high
  -
    - **fact**: Hydrogen permeates copper rapidly but dissolves negligibly: at 400 C, D = 8.3e-10 m2/s (penetration depth sqrt(4Dt) = 3.4 mm in 1 h) while equilibrium solubility at 1 bar is only 0.0096 wt-ppm (0.61 appm). Fast in, nothing retained — the damage is entirely via the internal water reaction.
    - **source**: Computed from Reiter et al. 1993 parameters (D0 = 6.60e-7 m2/s, Ed = 37.4 kJ/mol; Ks0 = 5.19 mol m-3 Pa-0.5, Es = 55.2 kJ/mol; valid 470-1200 K), tabulated in IntechOpen 'Interaction of Copper Alloys with Hydrogen', Table 1. https://cdn.intechopen.com/pdfs/30473/InTech-Interaction_of_copper_alloys_with_hydrogen.pdf
    - **confidence**: high
  -
    - **fact**: Carbon gasification crossover temperatures (unit activity): C + H2O -> CO + H2 becomes favourable at ~673 C; C + CO2 -> 2CO at ~695 C; C + 2H2 -> CH4 is favourable only BELOW ~650 C. Methanation is therefore a low-temperature route and steam gasification a high-temperature route, with a thermodynamic gap around 650-700 C.
    - **source**: Computed this session
    - **confidence**: medium
  -
    - **fact**: Copper is a poor catalyst for both methanation and steam reforming (unlike Fe, Ni, Co), so graphitised binder char on copper is kinetically stranded even where thermodynamics permits removal. This is the principal reason residual carbon is hard to eliminate from copper MIM/BJ/VPP parts.
    - **source**: unverified — mechanistic inference consistent with the observed difficulty; not directly sourced in this session
    - **confidence**: low
  -
    - **fact**: The only published vat-photopolymerisation copper study (60 vol% Cu DLP, air debind at 400 C + H2 sinter) achieved C = 0.018 wt% (180 ppm) but only 250 W/m.K thermal conductivity, attributed to PHOSPHORUS from the powder and from BAPO-type photoinitiators. Lithoz slurries are very likely BAPO/TPO-cured, making residual P a first-order risk.
    - **source**: Roumanie, Flassayer, Resch, Cortella, Laucournet, SN Applied Sciences (2021), DOI 10.1007/s42452-020-04049-3 (Gold OA, CC-BY). Abstract verified via Semantic Scholar API.
    - **confidence**: high
  -
    - **fact**: Copper phosphates (Cu3(PO4)2, Cu2P2O7) are MORE stable than copper oxides and form at lower pO2 than Cu2O. Phosphorus from the photoinitiator will therefore oxidise preferentially and survive any atmosphere that reduces Cu2O — it cannot be removed by atmosphere control.
    - **source**: SKB R-15-06, section 3.3 and experimental verification. https://skb.se/publikation/2485262/R-15-06.pdf
    - **confidence**: high
  -
    - **fact**: Oxygen in copper is only a weak conductivity poison (-0.126 %IACS per 0.01 wt% O) and actually getters other impurities into oxides, removing them from solid solution — ETP copper with 200-400 ppm O still meets >=100% IACS. The oxygen limit for this project is therefore set by BLISTERING and EMBRITTLEMENT, not by conductivity.
    - **source**: Smart, as reviewed in SKI Report 99:44 section 2.3; grade data from Wikipedia 'Oxygen-free copper' (C10100/C10200/C11000)
    - **confidence**: medium
  -
    - **fact**: Copper vapour pressure is 8.3e-3 Pa at 1000 C and 2.7e-2 Pa at 1050 C. Hard-vacuum sintering below ~0.03 Pa causes free evaporation of copper, condensing on furnace internals. A partial pressure backfill of >=100 Pa inert gas is required for vacuum sintering.
    - **source**: Computed from log10(P/Pa) = 14.129 - 17748/T - 0.7317 log10(T) (solid Cu, 298 K to Tm), CRC via Wikipedia 'Vapor pressures of the elements (data page)'
    - **confidence**: high
  -
    - **fact**: The Cu-Cu2O eutectic at ~1064-1066 C and ~0.39 wt% O (equivalently ~3.4 wt% Cu2O) lies BELOW typical copper sintering temperatures. If oxygen is not removed before reaching ~1065 C, a liquid oxide eutectic can form and cause slumping. Oxygen solubility in solid Cu is 0.015 wt% at 1050 C and 0.007 wt% at 600 C.
    - **source**: Archbutt, as reviewed in SKI Report 99:44 section 2.3 (reported there as '3.4% oxygen at 1064 C', which is consistent with 3.4 wt% Cu2O = 0.38 wt% O)
    - **confidence**: medium
  -
    - **fact**: In hydrogen, sintered copper reaches <0.01 mass% (<100 ppm) residual oxygen from starting powders of 0.193-0.471 mass% O — but reduction also occurred in N2 and vacuum to the same level, showing oxygen removal is not the differentiator; the damage from H2 is the RATE and LOCATION of the reduction, not its completeness.
    - **source**: Materials Transactions 51(12) 2010, Table 2
    - **confidence**: high
  -
    - **fact**: Oxide reduction onset temperatures in H2 for reference: Fe2O3 ~250 C, Fe3O4 >700 C, FeO >800 C, Cr2O3 >1060 C. Cu2O reduction by H2 has dG = -87 to -101 kJ/mol across 200-1050 C, i.e. it is thermodynamically trivial at ALL temperatures and is purely kinetically/transport limited.
    - **source**: Linde 'Furnace atmospheres no. 6' for the Fe/Cr values; Cu2O values computed this session
    - **confidence**: high
  -
    - **fact**: Residual carbon strongly inhibits copper densification — reported that small concentrations of carbonaceous matter virtually stopped shrinkage of copper preforms even when held near the melting point, with ~1500 ppm C reduced to 1000 ppm after a second sintering cycle reaching only 74% of theoretical density.
    - **source**: unverified — appeared in a Copper Development Association 'Powder Metallurgy: Production and Properties' page via search snippet; the page returned 404 when fetched directly and the numbers could not be confirmed at source
    - **confidence**: low
  -
    - **fact**: Copper powder surface oxide for AM is typically 2.5-9 nm thick, composed of CuO, Cu2O and Cu(OH)2 with Cu2O usually dominant; degraded/reused powder reached ~19 nm. Surface-bound oxygen on BJ-grade copper powder has been estimated at ~220 ppm.
    - **source**: S. Kazi, Licentiate thesis, Chalmers University of Technology, IMS-2025-6 (2025). https://research.chalmers.se/publication/546735/file/546735_Fulltext.pdf
    - **confidence**: medium
- **numbers**:
  -
    - **quantity**: Equilibrium oxygen partial pressure, Cu/Cu2O
    - **value**: 3.76e-30 (200 C); 3.24e-19 (400 C); 7.18e-16 (500 C); 2.73e-13 (600 C); 3.06e-11 (700 C); 1.42e-09 (800 C); 3.44e-08 (900 C); 5.04e-07 (1000 C); 1.66e-06 (1050 C)
    - **units**: atm
    - **context**: Pure Cu in equilibrium with pure Cu2O, 1 atm total. Above these values copper oxidises; below, Cu2O reduces.
    - **source**: Computed from dG = -333,400 + 141.3T J/mol-O2; anchor-validated against published ~1e-8 atm at 900 C (DoITPoMS) and SKB R-15-06
  -
    - **quantity**: Equilibrium H2O/H2 ratio at the Cu/Cu2O boundary
    - **value**: 1.04e7 (400 C); 1.64e6 (500 C); 3.97e5 (600 C); 1.28e5 (700 C); 5.12e4 (800 C); 2.39e4 (900 C); 1.26e4 (1000 C); 9.47e3 (1050 C)
    - **units**: dimensionless (pH2O/pH2)
    - **context**: Ratio ABOVE which copper oxidises. All values are unreachable in a real furnace — this is why copper cannot be oxidised in any H2-bearing gas.
    - **source**: Computed; corroborated by Linde Furnace atmospheres no. 6 Table 5
  -
    - **quantity**: Equilibrium CO2/CO ratio at the Cu/Cu2O boundary
    - **value**: 1.36e8 (400 C); 1.20e6 (600 C); 2.32e5 (700 C); 2.03e4 (900 C); 7.99e3 (1000 C)
    - **units**: dimensionless (pCO2/pCO)
    - **context**: Same conclusion as for H2/H2O: CO-bearing atmospheres are overwhelmingly reducing to copper.
    - **source**: Computed this session
  -
    - **quantity**: pO2 in inert gas (N2/Ar, no reductant) set by H2O dissociation
    - **value**: DP -40 C: 2.29e-14 (400 C), 1.95e-10 (700 C), 2.34e-08 (1000 C). DP -20 C: 9.21e-14 (400 C), 7.84e-10 (700 C). DP +24 C: 8.67e-13 (400 C), 4.25e-10 (580 C)
    - **units**: atm
    - **context**: Compare to pO2_eq above: inert gas is OXIDISING to copper below ~1000 C at every realistic dew point.
    - **source**: Computed via pO2 = (pH2O/2K)^(2/3); SKB R-15-06 reports 4e-10 atm for N2+2.9%H2O at 580 C vs my 4.20e-10
  -
    - **quantity**: O2 impurity level in inert gas at which copper oxidises
    - **value**: 0.1 ppm: oxidises below 938 C; 0.5 ppm: below 1000 C; 1 ppm: below 1028 C; 2 ppm: below 1058 C; >=5 ppm: oxidises at all solid-state temperatures
    - **units**: ppm O2 / C
    - **context**: Sets the leak-tightness and gas-purity requirement if any inert-only step is used
    - **source**: Computed this session
  -
    - **quantity**: dG for Cu2O + H2 -> 2Cu + H2O(g)
    - **value**: -87.2 (200 C); -90.4 (400 C); -95.2 (700 C); -99.9 (1000 C); -100.7 (1050 C)
    - **units**: kJ per mol Cu2O
    - **context**: Reduction of copper oxide by hydrogen is thermodynamically trivial at every temperature; the process is entirely kinetics- and transport-limited
    - **source**: Computed this session
  -
    - **quantity**: dG for Cu2O + C -> 2Cu + CO(g)
    - **value**: -19.9 (200 C); -51.6 (400 C); -99.0 (700 C); -146.5 (1000 C); -154.5 (1050 C)
    - **units**: kJ per mol Cu2O
    - **context**: Equilibrium pCO ~2.5e5 atm at 1000 C. Carbon and Cu2O cannot coexist — this is the internal CO-bloating / blistering driver
    - **source**: Computed this session
  -
    - **quantity**: Carbon gasification crossover temperatures (dG = 0, unit activities)
    - **value**: C + H2O -> CO + H2: ~673 C. C + CO2 -> 2CO: ~695 C. C + 2H2 -> CH4: ~650 C (favourable BELOW this)
    - **units**: C
    - **context**: Thermodynamic onset only; actual rates on copper are far slower than on Fe/Ni catalytic surfaces
    - **source**: Computed this session; CH4 line from dG = -74,600 + 80.8T J (2-term fit to 298 K data), so the CH4 crossover has ~+/-50 C uncertainty
  -
    - **quantity**: Internal steam pressure from H2 reduction of a confined Cu2O inclusion
    - **value**: 579 MPa (400 C); 665 (500 C); 837 (700 C); 1009 (900 C); 1095 (1000 C)
    - **units**: MPa
    - **context**: Free volume created by Cu2O -> 2Cu is 9.66 cm3 per mol H2O. Copper flow stress at these temperatures is ~10-100 MPa, so rupture is certain.
    - **source**: Computed from Cu2O density 6.0 g/cm3 (Wikipedia), Cu 8.96 g/cm3, ideal gas law
  -
    - **quantity**: Swelling onset temperature of copper powder in H2
    - **value**: 673-723 K (400-450 C); max expansion ~20% at ~1133 K for coarse powder with 0.471 mass% O; ~4% in N2
    - **units**: K / % linear
    - **context**: Loose-powder sintered copper compacts, dilatometry, four atmospheres (H2, N2-10%H2, N2, vacuum)
    - **source**: Materials Transactions 51(12) 2010, 2251-2258
  -
    - **quantity**: Hydrogen transport in pure copper (Reiter et al. 1993, valid 470-1200 K)
    - **value**: D0 = 6.60e-7 m2/s, Ed = 37.4 kJ/mol; Ks0 = 5.19 mol m-3 Pa-0.5, Es = 55.2 kJ/mol; Phi0 = 6.60e-6 mol m-1 Pa-0.5 s-1, E_Phi = 92.6 kJ/mol
    - **units**: see values
    - **context**: Pure Cu. Gives D = 8.27e-10 m2/s at 400 C and 1.93e-8 m2/s at 1000 C
    - **source**: IntechOpen, 'Interaction of Copper Alloys with Hydrogen', Table 1, citing Reiter et al. 1993
  -
    - **quantity**: Hydrogen penetration depth in copper, sqrt(4Dt), t = 1 h
    - **value**: 0.84 mm (200 C); 3.45 mm (400 C); 7.42 mm (600 C); 9.67 mm (700 C); 16.7 mm (1000 C)
    - **units**: mm
    - **context**: Shows a typical 2M30 part section is fully H2-saturated within minutes-to-an-hour at debinding temperature
    - **source**: Computed from the Reiter parameters above
  -
    - **quantity**: Equilibrium hydrogen solubility in copper at 1 bar H2
    - **value**: 0.0096 wt-ppm (400 C); 0.201 wt-ppm (700 C); 1.00 wt-ppm (1000 C)
    - **units**: wt ppm H
    - **context**: Extremely low — copper stores almost no hydrogen; damage is via the internal H2O reaction, not H retention
    - **source**: Computed from Ks0 = 5.19, Es = 55.2 kJ/mol (Reiter et al. 1993)
  -
    - **quantity**: Copper vapour pressure (solid)
    - **value**: 2.36e-5 Pa (800 C); 5.68e-4 (900 C); 8.26e-3 (1000 C); 1.70e-2 (1030 C); 2.70e-2 (1050 C); 4.72e-2 (1075 C); 5.75e-2 (1084 C)
    - **units**: Pa
    - **context**: log10(P/Pa) = 14.129 - 17748/T - 0.7317 log10(T), 298 K to Tm = 1357.77 K. Implies vacuum sintering needs >=100 Pa inert backfill to suppress evaporation and furnace contamination.
    - **source**: CRC Handbook coefficients via Wikipedia 'Vapor pressures of the elements (data page)'
  -
    - **quantity**: Copper powder oxygen contents and post-sinter residual
    - **value**: As-received: 0.471 mass% (coarse), 0.193 mass% (fine). After sintering: 0.005-0.008 mass% in H2, N2-10%H2, N2 and vacuum alike
    - **units**: mass%
    - **context**: Loose-powder copper compacts; recommendation given was powder O < 0.2 mass% and atmosphere H2 < 5 vol%
    - **source**: Materials Transactions 51(12) 2010, Table 2
  -
    - **quantity**: Copper grade oxygen limits and conductivity
    - **value**: C10100 (OFE): <=5 ppm O, >=101% IACS, 99.99% pure. C10200 (OF): <=10 ppm O, >=100% IACS. C11000 (ETP): 200-400 ppm O, >=100% IACS but H2-embrittlement-susceptible
    - **units**: ppm O / %IACS
    - **context**: Target for a sintered copper part intended for thermal/electrical duty; ETP-level oxygen is acceptable for conductivity but NOT if the part will ever see hot hydrogen
    - **source**: Wikipedia 'Oxygen-free copper' (ASTM/UNS grade data)
  -
    - **quantity**: Effect of oxygen on copper conductivity
    - **value**: -0.126 %IACS per 0.01 wt% (100 ppm) O — i.e. 400 ppm O costs only 0.50 %IACS
    - **units**: %IACS per wt%
    - **context**: Cu2O as a second phase. Confirms oxygen is a weak conductivity poison; the constraint is mechanical, not electrical
    - **source**: Smart, reviewed in SKI Report 99:44 section 2.3
  -
    - **quantity**: Effect of phosphorus on copper conductivity
    - **value**: -0.73 %IACS per 10 ppm P, up to 60 ppm (60 ppm P -> ~95.6% IACS). DHP copper C12200 at 0.015-0.040 wt% P is ~85% IACS
    - **units**: %IACS per ppm
    - **context**: P in solid solution. The dominant poison, and the likely origin of the 250 W/m.K result in the published copper VPP study. DHP figure is a standard handbook value.
    - **source**: Search-level sources; the -0.73%/10 ppm figure appeared in multiple secondary sources but was not traced to a primary reference in this session — treat as indicative
  -
    - **quantity**: Oxygen solubility in solid copper
    - **value**: 0.015 wt% at 1050 C; 0.007 wt% at 600 C
    - **units**: wt%
    - **context**: Excess oxygen above these limits is present as Cu2O particles — which are the blistering nucleation sites
    - **source**: Archbutt, reviewed in SKI Report 99:44 section 2.3
  -
    - **quantity**: Cu-Cu2O eutectic
    - **value**: ~1064-1066 C at ~0.39 wt% O (~3.4 wt% Cu2O)
    - **units**: C / wt%
    - **context**: Below normal copper sintering temperature — a hard upper bound on sintering temperature if oxygen has not been removed first
    - **source**: SKI Report 99:44 section 2.3 (reported there as 3.4% at 1064 C); the 0.39 wt% O conversion is mine
  -
    - **quantity**: Published copper vat-photopolymerisation result
    - **value**: 60 vol% Cu loading; air debind at 400 C + H2 sinter; C = 0.018 wt% (180 ppm); thermal conductivity 250 W/m.K (vs ~400 for pure Cu)
    - **units**: vol% / wt% / W m-1 K-1
    - **context**: The closest published analogue to the Lithoz 2M30 copper slurry. Low conductivity blamed on P from the powder and BAPO photoinitiators.
    - **source**: Roumanie et al., SN Applied Sciences (2021), DOI 10.1007/s42452-020-04049-3
  -
    - **quantity**: Linde industrial limit for avoiding Cu2O
    - **value**: ~0.5 vol% O2 (dew point +7 C) in 1% H2; ~0.5 vol% O2 (dew point +100 C) in 100% H2, at both 850 C and 1120 C
    - **units**: vol% O2 / C dew point
    - **context**: Industrial confirmation that the copper oxidation limit is off the practical scale. Contrast Cr2O3 at 100% H2, 850 C: 16 ppm O2 (dew point -51 C)
    - **source**: Linde, 'Furnace atmospheres no. 6: Sintering of steels', Table 5
  -
    - **quantity**: Cu2O thermochemical constants
    - **value**: dH_f(298) = -168.6 to -170.59 +/- 0.08 kJ/mol; melting point 1244 C; density 6.0 g/cm3
    - **units**: kJ/mol, C, g/cm3
    - **context**: The -170.59 value is a high-resolution emf measurement over 900-1300 K; the two-term Ellingham fit used here implies -166.7 kJ/mol, a ~2% linearisation offset
    - **source**: Wikipedia 'Copper(I) oxide'; emf value from the University of Michigan Deep Blue record for J. Chem. Thermodynamics (1989), 'Standard molar Gibbs free energy of formation for Cu2O'
- **models_or_methods**:
  -
    - **name**: Cu/Cu2O equilibrium oxygen partial pressure (Ellingham two-term form)
    - **formulation**: 4Cu(s) + O2(g) = 2Cu2O(s),  dG0(T) = -333,400 + 141.3*T   [J per mol O2]
At equilibrium K = 1/pO2, so dG0 = R*T*ln(pO2_eq)
  => ln(pO2_eq) = dG0(T)/(R*T)
  => log10(pO2_eq/atm) = (-333400 + 141.3*T)/(2.3026*R*T)
For CuO:  4CuO = 2Cu2O + O2 defines the upper (CuO/Cu2O) boundary; CuO is only stable at high pO2 and is irrelevant above ~1000 C in air.
    - **when_to_use**: Baseline for every atmosphere decision. Use to place the Cu/Cu2O line on a pO2-vs-T map, then overlay the actual furnace gas.
    - **inputs_needed**: Temperature only. For simulation, prefer full Cp-integrated data (NIST-JANAF / SGTE SSUB / Thermo-Calc) rather than the two-term fit.
    - **limitations**: The two-term fit assumes dH and dS constant. It implies dH_f(Cu2O) = -166.7 kJ/mol vs the measured -170.6, a ~2% offset that shifts log10(pO2) by ~0.3 at 900 C. Validated here against three independent anchors (DoITPoMS ~1e-8 atm at 900 C; SKB pO2; Linde Table 5) and found adequate for process-window work but NOT for precision oxygen-potential modelling.
    - **source**: Standard metallurgical thermodynamics (coefficients as commonly tabulated, e.g. Gaskell, 'Introduction to the Thermodynamics of Materials'). The specific coefficients could not be traced to a primary source in this session — they are validated by anchors, not by citation.
  -
    - **name**: Dew point to pH2O to pO2 conversion (the practical furnace control law)
    - **formulation**: Step 1 - Arden Buck saturation vapour pressure (Td in C, result in hPa, x100 for Pa):
  over water (Td >= 0):  pH2O = 6.1121*exp((18.678 - Td/234.5)*(Td/(257.14 + Td)))
  over ice   (Td <  0):  pH2O = 6.1115*exp((23.036 - Td/333.7)*(Td/(279.82 + Td)))
Step 2 - hydrogen buffer, 2H2 + O2 = 2H2O(g), dG0 = -492,900 + 109.6*T [J per mol O2]
  K = pH2O/(pH2 * pO2^0.5) = exp(-dG0/(2*R*T))
  => pO2 = ( pH2O / (pH2 * K) )^2
Step 3 - criterion: oxidising if pO2 > pO2_eq(T) from the model above.
Equivalently and more robustly, compare ratios directly:
  (pH2O/pH2)_eq = K(T) * sqrt(pO2_eq(T))     -- oxidise if actual ratio exceeds this
Inert gas with NO reductant (pH2 fixed only by H2O dissociation, pH2 = 2*pO2):
  pO2 = ( pH2O / (2*K) )^(2/3)
    - **when_to_use**: Every time you set or measure a furnace atmosphere. The ratio form is preferred because it is insensitive to total pressure and to the absolute accuracy of pO2_eq.
    - **inputs_needed**: Dew point (from a chilled-mirror or capacitive hygrometer at the furnace exhaust), H2 volume fraction, temperature, total pressure.
    - **limitations**: Assumes gas-phase equilibrium, which requires either catalysis or T > ~700 C. At low temperature the gas is frozen and the measured dew point reflects transport, not equilibrium. Buck is an empirical fit, accurate to ~0.05% over -80 to +50 C; extrapolation below -80 C dew point is unreliable and that is exactly the regime of dry bottled gas.
    - **source**: Buck equation: standard meteorological correlation (Arden Buck, 1981/1996). H2O Ellingham line: standard tabulation. Validated against SKB R-15-06 Table 3-1 to within 5%.
  -
    - **name**: Carbon removal reaction set for a carbide-free metal
    - **formulation**: Gasification routes (copper forms NO carbide, so these are the only exits):
  (a) C + O2 -> CO2                 dG0 = -394,100 - 0.84*T
  (b) 2C + O2 -> 2CO                dG0 = -223,400 - 175.3*T
  (c) C + H2O -> CO + H2            dG0 = 0.5*[(b) - dG0(H2O line)]   ; zero at ~673 C
  (d) C + CO2 -> 2CO (Boudouard)    dG0 = (b) - (a)                    ; zero at ~695 C
  (e) C + 2H2 -> CH4                dG0 ~ -74,600 + 80.8*T             ; zero at ~650 C, favourable BELOW
Internal oxide-carbon coupling (the bloating reaction):
  (f) Cu2O + C -> 2Cu + CO          dG0 = 0.5*[(b) - dG0(Cu2O line)] = 55,000 - 158.3*T
      => spontaneous above ~74 C; equilibrium pCO ~2.5e5 atm at 1000 C
    - **when_to_use**: To design the debinding segment. The key design question is which of (c), (d), (e) you intend to rely on, and whether the part is still open-porous when that reaction becomes viable.
    - **inputs_needed**: Temperature schedule, pH2O (dew point), pH2, pCO/pCO2 if a CO-bearing gas is used, and an estimate of char reactivity (from TGA of the actual Lithoz slurry).
    - **limitations**: These are THERMODYNAMIC criteria only. On copper the kinetics are the binding constraint: Cu is a poor methanation and steam-reforming catalyst, so real removal rates are far below what dG0 suggests. Reaction (e) also has ~+/-50 C uncertainty in its crossover because a 2-term fit anchored at 298 K was used. Rate constants for char gasification on copper were NOT found in this session and must be measured.
    - **source**: Reactions and Ellingham lines: standard. Crossover temperatures: computed this session.
  -
    - **name**: Steam-blistering (hydrogen disease) criterion for copper
    - **formulation**: Mechanism: H2 permeates Cu -> reduces internal Cu2O -> H2O forms -> H2O cannot diffuse in Cu -> pressurises.
Free volume created per mol H2O:
  dV = Vm(Cu2O) - 2*Vm(Cu) = 143.09/6.0 - 2*(63.546/8.96) = 23.85 - 14.19 = 9.66 cm3/mol
Steam pressure if fully confined:  p = R*T/dV
  => 579 MPa at 400 C, 1095 MPa at 1000 C
Failure criterion: blister/crack when p > sigma_flow(Cu,T) (~10-100 MPa at 400-900 C) => essentially ALWAYS.
H2 arrival time to depth x:  t ~ x^2/(4D),  D = 6.60e-7*exp(-37,400/(R*T)) m2/s
Safe-processing rule: the oxygen must be gone, or the part must be fully open-porous (so H2O escapes by Knudsen/viscous flow rather than pressurising), BEFORE H2 is admitted above ~400 C.
    - **when_to_use**: To decide WHEN in the cycle hydrogen may be introduced, and to set the maximum permissible oxygen in the green part.
    - **inputs_needed**: Oxygen content and its distribution (surface oxide vs dissolved vs discrete Cu2O), part section thickness, open-porosity fraction vs temperature, H2 partial pressure and admission temperature.
    - **limitations**: Assumes full confinement, which is the worst case; in an open-porous green body the H2O escapes and no damage occurs. The whole criterion therefore hinges on the pore-closure temperature, which must come from dilatometry/sintering simulation. Experimental onset is 673-723 K, consistent with this picture.
    - **source**: Mechanism and onset temperatures: Materials Transactions 51(12) 2010 and SKI Report 99:44 (Harper). Pressure calculation: mine, from standard densities.
  -
    - **name**: Copper evaporation loss and furnace contamination
    - **formulation**: log10(P_Cu/Pa) = 14.129 - 17748/T - 0.7317*log10(T)   [solid Cu, 298 K to Tm = 1357.77 K]
Langmuir free-evaporation flux (upper bound, into vacuum):
  J = alpha * P_Cu * sqrt( M / (2*pi*R*T) ),  M = 0.063546 kg/mol, alpha ~ 1
Suppression rule: evaporation is throttled when the inert backfill pressure greatly exceeds P_Cu, i.e. P_total >= ~100 Pa is ample at 1050 C (P_Cu = 0.027 Pa).
    - **when_to_use**: To decide vacuum vs partial-pressure vs flowing-gas sintering, and to predict condensation on furnace hot zone, thermocouples and windows.
    - **inputs_needed**: Sintering temperature and hold time, furnace pressure, exposed surface area, pumping speed.
    - **limitations**: Langmuir is a free-evaporation upper bound; real loss in flowing gas is diffusion-limited through the boundary layer and much lower. The vapour pressure correlation is for the SOLID; above 1084.6 C use the liquid branch, log10(P/Pa) = 10.855 - 16415/T.
    - **source**: CRC Handbook coefficients via Wikipedia 'Vapor pressures of the elements (data page)'; Langmuir equation is standard
  -
    - **name**: Recommended atmosphere strategy synthesised from the above
    - **formulation**: Stage 1 (RT - 400 C, binder pyrolysis): NOT inert. Use a slightly reducing but hydrogen-LEAN gas, e.g. N2 + 1-3% H2, to keep pO2 below the Cu/Cu2O line while keeping H2 too dilute to drive fast internal reduction. The part is fully open-porous here so H2O escapes freely.
Stage 2 (400 - 750 C, char removal): the leverage point. Because (pH2O/pH2)_eq for copper is 1e5-1e7, you may deliberately HUMIDIFY to dew point 0 to +30 C with 1-5% H2 and remain >10 orders of magnitude reducing to copper, while supplying H2O for C + H2O -> CO + H2. This is the elite move: free carbon gasification at zero oxidation cost.
Stage 3 (750 - 950 C, oxide cleanup before pore closure): dry out (dew point < -40 C), raise H2 to 5-25%, hold to strip residual O while porosity is still open.
Stage 4 (950 - 1050 C, densification): low or zero H2 (<5 vol%, per the Materials Transactions recommendation), or Ar backfill >= 100 Pa if vacuum. Stay below ~1060 C to avoid the Cu-Cu2O eutectic if any oxygen remains.
Verification: continuous exhaust-gas dew point + a mass spectrometer or NDIR on CO/CO2/CH4 to close the carbon balance in situ.
    - **when_to_use**: As the starting hypothesis for the DoE, not as a validated recipe.
    - **inputs_needed**: TGA-MS/FTIR of the actual Lithoz slurry in the candidate atmospheres (this is the single highest-value missing measurement), plus dilatometry to locate pore closure, plus LECO C/O on interrupted specimens.
    - **limitations**: UNVALIDATED for this specific proprietary feedstock. The humidified-debind step in particular is a thermodynamic deduction, not a demonstrated result on copper. Stages 2 and 4 are in tension (humidity helps carbon, H2 helps oxide but causes blistering) and the crossover must be set experimentally from the pore-closure temperature.
    - **source**: Synthesis by me from the computed thermodynamics plus the cited experimental sources; the staging logic itself is not from a single reference
- **open_questions**:
  - What is the char yield and pyrolysis signature of the actual Lithoz copper slurry binder? Everything downstream depends on this and it is unknown. Run TGA-MS and TGA-FTIR on the neat slurry AND on the cured green body in (a) N2, (b) N2+3%H2, (c) N2+3%H2 humidified to +20 C dew point, (d) air. The difference between (b) and (c) directly quantifies the value of the humidified-debind strategy.
  - Does the Lithoz slurry use a BAPO or TPO acylphosphine oxide photoinitiator, and at what loading? This sets the residual phosphorus, which is the dominant conductivity/thermal-conductivity poison and CANNOT be removed by atmosphere (copper phosphates are more stable than Cu2O). Ask Lithoz directly for the P content even if the full chemistry is confidential — it is a single number and they may release it. If P is present at >100 ppm the achievable thermal conductivity is capped well below pure copper regardless of how good the cycle is.
  - At what temperature does open porosity close in this specific system? This is the hinge of the entire cycle design — carbon and oxygen must both be gone before it. Measure by dilatometry plus interrupted-quench Archimedes/He-pycnometry, and cross-check against the divergence between pycnometer and Archimedes density (the method used in the Materials Transactions swelling study).
  - What are the actual gasification rate constants for this binder's char on a copper surface? The thermodynamic crossovers (673 C for steam, 695 C for Boudouard, 650 C for methanation) are established, but copper's poor catalytic activity means the kinetics may be 2-3 orders of magnitude slower than on iron. No rate data for char-on-copper was found in this session. Isothermal TGA in controlled pH2O at 600/700/800/900 C would give the Arrhenius parameters.
  - What is the oxygen content and surface oxide thickness of the copper powder in the slurry as supplied? Literature values for AM copper powder range 2.5-19 nm oxide and ~220 ppm surface-bound oxygen, but the actual value determines whether hydrogen can be used at all. Measure by XPS depth profiling plus inert-gas-fusion LECO on the as-received powder.
  - Can the humidified-debinding window be demonstrated experimentally on copper? The thermodynamics say you can run dew point +30 C at 1% H2 and still be >10 orders of magnitude reducing to copper. No published copper study appears to have exploited this. If it works, it is genuinely novel and is the paper.
  - What is the pore-closure-versus-blistering trade-off as a function of H2 fraction? The Materials Transactions study recommends <5 vol% H2 to avoid swelling, but oxide reduction wants more H2. A DoE over H2 fraction (0.5 / 2 / 5 / 25 / 100%) crossed with H2 admission temperature (300 / 500 / 700 / 900 C) would map this directly and is the core experimental matrix.
  - Is the Cu-Cu2O eutectic at ~1065 C actually reached in practice? If residual oxygen exceeds ~0.39 wt% locally at the sintering temperature, liquid forms below the normal sintering setpoint. Needs confirmation of the local (not bulk) oxygen level at temperature, and constrains the maximum safe sintering temperature.
  - What residual carbon level actually stops copper densification? The claim that small amounts of carbonaceous matter virtually stop shrinkage could not be verified at source (the CDA page 404s). This threshold is decisive for setting the debinding specification and should be established either from a traceable reference or by a dedicated experiment doping known carbon levels into copper compacts.
  - Should the first trials use vacuum with partial-pressure backfill rather than flowing gas? Copper vapour pressure of 0.027 Pa at 1050 C rules out hard vacuum, but a 100-1000 Pa Ar or Ar/H2 backfill gives better control of gas removal from the part interior than flowing gas at 1 atm. Worth one arm of the DoE.
- **references**:
  -
    - **citation**: Roumanie M., Flassayer C., Resch A., Cortella L., Laucournet R., 'Influence of debinding and sintering conditions on the composition and thermal conductivity of copper parts printed from highly loaded photocurable formulations', SN Applied Sciences, 2021. DOI 10.1007/s42452-020-04049-3 (Gold OA, CC-BY)
    - **url**: https://doi.org/10.1007/s42452-020-04049-3
    - **why**: THE closest published analogue to this project: 60 vol% copper DLP vat photopolymerisation, debinding and sintering study, residual C = 0.018 wt%, thermal conductivity 250 W/m.K, and the phosphorus-from-BAPO finding. Read this first. Metadata and abstract verified via Semantic Scholar API; the full PDF was blocked in this session and should be retrieved directly.
  -
    - **citation**: 'Swelling of Copper Powders during Sintering of Heat Pipes in Hydrogen-Containing Atmospheres', Materials Transactions, Vol. 51, No. 12 (2010), pp. 2251-2258. National Taiwan University (corresponding author K.S. Hwang).
    - **url**: https://www.jstage.jst.go.jp/article/matertrans/51/12/51_M2010151/_article
    - **why**: The key experimental paper on copper blistering: four atmospheres compared, dilatometry showing 673-723 K swelling onset and 20% peak expansion, oxygen contents before/after, and the explicit recommendation of <0.2 mass% O powder and <5 vol% H2. Open access, full text retrieved.
  -
    - **citation**: Linde, 'Furnace atmospheres no. 6: Sintering of steels', Expert Edition technical brochure, 60 pp.
    - **url**: https://static.prd.echannel.linde.com/wcsstore/REN_Industrial_Gas_Store/Sintering-of-steels-brochure-EN.pdf
    - **why**: Industrial primary reference. Table 5 gives maximum permissible O2 and dew point to avoid Cu2O in 1% and 100% H2 at 850 and 1120 C, independently confirming that copper oxidation is off the practical scale. Also gives oxide reduction onset temperatures in H2 for Fe/Cr and the dew-point/hydrogen buffering relationships.
  -
    - **citation**: SKB R-15-06, 'Oxidation of copper at low oxygen partial pressure' (Svensk Karnbranslehantering AB, 2015), 33 pp.
    - **url**: https://skb.se/publikation/2485262/R-15-06.pdf
    - **why**: Provides a measured/calculated pO2 for N2+2.9%H2O at 580 C (4e-10 atm) used here to validate the dew-point-to-pO2 model to within 5%, plus the critical finding that copper phosphates (Cu3(PO4)2, Cu2P2O7) are MORE stable than Cu2O and form at lower pO2 — directly relevant to the BAPO phosphorus problem. Full text retrieved.
  -
    - **citation**: SKI Report 99:44, 'The Effects of Impurities on the Properties of Copper' (Swedish Nuclear Power Inspectorate), 41 pp.
    - **url**: https://www.osti.gov/etdeweb/servlets/purl/20066161
    - **why**: Reviews Harper's hydrogen embrittlement experiments (TP copper >200 ppm O embrittled up to 400 C, accelerating above 374 C; OF copper cannot be embrittled), oxygen solubility in copper (0.015% at 1050 C), the Cu-Cu2O eutectic, and the -0.126 %IACS per 0.01 wt% O conductivity relation. Full text retrieved.
  -
    - **citation**: IntechOpen, 'Interaction of Copper Alloys with Hydrogen', Chapter 2, 20 pp. Table 1 compiles hydrogen transport parameters including pure Cu from Reiter et al. (1993).
    - **url**: https://cdn.intechopen.com/pdfs/30473/InTech-Interaction_of_copper_alloys_with_hydrogen.pdf
    - **why**: Source of the pure-copper hydrogen diffusivity, permeability and Sieverts constant Arrhenius parameters (D0 = 6.60e-7 m2/s, Ed = 37.4 kJ/mol; Ks0 = 5.19, Es = 55.2 kJ/mol; valid 470-1200 K) used for all penetration-depth and solubility calculations. Full text retrieved.
  -
    - **citation**: Kazi S., 'Evolution of Powder Surface Chemistry and Powder Properties during Powder-based Metal Additive Manufacturing', Licentiate thesis, Chalmers University of Technology, Technical report IMS-2025-6 (2025).
    - **url**: https://research.chalmers.se/publication/546735/file/546735_Fulltext.pdf
    - **why**: XPS characterisation of copper powder surface oxides for AM: CuO/Cu2O/Cu(OH)2 speciation, oxide layer thicknesses of 2.5 nm (virgin) to 9-19 nm (degraded). Sets expectations for the oxygen inventory on the powder in the slurry. Full text retrieved.
  -
    - **citation**: Wikipedia, 'Vapor pressures of the elements (data page)', copper entry, citing CRC Handbook (Alcock correlation).
    - **url**: https://en.wikipedia.org/wiki/Vapor_pressures_of_the_elements_(data_page)
    - **why**: Source of the copper vapour pressure correlation log10(P/Pa) = 14.129 - 17748/T - 0.7317 log10(T) for solid Cu and the liquid branch, used to rule out hard-vacuum sintering. The underlying primary source is C.B. Alcock's 'Vapor Pressure of the Metallic Elements' in the CRC Handbook, which should be consulted directly for the paper.
  -
    - **citation**: Wikipedia, 'Oxygen-free copper' — grade specifications C10100 (OFE), C10200 (OF), C11000 (ETP).
    - **url**: https://en.wikipedia.org/wiki/Oxygen-free_copper
    - **why**: Convenient summary of the oxygen limits (5 / 10 / 200-400 ppm) and IACS minima that define the quality targets, plus the steam-embrittlement mechanism. Secondary source — verify final specification numbers against ASTM B170 / B187 / UNS before publishing.
  -
    - **citation**: MIT 2.813 course reading, 'Ellingham Diagrams'.
    - **url**: https://web.mit.edu/2.813/www/readings/Ellingham_diagrams.pdf
    - **why**: Clean statement of the three uses of the Ellingham diagram and the nomographic pO2, H2/H2O and CO/CO2 scale construction. Useful as the methods citation for the process-window figure in a paper. Full text retrieved.
  -
    - **citation**: DoITPoMS (University of Cambridge), 'Ellingham Diagrams' teaching and learning package.
    - **url**: https://www.doitpoms.ac.uk/tlplib/ellingham_diagrams/printall.php
    - **why**: Source of the independent anchor value used to validate the model here: the dissociation pressure of Cu2O is about 1e-8 atm at 900 C (computed value 3.4e-8). Retrieved via search snippet only — the page itself returned 403 in this session, so re-verify before citing.
  -
    - **citation**: SKB TR-10-30, Korzhavyi P.A. and Johansson B., 'Thermodynamic properties of copper compounds with oxygen and hydrogen from first principles', Royal Institute of Technology / SKB, February 2010.
    - **url**: https://skb.com/publication/1997718/TR-10-30.pdf
    - **why**: DFT formation energies for Cu2O, CuO and CuH, with comparison to the experimental dH_f(Cu2O) = -169 kJ/mol. Useful for justifying the thermodynamic dataset choice and for the CuH question (copper hydride is not stable under process conditions). Full text retrieved.
  -
    - **citation**: University of Michigan Deep Blue record: 'Standard molar Gibbs free energy of formation for Cu2O: high-resolution electrochemical measurements from 900 to 1300 K', J. Chem. Thermodynamics (1989).
    - **url**: https://deepblue.lib.umich.edu/handle/2027.42/28184
    - **why**: The best experimental determination of the Cu2O Gibbs energy in exactly the sintering temperature range, giving dH_f(Cu2O, 298.15 K) = -(170.59 +/- 0.08) kJ/mol. Use this rather than a two-term Ellingham fit for any precision oxygen-potential modelling.
  -
    - **citation**: Sandia National Laboratories, 'Technical Reference on Hydrogen Compatibility of Materials — Copper Alloys' (code 4001).
    - **url**: https://www.sandia.gov/app/uploads/sites/158/2021/12/4001TechRef_Cu.pdf
    - **why**: Standard reference on hydrogen effects in copper alloys. Listed for completeness — the PDF was downloaded in this session but could not be text-extracted, so NO numbers were taken from it. Retrieve and read independently.