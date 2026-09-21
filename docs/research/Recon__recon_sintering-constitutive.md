- **summary**: Continuum sintering modelling for a copper-filled LCM slurry reduces to three coupled problems: (i) a viscous/visco-plastic constitutive law with two independent porosity-dependent moduli plus a sintering stress; (ii) a microstructure (grain-size) evolution law that feeds back into the sintering stress and into the moduli; (iii) an identification problem that is structurally ill-posed if only free dilatometry is used.

The workhorse is the Skorohod–Olevsky Viscous Sintering (SOVS) law. In the linear-viscous form actually implemented at Sandia (Sierra/SM) and in MFront/Code_Aster it reads ε̇^in_ij = s_ij/(2η0(T)φ(ρ)) + (σ_kk − 3σ_s(ρ))/(18 η0(T) ψ(ρ)) δ_ij, with φ(ρ)=a1ρ^b1, ψ(ρ)=a2ρ^b2/(1−ρ)^c2, σ_s=σ_s0·a3ρ^b3, σ_s0=3α/r0, and ρ̇=−ρ tr(ε̇^in) (integrated exactly as ρ_{t+Δt}=ρ_t exp(−tr Δε^in)). Skorohod's closed forms are recovered for (a1,b1)=(1,2), (a2,b2,c2)=(2/3,3,1), (a3,b3)=(1,2), i.e. φ=(1−θ)², ψ=(2/3)(1−θ)³/θ, P_L=(3α/r0)(1−θ)². Effective moduli are G_eff=η0φ, K_eff=2η0ψ. Free sintering then collapses analytically to dθ/dt = −9αθ/(4 r η0) (equivalently ξ̇=−3σ_s0ξ/(4η0) with ξ=1−ρ), which is the linearisable kernel used for calibration: ln[−3(1−θ)³/(T θ̇ ψ)] = ln(rη0'/α) + Q/RT.

Alternatives: the Riedel–Svoboda–Zipse / Kraft–Riedel micromechanical family writes ε̇_I = ε̇^s_I + (1/E_vis)[σ_I − ν_vis(3σ_m − σ_I)] with σ^s_I=E_vis ε̇^s_I and Hillert-type grain growth ḋ=(γ_b M_b/2d)(F_d/F_p), i.e. it works in the Bordia–Scherer elastic–viscous-analogy variables (uniaxial viscosity E_vis, viscous Poisson ratio ν_vis) rather than (K,G). Abouaf's power-law visco-plastic law, ε̇^vp = A(T)σ_eqv^{N−1}[(3/2)c(ρ)s + f(ρ)I₁I] with σ_eqv=(3cJ₂+fI₁²)^{1/2}, is the correct choice for metals where creep is non-Newtonian (n≈3–8) — likely for Cu near 900–1050 °C — and is implemented in Abaqus through CREEP (swelling + creep increments) plus USDFLD for ρ. Cocks' and Riedel's laws are the mechanism-based analogues that supply c/f (or ψ/φ) from grain-boundary-diffusion micromechanics instead of fitting them.

The critical, under-appreciated point is identifiability: free dilatometry (σ=0) only ever constrains the product 2η0ψ (the bulk branch). φ (the shear branch) is invisible, yet it governs gravity slumping, setter friction drag, overhang sag and warpage. Separating them requires a deviatoric experiment: discontinuous sinter-forging, cyclic-loading dilatometry (Cai/Bordia 1997 — superimposed load cycles give E_p, and with radial strain, ν_p, in a single run), constrained/bilayer camber, or — cheapest and demonstrated on printed ceramics — a gravity-driven slumping/deflection artefact whose measured H/R ratio fixes a scalar shear-viscosity correction (β=8.7 in the porcelain FFF case).

Practical staged protocol, proven in the AM literature: (1) dilatometry at ≥3 heating rates → MSC Θ=∫(1/T)exp(−Q/RT)dt minimisation plus Wang–Raj iso-density Arrhenius regression to get Q (agreement of the two is the validity check; 350 vs 357 kJ/mol for porcelain); (2) pointwise inversion η0(T) = −3σ_s(ρ)/(18 ε̇^in ψ(ρ)) — heating/cooling hysteresis in η0 exposes unmodelled microstructure evolution; (3) non-linear regression of ψ exponents (Skorohod vs Hsueh ψ=(2/3)(1−θ)^A/θ^B vs Abouaf-type ψ=(2/3)(θ_c−θ)³/θ); (4) grain growth from interrupted runs; (5) FEM back-fit of anisotropic sintering stress (P_lR,P_lZ) against directional dilatometry; (6) shear viscosity from a slump artefact; (7) validation on an independent geometry. Shrinkage compensation is then the inverse problem solved by fixed-point iteration on the green geometry (Simufact/Netfabb-style), giving <3% residual deviation in published BJ work.
- **key_facts**:
  -
    - **fact**: The SOVS inelastic flow rule as implemented at Sandia (Sierra/SolidMechanics) and in MFront/Code_Aster is: eps_dot_in_ij = s_ij/(2*eta0(T)*phi(rho)) + (sigma_kk - 3*sigma_s(rho))/(18*eta0(T)*psi(rho))*delta_ij, with density evolution rho_dot = -rho*tr(eps_dot_in).
    - **source**: B. Lester, 'Verification of the Skorohod-Olevsky Viscous Sintering (SOVS) Model', SAND2017-12933R, Sandia, 16 Nov 2017, Eqs. 1 and 5, DOI 10.2172/1411315, https://www.osti.gov/servlets/purl/1411315/ ; corroborated by TFEL/MFront SOVS page https://thelfer.github.io/tfel/web/sovs.html
    - **confidence**: high
  -
    - **fact**: The standard SOVS closure functions are phi(rho)=a1*rho^b1, psi(rho)=a2*rho^b2/(1-rho)^c2, sigma_s(rho)=sigma_s0*a3*rho^b3, sigma_s0 = 3*alpha/r0 (alpha = surface tension, r0 = mean grain/particle radius). Skorohod's original theory is the special case (a1,b1)=(1,2), (a2,b2,c2)=(2/3,3,1), (a3,b3)=(1,2), i.e. phi=(1-theta)^2, psi=(2/3)(1-theta)^3/theta, P_L=(3*alpha/r0)(1-theta)^2.
    - **source**: SAND2017-12933R Eqs. 2-3 and Table 1 (parameters for 0.2 um ZnO, taken from Olevsky 1998 and Arguello et al. 2009), https://www.osti.gov/servlets/purl/1411315/ ; Cabo Rios et al., Acta Materialia 249 (2023) 118822, Eqs. 10-11, DOI 10.1016/j.actamat.2023.118822
    - **confidence**: high
  -
    - **fact**: Effective moduli are G_eff = eta0*phi and K_eff = 2*eta0*psi; with Skorohod closures K_eff = (4/3)*eta0*(1-theta)^3/theta, G_eff = eta0*(1-theta)^2.
    - **source**: pSeven case study on SOVS for 3D-printed ceramics, https://www.pseven.io/blog/use-cases/numerical-simulation-of-sintering-for-3d-printed-ceramics-via-sovs-model.html (Gp, Kp expressions); consistent with SAND2017-12933R Eq. 1
    - **confidence**: high
  -
    - **fact**: Under free sintering (sigma=0) SOVS collapses to rho_dot = (a3*sigma_s0/(2*a2*eta0))*rho^(1+b3-b2)*(1-rho)^c2; with Skorohod values this is xi_dot = -3*sigma_s0*xi/(4*eta0) with xi = 1-rho, i.e. in porosity form dtheta/dt = -9*alpha*theta/(4*r*eta0). This is the analytic verification case for any implementation.
    - **source**: SAND2017-12933R Eqs. 30-31, https://www.osti.gov/servlets/purl/1411315/ ; equivalent porosity form in Cabo Rios et al. Acta Mater. 249 (2023) 118822 Eqs. 8, 14-15
    - **confidence**: high
  -
    - **fact**: FREE DILATOMETRY ALONE CANNOT SEPARATE BULK FROM SHEAR. With sigma_ij = 0 only the hydrostatic branch is excited, so a free-sintering curve constrains only the product 2*eta0*psi (and sigma_s); phi (shear branch) is completely unconstrained. Any deviatoric probe (sinter-forging, cyclic-loading dilatometry, constrained/bilayer, gravity slumping) is required to fix phi.
    - **source**: Structural consequence of SAND2017-12933R Eq. 1 (set sigma=0); explicitly exploited in the two-stage calibrations of Cabo Rios et al. (Acta Mater. 249, 2023, 118822) and arXiv:2512.02591
    - **confidence**: high
  -
    - **fact**: A workable substitute for sinter-forging is a gravity-driven slump artefact: a thin printed cylinder sintered on its side, with the measured aspect ratio H/R used to back out a scalar multiplier on the shear viscosity G = eta*beta*(1-theta)^chi. A factor beta = 8.7 was needed to reproduce the experimental H/R = 0.83 for FFF porcelain; the same value then predicted an independent bar-deflection test.
    - **source**: 'Finite Element Prediction of Sintering Deformation in 3D-Printed Porcelain Filament', arXiv:2512.02591, Section 3.5 and Eq. 9, https://arxiv.org/pdf/2512.02591
    - **confidence**: high
  -
    - **fact**: Shear viscosity can be obtained pointwise (not just as a fitted function) by inverting the free-sintering dilatometry trace: eta0(T) = -3*sigma_s(rho)/(18*eps_dot_in(t)*psi(rho)). Plotting the resulting eta0 vs T separately for heating, dwell and cooling exposes unmodelled microstructure evolution as a hysteresis (eta0 rises during dwell and stays high on cooling), which is then absorbed into a grain-volume-ratio factor lambda(rho) = (a5/(rho_c-rho))^b5 multiplying the bulk branch.
    - **source**: Enhanced SOVS paper: 'Enhanced Skorohod-Olevsky viscous model incorporating microstructure evolution for FE analysis of ceramic sintering', J. Eur. Ceram. Soc. 44 (2024) 7730-7739, Eqs. 6, 7, 11, 14, DOI 10.1016/j.jeurceramsoc.2024.05.035, OA copy https://biblio.ugent.be/publication/01HY0QQH7QJ4V4WS6WF8N0HSQZ/file/01HYB4TDD0PE7V7ZFJW5HR8ES4.pdf
    - **confidence**: high
  -
    - **fact**: The Master Sintering Curve work-of-sintering integral is Theta(t,T) = integral_0^t (1/T)*exp(-Q/RT) dt, with density fitted to a sigmoid rho = rho0 + a/[1+exp(-(log Theta - log Theta0)/b)]^c. Q is obtained by minimising the mean square residual of the collapse across >=3 constant-heating-rate runs.
    - **source**: DiAntonio & Ewsuk, 'Master Sintering Curve and Its Application in Sintering of Electronic Ceramics', SAND2010-2158P, Eqs. 4-7, https://www.osti.gov/servlets/purl/1728557 ; original Su & Johnson, J. Am. Ceram. Soc. 79 (1996) 3211-3217, DOI 10.1111/j.1151-2916.1996.tb08097.x
    - **confidence**: high
  -
    - **fact**: Park's extension of the MSC corrects the integrand for grain-size trajectory: Theta = integral (G0/G)^w * (1/T)*exp(-Q/RT) dt with w = 4 for grain-boundary diffusion and w = 3 for lattice diffusion. It requires the grain-size history to be known independently. On MgAl2O4 the conventional Su-Johnson MSC gave Q = 450 kJ/mol, Park's 485 kJ/mol.
    - **source**: 'Master sintering curve with dissimilar grain growth trajectories: a case study on MgAl2O4', J. Eur. Ceram. Soc. 41 (2021) 1048-1051, DOI 10.1016/j.jeurceramsoc.2020.09.003, OA arXiv:2011.11634
    - **confidence**: high
  -
    - **fact**: The Wang-Raj (kinetic field) method is an independent Q estimator: at fixed density, plot ln[T*(drho/dt)] vs 1/T across heating rates; slope m gives Q = -m*R. Cross-checking WR against MSC is the standard internal-consistency test (350 vs 357 kJ/mol on porcelain; MSC and WR agree closely when a single mechanism dominates).
    - **source**: DiAntonio & Ewsuk SAND2010-2158P Eqs. 8-10, https://www.osti.gov/servlets/purl/1728557 ; arXiv:2512.02591 Section 3.2; original Wang & Raj, J. Am. Ceram. Soc. 73 (1990) 1172-1175, DOI 10.1111/j.1151-2916.1990.tb05175.x
    - **confidence**: high
  -
    - **fact**: Abouaf's power-law visco-plastic model is ε̇^vp = A(T)*sigma_eqv^(N(T)-1)*[(3/2)*c(rho)*s + f(rho)*I1*I], sigma_eqv = (3*c(rho)*J2 + f(rho)*I1^2)^(1/2), rho = rho0*exp(-eps_vol^vp). c and f are the deviatoric and hydrostatic weighting functions; N=1 recovers the linear-viscous (SOVS-like) limit.
    - **source**: 'A visco-plastic constitutive model for accurate densification and shape predictions in PM-HIP', arXiv:2506.11946, Eqs. 7-8, 12 (published as Powder Technology, DOI 10.1016/j.powtec.2025.121526); original Abouaf et al., Int. J. Numer. Methods Eng. 25 (1988) 191-212, DOI 10.1002/nme.1620250116
    - **confidence**: high
  -
    - **fact**: Abouaf-type models map cleanly onto the Abaqus CREEP subroutine: Delta_eps^vp = (1/3)*Delta_eps_sw*I + Delta_eps_cr*n, with Delta_eps_sw = 3*f(rho)*I1*A(T)*sigma_eqv^(N-1)*Delta_t (swelling/volumetric) and Delta_eps_cr = c(rho)*sigma_eq*A(T)*sigma_eqv^(N-1)*Delta_t (deviatoric); relative density is carried as a field variable via USDFLD because it is not available inside CREEP.
    - **source**: arXiv:2506.11946, Eqs. 9-11 and surrounding text, https://arxiv.org/pdf/2506.11946
    - **confidence**: high
  -
    - **fact**: A three-step, fully determined calibration exists for Abouaf-type laws: (1) set c=1, f=0 and fit A(T), N(T) to fully dense uniaxial compression at 0.2% offset stress; (2) get f(rho) = [rho_dot/(rho*A(T)*I1^N)]^(2/(N+1)) from hydrostatic (HIP/interrupted) densification data; (3) get c(rho) = [eps_dot_1/(A(T)*sigma_1^N)]^(2/(N-1)) - f(rho) from uniaxial tests at partial density. This is the metals analogue of the bulk/shear separation problem.
    - **source**: arXiv:2506.11946, Eqs. 14-15, 18, 21, https://arxiv.org/pdf/2506.11946
    - **confidence**: high
  -
    - **fact**: The Riedel/Kraft (RSZ-family) continuum law is written in Bordia-Scherer variables: eps_dot_I = eps_dot_s_I + (1/E_vis)*[sigma_I - nu_vis*(3*sigma_m - sigma_I)], with intrinsic sintering stress sigma_s_I = E_vis*eps_dot_s_I, rho_dot = -rho*(eps_dot_1+eps_dot_2+eps_dot_3), and modified Hillert grain growth d_dot = (gamma_b*M_b/(2d))*(F_d/F_p) where F_p is the pore-drag (Zener) factor and F_d corrects for a non-steady-state grain size distribution.
    - **source**: 'Modeling and simulation of sintering process across scales', arXiv:2211.00821, Eqs. 25-28, https://arxiv.org/pdf/2211.00821 ; primary: Riedel, Zipse & Svoboda, Acta Metall. Mater. 42 (1994) 445-452, DOI 10.1016/0956-7151(94)90499-5 and Kraft & Riedel, J. Eur. Ceram. Soc. 24 (2004) 345-361, DOI 10.1016/S0955-2219(03)00222-X
    - **confidence**: high
  -
    - **fact**: Isotropic continuum laws provably FAIL for constrained sintering and sinter-forging: an isotropic law cannot reproduce the uniaxial compressive stress required for zero radial shrinkage in sinter-forging, whereas an anisotropic law parameterised by sintering STRAINS (rather than relative density) does. A general transversely isotropic viscous formulation needs 5 constitutive parameters plus 2 free densification rates.
    - **source**: arXiv:2211.00821 Section on constitutive laws (Figs. 41-42), https://arxiv.org/pdf/2211.00821 ; primary: Bordia, Zuo, Guillon, Salamone & Rodel, 'Anisotropic constitutive laws for sintering bodies', Acta Mater. 54 (2006) 111-118, DOI 10.1016/j.actamat.2005.08.025 ; Li, Pan, Guillon & Cocks, Acta Mater. 58 (2010) 5980-5988, DOI 10.1016/j.actamat.2010.07.015
    - **confidence**: high
  -
    - **fact**: A pragmatic and numerically stable way to inject AM layer anisotropy into an otherwise isotropic continuum model is to make the SINTERING STRESS directionally dependent (P_lR, P_lZ) rather than the viscosity tensor - justified by Olevsky's result that elliptical/oriented pores produce an anisotropic sintering stress whose deviatoric part drives anisotropic shrinkage.
    - **source**: arXiv:2512.02591 Section 3.4, https://arxiv.org/pdf/2512.02591 ; theory: Wakai & Shinoda, Acta Mater. (2009) on anisotropic sintering stress for orthotropic particle packings, cited as ref [209] in arXiv:2211.00821
    - **confidence**: high
  -
    - **fact**: Cyclic loading dilatometry (CLD) determines the equilibrium elastic and viscous properties plus the sintering stress of a sintering compact at any temperature in a SINGLE experiment, with no interrupted tests, by superposing load cycles on a constant-heating-rate run and using the change in strain rate to get the uniaxial viscosity. Gillia et al. extended it to yield both required viscosity constants.
    - **source**: Cai, Mohanram (et al.) / Bordia, 'Determination of the Mechanical Response of Sintering Compacts by Cyclic Loading Dilatometry', J. Am. Ceram. Soc. 80 (1997) 445-452, DOI 10.1111/j.1151-2916.1997.tb02850.x (abstract-level; full text paywalled in this session). Isothermal CLD variant: Mohanram et al., J. Am. Ceram. Soc. 87 (2004) 192-196, DOI 10.1111/j.1551-2916.2004.00192.x
    - **confidence**: medium
  -
    - **fact**: Discontinuous (interrupted) hot forging / sinter-forging yields uniaxial viscosity, sintering stress, and both uniaxial and bulk viscosities as explicit functions of density and temperature for an isotropic microstructure. Intermittent-loading on WC-Co compacts separates the free-sintering strain-rate part from the viscoplastic part, from which axial viscosity and viscous Poisson ratio follow.
    - **source**: arXiv:2211.00821, paragraph following Eq. 28, https://arxiv.org/pdf/2211.00821
    - **confidence**: high
  -
    - **fact**: The SOVS integration scheme matters: the legacy McHugh-Riedel semi-implicit scheme (Taylor expansion of rates about t_n) was blamed for requiring very fine meshes to capture curvature/warpage. A fully implicit Newton-Raphson scheme with an 'inelastic predictor - elastic corrector' initialisation and merit function m = 0.5*[(r_rho/rho0)^2 + (E/sigma_s0)^2 * r_eps:r_eps] improves temporal and spatial convergence.
    - **source**: SAND2017-12933R, Sections 2.2 and 3, Eqs. 12-29, https://www.osti.gov/servlets/purl/1411315/
    - **confidence**: high
  -
    - **fact**: SOVS is not separable into an elastic predictor / plastic corrector because BOTH the direction and the magnitude of the inelastic strain rate depend directly on the stress state; conventional return-mapping algorithms therefore cannot be used.
    - **source**: SAND2017-12933R, Section 2.2, https://www.osti.gov/servlets/purl/1411315/
    - **confidence**: high
  -
    - **fact**: Shape compensation is solved as an inverse (reverse pre-compensation) problem on the green geometry, iterated to a user-set 'acceptable distortion' or maximum iteration count, and exported directly as STL. Published BJ results: max relative error of the forward prediction within 8%; max geometrical deviation of pre-compensated sintered parts vs CAD below 3%.
    - **source**: 'Modelling of geometrical deformation and compensation during sintering of binder jetting', Virtual and Physical Prototyping (2024), DOI 10.1080/17452759.2024.2443958 (abstract via DOAJ, OA); iteration/convergence-goal mechanics from Chalmers MSc thesis on Simufact Additive, https://odr.chalmers.se/items/78d530b0-ce82-431d-9e9c-6e67d097cec7
    - **confidence**: high
  -
    - **fact**: Simufact Additive's binder-jet sintering module is a visco-plastic multi-physics model including gravity, friction, creep and grain growth; the DEFAULT part-to-setter friction coefficient is 0.3, and the exposed material parameters include an 'activation energy of viscous flow' and a pre-exponential constant. Independent testing found default material parameters inadequate, that a 20,000 J/mol default had to be dropped to 5,000 J/mol to fit (a value far below literature), and that literature-realistic values caused solver crashes.
    - **source**: Chalmers MSc thesis, 'Product Design and Simulation for Metal Binder Jetting', Sections 3.3-3.5 and 5, https://odr.chalmers.se/items/78d530b0-ce82-431d-9e9c-6e67d097cec7
    - **confidence**: medium
  -
    - **fact**: Temperature non-uniformity is NOT negligible for larger parts: averaged relative density may look fine while local relative density spans 0.84-0.94 against a 0.91 average, and the final shape differs from the uniform-temperature prediction. A transient thermal analysis feeding the SOVS mechanical step is cheap insurance. (Copper's very high thermal conductivity makes the part itself near-isothermal, but the furnace/setter/radiation boundary condition still governs.)
    - **source**: Petrovic, Buljak & Cornaggia, FME Transactions 49 (2021) 719-725, DOI 10.5937/fme2103719P, https://www.mas.bg.ac.rs/_media/istrazivanje/fme/vol49/3/20_v._buljak_et_al.pdf
    - **confidence**: high
  -
    - **fact**: Choice of the normalized bulk viscosity function materially changes the fitted skeleton viscosity: for binder-jet 316L, fitting with the parameter-free Skorohod psi gave eta0 more than one ORDER OF MAGNITUDE lower than fitting with the Hsueh or Abouaf-type psi, while all three fit the densification curve similarly. Since eta0 sets gravity-driven shear distortion (G = eta0*phi), a bulk-only fit can silently ruin the distortion prediction.
    - **source**: Cabo Rios et al., Acta Materialia 249 (2023) 118822, Section 4.3 and Fig. 7, DOI 10.1016/j.actamat.2023.118822, OA https://research.chalmers.se/publication/535046/file/535046_Fulltext.pdf
    - **confidence**: high
  -
    - **fact**: Two-step sintering (Chen & Wang) exploits a kinetic window between grain-boundary DIFFUSION (active at T2) and grain-boundary MIGRATION (frozen at T2 by triple-junction drag, which has a higher activation energy for migration). Rule of thumb from the literature survey: T1-T2 typically below 150 C, T1 held only briefly to reach a critical density that renders pores unstable, then a long isothermal hold at T2.
    - **source**: IntechOpen chapter 'Fabrication of Fine-Grained Functional Ceramics by Two-Step Sintering or SPS', https://www.intechopen.com/chapters/67294 ; original Chen & Wang, Nature 404 (2000) 168-171, DOI 10.1038/35004548
    - **confidence**: medium
  -
    - **fact**: No published SOVS/Olevsky/Abouaf parameter set for pure copper (surface tension alpha, eta0(T), psi exponents, grain-growth k0/Q_G/rho_c) was found in this session. Every continuum sintering parameter for this copper slurry will have to be identified in-house from dilatometry; literature values exist only for ZnO, alumina, 316L, porcelain and LTCC.
    - **source**: unverified (negative result of ~15 searches plus arXiv/Crossref/Unpaywall queries in this session)
    - **confidence**: medium
  -
    - **fact**: Copper's absence of carbides means residual carbon cannot be gettered by the metal, so the debinding end-state (residual C, residual O) directly sets the initial condition rho0 and, via pore-gas pressure, the achievable final density. In a continuum sintering model this enters as (a) rho0 and its spatial field, and (b) an entrapped-gas back-pressure term that must be subtracted from the sintering stress: sigma_s_eff = sigma_s - p_gas(theta). No validated p_gas closure for Cu was found.
    - **source**: unverified
    - **confidence**: low
- **numbers**:
  -
    - **quantity**: SOVS parameter set (phi, psi, sigma_s exponents)
    - **value**: a1=1, b1=2; a2=2/3, b2=3, c2=1; a3=1, b3=2
    - **units**: dimensionless
    - **context**: 0.2 um ZnO powder; the canonical Skorohod closure. Used as the verification benchmark for any new SOVS implementation.
    - **source**: SAND2017-12933R Table 1 (from Olevsky 1998 and Arguello et al. 2009), https://www.osti.gov/servlets/purl/1411315/
  -
    - **quantity**: SOVS polynomial skeleton viscosity coefficients
    - **value**: a4=517, b4=-1066, c4=564
    - **units**: GPa*s (eta0 = a4*(T/T0)^2 + b4*(T/T0) + c4)
    - **context**: 0.2 um ZnO, 750-1000 C ramp at 5 C/min. T0 reference temperature not stated in the report - must be inferred before reuse.
    - **source**: SAND2017-12933R Table 1, https://www.osti.gov/servlets/purl/1411315/
  -
    - **quantity**: Surface tension alpha and grain radius r0 used with SOVS for ZnO
    - **value**: alpha = 1.27, r0 = 1
    - **units**: J/m^2 ; um
    - **context**: gives sigma_s0 = 3*alpha/r0 = 3.81 MPa. E = 123.7 GPa, nu = 0.356 for the same ZnO material.
    - **source**: SAND2017-12933R Table 1 and Section 3, https://www.osti.gov/servlets/purl/1411315/
  -
    - **quantity**: SOVS Arrhenius viscosity constants for Al2O3 (eta0 = A*T^n*exp(B/T))
    - **value**: A = 1.5172e-10, B = 27716, n = 4.26
    - **units**: A in Pa*s*K^-n ; B in K ; n dimensionless
    - **context**: DLP 3D-printed alumina, sintered to 1700 C, ~12% linear shrinkage; alpha = 0.9 J/m^2, mean particle radius 0.525 um. Identified by Abaqus/Standard + pSeven optimisation, RMSPE 0.64% in 187 iterations.
    - **source**: pSeven case study, https://www.pseven.io/blog/use-cases/numerical-simulation-of-sintering-for-3d-printed-ceramics-via-sovs-model.html (Safonov et al., Ceram. Int. 45 (2019) 19027-19035)
  -
    - **quantity**: Skeleton shear viscosity constants and Q for binder-jet 316L, Skorohod psi
    - **value**: A0/alpha = 35.53 ; Q = 144.1
    - **units**: s*m^-1*K^-1 ; kJ/mol (eta0 = A0*T*exp(Q/RT))
    - **context**: 316L binder jetting, green porosity 0.428, dilatometry 1000-1300 C, dwells 2-600 min, isotropic assumption. NOTE: with the parameter-free Skorohod psi, eta0 comes out >1 order of magnitude lower than with the parameterised forms.
    - **source**: Cabo Rios et al., Acta Mater. 249 (2023) 118822, Table 3, DOI 10.1016/j.actamat.2023.118822
  -
    - **quantity**: Hsueh-type bulk viscosity parameters for binder-jet 316L
    - **value**: A0/alpha = 2.03 ; Q = 217.2 ; A = 11.35 ; B = 0.49
    - **units**: s*m^-1*K^-1 ; kJ/mol ; dimensionless ; dimensionless (psi1 = (2/3)*(1-theta)^A/theta^B)
    - **context**: Best-performing model: RMSE < 0.45% on porosity over 1000-1300 C and up to ~90% relative density. A = 11.35 vs Skorohod's 3 shows how far a printed green structure deviates from the idealised packing.
    - **source**: Cabo Rios et al., Acta Mater. 249 (2023) 118822, Table 3, DOI 10.1016/j.actamat.2023.118822
  -
    - **quantity**: Abouaf-type critical-porosity bulk viscosity parameters for binder-jet 316L
    - **value**: A0/alpha = 1.82 ; Q = 220.1 ; theta_c = 0.508
    - **units**: s*m^-1*K^-1 ; kJ/mol ; dimensionless (psi2 = (2/3)*(theta_c-theta)^3/theta)
    - **context**: Green porosity was 0.428; theta_c = 0.508 fitted. Largest RMSE 0.98% at 1300 C/600 min; accuracy degrades below 15% porosity. The authors flag theta_c as physically ambiguous.
    - **source**: Cabo Rios et al., Acta Mater. 249 (2023) 118822, Table 3 and Conclusions, DOI 10.1016/j.actamat.2023.118822
  -
    - **quantity**: Porosity-corrected grain growth parameters (Olevsky form dG/dt = (k0/3G^2)*((1-rho_c)/(2-rho_c-rho))^(3/2)*exp(-Q_G/RT)) for binder-jet 316L
    - **value**: k0 = 29.65e-5 ; Q_G = 164.8 ; rho_c = 0.948
    - **units**: um^3/s ; kJ/mol ; dimensionless
    - **context**: Grain size up to ~40 um at 1300 C / 600 min despite ~10% residual porosity. LOM linear-intercept data scaled to EBSD by kG = 1.417 (standard suggests 1.5).
    - **source**: Cabo Rios et al., Acta Mater. 249 (2023) 118822, Table 2 and Section 4.2, DOI 10.1016/j.actamat.2023.118822
  -
    - **quantity**: Apparent densification activation energy, FFF porcelain
    - **value**: 350 (MSC) vs 357 (Wang-Raj)
    - **units**: kJ/mol
    - **context**: Dilatometry at 2, 5, 10 K/min, relative density 70% green to ~98% sintered. Agreement of the two independent estimators is the validity check that a single mechanism dominates.
    - **source**: arXiv:2512.02591, Section 3.2, https://arxiv.org/pdf/2512.02591
  -
    - **quantity**: Fitted bulk viscosity exponents for FFF porcelain (psi = (2/3)*(theta_ci - theta)^gamma/(theta - theta_cf)^zeta)
    - **value**: zeta = 1.5 ; gamma = 1.0 ; theta_ci = 0.35 ; theta_cf = 0.01
    - **units**: dimensionless
    - **context**: R^2 > 0.98. Exponents chosen so the regression slope reproduces the independently measured Wang-Raj activation energy - an elegant way to remove the Q/psi degeneracy. Particle radius 3.48 um measured, mullite surface energy 0.66 J/m^2 from literature.
    - **source**: arXiv:2512.02591, Section 3.3 and Eq. 10, https://arxiv.org/pdf/2512.02591
  -
    - **quantity**: Shear viscosity correction factor from slump test, FFF porcelain
    - **value**: beta = 8.7
    - **units**: dimensionless multiplier on G = eta*beta*(1-theta)^chi
    - **context**: Needed to reproduce the experimental H/R = 0.83 of a thin ring slumped on its side. Demonstrates quantitatively that the viscosity governing densification differs from the viscosity governing shear distortion by nearly an order of magnitude.
    - **source**: arXiv:2512.02591, Section 3.5, https://arxiv.org/pdf/2512.02591
  -
    - **quantity**: Prediction accuracy of anisotropic sintering FEM, FFF porcelain
    - **value**: <5% (shrinkage, radial and axial) ; <3% (porosity evolution)
    - **units**: % deviation from experiment
    - **context**: COMSOL Multiphysics, second-order elements; gravity slumping and bar deflection validated separately.
    - **source**: arXiv:2512.02591, Section 3.4, https://arxiv.org/pdf/2512.02591
  -
    - **quantity**: Calibrated Olevsky/Hsueh parameters for BMD 316L (y-oriented)
    - **value**: gamma_s = 1.42 J/m^2 ; rho_c = 0.96 ; K0 = 4.45e3 um^3/s ; A_gamma = 1.00 Pa*s*K^-1 ; A_delta = 1e-18 Pa*s*K^-1 ; Q_gamma = 193.1 kJ/mol ; Q_delta = 709.3 kJ/mol ; T_trans = 1025 C ; p = 17.1 ; lambda = 1.32 ; rho0 = 62.6%
    - **units**: mixed (see value)
    - **context**: Bound Metal Deposition 316L. Hsueh power-law bulk viscosity eta_b = 4*eta0*(1-theta)^p/(3*theta^lambda) (Olevsky recovered at p=3, lambda=1). Dual-phase austenite/delta-ferrite mixture rule for eta0. CAE alpha = 6.9e-6 K^-1, G0 = 10 um.
    - **source**: Materials 19 (2026) 3294, 'Effect of Print Orientation on Sintering Shrinkage of BMD 316L Stainless Steel', DOI 10.3390/ma19153294, https://pmc.ncbi.nlm.nih.gov/articles/PMC13467325/
  -
    - **quantity**: Calibrated Olevsky/Hsueh parameters for BMD 316L (z-oriented)
    - **value**: gamma_s = 1.30 J/m^2 ; K0 = 3.39e1 um^3/s ; A_gamma = 1.71 Pa*s*K^-1 ; Q_delta = 732.5 kJ/mol ; T_trans = 1014 C ; p = 15.6 ; lambda = 1.22 ; rho0 = 61.7%
    - **units**: mixed
    - **context**: Same material, different build orientation. The constitutive model stays isotropic; print-orientation anisotropy is absorbed entirely into orientation-specific parameter sets - a legitimate but non-predictive workaround.
    - **source**: Materials 19 (2026) 3294, DOI 10.3390/ma19153294, https://pmc.ncbi.nlm.nih.gov/articles/PMC13467325/
  -
    - **quantity**: Measured directional shrinkage anisotropy, BMD 316L
    - **value**: 13.5% (x), 13.7% (y), 14.3% (z)
    - **units**: % linear shrinkage
    - **context**: Final densities 7.72 / 7.76 / 7.69 g/cm^3 (97.1 / 97.6 / 96.7% relative). Simulated 13.7% (y), 14.1% (z), absolute error <=0.2 percentage points.
    - **source**: Materials 19 (2026) 3294, DOI 10.3390/ma19153294, https://pmc.ncbi.nlm.nih.gov/articles/PMC13467325/
  -
    - **quantity**: Abaqus CREEP solver settings used for sintering, BMD 316L
    - **value**: Delta_t_max = 30 s ; Delta_T_max = 30 C ; artificial gravity 0.01 m/s^2 ; CAX4T elements ; 517 elements ; total 80,810-82,120 s
    - **units**: mixed
    - **context**: 2D axisymmetric. The 'artificial gravity' of 0.01 m/s^2 (rather than 9.81) is used purely to stabilise the quasi-static solve in a free-sintering cylinder.
    - **source**: Materials 19 (2026) 3294, DOI 10.3390/ma19153294, https://pmc.ncbi.nlm.nih.gov/articles/PMC13467325/
  -
    - **quantity**: PSO calibration settings for an 11-parameter sintering model
    - **value**: swarm 110 particles, 10 iterations, w 0.9->0.4, HPSO-TVAC c1 2.5->0.5, c2 0.5->2.5, Vmax = 0.2*(xmax-xmin); cost 1.2324 -> 0.6138
    - **units**: dimensionless
    - **context**: Objective J = mean squared shrinkage residual + 0.25*(final shrinkage error)^2 + 0.05*[100*(final density error)]^2. A realistic reference for how much optimisation budget an 11-parameter sintering identification needs.
    - **source**: Materials 19 (2026) 3294, DOI 10.3390/ma19153294, https://pmc.ncbi.nlm.nih.gov/articles/PMC13467325/
  -
    - **quantity**: Grain-volume-ratio (lambda) parameters for porcelain stoneware, enhanced SOVS
    - **value**: a5 = 1 (fixed) ; b5 = 1.1877-1.2759 ; rho_c = 0.9310-0.9420
    - **units**: dimensionless
    - **context**: lambda = (a5/(rho_c - rho))^b5, multiplying the bulk branch of SOVS. rho_c rises monotonically with green density (1797 -> 2032 kg/m^3 across 18 dilatometry samples, three pressing pressures 150/300/550 kg/cm^2). Solved in Code_Aster.
    - **source**: J. Eur. Ceram. Soc. 44 (2024) 7730-7739, Table 5, DOI 10.1016/j.jeurceramsoc.2024.05.035
  -
    - **quantity**: Apparent activation energy for ZnO densification from MSC
    - **value**: ~394
    - **units**: kJ/mol
    - **context**: Determined by mean-square-residual minimisation on constant-heating-rate dilatometry; consistent with grain-boundary-diffusion-controlled intermediate-stage densification.
    - **source**: DiAntonio & Ewsuk, SAND2010-2158P, https://www.osti.gov/servlets/purl/1728557
  -
    - **quantity**: Wang-Raj activation energies for alumina systems
    - **value**: 440 +/- 40 (Al2O3) ; 585 +/- 40 (Al2O3 + 5 vol% TiO2) ; 730 +/- 60 (Al2O3 + 5 vol% ZrO2)
    - **units**: kJ/mol
    - **context**: Constant-heating-rate kinetic field method; the canonical benchmark values for the WR technique.
    - **source**: Wang & Raj, J. Am. Ceram. Soc. 73 (1990) 1172-1175, DOI 10.1111/j.1151-2916.1990.tb05175.x (values quoted via search result summary; primary text not retrieved in this session)
  -
    - **quantity**: MgAl2O4 activation energies, stage-resolved
    - **value**: 450 (Su-Johnson MSC) ; 485 (Park MSC) ; 400 (low density) ; 700 (high density)
    - **units**: kJ/mol
    - **context**: Baikowski S30CR spinel, CIP 300 MPa, 1, 2, 5 K/min to 1773 K. The 400 -> 700 kJ/mol jump between initial/intermediate and final stage is direct evidence that a SINGLE Q is inadequate over the whole densification range.
    - **source**: J. Eur. Ceram. Soc. 41 (2021) 1048-1051, DOI 10.1016/j.jeurceramsoc.2020.09.003, OA arXiv:2011.11634
  -
    - **quantity**: Two-step sintering windows (representative)
    - **value**: Y2O3: T1=1250 C, T2=1100 C, 6-30 h -> 99% density, 123 nm grains ; ZnO: T1=800, T2=750 -> 98%, 68 nm ; 3YSZ: T1=1300, T2=1200, 15 h -> 99.2%, 184 nm ; BaTiO3: T1=950, T2=900, 2 h -> 35 nm
    - **units**: C, h, %, nm
    - **context**: Literature survey table. T1-T2 gap typically <150 C. These are oxides - the transferability of the triple-junction-drag argument to FCC copper is unproven.
    - **source**: IntechOpen chapter 67294, https://www.intechopen.com/chapters/67294
  -
    - **quantity**: Default part/setter friction coefficient in Simufact Additive binder-jet sintering
    - **value**: 0.3
    - **units**: dimensionless (Coulomb)
    - **context**: Governs frictional drag distortion of the base of the part. No calibration guidance is provided by the software; the thesis used the default unchanged.
    - **source**: Chalmers MSc thesis, Section 3.3, https://odr.chalmers.se/items/78d530b0-ce82-431d-9e9c-6e67d097cec7
  -
    - **quantity**: Binder-jet sintering compensation accuracy
    - **value**: forward prediction max relative error <8% ; pre-compensated parts max geometrical deviation <3% vs CAD
    - **units**: %
    - **context**: Thermo-elastic-viscoplastic constitutive model with thermal, plastic, creep and porosity evolution + reverse shape pre-compensation.
    - **source**: Virtual and Physical Prototyping (2024), DOI 10.1080/17452759.2024.2443958 (abstract via DOAJ)
  -
    - **quantity**: Typical metal binder-jetting linear shrinkage
    - **value**: ~20% (up to 35% reported)
    - **units**: % linear
    - **context**: Sets the scale of the compensation problem. A highly-filled LCM copper slurry with ~45-55 vol% solids loading should be expected in the same regime - the higher the binder fraction, the larger the shrinkage.
    - **source**: secondary, from search-result summaries of Simufact/PIM International coverage; https://www.pim-international.com/simufact-introduces-new-metal-binder-jetting-module-to-compensate-for-sintering-distortion/ - treat as order-of-magnitude only
  -
    - **quantity**: Local vs average relative density spread from a non-uniform furnace temperature field
    - **value**: local 0.84-0.94 against a 0.91 average
    - **units**: relative density
    - **context**: SOVS + transient thermal analysis of a component scaled 8x. Demonstrates that averaged density is a misleading acceptance criterion.
    - **source**: FME Transactions 49 (2021) 719-725, DOI 10.5937/fme2103719P
  -
    - **quantity**: Viscous Poisson ratio implied by the Skorohod closures
    - **value**: nu_p = (2 - 3*theta)/(4 - 3*theta)
    - **units**: dimensionless
    - **context**: DERIVED here from G_eff = eta0*(1-theta)^2 and K_eff = (4/3)*eta0*(1-theta)^3/theta via nu = (3K-2G)/(2(3K+G)). Gives nu = 0.5 at theta=0 (incompressible) and nu = 0.286 at theta = 0.4. Useful as a sanity bound on any CLD/sinter-forging measurement.
    - **source**: unverified (algebraic derivation in this digest from the moduli in SAND2017-12933R; not cross-checked against a published closed form)
  -
    - **quantity**: Copper melting point / practical sintering window
    - **value**: 1084.6 C melting ; solid-state sintering typically 0.85-0.95 T_m
    - **units**: C
    - **context**: Implies a sintering dwell in roughly 950-1075 C for Cu, i.e. a very narrow window above which liquid-phase/slumping risk becomes severe. Any SOVS/Abouaf calibration must cover this band densely.
    - **source**: unverified (textbook value for Cu melting point; the 0.85-0.95 T_m rule of thumb is not sourced in this session)
- **models_or_methods**:
  -
    - **name**: Skorohod-Olevsky Viscous Sintering (SOVS), linear-viscous form
    - **formulation**: eps_dot^in_ij = s_ij/(2*eta0(T)*phi(rho)) + (sigma_kk - 3*sigma_s(rho))/(18*eta0(T)*psi(rho))*delta_ij
s_ij = sigma_ij - (1/3)*sigma_kk*delta_ij
phi(rho) = a1*rho^b1 ;  psi(rho) = a2*rho^b2/(1-rho)^c2
sigma_s(rho) = sigma_s0*a3*rho^b3 ;  sigma_s0 = 3*alpha/r0
eta0(T) = a4*(T/T0)^2 + b4*(T/T0) + c4   OR   A0*T*exp(Q/RT)   OR   A*T^n*exp(B/T)
rho_dot = -rho*tr(eps_dot^in)  ->  rho|_{t+dt} = rho|_t * exp(-tr(delta_eps^in))
Skorohod closure (theta = 1-rho):  phi = (1-theta)^2 ,  psi = (2/3)*(1-theta)^3/theta ,  P_L = (3*alpha/r0)*(1-theta)^2
Effective moduli:  G_eff = eta0*phi ,  K_eff = 2*eta0*psi
Free-sintering limit:  dtheta/dt = -(1-theta)*P_L/(2*eta0*psi) = -9*alpha*theta/(4*r*eta0)
Total strain:  eps^tot = eps^el + eps^in (+ eps^th + eps^mass) ; sigma = lambda*tr(eps^el)*I + 2*mu*eps^el
    - **when_to_use**: Default choice for a first predictive model of the copper slurry: it is the only continuum law with (a) a fully documented Sandia verification suite, (b) an open-source MFront/Code_Aster implementation with consistent tangent, (c) an analytic free-sintering solution to verify your own UMAT against, and (d) a published inverse-calibration recipe from dilatometry alone for the bulk branch. Valid while creep is Newtonian (stress exponent ~1) - check this for Cu with a sinter-forging or CLD stress sweep before committing.
    - **inputs_needed**: alpha (surface energy of Cu, temperature-dependent), r0 or G(t) (particle/grain radius), eta0(T) (skeleton shear viscosity), the six psi/phi/sigma_s exponents, rho0 (green relative density field - from micro-CT of the printed green part), E(T) and nu(T) for the elastic branch, CTE(T), and a mass-loss strain rate eps_dot^mass from TGA if debinding overlaps the sintering ramp.
    - **limitations**: No grain growth, no microstructure evolution, no anisotropy, no entrapped-gas back-pressure, no phase change. Assumes linear viscosity. Cannot be integrated by standard return-mapping (direction AND magnitude of inelastic rate both depend on stress). The legacy McHugh-Riedel semi-implicit scheme needs very fine meshes to resolve warpage; use a fully implicit Newton-Raphson scheme instead. Free dilatometry cannot identify phi.
    - **source**: Olevsky, Mater. Sci. Eng. R 23 (1998) 41-100, DOI 10.1016/S0927-796X(98)00009-6 ; B. Lester, SAND2017-12933R, DOI 10.2172/1411315 ; Arguello, Reiterer & Ewsuk, J. Am. Ceram. Soc. 92 (2009) 1442-1449, DOI 10.1111/j.1551-2916.2009.03008.x ; MFront implementation https://thelfer.github.io/tfel/web/sovs.html
  -
    - **name**: Enhanced SOVS with microstructure factor lambda(rho)
    - **formulation**: eps_dot^in_ij = s_ij/(2*eta0*phi) + (sigma_kk - 3*sigma_s)/(18*eta0*psi*lambda(rho))*delta_ij
lambda(rho) = (a5/(rho_c - rho))^b5     [ratio of grain volume at rho to initial grain volume; rho_c = max attainable relative density]
rho_dot = rho*tr(eps_dot^mass - eps_dot^in - 3*eps_dot^th)
Inverse calibration:  eta0(T) = -3*sigma_s(rho)/(18*eps_dot^in(t)*psi(rho)*lambda(rho))
with eps_dot^in(t) = eps_dot^dil(t) - 3*eps_dot^th(t) from the dilatometer trace
    - **when_to_use**: When free-sintering dilatometry gives a physically impossible multi-valued eta0(T) (different values on heating, dwell and cooling at the same temperature). lambda absorbs grain growth, a finite achievable density, and reaction/mass-loss effects. Directly relevant to the copper case because debinding mass loss overlaps the early sintering ramp.
    - **inputs_needed**: Dilatometry at multiple green densities and multiple peak temperatures/dwells (18 runs used in the source study), TGA for eps^mass, and a separate thermal-expansion calibration on both heating and cooling.
    - **limitations**: lambda is phenomenological, not a grain-size model - it does not give you grain size as an output. rho_c must be re-fitted for every green density class (four classes were needed in the source study). Still isotropic.
    - **source**: 'Enhanced Skorohod-Olevsky viscous model incorporating microstructure evolution for finite element analysis of ceramic sintering', J. Eur. Ceram. Soc. 44 (2024) 7730-7739, DOI 10.1016/j.jeurceramsoc.2024.05.035
  -
    - **name**: Riedel-Svoboda-Zipse / Kraft-Riedel solid-state sintering model (Bordia-Scherer variables)
    - **formulation**: eps_dot_I = eps_dot^s_I + (1/E_vis)*[sigma_I - nu_vis*(3*sigma_m - sigma_I)]   , I = 1,2,3 principal
sigma^s_I = E_vis * eps_dot^s_I                       [intrinsic sintering stress]
rho_dot = -rho*(eps_dot_1 + eps_dot_2 + eps_dot_3)
d_dot = (gamma_b*M_b/(2d)) * (F_d/F_p)                [modified Hillert; M_b Arrhenius; F_p = pore/Zener drag; F_d = non-steady-state size distribution correction]
Elastic-viscous analogy mapping to SOVS:  G_eff = E_vis/(2*(1+nu_vis)) ,  K_eff = E_vis/(3*(1-2*nu_vis))
    - **when_to_use**: When you want mechanism-based (grain-boundary-diffusion) rather than fitted porosity functions, and when grain growth with pore drag must be an explicit output. This is the lineage behind commercial sintering modules (Fraunhofer IWM / Simufact). Preferable if you intend to publish a physically interpretable Q for copper rather than a lumped apparent Q.
    - **inputs_needed**: delta*D_b(T) (grain-boundary diffusivity x boundary width) for Cu, gamma_s and gamma_b for Cu, grain-boundary mobility M_b(T), initial particle size distribution, and pore-size statistics for F_p. For Cu, D_b and gamma are strongly atmosphere/oxygen-activity dependent - this is the weak link.
    - **limitations**: Isotropic. Cannot reproduce sinter-forging at zero radial shrinkage nor constrained-film densification (proven failure). Requires diffusion data that for Cu under H2/N2/vacuum with residual C and O is poorly constrained. Assumes equilibrium pore surfaces.
    - **source**: Riedel, Zipse & Svoboda, Acta Metall. Mater. 42 (1994) 445-452, DOI 10.1016/0956-7151(94)90499-5 (and Part I, 435-443, DOI 10.1016/0956-7151(94)90498-7) ; Kraft & Riedel, J. Eur. Ceram. Soc. 24 (2004) 345-361, DOI 10.1016/S0955-2219(03)00222-X ; Eqs. as summarised in arXiv:2211.00821 Eqs. 25-28
  -
    - **name**: Abouaf power-law visco-plastic model (metals; non-Newtonian creep)
    - **formulation**: eps_dot^vp = A(T)*sigma_eqv^(N(T)-1) * [ (3/2)*c(rho)*s + f(rho)*I1*I ]
sigma_eqv(rho) = ( 3*c(rho)*J2 + f(rho)*I1^2 )^(1/2) ,  J2 = (1/2)*s:s ,  I1 = tr(sigma)
rho = rho0 * exp(-eps^vp_vol)
Abaqus CREEP decomposition:
  delta_eps^vp = (1/3)*delta_eps_sw*I + delta_eps_cr*n ,  n = d(sigma_eq)/d(sigma)  [von Mises]
  delta_eps_sw = [ 3*f(rho)*I1*A(T)*sigma_eqv^(N-1) ] * delta_t
  delta_eps_cr = [ c(rho)*sigma_eq*A(T)*sigma_eqv^(N-1) ] * delta_t
  rho carried as a field variable via USDFLD
Sintering is included by replacing I1 with (I1 + 3*sigma_s) so the capillary stress acts as an internal hydrostatic pressure.
    - **when_to_use**: Strongly recommended as the SECOND model for copper. Cu deforms by power-law creep with stress exponent typically n = 3-8, not n = 1; a linear-viscous SOVS will misrepresent gravity sag and setter-friction drag even if it fits the free-shrinkage curve perfectly. Also the natural framework if you ever go to pressure-assisted sintering / HIP.
    - **inputs_needed**: A(T) and N(T) from isothermal uniaxial compression of FULLY DENSE Cu at the sintering temperatures; f(rho) from hydrostatic densification (interrupted runs or free sintering with known sigma_s); c(rho) from uniaxial compression of PARTIALLY dense compacts. Plus CTE(rho,T).
    - **limitations**: Requires mechanical testing of partially sintered compacts, which are fragile and geometry-sensitive. c and f are still phenomenological. The classic calibration needs multiple strain rates (expensive); the modified single-strain-rate + 0.2% offset approach reduces cost but is only validated where sigma_0.2 ~ sigma_ss (T >= 800 C).
    - **source**: Abouaf et al., Int. J. Numer. Methods Eng. 25 (1988) 191-212, DOI 10.1002/nme.1620250116 ; modern calibration and Abaqus implementation: arXiv:2506.11946 (Powder Technology, DOI 10.1016/j.powtec.2025.121526), Eqs. 7-11, 14-21
  -
    - **name**: Three-step Abouaf calibration (resolves the deviatoric/hydrostatic identifiability problem)
    - **formulation**: Step 1 - fully dense, set c=1, f=0:  eps_dot^vp = (3/2)*A(T)*sigma_eqv^(N-1)*s , sigma_eqv = (3*J2)^(1/2) = |sigma_1|
           -> fit A(T), N(T) by minimising error on the 0.2% offset stress in uniaxial compression
Step 2 - hydrostatic densification (HIP or free sintering with known capillary pressure):
           f(rho) = [ rho_dot / ( rho * A(T) * I1^N(T) ) ] ^ ( 2/(N(T)+1) )
Step 3 - uniaxial at partial density:
           c(rho) = [ eps_dot_1 / ( A(T) * sigma_1^N(T) ) ] ^ ( 2/(N(T)-1) )  -  f(rho)
    - **when_to_use**: Whenever you use an Abouaf/Cocks-type law. Each step isolates exactly one unknown, so the identification is well-posed - unlike the common practice of throwing all parameters into one global optimiser against free-shrinkage data only.
    - **inputs_needed**: Dense Cu compression at 3-5 temperatures spanning 800-1075 C; interrupted sintering density measurements (Archimedes + geometric); partially-dense compression specimens at 3-4 relative densities.
    - **limitations**: Step 3 is singular at N=1 (the linear-viscous limit) - use the SOVS route instead if Cu turns out Newtonian. Partially dense Cu specimens oxidise rapidly during handling; tests must be under controlled atmosphere.
    - **source**: arXiv:2506.11946, Eqs. 14-21, https://arxiv.org/pdf/2506.11946
  -
    - **name**: Master Sintering Curve (Su & Johnson) and Park's grain-size-corrected extension
    - **formulation**: Combined-stage sintering model:
  -(1/L)*dL/dt = (1/(3*rho))*drho/dt = (gamma*Omega/(k_B*T)) * [ Gamma_b*delta*D_b/G^4 + Gamma_v*D_v/G^3 ]
Separate process from microstructure and integrate:
  Theta(t, T(t)) = integral_0^t (1/T) * exp(-Q/(R*T)) dt
  Phi(rho) = integral_rho0^rho [ (G(rho))^n / (3*rho*f(rho)) ] drho    (density-side grouping)
  Theta(t,T) = ( k_B / (gamma*Omega*D0) ) * Phi(rho)
Sigmoid fit for prediction:  rho = rho0 + a / [ 1 + exp( -(log(Theta) - log(Theta0))/b ) ]^c
Q determination: minimise the mean square residual of the rho-vs-log(Theta) collapse over >=3 heating rates, scanning Q.
Park extension for dissimilar grain-growth trajectories:
  Theta = integral_0^t (G0/G)^w * (1/T) * exp(-Q/(R*T)) dt ,  w = 4 (gb diffusion), w = 3 (lattice diffusion)
    - **when_to_use**: First analysis you run on the copper dilatometry data. Gives (a) an apparent Q, (b) a heating-path-independent densification predictor you can use to DESIGN candidate cycles analytically before any FEM, and (c) an objective test of whether a single mechanism dominates (if the collapse is poor or Q drifts with density, it does not). Use Park's form if you measure grain size on interrupted samples.
    - **inputs_needed**: Dilatometry (or interrupted density) at >=3 constant heating rates, ideally spanning a factor of 5-10 in rate; green density; Archimedes final density to anchor the dilatometry-derived density. For Park: grain size vs time from interrupted runs.
    - **limitations**: Assumes a single dominant diffusion mechanism with one Q, and that G and Gamma depend only on rho (not on thermal path) - both violated when grain growth trajectories differ between heating rates, when a liquid or oxide phase forms, or when pore-gas pressure matters. Q from MSC is an APPARENT value that depends on the fitting function chosen. Stage-resolved analysis often shows Q rising sharply in the final stage (400 -> 700 kJ/mol on MgAl2O4).
    - **source**: Su & Johnson, J. Am. Ceram. Soc. 79 (1996) 3211-3217, DOI 10.1111/j.1151-2916.1996.tb08097.x ; DiAntonio & Ewsuk, SAND2010-2158P, https://www.osti.gov/servlets/purl/1728557 ; Park extension via J. Eur. Ceram. Soc. 41 (2021) 1048-1051, DOI 10.1016/j.jeurceramsoc.2020.09.003 ; critique: McCoy et al., J. Eur. Ceram. Soc. 38 (2018) 1030-1037, DOI 10.1016/j.jeurceramsoc.2017.12.025
  -
    - **name**: Wang-Raj kinetic field method (independent Q estimator)
    - **formulation**: General sintering rate equation:  (1/rho)*drho/dt = ( K * gamma * Omega ) / ( G^n * R * T ) * f(rho) * exp(-Q/(R*T))
Taking logs at constant density:
  ln[ T * (1/rho)*(drho/dt) ] = -Q/(R*T) + ln[f(rho)] + ln(K) - n*ln(G)
Plot ln[T*(drho/dt)/rho] vs 1/T along iso-density lines across heating rates; slope m gives Q = -m*R.
    - **when_to_use**: Always run alongside the MSC. Agreement of the two (e.g. 350 vs 357 kJ/mol) validates the single-mechanism assumption; disagreement is a red flag that the model form is wrong. Also gives Q as a FUNCTION of density, which immediately reveals a mechanism change (e.g. oxide reduction completing, or Cu surface diffusion giving way to grain-boundary diffusion).
    - **inputs_needed**: Same dilatometry dataset as the MSC (>=3 heating rates); no extra experiments.
    - **limitations**: Requires numerical differentiation of the density curve (noisy - smooth with a low-order spline, not a moving average, to avoid biasing the slope). Assumes grain size depends only on density.
    - **source**: Wang & Raj, J. Am. Ceram. Soc. 73 (1990) 1172-1175, DOI 10.1111/j.1151-2916.1990.tb05175.x ; formulation as given in DiAntonio & Ewsuk SAND2010-2158P Eqs. 8-10; applied in arXiv:2512.02591 Section 3.2
  -
    - **name**: Staged identification protocol for an AM part (MSC/WR -> psi -> anisotropy -> shear)
    - **formulation**: Step 1: Dilatometry at 2, 5, 10 K/min (and directionally: radial and axial on the same pellet). MSC + Wang-Raj -> Q.
Step 2: Linearised regression for the bulk branch:
   Y = ln[ -3*(1-theta)^3 / ( T * theta_dot * psi ) ] = ln( r*eta0'/alpha ) + Q/(R*T)
   Scan the psi exponents (gamma, zeta in psi = (2/3)*(theta_ci - theta)^gamma/(theta - theta_cf)^zeta) and pick the pair that (a) reproduces the independently measured Wang-Raj Q and (b) maximises R^2.
Step 3: Analytic forward check:  theta_{t+1} = theta_t + dt * [ -3*(1-theta)^3 / ( (r*eta0'/alpha)*T*exp(Q/RT) * psi ) ]
Step 4: FEM of the dilatometry pellet; tune anisotropic sintering stresses (P_lR, P_lZ) until simulated radial and axial shrinkage match the measured directional curves.
Step 5: Sinter a dedicated shear artefact (thin ring on its side, or a horizontal overhanging bar). Adjust G = eta*beta*(1-theta)^chi until the simulated H/R or tip deflection matches.
Step 6: Validate on an independent geometry not used in any fit.
    - **when_to_use**: This is the recommended end-to-end recipe for the copper slurry. It is the only published protocol that (i) removes the Q/psi degeneracy using a second, independent Q estimator, (ii) handles LCM layer anisotropy without a full anisotropic constitutive law, and (iii) fixes the shear branch with a cheap printed artefact instead of a sinter-forging rig.
    - **inputs_needed**: Anisotropic dilatometry (radial + axial on the same specimen), TGA, mean particle radius, an estimate of Cu surface energy alpha, a printed thin ring and a printed overhanging bar, and an FEM code that can do large-deformation viscous flow with gravity and contact (COMSOL, Abaqus, Code_Aster).
    - **limitations**: Steps 4-5 are sequential, not simultaneous, so parameter cross-correlation is not quantified - no confidence intervals come out. The anisotropy is baked into the sintering stress rather than the moduli, so it will not extrapolate to strongly constrained configurations (setters, co-sintering).
    - **source**: 'Finite Element Prediction of Sintering Deformation in 3D-Printed Porcelain Filament', arXiv:2512.02591, Figure 1 and Sections 2.5, 3.2-3.5, https://arxiv.org/pdf/2512.02591
  -
    - **name**: Cyclic Loading Dilatometry (CLD) and sinter-forging - separating bulk from shear
    - **formulation**: Sinter-forging (uniaxial load sigma_z superposed on free sintering, axial and radial strain both recorded):
   eps_dot_z - eps_dot_r = sigma_z / (3*G_eff)          -> gives the SHEAR branch directly
   eps_dot_z + 2*eps_dot_r = (sigma_z - 3*sigma_s)/(3*K_eff)  -> gives the BULK branch and sigma_s
   Equivalently:  E_p = sigma_z / (eps_dot_z - eps_dot_z^free)  and  nu_p = -eps_dot_r^load/eps_dot_z^load
CLD: superpose small load cycles (load on/off) during a constant-heating-rate run; the jump in strain rate on load application at fixed density and temperature gives the uniaxial viscosity E_p without interrupting the run; adding radial strain measurement gives nu_p, and extrapolating the load-strain-rate line to zero strain rate gives the sintering stress sigma_s.
Conversion:  G_eff = E_p/(2*(1+nu_p)) ,  K_eff = E_p/(3*(1-2*nu_p))
    - **when_to_use**: The rigorous answer to the identifiability problem, and the route to take if you want a publishable, fully determined constitutive law for copper rather than a fitted one. CLD is the cheapest rigorous option: one specimen, one run, all of E_p, nu_p and sigma_s as functions of T and rho.
    - **inputs_needed**: A dilatometer capable of applying and removing a controlled uniaxial load during the run (or a sinter-forging rig), plus radial strain measurement (laser/optical dilatometry or interrupted geometry) to get nu_p. Controlled atmosphere essential for Cu.
    - **limitations**: Load must be small enough not to perturb the microstructure but large enough to give a resolvable strain-rate jump - a narrow window for a soft, near-molten Cu skeleton at 1000 C. Radial strain measurement is the practical bottleneck. Only isotropic E_p and nu_p come out; an anisotropic green body needs the transversely isotropic extension (5 parameters + 2 free densification rates).
    - **source**: Cai/Bordia, J. Am. Ceram. Soc. 80 (1997) 445-452, DOI 10.1111/j.1151-2916.1997.tb02850.x ; Mohanram et al., J. Am. Ceram. Soc. 87 (2004) 192-196, DOI 10.1111/j.1551-2916.2004.00192.x ; discontinuous hot forging summarised in arXiv:2211.00821 (paragraph after Eq. 28); conversion is the standard elastic-viscous analogy of Bordia & Scherer, Acta Metall. 36 (1988) 2393-2397, DOI 10.1016/0001-6160(88)90189-7 (formula not directly verified against that paper in this session)
  -
    - **name**: Anisotropic / transversely isotropic constitutive laws for layered green bodies
    - **formulation**: Two established routes:
(a) Anisotropic SINTERING STRESS, isotropic moduli (cheap, numerically stable):
    sigma = 2*eta(T)*[ phi(theta)*eps_dot + (psi(theta) - (1/3)*phi(theta))*e_dot*I ] + P_l
    with P_l = diag(P_lR, P_lR, P_lZ) fitted to directional dilatometry. Justified by the fact that elongated/elliptical pores generate a deviatoric sintering stress.
(b) Fully anisotropic constitutive law: transversely isotropic viscous formulation requiring 5 constitutive parameters plus 2 free densification rates; or an anisotropic law parameterised by the SINTERING STRAINS rather than relative density, which degenerates to the isotropic law under free sintering.
    - **when_to_use**: (a) for the first LCM copper model - the layer-wise DLP structure will give anisotropic shrinkage (4-5% direction-to-direction differences are reported in binder jetting). (b) only if you need to predict CONSTRAINED sintering (on a setter with friction, co-sintered multimaterial, or films), where isotropic laws are proven to fail.
    - **inputs_needed**: (a) Directional dilatometry (radial and axial on the same specimen) at several heating rates. (b) Additionally, constrained-film densification or sinter-forging at zero lateral shrinkage.
    - **limitations**: (a) is a fit, not a theory: P_lR/P_lZ will not transfer to a different print orientation, layer thickness or exposure setting without re-fitting. (b) needs experiments most labs cannot run, and 5 parameters is a serious identification burden.
    - **source**: (a) arXiv:2512.02591 Section 3.4 ; (b) Bordia, Zuo, Guillon, Salamone & Rodel, Acta Mater. 54 (2006) 111-118, DOI 10.1016/j.actamat.2005.08.025 ; Li, Pan, Guillon & Cocks, Acta Mater. 58 (2010) 5980-5988, DOI 10.1016/j.actamat.2010.07.015 ; Wakai & Shinoda on anisotropic sintering stress (cited as ref [209] in arXiv:2211.00821)
  -
    - **name**: Grain growth laws coupled to densification (porosity/Zener drag)
    - **formulation**: Olevsky porosity-corrected form (used with SOVS for 316L):
   dG/dt = ( k0 / (3*G^2) ) * ( (1 - rho_c) / (2 - rho_c - rho) )^(3/2) * exp( -Q_G/(R*T) )
Alternative porosity-function form (spinel):
   G_dot = ( K(T) / G^p ) * ( theta_c / (theta + theta_c) )^n
Hillert/Riedel with explicit pore drag:
   d_dot = ( gamma_b * M_b / (2*d) ) * ( F_d / F_p )   ,  M_b = M_b0*exp(-Q_m/RT)
Classical Zener pinning limit:  G_lim ~ (4/3) * r_pore / f_v
Coupling back into the model: sigma_s = 3*alpha*(1-theta)^2 / (G/2)  - i.e. grain growth DECREASES the sintering driving force, which is the physical origin of the final-stage densification stall.
    - **when_to_use**: Mandatory for copper: Cu grain growth is fast and the final-stage stall vs grain coarsening trade-off is exactly what a two-step or rate-controlled cycle is designed to exploit. Needed if you want the model to inform grain-size (and hence conductivity/strength) targets, not just dimensions.
    - **inputs_needed**: Interrupted sintering runs (>= 8-12 T/t combinations) with quantitative metallography: LOM linear intercept calibrated against EBSD (a scaling factor kG ~ 1.4-1.5), plus pore size and volume fraction for the Zener term.
    - **limitations**: rho_c (or theta_c) is a fitted lumped parameter for the pore-pinning effect without a first-principles value. Assumes normal grain growth - abnormal grain growth in Cu (common with oxide inclusions or residual C) is not captured. Calibrating from LOM alone underestimates grain size by ~40%.
    - **source**: Cabo Rios et al., Acta Mater. 249 (2023) 118822, Eq. 18 and Section 4.2, DOI 10.1016/j.actamat.2023.118822 ; Olevsky grain-growth form as used in J. Eur. Ceram. Soc. 41 (2021) 1048-1051 Eq. 3 ; Hillert/pore-drag form via arXiv:2211.00821 Eq. 28 ; Zener limit expression is standard textbook - unverified in this session
  -
    - **name**: Numerical integration of SOVS: fully implicit scheme (recommended over McHugh-Riedel)
    - **formulation**: Hypoelastic update:  sigma^{n+1} = sigma^n + C:(d_eps - d_eps^in) ,  d_eps^in = (1-beta)*eps_dot^in,n*dt + beta*eps_dot^in,n+1*dt
Residuals:  r^eps_ij = -d_eps^in_ij + (1-beta)*eps_dot^in,n_ij*dt + beta*eps_dot^in,n+1_ij*dt
            r^rho    = -d_rho + (1-beta)*rho_dot^n*dt + beta*rho_dot^{n+1}*dt
Newton system:
  -r^eps_ij = L^-1_ijkl * d_sigma_kl + beta*dt*(d eps_dot^in_ij/d rho)*d_rho
  -r^rho    = beta*dt*(d rho_dot/d sigma_ij)*d_sigma_ij + (-1 + beta*dt*(d rho_dot/d rho))*d_rho
  with L^-1_ijkl = S_ijkl + beta*dt*(d eps_dot^in_ij / d sigma_kl)
Merit function:  m = 0.5*[ (r^rho/rho0)^2 + (E/sigma_s0)^2 * r^eps_ij*r^eps_ij ] ; converge on sqrt(m)
Initialisation ('inelastic predictor - elastic corrector'): sigma^(0)=sigma^n, d_eps^in,(0)=d_eps, rho^(0)=rho^n
    - **when_to_use**: If you write your own UMAT/UEL. The published complaint that SOVS needs 'fairly fine meshes' and 'massively parallel computing' to capture warpage traces to the legacy semi-implicit scheme, not to the physics.
    - **inputs_needed**: Analytic derivatives of eps_dot^in and rho_dot with respect to sigma, rho and T (all available in closed form for the power-law phi/psi/sigma_s).
    - **limitations**: Standard elastic-predictor initialisation fails because substantial inelastic deformation occurs at zero load; line-search or trust-region globalisation may still be needed. beta must be chosen (beta = 1 fully implicit).
    - **source**: B. Lester, SAND2017-12933R, Eqs. 6-29, DOI 10.2172/1411315, https://www.osti.gov/servlets/purl/1411315/
  -
    - **name**: Shrinkage compensation as an inverse problem
    - **formulation**: Forward map:  x_sint = F(x_green ; theta_params, cycle, BCs)
Fixed-point (reverse) compensation:
  x_green^{k+1} = x_green^k - lambda * ( F(x_green^k) - x_CAD )   ,  lambda in (0,1]
  iterate until max| F(x_green^k) - x_CAD | < tol (user-set 'acceptable distortion') or k = k_max
First-order isotropic starting guess:  x_green^0 = x_CAD / (rho0/rho_f)^(1/3)   [uniform scaling from the density ratio]
Output exported directly as the pre-deformed STL for printing.
    - **when_to_use**: The deliverable step. Note that for LCM the compensation must be applied to the SLICED geometry, and the isotropic uniform-scale starting guess is only the zeroth order - gravity sag, setter friction and layer anisotropy are what the iteration actually fixes.
    - **inputs_needed**: A converged forward model, the nominal CAD, a tolerance spec, and a robust mesh morphing / surface-projection operator (self-intersection of the compensated geometry is a documented failure mode).
    - **limitations**: The map F is not guaranteed contractive - reported failure cases include self-intersecting compensated geometries. Compensation is only as good as the forward model: a model that fits free shrinkage but has the wrong shear viscosity will compensate the bulk correctly and the sag incorrectly. Published success rate with default material data: 3 of 5 geometries.
    - **source**: Chalmers MSc thesis on Simufact Additive, https://odr.chalmers.se/items/78d530b0-ce82-431d-9e9c-6e67d097cec7 ; 'Modelling of geometrical deformation and compensation during sintering of binder jetting', Virtual and Physical Prototyping (2024), DOI 10.1080/17452759.2024.2443958
  -
    - **name**: Two-step sintering (Chen & Wang) and rate-controlled sintering as cycle strategies
    - **formulation**: TSS: ramp fast to T1, hold briefly (or zero dwell) to reach a critical relative density rho* at which pores become subcritical/unstable, cool rapidly to T2 (typically T1 - T2 < 150 C), hold long at T2.
Mechanism: kinetic window between grain-boundary DIFFUSION (active at T2, Q_gb,diff) and grain-boundary MIGRATION (frozen at T2 by triple-junction drag, Q_TJ > Q_gb,diff).
RCS: instead of prescribing T(t), prescribe the densification rate drho/dt (or shrinkage rate) and let a controller solve for T(t). Implementation with a continuum model: invert the free-sintering law, e.g. for SOVS/Skorohod
   eta0(T_required) = -9*alpha*theta / (4*r*(dtheta/dt)_target)
   -> T_required(t) from the calibrated eta0(T).
The MSC gives the same thing globally: choose any T(t) path that traces the required Theta(t) trajectory.
    - **when_to_use**: Both are directly actionable for copper once the MSC/SOVS model is calibrated. RCS is the natural way to keep the densification rate below the level at which trapped gas (CO, CO2, H2O from residual binder carbon and copper oxide reduction) causes blistering - a specific copper risk. TSS is the way to hit high density without the grain coarsening that would degrade conductivity.
    - **inputs_needed**: A calibrated MSC (to choose the T1 hold that reaches rho*) plus a grain-growth law (to verify grain size is actually frozen at T2). A furnace with closed-loop shrinkage feedback for true RCS; otherwise approximate RCS with a piecewise ramp solved offline from the model.
    - **limitations**: TSS is documented on oxide ceramics; the triple-junction-drag mechanism has NOT been demonstrated for FCC copper, where boundary mobility is far higher. rho* is material-specific and must be found experimentally. RCS by open-loop pre-computation is only as accurate as the model.
    - **source**: Chen & Wang, Nature 404 (2000) 168-171, DOI 10.1038/35004548 ; survey table in IntechOpen chapter 67294, https://www.intechopen.com/chapters/67294 ; rate-controlled sintering: Palmour & Johnson, 'Rate Controlled Sintering Revisited', in Sintering'85, DOI 10.1007/978-1-4613-2851-3_2
- **open_questions**:
  - Is copper's sintering creep Newtonian (stress exponent N=1, so SOVS applies) or power-law (N=3-8, so Abouaf applies) in the 900-1075 C window at 60-95% relative density? This single measurement (a stress sweep in sinter-forging or CLD) decides the entire constitutive architecture and no published answer was found.
  - What is the temperature- and atmosphere-dependent surface energy alpha of copper in H2/N2, in vacuum, and in a reducing atmosphere with residual carbon? sigma_s0 = 3*alpha/r0 scales the entire densification rate linearly, yet no sourced value was obtained in this session. Does surface oxide change alpha enough to matter?
  - Do the LCM layer interfaces produce an anisotropic sintering stress (P_lR != P_lZ) large enough to require directional calibration, and how does it scale with layer thickness (25/50/100 um) and exposure dose? Binder jetting shows 0.2-1 percentage point shrinkage anisotropy; DLP with 30 um pixels and a photopolymer network may be worse or better.
  - Is the green density field from a CeraFab 2M30 print uniform enough to treat rho0 as a scalar, or must it be mapped (micro-CT) and imported as an initial field? Simufact-type studies showed initial green density was the single most influential input, and local density variation drives warpage more strongly than the cycle does.
  - How should entrapped gas pressure from residual binder carbon and copper oxide reduction (CO, CO2, H2O) be added to the continuum sintering stress? sigma_s_eff = sigma_s - p_gas(theta, T) is the obvious form, but no validated p_gas closure for closed-pore copper was found. This determines the maximum attainable density and the blistering threshold.
  - Does the Chen & Wang triple-junction-drag mechanism (and hence two-step sintering) work at all for FCC copper, where grain-boundary mobility is orders of magnitude higher than in oxides? All published TSS successes are oxides.
  - Is a single apparent activation energy valid for copper across 60-95% relative density, or does Q jump in the final stage as it does for MgAl2O4 (400 -> 700 kJ/mol)? If it jumps, a single-Q MSC will systematically misplace the final-stage densification.
  - Can the shear branch (phi, or E_p and nu_p) be identified for copper from a printed slump artefact alone (the porcelain route, beta = 8.7), or is a sinter-forging / CLD rig unavoidable given copper's very low skeleton viscosity near T_m? Copper may simply collapse before a usable H/R can be measured.
  - How do the SOVS/Abouaf parameters change with the debinding endpoint (residual carbon and oxygen content)? Because binder content is proprietary and unknown, the practical question is whether one calibration covers the whole debinding parameter space or whether rho0 and eta0 must be re-identified per debinding recipe.
  - Does the normalized bulk viscosity for an LCM copper green body follow Skorohod (theoretical), Hsueh (two-parameter power law, exponent A ~ 11 for binder jet 316L vs Skorohod's 3), or the Abouaf critical-porosity form? The choice changes the fitted skeleton viscosity by >1 order of magnitude and hence the entire distortion prediction, even when all three fit the shrinkage curve.
  - Is the elastic branch worth carrying at all? Most authors argue elastic strain during sintering is negligible (Bordia & Scherer), but residual stress at cooldown - the thing that cracks copper parts on the setter - lives entirely in that branch plus CTE mismatch with the setter. What CTE(rho, T) should be used for partially dense copper?
  - What setter/part friction coefficient is appropriate for copper on alumina, zirconia or graphite setters under reducing atmosphere? Simufact's default of 0.3 is unjustified for this pair, and frictional drag is a first-order source of base distortion at 20%+ linear shrinkage.
  - Does the Master Sintering Curve remain valid when the heating path crosses the oxide-reduction temperature at different points for different heating rates? The MSC assumes path independence; a chemical reaction whose completion depends on rate breaks that assumption.
  - What is the right grain-growth critical-density parameter rho_c for copper, and does abnormal grain growth (from residual oxide or carbon inclusions) invalidate the normal-growth kinetic law? rho_c ~ 0.948-0.96 in the steel/porcelain literature, but no copper value was found.
- **references**:
  -
    - **citation**: B. T. Lester, 'Verification of the Skorohod-Olevsky Viscous Sintering (SOVS) Model', SAND2017-12933R, Sandia National Laboratories, 16 November 2017. DOI 10.2172/1411315
    - **url**: https://www.osti.gov/servlets/purl/1411315/
    - **why**: THE single most useful document for implementation. Gives the SOVS equations verbatim, the ZnO parameter table, the analytic free-sintering and sinter-forge verification solutions (Eqs. 30-32), and both the legacy McHugh-Riedel semi-implicit and a new fully implicit Newton-Raphson integration scheme with the merit function. Use its verification cases as unit tests for your own UMAT.
  -
    - **citation**: E. A. Olevsky, 'Theory of sintering: from discrete to continuum', Materials Science and Engineering R: Reports 23(2) (1998) 41-100. DOI 10.1016/S0927-796X(98)00009-6
    - **url**: https://doi.org/10.1016/s0927-796x(98)00009-6
    - **why**: The foundational continuum theory paper. Source of the phi, psi, P_L closures and of the anisotropic-sintering-stress argument for elliptical pores. Paywalled; obtain via library.
  -
    - **citation**: J. G. Arguello, M. W. Reiterer, K. G. Ewsuk, 'Verification, Performance, Validation, and Modifications to the SOVS Continuum Constitutive Model in a Nonlinear Large-Deformation Finite Element Code', J. Am. Ceram. Soc. 92(7) (2009) 1442-1449. DOI 10.1111/j.1551-2916.2009.03008.x
    - **url**: https://doi.org/10.1111/j.1551-2916.2009.03008.x
    - **why**: The reference V&V study (bilayer bar problem, mesh convergence, ZnO parameter set). Read together with SAND2017-12933R, which revisits and improves on it.
  -
    - **citation**: T. Helfer & J. Balaguer, 'Skorohod-Olevsky Viscous Sintering (SOVS) model', TFEL/MFront documentation, 2019
    - **url**: https://thelfer.github.io/tfel/web/sovs.html
    - **why**: Working open-source implementation of SOVS as an MFront behaviour with the StandardElasticity brick, implicit integration and automatic consistent tangent. Usable from Code_Aster, Abaqus (via mfront-abaqus interface), CalculiX and others. Fastest route to a running model - the clone-and-modify starting point.
  -
    - **citation**: A. Cabo Rios, E. Hryha, E. Olevsky, P. Harlin, 'Analytical models for initial and intermediate stages of sintering of additively manufactured stainless steel', Acta Materialia 249 (2023) 118822. DOI 10.1016/j.actamat.2023.118822
    - **url**: https://research.chalmers.se/publication/535046/file/535046_Fulltext.pdf
    - **why**: Open access. The best published CALIBRATION methodology paper for an AM green body: derives the porosity-evolution ODE, compares Skorohod vs Hsueh vs Abouaf bulk viscosity forms, gives the full non-linear regression protocol with stability analysis, and reports all fitted parameters plus the grain-growth law. Directly transferable to the copper case - copy the experimental design (4 temperatures x 4 dwell times).
  -
    - **citation**: 'Finite Element Prediction of Sintering Deformation in 3D-Printed Porcelain Filament', arXiv:2512.02591 (2025)
    - **url**: https://arxiv.org/pdf/2512.02591
    - **why**: The closest published analogue to what you want to do: AM ceramic, anisotropic dilatometry, MSC + Wang-Raj cross-check for Q, regression identification of the bulk modulus exponents, FEM back-fit of anisotropic sintering stress, and shear viscosity from a printed slump artefact. Figure 1 is a ready-made workflow diagram for your paper.
  -
    - **citation**: 'Enhanced Skorohod-Olevsky viscous model incorporating microstructure evolution for finite element analysis of ceramic sintering', Journal of the European Ceramic Society 44 (2024) 7730-7739. DOI 10.1016/j.jeurceramsoc.2024.05.035
    - **url**: https://biblio.ugent.be/publication/01HY0QQH7QJ4V4WS6WF8N0HSQZ/file/01HYB4TDD0PE7V7ZFJW5HR8ES4.pdf
    - **why**: Open access. Gives the direct pointwise inversion of dilatometry for eta0(T), the heating/dwell/cooling hysteresis diagnostic, the lambda(rho) microstructure factor, and the mass-loss-corrected density evolution (Eq. 5) - the last is directly relevant because your debinding mass loss will overlap the sintering ramp.
  -
    - **citation**: 'A visco-plastic constitutive model for accurate densification and shape predictions in powder metallurgy hot isostatic pressing', arXiv:2506.11946 (Powder Technology, DOI 10.1016/j.powtec.2025.121526)
    - **url**: https://arxiv.org/pdf/2506.11946
    - **why**: Open access. Complete Abouaf model with the Abaqus CREEP + USDFLD implementation (Eqs. 9-12) and the three-step calibration that cleanly separates A(T), N(T), f(rho) and c(rho) (Eqs. 14-21). Use this if copper turns out non-Newtonian.
  -
    - **citation**: C. B. DiAntonio & K. G. Ewsuk, 'Master Sintering Curve and Its Application in Sintering of Electronic Ceramics', SAND2010-2158P (also in Sintering of Advanced Materials, 2010, DOI 10.1533/9781845699949.1.130)
    - **url**: https://www.osti.gov/servlets/purl/1728557
    - **why**: Open access. The clearest exposition of MSC construction from the combined-stage model, the three independent methods for obtaining Q, the sigmoid fitting function, and the anisotropic MSC modification for LTCC tape (relevant to your layered LCM green body).
  -
    - **citation**: X. Su & D. L. Johnson, 'Master Sintering Curve: A Practical Approach to Sintering', J. Am. Ceram. Soc. 79(12) (1996) 3211-3217. DOI 10.1111/j.1151-2916.1996.tb08097.x
    - **url**: https://doi.org/10.1111/j.1151-2916.1996.tb08097.x
    - **why**: The original MSC paper - cite for the work-of-sintering integral and the residual-minimisation procedure for Q.
  -
    - **citation**: 'Master sintering curve with dissimilar grain growth trajectories: A case study on MgAl2O4', J. Eur. Ceram. Soc. 41 (2021) 1048-1051. DOI 10.1016/j.jeurceramsoc.2020.09.003
    - **url**: https://arxiv.org/pdf/2011.11634
    - **why**: Open access. Gives Park's grain-size-corrected MSC integrand Theta = int (G0/G)^w (1/T)exp(-Q/RT) dt and demonstrates stage-dependent activation energy (400 -> 700 kJ/mol). Essential caveat literature before you quote a single Q for copper.
  -
    - **citation**: McCoy et al., 'A critique of master sintering curve analysis', J. Eur. Ceram. Soc. 38 (2018) 1030-1037. DOI 10.1016/j.jeurceramsoc.2017.12.025
    - **url**: https://doi.org/10.1016/j.jeurceramsoc.2017.12.025
    - **why**: Read before publishing any MSC-derived Q. Documents the assumptions that break and the sensitivity of Q to the fitting function chosen. Paywalled.
  -
    - **citation**: Y. Wang & R. Raj, 'Estimate of the Activation Energies for Boundary Diffusion from Rate-Controlled Sintering of Pure Alumina, and Alumina Doped with Zirconia or Titania', J. Am. Ceram. Soc. 73(5) (1990) 1172-1175. DOI 10.1111/j.1151-2916.1990.tb05175.x
    - **url**: https://doi.org/10.1111/j.1151-2916.1990.tb05175.x
    - **why**: Original kinetic-field / WR method plus the benchmark alumina activation energies (440 / 585 / 730 kJ/mol). The independent Q estimator you must run alongside the MSC.
  -
    - **citation**: H. Riedel, H. Zipse, J. Svoboda, 'Equilibrium pore surfaces, sintering stresses and constitutive equations for the intermediate and late stages of sintering - II. Diffusional densification and creep', Acta Metall. Mater. 42(2) (1994) 445-452. DOI 10.1016/0956-7151(94)90499-5 (Part I: 42(2) 435-443, DOI 10.1016/0956-7151(94)90498-7)
    - **url**: https://doi.org/10.1016/0956-7151(94)90499-5
    - **why**: The mechanism-based alternative to SOVS: constitutive equations derived from grain-boundary diffusion with equilibrium pore surfaces, giving sintering stress and viscosities from micromechanics rather than fitting.
  -
    - **citation**: T. Kraft & H. Riedel, 'Numerical simulation of solid state sintering; model and application', J. Eur. Ceram. Soc. 24 (2004) 345-361. DOI 10.1016/S0955-2219(03)00222-X
    - **url**: https://doi.org/10.1016/s0955-2219(03)00222-x
    - **why**: The practical FEM engineering paper of the Riedel lineage (the model behind Fraunhofer IWM's sintering tools and, indirectly, commercial modules). Covers gravity, friction and grain growth with pore drag.
  -
    - **citation**: R. K. Bordia & G. W. Scherer, 'On constrained sintering - I. Constitutive model for a sintering body' / 'II. Comparison of constitutive models' / 'III. Rigid inclusions', Acta Metallurgica 36(9) (1988) 2393-2397 / 2399-2409 / 2411-2416. DOIs 10.1016/0001-6160(88)90189-7, ...90190-3, ...90191-5
    - **url**: https://doi.org/10.1016/0001-6160(88)90189-7
    - **why**: The origin of the linear-viscous formulation in (E_vis, nu_vis) and of the elastic-viscous analogy that lets you convert between (E_p, nu_p) measured by CLD/sinter-forging and the (K, G) used by SOVS. Part II is the direct comparison of competing constitutive models.
  -
    - **citation**: R. K. Bordia, R. Zuo, O. Guillon, S. M. Salamone, J. Rodel, 'Anisotropic constitutive laws for sintering bodies', Acta Materialia 54 (2006) 111-118. DOI 10.1016/j.actamat.2005.08.025
    - **url**: https://doi.org/10.1016/j.actamat.2005.08.025
    - **why**: The transversely isotropic viscous formulation (5 constitutive parameters + 2 free densification rates) for constrained films and sinter-forging. The rigorous route for your layered LCM green body if the cheap anisotropic-sintering-stress fit proves insufficient.
  -
    - **citation**: F. Li, J. Pan, O. Guillon, A. Cocks, 'Predicting sintering deformation of ceramic film constrained by rigid substrate using anisotropic constitutive law', Acta Materialia 58(18) (2010) 5980-5988. DOI 10.1016/j.actamat.2010.07.015
    - **url**: https://doi.org/10.1016/j.actamat.2010.07.015
    - **why**: Anisotropic law parameterised by sintering STRAINS rather than density; degenerates to the isotropic law under free sintering. Contains the figure demonstrating that an isotropic law cannot reproduce the sinter-forging zero-radial-shrinkage stress.
  -
    - **citation**: A. C. F. Cocks, 'Overview no. 117: The structure of constitutive laws for the sintering of fine grained materials', Acta Metallurgica et Materialia 42(7) (1994) 2191-2210. DOI 10.1016/0956-7151(94)90299-2 (see also the two-part 'A constitutive model for stage 2 sintering of fine grained materials', DOIs 10.1016/0956-7151(94)90138-4 and ...90139-2)
    - **url**: https://doi.org/10.1016/0956-7151(94)90299-2
    - **why**: The systematic classification of what a thermodynamically admissible sintering constitutive law must look like (potential structure, normality, the role of the sintering potential). Read for the theory chapter of your paper. Paywalled, no abstract available via Crossref.
  -
    - **citation**: M. Abouaf, J. L. Chenot, G. Raisson, P. Bauduin, 'Finite element simulation of hot isostatic pressing of metal powders', Int. J. Numer. Methods Eng. 25(1) (1988) 191-212. DOI 10.1002/nme.1620250116
    - **url**: https://doi.org/10.1002/nme.1620250116
    - **why**: Original Abouaf power-law visco-plastic model with the c(rho)/f(rho) weighting functions - the standard framework for METAL powder consolidation, and therefore the more defensible choice for copper than a linear-viscous ceramic model.
  -
    - **citation**: Z. Cai, R. K. Bordia et al., 'Determination of the Mechanical Response of Sintering Compacts by Cyclic Loading Dilatometry', J. Am. Ceram. Soc. 80(2) (1997) 445-452. DOI 10.1111/j.1151-2916.1997.tb02850.x
    - **url**: https://doi.org/10.1111/j.1151-2916.1997.tb02850.x
    - **why**: The CLD technique: equilibrium elastic modulus, viscosity and sintering stress from a single uninterrupted run. The single most cost-effective way to break the bulk/shear identifiability deadlock. See also Mohanram et al., J. Am. Ceram. Soc. 87 (2004) 192-196, DOI 10.1111/j.1551-2916.2004.00192.x, for the isothermal variant.
  -
    - **citation**: 'Modeling and simulation of sintering process across scales', arXiv:2211.00821 (review)
    - **url**: https://arxiv.org/pdf/2211.00821
    - **why**: Open access, ~60 pages. Best single literature map from atomistic through phase-field and DEM to continuum. Eqs. 25-28 give the Riedel/Bordia-Scherer continuum equations; the anisotropy section (around Figs. 41-42) summarises the sinter-forging and constrained-film failures of isotropic laws with full citations.
  -
    - **citation**: 'Effect of Print Orientation on Sintering Shrinkage of BMD 316L Stainless Steel: An Empirical and Numerical Study', Materials 19(15) (2026) 3294. DOI 10.3390/ma19153294
    - **url**: https://pmc.ncbi.nlm.nih.gov/articles/PMC13467325/
    - **why**: Open access. Complete worked example of an Abaqus CREEP-subroutine implementation of Olevsky+Hsueh for an AM metal, including the full 11-parameter table for two build orientations, the PSO calibration objective and settings, solver time/temperature step limits, and the 'artificial gravity' stabilisation trick. The closest published template for a copper AM sintering UMAT.
  -
    - **citation**: V. M. Petrovic, V. V. Buljak, A. Cornaggia, 'Skorohod-Olevsky Viscous Sintering Model Sensitivity to Temperature Distribution During the Sintering Process', FME Transactions 49(3) (2021) 719-725. DOI 10.5937/fme2103719P
    - **url**: https://www.mas.bg.ac.rs/_media/istrazivanje/fme/vol49/3/20_v._buljak_et_al.pdf
    - **why**: Open access. Quantifies when the usual 'uniform temperature' assumption breaks (local density 0.84-0.94 vs 0.91 average) and argues for a loosely coupled transient thermal -> SOVS mechanical workflow. Also a clean restatement of the SOVS equations in tensor notation.
  -
    - **citation**: A. Safonov, S. Chugunov, A. Tikhonov, M. Gusev, I. Akhatov, 'Numerical simulation of sintering for 3D-printed ceramics via SOVS model', Ceramics International 45(15) (2019) 19027-19035 - summarised with parameter values in the pSeven case study
    - **url**: https://www.pseven.io/blog/use-cases/numerical-simulation-of-sintering-for-3d-printed-ceramics-via-sovs-model.html
    - **why**: A worked SOVS calibration for a DLP-printed alumina (the closest printing process to your CeraFab 2M30), including the Abaqus/Standard + surrogate-optimisation inverse identification loop, the fitted A/B/n viscosity constants and an RMSPE of 0.64% in 187 iterations. Template for your own optimisation loop.
  -
    - **citation**: 'Numerical simulation of shrinkage and deformation during sintering in metal binder jetting with experimental validation', Materials & Design 216 (2022) 110490. DOI 10.1016/j.matdes.2022.110490
    - **url**: https://doi.org/10.1016/j.matdes.2022.110490
    - **why**: Open access (Elsevier OA). Uses measured viscosity and sinter stress instead of empirical models, sinters 7 replicates per geometry and proposes a statistical accuracy metric - a good template for the validation section of a paper. Explicitly concludes that anisotropic shrinkage and heterogeneous green density must be modelled for AM parts.
  -
    - **citation**: 'Modelling of geometrical deformation and compensation during sintering of binder jetting', Virtual and Physical Prototyping 20 (2024/25). DOI 10.1080/17452759.2024.2443958
    - **url**: https://doi.org/10.1080/17452759.2024.2443958
    - **why**: Open access. Thermo-elastic-viscoplastic constitutive model plus a reverse shape pre-compensation model; forward error <8%, pre-compensated deviation <3% vs CAD. The quantitative benchmark to beat.
  -
    - **citation**: Chalmers MSc thesis, 'Product Design and Simulation for Metal Binder Jetting - An investigation of sintering deformation and design compensation in Simufact Additive'
    - **url**: https://odr.chalmers.se/items/78d530b0-ce82-431d-9e9c-6e67d097cec7
    - **why**: Open access, honest negative results. Documents Simufact Additive's default friction coefficient (0.3), the exposed 'activation energy of viscous flow' / pre-exponential parameters, the compensation convergence mechanics, and the finding that default material data is inadequate while literature-realistic values crash the solver. Read before buying commercial software.
  -
    - **citation**: I.-W. Chen & X.-H. Wang, 'Sintering dense nanocrystalline ceramics without final-stage grain growth', Nature 404 (2000) 168-171. DOI 10.1038/35004548
    - **url**: https://doi.org/10.1038/35004548
    - **why**: Origin of two-step sintering and the triple-junction-drag argument. Cite for the TSS cycle strategy; note it is an oxide result whose transfer to copper is unproven.
  -
    - **citation**: 'Fabrication of Fine-Grained Functional Ceramics by Two-Step Sintering or Spark Plasma Sintering (SPS)', IntechOpen chapter 67294
    - **url**: https://www.intechopen.com/chapters/67294
    - **why**: Open access. Survey table of T1/T2/hold/density/grain-size for many materials plus the T1 - T2 < 150 C rule of thumb and the kinetic-window explanation. Useful for choosing candidate TSS windows to test on copper.
  -
    - **citation**: H. Palmour III & D. R. Johnson, 'Rate Controlled Sintering Revisited', in Sintering'85, Springer (1987) 17-34. DOI 10.1007/978-1-4613-2851-3_2
    - **url**: https://doi.org/10.1007/978-1-4613-2851-3_2
    - **why**: Primary reference for rate-controlled sintering as a cycle strategy - prescribing the densification rate and solving for T(t). Directly implementable once your eta0(T) is calibrated, and the natural way to cap the gas evolution rate that threatens copper.
  -
    - **citation**: C.-H. Hsueh, A. G. Evans, R. M. Cannon, R. J. Brook, 'Viscoelastic stresses and sintering damage in heterogeneous powder compacts', Acta Metallurgica 34(5) (1986) 927-936. DOI 10.1016/0001-6160(86)90066-0
    - **url**: https://doi.org/10.1016/0001-6160(86)90066-0
    - **why**: Source of the two-parameter power-law bulk viscosity psi = (2/3)(1-theta)^A/theta^B that outperformed Skorohod's theoretical form on binder-jet 316L (A = 11.35 vs 3), and of the interparticle-stress-concentration interpretation of A and B.