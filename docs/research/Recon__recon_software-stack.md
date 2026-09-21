- **summary**: The single most important finding is that the exact simulation stack this project needs already exists, open-source and MIT-licensed: **PUMA (Powder Utilization Modeling Application)** from ORNL's Applied Material Modeling group (github.com/applied-material-modeling/puma), published as Tran, Kounouho, Du, Sultana, Messner & Hu, "PUMA: A scalable framework for simulating powder post-processing in advanced manufacturing," Advances in Engineering Software (2026), DOI 10.1016/j.advengsoft.2026.104216. PUMA = MOOSE (FEM, four coupled PDEs: Darcy mass conservation in porous media, an L2-projection for pore pressure, energy conservation, linear-momentum balance) + NEML2 (batched, GPU-capable, auto-differentiated constitutive library, MIT). It explicitly targets *curing → debinding/pyrolysis → sintering → infiltration → solidification* and predicts distortion, residual stress and reaction-completion fraction. Its `examples/pyrolysis/{1D,2D,3D}` plus `examples/pyrolysis/material_calibration/TGA.i` are a working binder-burnout pipeline: an `ArrheniusParameter` rate coefficient feeding a `ContractingGeometry` reaction model for conversion α, with mass fractions of binder (w_b), char (w_s/w_c), gas (w_gcp) and open-pore fraction φ_op integrated by backward/forward Euler, composite density/c_p/k built by volume-fraction mixing, and a reaction heat source fed back into MOOSE's temperature kernels (`PumaCoupledTimeDerivative`, `PumaCoupledDiffusion`, `CoupledMaterialSource`). The calibration path is `pyzag` (MIT, adjoint sensitivities for recursive/implicit time-integrated models in PyTorch) driving NEML2 models against TGA curves — i.e. the unknown Lithoz binder chemistry can be handled as an *inverse problem* on a lumped multi-reaction kinetic model rather than requiring the recipe. `CoBRA` (MIT, Karhunen–Loève random-field generation from CT imagery) seeds spatially-correlated porosity ICs from micro-CT.

For the sintering half, no open-source code ships a ready SOVS/Olevsky continuum model. The nearest reusable object is MOOSE's `ADViscoplasticityStressUpdate` + `ADComputeMultiplePorousInelasticStress`, which implement Gurson–Tvergaard–Needleman and Leblond–Perrin–Suquet rate-dependent porous viscoplasticity with porosity evolution ḟ = (1−f)tr(Ė). Converting this into a sintering model is a modest modification (add sintering stress as a hydrostatic offset and let f decrease), not a rewrite. MOOSE also exposes `AbaqusUMATStress`, which compiles and runs a standard Abaqus UMAT verbatim inside MOOSE — so any SOVS UMAT written for the literature route (Reiterer, Ewsuk & Argüello, JACerS 2006, DOI 10.1111/j.1551-2916.2006.01041.x) is portable between Abaqus and MOOSE with no code change. This is the single best architectural hedge.

Microstructural/parameter-generating codes: **hpsint** (github.com/hpsint/hpsint, GPL-3.0, deal.II matrix-free, Ivannikov/Munch/Kronbichler/Ebel, Euro PM2023 DOI 10.59499/ep235764034) does large-scale 3D phase-field solid-state sintering of *metallic* powders with distributed grain tracking and graph colouring — the most mature open sintering phase-field code. MOOSE's `phase_field` module ships `GrandPotentialSinteringMaterial` (Greenquist/Tonks/Aagesen/Zhang, Comput. Mater. Sci. 2020, DOI 10.1016/j.commatsci.2019.109288) with parabolic/dilute/ideal solid free-energy options, plus `ElectrochemicalSinteringMaterial`. **PRISMS-PF** (LGPL-2.1, deal.II, >10⁹ DOF) has no sintering app out of the box. For DEM: **dp3D** (github.com/Xtof38/sourcedp3D_public, Fortran, C.L. Martin, SIMAP Grenoble) is the canonical particle-level sintering DEM, recently extended to level-set non-spherical particles (JTCAM DOI 10.46298/jtcam.13721, data Zenodo 10.5281/zenodo.15168970). LIGGGHTS/LAMMPS have cohesion models but no validated sintering contact law. **RefraSin** (MIT, Zenodo 10.5281/zenodo.18455089, M. Weiner, TU Bergakademie Freiberg) is a sharp-interface thermodynamic-extremal-principle alternative claimed faster than phase-field. **MALAMUTE** (idaholab/malamute, LGPL-2.1) does engineering-scale electric-field-assisted sintering (Joule heating, thermal/electrical contact) — useful furnace-scale machinery even if the process here is pressureless.

Supporting stack: pycalphad 0.11.2 (MIT), OpenCalphad (GPL-3, Fortran, OCASI C binding), Cantera 3.2.0 (BSD-3) and `thermo` 0.6.1 (MIT) for Cu–O–C–H gas equilibria; gmsh 4.15.2 (GPLv2+), meshio 5.3.5, pygalmesh 0.10.7 (GPL-3, CGAL), PyVista 0.49.0, trimesh 5.1.0, porespy 3.1.1 and NASA PuMA v3 (NOSA, micro-CT → effective k/τ/κ) for imaging and meshing; DVC 3.67.1, MLflow 3.16.1, pydantic 2.13.5, h5py/xarray for provenance; lmfit, emcee, PyMC, UQpy, Dakota and MOOSE's own `optimization` (PETSc/TAO adjoint) + `stochastic_tools` modules for calibration and UQ.

Verification practice is well-standardised: Method of Manufactured Solutions (Salari & Knupp, SAND, DOI 10.2172/759450; Roache, J. Fluids Eng. 2002, DOI 10.1115/1.1436090) for code verification of each kernel, grid/time convergence studies for solution verification, ASME V&V 10 (computational solid mechanics; overview DOI 10.1007/s00366-007-0072-z) for the validation hierarchy, and the ICTAC Kinetics Committee series (DOIs 10.1016/j.tca.2011.03.034, 10.1016/j.tca.2014.05.036, 10.1016/j.tca.2020.178597, 10.1016/j.tca.2022.179384) as the mandatory protocol for the TGA-based binder kinetics — multiple heating rates, isoconversional first, model-fitting second.
- **key_facts**:
  -
    - **fact**: PUMA (ORNL, github.com/applied-material-modeling/puma) is an MIT-licensed MOOSE+NEML2 framework explicitly built to simulate powder post-processing: curing, pyrolysis/debinding, sintering, infiltration, solidification. It predicts distortion, residual stress and reaction-completion fraction. Governing physics = Darcy flow mass conservation + L2-projection for pore pressure + energy conservation + linear momentum balance.
    - **source**: Tran H., Kounouho S., Du M., Sultana F., Messner M.C., Hu T., 'PUMA: A scalable framework for simulating powder post-processing in advanced manufacturing', Advances in Engineering Software (2026), DOI 10.1016/j.advengsoft.2026.104216; repo README https://github.com/applied-material-modeling/puma
    - **confidence**: high
  -
    - **fact**: PUMA ships a complete binder-pyrolysis example chain (examples/pyrolysis/1D, 2D, 3D) plus a TGA parameter-calibration input (examples/pyrolysis/material_calibration/TGA.i). This is directly reusable for an unknown proprietary binder because it treats the kinetics as a calibration target, not a known chemistry.
    - **source**: https://github.com/applied-material-modeling/puma (file listing via GitHub code search; TGA.i and neml2/neml2_material.i fetched raw)
    - **confidence**: high
  -
    - **fact**: NEML2 (github.com/applied-material-modeling/neml2, MIT, ~50 stars, ~349 commits on main) is a PyTorch/LibTorch-backed constitutive library with batched CPU/GPU evaluation, first-class automatic differentiation, operator fusion and lazy evaluation. Modules cover solid mechanics (incl. crystal plasticity), chemical reactions, phase-field fracture, porous flow, finite volume and KWN precipitation kinetics. Reported >400x GPU speedup vs CPU on a crystal-plasticity benchmark (68 s GPU vs ~15,000 s CPU).
    - **source**: https://github.com/applied-material-modeling/neml2 README
    - **confidence**: high
  -
    - **fact**: MOOSE's solid_mechanics module contains ADViscoplasticityStressUpdate implementing Gurson-Tvergaard-Needleman (rate-independent) and Leblond-Perrin-Suquet (rate-dependent) porous viscoplasticity, used with ADComputeMultiplePorousInelasticStress to evolve porosity. Porosity evolution is f_dot = (1-f) tr(E_dot). This is the closest built-in object to a continuum sintering constitutive model; it needs a sintering-stress hydrostatic offset added.
    - **source**: https://raw.githubusercontent.com/idaholab/moose/next/modules/solid_mechanics/doc/content/source/materials/ADViscoplasticityStressUpdate.md
    - **confidence**: high
  -
    - **fact**: MOOSE can execute standard Abaqus UMAT Fortran subroutines directly via AbaqusUMATStress, including PNEWDT-driven adaptive time stepping and multi-step analysis. A SOVS UMAT is therefore portable between Abaqus and MOOSE unchanged - a strong hedge against framework lock-in.
    - **source**: https://raw.githubusercontent.com/idaholab/moose/next/modules/solid_mechanics/doc/content/source/materials/abaqus/AbaqusUMATStress.md
    - **confidence**: high
  -
    - **fact**: MOOSE phase_field module ships GrandPotentialSinteringMaterial (parabolic, dilute-solution and ideal-solution solid free-energy variants, with mass-conservation option) and ElectrochemicalSinteringMaterial, with regression tests SinteringBase.i, SinteringIdeal.i, SinteringDilute.i, SinteringParabolic.i, GrandPotentialSintering_test.i.
    - **source**: GitHub code search repo:idaholab/moose 'Sintering in:path'; https://raw.githubusercontent.com/idaholab/moose/next/modules/phase_field/doc/content/source/materials/GrandPotentialSinteringMaterial.md
    - **confidence**: high
  -
    - **fact**: hpsint (github.com/hpsint/hpsint) is a GPL-3.0, deal.II-based, matrix-free, Jacobian-free phase-field sintering code for large-scale 3D solid-state sintering of metallic powders (hundreds-to-thousands of particles), using Wang's classical phase-field model with distributed grain tracking, graph colourisation to minimise order parameters, and problem-specific preconditioners. ~3,445 commits. Developers: V. Ivannikov, P. Munch, M. Kronbichler, D. Paukner, M. Schreter.
    - **source**: https://github.com/hpsint/hpsint ; Ivannikov, Munch, Kronbichler, Ebel, Euro PM2023 Proceedings, DOI 10.59499/ep235764034
    - **confidence**: high
  -
    - **fact**: dp3D (github.com/Xtof38/sourcedp3D_public, Fortran, SIMAP / Univ. Grenoble Alpes, C.L. Martin group) is the canonical DEM sintering code; recently extended with a level-set formulation and optimisation-based contact detection for non-spherical particles. No explicit licence file identified in the repo.
    - **source**: https://github.com/Xtof38/sourcedp3D_public ; Paredes-Goyes, Jauffres, Martin, JTCAM DOI 10.46298/jtcam.13721 ; dataset Zenodo 10.5281/zenodo.15168970 (CC-BY-4.0)
    - **confidence**: medium
  -
    - **fact**: LIGGGHTS/LAMMPS have no validated sintering contact law out of the box - they provide cohesion/bonded-particle models only. LIGGGHTS-PUBLIC (CFDEMproject) is GPL; the vendor has superseded it with commercial Aspherix. For sintering DEM, dp3D is the right tool, not LIGGGHTS.
    - **source**: https://github.com/CFDEMproject/LIGGGHTS-PUBLIC (repo description); absence confirmed by GitHub repo search - marked partly inferential
    - **confidence**: medium
  -
    - **fact**: RefraSin (Institute-of-Metal-Forming/refrasin, MIT, v1.0.0 published Feb 2026, author Max Weiner, TU Bergakademie Freiberg) simulates surface and grain-boundary diffusion during sintering with a sharp-interface formulation solved by a thermodynamic extremal principle; claimed higher efficiency than phase-field at equal versatility.
    - **source**: Zenodo record 10.5281/zenodo.18455089
    - **confidence**: high
  -
    - **fact**: MALAMUTE (github.com/idaholab/malamute, LGPL-2.1, ~2,057 commits) is INL's MOOSE-based advanced-manufacturing app. It has a full engineering-scale Electric-Field Assisted Sintering (EFAS/SPS) tutorial with Joule heating, graphite/steel tooling thermal+electrical contact (ThermalContactCondition interface kernel), temperature-dependent graphite and stainless conductivity/expansion materials, plus melt-pool level-set kernels for laser AM.
    - **source**: https://github.com/idaholab/malamute ; https://raw.githubusercontent.com/idaholab/malamute/main/doc/content/tutorials/efas/introduction/tutorial_overview.md
    - **confidence**: high
  -
    - **fact**: ORNL 'kelvin' (github.com/ORNL/kelvin) is described as a multiphysics sintering simulation code built on MFEM, ~108 commits, 7 stars, last meaningful activity Feb 2025. Low adoption; treat as a reference, not a base.
    - **source**: https://github.com/ORNL/kelvin
    - **confidence**: medium
  -
    - **fact**: pyzag (applied-material-modeling/pyzag, MIT, ~106 commits) solves recursive implicit equations f(x_{i-1}, x_i; p)=0 in PyTorch with batched nonlinear solvers and ADJOINT parameter sensitivities (far more memory-efficient than naive autodiff), and integrates with Pyro for stochastic/Bayesian variants. PUMA pins pyzag 2.0.0 and uses neml2.pyzag.NEML2PyzagModel for material calibration.
    - **source**: https://github.com/applied-material-modeling/pyzag ; PUMA README installation section
    - **confidence**: high
  -
    - **fact**: CoBRA (github.com/skounouho/puma-cobra, MIT, Python, ~134 commits) = 'Computed-tomography Based Random-field Approximation'. Five-stage pipeline (preprocess/Gaussianise -> covariance kernel fit -> eigen-factorisation -> sample -> postprocess) producing Karhunen-Loeve random-field realisations from CT imagery, used by PUMA to seed spatially correlated porosity initial conditions.
    - **source**: https://github.com/skounouho/puma-cobra ; PUMA README
    - **confidence**: high
  -
    - **fact**: NASA PuMA v3 (github.com/nasa/puma, NASA Open Source Agreement, C++ core with pumapy Python bindings, conda binaries; 2022 NASA Software of the Year) computes from micro-CT: porosity, volume fractions, pore diameter, specific surface area, thermal and electrical conductivity, diffusivity, tortuosity, material orientation, elastic properties and permeability. NOTE: unrelated to ORNL PUMA despite the name collision.
    - **source**: https://github.com/nasa/puma
    - **confidence**: high
  -
    - **fact**: MOOSE is LGPL-2.1, C++, built-in mesh adaptivity, automatically parallel with largest reported runs >100,000 CPU cores; PETSc-based nonlinear solvers; modules include solid_mechanics, heat_transfer, porous_flow, phase_field, chemical_reactions, contact, XFEM, optimization (PETSc/TAO PDE-constrained inverse problems) and stochastic_tools.
    - **source**: https://github.com/idaholab/moose ; module index .md files fetched from raw.githubusercontent.com/idaholab/moose/next
    - **confidence**: high
  -
    - **fact**: DOLFINx (FEniCSx) is LGPL-3.0-or-later, C++ core with Python bindings, MPI-parallel via PETSc, and ships NO solid-mechanics/plasticity constitutive library - every sintering constitutive law would have to be written from scratch (or via the external dolfinx-external-operator / MFront-MGIS route).
    - **source**: https://github.com/FEniCS/dolfinx
    - **confidence**: high
  -
    - **fact**: Kratos Multiphysics is BSD-4, v10.4.0, ~111,628 commits, C++ with Python interface. Ships StructuralMechanicsApplication, ConstitutiveLawsApplication (plasticity, damage, anisotropy, viscoelasticity, composites), DEMApplication, FluidDynamics, FSI, ContactStructuralMechanics, Meshing, Trilinos/Metis. No sintering model out of the box.
    - **source**: https://github.com/KratosMultiphysics/Kratos
    - **confidence**: high
  -
    - **fact**: PRISMS-PF v3.0.0 is LGPL-2.1, deal.II matrix-free, scales past 10^9 DOF with adaptive meshing and near-ideal scaling over 1000+ processors. Built-in apps are precipitate evolution, grain growth and solidification - there is NO sintering application shipped.
    - **source**: https://github.com/prisms-center/phaseField ; DeWitt et al., npj Computational Materials (2020)
    - **confidence**: high
  -
    - **fact**: SfePy v2026.2 (BSD) is pure-Python FEM with ~838 stars; suitable for rapid prototyping of a 1D/2D sintering constitutive test bed but not for production 3D distortion runs.
    - **source**: https://pypi.org/pypi/sfepy/json ; https://github.com/sfepy/sfepy
    - **confidence**: high
  -
    - **fact**: solids4foam (github.com/solids4foam/solids4foam, ~117 stars) provides finite-volume solid mechanics and FSI inside OpenFOAM with PETSc coupling. OpenFOAM's strength here is the gas-phase/furnace-atmosphere CFD, not the solid sintering mechanics.
    - **source**: https://github.com/solids4foam/solids4foam
    - **confidence**: medium
  -
    - **fact**: Commercial sinter-distortion tools exist (Simufact Additive sintering module, Autodesk Netfabb Simulation, Desktop Metal Live Sinter, Ansys Additive, GeonX Virfac, DEFORM). Their vendor pages were blocked (HTTP 403/404) during this research, so specific solver/calibration claims could not be verified.
    - **source**: unverified
    - **confidence**: low
  -
    - **fact**: Peer-reviewed precedent for the target workflow in metal binder jetting exists: Sadeghi Borujeni, Shad, Abburi Venkata, Guenther, Ploshikhin, 'Numerical simulation of shrinkage and deformation during sintering in metal binder jetting with experimental validation', Materials & Design (2022); and Zhang K. et al., 'Numerical simulation and experimental measurement of pressureless sintering of stainless steel part printed by Binder Jetting AM', Additive Manufacturing (2021).
    - **source**: DOI 10.1016/j.matdes.2022.110490 ; DOI 10.1016/j.addma.2021.102330
    - **confidence**: high
  -
    - **fact**: Direct precedent for the LCM/vat-photopolymerisation debinding+sintering evolution study exists: Bezek, Wilkerson, Chad, Quintana, Patterson, Adhikari, Lee, 'Evolution of debinding and sintering of a silica-based ceramic using vat photopolymerization additive manufacturing', Additive Manufacturing (2025).
    - **source**: DOI 10.1016/j.addma.2025.104795
    - **confidence**: high
  -
    - **fact**: The ICTAC Kinetics Committee has issued a five-part recommendation series that defines the accepted protocol for extracting kinetics from TGA - this is the standard a reviewer will hold the binder-kinetics work to.
    - **source**: DOIs 10.1016/j.tca.2011.03.034 (computations), 10.1016/j.tca.2014.05.036 (data collection), 10.1016/j.tca.2020.178597 (multi-step), 10.1016/j.tca.2022.179384 (thermal decomposition), 10.1016/j.tca.2022.179243 (polymerisation)
    - **confidence**: high
  -
    - **fact**: ASME V&V 10 (Guide for Verification and Validation in Computational Solid Mechanics, originally PTC 60/V&V 10) is the applicable validation-hierarchy standard; V&V 20 covers CFD/heat transfer and V&V 40 covers medical devices. Exact current edition years could not be verified (ASME pages returned 403/404).
    - **source**: Overview paper: Schwer L.E., 'An overview of the PTC 60/V&V 10: guide for verification and validation in computational solid mechanics', Engineering with Computers (2007), DOI 10.1007/s00366-007-0072-z; edition years unverified
    - **confidence**: medium
  -
    - **fact**: Method of Manufactured Solutions is the accepted code-verification technique and has direct precedent for conjugate heat transfer and multiphase scalar transport - i.e. for exactly the kernels in a debinding model.
    - **source**: Salari & Knupp, 'Code Verification by the Method of Manufactured Solutions', SAND2000-1444, DOI 10.2172/759450; Roache, J. Fluids Eng. 124(1), DOI 10.1115/1.1436090; Veeraragavan et al., J. Comput. Phys. 2016, DOI 10.1016/j.jcp.2015.12.004
    - **confidence**: high
  -
    - **fact**: Dakota (Sandia) remains the reference external UQ/calibration driver for black-box FE codes; MOOSE additionally has a native optimization module using PETSc/TAO for PDE-constrained (adjoint) inverse problems and a stochastic_tools module for sampling/surrogates.
    - **source**: Dakota: DOI 10.2172/1630693 (2020 manual); MOOSE optimization module index.md from raw.githubusercontent.com/idaholab/moose/next
    - **confidence**: high
- **numbers**:
  -
    - **quantity**: Char yield Y of the calibrated binder pyrolysis reaction in PUMA's TGA calibration example
    - **value**: 0.5835777126099713
    - **units**: dimensionless (mass of char formed per unit mass of binder consumed)
    - **context**: PUMA demo binder (phenolic-resin-like), fitted to a TGA curve; NOT a copper-slurry binder. Use as an order-of-magnitude template and a working code path, not as a value for the Lithoz binder.
    - **source**: https://raw.githubusercontent.com/applied-material-modeling/puma/main/examples/pyrolysis/material_calibration/TGA.i
  -
    - **quantity**: Reaction order n (contracting-geometry model) in PUMA TGA calibration
    - **value**: 1.0
    - **units**: dimensionless
    - **context**: Same demo binder; ContractingGeometry reaction-rate model with conversion degree alpha
    - **source**: https://raw.githubusercontent.com/applied-material-modeling/puma/main/examples/pyrolysis/material_calibration/TGA.i
  -
    - **quantity**: Arrhenius pre-exponential k0 in PUMA TGA calibration
    - **value**: 0.04210147513030456
    - **units**: s^-1 (units implied by the ODE; not stated explicitly in the file)
    - **context**: Demo binder pyrolysis; paired with Q below. Units inferred, flag as such.
    - **source**: https://raw.githubusercontent.com/applied-material-modeling/puma/main/examples/pyrolysis/material_calibration/TGA.i
  -
    - **quantity**: Apparent activation energy Q in PUMA TGA calibration
    - **value**: 21191.61425138572
    - **units**: J/mol
    - **context**: Demo binder pyrolysis (~21.2 kJ/mol - very low, consistent with a single lumped apparent step rather than a physical bond-scission energy). Real photopolymer binders typically give 100-250 kJ/mol; expect the Lithoz binder to be far higher.
    - **source**: https://raw.githubusercontent.com/applied-material-modeling/puma/main/examples/pyrolysis/material_calibration/TGA.i ; the 100-250 kJ/mol comparison range is unverified
  -
    - **quantity**: Ideal gas constant R used
    - **value**: 8.31446261815324
    - **units**: J/(mol K)
    - **context**: CODATA value hard-coded in the PUMA TGA input
    - **source**: https://raw.githubusercontent.com/applied-material-modeling/puma/main/examples/pyrolysis/material_calibration/TGA.i
  -
    - **quantity**: Reference densities in PUMA's NEML2 pyrolysis material model (binder / char / pyrolyzate-solid)
    - **value**: 1250 / 2100 / 3210
    - **units**: kg/m^3
    - **context**: Demo phenolic+SiC-like system, not copper. For a Cu system the solid reference density would be 8960 kg/m^3 (Cu, room T). Values read from a summarised fetch of neml2_material.i, not the raw file.
    - **source**: https://raw.githubusercontent.com/applied-material-modeling/puma/main/examples/pyrolysis/1D/neml2/neml2_material.i (read via summarising fetch)
  -
    - **quantity**: Reference thermal conductivities in PUMA's NEML2 pyrolysis model (binder / char / pyrolyzate)
    - **value**: 279 / 150 / 380
    - **units**: W/(m K)
    - **context**: Demo values; the '279 W/mK for binder' is physically implausible for a polymer and is almost certainly a placeholder or a different phase assignment. Do not reuse.
    - **source**: https://raw.githubusercontent.com/applied-material-modeling/puma/main/examples/pyrolysis/1D/neml2/neml2_material.i (read via summarising fetch) - value plausibility flagged, treat as unverified
  -
    - **quantity**: Heat of reaction coefficient in PUMA's NEML2 pyrolysis model
    - **value**: -3.318e8
    - **units**: J per unit (scaling on reaction rate; exact normalisation not stated in the fetched summary)
    - **context**: Demo binder; sign negative = endothermic sink in their convention. Units/normalisation unverified.
    - **source**: https://raw.githubusercontent.com/applied-material-modeling/puma/main/examples/pyrolysis/1D/neml2/neml2_material.i (read via summarising fetch)
  -
    - **quantity**: Heating rate and temperature window in PUMA's 1D pyrolysis demo
    - **value**: dTdt = 10 K/min, T0 = 300 K, Tmax = 1100 K, domain 2.0 m, nx = 100, dt = 20 s
    - **units**: mixed
    - **context**: Demonstrates the ramp-and-hold driver pattern (PiecewiseLinear function -> FunctionDirichletBC) and IterationAdaptiveDT with optimal_iterations=7. Directly reusable as the debinding-cycle driver skeleton; the 2 m domain is a demo artefact.
    - **source**: https://raw.githubusercontent.com/applied-material-modeling/puma/main/examples/pyrolysis/1D/pyrolysis.i
  -
    - **quantity**: MOOSE demonstrated parallel scale
    - **value**: >100,000
    - **units**: CPU cores
    - **context**: Largest reported MOOSE runs; relevant to whether full-part 3D sinter-distortion runs are feasible on a cluster
    - **source**: https://github.com/idaholab/moose README
  -
    - **quantity**: NEML2 GPU speedup on a crystal-plasticity benchmark
    - **value**: ~220x wall-clock (68 s GPU vs ~15,000 s CPU), described as >400x in the README
    - **units**: dimensionless speedup
    - **context**: Constitutive-update throughput only, not full FE solve. Indicates the constitutive layer will not be the bottleneck for a many-parameter calibration sweep.
    - **source**: https://github.com/applied-material-modeling/neml2 README
  -
    - **quantity**: PRISMS-PF demonstrated problem size
    - **value**: >1e9
    - **units**: degrees of freedom
    - **context**: deal.II matrix-free phase-field; near-ideal scaling over 1000+ processors
    - **source**: https://github.com/prisms-center/phaseField
  -
    - **quantity**: Kratos Multiphysics current version and repository scale
    - **value**: v10.4.0, ~111,628 commits, ~1.4k stars
    - **units**: -
    - **context**: Maturity indicator for a BSD-4 alternative to MOOSE
    - **source**: https://github.com/KratosMultiphysics/Kratos
  -
    - **quantity**: hpsint repository scale
    - **value**: ~3,445 commits, 15 stars, ~67 open issues
    - **units**: -
    - **context**: Actively developed but small user base; expect to need direct contact with the Hereon/Augsburg authors
    - **source**: https://github.com/hpsint/hpsint
  -
    - **quantity**: PUMA repository scale at time of survey
    - **value**: ~73-163 files indexed, 4 stars, 3 forks, last push 2026-08-26
    - **units**: -
    - **context**: Young, small-community codebase despite the peer-reviewed paper. Budget for building it from source (MOOSE fork hugary1995/moose @ neml2-v3-migration + NEML2 main as pinned submodules) and for upstreaming fixes.
    - **source**: https://github.com/applied-material-modeling/puma ; GitHub repo search metadata
  -
    - **quantity**: Current versions/licences of the supporting Python stack
    - **value**: pycalphad 0.11.2 (MIT); Cantera 3.2.0 (BSD-3); thermo 0.6.1 (MIT); CoolProp 8.0.0 (MIT); gmsh 4.15.2 (GPLv2+); meshio 5.3.5 (MIT); pygalmesh 0.10.7 (GPL-3.0-or-later); PyVista 0.49.0 (MIT); trimesh 5.1.0 (MIT); porespy 3.1.1 (MIT); SfePy 2026.2 (BSD); DVC 3.67.1 (Apache-2.0); MLflow 3.16.1; pydantic 2.13.5 (MIT); h5py 3.16.0 (BSD-3); xarray 2026.7.0 (Apache-2.0); lmfit 1.3.4 (BSD-3); emcee 3.1.6 (MIT); PyMC 6.3.2 (Apache-2.0); UQpy 4.2.1 (MIT); SMT 2.15.0 (BSD-3); BoTorch 0.18.1 (MIT); NLopt 2.11.0 (MIT); Optuna 5.0.0; pyMCR 0.5.1 (public domain); Pint 0.26.1 (BSD); uncertainties 3.2.3 (BSD)
    - **units**: -
    - **context**: Queried live from the PyPI JSON API on 2026-09-21. GPL-3 on pygalmesh and GPLv2+ on gmsh matter if any part of the toolchain must be redistributed non-copyleft.
    - **source**: https://pypi.org/pypi/<pkg>/json, queried 2026-09-21
  -
    - **quantity**: Licences of the candidate FEM/phase-field/DEM cores
    - **value**: MOOSE LGPL-2.1; MALAMUTE LGPL-2.1; PUMA MIT; NEML2 MIT; pyzag MIT; CoBRA MIT; DOLFINx LGPL-3.0+; Kratos BSD-4; PRISMS-PF LGPL-2.1; hpsint GPL-3.0; OpenCalphad GPL-3.0; LIGGGHTS-PUBLIC GPL; NASA PuMA NOSA; RefraSin MIT; dp3D licence not stated
    - **units**: -
    - **context**: hpsint's GPL-3.0 is the one that constrains combination with proprietary code; everything in the MOOSE/PUMA/NEML2 line is LGPL/MIT and safe for an industry-facing tool.
    - **source**: Repository LICENSE files / GitHub licence badges as fetched 2026-09-21; dp3D licence explicitly not found
- **models_or_methods**:
  -
    - **name**: Skorohod-Olevsky Viscous Sintering (SOVS) continuum constitutive model
    - **formulation**: sigma_ij = 2*eta_0(T) * [ phi(theta) * edot'_ij + psi(theta) * (edot_kk/3) * delta_ij ] + P_L(theta) * delta_ij

with
  theta = porosity,  rho_rel = 1 - theta
  phi(theta) = (1 - theta)^2                      (normalised shear viscosity modulus)
  psi(theta) = (2/3) * (1 - theta)^3 / theta      (normalised bulk viscosity modulus)
  P_L(theta) = (3*alpha_s / r0) * (1 - theta)^2   (sintering stress; alpha_s = surface energy, r0 = particle radius)
  eta_0(T)   = A * exp(Q_eta / (R*T))             (Arrhenius shear viscosity of the dense skeleton; Reiterer/Ewsuk)

and the densification/kinematic closure
  thetadot = -(1 - theta) * edot_kk   ,   edot_kk = tr(strain-rate)

Implement as an Abaqus UMAT (portable straight into MOOSE via AbaqusUMATStress) or as a NEML2 composed model.
    - **when_to_use**: The workhorse for part-scale shrinkage and distortion prediction of pressureless sintering. Use this for the actual heating-cycle optimisation and for geometric compensation of the printed green part.
    - **inputs_needed**: Q_eta and A from dilatometry at >=3 heating rates (free-sintering + optionally sinter-forging or loaded dilatometry to separate bulk from shear response); alpha_s (Cu surface energy) and r0 (Lithoz slurry particle size, get from the slurry via laser diffraction or SEM); green density theta_0 after debinding; CTE(T) and elastic moduli for the elastic/thermal part.
    - **limitations**: phi and psi as written assume isotropic spherical-pore geometry and give psi -> infinity as theta -> 0, which is numerically awkward near full density - regularise. Anisotropic shrinkage from layer-wise DLP printing is not captured without an anisotropic extension. The single Arrhenius Q_eta lumps grain-boundary and lattice diffusion; for Cu these have different activation energies so a single Q will only fit over a limited window.
    - **source**: Reiterer M., Ewsuk K., Arguello J., 'An Arrhenius-Type Viscosity Function to Model Sintering Using the Skorohod-Olevsky Viscous Sintering Model Within a Finite-Element Code', J. Am. Ceram. Soc. (2006), DOI 10.1111/j.1551-2916.2006.01041.x; Olevsky E.A., 'Theory of sintering: from discrete to continuum', Mater. Sci. Eng. R (1998), DOI 10.1016/S0927-796X(98)00009-6. Exact phi/psi expressions as written are the standard textbook forms - verify signs/powers against the primary text before coding.
  -
    - **name**: GTN / Leblond-Perrin-Suquet porous viscoplasticity as a sintering surrogate (MOOSE built-in)
    - **formulation**: GTN yield/potential:
  Phi = (Sigma_eq / sigma_M)^2 + 2*q1*f*cosh( 3*q2*Sigma_m / (2*sigma_M) ) - (1 + q3*f^2) = 0

Porosity evolution:
  fdot = (1 - f) * tr(Edot)

Sintering modification (the change you must make):
  replace Sigma_m  ->  Sigma_m + P_s(f, T)
so that with zero applied stress the hydrostatic sintering stress P_s drives fdot < 0 (densification) instead of void growth. LPS supplies the rate-dependent (creep-exponent n) version.
    - **when_to_use**: Fastest route to a running part-scale sintering model inside MOOSE without writing a constitutive law from scratch: ADViscoplasticityStressUpdate + ADComputeMultiplePorousInelasticStress already give you the return mapping, the AD tangent and the porosity state variable.
    - **inputs_needed**: q1,q2,q3 (Tvergaard parameters, default 1.5/1.0/q1^2), stress exponent n and reference creep rate from Cu creep data, P_s(f,T) from surface energy and pore size, initial f = 1 - green density.
    - **limitations**: GTN was built for void GROWTH in ductile fracture; the calibration ranges of q1..q3 are not established for densification. The model has no grain-growth coupling, so it cannot capture the late-stage slowdown of Cu densification. It is a pragmatic surrogate, not a first-principles sintering theory - state this clearly in any paper.
    - **source**: https://raw.githubusercontent.com/idaholab/moose/next/modules/solid_mechanics/doc/content/source/materials/ADViscoplasticityStressUpdate.md (cites Gurson 1977, Tvergaard 1984, Leblond-Perrin-Suquet 1994). The sintering-stress-offset modification is a standard idea but is NOT implemented in MOOSE - unverified as a published MOOSE capability.
  -
    - **name**: Master Sintering Curve (MSC)
    - **formulation**: Theta(t, T(t)) = integral_0^t (1 / T(t')) * exp( -Q / (R * T(t')) ) dt'

rho_rel = F(ln Theta),  commonly fitted as a sigmoid:
  rho_rel = rho_0 + (rho_f - rho_0) / ( 1 + exp( -( ln(Theta) - a ) / b ) )

Q is found by scanning Q and minimising the mean residual sum of squares of all heating-rate dilatometry curves collapsed onto one Theta axis.
    - **when_to_use**: First thing to do with the dilatometry data. Gives a single apparent Q that (per Reiterer/Ewsuk) can be fed straight into the SOVS Arrhenius viscosity, and gives a cheap zero-dimensional predictor of final density for ANY proposed heating cycle - ideal as the objective function inside a cycle optimiser before you spend FE time.
    - **inputs_needed**: Dilatometry (or interrupted-density) curves at >=3 heating rates spanning at least a factor of 4 (e.g. 2, 5, 10, 20 K/min), same green density.
    - **limitations**: Assumes a single dominant densification mechanism with constant Q over the whole trajectory - questionable for Cu where surface diffusion dominates early (non-densifying) and grain-boundary diffusion later. Two-stage MSC variants exist. Cannot predict distortion, only density.
    - **source**: Original: Su & Johnson (1996) - DOI not verified here. Practical construction: Pouchly & Maca, 'Master sintering curve: A practical approach to its construction', Science of Sintering (2010), DOI 10.2298/sos1001025p; and Science of Sintering (2008), DOI 10.2298/sos0802117m. Two-stage MSC: Ceramics International (2013), DOI 10.1016/j.ceramint.2012.10.036.
  -
    - **name**: Isoconversional (model-free) kinetics for binder burnout - Friedman and KAS
    - **formulation**: Friedman (differential):
  ln( dalpha/dt )_{alpha,i} = ln[ A_alpha * f(alpha) ] - E_alpha / ( R * T_{alpha,i} )
  -> for each fixed alpha, regress ln(dalpha/dt) against 1/T across heating rates i; slope = -E_alpha/R

Kissinger-Akahira-Sunose (integral):
  ln( beta_i / T_{alpha,i}^2 ) = const - E_alpha / ( R * T_alpha )

Vyazovkin advanced nonlinear method minimises
  sum_i sum_{j!=i} [ I(E_alpha, T_i(t_alpha)) * beta_j ] / [ I(E_alpha, T_j(t_alpha)) * beta_i ]

Then predict any arbitrary T(t) by numerically integrating with the E(alpha) spectrum.
    - **when_to_use**: MANDATORY first step for an unknown proprietary binder. It gives E as a function of conversion WITHOUT assuming a reaction model - which is exactly the situation here. A rising or multi-plateau E(alpha) immediately tells you how many distinct decomposition events the Lithoz binder has, which sets the number of holds in the debinding cycle.
    - **inputs_needed**: TGA at >=3-5 heating rates (ICTAC recommends at least 3, ideally 5, spanning a decade), in the actual process atmosphere (Ar, N2, H2/N2, and air for comparison), sample mass small enough to avoid self-heating and diffusion limitation (ICTAC: check by halving sample mass).
    - **limitations**: Isoconversional E(alpha) is only valid if the TGA is free of heat- and mass-transfer artefacts. For a Cu-filled slurry, the high thermal conductivity helps but the metal may catalyse decomposition, so TGA on neat binder (unavailable here) and on the filled slurry will differ - you only have the latter.
    - **source**: ICTAC Kinetics Committee recommendations: computations DOI 10.1016/j.tca.2011.03.034; data collection DOI 10.1016/j.tca.2014.05.036; multi-step DOI 10.1016/j.tca.2020.178597; thermal decomposition DOI 10.1016/j.tca.2022.179384
  -
    - **name**: Distributed Activation Energy Model (DAEM) for the binder
    - **formulation**: 1 - alpha(t) = integral_0^infinity exp( -A * integral_0^t exp( -E / (R*T(t')) ) dt' ) * f(E) dE

with f(E) usually Gaussian:  f(E) = (1/(sigma*sqrt(2*pi))) * exp( -(E - E0)^2 / (2*sigma^2) )
or Weibull (better for asymmetric DTG peaks).

Miura-Maki approximation gives a closed-form inversion from the TGA data.
    - **when_to_use**: When the Friedman E(alpha) is broad and monotonically varying rather than showing discrete plateaus - i.e. when the binder is a mixture of oligomers/photopolymer network fragments with a continuum of bond strengths, which is the likely case for a proprietary acrylate/methacrylate LCM binder.
    - **inputs_needed**: Same multi-heating-rate TGA. Fit (A, E0, sigma) or (A, Weibull shape/scale) by nonlinear least squares - lmfit or the pyzag adjoint route.
    - **limitations**: A and E0 are strongly correlated (kinetic compensation effect); do NOT report them as independently identified without a profile-likelihood or MCMC posterior. The model is purely a mass-loss description and says nothing about the gas species produced, which is what actually determines carbon residue on the Cu.
    - **source**: Method overview: Renewable Energy (2024), DOI 10.1016/j.renene.2024.121549 (Weibull DAEM); Applied Energy (2017), DOI 10.1016/j.apenergy.2016.02.056. No maintained open-source DAEM package was found on PyPI or GitHub during this survey - expect to write ~200 lines of scipy/lmfit yourself.
  -
    - **name**: PUMA/NEML2 reaction + mass-fraction + porosity chain (the reusable debinding implementation)
    - **formulation**: Rate coefficient:   k(T) = k0 * exp( -Q / (R*T) )                [NEML2 ArrheniusParameter]
Reaction rate:      alphadot = k * (1 - alpha)^n                 [NEML2 ContractingGeometry, order n]
Binder mass:        wbdot   = -1 * alphadot                      [ScalarLinearCombination]
Char mass:          wcdot   = +Y * alphadot                      [ScalarLinearCombination, Y = char yield]
Gas mass:           wgdot   = (1 - Y) * alphadot
Open porosity:      phi_op evolves from the volume released by binder -> char + gas
Composite props:    rho = sum_i phi_i * rho_i ;  cp = sum_i w_i * cp_i ;  k_th = sum_i phi_i * k_i
Heat source:        M3 = -DeltaH * alphadot
Time integration:   ScalarBackwardEulerTimeIntegration on alpha, wb, wc (implicit), solved by NEML2 Newton + DenseLU

Coupled to MOOSE energy equation via kernels PumaCoupledTimeDerivative (M1 dT/dt), PumaCoupledDiffusion (M2), CoupledMaterialSource (M3), with analytic dMi/dT derivatives passed through the [NEML2] block for a consistent Jacobian.
    - **when_to_use**: This is the code you should start from, literally. It already runs in 1D/2D/3D, already has a TGA calibration driver, and already couples reaction heat back into conduction with a consistent Jacobian. Swap the demo binder parameters for your fitted Lithoz ones and the demo solid for Cu.
    - **inputs_needed**: k0, Q, n, Y from your TGA fit; rho/cp/k for Cu, char and binder; green part geometry and mesh; furnace T(t) and h/emissivity BCs.
    - **limitations**: Single-step contracting-geometry kinetics as shipped - you will need to extend to 2-3 parallel reactions (trivial: compose more ArrheniusParameter+ContractingGeometry blocks) for a real photopolymer. Gas transport is present in PUMA's porous_flow examples but is NOT wired into the pyrolysis examples, so the crack-from-overpressure criterion needs assembling yourself. Build requires a pinned MOOSE fork (hugary1995/moose @ neml2-v3-migration) plus NEML2 main - non-trivial, budget a week.
    - **source**: https://raw.githubusercontent.com/applied-material-modeling/puma/main/examples/pyrolysis/material_calibration/TGA.i ; https://raw.githubusercontent.com/applied-material-modeling/puma/main/examples/pyrolysis/1D/pyrolysis.i ; https://raw.githubusercontent.com/applied-material-modeling/puma/main/examples/pyrolysis/1D/neml2/neml2_material.i ; PUMA README
  -
    - **name**: Gas generation / Darcy transport / cracking criterion during thermal debinding
    - **formulation**: Mass balance of pyrolysis gas in the open pore network:
  d( eps * rho_g ) / dt  +  div( rho_g * v )  =  mdot_gen ,   mdot_gen = rho_solid,0 * (1 - Y) * alphadot

Darcy velocity:
  v = -(K / mu) * grad(P)

Permeability (Kozeny-Carman):
  K = eps^3 * d_p^2 / ( 180 * (1 - eps)^2 )

Ideal gas closure:  rho_g = P * M_g / (R * T)

Cracking / blistering criterion:
  max over domain of P(x,t) - P_ambient  <  sigma_green(T, eps)
where sigma_green is the (weak) strength of the partially-debound body. The maximum allowable heating rate in the burnout window follows directly from enforcing this.
    - **when_to_use**: This is the physics that actually sets the debinding ramp rate and is the reason naive slow ramps are used industrially. For a THICK Cu part it matters; for thin LCM lattices it may not bind. Compute it to prove which regime you are in.
    - **inputs_needed**: eps_0 and d_p (pore size) after binder softening - from micro-CT or Hg porosimetry; gas viscosity mu(T) and mean molar mass M_g (from Cantera or evolved-gas-analysis MS if available); green strength sigma_green (3-point bend on debound-interrupted samples).
    - **limitations**: Kozeny-Carman is poor for the partially-blocked, evolving pore network of early debinding (it assumes a percolating granular bed). The molar mass of the evolved gas mixture changes continuously. Green strength during burnout is the hardest number to obtain and typically dominates the uncertainty budget.
    - **source**: Governing form is standard porous-media theory as implemented in MOOSE's PorousFlow module (https://raw.githubusercontent.com/idaholab/moose/next/modules/porous_flow/doc/content/modules/porous_flow/index.md). Review context: 'Thermal Debinding for Binder Burnout in Metal and Ceramic Processing', Heat Transfer Engineering (2024), DOI 10.1080/01457632.2024.2332111. The specific Kozeny-Carman constant 180 and the strength-based cracking criterion as stated are textbook forms - unverified against a sintering-specific primary source.
  -
    - **name**: Cu-O-C-H gas-phase equilibrium screening (the atmosphere design calculation)
    - **formulation**: Key equilibria to evaluate as a function of T and gas composition:
  (1) 2Cu(s) + 1/2 O2(g) = Cu2O(s)        -> defines the max allowable pO2
  (2) Cu2O(s) + H2(g) = 2Cu(s) + H2O(g)   -> defines the max allowable pH2O/pH2
  (3) C(s) + H2O(g) = CO(g) + H2(g)       -> the ONLY practical carbon removal route for Cu (no stable Cu carbide)
  (4) C(s) + 2H2(g) = CH4(g)              -> methanation, favoured at LOW T
  (5) 2CO(g) = C(s) + CO2(g)              -> Boudouard, deposits carbon at intermediate T

Process window: choose pH2O/pH2 at each T such that
  [pH2O/pH2]_carbon-removal(T)  <  pH2O/pH2  <  [pH2O/pH2]_Cu/Cu2O(T)
If that window is empty at a given T, no atmosphere can simultaneously decarburise and avoid oxidation there - which is the central thermodynamic difficulty of copper debinding.

Compute with Cantera (Gibbs minimisation, `equilibrate('TP')`) for the gas phase and pycalphad / OpenCalphad / FactSage for the condensed Cu-O phases.
    - **when_to_use**: Before ANY furnace run. This single plot (log(pH2O/pH2) vs 1/T with the Cu/Cu2O line and the C-removal line) is the deliverable that turns 'we have no heating cycle' into a defensible atmosphere+temperature schedule, and it is a publishable figure in its own right.
    - **inputs_needed**: Gibbs energy data for Cu, Cu2O, CuO, C(graphite), and the H-C-O gas species. Cantera ships NASA polynomials for the gas species; condensed Cu oxides need a CALPHAD TDB (pycalphad reads TDB) or SGTE/SSUB-type data.
    - **limitations**: Equilibrium says what is possible, not what is kinetically reachable - carbon removal from a closing pore network is transport-limited, so the real window is narrower than the thermodynamic one. Free, well-assessed Cu-O TDB files are not abundant; a Cu-O-S assessment exists (Calphad 2015, DOI 10.1016/j.calphad.2015.01.111) but a directly usable free Cu-O-C-H database was NOT located in this survey.
    - **source**: Cantera 3.2.0 (BSD-3) https://pypi.org/pypi/cantera/json ; pycalphad 0.11.2 (MIT), Otis & Liu, J. Open Research Software (2017), DOI 10.5334/jors.140 ; OpenCalphad https://github.com/sundmanbo/opencalphad (GPL-3, Fortran, OCASI C binding). The specific reaction set and the window construction are standard powder-metallurgy practice - the exact boundary values are unverified and must be computed.
  -
    - **name**: Multiscale parameter generation: phase-field and DEM in place of missing experiments
    - **formulation**: Phase-field (grand-potential, MOOSE GrandPotentialSinteringMaterial) solid free energies:
  parabolic:  f_s = (1/2) * k_s * (c_s - c_s^eq)^2
  dilute:     f_s = E_f/V_a + (kB*T/V_a) * ( c*ln(c) - c )
  ideal:      f_s = c*E_f/V_a + (kB*T/V_a) * [ c*ln(c) + (1-c)*ln(1-c) ]
with switching functions between void/solid and solid/grain-boundary, and m, kappa, gamma the phase-field energy parameters.

Upscaling protocol: run a periodic RVE of N particles at several temperatures and applied hydrostatic/deviatoric stresses; measure the macroscopic strain-rate response; regress phi(theta), psi(theta), P_L(theta) and eta_0(T) for the SOVS law. This is how you obtain the continuum constitutive parameters when you cannot run enough dilatometry.
    - **when_to_use**: When experiment budget is the binding constraint - which it is here, because the slurry is precious R&D material. Also the natural 'novelty' axis for a paper: bottom-up parameterisation of a continuum sintering law for a Cu LCM feedstock.
    - **inputs_needed**: Cu surface energy, grain-boundary energy, surface/GB/lattice diffusivities and their activation energies (literature), particle size distribution from the slurry, and a packing (from micro-CT of a green part, or from DEM packing generation).
    - **limitations**: Phase-field RVEs of a few hundred particles are 10^7-10^9 DOF problems - hpsint or PRISMS-PF class codes, days of cluster time each. The upscaled parameters inherit every uncertainty in the input diffusivities. DEM (dp3D) is cheaper and handles thousands of particles but needs its own contact-law calibration.
    - **source**: https://raw.githubusercontent.com/idaholab/moose/next/modules/phase_field/doc/content/source/materials/GrandPotentialSinteringMaterial.md ; Greenquist, Tonks, Aagesen, Zhang, Comput. Mater. Sci. (2020), DOI 10.1016/j.commatsci.2019.109288 ; Ivannikov et al., Euro PM2023, DOI 10.59499/ep235764034 ; Paredes-Goyes, Jauffres, Martin, JTCAM, DOI 10.46298/jtcam.13721
  -
    - **name**: Verification and validation protocol for the codebase
    - **formulation**: Code verification (does the code solve the equations right):
  - Method of Manufactured Solutions per kernel: choose u_exact(x,t), substitute into the PDE, derive the source term S = L[u_exact], add S, verify observed order of accuracy p_obs -> p_theoretical
  - p_obs = ln( ||e_{h1}|| / ||e_{h2}|| ) / ln( h1/h2 )
Solution verification (is the discretisation fine enough):
  - Grid Convergence Index, GCI = Fs * |(f2-f1)/f1| / (r^p - 1), Fs = 1.25 for 3-grid studies
Validation (are these the right equations):
  - ASME V&V 10 hierarchy: unit -> benchmark -> subsystem -> full part; validation metric with experimental uncertainty bars at each level
Kinetics-specific:
  - ICTAC protocol compliance for every TGA-derived number
    - **when_to_use**: Continuously, from day one. For a paper this is the difference between 'we ran a simulation' and 'we built a validated capability'. Encode MMS cases and convergence studies as CI tests in the repo.
    - **inputs_needed**: Nothing beyond the code itself for verification; for validation: interrupted-sintering density/geometry measurements, dilatometry, and ideally in-situ or DVC-based shrinkage fields.
    - **limitations**: MMS on a fully coupled reaction-porous-flow-viscoplastic system is laborious; do it kernel-by-kernel, not on the coupled system. The GCI safety factor is a convention, not a bound.
    - **source**: Salari & Knupp, DOI 10.2172/759450 ; Roache, J. Fluids Eng. (2002), DOI 10.1115/1.1436090 ; conjugate heat transfer MMS: DOI 10.1016/j.jcp.2015.12.004 ; ASME V&V 10 overview: Schwer, Engineering with Computers (2007), DOI 10.1007/s00366-007-0072-z ; ICTAC DOIs as above. GCI formula as stated is the standard Roache form - the Fs=1.25 value is convention, unverified against the current ASME V&V 20 edition.
- **open_questions**:
  - Can PUMA actually be built and run today outside ORNL? It pins a MOOSE FORK (hugary1995/moose @ branch neml2-v3-migration) plus NEML2 main as git submodules, and requires torch + nmhit + pyzag 2.0.0 + scikit-build-core in a conda env. Someone needs to spend 2-3 days proving the build before the whole architecture is staked on it. If it does not build, what is the fallback - vanilla MOOSE + NEML2 with the PUMA kernels ported in?
  - Does PUMA have a working SINTERING example, or only pyrolysis/infiltration/solidification/curing? The examples directory listing shows lsi, pip_and_lsi, porous_flow, pyrolysis, random_field_cobra, solidification - no sintering directory was found. The README and the paper both claim sintering capability. This gap must be resolved directly with the ORNL authors (Huy Tran, Tianchen Hu, Mark Messner) before committing.
  - Is there any NEML2 constitutive model for sintering (porous viscoplastic with sintering stress), or must one be written? GitHub code search on the neml2 repo for sintering-related model paths returned nothing. If it must be written, is the right vehicle a NEML2 composed model (gains GPU + adjoint calibration for free) or a MOOSE ADViscoplasticityStressUpdate derivative (faster to write, loses the pyzag calibration path)?
  - What are the actual licence terms of dp3D? No LICENSE file was identified. Without one, the code is legally all-rights-reserved and cannot be redistributed or built upon in a published workflow. Contact C.L. Martin at SIMAP.
  - Is a free, well-assessed Cu-O (ideally Cu-O-C-H) CALPHAD database available in TDB format for pycalphad/OpenCalphad, or is a Thermo-Calc/FactSage licence unavoidable for the atmosphere-window calculation? Only a Cu-O-S assessment (Calphad 2015) was located.
  - How should the DLP layer-wise build anisotropy be represented? SOVS as written is isotropic. Do we need an anisotropic sintering-viscosity tensor (cf. J. Eur. Ceram. Soc. 2024, DOI 10.1016/j.jeurceramsoc.2024.03.031 on anisotropic sintering of multilayer laminates), and if so does any existing code implement it?
  - Is gravity/friction on the setter plate a first-order effect for the geometries of interest? Binder-jetting literature (wt Werkstattstechnik 2024, DOI 10.37544/1436-4980-2024-06-119; Springer 2025, DOI 10.1007/978-3-662-69327-8_10) treats sintering-base friction as a dominant distortion driver. This requires a contact model and a friction coefficient measurement, which is extra scope.
  - Which single scalar objective should the heating-cycle optimiser minimise - cycle time subject to (final density > target AND max overpressure < green strength AND max distortion < tolerance AND residual carbon < limit)? And is the MSC-based zero-D surrogate accurate enough to do the outer optimisation loop, with full 3D FE only for verification of the optimum?
  - No maintained open-source DAEM or isoconversional-kinetics package was found on PyPI or GitHub. Is it genuinely absent (in which case writing and releasing one is a small but real contribution alongside the paper), or did the search miss it? Commercial equivalents are NETZSCH Kinetics Neo and AKTS - is a licence available to the group as a cross-check?
  - Vendor claims for Simufact Additive, Autodesk Netfabb Simulation, Desktop Metal Live Sinter, Ansys Additive and GeonX Virfac could not be verified - all vendor pages returned 403/404 to automated fetching. Someone must check directly whether any of these already does pressureless Cu sintering with compensation, because if one does, the build-vs-buy calculus changes.
  - Can in-situ validation data be obtained - dilatometry is a must, but is synchrotron or lab micro-CT with digital volume correlation available to give a full 3D shrinkage FIELD rather than a single scalar? That would elevate the validation from V&V 10 'benchmark' level to 'subsystem' level and is what makes the paper strong.
- **references**:
  -
    - **citation**: Tran H., Kounouho S., Du M., Sultana F., Messner M.C., Hu T., 'PUMA: A scalable framework for simulating powder post-processing in advanced manufacturing', Advances in Engineering Software, 2026.
    - **url**: https://doi.org/10.1016/j.advengsoft.2026.104216
    - **why**: THE reference implementation. MOOSE+NEML2 framework covering curing, pyrolysis/debinding, sintering, infiltration and solidification with distortion and residual-stress prediction. Read this first; it defines the architecture you should adopt or deliberately reject.
  -
    - **citation**: PUMA source repository, applied-material-modeling/puma (MIT).
    - **url**: https://github.com/applied-material-modeling/puma
    - **why**: Working code: pyrolysis examples in 1D/2D/3D, a TGA material-calibration driver, porous_flow examples, CoBRA CT-based random-field ICs, and full build instructions. Clone and build before doing anything else.
  -
    - **citation**: NEML2 - New Engineering Material model Library v2, applied-material-modeling/neml2 (MIT).
    - **url**: https://github.com/applied-material-modeling/neml2
    - **why**: The constitutive layer: PyTorch-backed, batched, GPU-capable, automatic differentiation, composable models. Where a Cu sintering constitutive law should be written so it is simultaneously usable in MOOSE and calibratable by adjoint.
  -
    - **citation**: pyzag - training models defined by recursive nonlinear equations, applied-material-modeling/pyzag (MIT).
    - **url**: https://github.com/applied-material-modeling/pyzag
    - **why**: Adjoint-based, memory-efficient parameter sensitivities for implicit time-integrated constitutive models, with Pyro integration for Bayesian calibration. This is the tool that turns 'we do not know the binder' into a tractable inverse problem with posteriors.
  -
    - **citation**: MOOSE ADViscoplasticityStressUpdate documentation (GTN / Leblond-Perrin-Suquet porous viscoplasticity).
    - **url**: https://raw.githubusercontent.com/idaholab/moose/next/modules/solid_mechanics/doc/content/source/materials/ADViscoplasticityStressUpdate.md
    - **why**: The built-in object closest to a continuum sintering law, with full theory write-up and the porosity evolution law. Read alongside ADComputeMultiplePorousInelasticStress.
  -
    - **citation**: MOOSE AbaqusUMATStress documentation.
    - **url**: https://raw.githubusercontent.com/idaholab/moose/next/modules/solid_mechanics/doc/content/source/materials/abaqus/AbaqusUMATStress.md
    - **why**: Proves a SOVS UMAT is portable between Abaqus and MOOSE unchanged, including PNEWDT time-step control. This is the key de-risking fact for the constitutive-model decision.
  -
    - **citation**: Reiterer M., Ewsuk K., Arguello J., 'An Arrhenius-Type Viscosity Function to Model Sintering Using the Skorohod-Olevsky Viscous Sintering Model Within a Finite-Element Code', J. Am. Ceram. Soc. 89(6), 2006.
    - **url**: https://doi.org/10.1111/j.1551-2916.2006.01041.x
    - **why**: The canonical FE-implementable SOVS formulation, and explicitly shows that the Master Sintering Curve apparent activation energy Q can be reused as the activation energy in the viscosity function - which links your cheap dilatometry analysis directly to the expensive FE model.
  -
    - **citation**: Olevsky E.A., 'Theory of sintering: from discrete to continuum', Materials Science and Engineering: R: Reports, 1998.
    - **url**: https://doi.org/10.1016/S0927-796X(98)00009-6
    - **why**: Primary source for the continuum sintering theory, the normalised bulk/shear viscosity moduli and the sintering stress. Verify the exact phi/psi/P_L expressions here before coding them.
  -
    - **citation**: Greenquist I., Tonks M., Aagesen L., Zhang Y., 'Development of a microstructural grand potential-based sintering model', Computational Materials Science, 2020.
    - **url**: https://doi.org/10.1016/j.commatsci.2019.109288
    - **why**: The theory behind MOOSE's GrandPotentialSinteringMaterial, which is already in the MOOSE tree with four regression-test input files you can run today.
  -
    - **citation**: Ivannikov V., Munch P., Kronbichler M., Ebel T., 'Large-scale Phase-field Simulations of Solid-State Sintering of Metallic Powders', Euro PM2023 Proceedings.
    - **url**: https://doi.org/10.59499/ep235764034
    - **why**: The hpsint paper. Specifically about METALLIC powders at scale (hundreds-thousands of particles, 3D) - the closest published microstructural work to a Cu sintering study, and the route to generating SOVS parameters bottom-up.
  -
    - **citation**: hpsint source repository (GPL-3.0, deal.II matrix-free).
    - **url**: https://github.com/hpsint/hpsint
    - **why**: The most mature open-source sintering phase-field code. Note the GPL-3.0 licence if any of this must combine with proprietary code.
  -
    - **citation**: Paredes-Goyes B., Jauffres D., Martin C.L., 'A Level Set Discrete Element Model (LS-DEM) for sintering with an optimization-based contact detection', Journal of Theoretical, Computational and Applied Mechanics.
    - **url**: https://doi.org/10.46298/jtcam.13721
    - **why**: State of the art in particle-level DEM sintering with non-spherical particles. Accompanying data at Zenodo 10.5281/zenodo.15168970 (CC-BY-4.0); code at github.com/Xtof38/sourcedp3D_public.
  -
    - **citation**: MALAMUTE - MOOSE Application Library for Advanced Manufacturing UTilitiEs, idaholab/malamute (LGPL-2.1).
    - **url**: https://github.com/idaholab/malamute
    - **why**: Engineering-scale furnace/tooling physics done properly in MOOSE: thermal and electrical contact conditions, temperature-dependent graphite and steel properties, radiative BCs. Its EFAS tutorial is a model for how to structure a furnace-scale parametric study.
  -
    - **citation**: Sadeghi Borujeni S., Shad A., Abburi Venkata K., Guenther N., Ploshikhin V., 'Numerical simulation of shrinkage and deformation during sintering in metal binder jetting with experimental validation', Materials & Design, 2022.
    - **url**: https://doi.org/10.1016/j.matdes.2022.110490
    - **why**: Direct methodological precedent: continuum sintering FE with experimental validation for a powder-bed metal AM part. The closest published analogue to what this project must produce, and the natural benchmark to reproduce first.
  -
    - **citation**: Zhang K., Zhang W., Brune R., Herderick E., Zhang X., Cornell J., Forsmark J., 'Numerical simulation and experimental measurement of pressureless sintering of stainless steel part printed by Binder Jetting Additive Manufacturing', Additive Manufacturing, 2021.
    - **url**: https://doi.org/10.1016/j.addma.2021.102330
    - **why**: Second independent validated pressureless-sintering FE study for an AM part; useful for cross-checking constitutive choices and for the paper's related-work section.
  -
    - **citation**: Bezek L., Wilkerson R., Chad J., Quintana T., Patterson B., Adhikari S., Lee K., 'Evolution of debinding and sintering of a silica-based ceramic using vat photopolymerization additive manufacturing', Additive Manufacturing, 2025.
    - **url**: https://doi.org/10.1016/j.addma.2025.104795
    - **why**: The closest published work on the actual process route (vat photopolymerisation -> debinding -> sintering), including in-situ/interrupted characterisation methodology you can copy for the Cu system.
  -
    - **citation**: ICTAC Kinetics Committee recommendations - five-part series in Thermochimica Acta (2011, 2014, 2020, 2022, 2023).
    - **url**: https://doi.org/10.1016/j.tca.2011.03.034
    - **why**: The mandatory protocol for the binder-kinetics work. Also DOIs 10.1016/j.tca.2014.05.036 (data collection), 10.1016/j.tca.2020.178597 (multi-step kinetics), 10.1016/j.tca.2022.179384 (thermal decomposition). Reviewers will check compliance.
  -
    - **citation**: Pouchly V., Maca K., 'Master sintering curve: A practical approach to its construction', Science of Sintering, 2010.
    - **url**: https://doi.org/10.2298/sos1001025p
    - **why**: Practical recipe for building the MSC from dilatometry and extracting the apparent Q - the cheapest high-value analysis available from the data you will collect anyway.
  -
    - **citation**: Salari K., Knupp P., 'Code Verification by the Method of Manufactured Solutions', SAND2000-1444.
    - **url**: https://doi.org/10.2172/759450
    - **why**: The definitive MMS reference. Use it to build per-kernel verification tests into CI from day one; this is what makes the codebase publishable rather than merely functional.
  -
    - **citation**: Schwer L.E., 'An overview of the PTC 60/V&V 10: guide for verification and validation in computational solid mechanics', Engineering with Computers, 2007.
    - **url**: https://doi.org/10.1007/s00366-007-0072-z
    - **why**: Accessible summary of the ASME V&V 10 validation hierarchy to structure the experimental campaign (unit -> benchmark -> subsystem -> full part).
  -
    - **citation**: Otis R., Liu Z.-K., 'pycalphad: CALPHAD-based Computational Thermodynamics in Python', Journal of Open Research Software, 2017.
    - **url**: https://doi.org/10.5334/jors.140
    - **why**: MIT-licensed CALPHAD in Python, reads TDB databases - the free route to the Cu-O condensed-phase equilibria that set the oxidation boundary of the debinding atmosphere window.
  -
    - **citation**: OpenCalphad, sundmanbo/opencalphad (GPL-3.0, Fortran, with OCASI C binding).
    - **url**: https://github.com/sundmanbo/opencalphad
    - **why**: The alternative free CALPHAD engine, with an application software interface designed for embedding in simulation codes - relevant if the thermochemistry must be called from inside the FE loop rather than pre-tabulated.
  -
    - **citation**: Cantera 3.2.0 (BSD-3-Clause).
    - **url**: https://cantera.org
    - **why**: Gibbs-minimisation gas-phase equilibria for the Cu-O-C-H system (H2/H2O/CO/CO2/CH4), i.e. the pH2O/pH2 process-window plot. BSD licence, mature, Python API.
  -
    - **citation**: NASA PuMA (Porous Microstructure Analysis) v3, nasa/puma (NASA Open Source Agreement), with pumapy Python bindings.
    - **url**: https://github.com/nasa/puma
    - **why**: Micro-CT to effective properties: porosity, specific surface area, tortuosity, permeability, effective thermal conductivity, elastic properties. Feeds the green-body property inputs that the continuum model needs. Note: unrelated to ORNL PUMA despite the identical name.
  -
    - **citation**: CoBRA - Computed-tomography Based Random-field Approximation, skounouho/puma-cobra (MIT).
    - **url**: https://github.com/skounouho/puma-cobra
    - **why**: Karhunen-Loeve random-field generation from CT imagery, integrated with PUMA. The principled way to seed spatially correlated green-density variation as an initial condition instead of assuming uniformity - and a good source of UQ realisations.
  -
    - **citation**: Adams B.M. et al., 'Dakota: A Multilevel Parallel Object-Oriented Framework for Design Optimization, Parameter Estimation, Uncertainty Quantification, and Sensitivity Analysis', Sandia National Laboratories, 2020 manual.
    - **url**: https://doi.org/10.2172/1630693
    - **why**: The reference external driver for calibration, sensitivity analysis and UQ around a black-box FE code, if the native MOOSE optimization/stochastic_tools route proves insufficient.
  -
    - **citation**: MOOSE framework, idaholab/moose (LGPL-2.1).
    - **url**: https://github.com/idaholab/moose
    - **why**: The substrate. Modules directly relevant here: solid_mechanics (creep/viscoplasticity/UMAT), heat_transfer (conduction + gray-diffuse radiation with view factors), porous_flow (multiphase Darcy + heat), phase_field (grand-potential sintering), chemical_reactions, optimization (PETSc/TAO adjoint inverse problems), stochastic_tools.
  -
    - **citation**: RefraSin v1.0.0, M. Weiner, TU Bergakademie Freiberg (MIT), Zenodo.
    - **url**: https://doi.org/10.5281/zenodo.18455089
    - **why**: Sharp-interface sintering via a thermodynamic extremal principle - a cheaper alternative to phase-field for generating microstructural insight, MIT-licensed, recently released. Worth a look as a second opinion against hpsint.