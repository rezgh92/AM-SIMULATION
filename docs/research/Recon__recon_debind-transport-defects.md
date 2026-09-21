- **summary**: Thermal debinding of a highly-filled photopolymer green body is a coupled reaction–transport–mechanics problem in a porous medium whose pore network is initially 100% saturated with a cross-linked (non-melting) organic phase. For an LCM/LMM copper part the physics decomposes into four sequential regimes that a simulation must span continuously, because the defect mechanism changes in each one.

REGIME I — saturated, no open porosity (RT to ~250–300 °C). No connected gas path exists. Degradation products (monomer, oligomer, scission fragments, residual non-reactive diluent) must diffuse through the polymer itself. This is the Matar/Song/Evans regime: transient diffusion with a strongly concentration- and temperature-dependent D in a molten/softened polymer, with a defect criterion of *boiling* — a defect forms when the local partial pressure of dissolved monomer exceeds ambient plus capillary resistance, nucleating bubbles at the part centre. Matar et al. (JACerS 79:749, 1996) solved this for slab/cylinder/sphere and matched measured critical heating rates for 3 mm plates. Crucially, a photopolymer is thermoset: it does not wick or drain, so the whole Barone & Ulicny (JACerS 73:3323, 1990) capillary-liquid-migration branch and German's "wicking" branch are largely inactive — a first-order structural difference from wax-based MIM. In LCM this regime is where 65% of crack-initiation risk sits (Si3N4 VPP review, PMC11990554), and it is where the interlayer degree-of-conversion gradient matters: the weakly cross-linked boundary layer of each 25–100 µm layer depolymerises earlier and faster, concentrating gas generation precisely at the mechanically weakest plane — the delamination mechanism.

REGIME II — open-pore permeation (≈300–500 °C). Once ~10–20% of the binder has left, a percolating pore network appears and Darcy flow takes over. Combining continuity, ideal gas and Darcy with a volumetric source Ṡ gives ε∂P/∂t = (K/2μ)∇²(P²) + (RT/M)Ṡ; the pseudo-steady-state limit ∇²(P²) = −2μRTṠ/(KM) is accurate for realistic parameters (Lombardo & Retzloff, Adv Appl Ceram 119:158, 2020; verified against FE). For a slab of half-thickness L this yields P_c²−P₀² = μRTṠL²/(KM) — the canonical L² scaling — and, with Ṡ from Kissinger-type peak kinetics, a closed-form critical heating rate β_crit = e·K·M·T_p(P_max²−P₀²)/(μ·W_B·E·L²). The failure criterion is poroelastic: σ_t ≈ b(P_c−P₀) > σ_green(T,α), with Tsai (AIChE J 37:547, 1991) showing the stresses are tensile, maximal at the centre, and hoop > radial in a cylinder. Yun & Lombardo report that K only begins to control β_crit below ~1e-15 m²; measured permeability of a debound/pre-sintered alumina body at 36% porosity is 2.37e-15 m² (PMC6926824), i.e. real green bodies sit right on that boundary. Permeability evolves as K = ε_open³d_p²/(36k₀(1−ε_open)²) (Carman–Kozeny) with ε_open = ε_tot·α, so K rises by orders of magnitude across the burnout — the model is strongly nonlinear and self-accelerating, which is exactly why "constant weight-loss-rate" (uniform-rate) control beats constant heating rate.

REGIME III — Knudsen/transition correction. Pore radii in a debound LCM body are of order 0.2–2 µm; at 1 bar and 700 K the N₂ mean free path is ~1.5e-7 m, so Kn ≈ 0.05–0.7 — squarely transition regime. Darcy must be Klinkenberg-corrected (k_app = k_∞(1+b_K/P)) and diffusive transport must use the Bosanquet/dusty-gas combination, or the model over-predicts the safe heating rate at low absolute pressure (vacuum debinding) by a large factor.

REGIME IV — zero-strength window and pre-sintering overlap. Between the last binder leaving and the first sinter necks forming, strength is set only by inter-particle friction. German's data show a compact green strength of 2–20 MPa dropping (e.g. 10 → 4 MPa by 400 °C) before neck growth by surface diffusion recovers it, and gives a distortion threshold stress of only 0.2–25 kPa. Copper's advantage is that surface-diffusion neck growth starts low (~0.3 T_m ≈ 130–400 °C), so pre-sintering can be made to overlap binder removal; the design goal is to keep σ_applied (self-weight + setter friction, both ~0.3–3 kPa for a 20 mm part) below that threshold throughout.

Two copper-specific amplifiers: (a) oxidative decomposition is catalysed by the metal/oxide filler (Liau & Lombardo showed BaTiO₃+Pt accelerates PVB burnout), so TGA of the neat resin is invalid — kinetics must be measured on the actual filled green body; (b) full oxidative burnout is energetically uncontainable (adiabatic ΔT of order 10³–10⁴ K), so a Frank-Kamenetskii runaway check is mandatory and the cycle must be oxygen-starved or CO₂/inert. Conversely copper's high thermal diffusivity makes conduction-driven thermal-gradient stress negligible (ΔT ≈ 0.2 K for 1 K/min through a 10 mm section), so gas pressure, not heat flow, is the sole rate limiter.
- **key_facts**:
  -
    - **fact**: German (1987, 'Theory of Thermal Debinding') established three limiting transport mechanisms for thermal debinding — diffusion control, permeation control, and fluid wicking — and showed removal time is minimised by large particle size, thin sections, high compact porosity, high temperature and large pressure gradients. Essentially all later continuum models build on this framework.
    - **source**: R. M. German, 'Theory of Thermal Debinding', Int. J. Powder Metallurgy (1987). https://www.researchgate.net/publication/279591269_Theory_of_Thermal_Debinding
    - **confidence**: high
  -
    - **fact**: For a photopolymer (thermoset) binder the wicking and capillary-liquid-migration branches are largely inoperative because the cross-linked network does not melt and drain; this is the single biggest structural difference between LCM/VPP debinding and wax-based MIM debinding, and it means the saturated diffusion-limited regime (Matar/Song/Evans) governs the early, most dangerous part of the cycle.
    - **source**: unverified (inference from Barone & Ulicny 1990 liquid-transport model applying to molten thermoplastic binders, and from LCM binder chemistry being acrylate/methacrylate thermosets per Ożóg et al. J. Ceram. Sci. Technol. 2019, DOI 10.4416/JCST2019-00023)
    - **confidence**: medium
  -
    - **fact**: Matar, Edirisinghe, Evans & Twizell used a single general equation valid for sphere / infinite plate / infinite cylinder to compute transient diffusion of degradation products with a concentration-dependent diffusion coefficient, explicitly to find 'the critical heating rate above which defects are produced in the early stages of pyrolysis before continuous porosity develops', with reasonable agreement against measured critical heating rates for 3 mm thick plates.
    - **source**: Matar, Edirisinghe, Evans, Twizell, J. Am. Ceram. Soc. 79 (1996) 749-755, DOI 10.1111/j.1151-2916.1996.tb07938.x; abstract confirmed at https://staff-old.najah.edu/dr-sameer-matar/published-research/diffusion-degradation-products-ceramic-mouldings-during-pyrolysis
    - **confidence**: high
  -
    - **fact**: Song, Edirisinghe, Evans & Twizell extended this by combining a gas-flow-regime equation (covering diffusion AND viscous flow, i.e. transition-regime transport) with polymer-melt transport, with a moving boundary between an undegraded core and a porous outer shell; defects occur by 'boiling of the polymer-monomer solution at the centre of the molding', and the porous outer layer's flow resistance feeds back on the core boundary condition.
    - **source**: Song, Edirisinghe, Evans, Twizell, J. Mater. Res. 11(4) (1996) 830-840; abstract at https://www.cambridge.org/core/journals/journal-of-materials-research/article/abs/modeling-the-effect-of-gas-transport-on-the-formation-of-defects-during-thermolysis-of-powder-moldings/976842CBDBCF8EA8589AB527BDEC79E7
    - **confidence**: high
  -
    - **fact**: Tsai (1991) coupled intrinsic pyrolysis kinetics with either the Carman-Kozeny equation or the Wakao-Smith slip-flow model to get the pressure field in a cylindrical green body, then derived stresses from elasticity theory. Result: the skeleton stresses are TENSILE with maxima at the cylinder centre, and the tangential (hoop) stress exceeds the radial stress. Pressurising the furnace atmosphere effectively reduces both interstitial pressure and internal stress.
    - **source**: D.-S. Tsai, AIChE J. 37 (1991) 547-554, DOI 10.1002/aic.690370408; https://aiche.onlinelibrary.wiley.com/doi/abs/10.1002/aic.690370408
    - **confidence**: high
  -
    - **fact**: Stangle & Aksay (1990) built the reference simultaneous momentum/heat/mass-transfer-with-reaction model for a disordered porous medium, predicting local T and mass distribution vs time and position, which is then coupled to mechanical properties to predict internal stress. Binder removal is initially capillary-dominated and transitions to gas-phase diffusion + convection as saturation falls.
    - **source**: G. C. Stangle, I. A. Aksay, Chem. Eng. Sci. 45 (1990) 1719-1731; https://www.sciencedirect.com/science/article/abs/pii/0009250990870503
    - **confidence**: high
  -
    - **fact**: Feng & Lombardo obtained analytical solutions to the binder-removal pressure PDE for parallelepiped and cylindrical bodies including ANISOTROPIC permeability, and derived explicit scaling relationships for pressure build-up in terms of body dimensions, reaction rate and permeability. They also showed the steady-state (pseudo-steady) analytical solution is a good representation of the full unsteady numerical solution over most of the binder-removal parameter space.
    - **source**: K. Feng, S. J. Lombardo, J. Am. Ceram. Soc. 86 (2003), DOI 10.1111/j.1151-2916.2003.tb00005.x; and J. Mater. Res. 17 (2002), DOI 10.1557/JMR.2002.0213
    - **confidence**: high
  -
    - **fact**: Lombardo & Retzloff formulate the optimum-cycle problem as: spatial-temporal reaction-permeability PDE + ODEs for decomposition rate and T(t) + an ALGEBRAIC INEQUALITY CONSTRAINT capping the internal pressure. Solving by variational calculus / process control gives a continuously INCREASING heating rate as the optimal policy, which is shorter than any sequence of isothermal holds at the same pressure limit.
    - **source**: S. J. Lombardo, D. G. Retzloff, Adv. Appl. Ceram. 119 (2020), DOI 10.1080/17436753.2019.1707393; https://journals.sagepub.com/doi/10.1080/17436753.2019.1707393
    - **confidence**: high
  -
    - **fact**: In the Lombardo/Retzloff optimal-control formulation the permeability only begins to affect the critical (defect-free) heating rate once it falls below ~1e-15 m^2; above that the process is reaction-rate limited, not transport limited. (Source text renders the exponent ambiguously as '10-15 m2'; interpretation as 1e-15 m^2 is consistent with measured green-body permeabilities.)
    - **source**: Lombardo & Retzloff, Adv. Appl. Ceram. 119 (2020), DOI 10.1080/17436753.2019.1707393 (value read from search-engine extract, exponent formatting ambiguous)
    - **confidence**: medium
  -
    - **fact**: Xie et al. define a CRITICAL THICKNESS of debinding: the thickness at which control switches from diffusion of gas products through liquid binder to diffusion/permeation in pores. It is independent of the green body thickness and depends only on particle size, solids content and binder composition; larger particles and higher solids loading raise it, permitting a higher heating rate in the EARLY stage.
    - **source**: Xie et al., Int. J. Appl. Ceram. Technol. 17 (2020), DOI 10.1111/ijac.13349; https://ceramics.onlinelibrary.wiley.com/doi/abs/10.1111/ijac.13349
    - **confidence**: high
  -
    - **fact**: Shivashankar & German introduced an EFFECTIVE LENGTH SCALE L_eff = V/A (compact volume divided by exposed surface area) for predicting solvent- and wick-debinding times of arbitrary PIM geometries; this is the correct geometric collapse variable for non-slab parts and should replace naive 'wall thickness' in a lattice or shelled LCM part.
    - **source**: T. S. Shivashankar, R. M. German, J. Am. Ceram. Soc. 82 (1999), DOI 10.1111/j.1151-2916.1999.tb01888.x
    - **confidence**: high
  -
    - **fact**: Liau & Lombardo showed the filler is CATALYTICALLY ACTIVE: PVB weight-loss rate was accelerated when both BaTiO3 and Pt metal were present relative to the neat binder. Direct implication for a copper-filled acrylate: TGA/DSC kinetics must be measured on the actual filled green body (and in the actual atmosphere), never on the neat resin.
    - **source**: L. C. K. Liau, S. J. Lombardo, J. Am. Ceram. Soc. 83 (2000) 2645-2653, DOI 10.1111/j.1151-2916.2000.tb01609.x
    - **confidence**: high
  -
    - **fact**: Liau & Lombardo also quantified a pure GEOMETRY effect on yield: for MLCCs 1.3-3.8 cm long and 0.3-1.3 cm high, optimum yield occurred at a height:length aspect ratio of 1:3 — i.e. at fixed volume there is an optimal shape that minimises peak internal pressure. Feng & Lombardo generalised this to an 'optimum geometry' for 3D bodies.
    - **source**: Liau & Lombardo, J. Am. Ceram. Soc. 83 (2000) 2645-2653, DOI 10.1111/j.1151-2916.2000.tb01609.x
    - **confidence**: high
  -
    - **fact**: Oliveira, Kaviany, Hrdina & Halloran (Int. J. Heat Mass Transfer 42 (1999) 3307-3329) predicted the critical heating rate in 1-D thermal debinding of a high-molar-weight polymer component from the estimated vapour pressure of the degradation products; simulations in 1-D and 2-D showed there is NO sharp liquid-gas interface front — the residual polymer distribution is a smooth continuous function of position. This invalidates sharp shrinking-core formulations for fine-powder systems.
    - **source**: Oliveira et al., Int. J. Heat Mass Transfer 42 (1999) 3307-3329 (citation reported in secondary sources; original not directly fetched); related: Metall. Mater. Trans. B DOI 10.1007/s11663-002-0058-6 and J. Mater. Res. DOI 10.1557/JMR.2001.0334
    - **confidence**: medium
  -
    - **fact**: Oliveira-type 2-D models of mass transport AND deformation show that non-uniform residual polymer (from non-uniform polymer flow) produces non-uniform deformation, and that severe non-uniform deformation is the route to cracking/distortion/failure. Polymer removal is dominated by pressure-forced liquid flow, not capillary-driven flow.
    - **source**: Metall. Mater. Trans. B 33 (2002), DOI 10.1007/s11663-002-0058-6; https://link.springer.com/article/10.1007/s11663-002-0058-6
    - **confidence**: high
  -
    - **fact**: Delamination in lithography-printed parts is driven by the intra-layer cure gradient: each layer comprises a highly cross-linked zone and a weakly cross-linked zone with DIFFERENT decomposition kinetics; the resulting gradient in decomposition rate creates large stress gradients that promote interlaminar cracking. Post-curing the green body and lowering the debinding heating rate reduce this anisotropy and the delamination cracking.
    - **source**: Open Ceramics (2023), 'Elimination of delamination cracks in ceramics manufactured using LCD stereolithography', https://www.sciencedirect.com/science/article/pii/S2666539523002031 (content obtained via search extract; full text 403)
    - **confidence**: high
  -
    - **fact**: For VPP Si3N4, ~65% of crack-initiation risk is attributed to RAPID VOLATILISATION BELOW 300 C — i.e. to the saturated/low-porosity regime, before the pore network percolates, not to the main pyrolysis peak.
    - **source**: Vat Photopolymerization-Based AM of Si3N4 review, PMC11990554, https://pmc.ncbi.nlm.nih.gov/articles/PMC11990554/
    - **confidence**: medium
  -
    - **fact**: Atmosphere is a first-order control on the SHAPE of the source term, not just on chemistry: TGA of an LSM green body showed dry air produced two sharp weight-loss bursts (1.5 wt% over 150-200 C and 3.5 wt% over 250-350 C) plus two exotherms at ~180 C and ~350 C, whereas argon spread the same loss over 110 C and 100 C wide windows with NO significant exotherm. Nitrogen was indistinguishable from argon and is recommended on cost.
    - **source**: WPI MQP thesis, 'Binder Burnout Investigation on Lanthanum Strontium Manganite', https://digital.wpi.edu/downloads/sn00b1354
    - **confidence**: high
  -
    - **fact**: Oxygen only reaches the interior of a green body after surface-layer burnout is complete, so even an 'air debind' is internally a PYROLYSIS. A simulation must therefore solve an O2 transport/consumption field, not assume a uniform oxidative mechanism.
    - **source**: Fraunhofer HTL, Debinding research page, https://www.htl.fraunhofer.de/en/ResearchAreas/thermal-processes/debinding.html
    - **confidence**: high
  -
    - **fact**: Fraunhofer HTL's production debinding-simulation stack is exactly the architecture required here: coupled FE of (i) temperature field with reaction heat, (ii) local debinding rate from a measured kinetic model, (iii) gas-phase concentration and pressure gradients, (iv) mechanical stress from thermal mismatch and overpressure — with in-situ acoustic emission and gas-emission monitoring for damage detection, and mass-loss reproducibility of 0.1%.
    - **source**: Fraunhofer HTL, https://www.htl.fraunhofer.de/en/ResearchAreas/thermal-processes/debinding.html
    - **confidence**: high
  -
    - **fact**: In-situ acoustic emission plus evolved-gas analysis during debinding detects even minor internal damage, giving a direct experimental observable to calibrate a crack criterion against (rather than post-mortem dye penetration / CT).
    - **source**: Fraunhofer HTL, https://www.htl.fraunhofer.de/en/ResearchAreas/thermal-processes/debinding.html
    - **confidence**: high
  -
    - **fact**: Crack-free thermal debinding of LCM (Lithoz/TU Wien) parts with wall thickness up to 20 mm has been demonstrated using geometry-specific optimised cycles up to 400 C. This is the practical ceiling to benchmark against — and it was achieved with a CERAMIC filler, not copper.
    - **source**: Pfaffinger, Mitteramskogler, Gmeiner, Stampfl, Mater. Sci. Forum 825-826 (2015) 75, DOI 10.4028/www.scientific.net/MSF.825-826.75; abstract at https://repositum.tuwien.at/handle/20.500.12708/67284
    - **confidence**: high
  -
    - **fact**: The transition from 'debinding' to 'pre-sintering' is a strength MINIMUM, not a monotonic recovery: German's in-situ transverse-rupture data for a compact starting at 10 MPa green strength show annealing DROPS the strength to ~4 MPa by 400 C, after which surface-diffusion neck growth raises it rapidly, peaking near 600 C, before thermal softening takes over. The cycle must be designed so that binder removal completes inside a window where neck growth has already begun.
    - **source**: R. M. German, 'Strength Evolution in Debinding and Sintering', CAVS/Penn State, https://www.cavs.msstate.edu/publications/docs/2003/07/2003-16.pdf
    - **confidence**: high
  -
    - **fact**: German's in-situ sintering strength model: S = sigma_0(T)*(X/D)^2*N_C/K with stress-concentration factor K inversely proportional to neck-base curvature, K -> 2 once X/D reaches its ~0.5 ceiling; and the sintered neck size X/D is computed from the fractional density change from V_S0 to V_S. This gives a physically-grounded brown/pre-sintered strength sigma(T, alpha_sinter) to compare against the gas-pressure-induced stress.
    - **source**: R. M. German, 'Strength Evolution in Debinding and Sintering', https://www.cavs.msstate.edu/publications/docs/2003/07/2003-16.pdf
    - **confidence**: high
  -
    - **fact**: Distortion/slumping during sintering has a THRESHOLD STRESS, measured from distortion profiles at only 0.2-25 kPa. Any self-weight, setter-friction or support-reaction stress above this causes creep distortion, which is 3-4 orders of magnitude below the fracture-relevant stresses — so slumping and cracking are governed by completely different criteria and must be checked separately.
    - **source**: R. M. German, 'Strength Evolution in Debinding and Sintering', https://www.cavs.msstate.edu/publications/docs/2003/07/2003-16.pdf
    - **confidence**: high
  -
    - **fact**: Copper sinters with a very low effective viscosity relative to refractory ceramics: Mackenzie-Shuttleworth estimated 2e8-3e11 Pa.s at 850 C and Schatt measured 2.3e9 Pa.s at 800 C. These are the numbers to put into a viscous (Bingham/Norton) creep model for slumping of a copper brown body — and they show copper can creep at temperatures well below its melting point.
    - **source**: R. M. German, 'Strength Evolution in Debinding and Sintering', https://www.cavs.msstate.edu/publications/docs/2003/07/2003-16.pdf (citing Mackenzie & Shuttleworth; Schatt)
    - **confidence**: high
  -
    - **fact**: Copper thermally softens extremely strongly in the relevant band: at 1e-4 1/s strain rate the yield strength of copper drops 31-fold between room temperature and 1000 C; at 800 C and 1e-3 1/s, a 100 C temperature rise cuts strength by 70% while a decade change in strain rate only changes it by 25%. Temperature, not strain rate, dominates — so an isothermal-strength lookup vs T is an acceptable constitutive simplification.
    - **source**: R. M. German, 'Strength Evolution in Debinding and Sintering', https://www.cavs.msstate.edu/publications/docs/2003/07/2003-16.pdf
    - **confidence**: high
  -
    - **fact**: For VPP/DLP ceramics, debinding under ARGON at 0.2 or 0.5 C/min gave crack-free parts whereas flowing air did not (dye penetration + SEM verification); mass loss began between 200-300 C (~1%), the bulk occurred 300-600 C (down to 74% of original mass), and debinding was complete above 600 C.
    - **source**: Wang, Qiu et al., Ceram. Int. 46 (2020) 2438-2446, 'Study on defect-free debinding green body of ceramic formed by DLP technology', https://www.sciencedirect.com/science/article/abs/pii/S0272884219327725
    - **confidence**: high
  -
    - **fact**: A 95 vol% N2 + 5 vol% H2 debinding atmosphere enabled crack-free VPP Si3N4 GREEN bodies up to 5 mm wall thickness (vs ~4 mm conventional limit), reportedly by promoting hydrocarbon formation that distributes gas-evolution pressure over a wider temperature window. Direct relevance to copper, where H2 is needed anyway for oxide reduction.
    - **source**: Si3N4 VPP review PMC11990554 (https://pmc.ncbi.nlm.nih.gov/articles/PMC11990554/) summarising Ceram. Int. paper S0272884224035715
    - **confidence**: medium
  -
    - **fact**: Residual carbon from incomplete binder removal is quantitatively catastrophic in ceramics (flexural strength 469 -> 184 MPa in Si3N4); a post-debind oxidation hold at 450 C for 5 h eliminated carbon without dimensional instability. For copper the analogous problem is worse because Cu forms no carbide, so carbon must leave as CO/CO2/CH4 in the gas phase.
    - **source**: Si3N4 VPP review PMC11990554, https://pmc.ncbi.nlm.nih.gov/articles/PMC11990554/
    - **confidence**: medium
  -
    - **fact**: Model-free (isoconversional) kinetics — Friedman (differential), KAS, Flynn-Wall-Ozawa and Vyazovkin (integral) — are the correct tool when the binder chemistry is UNKNOWN, because model-fitting Arrhenius parameters are unreliable unless the mechanism is known in detail. Friedman and Vyazovkin are cited as best for capturing E_a(alpha) dependence. This gives E_a(alpha) directly from multi-heating-rate TGA of the actual filled green body, with no assumption about the Lithoz binder chemistry.
    - **source**: ScienceDirect Thermochim. Acta review on isoconversional methods, https://www.sciencedirect.com/science/article/abs/pii/S0040603124000297; and ICTAC-style guidance summarised at https://kinetics.netzsch.com/en/features/model-free-analysis
    - **confidence**: high
  -
    - **fact**: A distributed-activation-energy (DAEM) or independent-parallel-reaction (IPR) multi-pseudo-component fit is the demonstrated best practice for VPP resin pyrolysis: a 3-component modified DAEM fitted a ceramic VPP resin's TGA to R^2 > 0.9999 globally and was then used to predict the internal gas pressure vs temperature. IPR reportedly outperforms DAEM for Si3N4 VPP resins.
    - **source**: Materials 18 (2025) 4004, DOI 10.3390/ma18174004, PMC12429858; and PMC11990554
    - **confidence**: high
  -
    - **fact**: Ultra-fast routes exist and break the L^2 scaling by changing the boundary condition rather than the physics: vacuum + rapid heating with porous graphite felts gave complete binder removal from VPP zirconia in <30 minutes (40-200x time reduction, ~3500x energy reduction); UHS (carbon-felt Joule heating) achieved combined debind+densify in 30-120 s. Both are credible 'stretch' targets once a validated pressure model exists.
    - **source**: Mosadegh et al., Ceram. Int. (2025), https://www.sciencedirect.com/science/article/abs/pii/S0272884225023417 (abstract via search); UHS: J. Eur. Ceram. Soc. (2023), https://www.sciencedirect.com/science/article/pii/S0955221923006660
    - **confidence**: medium
  -
    - **fact**: Setter/part friction is an explicit contributor to distortion and failure in sinter-based AM: parts experience forces from gravity, friction and uneven shrinkage, and drag between baseplate/setter and part inhibits movement. Micro-structured setter plates are being engineered specifically to reduce this friction for binder-jet metal parts.
    - **source**: Desktop Metal, 'Thermal Debinding and Sintering 101', https://www.desktopmetal.com/resources/sintering-101; and Tribology Transactions (2025), DOI 10.1080/10402004.2025.2595444
    - **confidence**: medium
  -
    - **fact**: The brown state — after complete thermal binder removal but before neck formation — is explicitly the most fragile state, with particles held only by frictional contact. This is the 'zero-strength window' and the cycle must minimise its duration and the stress applied during it.
    - **source**: Search extract from sinter-based AM literature (Desktop Metal sintering primer and MEX distortion literature); https://www.desktopmetal.com/resources/sintering-101
    - **confidence**: medium
  -
    - **fact**: LCM/VPP green bodies have MORE binder by volume than MIM feedstock: VPP binder content is quoted as 40-60 vol% (solids loading 40-50 vol%), versus typical MIM at ~35-45 vol% binder. Combined with the absence of a solvent-extractable wax component, this means the LCM body must expel a larger binder mass entirely through the thermal route with no pre-formed open-pore network.
    - **source**: Solids loading: LithaLox HP500 = 49 vol% (Ożóg et al., DOI 10.4416/JCST2019-00023); AlN UV-LCM = 40 vol% (PMC7579482); VPP binder content 40-60 vol% quoted in Mosadegh et al. (https://www.sciencedirect.com/science/article/abs/pii/S0272884225023417). MIM comparison figure is unverified.
    - **confidence**: medium
  -
    - **fact**: For copper specifically, a debind in AIR at 400 C followed by sintering in H2 gave final C content of 0.018 wt% (equal to the raw powder) at the cost of higher oxygen; staying longer in H2 and raising sintering from 980 to 1050 C reduced oxygen to 0.067 wt%. Copper LMM/photopolymer parts were sintered in H2 at 980/1030/1050 C dwells at a constant 3 C/min.
    - **source**: Discover Applied Sciences (SN Appl. Sci.) 2 (2020), DOI 10.1007/s42452-020-04049-3 — content obtained via search extract only, full text blocked
    - **confidence**: medium
  -
    - **fact**: Copper MIM benchmark for the sintering half of the cycle: sintering at 950/1000/1030/1050 C gave highest relative density 94.5% at the highest temperature with isotropic shrinkage; thermal debind to 500 C; total green weight loss ~6.5%; observed shrinkage 10-18%; Cu oxides formed during debinding were reduced in H2 at 500 C.
    - **source**: Int. J. Adv. Manuf. Technol. (2021), DOI 10.1007/s00170-021-07188-y — via search extract; full text not fetched
    - **confidence**: medium
  -
    - **fact**: Copper's very high thermal conductivity makes conduction-limited thermal-gradient stress essentially irrelevant during debinding: for a 10 mm thick section at 1 K/min with a green-body thermal diffusivity of order 1e-6 m2/s, the steady internal delta-T is ~0.2 K. The binding constraint is therefore gas pressure and, in oxidising atmospheres, reaction exotherm — NOT furnace-to-part heat transfer.
    - **source**: unverified (derived: delta-T = beta*L^2/(2a); green-body diffusivity assumed, must be measured by laser flash as Fraunhofer HTL do)
    - **confidence**: medium
  -
    - **fact**: Full oxidative burnout of the binder cannot be thermally contained: for ~10-15 wt% acrylate binder with a heat of combustion of order 25 MJ/kg in a copper-dominated body (c_p ~ 400-450 J/kg.K), the adiabatic temperature rise is of order 10^3-10^4 K. Any cycle that allows simultaneous oxygen access and high conversion rate will run away locally. This is why inert/oxygen-limited or CO2 (endothermic) burnout is mandatory for a thick copper part.
    - **source**: unverified (derived: delta-T_ad = w_B*deltaH_c/c_p; heat of combustion of acrylate/PMMA-like polymer ~25 MJ/kg is a textbook value not verified in a debinding-specific source). Endothermic CO2 burnout claim: patent/industrial literature surfaced via search (US5419857 family).
    - **confidence**: low
  -
    - **fact**: Measured absolute (Klinkenberg-corrected) gas permeability of a DEBOUND/PRE-SINTERED alumina body at 36.0% open porosity is 2.37e-15 m2 (range 2.29-2.43e-15), measured by He transient-pressure permeametry. A copper green body at ~50 vol% solids with a coarser powder should be more permeable, but this is the right order of magnitude to seed a model before measurement.
    - **source**: Materials / PMC6926824, 'Towards Creation of Ceramic-Based Low Permeability Reference Standards', https://pmc.ncbi.nlm.nih.gov/articles/PMC6926824/
    - **confidence**: high
  -
    - **fact**: Real LCM debinding schedules are extremely slow and multi-step: a published UV-LCM AlN cycle used 0.1 C/min to 120 C (6 h hold), 0.5 C/min to 360 C (16 h hold), 0.5 C/min to 460 C (6 h hold), then free cooling — i.e. ~28 h of holds alone. A silica VPP cycle used 0.5 C/min with 4 h holds at 150, 330 and 420 C.
    - **source**: AlN: PMC7579482, https://pmc.ncbi.nlm.nih.gov/articles/PMC7579482/. Silica: Polymers 15 (2023) 3141, DOI 10.3390/polym15143141, PMC10383664
    - **confidence**: high
  -
    - **fact**: Green strength of VPP parts is strongly formulation-dependent and is the denominator of the crack criterion: a 75 wt% silica VPP system peaked at ~15 MPa flexural strength (50% HDDA / 20% urethane acrylate / 15% NVP / 15% PEA); >15 wt% NVP caused uncontrolled thermal degradation and debinding cracks, with a sharp NVP decomposition at 420 C generating the crack-driving pressure.
    - **source**: Polymers 15 (2023) 3141, DOI 10.3390/polym15143141, https://pmc.ncbi.nlm.nih.gov/articles/PMC10383664/
    - **confidence**: high
  -
    - **fact**: A 3-pseudo-component DAEM fit of a ceramic VPP resin yielded maximum internal gas pressures of only 0.20-0.34 MPa (i.e. ~1-2.4 bar gauge) at 158-355 C depending on formulation, for a debinding rate <= 0.5 C/min. These are the right magnitudes to compare against a green strength of 10-15 MPa — i.e. for THIN sections the model predicts a large safety margin, and cracking must then be attributed to stress concentration at layer interfaces or to local (not bulk) pressure.
    - **source**: Materials 18 (2025) 4004, DOI 10.3390/ma18174004, https://pmc.ncbi.nlm.nih.gov/articles/PMC12429858/
    - **confidence**: high
  -
    - **fact**: A 'uniform-rate' (constant mass-loss-rate) stepwise heating schedule derived from the multi-component decomposition characteristics of the resin is a published, validated alternative to constant heating rate for VPP green parts, with an explicit formula predicting residual resin weight at each stage. This is the practical realisation of Lombardo's constant-maximum-pressure optimal policy.
    - **source**: Duan et al., Addit. Manuf. (2024), https://www.sciencedirect.com/science/article/abs/pii/S2214860424001659 (abstract via search)
    - **confidence**: medium
- **numbers**:
  -
    - **quantity**: Absolute (Klinkenberg-corrected) gas permeability, debound/pre-sintered alumina
    - **value**: 2.37e-15 (range 2.29-2.43e-15)
    - **units**: m^2
    - **context**: 36.0% open porosity, He transient permeametry, room temperature. Use as the seed value for K at full binder removal; scale by d_p^2 for a coarser copper powder.
    - **source**: PMC6926824, https://pmc.ncbi.nlm.nih.gov/articles/PMC6926824/
  -
    - **quantity**: Permeability threshold below which K starts to control the critical heating rate
    - **value**: ~1e-15
    - **units**: m^2
    - **context**: Lombardo/Retzloff reaction-permeability model; above this the cycle is reaction-rate limited. Note: source formatting of the exponent was ambiguous.
    - **source**: Adv. Appl. Ceram. 119 (2020), DOI 10.1080/17436753.2019.1707393
  -
    - **quantity**: Open porosity of the reference debound alumina body
    - **value**: 36.0
    - **units**: %
    - **context**: Corresponds to the permeability value above; an LCM copper body at 50 vol% solids would reach ~50% open porosity after full burnout, i.e. higher K.
    - **source**: PMC6926824
  -
    - **quantity**: Maximum computed internal gas pressure during VPP ceramic debinding
    - **value**: 0.20 / 0.34 / 0.22
    - **units**: MPa (absolute)
    - **context**: Three resin formulations (S1/S2/S3) at <=0.5 C/min, peaks at 158 / 352 / 355 C respectively; 40 vol% Si3N4-based slurry. Compare against green strength ~10-15 MPa.
    - **source**: Materials 18 (2025) 4004, DOI 10.3390/ma18174004
  -
    - **quantity**: Activation energies of the dominant pyrolysis pseudo-component, VPP acrylate resins
    - **value**: 215.3 / 238.3 / 216.3
    - **units**: kJ/mol
    - **context**: M-DAEM 3-component fit; log10 A = 17 or 19 s^-1; mass fractions 0.64 / 0.85 / 0.64. HEA/HDDA/PPTTA blends at 40 vol% ceramic. Good priors for an acrylate-based Lithoz binder.
    - **source**: Materials 18 (2025) 4004, DOI 10.3390/ma18174004
  -
    - **quantity**: Activation energy / pre-exponential used in the Lombardo binder-removal optimal control model
    - **value**: E = 2.22e5 J/mol; A = 1.67e16
    - **units**: J/mol ; s^-1
    - **context**: First-order decomposition of a ceramic green-body binder; used with T0 = 300 K, P_ambient = 1.0e5 Pa.
    - **source**: Discrete Contin. Dyn. Syst. B, DOI 10.3934/dcdsb.2021034
  -
    - **quantity**: Maximum allowable internal gas pressure used as the failure constraint
    - **value**: 1.5e5 - 2.0e5
    - **units**: Pa (absolute)
    - **context**: i.e. 0.5-1.0 bar gauge, application dependent. This is the algebraic constraint in the optimal-control formulation.
    - **source**: DOI 10.3934/dcdsb.2021034
  -
    - **quantity**: Maximum heating rate constraint used in the same optimal-control study
    - **value**: 10
    - **units**: K/min
    - **context**: Furnace capability bound, not a material bound.
    - **source**: DOI 10.3934/dcdsb.2021034
  -
    - **quantity**: Distortion / slumping THRESHOLD STRESS in sintering compacts
    - **value**: 0.2 - 25
    - **units**: kPa
    - **context**: Back-calculated from measured distortion profiles. Stresses above this cause creep distortion. Compare self-weight (~0.5-1.5 kPa for a 20 mm tall copper green body) and setter friction.
    - **source**: German, 'Strength Evolution in Debinding and Sintering', https://www.cavs.msstate.edu/publications/docs/2003/07/2003-16.pdf
  -
    - **quantity**: Effective sintering viscosity of copper
    - **value**: 2e8 - 3e11 (Mackenzie-Shuttleworth, 850 C); 2.3e9 (Schatt, 800 C)
    - **units**: Pa.s
    - **context**: Use in a linear-viscous (Norton/Bingham) creep model for slumping of a copper brown/pre-sintered body.
    - **source**: German, 'Strength Evolution in Debinding and Sintering' (citing Mackenzie & Shuttleworth; Schatt)
  -
    - **quantity**: Green strength of a pressed powder compact (range)
    - **value**: 2 - 20
    - **units**: MPa
    - **context**: General PM compacts. LCM photopolymer green bodies are comparable-to-higher (see next entry).
    - **source**: German, 'Strength Evolution in Debinding and Sintering'
  -
    - **quantity**: In-situ strength trajectory of a bronze compact through debinding/pre-sintering
    - **value**: 10 MPa green -> 4 MPa at 400 C -> peak at 600 C -> 50 MPa at 800 C in situ -> ~700 MPa after cooling
    - **units**: MPa
    - **context**: Demonstrates the strength MINIMUM near 400 C (annealing) before surface-diffusion neck growth dominates. Copper should behave similarly but at lower homologous temperature.
    - **source**: German, 'Strength Evolution in Debinding and Sintering'
  -
    - **quantity**: Flexural (green) strength of an optimised 75 wt% silica VPP green body
    - **value**: ~15
    - **units**: MPa
    - **context**: 50% HDDA / 20% urethane acrylate / 15% NVP / 15% PEA. Use as the sigma_green prior for an acrylate LCM body until measured on the copper slurry.
    - **source**: Polymers 15 (2023) 3141, DOI 10.3390/polym15143141
  -
    - **quantity**: Quoted green-body strength range for 3-point bend of sinter-based AM green parts
    - **value**: 10 - 25
    - **units**: MPa
    - **context**: Patent-literature range; brown-body strength quoted separately as 1-5 MPa. The ~5-25x drop from green to brown is the zero-strength window.
    - **source**: US patent literature surfaced via search (US11919233 family); treat as indicative
  -
    - **quantity**: Maximum crack-free wall thickness achieved in LCM ceramic debinding
    - **value**: 20
    - **units**: mm
    - **context**: With geometry-specific optimised cycles to 400 C, Lithoz/TU Wien DLP system. The benchmark to beat (or match) for copper.
    - **source**: Pfaffinger et al., Mater. Sci. Forum 825-826 (2015) 75, DOI 10.4028/www.scientific.net/MSF.825-826.75
  -
    - **quantity**: Crack-free wall thickness for VPP Si3N4 green bodies under N2/H2 vs conventional
    - **value**: 5 (with 95%N2/5%H2) vs ~4 (conventional)
    - **units**: mm
    - **context**: Atmosphere alone bought ~25% more thickness; graded protocols reached 9 mm sintered wall via liquid-phase crack healing.
    - **source**: PMC11990554
  -
    - **quantity**: Heating rates that gave crack-free DLP ceramic parts under argon
    - **value**: 0.2 and 0.5
    - **units**: C/min
    - **context**: Dye-penetration + SEM verified; flowing air at the same rates cracked. 0.2 C/min slightly better.
    - **source**: Ceram. Int. 46 (2020) 2438-2446, https://www.sciencedirect.com/science/article/abs/pii/S0272884219327725
  -
    - **quantity**: Published UV-LCM AlN debinding schedule
    - **value**: 0.1 C/min -> 120 C (360 min hold); 0.5 C/min -> 360 C (960 min hold); 0.5 C/min -> 460 C (360 min hold)
    - **units**: C/min and minutes
    - **context**: 40 vol% AlN in HDDA + GTO dispersant + TPO-L; 25 um layers. ~28 h of holds. Demonstrates that the FIRST ramp (through the saturated regime) is the slowest.
    - **source**: PMC7579482
  -
    - **quantity**: Published silica VPP debinding schedule
    - **value**: 0.5 C/min with 4 h holds at 150, 330 and 420 C; sinter 1250 C / 6 h
    - **units**: C/min, C, h
    - **context**: 75 wt% silica. Holds placed at the DTG peaks of the individual monomers.
    - **source**: Polymers 15 (2023) 3141, DOI 10.3390/polym15143141
  -
    - **quantity**: Mass-loss staging of a DLP ceramic green body
    - **value**: ~1% between 200-300 C; down to 74% of original mass between 300-600 C; complete above 600 C
    - **units**: % of original mass
    - **context**: TG/DSC, DLP-printed ceramic. The 300-600 C band carries the overwhelming majority of the gas generation.
    - **source**: Ceram. Int. 46 (2020) 2438-2446
  -
    - **quantity**: LSM green body TGA under dry air vs argon
    - **value**: air: 1.5 wt% over 150-200 C + 3.5 wt% over 250-350 C, exotherms at ~180 and ~350 C; argon: 1 wt% over 100-210 C + 2.5 wt% over 300-400 C, no significant exotherm
    - **units**: wt%, C
    - **context**: 5 C/min. Quantifies how much atmosphere flattens the source term. Nitrogen was indistinguishable from argon.
    - **source**: WPI MQP, https://digital.wpi.edu/downloads/sn00b1354
  -
    - **quantity**: Total weight loss achievable in air vs inert for the same green body
    - **value**: 5.5 (air) vs slightly less in Ar/N2 (residual carbon)
    - **units**: wt%
    - **context**: Air removes all carbon but with violent exotherms; the recommended compromise is inert first, then an air/oxidising finish to strip residual carbon.
    - **source**: WPI MQP, https://digital.wpi.edu/downloads/sn00b1354
  -
    - **quantity**: Nitrogen mean free path at 20 C, 1 atm
    - **value**: ~6.5e-8
    - **units**: m
    - **context**: With sigma = 3.75e-10 m and n = 2.5e25 m^-3. At 700 K and 1 bar it rises to ~1.5e-7 m; against 0.2-2 um pores this gives Kn = 0.05-0.7 -> transition regime, so Klinkenberg/Bosanquet corrections are mandatory.
    - **source**: GW-Project, 'Flux Equations for Gas Diffusion in Porous Media', https://books.gw-project.org/flux-equations-for-gas-diffusion-in-porous-media/chapter/molecular-knudsen-and-transition-regimes/
  -
    - **quantity**: Permeability above which the molecular (non-Knudsen) regime applies
    - **value**: k > ~1e-12
    - **units**: m^2
    - **context**: Below this, transition-regime corrections are needed. Green-body permeabilities (~1e-15 m^2) are three orders below this threshold.
    - **source**: GW-Project, same chapter
  -
    - **quantity**: Kozeny constant (F_s * tau) from Carman's experiments
    - **value**: ~5
    - **units**: dimensionless
    - **context**: Used in K = eps^3 d_p^2 / (36 k0 (1-eps)^2) or K = eps^3/(5 S_v^2 (1-eps)^2).
    - **source**: DoITPoMS, https://www.doitpoms.ac.uk/tlplib/powder/carman.php; SPE, https://onepetro.org/spe/general-information/1540/Estimating-permeability-based-on-Kozeny-Carman
  -
    - **quantity**: Solids loading of commercial Lithoz LCM alumina slurry (LithaLox HP500)
    - **value**: 49
    - **units**: vol%
    - **context**: Density 2.52 g/cm3; (meth)acrylate reactive binder plus proprietary NON-REACTIVE solvent, dispersant, photoinitiators. The non-reactive solvent is a separate, lower-temperature volatile the model must treat as its own species.
    - **source**: Ożóg et al., J. Ceram. Sci. Technol. (2019), DOI 10.4416/JCST2019-00023
  -
    - **quantity**: Binder content of vat-photopolymerisation green parts
    - **value**: 40 - 60
    - **units**: vol%
    - **context**: Cited as the reason conventional thermal debinding takes 20-100 h. Higher binder VOLUME fraction than typical MIM.
    - **source**: Mosadegh et al., Ceram. Int. (2025), https://www.sciencedirect.com/science/article/abs/pii/S0272884225023417
  -
    - **quantity**: Conventional VPP thermal debinding cycle duration
    - **value**: 20 - 100
    - **units**: hours
    - **context**: The baseline this project should beat. Cited alongside a >48 h typical figure for Si3N4.
    - **source**: Mosadegh et al. (as above); PMC11990554
  -
    - **quantity**: Copper LMM/photopolymer sintering conditions and outcome
    - **value**: debind in air at 400 C; sinter in H2 at 980/1030/1050 C dwells, 3 C/min; final C = 0.018 wt%; O reduced to 0.067 wt% at 1050 C
    - **units**: C, C/min, wt%
    - **context**: Highly loaded photocurable copper formulation - the closest published analogue to the Lithoz copper slurry.
    - **source**: SN Appl. Sci. 2 (2020), DOI 10.1007/s42452-020-04049-3 (via search extract; full text blocked)
  -
    - **quantity**: Copper MIM sintering benchmark
    - **value**: 94.5% relative density at 1050 C; thermal debind to 500 C; ~6.5 wt% total green weight loss; 10-18% shrinkage
    - **units**: %, C, wt%
    - **context**: Sintered at 950/1000/1030/1050 C; highest T gave isotropic shrinkage. Sets the expected shrinkage range for the copper LCM part.
    - **source**: Int. J. Adv. Manuf. Technol. (2021), DOI 10.1007/s00170-021-07188-y (via search extract)
  -
    - **quantity**: Optimum MLCC aspect ratio (height:length) for binder-burnout yield
    - **value**: 1:3
    - **units**: dimensionless
    - **context**: Over samples 1.3-3.8 cm long, 0.3-1.3 cm high. Evidence that geometry optimisation at fixed volume is a real lever.
    - **source**: Liau & Lombardo, J. Am. Ceram. Soc. 83 (2000) 2645-2653, DOI 10.1111/j.1151-2916.2000.tb01609.x
  -
    - **quantity**: Debinding mass-loss measurement reproducibility achievable (Fraunhofer HTL thermo-optical/gravimetric rigs)
    - **value**: 0.1
    - **units**: % of mass
    - **context**: Sets the practical noise floor for building a kinetic database from a small amount of a scarce R&D slurry.
    - **source**: https://www.htl.fraunhofer.de/en/ResearchAreas/thermal-processes/debinding.html
  -
    - **quantity**: Lithoz CeraFab Multi 2M30 build envelope
    - **value**: 76 x 43 x 170
    - **units**: mm
    - **context**: Two vats; multi-material (ceramic-metal, ceramic-polymer, ceramic-ceramic). ~30 um pixel implied by the model designation. Layer thickness for the 2M30 was not found in an authoritative source.
    - **source**: Aniwaa product page, https://www.aniwaa.com/product/3d-printers/lithoz-cerafab-multi-2m30/ (secondary source)
  -
    - **quantity**: Estimated internal thermal gradient in a copper green body
    - **value**: ~0.2
    - **units**: K
    - **context**: Derived: delta-T = beta L^2 / (2a) with beta = 1 K/min, L = 5 mm half-thickness, a = 1e-6 m2/s. Confirms thermal-gradient stress is NOT the limiting defect mechanism for copper. Green-body diffusivity must be measured (laser flash).
    - **source**: unverified (derived)
  -
    - **quantity**: Adiabatic temperature rise for fully oxidative burnout of the binder in a copper green body
    - **value**: order 1e3 - 1e4
    - **units**: K
    - **context**: Derived: delta-T_ad = w_B * deltaH_c / c_p, with w_B ~ 0.10-0.15 (binder mass fraction), deltaH_c ~ 25 MJ/kg (acrylate), c_p ~ 400-450 J/kg.K (copper-dominated). Demonstrates that air debinding of a thick copper part is fundamentally uncontrollable without oxygen starvation.
    - **source**: unverified (derived; deltaH_c is a generic polymer value, not measured for this binder)
  -
    - **quantity**: Frank-Kamenetskii critical parameter for thermal explosion
    - **value**: 0.878 (infinite slab), 2.00 (infinite cylinder), 3.32 (sphere)
    - **units**: dimensionless
    - **context**: Classical values; use with delta = (Q rho A E / (k_eff R T_a^2)) L^2 exp(-E/(R T_a)) to screen for exothermic runaway in an oxidising debind.
    - **source**: unverified in a debinding-specific source; classical combustion-theory values (Frank-Kamenetskii)
- **models_or_methods**:
  -
    - **name**: Reaction-permeation (Darcy) pressure model for the open-pore regime — the core PDE
    - **formulation**: Gas continuity in a rigid porous skeleton with a volumetric source:
  d(eps_g * rho_g)/dt + div(rho_g * v) = S_dot
with Darcy velocity  v = -(K/mu) grad(P)  and ideal gas  rho_g = P*M/(R*T).
For spatially uniform T, mu, K this collapses to the P-squared (Leibenzon) form:
  eps_g * dP/dt = (K / (2*mu)) * Laplacian(P^2) + (R*T/M) * S_dot
Pseudo-steady-state limit (validated by Lombardo/Retzloff against full FE):
  Laplacian(P^2) = -2*mu*R*T*S_dot / (K*M)
Source term from binder decomposition:
  S_dot = W_B * dalpha/dt   [kg m^-3 s^-1],  W_B = binder mass per unit green-body volume
1-D slab, half-thickness L, P = P0 on both faces, uniform source:
  P(x)^2 = P0^2 + (mu*R*T*S_dot/(K*M)) * (L^2 - x^2)
  => P_centre^2 - P0^2 = mu*R*T*S_dot*L^2 / (K*M)      <-- the L^2 scaling law
Anisotropic 3D generalisation (approximate, exact series solutions in Feng & Lombardo):
  P_c^2 - P0^2 ~= (mu*R*T*S_dot/M) / [ 2*( K_x/a^2 + K_y/b^2 + K_z/c^2 ) ]
for a parallelepiped of half-dimensions a,b,c. For an LCM part, K_z (through-layer) < K_x = K_y (in-plane) is expected, so the layer-normal direction dominates the denominator.
    - **when_to_use**: Once open porosity percolates (roughly alpha > 0.1-0.2), i.e. above ~300 C for an acrylate LCM body. This is the workhorse equation for the main pyrolysis peak.
    - **inputs_needed**: K(alpha, T) [m^2], mu_gas(T) [Pa.s], M of the evolved gas mixture [kg/mol], T(t), W_B [kg/m^3], dalpha/dt from kinetics, P0 (furnace pressure), part half-dimensions.
    - **limitations**: Assumes rigid skeleton (no shrinkage/creep coupling), single-component ideal gas with a single M, isothermal in space, Darcy (no Klinkenberg/Knudsen), and K uniform. All four assumptions are violated somewhere in a real cycle — K varies by orders of magnitude with alpha, the gas is a mixture with M from ~30 to >200 g/mol, and near 1e-15 m^2 the Knudsen correction is significant.
    - **source**: German (1987); Tsai, AIChE J 37 (1991) 547, DOI 10.1002/aic.690370408; Feng & Lombardo, JACerS 86 (2003) DOI 10.1111/j.1151-2916.2003.tb00005.x and JMR 17 (2002) DOI 10.1557/JMR.2002.0213; Lombardo & Retzloff, Adv Appl Ceram 119 (2020) DOI 10.1080/17436753.2019.1707393. The P^2 collapse and the slab solution are standard; the explicit algebra written here is my derivation from those sources.
  -
    - **name**: Closed-form CRITICAL HEATING RATE from the permeation model
    - **formulation**: For an n=1 (or Kissinger-type) decomposition at constant heating rate beta, the peak volumetric gas generation is
  (dalpha/dt)_max = beta*E / (e * R * T_p^2)     with  beta*E/(R*T_p^2) = A*exp(-E/(R*T_p))  (Kissinger)
Substituting S_dot = W_B*(dalpha/dt)_max into the slab solution and imposing P_centre <= P_max:

  beta_crit = e * K * M * T_p * (P_max^2 - P0^2) / ( mu * W_B * E * L^2 )

Scalings that fall out directly:
  beta_crit ~ 1/L^2       (halving the section quadruples the safe rate)
  beta_crit ~ K ~ d_p^2 * eps^3/(1-eps)^2   (Carman-Kozeny: coarser powder is dramatically safer)
  beta_crit ~ 1/W_B       (lower binder loading is linearly safer)
  beta_crit ~ (P_max^2 - P0^2) ~ 2*P0*sigma_green  for small overpressure, i.e. running the furnace at ELEVATED pressure raises the safe rate roughly linearly in P0 (Tsai's pressurised-atmosphere result), while VACUUM debinding LOWERS it for a fixed absolute sigma_green unless Knudsen enhancement of K compensates.
Debinding TIME scalings (German): diffusion control t ~ L^2/D_eff ; permeation control t ~ mu*W_B*L^2/(K*P).
For non-slab geometry replace L by the Shivashankar-German effective length L_eff = V/A.
    - **when_to_use**: As the closed-form design equation for the first-cut cycle, as the analytic check on any FE result, and as the sensitivity/uncertainty propagation kernel for the unknown binder content W_B.
    - **inputs_needed**: K, mu, M, W_B, E, T_p, P_max (= f(sigma_green)), L. T_p and E come from multi-rate TGA; W_B from ash/TGA residue on the actual slurry.
    - **limitations**: Assumes the peak of gas generation coincides with the peak of pressure (true only if K is roughly constant across the peak — it is not, K rises steeply), assumes single-step kinetics (a real acrylate has 2-4 steps), and assumes the pressure criterion rather than the boiling criterion governs (false below ~300 C).
    - **source**: Derived by me from the model equations of German (1987) / Feng & Lombardo (2002, 2003) / Lombardo & Retzloff (2020) plus standard Kissinger peak-condition algebra. The 1/L^2 dependence and the reported strong dependence of critical heating rate on part radius are explicitly stated in those sources; the assembled closed form is not quoted verbatim from any one paper.
  -
    - **name**: Saturated-regime (pre-percolation) model: diffusion through the polymer + boiling criterion
    - **formulation**: Before open porosity forms, degradation products move by diffusion through the softened/decomposing polymer:
  dC/dt = div( D(C,T) grad(C) ) + r_gen(T, alpha)
with a general radial operator valid for slab/cylinder/sphere:
  dC/dt = (1/x^s) d/dx [ x^s * D(C,T) * dC/dx ] + r_gen,   s = 0, 1, 2
DEFECT CRITERION (boiling / bubble nucleation), not a stress criterion:
  p_i(C_centre, T) = gamma_i * x_i * P_sat,i(T)  >=  P_ambient + 2*sigma_surf/r_nucleus
Critical heating rate = the largest beta for which this is never satisfied anywhere in the body.
When a porous shell has already formed on the outside (shrinking-core), the core boundary condition becomes flux-coupled to the shell resistance:
  C_surface_of_core = f( surface flux, gas transport coefficient in the shell, shell thickness )
and the shell itself is transported with a combined viscous+diffusive (dusty-gas) flux.
    - **when_to_use**: From room temperature to the percolation threshold of the pore network (~first 10-20% of binder mass loss). This is where 65% of crack initiation happens in VPP, and where LCM differs most from MIM.
    - **inputs_needed**: D(C,T) for the degradation products in the partially-degraded network (hard to get; can be inferred by fitting the low-temperature mass-loss tail and by pressurised-TGA), vapour pressures P_sat,i(T) of the identified species (from TGA-FTIR / TGA-MS / Py-GC-MS of the actual green body), and the percolation threshold of the pore network.
    - **limitations**: D(C,T) is the weakest link and is essentially unmeasurable directly. The thermoset nature of a photopolymer means there is no true 'molten binder' phase - the network degrades in place - so the classical formulation (written for thermoplastics) needs adapting: the correct picture is a rubbery, chain-scissioning network with a rising free volume.
    - **source**: Matar, Edirisinghe, Evans, Twizell, JACerS 79 (1996) 749-755, DOI 10.1111/j.1151-2916.1996.tb07938.x; Song, Edirisinghe, Evans, Twizell, J. Mater. Res. 11 (1996) 830-840; Matar et al., J. Mater. Sci., DOI 10.1007/BF01153938; Oliveira et al., Int. J. Heat Mass Transfer 42 (1999) 3307-3329.
  -
    - **name**: Two-phase (liquid + gas) Darcy model with capillarity — Barone & Ulicny / Stangle & Aksay
    - **formulation**: Liquid (molten binder) phase:
  u_l = -(K * k_rl(S) / mu_l) * grad(P_l),   P_l = P_g - P_c(S)
  P_c(S) = (gamma * cos(theta) / sqrt(K/eps)) * J(S)      (Leverett J-function)
Gas phase:
  u_g = -(K * k_rg(S) / mu_g) * grad(P_g)
Relative permeabilities (Brooks-Corey / cubic):
  k_rl = S_e^3 ,  k_rg = (1 - S_e)^3 ,  S_e = (S - S_irr)/(1 - S_irr)
Saturation transport with evaporation:
  eps * dS/dt + div(u_l) = -m_evap / rho_l
Coupled energy equation (Stangle & Aksay):
  (rho*c_p)_eff * dT/dt + (rho_g c_pg u_g + rho_l c_pl u_l) . grad(T) = div(k_eff grad T) + sum_i (deltaH_i * r_i)
where deltaH_i covers pyrolysis (endo), combustion (exo) and evaporation (endo).
    - **when_to_use**: ONLY if the Lithoz copper slurry turns out to contain a substantial non-reactive diluent / plasticiser / solvent that liquefies and migrates. Commercial Lithoz slurries are documented to contain a proprietary NON-REACTIVE solvent, so a liquid phase very likely does exist at low temperature — this branch cannot be dismissed without measurement.
    - **inputs_needed**: gamma, cos(theta) for the liquid on copper, mu_l(T), S_irr, the J-function shape, and the evaporation kinetics. All require dedicated experiments.
    - **limitations**: Barone & Ulicny concluded capillary migration dominates most binder removal for thermoplastic systems; Oliveira-type models concluded the opposite (pressure-forced flow dominates). The disagreement is real and unresolved, and it turns on the binder viscosity and the pore size. For a cross-linked photopolymer with a minor solvent fraction, only the solvent participates.
    - **source**: Barone & Ulicny, J. Am. Ceram. Soc. 73 (1990) 3323-3333; Stangle & Aksay, Chem. Eng. Sci. 45 (1990) 1719-1731; Metall. Mater. Trans. B 33 (2002) DOI 10.1007/s11663-002-0058-6.
  -
    - **name**: Permeability evolution: Carman-Kozeny + saturation + percolation
    - **formulation**: Carman-Kozeny with the Kozeny constant k0 ~ 5:
  K = eps_open^3 * d_p^2 / ( 36 * k0 * (1 - eps_open)^2 )
or equivalently K = eps^3 / ( 5 * S_v^2 * (1-eps)^2 ), S_v = specific surface per unit solid volume;
alternative form used in the geoscience literature: K_CK = d_p^2/(16*F_s) * (eps/tau), with F_s*tau = Kozeny constant.
Coupling to binder conversion:
  eps_open(alpha) = eps_total * alpha          (binder-vacated fraction)
  eps_total = V_binder / V_green               (= 1 - solids loading)
With residual liquid saturation S:
  K_eff = K(eps_total) * (1 - S)^3             (cubic relative permeability)
PERCOLATION correction near the onset of connectivity (essential, because C-K predicts finite K at any eps > 0, which is wrong):
  K = K_0 * ( eps_open - eps_c )^t   for eps_open > eps_c, K = 0 below
  with eps_c ~ 0.15-0.3 for continuum percolation in a random packing and t ~ 2 for 3-D transport exponents.
Klinkenberg / Knudsen correction on top:
  K_app = K_inf * (1 + b_K / P),   b_K ~ 4*c*lambda*P / r_pore
Transition-regime diffusion (Bosanquet):
  1/D_eff = 1/D_molecular + 1/D_Knudsen,   D_Knudsen = (2/3)*r_pore*sqrt(8*R*T/(pi*M))
  Kn = lambda / r_pore, with lambda = 1/(sqrt(2)*pi*sigma^2*n)
    - **when_to_use**: Everywhere in the open-pore regime; it is the single most important nonlinearity in the whole model because K rises by 3+ orders of magnitude across the burnout, which is why a constant-beta cycle is grossly suboptimal.
    - **inputs_needed**: d_p (copper powder d50 and PSD), solids loading (vol%), tortuosity, and ideally a measured K on a partially-debound sample (transient He permeametry as in PMC6926824).
    - **limitations**: The percolation threshold eps_c and exponent t for a DEBINDING pore network are not established in the debinding literature — I could not verify them; they are taken from general continuum-percolation results and must be treated as fitted parameters. Carman-Kozeny is known to fail for broad PSDs and for anisotropic layered packings, which is exactly what an LCM body is.
    - **source**: Carman-Kozeny: DoITPoMS (https://www.doitpoms.ac.uk/tlplib/powder/carman.php), SPE (https://onepetro.org/spe/general-information/1540/Estimating-permeability-based-on-Kozeny-Carman); use inside a debinding model: Tsai 1991 (DOI 10.1002/aic.690370408). Knudsen/Klinkenberg/Bosanquet: GW-Project chapter (https://books.gw-project.org/flux-equations-for-gas-diffusion-in-porous-media/chapter/molecular-knudsen-and-transition-regimes/). Percolation exponents: unverified for this application.
  -
    - **name**: Defect criteria set — the six inequalities the simulation must monitor
    - **formulation**: (1) BULK CRACKING (poroelastic):  b * ( P_centre - P0 )  >=  sigma_t(T, alpha)
    with Biot coefficient b -> 1 for a loosely bonded particle skeleton. Tsai: stress is tensile, maximal at the centre, hoop > radial in a cylinder.
(2) BLISTERING / BLOATING (pre-percolation, surface-limited): a gas-tight outer skin forms before the interior has vented, so
    P_sat,monomer(T) >= P0 + 2*sigma_surf/r_nucleus  at a subsurface plane -> bubble nucleates and lifts the skin.
    Mitigation: keep the surface OPEN (no early high-temperature skin formation, no oxide skin on copper).
(3) DELAMINATION at layer interfaces (LCM-specific, the governing one):
    sigma_zz(P) + sigma_thermal + sigma_shrinkage  >=  sigma_interlaminar(z)
    where sigma_interlaminar is set by the LOWEST degree-of-conversion plane in each layer. Because DoC and hence decomposition kinetics are graded through the layer, the local gas source and the local strength minimum COINCIDE. Practical model: give the layer-boundary a reduced sigma_t (cohesive zone) and an enhanced early dalpha/dt.
(4) SLUMPING / CREEP:  sigma_applied (self-weight + setter friction + support reactions) >= sigma_threshold ~ 0.2-25 kPa.
    Viscous-beam estimate of the sag rate for a simply-supported span L, thickness h:
      d(delta)/dt = 5 * rho * g * L^4 / ( 96 * eta_uniaxial * h^2 ),   eta_uniaxial = 3*eta (Trouton)
    Setter-friction tensile stress at the centre of a part of half-length L_s on a setter:
      sigma_friction = mu_f * rho * g * L_s   (~0.3 kPa for mu_f=0.3, rho=4500, L_s=20 mm)
(5) THERMAL-GRADIENT STRESS:  delta-T = beta*L^2/(2*a) ; sigma_th ~ E*alpha_CTE*delta-T/(3*(1-nu)).
    For copper this is negligible (delta-T ~ 0.2 K) — but it must still be evaluated to PROVE it is negligible, which is itself a publishable point.
(6) EXOTHERMIC RUNAWAY (oxidative debinding), Frank-Kamenetskii:
      delta = ( Q * rho * A * E / (k_eff * R * T_a^2) ) * L^2 * exp( -E/(R*T_a) )
      runaway if delta > delta_crit:  0.878 (slab), 2.00 (cylinder), 3.32 (sphere)
    plus a Semenov-type surface-cooling criterion for the whole part in the furnace.
    Coupled to an O2 transport/consumption field, because oxygen only reaches the interior after the surface has burned out.
    - **when_to_use**: Continuously, at every timestep and every node. The optimiser's feasible set is the intersection of all six.
    - **inputs_needed**: sigma_t(T, alpha) — measure by interrupted debinding + 3-point bend / B3B on the actual copper green body at a series of quench temperatures; sigma_interlaminar (measure in Z vs XY); eta(T) for the pre-sintered skeleton; Q and E for the oxidative branch; k_eff(alpha) by laser flash.
    - **limitations**: sigma_t(T, alpha) is the least-known input in the whole problem and is the direct denominator of criterion (1). Criterion (3) has essentially no published constitutive data for LCM bodies — I found qualitative mechanism papers but no measured interlaminar strength vs temperature.
    - **source**: (1) Tsai DOI 10.1002/aic.690370408; Lombardo DOI 10.1080/17436753.2019.1707393. (3) Open Ceramics S2666539523002031. (4) German, https://www.cavs.msstate.edu/publications/docs/2003/07/2003-16.pdf. (2),(5),(6) assembled by me from standard theory; the Frank-Kamenetskii values are classical but I did not find them applied to debinding in the literature — unverified in this context.
  -
    - **name**: Kinetics identification for an UNKNOWN proprietary binder
    - **formulation**: Step 1 — model-free isoconversional E_a(alpha) from >=3 (preferably 5) heating rates (e.g. 0.5, 1, 2, 5, 10 K/min) on the ACTUAL filled green body in the ACTUAL atmosphere:
  Friedman (differential):  ln( beta_j * dalpha/dT |_{alpha} ) = ln( A*f(alpha) ) - E_a(alpha)/(R*T_{alpha,j})
  KAS (integral):           ln( beta_j / T_{alpha,j}^2 )        = const - E_a(alpha)/(R*T_{alpha,j})
  Vyazovkin (numerical integral): minimise sum_i sum_{j!=i} [ I(E,T_alpha,i)*beta_j ] / [ I(E,T_alpha,j)*beta_i ]
Step 2 — fit a multi-component DAEM or independent-parallel-reaction (IPR) model:
  alpha_total(T) = sum_i c_i * alpha_i(T),  sum c_i = 1
  DAEM:  alpha_i = 1 - integral_0^inf exp[ -(A_i/beta) * integral_{T0}^{T} exp(-E/(R*T')) dT' ] * f_i(E) dE,  f_i = N(E_0i, sigma_i)
  IPR:   dalpha_i/dt = A_i * exp(-E_i/(R*T)) * (1-alpha_i)^{n_i}
Step 3 — convert mass loss to MOLAR gas release: S_dot [mol m^-3 s^-1] = (W_B/M_gas(alpha)) * dalpha/dt, with M_gas(alpha) from TGA-MS/FTIR speciation (it is NOT constant; early solvent has low M, late char-forming fragments have high M).
Step 4 — validate by predicting an unseen heating rate and an isothermal hold.
    - **when_to_use**: First thing. Everything downstream depends on S_dot(T, alpha), and with a proprietary binder there is no alternative to measuring it.
    - **inputs_needed**: TGA/DSC (multi-rate, multi-atmosphere: Ar, N2, N2/5%H2, air, CO2), TGA-FTIR or TGA-MS for speciation and M_gas, and dilatometry for the shrinkage coupling. Total slurry consumption can be kept to a few grams.
    - **limitations**: The filler is catalytic (Liau & Lombardo showed BaTiO3+Pt accelerates PVB burnout) so neat-resin kinetics are invalid; copper/copper-oxide is a known oxidation catalyst, so the air-atmosphere kinetics in particular will differ strongly from the neat binder. Also, TGA at mg scale has no internal pressure gradient — it measures the INTRINSIC source term only, which is exactly what you want for the model, but it means TGA can never by itself tell you the safe heating rate for a 20 mm part.
    - **source**: Isoconversional methods: Thermochim. Acta review, https://www.sciencedirect.com/science/article/abs/pii/S0040603124000297; NETZSCH model-free summary, https://kinetics.netzsch.com/en/features/model-free-analysis. M-DAEM applied to VPP resin with pressure prediction: Materials 18 (2025) 4004, DOI 10.3390/ma18174004. IPR vs DAEM for VPP Si3N4: PMC11990554. Catalytic filler effect: Liau & Lombardo, DOI 10.1111/j.1151-2916.2000.tb01609.x.
  -
    - **name**: Optimal heating-cycle synthesis (the deliverable)
    - **formulation**: Problem statement (Lombardo & Retzloff):
  minimise  t_f = integral_0^{t_f} dt
  subject to:
    the reaction-permeability PDE for P(x,t)
    dalpha/dt = k(T)*f(alpha)                       (from the measured kinetics)
    dT/dt = beta(t),  0 <= beta(t) <= beta_furnace_max
    g1: max_x P(x,t) <= P_max(T, alpha) := P0 + sigma_t(T,alpha)/b
    g2..g6: the remaining defect criteria above
    alpha(t_f) >= alpha_target (e.g. 0.999)
Solution routes:
  (a) Pseudo-steady-state + calculus of variations -> analytic/semi-analytic optimal beta(t). Lombardo & Retzloff showed this agrees with full FE and that the optimum is a CONTINUOUSLY INCREASING heating rate, strictly better than any sequence of isothermal holds at the same pressure cap.
  (b) Feedback/process-control form: hold P_centre at P_max by manipulating beta(t) — a PI controller on the simulated pressure, which is the practical realisation and is robust to kinetic-parameter error.
  (c) Constant-mass-loss-rate ('uniform rate') stepwise schedule derived from the multi-component decomposition characteristics — the published VPP-specific realisation of the same idea.
  (d) Diffusion-controlled variant for the pre-percolation regime (Lombardo 2015, JACerS 98, DOI 10.1111/jace.13284).
    - **when_to_use**: After the kinetics and the strength-vs-temperature curve are in hand. Note that for copper the cycle must then be spliced to the sintering cycle such that neck formation OVERLAPS the end of binder removal (closing the zero-strength window).
    - **inputs_needed**: Everything above, plus P_max(T, alpha) which requires sigma_t(T, alpha).
    - **limitations**: The 'optimal' cycle is only as good as P_max; if sigma_t is uncertain by 2x, the cycle time is uncertain by ~2x (beta_crit is linear in P_max^2 - P0^2, which is ~linear in sigma_t for small overpressure). Robust/chance-constrained optimisation over the uncertain W_B and sigma_t is therefore the correct formulation for an unknown proprietary binder, not deterministic optimisation.
    - **source**: Lombardo & Retzloff, Adv. Appl. Ceram. 119 (2020), DOI 10.1080/17436753.2019.1707393; Lombardo, JACerS 98 (2015), DOI 10.1111/jace.13284; Lombardo & Retzloff, DCDS-B, DOI 10.3934/dcdsb.2021034; Yun & Lombardo, Adv. Appl. Ceram. (2009), DOI 10.1179/174367508X306505; uniform-rate stepwise: Duan et al., Addit. Manuf. (2024), https://www.sciencedirect.com/science/article/abs/pii/S2214860424001659.
- **open_questions**:
  - What is the actual binder MASS fraction W_B and volume fraction of the Lithoz copper slurry, and how is it split between reactive (meth)acrylate network, non-reactive solvent/diluent, dispersant and photoinitiator? W_B appears linearly in beta_crit, so this is the single largest source of uncertainty. It is directly measurable (TGA residue + pycnometry + ash) on a few grams without any disclosure from Lithoz — this should be experiment #1.
  - What is the copper powder d50 and PSD? K scales as d_p^2, so a 10 um vs 3 um powder is a ~10x difference in the safe heating rate. LMM copper powders are coarser than LCM ceramic powders because UV must penetrate, but I found no published d50 for a Lithoz/LMM copper feedstock.
  - Is there a measured permeability, in-plane and through-layer, for ANY vat-photopolymerised green body at partial binder conversion? I found no such measurement. The anisotropy ratio K_xy/K_z is the key unknown for predicting delamination vs bulk cracking, and the isotropic 2.37e-15 m^2 alumina figure is the only usable anchor.
  - What is sigma_t(T, alpha) — the tensile/flexural strength of the copper green body as a function of temperature AND binder conversion — and what is the corresponding interlaminar (Z-direction) strength? This is the denominator of the primary crack criterion and I found no data for a metal-filled photopolymer.
  - Where exactly is the percolation threshold alpha_c at which open porosity first connects in a 50 vol% solids photopolymer body, and what are K_0 and the exponent t in K ~ (eps_open - eps_c)^t? Nothing in the debinding literature quantifies this; it is the hinge between the two transport regimes.
  - Does copper (or Cu2O formed in situ) catalyse the decomposition of the acrylate binder, and by how much? Liau & Lombardo proved a catalytic effect for BaTiO3+Pt on PVB. If copper is strongly catalytic in air the onset temperature and peak sharpness will shift enough to invalidate any schedule transferred from a ceramic LCM material.
  - What is the heat of reaction (per kg binder) under each candidate atmosphere, and does a Frank-Kamenetskii analysis predict runaway for a 20 mm copper section in any of them? I could not find a single debinding paper that applies a formal thermal-explosion criterion, despite exotherms being repeatedly blamed for cracking.
  - Is a CO2 (endothermic, Boudouard-reverse) burnout atmosphere viable for copper? The endothermic-oxidant idea appeared only in patent literature; there is no peer-reviewed debinding study of CO2 burnout for copper that I could verify.
  - At what temperature do copper sinter necks first carry measurable strength (i.e. where does the zero-strength window close)? German's bronze data show the minimum near 400 C with recovery by 600 C, but I found no equivalent in-situ strength-vs-temperature curve for a fine copper powder compact.
  - Does the N2/5%H2 benefit reported for Si3N4 VPP (5 mm crack-free vs 4 mm) transfer to copper, where H2 is simultaneously required for Cu2O reduction and is a hydrogen-embrittlement risk if oxide and H2 coexist? The mechanism claimed (hydrocarbon formation spreading the gas-evolution pressure) is plausible but I could not verify it quantitatively.
  - What is the effective thermal conductivity and diffusivity of the copper green body as a function of alpha? I asserted thermal gradients are negligible using an assumed a = 1e-6 m^2/s; this needs a laser-flash measurement to be publishable, and if k_eff collapses when the polymer leaves (before necks form) the conclusion could change in the brown state.
  - Which of the two competing claims about the dominant liquid-transport mechanism applies here: Barone & Ulicny (capillary migration dominates) or Oliveira et al. (pressure-forced flow dominates)? The answer depends on whether the Lithoz non-reactive solvent forms a mobile liquid phase at all, which is measurable by interrupted-debinding gravimetry plus cross-section EDS/neutron imaging.
  - Can a McAleer-style neutron-imaging or high-temperature in-situ CT experiment resolve the residual binder profile in a COPPER green body? Neutrons see hydrogen well and copper is relatively transparent to them, so this may be a stronger technique here than for ceramics — and would be a novel, publishable validation of the transport model.
  - What layer thickness and pixel size does the 2M30 actually run with this copper slurry, and what is the resulting degree-of-conversion profile through each layer? This sets the delamination cohesive-zone parameters and I could find no authoritative specification for the 2M30's layer range.
- **references**:
  -
    - **citation**: German, R. M., 'Theory of Thermal Debinding', International Journal of Powder Metallurgy, 1987.
    - **url**: https://www.researchgate.net/publication/279591269_Theory_of_Thermal_Debinding
    - **why**: The foundational paper: defines the diffusion / permeation / wicking control regimes and gives the scaling of removal time with particle size, section thickness, porosity, temperature and pressure gradient. Every later model is a refinement of this.
  -
    - **citation**: Tsai, D.-S., 'Pressure buildup and internal stresses during binder burnout: Numerical analysis', AIChE Journal 37 (1991) 547-554, DOI 10.1002/aic.690370408.
    - **url**: https://aiche.onlinelibrary.wiley.com/doi/abs/10.1002/aic.690370408
    - **why**: First proper coupling of pyrolysis kinetics + Carman-Kozeny/Wakao-Smith slip flow + elasticity to get the stress field. Establishes that stresses are tensile, centre-maximal, hoop>radial, and that pressurising the furnace atmosphere suppresses them — a directly actionable process lever.
  -
    - **citation**: Stangle, G. C. & Aksay, I. A., 'Simultaneous momentum, heat and mass transfer with chemical reaction in a disordered porous medium: application to binder removal from a ceramic green body', Chemical Engineering Science 45 (1990) 1719-1731.
    - **url**: https://www.sciencedirect.com/science/article/abs/pii/0009250990870503
    - **why**: The most complete continuum formulation (momentum + heat + mass + reaction, two-phase, disordered medium). This is the template for the full multiphysics model if you want a defensible 'elite-level' simulation rather than a reduced-order one.
  -
    - **citation**: Barone, M. R. & Ulicny, J. C., 'Liquid-phase transport during removal of organic binders in injection-molded ceramics', J. Am. Ceram. Soc. 73(11) (1990) 3323-3333.
    - **url**: https://www.researchgate.net/publication/229745172_Liquid-Phase_Transport_During_Binder_Removal_of_Organic_Binders_in_Injection-Molded_Ceramics
    - **why**: The capillary/liquid-migration branch. Needed to decide (and to justify in a paper) whether the Lithoz non-reactive solvent fraction migrates or simply evaporates in place.
  -
    - **citation**: Matar, S. A., Edirisinghe, M. J., Evans, J. R. G. & Twizell, E. H., 'Diffusion of Degradation Products in Ceramic Moldings during Pyrolysis: Effect of Geometry', J. Am. Ceram. Soc. 79 (1996) 749-755, DOI 10.1111/j.1151-2916.1996.tb07938.x.
    - **url**: https://ceramics.onlinelibrary.wiley.com/doi/abs/10.1111/j.1151-2916.1996.tb07938.x
    - **why**: Gives the single general slab/cylinder/sphere diffusion equation and explicitly computes the CRITICAL HEATING RATE for the pre-porosity regime, validated on 3 mm plates. This is the model for the first, most dangerous ramp of an LCM cycle.
  -
    - **citation**: Song, J. H., Edirisinghe, M. J., Evans, J. R. G. & Twizell, E. H., 'Modeling the effect of gas transport on the formation of defects during thermolysis of powder moldings', J. Materials Research 11(4) (1996) 830-840.
    - **url**: https://www.cambridge.org/core/journals/journal-of-materials-research/article/abs/modeling-the-effect-of-gas-transport-on-the-formation-of-defects-during-thermolysis-of-powder-moldings/976842CBDBCF8EA8589AB527BDEC79E7
    - **why**: Couples multi-regime gas flow in the porous shell to polymer-melt transport in the core with a moving boundary, and identifies BOILING of the polymer-monomer solution as the defect mechanism — the correct criterion in the saturated regime, distinct from the stress criterion.
  -
    - **citation**: Matar, S. A., Edirisinghe, M. J., Evans, J. R. G., Twizell, E. H. & Song, J. H., 'Modelling the removal of organic vehicle from ceramic or metal mouldings: the effect of gas permeation on the incidence of defects', J. Materials Science, DOI 10.1007/BF01153938.
    - **url**: https://link.springer.com/article/10.1007/BF01153938
    - **why**: The shrinking-core + porous-shell resistance model; quantifies how the outer porous layer's transport resistance feeds back on defects nucleating in the core.
  -
    - **citation**: Feng, K. & Lombardo, S. J., 'Modeling of the Pressure Distribution in Three-Dimensional Porous Green Bodies during Binder Removal', J. Am. Ceram. Soc. 86 (2003), DOI 10.1111/j.1151-2916.2003.tb00005.x; and 'Pressure distribution during binder burnout in three-dimensional porous ceramic bodies with anisotropic permeability', J. Mater. Res. 17 (2002), DOI 10.1557/JMR.2002.0213.
    - **url**: https://ceramics.onlinelibrary.wiley.com/doi/10.1111/j.1151-2916.2003.tb00005.x
    - **why**: Analytical solutions for parallelepiped and cylinder WITH ANISOTROPIC PERMEABILITY, plus explicit pressure scaling laws. This is the paper that makes the LCM layered-anisotropy case tractable analytically, and it validates the pseudo-steady-state assumption.
  -
    - **citation**: Lombardo, S. J. & Retzloff, D. G., 'Reaction-permeability optimum time heating policy via process control for debinding green ceramic components', Advances in Applied Ceramics 119 (2020) DOI 10.1080/17436753.2019.1707393.
    - **url**: https://journals.sagepub.com/doi/10.1080/17436753.2019.1707393
    - **why**: The optimal-cycle formulation: PDE + kinetics ODE + T(t) ODE + algebraic pressure constraint, solved by FE-with-controller and by variational calculus on the PSSA. The result — a continuously increasing heating rate beats holds — is the design principle for the deliverable cycle.
  -
    - **citation**: Lombardo, S. J. & Retzloff, D. G., 'Modeling, approximation, and time optimal temperature control for binder removal from ceramics', Discrete & Continuous Dynamical Systems B, DOI 10.3934/dcdsb.2021034.
    - **url**: https://www.aimsciences.org//article/doi/10.3934/dcdsb.2021034
    - **why**: The rigorous version with L2 error analysis and singular perturbation justification of the PSSA, plus a concrete parameter set (E = 2.22e5 J/mol, A = 1.67e16 1/s, P_max = 1.5-2.0e5 Pa, beta_max = 10 K/min) usable as a sanity benchmark for your own solver.
  -
    - **citation**: Lombardo, S. J., 'Minimum Time Heating Cycles for Diffusion-Controlled Binder Removal from Ceramic Green Bodies', J. Am. Ceram. Soc. 98 (2015), DOI 10.1111/jace.13284; and Yun, J. W. & Lombardo, S. J., 'Determination of rapid heating cycles for binder removal from open pore green ceramic components', Adv. Appl. Ceram. (2009), DOI 10.1179/174367508X306505.
    - **url**: https://ceramics.onlinelibrary.wiley.com/doi/10.1111/jace.13284
    - **why**: The diffusion-controlled counterpart of the permeation optimal-control problem (needed for the early, saturated ramp), and the experimentally validated rapid-cycle algorithm including the permeability threshold below which K starts to matter.
  -
    - **citation**: Liau, L. C. K. & Lombardo, S. J., 'Role of Length Scale on Pressure Increase and Yield of PVB-BaTiO3-Pt Multilayer Ceramic Capacitors during Binder Burnout', J. Am. Ceram. Soc. 83 (2000) 2645-2653, DOI 10.1111/j.1151-2916.2000.tb01609.x.
    - **url**: https://ceramics.onlinelibrary.wiley.com/doi/10.1111/j.1151-2916.2000.tb01609.x
    - **why**: Two things you need: (i) proof that the inorganic filler + metal CATALYSE binder decomposition (so measure kinetics on the copper-filled body, not the resin), and (ii) a quantified geometry/aspect-ratio effect on yield (optimum 1:3 height:length).
  -
    - **citation**: Shivashankar, T. S. & German, R. M., 'Effective Length Scale for Predicting Solvent-Debinding Times of Components Produced by Powder Injection Molding', J. Am. Ceram. Soc. 82 (1999), DOI 10.1111/j.1151-2916.1999.tb01888.x.
    - **url**: https://ceramics.onlinelibrary.wiley.com/doi/10.1111/j.1151-2916.1999.tb01888.x
    - **why**: Provides L_eff = V/A, the correct length scale to substitute for 'wall thickness' in beta_crit ~ 1/L^2 for real 3D LCM geometries (lattices, shelled parts, thin fins).
  -
    - **citation**: German, R. M., 'Strength Evolution in Debinding and Sintering', Center for Innovative Sintered Products, Penn State / CAVS.
    - **url**: https://www.cavs.msstate.edu/publications/docs/2003/07/2003-16.pdf
    - **why**: The quantitative basis for the strength side of every defect criterion: in-situ strength trajectory through the 400 C minimum, S = sigma_0(T)(X/D)^2 N_C/K neck-strength model, the 0.2-25 kPa distortion threshold stress, copper sintering viscosities (2e8-3e11 Pa.s at 850 C; 2.3e9 Pa.s at 800 C) and copper thermal-softening data (31-fold strength drop RT to 1000 C).
  -
    - **citation**: Xie, Z. et al., 'Theory and practice of rapid and safe thermal debinding in ceramic injection molding', Int. J. Applied Ceramic Technology 17 (2020), DOI 10.1111/ijac.13349.
    - **url**: https://ceramics.onlinelibrary.wiley.com/doi/abs/10.1111/ijac.13349
    - **why**: Defines and derives the CRITICAL THICKNESS separating diffusion-in-liquid-binder control from pore diffusion/permeation control, shows it depends only on particle size, solids content and binder composition, and uses it to justify a higher heating rate in the early stage — directly applicable to staging a copper LCM cycle.
  -
    - **citation**: 'Elimination of delamination cracks in ceramics manufactured using LCD stereolithography', Open Ceramics (2023), article S2666539523002031.
    - **url**: https://www.sciencedirect.com/science/article/pii/S2666539523002031
    - **why**: The LCM/VPP-specific delamination mechanism: each layer has a highly and a weakly cross-linked zone with different decomposition kinetics; the resulting anisotropy and gradient in decomposition rate drives interlaminar cracking, and post-curing plus slower rates suppress it. This is the physical justification for a cohesive-zone layer-interface model.
  -
    - **citation**: Wang, J., Qiu, T. et al., 'Study on defect-free debinding green body of ceramic formed by DLP technology', Ceramics International 46 (2020) 2438-2446.
    - **url**: https://www.sciencedirect.com/science/article/abs/pii/S0272884219327725
    - **why**: Hard experimental anchor for a DLP body: argon vs flowing air at 0.2 and 0.5 C/min, dye-penetration + SEM verification, and the TG/DSC staging (1% at 200-300 C, down to 74% mass by 600 C).
  -
    - **citation**: Pfaffinger, M., Mitteramskogler, G., Gmeiner, R. & Stampfl, J., 'Thermal Debinding of Ceramic-Filled Photopolymers', Materials Science Forum 825-826 (2015) 75, DOI 10.4028/www.scientific.net/MSF.825-826.75.
    - **url**: https://repositum.tuwien.at/handle/20.500.12708/67284
    - **why**: The Lithoz/TU Wien source itself: states that optimised geometry-specific cycles achieve CRACK-FREE debinding up to 20 mm wall thickness at up to 400 C. This is the benchmark, and the group behind the machine you are using.
  -
    - **citation**: Ożóg, P., Blugan, G., Kata, D. & Graule, T., 'Influence of the Printing Parameters on the Quality of Alumina Ceramics Shaped by UV-LCM Technology', J. Ceramic Science and Technology (2019), DOI 10.4416/JCST2019-00023.
    - **url**: http://www.ceramic-science.com
    - **why**: Documents the composition of a commercial Lithoz slurry (LithaLox HP500: 49 vol% alumina, density 2.52 g/cm3, (meth)acrylate reactive binder PLUS a proprietary NON-REACTIVE solvent, dispersant, photoinitiators) and the layer-adhesion/exposure-energy relationships. Establishes that there is a second, lower-temperature volatile species to model.
  -
    - **citation**: 'Vat Photopolymerization-Based Additive Manufacturing of Si3N4 Ceramic Structures: Printing Optimization, Debinding/Sintering, and Applications', PMC11990554.
    - **url**: https://pmc.ncbi.nlm.nih.gov/articles/PMC11990554/
    - **why**: Densest single source of VPP-debinding quantitative practice: <1 C/min conventional vs up to 10 C/min with optimised atmosphere, 65% of crack risk below 300 C, 95%N2/5%H2 giving 5 mm crack-free green bodies, carbon residue costing 469 -> 184 MPa, 450 C/5 h oxidative carbon strip, and a comparison of Coats-Redfern vs DAEM vs IPR kinetic models.
  -
    - **citation**: 'Pyrolysis Kinetics-Driven Resin Optimization for Enhanced Reliability in Ceramic Vat Photopolymerization Manufacturing', Materials 18 (2025) 4004, DOI 10.3390/ma18174004.
    - **url**: https://pmc.ncbi.nlm.nih.gov/articles/PMC12429858/
    - **why**: A complete worked example of exactly the workflow you need: multi-rate TGA -> 3-component modified DAEM (E0, sigma, logA, c for each pseudo-component) -> predicted maximum internal gas pressure (0.20-0.34 MPa) and its temperature -> resin selection. Gives numeric priors for acrylate activation energies (215-238 kJ/mol) and an R^2 > 0.9999 fit quality target.
  -
    - **citation**: 'A Systematic Study on Impact of Binder Formulation on Green Body Strength of Vat-Photopolymerisation 3D Printed Silica Ceramics', Polymers 15 (2023) 3141, DOI 10.3390/polym15143141.
    - **url**: https://pmc.ncbi.nlm.nih.gov/articles/PMC10383664/
    - **why**: Green strength (~15 MPa) vs monomer formulation for a VPP body, plus a real 0.5 C/min schedule with 4 h holds at 150/330/420 C and a documented case of a single monomer (NVP) decomposing sharply at 420 C and cracking the part — the clearest published demonstration of the source-term-sharpness -> cracking link.
  -
    - **citation**: UV-LCM of AlN-based photocurable dispersions, PMC7579482.
    - **url**: https://pmc.ncbi.nlm.nih.gov/articles/PMC7579482/
    - **why**: A fully specified real LCM debinding schedule (0.1 C/min to 120 C/6 h; 0.5 C/min to 360 C/16 h; 0.5 C/min to 460 C/6 h) with 40 vol% solids, 25 um layers, HDDA binder, and observed defects (delamination from insufficient cure depth, microcracking during debinding). Use as the starting schedule to beat.
  -
    - **citation**: 'Towards Creation of Ceramic-Based Low Permeability Reference Standards', PMC6926824.
    - **url**: https://pmc.ncbi.nlm.nih.gov/articles/PMC6926824/
    - **why**: The only directly usable measured permeability for a DEBOUND/pre-sintered ceramic body: 2.37e-15 m^2 (Klinkenberg-corrected) at 36.0% open porosity by He transient permeametry. Seeds K in the model and defines the measurement technique to replicate on the copper body.
  -
    - **citation**: GW-Project, 'Flux Equations for Gas Diffusion in Porous Media' — chapter: Molecular, Knudsen and Transition Regimes.
    - **url**: https://books.gw-project.org/flux-equations-for-gas-diffusion-in-porous-media/chapter/molecular-knudsen-and-transition-regimes/
    - **why**: Clean open-access statement of Kn = lambda/lambda_p with lambda_p = sqrt(k), the mean-free-path formula and worked N2 value (6.5e-8 m at 20 C/1 atm), and the permeability boundary (k > ~1e-12 m^2 for the molecular regime) that proves green bodies are in the transition regime and require Klinkenberg/dusty-gas treatment.
  -
    - **citation**: Fraunhofer HTL, Debinding research area (thermo-optical measurement, coupled FE debinding simulation, in-situ acoustic and gas emission).
    - **url**: https://www.htl.fraunhofer.de/en/ResearchAreas/thermal-processes/debinding.html
    - **why**: Describes an operating industrial version of the exact simulation architecture proposed here (temperature+reaction heat, local kinetics, gas concentration and pressure, mechanical stress) plus the supporting metrology (0.1% mass reproducibility, laser-flash k, gas permeability, acoustic-emission damage detection). Useful both as a design template and as a potential collaboration/benchmark partner.
  -
    - **citation**: McAleer, C. et al., 'Binder removal from ceramic stereolithography green bodies: A neutron imaging and thermal analysis study', J. Am. Ceram. Soc. (2023), DOI 10.1111/jace.19095.
    - **url**: https://ceramics.onlinelibrary.wiley.com/doi/10.1111/jace.19095
    - **why**: The key validation-technique paper: spatially resolved binder distribution during debinding of a vat-photopolymerised body by neutron imaging. This is the experiment that can validate a transport model's predicted alpha(x,t) field rather than just its integral mass loss — and neutrons should work even better on copper than on ceramics.
  -
    - **citation**: '4D insight into the defect evolution of additively manufactured ceramics during debinding and sintering', Additive Manufacturing (2025), article S2214860425002374.
    - **url**: https://www.sciencedirect.com/science/article/abs/pii/S2214860425002374
    - **why**: First high-temperature in-situ CT of defect nucleation and growth through debinding AND sintering of VPP ceramics, with quantitative temperature-dependent defect statistics. The state-of-the-art validation target and a strong model for the experimental half of a publication.
  -
    - **citation**: 'Influence of debinding and sintering conditions on the composition and thermal conductivity of copper parts printed from highly loaded photocurable formulations', Discover Applied Sciences 2 (2020), DOI 10.1007/s42452-020-04049-3.
    - **url**: https://link.springer.com/article/10.1007/s42452-020-04049-3
    - **why**: The closest published analogue to the Lithoz copper slurry: air debind at 400 C, H2 sinter at 980/1030/1050 C at 3 C/min, final C = 0.018 wt% and O down to 0.067 wt%. Note: full text was blocked by the publisher's bot protection, so the numbers here came from a search-engine extract and should be re-verified from the PDF.
  -
    - **citation**: Mosadegh, M. et al., 'Single-step thermal debinding for ceramics vat photopolymerization in less than 30 minutes', Ceramics International (2025), article S0272884225023417.
    - **url**: https://www.sciencedirect.com/science/article/abs/pii/S0272884225023417
    - **why**: Demonstrates that vacuum + rapid heating with porous graphite felts gives complete binder removal in <30 min (40-200x faster, ~3500x less energy) for VPP zirconia. The aggressive end-state target once a validated pressure model tells you where the constraint actually binds.
  -
    - **citation**: Duan, W. et al., 'Uniform rate debinding for Si3N4 vat photopolymerization 3D printing green parts using a specific-stage stepwise heating process', Additive Manufacturing (2024), article S2214860424001659.
    - **url**: https://www.sciencedirect.com/science/article/abs/pii/S2214860424001659
    - **why**: The practical, published implementation of constant-mass-loss-rate debinding for VPP parts, with an explicit formula for residual resin weight at each stage — i.e. the engineering realisation of Lombardo's constant-maximum-pressure optimal policy, already validated on the hardest VPP ceramic.
  -
    - **citation**: 'Isoconversional methods: A powerful tool for kinetic analysis and the identification of experimental data quality', Thermochimica Acta (2024), article S0040603124000297.
    - **url**: https://www.sciencedirect.com/science/article/abs/pii/S0040603124000297
    - **why**: Methodological reference for extracting E_a(alpha) from multi-rate TGA when the chemistry is unknown (Friedman, KAS, FWO, Vyazovkin), including why model-fitting is unreliable without a known mechanism. This is the legitimate way to handle the proprietary Lithoz binder.
  -
    - **citation**: Uhland, S. A. et al., 'Strength of Green Ceramics with Low Binder Content', J. Am. Ceram. Soc. 84 (2001), DOI 10.1111/j.1151-2916.2001.tb01098.x.
    - **url**: https://ceramics.onlinelibrary.wiley.com/doi/abs/10.1111/j.1151-2916.2001.tb01098.x
    - **why**: Quantifies how green strength collapses as binder is removed (e.g. Al2O3 strength 0.3 -> 7.6 MPa going from no binder to 2.5 vol% binder, a ~24x factor). This gives the shape of sigma_t(alpha) for the crack criterion as binder is progressively lost.
  -
    - **citation**: Binder Burnout Investigation on Lanthanum Strontium Manganite (WPI MQP report).
    - **url**: https://digital.wpi.edu/downloads/sn00b1354
    - **why**: Open full text with side-by-side TGA/DSC of the same green body in dry air, argon, Ar+5% air and N2 at identical 5 C/min, quantifying how much the atmosphere flattens the weight-loss bursts and suppresses the exotherms, plus the argument for inert-then-air staging to strip residual carbon. Directly transferable reasoning for copper.