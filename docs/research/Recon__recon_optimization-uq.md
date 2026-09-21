- **summary**: The inverse/UQ/optimal-control machinery for this problem is mature and almost entirely off-the-shelf; the hard part is that the *identifiability structure* is dictated by an unknown proprietary binder, so the architecture must be built around parameter triage and sequential experiment design rather than around one big calibration.

CALIBRATION LAYER. The forward model is a coupled DAE/PDE chain: (i) binder decomposition kinetics dα/dt = A exp(-E/RT) f(α), generalised for an unknown multi-component acrylate/dispersant binder to a distributed-activation-energy model (DAEM), α(t) = 1 - ∫ exp(-∫A e^{-E/RT}dt') p(E)dE with p(E) a Gaussian/Weibull/log-normal mixture; (ii) Darcy/Knudsen transport of degradation products through the evolving green pore network with a maximum-internal-pressure failure criterion (Lombardo/Feng; Matar–Evans–Edirisinghe); (iii) densification via a master sintering curve Θ(t,T) = ∫ (1/T) exp(-Q/RT) dt or a full Skorohod–Olevsky viscous sintering (SOVS) continuum model for distortion. SOVS in the verified Sandia form has 11 fitted constants plus a viscosity activation energy — far more than sparse dilatometry can identify, which is precisely why global sensitivity analysis and practical-identifiability analysis are not optional preliminaries but the load-bearing step.

Recommended sequence: Morris elementary-effects screening (cost r(k+1) runs) to cull; Sobol' first/total indices (Saltelli design, N(k+2) runs) on the survivors, computed on a sparse-PCE or GP surrogate rather than the FE model; then profile likelihood (Raue et al.) and Fisher-information/parameter-subset-selection to expose the structural degeneracies you *will* hit — above all the Arrhenius kinetic compensation effect, where ln A and E are near-perfectly correlated along ln A ≈ a + bE so only the isokinetic combination is identifiable from a single heating rate. ICTAC guidance (multiple heating rates, ≥3–5 β values, small sample mass, isoconversional pre-analysis before any model fitting) is the standard that makes the kinetics publishable.

Inference itself: NUTS/HMC (NumPyro/Stan/PyMC) with adjoint ODE sensitivities for the smooth low-dimensional kinetic block; affine-invariant ensemble sampling (emcee) as a robustness cross-check; Sequential Monte Carlo / TMCMC (Ching–Chen) when the Arrhenius posterior is ridged or multimodal and when you need the model evidence to choose between nth-order, Avrami, and DAEM binder models; simulation-based inference (neural posterior estimation, sbi) or ABC-SMC when the observable is a pass/fail crack outcome or a censored off-gas trace with no tractable likelihood. Model form error must be handled explicitly — either Kennedy–O'Hagan (y = η(x,θ) + δ(x) + ε with GP priors on η and δ, accepting the known δ–θ non-identifiability) or Sargsyan's embedded model error, which injects the discrepancy into the physical parameters and therefore keeps predictions physically admissible (mass conservation, α ∈ [0,1]) — preferable here.

EXPERIMENT DESIGN. Because Lithoz will not give you binder chemistry and every furnace run is expensive, Bayesian OED is the highest-leverage piece: maximise expected information gain U(d) = ∫∫ log[p(y|θ,d)/p(y|d)] p(y|θ,d)p(θ) dy dθ, estimated by nested Monte Carlo (biased, O(1/M_inner)) or by variational/contrastive lower bounds; use it to choose heating rates, atmospheres, sample thicknesses and which instrument (TGA vs dilatometer vs EGA-MS vs load cell) to spend on next.

OPTIMAL CYCLE DESIGN. Formulate directly as an optimal control problem: min ∫dt (or a weighted cycle-time/energy/distortion objective) s.t. the kinetic+transport+densification dynamics, |dT/dt| ≤ β_max, T ≤ T_max, internal pressure P ≤ σ_strength, |∇T| ≤ ΔT_max, residual carbon ≤ target, final relative density ≥ target. Solve by direct transcription/orthogonal collocation in CasADi + IPOPT (or multiple shooting, Bock–Plitt) for the ODE-reduced model, and by adjoint-based PDE-constrained optimisation (dolfin-adjoint/pyadjoint over FEniCS/Firedrake) for the full 3D distortion problem. The classical solution of the min-time debinding OCP with an active rate/pressure constraint is a *constant-conversion-rate* trajectory — i.e. CRTA / sample-controlled thermal analysis (Rouquerol) — which is exactly the "uniform-rate debinding" now being applied to vat-photopolymerised ceramics; the sintering analogue is Palmour's rate-controlled sintering. Wrap with NSGA-III/qNEHVI for the cycle-time vs density vs distortion vs energy Pareto front, PCE- or scenario-based chance constraints for robustness to the unknown binder, and an NMPC + moving-horizon-estimation loop (do-mpc) that re-estimates binder state online from TGA/dilatometer/off-gas/load-cell signals.
- **key_facts**:
  -
    - **fact**: The SOVS (Skorohod–Olevsky Viscous Sintering) continuum model, in the form verified at Sandia, is: eps_dot_in_ij = sigma'_ij/(2*eta0(theta)*phi(rho)) + [sigma_kk - 3*sigma_s(rho)]/(18*eta0(theta)*psi(rho)) * delta_ij, with rho_dot = -rho*eps_dot_in_kk. This is the canonical forward model for predicting sintering shrinkage AND distortion, and is what an inverse/UQ layer must calibrate.
    - **source**: B. Lester, 'Verification of the Skorohod-Olevsky Viscous Sintering (SOVS) Model', SAND2017-12933R, Sandia National Laboratories, 2017. https://doi.org/10.2172/1411315
    - **confidence**: high
  -
    - **fact**: The standard SOVS closure forms are phi(rho)=a1*rho^b1, psi(rho)=a2*rho^b2/(1-rho)^c2, sigma_s(rho)=sigma_s0*a3*rho^b3 with sigma_s0=3*alpha/r0 (alpha = surface tension, r0 = grain size), and eta0(theta)=a4*(theta/theta0)^2 + b4*(theta/theta0) + c4. That is 10 shape constants plus sigma_s0 — an 11-parameter model, which is the core practical-identifiability problem for sparse dilatometry data.
    - **source**: SAND2017-12933R, Sandia, 2017. https://doi.org/10.2172/1411315
    - **confidence**: high
  -
    - **fact**: For free sintering (sigma_ij=0) the SOVS model collapses, with the standard parameter set, to the closed-form porosity ODE xi_dot = -3*sigma_s0*xi/(4*eta0); under a 1 MPa uniaxial load (sinter-forge) it becomes xi_dot = sigma*xi/(4*eta0*(1-xi)^2) - 3*sigma_s0*xi/(4*eta0). These give cheap analytic/1-D low-fidelity models for a multi-fidelity surrogate hierarchy.
    - **source**: SAND2017-12933R, Sandia, 2017 (Eqns 30–32). https://doi.org/10.2172/1411315
    - **confidence**: high
  -
    - **fact**: Argüello et al. (quoted verbatim in the Sandia verification report) found that sintering-induced curvature and warpage 'cannot be captured in this model without significant mesh refinement', making full-3D SOVS distortion prediction computationally intensive. This is the direct justification for surrogate-based and multi-fidelity optimisation rather than direct FE-in-the-loop optimisation.
    - **source**: SAND2017-12933R, Sandia, 2017, Sec. 1, quoting Argüello et al. https://doi.org/10.2172/1411315
    - **confidence**: high
  -
    - **fact**: There is a complete, directly transferable body of work formulating debinding as a MINIMUM-TIME optimal control problem: Lombardo, 'Minimum Time Heating Cycles for Diffusion-Controlled Binder Removal from Ceramic Green Bodies' (2014/2015); 'Minimum time heating cycles for diffusion- versus permeability-controlled binder removal' (2016/2017); and Lombardo & Retzloff, 'A process control algorithm for reaction-diffusion minimum time heating cycles for binder removal from green bodies' (2018) — the last being an explicit process-control (MPC-like) formulation.
    - **source**: doi:10.1111/jace.13284; doi:10.1111/jace.14585; doi:10.1111/jace.15964 (titles/DOIs verified via Crossref; full text not accessible in this session)
    - **confidence**: high
  -
    - **fact**: The pressure-based failure criterion for debinding is established: internal gas pressure from binder decomposition, transported by Darcy flow through an anisotropic-permeability green body, must remain below the green strength. Lombardo & Feng modelled 3-D pressure distributions with anisotropic permeability, and Yun & Lombardo measured green-tape permeability as an explicit function of binder loading — the latter is exactly the constitutive input that is UNKNOWN for a proprietary Lithoz slurry and must therefore be inferred.
    - **source**: doi:10.1557/jmr.2002.0213 (Lombardo & Feng 2002); doi:10.1111/j.1151-2916.2003.tb00005.x (Feng & Lombardo 2003); doi:10.1111/j.1551-2916.2006.01444.x (Yun & Lombardo 2007)
    - **confidence**: high
  -
    - **fact**: Explicit dynamic-optimisation (optimal control) of binder burnout has been published: Liau & Chiu, 'Optimal Heating Strategies of Polymer Binder Burnout Process Using Dynamic Optimization Scheme', Ind. Eng. Chem. Res. 2005. Also Song, Evans & Edirisinghe, 'Optimization of heating schedules in pyrolytic binder removal from ceramic moldings', J. Mater. Res. 15 (2000).
    - **source**: doi:10.1021/ie049143a; doi:10.1557/jmr.2000.0068 (titles/DOIs verified via Crossref; full texts paywalled/not read)
    - **confidence**: high
  -
    - **fact**: The Evans/Edirisinghe school established the physics that sets the safe heating-rate constraint: porosity development during vehicle removal, gas permeation as the control on defect incidence, geometry effects on degradation-product diffusion, and critical heating rates modified by the presence of a powder bed. These are the constraint functions g(x,u) <= 0 in the OCP.
    - **source**: doi:10.1557/jmr.1993.0617; doi:10.1007/BF01153938; doi:10.1111/j.1151-2916.1996.tb07938.x; doi:10.1002/aic.690420623; doi:10.1179/imr.1996.41.3.116
    - **confidence**: high
  -
    - **fact**: Constant-Rate Thermal Analysis (CRTA) / Sample-Controlled Thermal Analysis (SCTA) — where the furnace temperature is slaved to hold the decomposition rate dalpha/dt constant — originates with Rouquerol (1969) and is the physical realisation of the min-time debinding solution when the decomposition-rate (or pressure) constraint is active. Reviews and the framework are collected in Sorensen & Rouquerol, 'Sample Controlled Thermal Analysis' (2003).
    - **source**: doi:10.1016/B978-0-12-395733-7.50026-5 (Rouquerol 1969); doi:10.1007/BF01913412 (Bordère, Rouquerol & Rouquerol 1990); doi:10.1007/978-1-4757-3735-6 (SCTA book, 2003); doi:10.1007/978-1-4757-3735-6_5 (SCTA and Ceramics)
    - **confidence**: high
  -
    - **fact**: CRTA-style 'uniform rate debinding' has already been demonstrated specifically for vat-photopolymerisation ceramic green parts: Wang, Duan & Chen et al., 'Uniform rate debinding for Si3N4 vat photopolymerization 3D printing green parts using a specific-stage stepwise heating process', Additive Manufacturing (2024). This is the closest published precedent to the proposed copper-LCM debinding cycle.
    - **source**: doi:10.1016/j.addma.2024.104119 (title/DOI verified via Crossref; full text not read)
    - **confidence**: high
  -
    - **fact**: The Distributed Activation Energy Model (DAEM) has been applied to thermal debinding of a ceramic green body with finite-element simulation: Li, Zhang & Yin et al., 'DAEM kinetics analysis and finite element simulation of thermal debinding process for a gelcast SiAlON green body', Ceramics International (2019). DAEM is the correct model class for a binder of UNKNOWN, multi-component composition, because it replaces a fitted mechanism function f(alpha) with a continuous distribution p(E) that absorbs the unknown chemistry.
    - **source**: doi:10.1016/j.ceramint.2019.01.118 (title/DOI verified via Crossref)
    - **confidence**: high
  -
    - **fact**: Rate-Controlled Sintering (RCS) — feedback control of furnace temperature to hold a prescribed densification (shrinkage) rate trajectory — is a decades-established method (Palmour & Hare, 'Rate Controlled Sintering Revisited', 1987; Palmour, 'Rate Controlled Sintering for Ceramics and Selected Powder Metals', 1989; Huckabee, Hare & Palmour 1978). A shrinkage-rate-controlled sintering dilatometer has been built and described (Speyer, Echiverri & Lee, J. Mater. Sci. Lett. 1992), giving a direct hardware precedent for closed-loop control on an in-situ dilatometer signal.
    - **source**: doi:10.1007/978-1-4613-2851-3_2; doi:10.1007/978-1-4899-0933-6_29; doi:10.1007/978-1-4684-3378-4_18; doi:10.1007/BF00730840
    - **confidence**: high
  -
    - **fact**: Wang & Raj showed that boundary-diffusion activation energies can be EXTRACTED from rate-controlled sintering experiments ('Estimate of the Activation Energies for Boundary Diffusion from Rate-Controlled Sintering of Pure Alumina, and Alumina Doped with Zirconia or Titania', JACerS 1990). RCS is therefore simultaneously an optimal-cycle strategy and an optimal-experiment-design strategy — it maximises information about Q at the same time as it controls microstructure.
    - **source**: doi:10.1111/j.1151-2916.1990.tb05175.x
    - **confidence**: high
  -
    - **fact**: The kinetic compensation effect (near-perfect correlation between ln A and E across fitted Arrhenius pairs) is a well-documented, reviewed phenomenon in solid-state thermal analysis. Practically it means (ln A, E) are NOT jointly identifiable from a single heating rate: only the isokinetic combination is. Multiple heating rates and isoconversional pre-analysis are mandatory.
    - **source**: doi:10.1016/0040-6031(94)80202-5 (Koga, Thermochim. Acta 1994, review); doi:10.1007/s11144-020-01898-2 (Mianowski et al. 2020)
    - **confidence**: high
  -
    - **fact**: The ICTAC Kinetics Committee has issued four authoritative recommendation papers that define what is publishable in this area: kinetic computations (2011), collecting experimental thermal-analysis data (2014), multi-step kinetics (2020), and analysis of thermal decomposition kinetics (2023). Any binder-kinetics identification for a paper must follow these.
    - **source**: doi:10.1016/j.tca.2011.03.034; doi:10.1016/j.tca.2014.05.036; doi:10.1016/j.tca.2020.178597; doi:10.1016/j.tca.2022.179384
    - **confidence**: high
  -
    - **fact**: The Kennedy–O'Hagan framework (y_obs(x) = eta(x,theta) + delta(x) + epsilon, GP priors on the simulator eta and the discrepancy delta) is the canonical treatment of model-form error in computer-model calibration and is the most-cited work in the field (>4400 citations).
    - **source**: doi:10.1111/1467-9868.00294; citation count from Semantic Scholar API
    - **confidence**: high
  -
    - **fact**: An alternative to KO that avoids the delta–theta non-identifiability and keeps predictions physically admissible is 'embedded model error', where the discrepancy is represented as a stochastic perturbation of the physical parameters themselves (Sargsyan, Huan & Najm, Int. J. UQ 2019). For a mass-conserving binder-burnout model this is strongly preferable to an additive GP discrepancy, which can drive alpha outside [0,1].
    - **source**: doi:10.1615/Int.J.UncertaintyQuantification.2019027384
    - **confidence**: high
  -
    - **fact**: Profile likelihood is the established method for PRACTICAL identifiability of partially observed ODE models: re-optimise all other parameters while scanning one, and declare a parameter practically non-identifiable when the profile is flat in one or both directions. Raue et al. (Bioinformatics 2009) is the reference implementation of this idea (>1400 citations); Boiger et al. (Inverse Problems 2016) extended profile-likelihood computation to PDE-constrained parameter estimation.
    - **source**: doi:10.1093/bioinformatics/btp358; doi:10.1088/0266-5611/32/12/125009
    - **confidence**: high
  -
    - **fact**: Bayesian optimal experimental design for nonlinear simulation-based models — maximising expected information gain, estimated by nested Monte Carlo with polynomial-chaos surrogates and stochastic-approximation optimisation — is established and was demonstrated on detailed COMBUSTION KINETICS, a closely analogous inverse problem to binder decomposition kinetics (Huan & Marzouk, JCP 2013). Huan, Jagalur & Marzouk (Acta Numerica 2024) is the current comprehensive survey, including sequential/non-myopic policies.
    - **source**: doi:10.1016/j.jcp.2012.08.013 (arXiv:1108.4146); doi:10.1017/S0962492924000023
    - **confidence**: high
  -
    - **fact**: Amortised/policy-based sequential BOED now exists and removes the need to re-solve the design optimisation after every experiment: Deep Adaptive Design (arXiv:2103.02438), Implicit DAD for likelihood-free models (arXiv:2111.02329), variational sequential OED via reinforcement learning (arXiv:2306.10430), and the unified stochastic-gradient EIG-bound approach (arXiv:1911.00294).
    - **source**: https://arxiv.org/abs/2103.02438; https://arxiv.org/abs/2111.02329; https://arxiv.org/abs/2306.10430; https://arxiv.org/abs/1911.00294
    - **confidence**: high
  -
    - **fact**: Direct transcription/collocation with a sparse NLP solver is the standard route for constrained optimal control of this kind; CasADi provides symbolic AD and interfaces to IPOPT, an interior-point filter line-search NLP solver. do-mpc builds robust/multi-stage NMPC and moving-horizon estimation directly on CasADi+IPOPT.
    - **source**: doi:10.1007/s12532-018-0139-4 (CasADi); doi:10.1007/s10107-004-0559-y (IPOPT); doi:10.1016/j.conengprac.2023.105676 (do-mpc); doi:10.2514/2.4231 (Betts, trajectory-optimisation survey)
    - **confidence**: high
  -
    - **fact**: For the full 3-D PDE (heat + species transport + SOVS viscous flow), gradients w.r.t. the whole temperature programme are obtained at ~O(1) extra solves by the adjoint method; dolfin-adjoint/pyadjoint derives and solves the adjoint of transient FEniCS/Firedrake programs automatically.
    - **source**: doi:10.1137/120873558 (Farrell, Ham, Funke, Rognes, SISC 2013); doi:10.21105/joss.01292 (dolfin-adjoint 2018.1)
    - **confidence**: high
  -
    - **fact**: Multi-fidelity surrogate machinery for coupling a cheap 1-D/MSC model to an expensive 3-D SOVS FE model is well developed: Kennedy–O'Hagan autoregressive co-kriging, Le Gratiet & Garnier's recursive co-kriging formulation (which decouples the levels and makes inference cheap), and cross-validation-based sequential design for multi-fidelity codes.
    - **source**: doi:10.1615/Int.J.UncertaintyQuantification.2014006914; doi:10.1098/rspa.2015.0018; doi:10.1080/00401706.2014.928233
    - **confidence**: high
  -
    - **fact**: Chance-constrained and robust optimal control under parametric uncertainty can be done either by the scenario approach (Calafiore & Campi — sample the uncertainty, enforce constraints on all samples, get a distribution-free probabilistic guarantee) or by propagating a generalized polynomial chaos expansion of the state and enforcing constraints on moments/reachable sets (Bergner & Kirches, OCAM 2017; Lefebvre et al., OCAM 2020).
    - **source**: doi:10.1109/CDC.2007.4434039; doi:10.1002/oca.2329; doi:10.1002/oca.2575
    - **confidence**: high
  -
    - **fact**: Sintering-shrinkage CALIBRATION for metal AM against real parts is an active, publishable topic right now: Burr, Lopez & Becerra et al., 'A calibration method to predict shape change during sintering: Application to 316L parts made by Metal Binder Jetting', Additive Manufacturing (2025); and Balaguer et al., 'Enhanced Skorohod–Olevsky viscous model incorporating microstructure evolution for finite element analysis of ceramic sintering', JECS (2024).
    - **source**: doi:10.1016/j.addma.2025.104938; doi:10.1016/j.jeurceramsoc.2024.05.035
    - **confidence**: high
  -
    - **fact**: A directly comparable copper system has been published: 'Debinding and sintering of copper powder material extrusion parts with a polylactide binder' (J. Manufacturing Processes). Copper + sacrificial polymer + debind/sinter is therefore an established comparison point, though the binder chemistry (PLA) differs from a Lithoz acrylate photopolymer.
    - **source**: doi:10.1016/j.jmapro.2026.01.072 (title/DOI verified via Crossref; full text not read)
    - **confidence**: medium
  -
    - **fact**: Sequential Monte Carlo samplers (Del Moral, Doucet & Jasra, JRSS-B 2006) and Transitional MCMC (Ching & Chen, J. Eng. Mech. 2007) provide tempered sampling of ridged/multimodal posteriors AND a by-product estimate of the model evidence, enabling formal Bayesian model-class selection among competing binder-kinetics mechanisms (nth-order vs Avrami vs DAEM vs multi-step).
    - **source**: doi:10.1111/j.1467-9868.2006.00553.x; doi:10.1061/(ASCE)0733-9399(2007)133:7(816)
    - **confidence**: high
  -
    - **fact**: Adaptive SMC-ABC exists for genuinely intractable likelihoods (Del Moral, Doucet & Jasra, Stat. Comput. 2011), and modern neural simulation-based inference is packaged in 'sbi' (arXiv:2411.17337), which is the appropriate tool if the only observable from some furnace runs is a binary crack/no-crack or a coarse visual distortion score.
    - **source**: doi:10.1007/s11222-011-9271-y; https://arxiv.org/abs/2411.17337
    - **confidence**: high
  -
    - **fact**: The Master Sintering Curve (Su & Johnson, JACerS 1996) reduces densification to rho = f(ln Theta) with Theta(t,T) = integral_0^t (1/T) exp(-Q/RT) dt', collapsing all heating schedules onto one curve for a single apparent Q. It is the natural cheap low-fidelity model in a multi-fidelity hierarchy and the natural reduced model inside an NMPC loop. Pouchly & Maca (2010) give a practical construction procedure.
    - **source**: doi:10.1111/j.1151-2916.1996.tb08097.x; doi:10.2298/SOS1001025P
    - **confidence**: high
  -
    - **fact**: Lithoz's CeraFab Multi 2M30 specifications could not be retrieved in this session (manufacturer pages returned HTTP 404 through the proxy). Build envelope, pixel size and layer thickness must be taken from the machine documentation the group holds.
    - **source**: unverified
    - **confidence**: low
- **numbers**:
  -
    - **quantity**: SOVS normalised-viscosity shape constants (phi = a1*rho^b1)
    - **value**: a1 = 1, b1 = 2
    - **units**: dimensionless
    - **context**: 0.2 um ZnO powder; reference parameter set used for SOVS verification. Use as a prior CENTRE, not a copper value.
    - **source**: SAND2017-12933R Table 1, Sandia 2017. https://doi.org/10.2172/1411315
  -
    - **quantity**: SOVS normalised bulk-viscosity constants (psi = a2*rho^b2/(1-rho)^c2)
    - **value**: a2 = 2/3, b2 = 3, c2 = 1
    - **units**: dimensionless
    - **context**: 0.2 um ZnO powder, same verification set.
    - **source**: SAND2017-12933R Table 1, Sandia 2017. https://doi.org/10.2172/1411315
  -
    - **quantity**: SOVS normalised sintering-stress constants (sigma_s_bar = a3*rho^b3)
    - **value**: a3 = 1, b3 = 2
    - **units**: dimensionless
    - **context**: 0.2 um ZnO powder, same verification set.
    - **source**: SAND2017-12933R Table 1, Sandia 2017. https://doi.org/10.2172/1411315
  -
    - **quantity**: SOVS skeleton shear-viscosity quadratic coefficients (eta0 = a4*(T/T0)^2 + b4*(T/T0) + c4)
    - **value**: a4 = 517, b4 = -1066, c4 = 564
    - **units**: GPa*s
    - **context**: 0.2 um ZnO, 750–1000 C. Note this is a quadratic in T/T0, NOT Arrhenius; Reiterer/Ewsuk/Arguello (doi:10.1111/j.1551-2916.2006.01041.x) replaced it with an Arrhenius form, which is the better choice for copper.
    - **source**: SAND2017-12933R Table 1, Sandia 2017. https://doi.org/10.2172/1411315
  -
    - **quantity**: Surface tension and grain size used to set the local sintering stress sigma_s0 = 3*alpha/r0
    - **value**: alpha = 1.27, r0 = 1
    - **units**: J/m^2 and um
    - **context**: ZnO reference set. For copper, alpha is different (solid Cu surface energy ~1.7-1.8 J/m^2 is commonly quoted but was NOT verified here).
    - **source**: SAND2017-12933R Table 1, Sandia 2017. https://doi.org/10.2172/1411315
  -
    - **quantity**: Local sintering stress sigma_s0 implied by the above (3*alpha/r0)
    - **value**: 3.81
    - **units**: MPa
    - **context**: Arithmetic from alpha=1.27 J/m^2 and r0=1 um. Scales as 1/r0, so a 1 um Cu powder gives MPa-level sintering stress; a 100 nm powder gives ~38 MPa. Use as a sanity bound on the driving stress in the OCP.
    - **source**: Derived from SAND2017-12933R Table 1. https://doi.org/10.2172/1411315
  -
    - **quantity**: Elastic constants used alongside SOVS in the Sierra/SolidMechanics verification
    - **value**: E = 123.7 GPa, nu = 0.356
    - **units**: GPa, dimensionless
    - **context**: ZnO verification problem. Shown here only to indicate that a small elastic response is carried alongside the viscous sintering strain rate.
    - **source**: SAND2017-12933R, Sandia 2017. https://doi.org/10.2172/1411315
  -
    - **quantity**: SOVS verification thermal programme
    - **value**: 750 -> 1000 C at 5 C/min, tf = 3000 s
    - **units**: C, C/min, s
    - **context**: Free-sinter and sinter-forge (1 MPa tensile) benchmark problems; relative density evolved from ~0.45 to ~0.70 over this ramp. Use this as the verification case for your own SOVS implementation before touching copper.
    - **source**: SAND2017-12933R, Sec. 3.1, Sandia 2017. https://doi.org/10.2172/1411315
  -
    - **quantity**: Time step required for accurate SOVS constitutive integration in the verification problem
    - **value**: dt = 15 s adequate; dt = 600 s inadequate
    - **units**: s
    - **context**: 5 uniform steps (600 s) showed visible error in rho(T) for both McHugh-Riedel and fully implicit schemes; 200 uniform steps (15 s) reproduced the analytic solution. Sets a floor on temporal resolution for the forward model inside any optimiser.
    - **source**: SAND2017-12933R, Fig. 1, Sandia 2017. https://doi.org/10.2172/1411315
  -
    - **quantity**: Model evaluations for a full Sobol' first+total-order sensitivity analysis (Saltelli design)
    - **value**: N*(k+2)
    - **units**: model runs
    - **context**: k = number of uncertain parameters, N = base sample size (typically 2^10-2^14 for stable total indices). For k=12 SOVS+kinetic parameters and N=1024 that is ~14,336 forward runs — infeasible on a 3-D FE model, hence mandatory surrogate.
    - **source**: Saltelli, Annoni, Azzini et al., Comput. Phys. Commun. 181 (2010) 259. https://doi.org/10.1016/j.cpc.2009.09.018 (design cited from standard practice; paper not read in this session)
  -
    - **quantity**: Model evaluations for a Morris elementary-effects screening
    - **value**: r*(k+1)
    - **units**: model runs
    - **context**: r = number of trajectories, typically 10-50. For k=20 and r=20 that is 420 runs — cheap enough to run on the mid-fidelity model directly, which is why screening precedes Sobol'.
    - **source**: Morris, Technometrics 33 (1991) 161. https://doi.org/10.1080/00401706.1991.10484804 (cost formula from standard practice; paper not read in this session)
  -
    - **quantity**: Profile-likelihood threshold for a 95% pointwise confidence interval on one parameter
    - **value**: Delta(-2 log L) = 3.84
    - **units**: dimensionless (chi^2_{1,0.95})
    - **context**: Scan one parameter, re-optimise the rest; the interval is where the profile stays below this threshold. Use df = number of parameters for simultaneous intervals. A profile that never crosses the threshold on one side = practically non-identifiable in that direction.
    - **source**: Raue et al., Bioinformatics 25 (2009) 1923. https://doi.org/10.1093/bioinformatics/btp358 (threshold is the standard chi^2 result; value not re-read from the paper here)
  -
    - **quantity**: Cardinality of a total-degree-p polynomial chaos expansion in n random inputs
    - **value**: P+1 = (n+p)! / (n! p!)
    - **units**: basis terms
    - **context**: n=10 inputs, p=3 gives 286 terms — already demanding ~2-3x that many model runs for least-squares regression, which motivates sparse/LARS-based PCE for the full parameter set.
    - **source**: standard multivariate-polynomial result (combinatorial identity); see Feinberg & Langtangen, J. Comput. Sci. 11 (2015) 46, https://doi.org/10.1016/j.jocs.2015.08.008
  -
    - **quantity**: Training cost of an exact Gaussian-process surrogate
    - **value**: O(n^3) time, O(n^2) memory
    - **units**: —
    - **context**: n = number of training simulations. Practical exact-GP ceiling ~5,000-10,000 points; beyond that use sparse/inducing-point GPs or sparse PCE. Relevant because a full 3-D SOVS design of experiments will be limited to O(100) runs anyway.
    - **source**: standard GP regression complexity (textbook result); unverified in this session
  -
    - **quantity**: Nested Monte Carlo estimator of expected information gain: bias and total error scaling
    - **value**: bias ~ O(1/M_inner); MSE ~ O(1/N_outer) + O(1/M_inner^2); with M ~ N^(1/2) the RMSE is ~O(N^(-1/3)) in total cost
    - **units**: —
    - **context**: Sets the budget for EIG evaluation when choosing the next furnace/TGA experiment. If this cost is prohibitive, use the variational/contrastive lower bounds instead (arXiv:1911.00294).
    - **source**: unverified (standard nested-MC OED result; framework in Huan & Marzouk, J. Comput. Phys. 232 (2013) 288, https://doi.org/10.1016/j.jcp.2012.08.013 — the specific exponents were NOT confirmed from the paper in this session)
  -
    - **quantity**: Melting point of pure copper (hard upper bound on any sintering hold)
    - **value**: 1084.62
    - **units**: C
    - **context**: Absolute T_max in the optimal-control problem; practical peak sintering holds for Cu are normally set 100-200 C below this. Any optimiser must be given T_max strictly below this value.
    - **source**: unverified (standard reference value; not confirmed against a primary source in this session)
  -
    - **quantity**: Number of independent parameters in a bare SOVS + Arrhenius-viscosity + MSC forward model
    - **value**: 11 SOVS constants + 1 viscosity activation energy + (2 to 3N) binder-kinetics parameters
    - **units**: parameters
    - **context**: With a 3-Gaussian DAEM binder model (3 x {A, E_mean, sigma_E, weight}) the joint inverse problem is ~24-dimensional. Sparse dilatometry + TGA will identify maybe 4-8 of these; the rest must be fixed by screening or absorbed into an embedded-error term.
    - **source**: Parameter count derived from SAND2017-12933R Table 1 (https://doi.org/10.2172/1411315) plus standard DAEM structure; the 'identifiable subset' estimate is unverified
  -
    - **quantity**: Minimum number of distinct heating rates required for a defensible isoconversional kinetic analysis
    - **value**: >= 3, preferably 5
    - **units**: heating rates (K/min)
    - **context**: ICTAC recommendation for collecting thermal-analysis data for kinetic computations; typically spanning roughly a decade, e.g. 1, 2, 5, 10, 20 K/min. This is the minimum TGA campaign needed before any binder-kinetics posterior is credible.
    - **source**: Vyazovkin et al., Thermochim. Acta 590 (2014) 1, https://doi.org/10.1016/j.tca.2014.05.036 (recommendation is standard ICTAC practice; the exact numeric minimum was NOT re-read from the paper in this session — treat as unverified)
- **models_or_methods**:
  -
    - **name**: Kennedy–O'Hagan Bayesian calibration with additive GP discrepancy
    - **formulation**: y_obs(x_i) = zeta(x_i) + eps_i ;  zeta(x) = rho * eta(x, theta) + delta(x) ;  eta ~ GP(m_eta, k_eta), delta ~ GP(m_delta, k_delta), eps ~ N(0, sigma^2 I).
Posterior: p(theta, phi_eta, phi_delta, sigma | y) ∝ L(y | theta, ...) * p(theta) * p(phi) .
In the 'modularised' variant the emulator hyperparameters phi_eta are fitted first from simulator runs alone and then held fixed, which removes feedback from field data into the emulator.
    - **when_to_use**: When you have (a) a slow simulator you must emulate, (b) field data at several controllable settings x (sample thickness, heating rate, atmosphere), and (c) an acknowledged structural error in the physics — e.g. a 1-D debinding model applied to a 3-D LCM lattice. Gives calibrated predictions WITH discrepancy bands.
    - **limitations**: theta and delta(x) are fundamentally confounded: an unidentified bias can be absorbed either by shifting theta or by inflating delta. The posterior on theta is then not the 'true physical value'. An additive GP delta can also drive unphysical predictions (alpha outside [0,1], negative porosity). Mitigate by strong physical priors on theta, by modularisation, and/or by switching to embedded model error.
    - **inputs_needed**: Simulator runs at a design over (x, theta); field observations y at several x; priors on theta.
    - **source**: Kennedy & O'Hagan, JRSS-B 63 (2001) 425. https://doi.org/10.1111/1467-9868.00294
  -
    - **name**: Embedded model error (Sargsyan–Huan–Najm)
    - **formulation**: Replace theta by a random field: theta -> theta + sum_k alpha_k * Psi_k(xi), xi ~ N(0,I), i.e. push the discrepancy INTO the physical parameters. Then
 y_obs = eta(x, theta(xi)) + eps ,
and the induced predictive distribution automatically respects every structural constraint the forward model enforces (mass conservation, 0 <= alpha <= 1, 0 <= rho <= 1). Calibrate (theta, alpha) by matching moments or by an approximate likelihood on the pushed-forward distribution.
    - **when_to_use**: Preferred over KO for this project, because binder burnout and densification models are conservation-law-based and an additive GP discrepancy will violate them. Use when you want predictions at NEW geometries/cycles to remain physically admissible.
    - **limitations**: Likelihood is intractable (requires moment matching or an approximate Bayesian computation-style distance); harder to implement than KO; extra parameters alpha_k must themselves be screened for identifiability.
    - **inputs_needed**: Same as KO, plus a choice of which parameters carry the embedded error.
    - **source**: Sargsyan, Huan & Najm, Int. J. Uncertainty Quantification 9 (2019). https://doi.org/10.1615/Int.J.UncertaintyQuantification.2019027384
  -
    - **name**: Distributed Activation Energy Model (DAEM) for an UNKNOWN multi-component binder
    - **formulation**: alpha(t) = 1 - Integral_0^inf exp( - Integral_0^t A(E) * exp(-E/(R*T(t'))) dt' ) * p(E) dE ,
with p(E) = sum_j w_j * N(E; E_j, sigma_j) (or Weibull / log-normal), sum_j w_j = 1.
The Miura–Maki inversion gives a non-parametric p(E) directly from >=3 TGA curves at different beta.
Special cases: sigma_j -> 0 recovers a discrete multi-step nth-order model; a single narrow Gaussian recovers classical single-step Arrhenius.
    - **when_to_use**: This is THE right model class here. Lithoz's binder is proprietary and almost certainly a mixture (acrylate monomers/oligomers, photoinitiator, dispersant, possibly a wax or plasticiser). DAEM lets you fit the observable mass-loss behaviour without pretending to know the chemistry, and p(E) becomes the physically interpretable, publishable deliverable ('the binder's activation-energy spectrum').
    - **limitations**: p(E) is only weakly identifiable from few heating rates — regularise it (Dirichlet prior on w_j, log-normal on sigma_j) and report the posterior over p(E), not a point estimate. Strong A-E compensation persists within each mode. Oxidative vs inert atmosphere gives genuinely DIFFERENT p(E) — must be fitted per atmosphere.
    - **inputs_needed**: TGA (and ideally TGA-MS/FTIR) at >=3, preferably 5 heating rates, in each candidate atmosphere (Ar, Ar/H2, N2, low-pO2), on printed green samples not on raw slurry.
    - **source**: Li, Zhang, Yin et al., Ceramics International 45 (2019), https://doi.org/10.1016/j.ceramint.2019.01.118 ; DAEM methodology e.g. Wu, Cai & Liu, Ind. Eng. Chem. Res. 52 (2013), https://doi.org/10.1021/ie4021123
  -
    - **name**: Isoconversional (model-free) pre-analysis: Friedman and KAS/FWO
    - **formulation**: Friedman (differential): ln(d alpha/dt)_{alpha,i} = ln[A(alpha) f(alpha)] - E(alpha)/(R * T_{alpha,i}) — slope over heating rates i at fixed alpha gives E(alpha).
KAS: ln(beta_i / T_{alpha,i}^2) = const - E(alpha)/(R * T_{alpha,i}).
FWO: ln(beta_i) = const - 1.052 * E(alpha)/(R * T_{alpha,i}).
    - **when_to_use**: MANDATORY first step before any model fitting, per ICTAC. E(alpha) vs alpha immediately tells you how many kinetic steps you are dealing with: flat E(alpha) => single step; a step change or monotone drift => multi-step / DAEM required. It also gives you the priors for E in the Bayesian fit, which is the only way to break the compensation ridge.
    - **limitations**: Friedman is noise-amplifying (needs dalpha/dt); KAS/FWO use integral approximations and are biased when E(alpha) varies strongly. None of them gives A or f(alpha).
    - **inputs_needed**: TGA at >=3 heating rates.
    - **source**: ICTAC recommendations, Vyazovkin et al., Thermochim. Acta 520 (2011) 1, https://doi.org/10.1016/j.tca.2011.03.034 ; Budrugeac & Cucos, Thermochim. Acta (2025), https://doi.org/10.1016/j.tca.2025.180104
  -
    - **name**: Internal-pressure / Darcy debinding model with a strength constraint
    - **formulation**: Species: d(eps_p * c)/dt = div( D_eff(eps_p) * grad c ) - div( c * v ) + S(alpha, T) , S = rho_b0 * (d alpha/dt) / M .
Darcy: v = -(K(eps_p)/mu) * grad P ; with ideal gas c = P/(R T).
Combined (permeation-controlled limit): d(eps_p * P/(RT))/dt = div( (K(eps_p) * P /(mu R T)) * grad P ) + S .
Constraint: max_over_x,t [ P(x,t) - P_ambient ] <= sigma_green / SF .
The Evans/Edirisinghe result is that the safe heating rate scales roughly as beta_max ~ C * K * sigma_green / (L^2 * rho_b0) — i.e. quadratically penalised by the largest wall thickness L.
    - **when_to_use**: This is the constraint that actually sets the debinding ramp rate. Build it in 1-D through the thickest section first (cheap, differentiable, usable inside CasADi), then in 3-D for the real lattice geometry.
    - **limitations**: K(eps_p) for a Lithoz copper green body is UNKNOWN and is the single most influential unmeasured parameter. Yun & Lombardo showed K depends strongly on binder loading — so K evolves with alpha during the cycle. sigma_green is also unknown and temperature-dependent (it collapses once the binder softens). Both must be inferred or bounded.
    - **inputs_needed**: Green permeability vs binder burn-off fraction (gas-flow permeametry on green discs at partial burn-out), green strength vs temperature (hot 3-pt bend or in-situ), binder mass fraction (get it from TGA residue), open porosity.
    - **source**: Lombardo & Feng, J. Mater. Res. 17 (2002) https://doi.org/10.1557/jmr.2002.0213 ; Feng & Lombardo, JACerS 86 (2003) https://doi.org/10.1111/j.1151-2916.2003.tb00005.x ; Yun & Lombardo, JACerS 90 (2007) https://doi.org/10.1111/j.1551-2916.2006.01444.x ; Matar, Edirisinghe & Evans, J. Mater. Sci. 30 (1995) https://doi.org/10.1007/BF01153938
  -
    - **name**: Minimum-time debinding as an optimal control problem (the Lombardo formulation)
    - **formulation**: min_{T(t)} t_f
 s.t.  dot(z) = f(z, T)            [DAEM kinetics + Darcy/diffusion transport]
       P_max(z(t)) <= P_crit          [no cracking]
       |dT/dt| <= beta_max            [furnace hardware]
       T_min <= T(t) <= T_max
       alpha(t_f) >= 1 - eps_residual  [residual carbon spec]
The solution structure is bang-constraint: T(t) rises as fast as the hardware allows until the pressure/rate constraint activates, then rides ALONG that constraint (a singular arc) — which is exactly a constant-decomposition-rate trajectory, i.e. CRTA.
    - **when_to_use**: This is your headline result for the paper: derive the optimal cycle rather than trial-and-error it. Solve the 1-D reduced model by direct collocation in CasADi+IPOPT (fast, minutes), then validate against the 3-D FE model.
    - **limitations**: The solution is only as good as P_crit, K(alpha) and the kinetics; propagate the posterior through it (see robust/chance-constrained entry). The true optimum is often a 'staircase' in real furnaces because programmers only accept segmented ramp/hold programmes — impose that structure explicitly as a discrete parametrisation if needed.
    - **inputs_needed**: Calibrated kinetics + transport model, furnace ramp/temperature limits, residual-carbon spec.
    - **source**: Lombardo, JACerS (2015) https://doi.org/10.1111/jace.13284 ; Lombardo, JACerS (2017) https://doi.org/10.1111/jace.14585 ; Lombardo & Retzloff, JACerS (2018) https://doi.org/10.1111/jace.15964 ; Liau & Chiu, Ind. Eng. Chem. Res. 44 (2005) https://doi.org/10.1021/ie049143a ; Song, Evans & Edirisinghe, J. Mater. Res. 15 (2000) https://doi.org/10.1557/jmr.2000.0068
  -
    - **name**: CRTA / Sample-Controlled Thermal Analysis as the realised feedback law
    - **formulation**: Control law: choose T(t) such that d alpha/dt = C (a constant set-point), i.e.
 T(t) = E / ( R * ln[ A * f(alpha(t)) / C ] )   for a single-step model,
 or, model-free, drive T by a PI loop on the measured evolution rate (TGA mass-loss rate, or evolved-gas partial pressure, or furnace pumping rate at constant residual pressure).
Rate-jump variant: step C between C1 and C2 at fixed alpha; then E(alpha) = R * ln(C2/C1) / (1/T1 - 1/T2) — a direct, model-free activation-energy measurement.
    - **when_to_use**: Two uses. (1) As the ACTUAL debinding cycle: it is the optimal-control solution under an active rate constraint and it is already demonstrated for vat-photopolymerised ceramics ('uniform rate debinding'). (2) As an EXPERIMENT: the rate-jump protocol is an exceptionally information-dense way to get E(alpha) for an unknown binder in one run.
    - **limitations**: Needs a furnace with a fast, trustworthy rate signal (TGA-in-furnace, off-gas MS, or manostat-controlled vacuum). C must be chosen small enough that internal pressure stays subcritical — C is effectively the decision variable that the OCP above chooses for you.
    - **inputs_needed**: Real-time evolved-gas or mass-loss signal; a furnace controller that accepts an external set-point.
    - **source**: Rouquerol (1969) https://doi.org/10.1016/B978-0-12-395733-7.50026-5 ; Bordère, Rouquerol & Rouquerol, J. Therm. Anal. 36 (1990) https://doi.org/10.1007/BF01913412 ; Rouquerol & Sorensen (eds), Sample Controlled Thermal Analysis (2003) https://doi.org/10.1007/978-1-4757-3735-6 ; Wang, Duan & Chen et al., Additive Manufacturing (2024) https://doi.org/10.1016/j.addma.2024.104119
  -
    - **name**: Rate-Controlled Sintering (RCS) and its use as optimal experimental design
    - **formulation**: Control T(t) so that the measured densification rate follows a prescribed schedule, typically
 d rho/dt = g(rho)  (e.g. a trapezoid in rho: fast early, slow through the final-stage pore-closure window).
Instrumentally: a dilatometer measures dL/L; a PI/model-based controller adjusts furnace power to track the shrinkage-rate set-point (Speyer et al. built exactly this).
Inverse use (Wang & Raj): from RCS runs at different rho-dot set-points, Q_boundary is extracted from the T(rho) shift needed to hold each rate.
    - **when_to_use**: For the sintering half of the cycle. Copper's narrow window below 1084.6 C and its tendency to coarsen make rate control much safer than a fixed ramp. RCS also lets you deliberately slow through the final-stage window to close porosity without grain growth.
    - **limitations**: Requires an in-situ dilatometer coupled to the furnace, which most production furnaces lack; the group will likely need a push-rod or optical dilatometer as a separate instrument, then TRANSFER the resulting T(t) open-loop to the production furnace.
    - **inputs_needed**: In-situ dilatometry; a densification model (MSC or SOVS) to convert the measured shrinkage into rho.
    - **source**: Palmour & Hare, 'Rate Controlled Sintering Revisited' (1987) https://doi.org/10.1007/978-1-4613-2851-3_2 ; Speyer, Echiverri & Lee, J. Mater. Sci. Lett. 11 (1992) https://doi.org/10.1007/BF00730840 ; Wang & Raj, JACerS 73 (1990) https://doi.org/10.1111/j.1151-2916.1990.tb05175.x ; Hareesh & Johnson, Trans. Ind. Ceram. Soc. 66 (2007) https://doi.org/10.1080/0371750X.2007.11012271
  -
    - **name**: Master Sintering Curve (MSC) as the reduced-order densification model
    - **formulation**: Theta(t, T) = Integral_0^t (1/T(t')) * exp( -Q / (R T(t')) ) dt'
 rho = f( ln Theta ) , usually fitted as a sigmoid: rho = rho0 + (rho_f - rho0) / (1 + exp( -(ln Theta - a)/b )).
Q is chosen to MINIMISE the mean residual (scatter) of rho vs ln Theta across dilatometry runs at several heating rates — i.e. Q is itself an inverse-problem output with a well-defined objective.
    - **when_to_use**: As the cheap low-fidelity model inside a multi-fidelity surrogate, inside the NMPC loop, and as the first-pass answer to 'what peak temperature and hold do I need for 98% density?'. Requires only 3-4 constant-heating-rate dilatometry runs.
    - **limitations**: Assumes a single dominant mechanism with constant Q and no microstructure-path dependence; breaks down if a reduction reaction (Cu2O + H2) or a wetting/liquid phase intervenes, and gives NO distortion information (it is a scalar model). For copper the MSC will likely fail if the oxide state changes mid-cycle — fit it separately per atmosphere.
    - **inputs_needed**: Dilatometry at >=3 heating rates on identical green bodies (same LCM print, same debinding cycle), plus green density and final Archimedes density.
    - **source**: Su & Johnson, JACerS 79 (1996) 3211, https://doi.org/10.1111/j.1151-2916.1996.tb08097.x ; Pouchly & Maca, Sci. Sintering 42 (2010), https://doi.org/10.2298/SOS1001025P
  -
    - **name**: Morris screening then Sobol' variance-based global sensitivity analysis
    - **formulation**: Morris elementary effect: EE_i = [ Y(x_1,..,x_i + Delta,..,x_k) - Y(x) ] / Delta ; report mu*_i = mean|EE_i| and sigma_i (interaction/nonlinearity indicator). Cost r*(k+1).
Sobol': S_i = Var_{x_i}[ E(Y | x_i) ] / Var(Y) ; S_Ti = 1 - Var_{x_~i}[ E(Y | x_~i) ] / Var(Y) = E_{x_~i}[ Var(Y|x_~i) ]/Var(Y). Saltelli design costs N*(k+2).
Decision rule: parameters with S_Ti below ~0.01-0.05 for EVERY quantity of interest are fixed at nominal values and removed from the calibration.
    - **when_to_use**: Before any MCMC. With ~24 candidate parameters and O(10) experiments, calibration is hopeless unless you first cut to the 4-8 that matter. Run it on separate QoIs: final density, max distortion, max internal pressure, residual carbon, cycle time — the important subset differs per QoI and that is itself a publishable result.
    - **limitations**: Sobol' assumes independent inputs; Arrhenius (ln A, E) pairs are strongly dependent, so either reparametrise onto (E, T_iso) where T_iso is the isokinetic temperature, or use Kucherenko/Shapley indices for dependent inputs. Both methods need a surrogate for a 3-D FE model.
    - **inputs_needed**: Parameter ranges (from the isoconversional pre-analysis and literature bounds), a surrogate, defined QoIs.
    - **source**: Morris, Technometrics 33 (1991) 161, https://doi.org/10.1080/00401706.1991.10484804 ; Sobol', Math. Comput. Simul. 55 (2001) 271, https://doi.org/10.1016/S0378-4754(00)00270-6 ; Saltelli et al., Comput. Phys. Commun. 181 (2010) 259, https://doi.org/10.1016/j.cpc.2009.09.018 ; SALib: https://doi.org/10.21105/joss.00097
  -
    - **name**: Practical identifiability: profile likelihood, Fisher information, parameter subset selection
    - **formulation**: Profile: PL(theta_i) = min_{theta_~i} [ -2 log L(theta_i, theta_~i) ] ; theta_i is practically non-identifiable if PL stays below the chi^2 threshold out to the prior bound on one or both sides.
FIM: F_jk = sum_n (1/sigma_n^2) * (d y_n/d theta_j)(d y_n/d theta_k) ; Cramer-Rao Cov(theta) >= F^{-1}. Compute the eigen-decomposition of F: near-zero eigenvalues identify sloppy DIRECTIONS in parameter space (which are usually the ln A - E compensation direction, not any single parameter).
Subset selection: rank-revealing QR / column pivoting on the scaled sensitivity matrix S = [d y/d theta] to pick the best-conditioned identifiable subset; fix the rest.
    - **when_to_use**: Immediately after screening and again after the first MCMC. This is what stops you from publishing a confident posterior on a parameter that the data never constrained. For PDE models use the integration-based profile-likelihood method of Boiger et al.
    - **limitations**: Profile likelihood costs one full re-optimisation per grid point per parameter (expensive but embarrassingly parallel). FIM is local — it describes the curvature at one point, not the global posterior geometry; check it against the MCMC posterior.
    - **inputs_needed**: Forward-model sensitivities (adjoint or forward AD), an optimiser, the observation error model.
    - **source**: Raue et al., Bioinformatics 25 (2009) 1923, https://doi.org/10.1093/bioinformatics/btp358 ; Boiger et al., Inverse Problems 32 (2016) 125009, https://doi.org/10.1088/0266-5611/32/12/125009 ; Simpson & Maclaren, PLoS Comput. Biol. 19 (2023) e1011515, https://doi.org/10.1371/journal.pcbi.1011515
  -
    - **name**: Posterior sampling: NUTS/HMC, ensemble MCMC, SMC/TMCMC, and simulation-based inference
    - **formulation**: NUTS/HMC: sample p(theta|y) using gradients d log p/d theta obtained by AD through the ODE solve (or by the continuous adjoint). Diagnostics: R-hat < 1.01, ESS > 400 per parameter, zero divergences.
Affine-invariant ensemble (emcee): stretch move z ~ g(z) on 2L walkers; handles badly scaled/correlated posteriors without gradients (use >= 2k walkers).
SMC/TMCMC: temper p_j(theta) ∝ p(theta) * L(theta)^{beta_j}, 0 = beta_0 < ... < beta_J = 1, adapting beta_j to hold a target ESS; by-product = log evidence log Z, enabling Bayes-factor comparison of binder mechanism models.
SBI/ABC: when the likelihood is intractable (binary crack outcome, censored EGA), train a neural posterior/likelihood estimator on simulated (theta, y) pairs, or run SMC-ABC with a summary-statistic distance.
    - **when_to_use**: NUTS for the smooth 4-8 parameter reduced model. emcee as a gradient-free cross-check and when the model is a black-box FE call. SMC/TMCMC when the posterior is a curved ridge (guaranteed for Arrhenius pairs) or when you must select among mechanism models. SBI when the only observable is pass/fail.
    - **limitations**: NUTS needs differentiable solvers — stiff DAEM integrals and FE contact make this non-trivial (use diffrax/JAX for the ODE block, keep the FE block in a surrogate). Ensemble samplers scale badly past ~20 dimensions. Evidence estimates from SMC are sensitive to the tempering schedule.
    - **inputs_needed**: A likelihood (Gaussian on TGA mass-loss and dilatometer strain, with a per-instrument sigma treated as a nuisance parameter), priors from the isoconversional analysis.
    - **source**: Hoffman & Gelman NUTS via Stan, https://doi.org/10.18637/jss.v076.i01 ; PyMC https://doi.org/10.7717/peerj-cs.1516 ; NumPyro https://arxiv.org/abs/1912.11554 ; emcee https://doi.org/10.1086/670067 ; Del Moral, Doucet & Jasra, JRSS-B 68 (2006) 411, https://doi.org/10.1111/j.1467-9868.2006.00553.x ; Ching & Chen, J. Eng. Mech. 133 (2007) 816, https://doi.org/10.1061/(ASCE)0733-9399(2007)133:7(816) ; SMC-ABC https://doi.org/10.1007/s11222-011-9271-y ; sbi https://arxiv.org/abs/2411.17337
  -
    - **name**: Surrogates: sparse PCE, GP, and multi-fidelity recursive co-kriging
    - **formulation**: Sparse PCE: Y(xi) ≈ sum_{a in A} c_a * Psi_a(xi), Psi_a = product of orthonormal univariate polynomials w.r.t. the input marginals; A chosen by LAR / hyperbolic truncation. Sobol' indices come ANALYTICALLY from the c_a: S_i = sum_{a in A_i} c_a^2 / sum_{a != 0} c_a^2.
GP: y ~ GP(m(x), k(x,x')), k typically Matern-5/2 with ARD lengthscales (the lengthscales are themselves a sensitivity diagnostic).
Multi-fidelity AR(1)/co-kriging: y_H(x) = rho(x) * y_L(x) + delta(x), with y_L and delta independent GPs. Le Gratiet's recursive formulation fits each level independently, reducing the training cost from O((n_L+n_H)^3) to O(n_L^3) + O(n_H^3).
    - **when_to_use**: Essential. Low fidelity = 1-D axisymmetric/analytic SOVS + MSC (seconds); high fidelity = 3-D FE SOVS on the real lattice (hours). Train ~500-2000 LF runs and ~30-100 HF runs. Use the surrogate for GSA, MCMC, EIG and the outer optimisation loop.
    - **limitations**: PCE degrades in high dimension and for non-smooth responses (e.g. a crack/no-crack indicator is discontinuous — use a GP classifier there instead). Co-kriging assumes the LF model is CORRELATED with the HF model; verify with a held-out set before trusting it.
    - **inputs_needed**: A space-filling design (Sobol' sequence or LHS) over the parameter x cycle-design space; a nested design for the multi-fidelity levels.
    - **source**: Feinberg & Langtangen (ChaosPy), J. Comput. Sci. 11 (2015) 46, https://doi.org/10.1016/j.jocs.2015.08.008 ; Le Gratiet & Garnier, Int. J. UQ 4 (2014), https://doi.org/10.1615/Int.J.UncertaintyQuantification.2014006914 ; Perdikaris et al., Proc. R. Soc. A 471 (2015), https://doi.org/10.1098/rspa.2015.0018 ; Le Gratiet & Cannamela, Technometrics 57 (2015), https://doi.org/10.1080/00401706.2014.928233
  -
    - **name**: Bayesian Optimal Experimental Design (which experiment to run next)
    - **formulation**: U(d) = E_{y,theta|d} [ log p(theta | y, d) - log p(theta) ]
     = Integral Integral log[ p(y | theta, d) / p(y | d) ] * p(y | theta, d) * p(theta) dy dtheta .
Nested MC: U_hat(d) = (1/N) sum_n [ log p(y_n | theta_n, d) - log( (1/M) sum_m p(y_n | theta_m, d) ) ].
Variational/contrastive lower bounds (PCE, NMC-with-critic, InfoNCE/NWJ) remove the nested inner loop and permit stochastic-gradient optimisation over continuous d.
Gaussian/linear special case: U(d) reduces to (1/2) log det( F(d) + Sigma_prior^{-1} ) — i.e. Bayesian D-optimality.
Goal-oriented variant: replace theta by a QoI (e.g. 'the peak temperature needed for 98% density') and maximise information about THAT instead of about all parameters.
    - **when_to_use**: This is the highest-value component of the whole architecture given that (a) the binder is unknown and (b) each furnace run costs days. Design variables d = {heating rate, atmosphere, sample thickness, hold temperature, which instrument, which sample geometry}. Run it before every experimental campaign.
    - **limitations**: Nested MC is biased and expensive; the EIG surface is noisy and often flat, so the ranking of designs can be unstable — report EIG with error bars and prefer a design only if the gap exceeds them. Greedy (myopic) sequential design is suboptimal; amortised policies (DAD/iDAD/RL) fix this but need a reliable simulator to train on.
    - **inputs_needed**: A calibrated-so-far posterior p(theta), a simulator fast enough to evaluate O(10^4-10^6) times (hence the surrogate), an explicit noise model per instrument, and cost weights per experiment type.
    - **source**: Huan & Marzouk, J. Comput. Phys. 232 (2013) 288, https://doi.org/10.1016/j.jcp.2012.08.013 ; Huan, Jagalur & Marzouk, Acta Numerica 33 (2024), https://doi.org/10.1017/S0962492924000023 ; Foster et al., https://arxiv.org/abs/1911.00294 ; DAD https://arxiv.org/abs/2103.02438 ; iDAD https://arxiv.org/abs/2111.02329 ; VSOED-RL https://arxiv.org/abs/2306.10430
  -
    - **name**: Direct transcription / orthogonal collocation for the furnace-programme OCP
    - **formulation**: Discretise t in [0, t_f] into N elements with Radau/Legendre collocation of degree K. Decision variables: states z_{i,k}, control T_i (piecewise constant or linear), plus t_f.
NLP: min J(z, T, t_f)
 s.t. collocation residuals  sum_k A_{kj} z_{i,k} - h_i * f(z_{i,j}, T_i) = 0
      continuity z_{i+1,0} = z_{i,K}
      path constraints g(z_{i,k}, T_i) <= 0  (P <= P_crit, |grad T| <= dT_max, dalpha/dt <= r_max)
      |T_{i+1} - T_i| / h_i <= beta_max ,  T_min <= T_i <= T_max .
Solve with IPOPT; exact first and second derivatives from CasADi's AD. Typical size: N = 200-500 elements, a few thousand variables — solves in seconds to minutes.
Alternative: direct multiple shooting (Bock–Plitt) — integrate on each interval with an adaptive stiff solver and match at the nodes; better for very stiff DAEM kinetics.
    - **when_to_use**: For the ODE-reduced (1-D or lumped) model. This is where you get the actual recommended cycle: a segmented T(t) that a furnace controller can be programmed with.
    - **limitations**: Only for the reduced model; the full 3-D FE problem needs adjoints instead. Stiff Arrhenius terms make the NLP badly scaled — scale all states and use log-temperature or 1/T as the control where possible. Non-convex: multi-start from several initial guesses (including a naive slow ramp) and report the best.
    - **inputs_needed**: Differentiable forward model in CasADi/JAX, furnace hardware limits, an explicit objective (min time, min energy, or a weighted combination).
    - **source**: Betts, J. Guid. Control Dyn. 21 (1998) 193, https://doi.org/10.2514/2.4231 ; Bock & Plitt, IFAC Proc. 17 (1984), https://doi.org/10.1016/S1474-6670(17)61205-9 ; CasADi, Math. Prog. Comp. 11 (2019) 1, https://doi.org/10.1007/s12532-018-0139-4 ; IPOPT, Math. Prog. 106 (2006) 25, https://doi.org/10.1007/s10107-004-0559-y
  -
    - **name**: Adjoint-based PDE-constrained optimisation of the 3-D cycle
    - **formulation**: Reduced functional: J_hat(u) = J(z(u), u) with z solving the transient PDE F(z, u) = 0, u = the discretised T(t) programme (or furnace boundary flux).
Adjoint: solve (dF/dz)^T * lambda = -(dJ/dz)^T BACKWARD in time; then dJ_hat/du = dJ/du + lambda^T * dF/du.
Cost: one forward solve + one adjoint solve per gradient, INDEPENDENT of dim(u) — so a 500-segment temperature programme costs the same as a 5-segment one.
Checkpointing (revolve) bounds the memory of storing the forward trajectory.
    - **when_to_use**: Once you care about DISTORTION of the actual printed lattice, not just density. Gradients of max-warpage or shape-error functionals w.r.t. the whole T(t) are only affordable this way.
    - **limitations**: SOVS is a strongly nonlinear viscous law and the Sandia report documents that warpage needs fine meshes, so each forward solve is expensive — budget hours per gradient. Automatic adjoints via dolfin-adjoint require the model to be written in FEniCS/Firedrake; a commercial FE code (Abaqus/Simufact/Netfabb) will force you to use finite differences or a surrogate instead.
    - **inputs_needed**: A FEniCS/Firedrake implementation of heat + SOVS, a differentiable objective (e.g. integrated squared deviation from the CAD shape).
    - **source**: Farrell, Ham, Funke & Rognes, SIAM J. Sci. Comput. 35 (2013) C369, https://doi.org/10.1137/120873558 ; Mitusch, Funke & Dokken, JOSS 4 (2019) 1292, https://doi.org/10.21105/joss.01292
  -
    - **name**: Multi-objective Pareto optimisation of the cycle
    - **formulation**: min_u [ f1 = t_cycle, f2 = (1 - rho_final), f3 = max shape deviation, f4 = energy = Integral P_furnace dt, f5 = residual carbon ]
 s.t. the same path and hardware constraints.
Evolutionary: NSGA-II/NSGA-III or R-NSGA-III in pymoo, run on the surrogate (needs ~10^4-10^5 evaluations).
Bayesian: qEHVI / qNEHVI acquisition in BoTorch when each evaluation is an expensive FE run (needs only ~50-200 evaluations); qNEHVI is the noise-robust version and supports parallel batches.
    - **when_to_use**: To present a defensible trade-off rather than a single cycle — 'you can have 97% density in 18 h or 99% in 46 h' is a much stronger paper result than one number. Also the right framing for the reviewer question 'why this cycle?'.
    - **limitations**: Evolutionary methods need a cheap surrogate; BO methods degrade above ~4-5 objectives and ~20 design variables. Scalarisation (weighted sum) misses non-convex parts of the front — use hypervolume-based methods.
    - **inputs_needed**: A parametrised cycle (e.g. 6-10 ramp/hold segments), the surrogate or simulator, reference point for hypervolume.
    - **source**: pymoo: Blank & Deb, IEEE Access 8 (2020) 89497, https://doi.org/10.1109/ACCESS.2020.2990567 ; BoTorch: https://arxiv.org/abs/1910.06403 ; qEHVI/qNEHVI: https://arxiv.org/abs/2006.05078
  -
    - **name**: Robust and chance-constrained cycle design under the posterior on binder parameters
    - **formulation**: Chance-constrained: min E_theta[J(u, theta)] s.t. Pr_theta[ g(z(u,theta)) <= 0 ] >= 1 - eps  (e.g. eps = 0.05 for 'the part cracks in <5% of plausible worlds').
Scenario approach: draw S i.i.d. samples theta_s ~ p(theta|data), enforce g(z(u, theta_s)) <= 0 for all s. The Calafiore–Campi bound gives the S needed for a distribution-free (1-eps, 1-beta) guarantee as a function of the number of decision variables.
gPC approach: expand z(t; theta) = sum_a z_a(t) Psi_a(theta); enforce E[g] + kappa * sqrt(Var[g]) <= 0 with kappa from a Cantelli/Chebyshev or Gaussian quantile — a smooth, differentiable surrogate constraint that plugs straight into the collocation NLP.
Multi-stage / scenario-tree NMPC (do-mpc) handles this recursively when feedback is available.
    - **when_to_use**: MANDATORY here. You will have a WIDE posterior on the binder kinetics and on green permeability. A cycle optimised at the posterior mean will crack parts. Design for the 95th percentile of the pressure constraint, not the mean.
    - **limitations**: Scenario approach can be very conservative and the sample count grows with the number of decision variables; gPC moment constraints are only exact for mild nonlinearity. Report the price of robustness explicitly (extra cycle hours vs reduction in failure probability) — that comparison is itself a paper figure.
    - **inputs_needed**: Posterior samples of theta from the calibration step; a defined acceptable failure probability eps.
    - **source**: Calafiore & Campi scenario approach, https://doi.org/10.1109/CDC.2007.4434039 ; Bergner & Kirches, Optim. Control Appl. Methods 38 (2017), https://doi.org/10.1002/oca.2329 ; Lefebvre, De Belie & Crevecoeur, OCAM 41 (2020), https://doi.org/10.1002/oca.2575 ; do-mpc (multi-stage robust NMPC), https://doi.org/10.1016/j.conengprac.2023.105676
  -
    - **name**: NMPC + Moving Horizon Estimation with in-situ signals
    - **formulation**: MHE (every sampling instant, window length N_e):
 min_{z_{-Ne}, w, theta} sum_{j} || y_j - h(z_j) ||^2_{R^-1} + || w_j ||^2_{Q^-1} + arrival cost
 s.t. z_{j+1} = F(z_j, T_j) + w_j
 — jointly re-estimating the binder state alpha and the slowly drifting parameters theta from TGA/load-cell mass, dilatometer strain, and off-gas partial pressures.
NMPC (every sampling instant, horizon N_p):
 min_{T_{0..Np-1}} sum_k L(z_k, T_k) + V_f(z_Np)
 s.t. dynamics, P <= P_crit, |dT/dt| <= beta_max, T <= T_max ; apply T_0, discard the rest, re-solve.
Economic NMPC variant: L = direct cost (time + energy) rather than a tracking error.
    - **when_to_use**: This is the step that converts 'a simulated optimal cycle' into 'a robust real process' and is the strongest novelty claim available for a paper: closed-loop, model-based debinding+sintering control for a metal LCM material with an unknown binder. Lombardo & Retzloff (2018) already published the process-control algorithm for the debinding half, so there is a citable precedent to build on.
    - **limitations**: Needs instrumented furnace hardware (in-situ balance, dilatometer, or quadrupole MS on the exhaust) — this is the main capital barrier. Real-time feasibility requires the reduced (ODE/MSC) model, not the FE model. State estimation of alpha from an integral mass signal is only observable if the mass resolution beats the total binder mass change.
    - **inputs_needed**: Instrumented furnace with an external set-point input; sampling rate ~0.1-1 Hz; a reduced model that runs faster than real time.
    - **source**: Lombardo & Retzloff, JACerS (2018), https://doi.org/10.1111/jace.15964 ; Rao, Rawlings & Mayne, IEEE TAC 48 (2003) 246, https://doi.org/10.1109/TAC.2002.808470 ; do-mpc, Control Eng. Practice 140 (2023) 105676, https://doi.org/10.1016/j.conengprac.2023.105676
- **open_questions**:
  - What is the actual binder mass fraction and solids loading of the Lithoz copper slurry? Everything downstream (internal pressure magnitude, shrinkage, permeability evolution) scales with it. If Lithoz will not disclose it, it must be measured: TGA to constant mass in inert atmosphere on a printed green sample gives the total organic fraction directly, and He pycnometry plus Archimedes on green and sintered parts closes the mass balance. This single measurement is probably the highest-information, lowest-cost experiment available and should be the first thing the BOED loop recommends.
  - Is the binder decomposition single-step or multi-step, and does E(alpha) vary? Run isoconversional (Friedman + KAS) analysis on >=3 heating rates FIRST. If E(alpha) is flat, a 2-parameter Arrhenius model suffices and the calibration is easy; if it drifts or steps, DAEM or a multi-step scheme is mandatory and the parameter count roughly triples. The answer determines the entire calibration architecture and cannot be assumed.
  - Does the binder decomposition mechanism CHANGE between inert (Ar), reducing (Ar/H2) and slightly oxidising atmospheres? Copper catalyses oxidation of organics, and copper oxide can act as an internal oxygen source. If the binder kinetics are atmosphere-dependent (very likely), the kinetic parameters theta become functions of pO2/pH2, and the atmosphere set-point becomes a second CONTROL variable in the OCP — substantially enlarging the design space and the paper's contribution.
  - Is the binder-removal regime for the specific LCM geometry diffusion-controlled or permeation(pressure)-controlled? Lombardo's 2016/2017 paper explicitly contrasts the two, and the minimum-time cycle differs qualitatively between them. The dimensionless group that discriminates them (roughly a Damkohler/permeation number combining decomposition rate, permeability, wall thickness and viscosity) should be evaluated first for the thinnest and thickest sections of the intended parts. Thin LCM lattice struts may be diffusion-limited and therefore tolerate much faster ramps than a monolithic test bar.
  - What is the green permeability K as a function of burn-off fraction for this material, and what is the green strength as a function of temperature? These are the two constitutive functions that set the pressure constraint, and neither exists for a proprietary slurry. Can K be inferred indirectly from cracking/no-cracking outcomes across a designed thickness series (simulation-based inference on a binary observable), or must it be measured directly by gas permeametry on partially debound discs?
  - Can a single apparent activation energy Q be used in a Master Sintering Curve for copper across the whole cycle, given that the oxide state of the powder surface changes during heating in H2? If not, the MSC low-fidelity model is invalid and the multi-fidelity hierarchy loses its cheap level — a piecewise MSC (one Q before oxide reduction, one after) or a coupled reduction+densification model would be needed. This is directly testable with 3-4 dilatometry runs in a fixed atmosphere.
  - Which quantity of interest actually needs the 3-D SOVS model? If the parts are geometrically simple and the shrinkage is near-isotropic, an MSC + isotropic scaling factor may predict final dimensions to within tolerance and the whole expensive FE/adjoint branch can be deferred. A quantitative decision criterion is needed: run the Burr-style calibration approach on a few benchmark geometries and measure the anisotropy and warpage; only invest in SOVS + adjoint optimisation if warpage exceeds the dimensional spec.
  - What is the measurement noise model and, crucially, the run-to-run reproducibility of the furnace and of the LCM print itself? A Bayesian calibration with an over-optimistic sigma will produce a falsely narrow posterior and a cycle that fails. Replicate prints and replicate runs are needed to separate instrument noise from part-to-part variability, and the latter should be modelled as a hierarchical random effect over prints, not folded into sigma.
  - Does the group have (or can they access) a furnace with an EXTERNAL set-point input and an in-situ signal (balance, dilatometer, or exhaust MS)? Without one, CRTA/RCS and NMPC are unavailable and the project reduces to open-loop optimal cycle design plus offline validation. This is a hard architectural fork and should be resolved before committing to the control branch.
  - Is the expected information gain surface over candidate experiments actually informative enough to discriminate designs, or is it flat? If EIG differences between candidate heating rates and geometries are within their Monte Carlo error bars, the BOED machinery adds cost without value and a simple factorial/space-filling design is better. This must be checked numerically on the prior predictive before committing to a sequential-design campaign.
  - How should model-form error be represented so that the calibrated model extrapolates to NEW geometries (which is the whole point)? Kennedy–O'Hagan discrepancy is indexed by x and does not extrapolate; embedded model error does, but is harder to fit. A concrete discriminating test: calibrate on two thicknesses, predict a third, and compare the two error representations' predictive coverage.
  - For the sintering half, is the correct objective maximum density, or is it minimum grain size at a target density? Copper coarsens readily, and the RCS literature's central claim is microstructure control rather than density. If grain size is a constraint, a grain-growth kinetic law must be added to the state vector and calibrated — adding parameters that will almost certainly be non-identifiable from dilatometry alone and requiring interrupted-quench metallography as a separate observable.
- **references**:
  -
    - **citation**: B. Lester, 'Verification of the Skorohod-Olevsky Viscous Sintering (SOVS) Model', SAND2017-12933R, Sandia National Laboratories, 2017.
    - **url**: https://doi.org/10.2172/1411315
    - **why**: OPEN ACCESS and fully read in this session. Gives the complete SOVS constitutive equations, the closure forms, a verified parameter table for 0.2 um ZnO, the closed-form free-sinter and sinter-forge porosity ODEs, and explicit time-step/mesh convergence guidance. Use it to verify your own SOVS implementation before calibrating copper.
  -
    - **citation**: E. A. Olevsky, 'Theory of sintering: from discrete to continuum', Mater. Sci. Eng. R 23 (1998) 41-100.
    - **url**: https://doi.org/10.1016/S0927-796X(98)00009-6
    - **why**: The canonical derivation of the continuum sintering theory that SOVS implements. Required citation for any paper using SOVS.
  -
    - **citation**: M. Reiterer, K. Ewsuk, J. Arguello, 'An Arrhenius-Type Viscosity Function to Model Sintering Using the Skorohod-Olevsky Viscous Sintering Model Within a Finite-Element Code', J. Am. Ceram. Soc. 89 (2006).
    - **url**: https://doi.org/10.1111/j.1551-2916.2006.01041.x
    - **why**: Replaces the quadratic eta0(T) in the Sandia parameter set with a physically meaningful Arrhenius form — the right choice for copper, and it reduces the viscosity parameter count from 3 to 2 (eta_ref, Q_eta), improving identifiability.
  -
    - **citation**: J. Balaguer, J. Tiscar, A. Saburit et al., 'Enhanced Skorohod-Olevsky viscous model incorporating microstructure evolution for finite element analysis of ceramic sintering', J. Eur. Ceram. Soc. 44 (2024).
    - **url**: https://doi.org/10.1016/j.jeurceramsoc.2024.05.035
    - **why**: Current state of the art for SOVS + grain growth coupling; relevant if grain size becomes a constrained objective for copper.
  -
    - **citation**: A. Burr, C. Lopez, J. Becerra et al., 'A calibration method to predict shape change during sintering: Application to 316L parts made by Metal Binder Jetting', Additive Manufacturing (2025).
    - **url**: https://doi.org/10.1016/j.addma.2025.104938
    - **why**: The closest recent methodological precedent for calibrating a sintering shape-change model against real metal AM parts. Read it before designing your own calibration benchmark geometries.
  -
    - **citation**: H. Su, D. L. Johnson, 'Master Sintering Curve: A Practical Approach to Sintering', J. Am. Ceram. Soc. 79 (1996) 3211.
    - **url**: https://doi.org/10.1111/j.1151-2916.1996.tb08097.x
    - **why**: Defines the MSC integral Theta(t,T) and the collapse of all heating schedules onto one curve. Your cheap low-fidelity model and your first-pass answer on peak temperature.
  -
    - **citation**: V. Pouchly, K. Maca, 'Master sintering curve: A practical approach to its construction', Sci. Sintering 42 (2010) 25.
    - **url**: https://doi.org/10.2298/SOS1001025P
    - **why**: Practical recipe for fitting Q by minimising the residual scatter across heating rates — i.e. the concrete inverse-problem procedure for the MSC.
  -
    - **citation**: S. J. Lombardo, 'Minimum Time Heating Cycles for Diffusion-Controlled Binder Removal from Ceramic Green Bodies', J. Am. Ceram. Soc. (2015).
    - **url**: https://doi.org/10.1111/jace.13284
    - **why**: Direct precedent for formulating debinding as a minimum-time optimal control problem. Full text was NOT accessible in this session — obtain it; it is the single most important paper for the cycle-design half of this project.
  -
    - **citation**: S. J. Lombardo, 'Minimum time heating cycles for diffusion- versus permeability-controlled binder removal from ceramic green bodies', J. Am. Ceram. Soc. (2017).
    - **url**: https://doi.org/10.1111/jace.14585
    - **why**: Tells you which transport regime you are in and how the optimal cycle differs between them — the first structural question to answer for LCM copper parts. Full text not accessed here.
  -
    - **citation**: S. J. Lombardo, D. G. Retzloff, 'A process control algorithm for reaction-diffusion minimum time heating cycles for binder removal from green bodies', J. Am. Ceram. Soc. (2018).
    - **url**: https://doi.org/10.1111/jace.15964
    - **why**: An explicit process-control (feedback) algorithm for optimal debinding — the published precedent your NMPC branch would extend to a metal LCM system. Full text not accessed here.
  -
    - **citation**: S. J. Lombardo, Z. C. Feng, 'Pressure Distribution During Binder Burnout in Three-dimensional Porous Ceramic Bodies with Anisotropic Permeability', J. Mater. Res. 17 (2002).
    - **url**: https://doi.org/10.1557/jmr.2002.0213
    - **why**: The 3-D internal-pressure model that supplies the crack constraint g(z) <= 0 in the optimal control problem, with anisotropic permeability — relevant because LCM layerwise builds ARE anisotropic.
  -
    - **citation**: J. Yun, S. J. Lombardo, 'Permeability of Green Ceramic Tapes as a Function of Binder Loading', J. Am. Ceram. Soc. 90 (2007).
    - **url**: https://doi.org/10.1111/j.1551-2916.2006.01444.x
    - **why**: Shows K(binder loading) explicitly. This is the constitutive function you must measure or infer for the Lithoz slurry; the paper also gives the measurement method.
  -
    - **citation**: R. Shende, S. J. Lombardo, 'Determination of Binder Decomposition Kinetics for Specifying Heating Parameters in Binder Burnout Cycles', J. Am. Ceram. Soc. 85 (2002).
    - **url**: https://doi.org/10.1111/j.1151-2916.2002.tb00172.x
    - **why**: The workflow from TGA kinetics to prescribed heating parameters — the exact task here, for a known binder. Read it as the template and then replace the single-step kinetics with a DAEM.
  -
    - **citation**: J. R. G. Song, J. R. G. Evans, M. J. Edirisinghe, 'Optimization of heating schedules in pyrolytic binder removal from ceramic moldings', J. Mater. Res. 15 (2000).
    - **url**: https://doi.org/10.1557/jmr.2000.0068
    - **why**: Explicit heating-schedule optimisation from the Evans/Edirisinghe school. Full text not accessed here; obtain it for the safe-heating-rate scaling law.
  -
    - **citation**: S. A. Matar, M. J. Edirisinghe, J. R. G. Evans, 'Modelling the removal of organic vehicle from ceramic or metal mouldings: The effect of gas permeation on the incidence of defects', J. Mater. Sci. 30 (1995) 3805.
    - **url**: https://doi.org/10.1007/BF01153938
    - **why**: Establishes the gas-permeation-to-defect link that justifies the pressure constraint. Note the title explicitly covers METAL mouldings, so it is directly on-point for copper.
  -
    - **citation**: L. C. Liau, C. Chiu, 'Optimal Heating Strategies of Polymer Binder Burnout Process Using Dynamic Optimization Scheme', Ind. Eng. Chem. Res. 44 (2005).
    - **url**: https://doi.org/10.1021/ie049143a
    - **why**: A dynamic-optimisation (optimal control) solution for binder burnout from the chemical-engineering literature — a second, independent formulation to benchmark yours against. Full text not accessed here.
  -
    - **citation**: X. Wang, W. Duan, Z. Chen et al., 'Uniform rate debinding for Si3N4 vat photopolymerization 3D printing green parts using a specific-stage stepwise heating process', Additive Manufacturing (2024).
    - **url**: https://doi.org/10.1016/j.addma.2024.104119
    - **why**: CRTA-style constant-rate debinding applied specifically to VAT PHOTOPOLYMERISED ceramic green parts — the nearest published analogue to what you must do with an LCM copper part. Full text not accessed here; this is a must-read.
  -
    - **citation**: J. Li, C. Zhang, R. Yin et al., 'DAEM kinetics analysis and finite element simulation of thermal debinding process for a gelcast SiAlON green body', Ceramics International 45 (2019).
    - **url**: https://doi.org/10.1016/j.ceramint.2019.01.118
    - **why**: The template for exactly the modelling approach recommended here: DAEM kinetics for a complex binder, coupled into a finite-element debinding simulation. Full text not accessed here.
  -
    - **citation**: T. Rijwani, P. Ramkumar, 'Thermal Debinding for Binder Burnout in Metal and Ceramic Processing', Heat Transfer Engineering (2024).
    - **url**: https://doi.org/10.1080/01457632.2024.2332111
    - **why**: Recent review (abstract verified here). Explicitly states that an inappropriate burnout cycle causes cracks, blistering, swell, distortion or breaking, and that ineffective debinding leaves residual binder that changes final properties — the plain-language justification for the whole project. Good source of a consolidated bibliography.
  -
    - **citation**: J. Rouquerol, 'Vacuum thermal analysis apparatus with controlled residual pressure and constant decomposition rate', in Thermal Analysis (1969).
    - **url**: https://doi.org/10.1016/B978-0-12-395733-7.50026-5
    - **why**: The origin of CRTA. Cite for priority when you claim your optimal cycle is a constant-rate trajectory.
  -
    - **citation**: S. Bordere, F. Rouquerol, J. Rouquerol, 'Kinetical possibilities of controlled transformation rate thermal analysis (CRTA)', J. Thermal Analysis 36 (1990).
    - **url**: https://doi.org/10.1007/BF01913412
    - **why**: The kinetic-analysis capability of CRTA, including the rate-jump method for model-free activation energy — i.e. CRTA as optimal experimental design, not just process control.
  -
    - **citation**: O. T. Sorensen, J. Rouquerol (eds), 'Sample Controlled Thermal Analysis: Origin, Goals, Multiple Forms, Applications and Future', Kluwer (2003).
    - **url**: https://doi.org/10.1007/978-1-4757-3735-6
    - **why**: The reference monograph. Chapter 5 ('SCTA and Ceramics', https://doi.org/10.1007/978-1-4757-3735-6_5) is the directly relevant one for debinding.
  -
    - **citation**: H. Palmour III, T. M. Hare, 'Rate Controlled Sintering Revisited', in Sintering '85 (1987).
    - **url**: https://doi.org/10.1007/978-1-4613-2851-3_2
    - **why**: The definitive statement of rate-controlled sintering, the sintering counterpart of CRTA and the basis for the sintering half of the cycle.
  -
    - **citation**: R. F. Speyer, L. Echiverri, C. Lee, 'A shrinkage rate-controlled sintering dilatometer', J. Mater. Sci. Lett. 11 (1992) 1089.
    - **url**: https://doi.org/10.1007/BF00730840
    - **why**: Hardware precedent: an actual dilatometer with shrinkage-rate feedback control. Read before specifying instrumentation for the closed-loop branch.
  -
    - **citation**: J. Wang, R. Raj, 'Estimate of the Activation Energies for Boundary Diffusion from Rate-Controlled Sintering of Pure Alumina...', J. Am. Ceram. Soc. 73 (1990).
    - **url**: https://doi.org/10.1111/j.1151-2916.1990.tb05175.x
    - **why**: Shows RCS doubles as a parameter-identification experiment. Supports the argument that the control strategy and the experimental design should be co-designed.
  -
    - **citation**: S. Vyazovkin, A. K. Burnham, J. M. Criado et al., 'ICTAC Kinetics Committee recommendations for performing kinetic computations on thermal analysis data', Thermochim. Acta 520 (2011) 1.
    - **url**: https://doi.org/10.1016/j.tca.2011.03.034
    - **why**: The standard your kinetics analysis must meet to be publishable. Companion papers: data collection (https://doi.org/10.1016/j.tca.2014.05.036), multi-step kinetics (https://doi.org/10.1016/j.tca.2020.178597), thermal decomposition (https://doi.org/10.1016/j.tca.2022.179384).
  -
    - **citation**: N. Koga, 'A review of the mutual dependence of Arrhenius parameters evaluated by the thermoanalytical study of solid-state reactions: The kinetic compensation effect', Thermochim. Acta 244 (1994) 1.
    - **url**: https://doi.org/10.1016/0040-6031(94)80202-5
    - **why**: The definitive review of the ln A - E compensation effect — the specific non-identifiability that will dominate your posterior geometry. Cite when justifying multiple heating rates and reparametrisation.
  -
    - **citation**: M. C. Kennedy, A. O'Hagan, 'Bayesian calibration of computer models', J. R. Stat. Soc. B 63 (2001) 425.
    - **url**: https://doi.org/10.1111/1467-9868.00294
    - **why**: The foundational model-discrepancy framework. Open-access PDF available via Oxford Academic.
  -
    - **citation**: K. Sargsyan, X. Huan, H. N. Najm, 'Embedded model error representation for Bayesian model calibration', Int. J. Uncertainty Quantification 9 (2019).
    - **url**: https://doi.org/10.1615/Int.J.UncertaintyQuantification.2019027384
    - **why**: The physically-admissible alternative to KO discrepancy, and the better choice for conservation-law models like binder burnout. Read this before defaulting to KO.
  -
    - **citation**: A. Raue, C. Kreutz, T. Maiwald et al., 'Structural and practical identifiability analysis of partially observed dynamical models by exploiting the profile likelihood', Bioinformatics 25 (2009) 1923.
    - **url**: https://doi.org/10.1093/bioinformatics/btp358
    - **why**: The reference method for practical identifiability of ODE models from sparse observations. Open-access PDF available. Directly transferable to debinding kinetics.
  -
    - **citation**: R. Boiger, J. Hasenauer, S. Hross, B. Kaltenbacher, 'Integration based profile likelihood calculation for PDE constrained parameter estimation problems', Inverse Problems 32 (2016) 125009.
    - **url**: https://doi.org/10.1088/0266-5611/32/12/125009
    - **why**: Extends profile likelihood to PDE-constrained problems, which is what you have once the 3-D transport/SOVS model is in the loop.
  -
    - **citation**: X. Huan, Y. M. Marzouk, 'Simulation-based optimal Bayesian experimental design for nonlinear systems', J. Comput. Phys. 232 (2013) 288.
    - **url**: https://arxiv.org/abs/1108.4146
    - **why**: OPEN ACCESS (arXiv). The EIG framework with PCE surrogates and stochastic approximation, demonstrated on combustion kinetics — the closest analogue to binder-decomposition kinetics. The template for choosing your next experiment.
  -
    - **citation**: X. Huan, J. Jagalur, Y. Marzouk, 'Optimal experimental design: Formulations and computations', Acta Numerica 33 (2024) 715.
    - **url**: https://doi.org/10.1017/S0962492924000023
    - **why**: The current comprehensive survey, including EIG estimation, discrete vs continuous design optimisation, and non-myopic sequential design policies. The single best entry point to modern OED.
  -
    - **citation**: A. Foster, M. Jankowiak, M. O'Meara et al., 'A Unified Stochastic Gradient Approach to Designing Bayesian-Optimal Experiments', arXiv:1911.00294.
    - **url**: https://arxiv.org/abs/1911.00294
    - **why**: Variational lower bounds on EIG that remove the nested Monte Carlo loop, making continuous design optimisation tractable. Implemented in Pyro.
  -
    - **citation**: A. Foster, D. R. Ivanova, I. Malik, T. Rainforth, 'Deep Adaptive Design: Amortizing Sequential Bayesian Experimental Design', arXiv:2103.02438.
    - **url**: https://arxiv.org/abs/2103.02438
    - **why**: Amortised sequential design — train a policy offline, then choose the next experiment in milliseconds. Relevant if the campaign runs over many months. Likelihood-free variant: arXiv:2111.02329.
  -
    - **citation**: P. Del Moral, A. Doucet, A. Jasra, 'Sequential Monte Carlo samplers', J. R. Stat. Soc. B 68 (2006) 411.
    - **url**: https://doi.org/10.1111/j.1467-9868.2006.00553.x
    - **why**: Tempered sampling for ridged/multimodal posteriors, with a free model-evidence estimate. The right sampler for Arrhenius compensation ridges.
  -
    - **citation**: J. Ching, Y.-C. Chen, 'Transitional Markov Chain Monte Carlo Method for Bayesian Model Updating, Model Class Selection, and Model Averaging', J. Eng. Mech. 133 (2007) 816.
    - **url**: https://doi.org/10.1061/(ASCE)0733-9399(2007)133:7(816)
    - **why**: Engineering-facing SMC variant, widely used for model updating; gives Bayes factors for choosing among competing binder-kinetics mechanisms.
  -
    - **citation**: L. Le Gratiet, J. Garnier, 'Recursive co-kriging model for design of computer experiments with multiple levels of fidelity', Int. J. Uncertainty Quantification 4 (2014) 365.
    - **url**: https://doi.org/10.1615/Int.J.UncertaintyQuantification.2014006914
    - **why**: The recursive formulation that makes multi-fidelity GP inference cheap, letting you fuse fast 1-D sintering models with slow 3-D FE runs.
  -
    - **citation**: A. Saltelli, P. Annoni, I. Azzini et al., 'Variance based sensitivity analysis of model output. Design and estimator for the total sensitivity index', Comput. Phys. Commun. 181 (2010) 259.
    - **url**: https://doi.org/10.1016/j.cpc.2009.09.018
    - **why**: The standard estimator design for total-order Sobol' indices and the source of the N(k+2) cost. What SALib implements.
  -
    - **citation**: M. D. Morris, 'Factorial Sampling Plans for Preliminary Computational Experiments', Technometrics 33 (1991) 161.
    - **url**: https://doi.org/10.1080/00401706.1991.10484804
    - **why**: Elementary-effects screening — the cheap first pass that culls your ~24 candidate parameters before any expensive analysis.
  -
    - **citation**: J. Herman, W. Usher, 'SALib: An open-source Python library for Sensitivity Analysis', J. Open Source Software 2 (2017) 97.
    - **url**: https://doi.org/10.21105/joss.00097
    - **why**: The practical tool for Morris, Sobol', FAST, PAWN, delta-MIM. See also SALib 2.0: https://doi.org/10.18174/sesmo.18155
  -
    - **citation**: J. Feinberg, H. P. Langtangen, 'Chaospy: An open source tool for designing methods of uncertainty quantification', J. Comput. Sci. 11 (2015) 46.
    - **url**: https://doi.org/10.1016/j.jocs.2015.08.008
    - **why**: Polynomial chaos and quadrature toolbox; the easiest route to sparse PCE surrogates and analytic Sobol' indices from PCE coefficients.
  -
    - **citation**: A. Olivier, D. G. Giovanis, B. S. Aakash et al., 'UQpy: A general purpose Python package and development environment for uncertainty quantification', J. Comput. Sci. 47 (2020) 101204.
    - **url**: https://doi.org/10.1016/j.jocs.2020.101204
    - **why**: Broad UQ toolbox covering sampling, surrogates, reliability, and Bayesian inference in one package. Current releases: v4.1 https://doi.org/10.1016/j.softx.2023.101561 , v4.2 https://doi.org/10.1016/j.softx.2025.102364
  -
    - **citation**: L. Swiler, M. Eldred, B. Adams, 'Dakota: Bridging Advanced Scalable Uncertainty Quantification Algorithms with Production Deployment', in Handbook of Uncertainty Quantification (2017).
    - **url**: https://doi.org/10.1007/978-3-319-12385-1_52
    - **why**: The DOE-grade non-intrusive driver for coupling UQ/optimisation to an external FE code — the pragmatic choice if the sintering model lives in a commercial solver you cannot differentiate.
  -
    - **citation**: O. Abril-Pla, V. Andreani, C. Carroll et al., 'PyMC: a modern, and comprehensive probabilistic programming framework in Python', PeerJ Comput. Sci. 9 (2023) e1516.
    - **url**: https://doi.org/10.7717/peerj-cs.1516
    - **why**: Primary Bayesian inference engine (NUTS, SMC, variational) with an ODE interface. Open access.
  -
    - **citation**: D. Phan, N. Pradhan, M. Jankowiak, 'Composable Effects for Flexible and Accelerated Probabilistic Programming in NumPyro', arXiv:1912.11554.
    - **url**: https://arxiv.org/abs/1912.11554
    - **why**: JAX-backed NUTS — the fastest practical route to gradient-based MCMC through a differentiable ODE solve (pair with diffrax for the DAEM/kinetics block).
  -
    - **citation**: D. Foreman-Mackey, D. W. Hogg, D. Lang, J. Goodman, 'emcee: The MCMC Hammer', PASP 125 (2013) 306.
    - **url**: https://doi.org/10.1086/670067
    - **why**: Gradient-free affine-invariant ensemble sampler; the robustness cross-check when the forward model is a black-box FE call. v3 JOSS paper: https://doi.org/10.21105/joss.01864
  -
    - **citation**: J. Boelrijk et al. / sbi developers, 'sbi reloaded: a toolkit for simulation-based inference workflows', arXiv:2411.17337.
    - **url**: https://arxiv.org/abs/2411.17337
    - **why**: Neural posterior/likelihood/ratio estimation for intractable likelihoods — the right tool when the only observation from a furnace run is a binary crack/no-crack outcome or a coarse distortion score.
  -
    - **citation**: J. A. E. Andersson, J. Gillis, G. Horn, J. B. Rawlings, M. Diehl, 'CasADi: a software framework for nonlinear optimization and optimal control', Math. Prog. Comput. 11 (2019) 1.
    - **url**: https://doi.org/10.1007/s12532-018-0139-4
    - **why**: The workhorse for building the collocation NLP with exact derivatives. Pair with IPOPT.
  -
    - **citation**: A. Wachter, L. T. Biegler, 'On the implementation of an interior-point filter line-search algorithm for large-scale nonlinear programming', Math. Prog. 106 (2006) 25.
    - **url**: https://doi.org/10.1007/s10107-004-0559-y
    - **why**: IPOPT — the NLP solver for the transcribed optimal control problem. Free, handles thousands of variables and path constraints.
  -
    - **citation**: F. Fiedler, B. Karg, L. Luken et al., 'do-mpc: Towards FAIR nonlinear and robust model predictive control', Control Eng. Practice 140 (2023) 105676.
    - **url**: https://doi.org/10.1016/j.conengprac.2023.105676
    - **why**: Ready-made multi-stage robust NMPC and moving-horizon estimation on top of CasADi/IPOPT — the fastest route to a closed-loop furnace controller prototype.
  -
    - **citation**: P. E. Farrell, D. A. Ham, S. W. Funke, M. E. Rognes, 'Automated Derivation of the Adjoint of High-Level Transient Finite Element Programs', SIAM J. Sci. Comput. 35 (2013) C369.
    - **url**: https://doi.org/10.1137/120873558
    - **why**: dolfin-adjoint: automatic adjoints for transient FE models, giving gradients of a distortion functional w.r.t. the whole temperature programme at O(1) extra cost. JOSS release paper: https://doi.org/10.21105/joss.01292
  -
    - **citation**: J. T. Betts, 'Survey of Numerical Methods for Trajectory Optimization', J. Guid. Control Dyn. 21 (1998) 193.
    - **url**: https://doi.org/10.2514/2.4231
    - **why**: The standard reference distinguishing direct transcription, collocation, single and multiple shooting, and indirect methods. Cite for the choice of transcription scheme.
  -
    - **citation**: H. G. Bock, K. J. Plitt, 'A Multiple Shooting Algorithm for Direct Solution of Optimal Control Problems', IFAC Proc. 17 (1984) 1603.
    - **url**: https://doi.org/10.1016/S1474-6670(17)61205-9
    - **why**: Direct multiple shooting — the better choice when the DAEM kinetics make the ODE very stiff and you want an adaptive integrator per interval. Parameter-estimation companion: https://doi.org/10.1007/978-3-319-23321-5_1
  -
    - **citation**: J. Blank, K. Deb, 'pymoo: Multi-Objective Optimization in Python', IEEE Access 8 (2020) 89497.
    - **url**: https://doi.org/10.1109/ACCESS.2020.2990567
    - **why**: NSGA-II/III and constraint handling for the cycle-time vs density vs distortion vs energy Pareto front, run on the surrogate.
  -
    - **citation**: M. Balandat, B. Karrer, D. R. Jiang et al., 'BoTorch: A Framework for Efficient Monte-Carlo Bayesian Optimization', arXiv:1910.06403.
    - **url**: https://arxiv.org/abs/1910.06403
    - **why**: Bayesian optimisation for expensive black-box simulators and for real experiments. Multi-objective acquisition qEHVI/qNEHVI: https://arxiv.org/abs/2006.05078
  -
    - **citation**: T. Akiba, S. Sano, T. Yanase et al., 'Optuna: A Next-generation Hyperparameter Optimization Framework', KDD 2019.
    - **url**: https://doi.org/10.1145/3292500.3330701
    - **why**: Pragmatic TPE-based optimiser with pruning; useful for quick parametric cycle searches and for tuning the surrogates, though inferior to BoTorch for genuinely expensive evaluations.
  -
    - **citation**: G. Calafiore, M. C. Campi, 'New results on the scenario design approach', IEEE CDC 2007.
    - **url**: https://doi.org/10.1109/CDC.2007.4434039
    - **why**: Distribution-free sample-complexity bounds for enforcing chance constraints by sampling the posterior — the rigorous way to say 'this cycle cracks fewer than 5% of parts'.
  -
    - **citation**: L. Bergner, C. Kirches, 'The polynomial chaos approach for reachable set propagation with application to chance-constrained nonlinear optimal control under parametric uncertainties', Optim. Control Appl. Methods 38 (2017).
    - **url**: https://doi.org/10.1002/oca.2329
    - **why**: Smooth, differentiable chance constraints via gPC that plug directly into the collocation NLP — the practical alternative to scenario sampling.
  -
    - **citation**: E. Adeli, B. Rosic, H. G. Matthies et al., 'Comparison of Bayesian Methods on Parameter Identification for a Viscoplastic Model with Damage', Metals 10 (2020) 876.
    - **url**: https://doi.org/10.3390/met10070876
    - **why**: OPEN ACCESS, and a close methodological analogue: Bayesian identification of a viscoplastic constitutive model from sparse mechanical data. Useful as a template for the SOVS calibration write-up.
  -
    - **citation**: C. C. Rao, J. B. Rawlings, D. Q. Mayne, 'Constrained state estimation for nonlinear discrete-time systems: stability and moving horizon approximations', IEEE Trans. Autom. Control 48 (2003) 246.
    - **url**: https://doi.org/10.1109/TAC.2002.808470
    - **why**: The theory behind moving-horizon estimation, which is how you infer the unobserved binder state alpha online from a mass or dilatometer signal.
  -
    - **citation**: B. Jones, J. Wang, B. Tai, 'Debinding and sintering of copper powder material extrusion parts with a polylactide binder', J. Manufacturing Processes (2026).
    - **url**: https://doi.org/10.1016/j.jmapro.2026.01.072
    - **why**: Copper-specific debind+sinter data from a comparable sacrificial-polymer route. The nearest available source of copper densification and residual-carbon numbers; obtain the full text. Not read in this session.
  -
    - **citation**: A. Hofer, A. Kocjan, R. Bermejo et al., 'High-strength lithography-based additive manufacturing of ceramic components with rapid sintering', Additive Manufacturing 59 (2022) 103141.
    - **url**: https://doi.org/10.1016/j.addma.2022.103141
    - **why**: LCM-specific thermal post-processing including rapid sintering; useful for establishing what ramp rates are actually achievable on LCM green bodies and for framing your contribution against LCM practice.
  -
    - **citation**: L. Bezek, R. Wilkerson et al., 'Evolution of Debinding and Sintering of a Silica-Based Ceramic using Vat Photopolymerization Additive Manufacturing', Additive Manufacturing (2025).
    - **url**: https://doi.org/10.1016/j.addma.2025.104795
    - **why**: Recent, highly-cited-for-its-age study tracking debinding AND sintering evolution for a VPP ceramic — the closest published experimental methodology to what you need to replicate for copper. Not read in this session.