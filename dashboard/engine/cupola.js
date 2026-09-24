/*
 * CUPOLA engine (JavaScript port of src/cupola). Mirrors the Python implementation line for line:
 * same state layout, same equations, same Rosenbrock 2(3) integrator, same synthesizer logic.
 * Parity with Python is checked by dashboard/engine/parity.test.mjs.
 *
 * Works in the browser (window.Cupola) and in Node (module.exports).
 */
(function (root) {
  "use strict";

  // ------------------------------------------------------------------ constants
  const R = 8.314462618, KB = 1.380649e-23, SIGMA_SB = 5.670374419e-8, P_ATM = 101325.0, T0C = 273.15;
  const M_CU = 63.546e-3, M_O = 15.999e-3, M_C = 12.011e-3, M_O2 = 31.998e-3;
  const RHO_CU = 8960.0, RHO_CU2O = 6000.0, RHO_CUO = 6310.0, RHO_CHAR = 1800.0;
  const V_CU = M_CU / RHO_CU;
  const V_CU_IN_CU2O = (2 * M_CU + M_O) / RHO_CU2O / 2;
  const V_CU_IN_CUO = (M_CU + M_O) / RHO_CUO;
  const OMEGA_CU = 1.18e-29, T_MELT_CU = 1357.77, T_EUTECTIC_CU_O = 1066.2 + T0C, O_SOLIDUS_PPM = 80.0;
  const SLPM_TO_MOLS = P_ATM / (R * T0C) / 1000.0 / 60.0;

  const BETA_REF = 10.0 / 60.0;
  const DV0 = 2.0e-5, QV = 197000.0, DDB0 = 5.0e-15, QB = 104000.0, KG0 = 1.39e-13, THETA_PIN = 0.03;
  const CUOX_K350 = 1.9001e-7, CUOX_M = 4.304, CUOX_X0 = 2.0e-3, CUOX_DREF = 10e-6;
  const NU_O2_BINDER = 64.2, N_CO2_BINDER = 53.1, N_H2O_BINDER = 40.0;
  const DH_CU_OX = 165e3, DH_RED_H2 = 73.2e3, DH_CARBOTHERMIC = 58.1e3, DH_GASIF = 131.3e3, DH_CHAR_OX = 393.5e3;
  const M_SOLVENT = 0.15, CP_BINDER = 1800.0, CP_CHAR = 1200.0;

  const NV = 10, IT = 0, IB1 = 1, IB2 = 2, IB3 = 3, IC = 4, IX = 5, IY = 6, ILV = 7, IG = 8, INT = 9;
  const NG = 7, GTF = 0, GO2 = 1, GH2 = 2, GH2O = 3, GCO = 4, GCO2 = 5, GEZ = 6;
  const Y_SMALL = 1e-4, X_SWITCH = 1e-3, EPS_ACC = 0.02, MESH_GRADE = 1.35, D_POLY_O2 = 1e-10;

  const exp = Math.exp, sqrt = Math.sqrt, pow = Math.pow, tanh = Math.tanh, abs = Math.abs;
  const min = Math.min, max = Math.max, PI = Math.PI;

  function pos(z, w) { return 0.5 * (z + sqrt(z * z + w * w)); }
  function clip(x, a, b) { return x < a ? a : (x > b ? b : x); }
  function smoothstep(x) { x = clip(x, 0, 1); return x * x * (3 - 2 * x); }
  function sigmoid(x) { return 0.5 * (1 + tanh(0.5 * x)); }

  // ------------------------------------------------------------------ thermochemistry (T0)
  const G_LINES = {
    "4Cu+O2=2Cu2O": [-333400.0, 141.3],
    "2Cu2O+O2=4CuO": [-287800.0, 204.7],
    "2H2+O2=2H2O": [-492900.0, 109.6],
    "2C+O2=2CO": [-223000.0, -175.3],
    "C+O2=CO2": [-394100.0, -0.8],
    "C+2H2=CH4": [-74870.0, 80.8],
  };
  function dG(r, T) { const a = G_LINES[r]; return a[0] + a[1] * T; }
  const thermo = {
    dG,
    pO2_eq_Cu_Cu2O: (T) => exp(dG("4Cu+O2=2Cu2O", T) / (R * T)),
    K_H2O: (T) => exp(-dG("2H2+O2=2H2O", T) / (2 * R * T)),
    h2o_h2_boundary_Cu(T) { return this.K_H2O(T) * sqrt(this.pO2_eq_Cu_Cu2O(T)); },
    reducing_margin(ratio, T) { return this.h2o_h2_boundary_Cu(T) / max(ratio, 1e-300); },
    dG_carbothermic: (T) => 0.5 * dG("2C+O2=2CO", T) - 0.5 * dG("4Cu+O2=2Cu2O", T),
    K_steam_gasification: (T) => exp(-(0.5 * dG("2C+O2=2CO", T) - 0.5 * dG("2H2+O2=2H2O", T)) / (R * T)),
    p_sat_water_Pa(Td) {
      return Td >= 0 ? 611.21 * exp((18.678 - Td / 234.5) * (Td / (257.14 + Td)))
                     : 611.15 * exp((23.036 - Td / 333.7) * (Td / (279.82 + Td)));
    },
    x_h2o_from_dewpoint(Td, P = P_ATM) { return this.p_sat_water_Pa(Td) / P; },
    dewpoint_from_x_h2o(x, P = P_ATM) {
      let lo = -90, hi = 100;
      for (let k = 0; k < 60; k++) {
        const mid = 0.5 * (lo + hi);
        if (this.x_h2o_from_dewpoint(mid, P) - x > 0) hi = mid; else lo = mid;
      }
      return 0.5 * (lo + hi);
    },
    T_solidus_Cu_O(O_ppm) {
      const f = clip(O_ppm / O_SOLIDUS_PPM, 0, 1);
      return T_MELT_CU - (T_MELT_CU - T_EUTECTIC_CU_O) * f;
    },
  };
  // hot-path caches of the Arrhenius-like thermo functions
  const A_CU2O = G_LINES["4Cu+O2=2Cu2O"], A_H2O = G_LINES["2H2+O2=2H2O"], A_CO = G_LINES["2C+O2=2CO"];
  function pO2eqCu(T) { return exp((A_CU2O[0] + A_CU2O[1] * T) / (R * T)); }
  function boundaryCu(T) {
    const K = exp(-(A_H2O[0] + A_H2O[1] * T) / (2 * R * T));
    return K * sqrt(pO2eqCu(T));
  }
  function Ksteam(T) {
    return exp(-(0.5 * (A_CO[0] + A_CO[1] * T) - 0.5 * (A_H2O[0] + A_H2O[1] * T)) / (R * T));
  }

  // ------------------------------------------------------------------ properties
  function cp_cu(T) { return 360.0 + 0.0870 * T; }
  function k_cu(T) { return 401.0 - 0.064 * (T - 300.0); }
  function mu_gas(T) { return 1.663e-5 * pow(T / 273.15, 0.7); }
  function D_O2_N2(T) { return 2.02e-5 * pow(T / 293.15, 1.75); }
  function kpFromTpeak(Tp, E) { return E * BETA_REF / (R * Tp * Tp); }

  function Setup(s) {
    const g = Object.assign({}, s);
    this.s = g;
    this.d50 = g.d50_um * 1e-6;
    const sig = Math.asinh(g.span / 2.0) / 1.2815516;
    this.d32 = this.d50 * exp(-0.5 * sig * sig);
    this.r_s = 0.5 * this.d32;
    this.G0 = g.grain_ratio * this.d50;
    this.phi = g.phi;
    this.rho_b = g.rho_binder;
    this.mb0 = (1 - this.phi) * this.rho_b;
    this.nCu = this.phi * RHO_CU / M_CU;
    this.mCu = this.phi * RHO_CU;
    const w1 = g.solvent_frac, wnet = 1 - w1, w3 = wnet * g.w_backbone, w2 = wnet - w3;
    this.b0 = [w1 * this.mb0, w2 * this.mb0, w3 * this.mb0];
    this.chi = [0.0, g.char_yield, g.char_yield];
    this.Mgas = [M_SOLVENT, g.M_vol, g.M_vol];
    this.Tp = [g.Tp_solvent_C + T0C, g.Tp_network_C + T0C, g.Tp_backbone_C + T0C];
    this.E = [g.E_solvent * 1e3, g.E_network * 1e3, g.E_backbone * 1e3];
    this.kp = this.E.map((E, k) => E * BETA_REF / (R * this.Tp[k] * this.Tp[k]));
    this.Tp_ox = this.Tp.map((T) => T - g.ox_shift_K);
    this.E_ox = [g.E_oxdeg * 1e3, g.E_oxdeg * 1e3, g.E_oxdeg * 1e3];
    this.kp_ox = this.E_ox.map((E, k) => E * BETA_REF / (R * this.Tp_ox[k] * this.Tp_ox[k]));
    this.dHc = g.dHc_MJkg * 1e6;
    this.dHpyr = g.dHpyr_MJkg * 1e6;
    this.Tp_cox = g.Tp_charox_C + T0C;
    this.E_cox = 150e3;
    this.kp_cox = kpFromTpeak(this.Tp_cox, this.E_cox);
    const Sv = 6.0 / this.d32;
    const n_ox = Sv * g.native_oxide_nm * 1e-9 * RHO_CU2O / (2 * M_CU + M_O);
    this.X0 = n_ox / (RHO_CU / M_CU);
    this.E_cuox = g.E_cu_ox * 1e3;
    this.Tp_red = g.Tp_reduction_C + T0C;
    this.E_red = g.E_reduction * 1e3;
    this.kp_red = kpFromTpeak(this.Tp_red, this.E_red);
    this.T_ref_g = 800.0 + T0C;
    this.x_h2o_ref = thermo.x_h2o_from_dewpoint(20.0);
    this.K_inh = 25.0;
    this.k_g_ref = Math.LN2 / (g.t_half_gasif_h * 3600.0);
    this.E_g = g.E_gasif * 1e3;
    this.T_cth = g.T_carbothermic_C + T0C;
    this.E_cth = 180e3;
    this.k_cth_ref = 1e-4;
    this.gamma = g.gamma_s;
    this.f_eta = g.f_eta;
    this.kG = g.kG_mult * KG0;
    this.rho_close = g.rho_close;
    this.C_inh = g.C_inhibit_ppm;
    this.aniso = g.anisotropy;
    this.L0 = g.half_thickness_mm * 1e-3;
    this.V_load = g.load_cm3 * 1e-6;
    this.h_conv = g.h_conv;
    this.ramp_max = g.max_ramp_Kmin / 60.0;
    this.tau_f = g.furnace_lag_min * 60.0;
    this.T_f_max = g.T_furnace_max_C + T0C;
    this.F_in = g.flow_slpm * SLPM_TO_MOLS;
    this.V_r = g.retort_L * 1e-3;
    this.x_o2_imp = g.o2_impurity_ppm * 1e-6;
    this.perm_poly = g.perm_polymer_barrer * 3.35e-16;
    this.eps_c = g.eps_perc;
    this.sig_green = g.sigma_green_MPa * 1e6;
    this.f_int = g.interlayer_factor;
    this.Tg = g.Tg_C + T0C;
    this.r_rub = g.rubbery_ratio;
    this.k_green = g.k_green;
    this.dT_exo = g.dT_exo_max;
    this.ramp_guard = g.debind_ramp_cap_Kmin;
    this.sf_gas = g.sf_gas;
    this.C_spec = g.C_spec_ppm;
    this.O_spec = g.O_spec_ppm;
    this.rho_target = g.rho_target;
    this.T_margin = g.T_margin_K + g.T_uniformity_K;
    this.P_ppm = g.P_ppm;
    this.P_diss = g.P_dissolved_frac;
  }
  Setup.prototype.inorganic_volume = function (X) {
    X = clip(X, 0, 1);
    const v = X <= 0.5 ? V_CU + (V_CU_IN_CU2O - V_CU) * (X / 0.5)
                       : V_CU_IN_CU2O + (V_CU_IN_CUO - V_CU_IN_CU2O) * ((X - 0.5) / 0.5);
    return this.nCu * v;
  };
  Setup.prototype.inorganic_mass = function (X) { return this.mCu + this.nCu * clip(X, 0, 1) * M_O; };
  Setup.prototype.O_ppm = function (X) { return 1e6 * this.nCu * clip(X, 0, 1) * M_O / this.inorganic_mass(X); };
  Setup.prototype.k_cu_ox = function (T) {
    return CUOX_K350 * exp(-(this.E_cuox / R) * (1 / T - 1 / (350 + T0C))) * pow(CUOX_DREF / this.d50, 2);
  };
  Setup.prototype.k_red = function (T) {
    return this.kp_red * exp(-(this.E_red / R) * (1 / T - 1 / this.Tp_red)) * (10e-6 / this.d32);
  };
  Setup.prototype.k_gasif = function (T) { return this.k_g_ref * exp(-(this.E_g / R) * (1 / T - 1 / this.T_ref_g)); };
  Setup.prototype.k_carbothermic = function (T) { return this.k_cth_ref * exp(-(this.E_cth / R) * (1 / T - 1 / this.T_cth)); };
  Setup.prototype.k_char_ox = function (T) { return this.kp_cox * exp(-(this.E_cox / R) * (1 / T - 1 / this.Tp_cox)); };
  Setup.prototype.eta0 = function (T, G) {
    const Dv = DV0 * exp(-QV / (R * T)), dDb = DDB0 * exp(-QB / (R * T));
    return this.f_eta * KB * T * G * G / (42.0 * OMEGA_CU * (Dv + PI * dDb / G));
  };
  Setup.prototype.kG_rate = function (T) { return this.kG * exp(-QB / (R * T)); };
  Setup.prototype.k_eff = function (T, w_b, rho) {
    const neck = clip((rho - this.phi) / (1 - this.phi), 0, 1) + 0.002;
    const k_brown = 0.15 + k_cu(T) * pow(neck, 1.5);
    return w_b * this.k_green + (1 - w_b) * k_brown;
  };
  Setup.prototype.emissivity = function (w_dark, theta) {
    const eps_cu = 0.10 + 0.30 * clip(theta, 0, 0.5);
    return eps_cu + (0.90 - eps_cu) * clip(w_dark, 0, 1);
  };
  Setup.prototype.sigma_green = function (T, a_net) {
    const soft = this.r_rub + (1 - this.r_rub) * sigmoid((this.Tg - T) / 5.0);
    const f = clip(1 - a_net, 0, 1);
    return this.sig_green * soft * f * f;
  };
  Setup.prototype.sigma_brown = function (rho) {
    const neck = clip((rho - this.phi) / (1 - this.phi), 0, 1);
    return 0.3e6 + 60e6 * pow(neck, 1.5);
  };
  Setup.prototype.E_green = function (T, a_net) {
    const soft = this.r_rub + (1 - this.r_rub) * sigmoid((this.Tg - T) / 5.0);
    const f = clip(1 - a_net, 0, 1);
    return 10e9 * soft * f * f + 0.5e9;
  };
  Setup.prototype.iacs = function (rho) {
    return max(0, 101.0 * pow(clip(rho, 0, 1), 1.5) - 0.073 * this.P_ppm * this.P_diss);
  };

  // ------------------------------------------------------------------ controls
  function Controls(t0, t1, Ta, Tb, xO2_in, xH2_in, xH2O_in) {
    this.t0 = t0; this.t1 = t1; this.Ta = Ta; this.Tb = Tb;
    this.xO2_in = xO2_in; this.xH2_in = xH2_in; this.xH2O_in = xH2O_in;
  }
  Controls.prototype.Tset = function (t) {
    if (this.t1 <= this.t0) return this.Tb;
    const f = clip((t - this.t0) / (this.t1 - this.t0), 0, 1);
    return this.Ta + f * (this.Tb - this.Ta);
  };

  // ------------------------------------------------------------------ the slab model (T1)
  function Slab(su, N) {
    this.su = su;
    this.N = N || (su.s.n_nodes | 0);
    const n = this.N;
    this.n = NV * n + NG;
    const w = new Float64Array(n);
    let sum = 0;
    for (let i = 0; i < n; i++) { w[i] = pow(MESH_GRADE, n - 1 - i); sum += w[i]; }
    for (let i = 0; i < n; i++) w[i] = w[i] / sum * su.L0;
    this.w = w;
    this.dface = new Float64Array(n - 1);
    for (let i = 0; i < n - 1; i++) this.dface[i] = 0.5 * (w[i] + w[i + 1]);
    this.wt = new Float64Array(n);
    for (let i = 0; i < n; i++) this.wt[i] = w[i] / su.L0;
    this.Vb0 = su.mb0 / su.rho_b;
    this.b_net0 = (su.b0[1] + su.b0[2]) / su.mb0;
    this.theta0 = 1 - su.phi;
    // pores within ~1-3 particle diameters of the free surface vent to it and cannot trap gas
    this.trapDepth = new Float64Array(n);
    { let xc = 0; for (let i = 0; i < n; i++) { const c = xc + 0.5 * w[i]; xc += w[i];
        this.trapDepth[i] = smoothstep(((su.L0 - c) - su.d50) / (2 * su.d50)); } }
    const scN = [300, 1, 1, 1, 1, 0.01, 0.01, 0.01, 10, 1], scG = [300, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01];
    const atN = [1e-3, 1e-7, 1e-7, 1e-7, 1e-6, 1e-8, 1e-9, 1e-8, 1e-5, 1e-7];
    const atG = [1e-3, 1e-9, 1e-9, 1e-9, 1e-9, 1e-9, 1e-8];
    this.scale = new Float64Array(this.n);
    this.atol = new Float64Array(this.n);
    for (let v = 0; v < NV; v++) for (let i = 0; i < n; i++) { this.scale[v * n + i] = scN[v]; this.atol[v * n + i] = atN[v]; }
    for (let g = 0; g < NG; g++) { this.scale[NV * n + g] = scG[g]; this.atol[NV * n + g] = atG[g]; }
    // workspace
    const W = {};
    for (const k of ["T", "y", "s", "kk", "ctot", "Deff", "ndot", "R_O2", "q", "Ccap", "wdark", "theta", "V",
                     "eps", "eps_open", "rho_s", "a_net", "fcl", "Cppm", "pg", "PL", "Xn", "cn", "wb", "rho_m",
                     "eta", "edot", "J", "nvol", "nredopen", "rg", "rcth", "rco", "rosum", "nred", "dez", "Gum"])
      W[k] = new Float64Array(n);
    this.W = W;
  }

  Slab.prototype.y0 = function (T0K, x_in) {
    const su = this.su, n = this.N, Y = new Float64Array(this.n);
    const b = su.b0.slice();
    let rem = (su.s.pre_extracted_frac || 0) * su.mb0;
    for (let k = 0; k < 3; k++) { const take = min(b[k], rem); b[k] -= take; rem -= take; }
    for (let i = 0; i < n; i++) {
      Y[IT * n + i] = T0K;
      Y[IB1 * n + i] = b[0] / su.mb0;
      Y[IB2 * n + i] = b[1] / su.mb0;
      Y[IB3 * n + i] = b[2] / su.mb0;
      Y[IC * n + i] = 0;
      Y[IX * n + i] = su.X0;
      Y[IY * n + i] = x_in[0];
      Y[ILV * n + i] = 0;
      Y[IG * n + i] = su.G0 * 1e6;
      Y[INT * n + i] = 0;
    }
    const g = NV * n;
    Y[g + GTF] = T0K; Y[g + GO2] = x_in[0]; Y[g + GH2] = x_in[1]; Y[g + GH2O] = x_in[2];
    Y[g + GCO] = 0; Y[g + GCO2] = 0; Y[g + GEZ] = 0;
    return Y;
  };

  /** dY/dt into `out`. With wantDiag returns a diagnostics object. */
  Slab.prototype.evaluate = function (t, Y, ctl, out, wantDiag) {
    const su = this.su, n = this.N, w = this.w, dface = this.dface, wt = this.wt, W = this.W;
    const g0 = NV * n;
    const Tf = Y[g0 + GTF];
    const xO2r = pos(Y[g0 + GO2], 1e-12), xH2r = pos(Y[g0 + GH2], 1e-12), xH2Or = pos(Y[g0 + GH2O], 1e-12);
    const xCOr = pos(Y[g0 + GCO], 1e-12), xCO2r = pos(Y[g0 + GCO2], 1e-12);
    const chi_f = 1.0 - 0.36 * xH2r;
    const fH2 = 2.0 * xH2r / (xH2r + 0.04);
    const inh = (1.0 + su.K_inh * 0.04) / (1.0 + su.K_inh * xH2r);
    const Qst = xCOr * xH2r / max(xH2Or, 1e-12);
    const ratio = xH2Or / max(xH2r, 1e-12);
    const sqh2o = sqrt(xH2Or / su.x_h2o_ref);
    const x_insol = 1.0 - xH2r;
    const aN = su.aniso;
    let S_nred_open = 0, S_ro = 0, S_rg = 0, S_nred = 0, S_esc_cth = 0, S_rco = 0, S_nvol = 0, dez = 0;

    for (let i = 0; i < n; i++) {
      const T = Y[IT * n + i];
      const b1 = Y[IB1 * n + i], b2 = Y[IB2 * n + i], b3 = Y[IB3 * n + i];
      const B1 = pos(b1, 1e-12) * su.mb0, B2 = pos(b2, 1e-12) * su.mb0, B3 = pos(b3, 1e-12) * su.mb0;
      const c = pos(Y[IC * n + i], 1e-9);
      const X = min(pos(Y[IX * n + i], 1e-9), 1.0);
      const y = min(pos(Y[IY * n + i], 1e-12), 1.0);
      const lnV = Y[ILV * n + i];
      const V = exp(lnV);
      const G = max(Y[IG * n + i], 1e-3) * 1e-6;
      const ntr = max(Y[INT * n + i], 0.0);

      const Vsol = su.inorganic_volume(X);
      const Vb = (B1 + B2 + B3) / su.rho_b;
      const Vc = c / RHO_CHAR;
      const eps = clip(1 - (Vsol + Vb + Vc) / V, 0, 1);
      const rho_s = clip(Vsol / V, 1e-3, 0.99999);
      const theta = 1 - rho_s;
      const rho_m = clip(su.nCu * V_CU / V, 1e-3, 0.99999);
      const u_cl = (rho_m - (su.rho_close - 0.03)) / 0.06;
      const f_cl = smoothstep(u_cl);
      const eps_open = eps * (1 - f_cl);
      const w_b = clip(Vb / this.Vb0, 0, 1);
      const a_net = 1 - (b2 + b3) / this.b_net0;
      const acc = eps_open / (eps_open + EPS_ACC);
      const m_inorg = su.inorganic_mass(X);
      const C_ppm = 1e6 * c / m_inorg;

      // binder
      const iT = 1 / T;
      const rp0 = su.kp[0] * exp(-(su.E[0] / R) * (iT - 1 / su.Tp[0])) * B1;
      const rp1 = su.kp[1] * exp(-(su.E[1] / R) * (iT - 1 / su.Tp[1])) * B2;
      const rp2 = su.kp[2] * exp(-(su.E[2] / R) * (iT - 1 / su.Tp[2])) * B3;
      const yo = y / 0.21;
      const ro1 = su.kp_ox[1] * exp(-(su.E_ox[1] / R) * (iT - 1 / su.Tp_ox[1])) * B2 * yo;
      const ro2 = su.kp_ox[2] * exp(-(su.E_ox[2] / R) * (iT - 1 / su.Tp_ox[2])) * B3 * yo;
      const char_form = (su.chi[0] * rp0 + su.chi[1] * rp1 + su.chi[2] * rp2) * chi_f;
      const r_co = su.k_char_ox(T) * c * yo * (1 - f_cl);

      // copper oxide & carbon chemistry
      const pO2eq = pO2eqCu(T);
      const th_ox = pos(1 - sqrt(pO2eq / max(y, 1e-30)), 0.01);
      const fy = pow(yo, 1 / 7) * y / (y + Y_SMALL);
      const dX_ox = su.k_cu_ox(T) * fy * th_ox * pos(1 - X, 1e-6) / pow(X + CUOX_X0, CUOX_M) * (1 - f_cl);
      const th_red = pos(1 - ratio / boundaryCu(T), 0.01);
      const hot = sigmoid((T - 600) / 20);
      const k_rX = su.k_red(T) * X * fH2 * th_red;
      const rX_open = acc * (1 - f_cl) * k_rX;
      const rX_closed = f_cl * hot * k_rX;
      const rX_red = rX_open + rX_closed;
      const th_g = pos(1 - Qst / Ksteam(T), 0.01);
      const r_g = acc * (1 - f_cl) * su.k_gasif(T) * (c / M_C) * sqh2o * inh * th_g;
      const r_cth = su.k_carbothermic(T) * (c / M_C) * X / (X + X_SWITCH);

      const dXdt = dX_ox - rX_red - r_cth / su.nCu;
      const dcdt = char_form - r_co - M_C * (r_g + r_cth);
      const rosum = ro1 + ro2;
      const n_vol = rp0 * (1 - su.chi[0] * chi_f) / su.Mgas[0] + rp1 * (1 - su.chi[1] * chi_f) / su.Mgas[1]
                  + rp2 * (1 - su.chi[2] * chi_f) / su.Mgas[2];
      const n_ox_net = (N_CO2_BINDER + N_H2O_BINDER - NU_O2_BINDER) * rosum;
      const n_red = su.nCu * rX_red, n_red_open = su.nCu * rX_open, n_red_closed = su.nCu * rX_closed;
      const ndot = n_vol + n_ox_net - 0.5 * su.nCu * dX_ox + r_g + r_cth;
      const R_O2 = NU_O2_BINDER * rosum + r_co / M_C + 0.5 * su.nCu * dX_ox;

      const q = -0.4e6 * rp0 - su.dHpyr * (rp1 + rp2) + su.dHc * rosum + DH_CHAR_OX * r_co / M_C
              + DH_CU_OX * su.nCu * dX_ox + DH_RED_H2 * n_red - DH_CARBOTHERMIC * r_cth - DH_GASIF * r_g;
      const Ccap = m_inorg * cp_cu(T) + (B1 + B2 + B3) * CP_BINDER + c * CP_CHAR;
      const s = exp(lnV / 3);
      const kk = su.k_eff(T, w_b, rho_s);
      const wdark = max(w_b, max(clip(C_ppm / 300, 0, 1), clip(X / 0.02, 0, 1)));

      const ctot = P_ATM / (R * T);
      const d_pore = max((2 / 3) * eps_open / max(1 - eps_open, 1e-3) * su.d32, 1e-9);
      const DKn = d_pore / 3 * sqrt(8 * R * T / (PI * M_O2));
      const Dm = 1 / (1 / D_O2_N2(T) + 1 / DKn);
      const Deff = pow(eps_open, 1.5) * Dm + D_POLY_O2 * w_b;

      // sintering
      const th = clip(theta, 1e-4, 0.999);
      const psi = (2 / 3) * pow(1 - th, 3) / th;
      const phi_s = (1 - th) * (1 - th);
      const PL = 3 * su.gamma / su.r_s * (1 - th) * (1 - th);
      const Vcl = f_cl * eps * V + 1e-4 * pos(eps, 1e-6) * V + 1e-9;
      const p_g = ntr * R * T / Vcl;
      const dP_raw = f_cl * (p_g - P_ATM);
      const dP = 3 * PL * tanh(dP_raw / (3 * PL));
      const Cr = C_ppm / su.C_inh;
      const eta = su.eta0(T, G) * (1 + Cr * Cr) * (1 + 1e4 * w_b);
      const e_dot = -(PL - dP) / (2 * eta * psi);
      const dvdX = (X < 0.5 ? (V_CU_IN_CU2O - V_CU) / 0.5 : (V_CU_IN_CUO - V_CU_IN_CU2O) / 0.5) * su.nCu;
      const swell = smoothstep((0.04 - eps) / 0.04) * dvdX * dXdt / V;
      const dlnVdt = e_dot + swell;
      const pin = THETA_PIN / (th + THETA_PIN);
      const dGdt = 1e6 * su.kG_rate(T) / (3 * G * G) * pin * pin;
      const drho = -rho_m * dlnVdt;
      const uc = clip(u_cl, 0, 1);
      const dfcl = 6 * uc * (1 - uc) / 0.06 * drho;
      const dep = this.trapDepth[i];
      const trap = dep * (P_ATM / (R * T)) * x_insol * eps * V * pos(dfcl, 1e-12);
      const gen_cl = dep * (n_red_closed + f_cl * r_cth);
      const release = ntr * pos(-dfcl, 1e-12) / max(f_cl, 1e-3) + ntr * (1 - smoothstep(f_cl / 0.01)) * 1e-3;
      const dntr = trap + gen_cl - release;
      const dez_node = -PL * aN * (th / this.theta0) * (2 / 3) / (2 * eta * phi_s);

      out[IB1 * n + i] = -rp0 / su.mb0;
      out[IB2 * n + i] = (-rp1 - ro1) / su.mb0;
      out[IB3 * n + i] = (-rp2 - ro2) / su.mb0;
      out[IC * n + i] = dcdt;
      out[IX * n + i] = dXdt;
      out[ILV * n + i] = dlnVdt;
      out[IG * n + i] = dGdt;
      out[INT * n + i] = dntr;

      W.T[i] = T; W.y[i] = y; W.s[i] = s; W.kk[i] = kk; W.ctot[i] = ctot; W.Deff[i] = Deff; W.ndot[i] = ndot;
      W.R_O2[i] = R_O2; W.q[i] = q; W.Ccap[i] = Ccap; W.wdark[i] = wdark; W.theta[i] = theta; W.V[i] = V;
      W.eps[i] = eps; W.eps_open[i] = eps_open; W.rho_s[i] = rho_s; W.a_net[i] = a_net; W.fcl[i] = f_cl;
      W.Cppm[i] = C_ppm; W.pg[i] = p_g; W.PL[i] = PL; W.Xn[i] = X; W.cn[i] = c; W.wb[i] = w_b; W.rho_m[i] = rho_m;
      W.eta[i] = eta; W.edot[i] = e_dot; W.nvol[i] = n_vol; W.Gum[i] = G * 1e6;

      const wi = wt[i];
      S_nred_open += wi * n_red_open; S_ro += wi * rosum; S_rg += wi * r_g; S_nred += wi * n_red;
      S_esc_cth += wi * (1 - f_cl) * r_cth; S_rco += wi * r_co; S_nvol += wi * n_vol; dez += wi * dez_node;
    }

    // ---- heat conduction
    const Tn1 = W.T[n - 1];
    const epsr = su.emissivity(W.wdark[n - 1], W.theta[n - 1]);
    const h_rad = epsr * SIGMA_SB * (Tf * Tf + Tn1 * Tn1) * (Tf + Tn1);
    const h_cv = su.h_conv * pow(1 + 6 * xH2r, 0.7);
    const h_tot = h_cv + h_rad;
    const sN = W.s[n - 1];
    const Rs = 1 / h_tot + 0.5 * w[n - 1] * sN / W.kk[n - 1];
    const Qs = sN * sN * (Tf - Tn1) / Rs;
    // ---- O2 transport with blowing
    let Jc = 0;
    for (let i = 0; i < n; i++) { Jc += W.ndot[i] * w[i]; W.J[i] = Jc; }
    const ctg = P_ATM / (R * Tf);
    const k_m = h_cv / (ctg * 29.1);
    const Rsm = 1 / (k_m * ctg) + 0.5 * w[n - 1] * sN / (W.Deff[n - 1] * W.ctot[n - 1]);
    const Js = W.J[n - 1];
    const yN = W.y[n - 1];
    const Ns = sN * sN * (xO2r - yN) / Rsm - max(Js, 0) * yN + max(-Js, 0) * xO2r;
    for (let i = 0; i < n; i++) { out[IT * n + i] = 0; out[IY * n + i] = 0; }
    for (let i = 0; i < n - 1; i++) {
      const kf = 2 * W.kk[i] * W.kk[i + 1] / (W.kk[i] + W.kk[i + 1]);
      const sf = 0.5 * (W.s[i] + W.s[i + 1]);
      const dist = dface[i] * sf;
      const Qf = sf * sf * kf * (W.T[i + 1] - W.T[i]) / dist;
      out[IT * n + i] += Qf; out[IT * n + i + 1] -= Qf;
      const Df = 2 * W.Deff[i] * W.Deff[i + 1] / (W.Deff[i] + W.Deff[i + 1]);
      const cf = 0.5 * (W.ctot[i] + W.ctot[i + 1]);
      const Nd = sf * sf * Df * cf * (W.y[i + 1] - W.y[i]) / dist;
      const Jf = W.J[i];
      const Na = -max(Jf, 0) * W.y[i] + max(-Jf, 0) * W.y[i + 1];
      out[IY * n + i] += Nd + Na; out[IY * n + i + 1] -= Nd + Na;
    }
    out[IT * n + n - 1] += Qs;
    out[IY * n + n - 1] += Ns;
    for (let i = 0; i < n; i++) {
      out[IT * n + i] = (out[IT * n + i] / w[i] + W.q[i]) / W.Ccap[i];
      const Cg = (W.eps_open[i] + 0.01) * W.ctot[i] * W.V[i];
      out[IY * n + i] = (out[IY * n + i] / w[i] - W.R_O2[i]) / Cg;
    }

    // ---- furnace and retort
    const Tset = ctl.Tset(t);
    const dTf = su.ramp_max * tanh((Tset - Tf) / (su.tau_f * su.ramp_max));
    const Nr = P_ATM * su.V_r / (R * Tf);
    const vol = su.V_load;
    let S_O2 = -vol * Ns / su.L0;
    let S_H2O = vol * (S_nred_open + N_H2O_BINDER * S_ro - S_rg);
    let S_H2 = vol * (-S_nred + S_rg);
    const S_CO = vol * (S_rg + S_esc_cth);
    let S_CO2 = vol * (N_CO2_BINDER * S_ro + S_rco / M_C);
    let S_HC = vol * S_nvol;
    const Mv = su.s.M_vol;
    const nu_hc = NU_O2_BINDER * Mv;
    const f_gc = sigmoid((Tf - (350 + T0C)) / 15);
    const r_gc = f_gc * nu_hc * S_HC * xO2r / (xO2r + 1e-3);
    const burnt = r_gc / nu_hc;
    const r_rec = 50 * sigmoid((Tf - 473.15) / 20) * Nr * xH2r * xO2r;
    S_O2 = S_O2 - r_gc - 0.5 * r_rec;
    S_H2 = S_H2 - r_rec;
    S_H2O = S_H2O + r_rec + N_H2O_BINDER * Mv * burnt;
    S_CO2 = S_CO2 + N_CO2_BINDER * Mv * burnt;
    S_HC = S_HC - burnt;
    const S_tot = S_O2 + S_H2 + S_H2O + S_CO + S_CO2 + S_HC;
    const Fin = su.F_in;
    out[g0 + GTF] = dTf;
    out[g0 + GO2] = (Fin * (ctl.xO2_in - xO2r) + S_O2 - xO2r * S_tot) / Nr;
    out[g0 + GH2] = (Fin * (ctl.xH2_in - xH2r) + S_H2 - xH2r * S_tot) / Nr;
    out[g0 + GH2O] = (Fin * (ctl.xH2O_in - xH2Or) + S_H2O - xH2Or * S_tot) / Nr;
    out[g0 + GCO] = (Fin * (0 - xCOr) + S_CO - xCOr * S_tot) / Nr;
    out[g0 + GCO2] = (Fin * (0 - xCO2r) + S_CO2 - xCO2r * S_tot) / Nr;
    out[g0 + GEZ] = dez;
    if (!wantDiag) return null;

    // ---- diagnostics
    let dPhi = 0;
    const dp = new Float64Array(n);
    let Pi_gas = -Infinity, Tmax = -Infinity, Tmin = Infinity;
    for (let i = 0; i < n; i++) { Tmax = max(Tmax, W.T[i]); Tmin = min(Tmin, W.T[i]); }
    const dT_int = Tmax - Tmin;
    for (let i = n - 1; i >= 0; i--) {
      const T = W.T[i], eps = W.eps[i], mu = mu_gas(T);
      const dK = max((2 / 3) * eps / max(1 - eps, 1e-3) * su.d32, 1e-9);
      const K_kc = pow(eps, 3) * su.d32 * su.d32 / (180 * pow(max(1 - eps, 1e-3), 2));
      const K_kn = pow(eps, 1.5) * dK / 3 * sqrt(8 * R * T / (PI * Mv)) * mu / P_ATM;
      const perc = sigmoid((W.eps_open[i] - su.eps_c) / 0.005);
      const K_poly = su.perm_poly * mu * R * T / P_ATM;
      const K_app = perc * (K_kc + K_kn) + K_poly;
      const gface = 2 * mu * R * T * max(W.J[i], 0) / K_app;
      dPhi += gface * w[i] * W.s[i];
      dp[i] = dPhi / (sqrt(P_ATM * P_ATM + dPhi) + P_ATM);   // sqrt(P^2+d)-P without cancellation
    }
    let Pi_th = -Infinity, melt = Infinity, Pi_bloat = -Infinity, qmax = -Infinity;
    for (let i = 0; i < n; i++) qmax = max(qmax, W.q[i]);
    for (let i = 0; i < n; i++) {
      const T = W.T[i];
      const sg = su.sigma_green(T, W.a_net[i]), sb = su.sigma_brown(W.rho_s[i]);
      const sig_t = sg + sb, sig_tz = su.f_int * sg + sb;
      Pi_gas = max(Pi_gas, su.sf_gas * dp[i] / sig_tz);
      const sig_th = su.E_green(T, W.a_net[i]) * 30e-6 * (2 / 3) * dT_int / 0.7;
      Pi_th = max(Pi_th, sig_th / sig_t);
      const Oppm = su.O_ppm(W.Xn[i]);
      melt = min(melt, (thermo.T_solidus_Cu_O(Oppm) - su.T_margin) - T);
      const pb = W.fcl[i] >= 0.5 ? (W.pg[i] - P_ATM) / W.PL[i] : 0;
      Pi_bloat = max(Pi_bloat, pb);
    }
    const S_totp = max(S_tot, 0);
    return {
      Tf, Tset, T: Array.from(W.T), Tmax, exo: Tmax - Tf, exo_gen: qmax > 1e3 ? Tmax - Tf : -Infinity, dT_int, Pi_gas, Pi_th, melt, Pi_bloat,
      C_ppm: Array.from(W.Cppm), X: Array.from(W.Xn), O_ppm: Array.from(W.Xn, (x) => su.O_ppm(x)),
      rho: Array.from(W.rho_s), f_cl: Array.from(W.fcl), eps_open: Array.from(W.eps_open),
      p_g: Array.from(W.pg), G_um: Array.from(W.Gum), y: Array.from(W.y), dp_gas: Array.from(dp),
      wb: Array.from(W.wb), a_net: Array.from(W.a_net),
      xO2: xO2r, xH2: xH2r, xH2O: xH2Or, xCO: xCOr, xCO2: xCO2r,
      x_hc: max(S_HC, 0) / (Fin + S_totp), h_tot,
    };
  };

  // ------------------------------------------------------------------ linear algebra & integrator
  function luFactor(A, n, piv) {
    for (let k = 0; k < n; k++) {
      let p = k, m = abs(A[k * n + k]);
      for (let i = k + 1; i < n; i++) { const v = abs(A[i * n + k]); if (v > m) { m = v; p = i; } }
      piv[k] = p;
      if (m === 0) throw new Error("singular matrix");
      if (p !== k) for (let j = 0; j < n; j++) { const tmp = A[k * n + j]; A[k * n + j] = A[p * n + j]; A[p * n + j] = tmp; }
      const akk = A[k * n + k];
      for (let i = k + 1; i < n; i++) {
        const f = (A[i * n + k] /= akk);
        if (f !== 0) { const ri = i * n, rk = k * n; for (let j = k + 1; j < n; j++) A[ri + j] -= f * A[rk + j]; }
      }
    }
  }
  function luSolve(A, n, piv, b, x) {
    for (let i = 0; i < n; i++) x[i] = b[i];
    for (let k = 0; k < n; k++) { const p = piv[k]; if (p !== k) { const t = x[k]; x[k] = x[p]; x[p] = t; } }
    for (let i = 1; i < n; i++) { let s = x[i]; const ri = i * n; for (let j = 0; j < i; j++) s -= A[ri + j] * x[j]; x[i] = s; }
    for (let i = n - 1; i >= 0; i--) { let s = x[i]; const ri = i * n; for (let j = i + 1; j < n; j++) s -= A[ri + j] * x[j]; x[i] = s / A[ri + i]; }
  }

  const D_ROS = 1 / (2 + Math.SQRT2), E32 = 6 + Math.SQRT2;
  class StepFailure extends Error {}

  function ode23s(f, t0, t1, y0, atol, rtol, opts) {
    opts = opts || {};
    const n = y0.length, scale = opts.scale;
    let y = Float64Array.from(y0);
    let t = t0;
    const span = t1 - t0;
    const ts = [t], ys = [Float64Array.from(y)];
    if (span <= 0) return { ts, ys, nstep: 0, nrej: 0, hLast: opts.h0 };
    const F0 = new Float64Array(n), F1 = new Float64Array(n), F2 = new Float64Array(n), Ft = new Float64Array(n);
    const k1 = new Float64Array(n), k2 = new Float64Array(n), k3 = new Float64Array(n);
    const tmp = new Float64Array(n), rhs = new Float64Array(n), yn = new Float64Array(n), yp = new Float64Array(n);
    const J = new Float64Array(n * n), Wm = new Float64Array(n * n), piv = new Int32Array(n), Fp = new Float64Array(n);
    f(t, y, F0);
    let h;
    if (opts.h0 == null) {
      let d0 = 0, d1 = 0;
      for (let i = 0; i < n; i++) { const sc = atol[i] + rtol * abs(y[i]); d0 += (y[i] / sc) ** 2; d1 += (F0[i] / sc) ** 2; }
      d0 = sqrt(d0 / n); d1 = sqrt(d1 / n);
      h = (d0 > 1e-5 && d1 > 1e-5) ? 0.01 * d0 / d1 : 1e-3;
      h = min(max(h, 1e-6), 0.1 * span);
    } else h = min(opts.h0, span);
    const hmax = opts.hmax || Infinity;
    const jacEvery = opts.jacEvery || 1;
    let nstep = 0, nrej = 0, err = 1, sinceJac = 0, haveJ = false;
    const eps64 = 2.220446049250313e-16;
    const refreshJ = () => {
      // finite-difference Jacobian (column by column) and time derivative
      for (let j = 0; j < n; j++) {
        const dy = 1e-7 * max(abs(y[j]), scale[j]);
        yp.set(y); yp[j] += dy;
        f(t, yp, Fp);
        for (let i = 0; i < n; i++) J[i * n + j] = (Fp[i] - F0[i]) / dy;
      }
      const dtfd = 1e-7 * max(abs(t), 1.0);
      f(t + dtfd, y, Ft);
      for (let i = 0; i < n; i++) Ft[i] = (Ft[i] - F0[i]) / dtfd;
      sinceJac = 0; haveJ = true;
    };
    while (t < t1) {
      if (nstep > (opts.maxSteps || 200000)) throw new StepFailure("too many steps at t=" + t.toFixed(1));
      h = min(h, hmax, t1 - t);
      if (t + 1.01 * h >= t1) h = t1 - t;
      if (!haveJ || sinceJac >= jacEvery) refreshJ();
      let fresh = sinceJac === 0;
      for (;;) {
        for (let i = 0; i < n * n; i++) Wm[i] = -h * D_ROS * J[i];
        for (let i = 0; i < n; i++) Wm[i * n + i] += 1;
        luFactor(Wm, n, piv);
        for (let i = 0; i < n; i++) rhs[i] = F0[i] + h * D_ROS * Ft[i];
        luSolve(Wm, n, piv, rhs, k1);
        for (let i = 0; i < n; i++) tmp[i] = y[i] + 0.5 * h * k1[i];
        f(t + 0.5 * h, tmp, F1);
        for (let i = 0; i < n; i++) rhs[i] = F1[i] - k1[i];
        luSolve(Wm, n, piv, rhs, k2);
        for (let i = 0; i < n; i++) { k2[i] += k1[i]; yn[i] = y[i] + h * k2[i]; }
        f(t + h, yn, F2);
        for (let i = 0; i < n; i++) rhs[i] = F2[i] - E32 * (k2[i] - F1[i]) - 2 * (k1[i] - F0[i]) + h * D_ROS * Ft[i];
        luSolve(Wm, n, piv, rhs, k3);
        err = 0;
        let finite = true;
        for (let i = 0; i < n; i++) {
          const e = (h / 6) * (k1[i] - 2 * k2[i] + k3[i]);
          const sc = atol[i] + rtol * max(abs(y[i]), abs(yn[i]));
          const r = abs(e) / sc;
          if (!(r <= 1e300) || !isFinite(yn[i])) finite = false;
          if (r > err) err = r;
        }
        if (!finite) err = 1e10;
        if (err <= 1.0) break;
        nrej++;
        if (!fresh) { refreshJ(); fresh = true; continue; }   // stale Jacobian: refresh before shrinking h
        h = h * max(0.1, 0.8 * pow(err, -1 / 3));
        if (h < 64 * eps64 * max(1, abs(t))) throw new StepFailure("step size underflow at t=" + t.toFixed(3));
      }
      t = t + h;
      y.set(yn);
      F0.set(F2);
      nstep++;
      sinceJac++;
      ts.push(t); ys.push(Float64Array.from(y));
      if (opts.callback && opts.callback(t, y)) break;
      h = h * min(5, max(0.2, 0.8 * pow(max(err, 1e-10), -1 / 3)));
    }
    return { ts, ys, nstep, nrej, hLast: ts.length > 1 ? ts[ts.length - 1] - ts[ts.length - 2] : null };
  }

  // ------------------------------------------------------------------ cycles
  function Segment(T_end_C, ramp_Kmin, hold_h, O2, H2, dp_C, note) {
    return { T_end_C, ramp_Kmin, hold_h: hold_h || 0, O2: O2 || 0, H2: H2 || 0, dp_C: dp_C == null ? -60 : dp_C, note: note || "" };
  }
  function cycleBoundaries(cyc) {
    const out = [];
    let t = 0, T = cyc.T_start_C == null ? 25 : cyc.T_start_C;
    for (const sg of cyc.segments) {
      const dT = sg.T_end_C - T;
      if (abs(dT) > 1e-9) {
        const rate = max(sg.ramp_Kmin, 1e-6) / 60;
        const dt = abs(dT) / rate;
        out.push([t, t + dt, sg, T, "ramp"]); t += dt;
      }
      if (sg.hold_h > 0) { out.push([t, t + sg.hold_h * 3600, sg, sg.T_end_C, "hold"]); t += sg.hold_h * 3600; }
      T = sg.T_end_C;
    }
    return out;
  }
  function cycleDurationH(cyc) { const b = cycleBoundaries(cyc); return b.length ? b[b.length - 1][1] / 3600 : 0; }
  function cycleTsetK(cyc, t, bounds) {
    bounds = bounds || cycleBoundaries(cyc);
    for (const [t0, t1, sg, Tfrom, kind] of bounds) {
      if (t <= t1) {
        if (kind === "hold") return sg.T_end_C + T0C;
        const f = (t - t0) / max(t1 - t0, 1e-12);
        return Tfrom + f * (sg.T_end_C - Tfrom) + T0C;
      }
    }
    return cyc.segments[cyc.segments.length - 1].T_end_C + T0C;
  }
  function baselineV0() {
    return { name: "v0 envelope", T_start_C: 25, segments: [
      Segment(80, 0.5, 4.0, 0.0, 0.0, -60, "solvent removal"),
      Segment(150, 0.1, 12.0, 0.0, 0.0, -60, "solvent, evaporation-limited"),
      Segment(205, 0.1, 8.0, 0.0, 0.0, -60, "onset of scission"),
      Segment(300, 0.05, 6.0, 0.002, 0.0, -60, "throttled burn"),
      Segment(400, 0.05, 4.0, 0.002, 0.0, -60, "throttled burn"),
      Segment(450, 0.2, 1.0, 0.0, 0.0, -60, "complete pyrolysis, purge"),
      Segment(800, 2.0, 8.0, 0.0, 0.001, 40, "wet-H2 gasification + reduction"),
      Segment(1040, 3.0, 3.0, 0.0, 0.04, -60, "densification"),
      Segment(600, 3.0, 0.0, 0.0, 0.04, -60, "reducing cool"),
      Segment(25, 5.0, 0.0, 0.0, 0.0, -60, "inert cool"),
    ] };
  }

  function inletComposition(sg, su) {
    let xo2 = su.s.has_air_bleed >= 0.5 ? min(max(sg.O2, 0), 0.2095) : 0;
    xo2 = xo2 + su.x_o2_imp * (1 - xo2 / 0.2095);
    const xh2 = min(max(sg.H2, 0), su.s.h2_max);
    const dp = min(sg.dp_C, su.s.dp_max_C);
    const xh2o = thermo.x_h2o_from_dewpoint(dp > -60 ? dp : -60);
    return [xo2, xh2, xh2o];
  }

  // ------------------------------------------------------------------ simulate + postprocess
  function simulate(scenario, cyc, opts) {
    opts = opts || {};
    const su = new Setup(scenario);
    const sl = new Slab(su, opts.N);
    const rtol = opts.rtol || 1e-3;
    const bounds = cycleBoundaries(cyc);
    let Y = sl.y0((cyc.T_start_C == null ? 25 : cyc.T_start_C) + T0C, inletComposition(bounds[0][2], su));
    const ts = [0], ys = [Float64Array.from(Y)], segOf = [0];
    let h = null, ok = true, message = "", nstep = 0;
    const f0 = (ctl) => (t, y, out) => sl.evaluate(t, y, ctl, out, false);
    for (let k = 0; k < bounds.length; k++) {
      const [t0, t1, sg, Tfrom, kind] = bounds[k];
      const [xo2, xh2, xh2o] = inletComposition(sg, su);
      const Ta = (kind === "ramp" ? Tfrom : sg.T_end_C) + T0C;
      const ctl = new Controls(t0, t1, Ta, sg.T_end_C + T0C, xo2, xh2, xh2o);
      let r;
      try {
        r = ode23s(f0(ctl), t0, t1, Y, sl.atol, rtol, { scale: sl.scale, h0: h, hmax: max(600, 0.02 * (t1 - t0)),
                                                       jacEvery: opts.jacEvery || 1 });
      } catch (e) {
        ok = false; message = "integration failed in segment '" + sg.note + "' (" + kind + "): " + e.message; break;
      }
      nstep += r.nstep;
      for (let i = 1; i < r.ts.length; i++) { ts.push(r.ts[i]); ys.push(r.ys[i]); segOf.push(k); }
      Y = r.ys[r.ys.length - 1];
      h = r.ts.length > 1 ? min(max(r.ts[r.ts.length - 1] - r.ts[r.ts.length - 2], 1), 600) : null;
      if (opts.onSegment) opts.onSegment(k + 1, bounds.length);
    }
    const pp = postprocess(sl, cyc, bounds, ts, ys, segOf);
    pp.ok = ok; pp.message = message; pp.nstep = nstep; pp.cycle = cyc;
    return pp;
  }

  function postprocess(sl, cyc, bounds, ts, ys, segOf) {
    const su = sl.su, n = sl.N, wt = sl.wt, M = ts.length;
    const S = {};
    const keys = ["Tset", "Tf", "T_center", "T_surface", "exo", "dT_int", "binder_left", "C_ppm_center", "C_ppm_mean",
                  "O_ppm_center", "O_ppm_mean", "rho_center", "rho_surface", "rho_mean", "eps_open", "f_cl_center",
                  "G_um", "p_trap_bar", "exo_gen", "y_center", "dp_gas_bar", "Pi_gas", "Pi_th", "Pi_bloat", "melt_margin",
                  "xO2", "xH2", "xH2O", "xCO", "xCO2", "x_hc", "shrink_xy", "shrink_z", "dewpoint_out"];
    for (const k of keys) S[k] = new Float64Array(M);
    const out = new Float64Array(sl.n);
    const wmean = (a) => { let s = 0; for (let i = 0; i < n; i++) s += a[i] * wt[i]; return s; };
    for (let m = 0; m < M; m++) {
      const [t0, t1, sg, Tfrom, kind] = bounds[min(segOf[m], bounds.length - 1)];
      const [xo2, xh2, xh2o] = inletComposition(sg, su);
      const ctl = new Controls(t0, t1, (kind === "ramp" ? Tfrom : sg.T_end_C) + T0C, sg.T_end_C + T0C, xo2, xh2, xh2o);
      const Y = ys[m];
      const d = sl.evaluate(ts[m], Y, ctl, out, true);
      S.Tset[m] = cycleTsetK(cyc, ts[m], bounds) - T0C;
      S.Tf[m] = d.Tf - T0C; S.T_center[m] = d.T[0] - T0C; S.T_surface[m] = d.T[n - 1] - T0C;
      S.exo[m] = d.exo; S.exo_gen[m] = d.exo_gen; S.dT_int[m] = d.dT_int;
      let bl = 0;
      for (let i = 0; i < n; i++) bl += (Y[IB1 * n + i] + Y[IB2 * n + i] + Y[IB3 * n + i]) * wt[i];
      S.binder_left[m] = bl;
      S.C_ppm_center[m] = d.C_ppm[0]; S.C_ppm_mean[m] = wmean(d.C_ppm);
      S.O_ppm_center[m] = d.O_ppm[0]; S.O_ppm_mean[m] = wmean(d.O_ppm);
      S.rho_center[m] = d.rho[0]; S.rho_surface[m] = d.rho[n - 1]; S.rho_mean[m] = wmean(d.rho);
      S.eps_open[m] = wmean(d.eps_open); S.f_cl_center[m] = d.f_cl[0]; S.G_um[m] = wmean(d.G_um);
      S.p_trap_bar[m] = d.p_g[0] / 1e5; S.y_center[m] = d.y[0];
      let dpm = 0; for (let i = 0; i < n; i++) dpm = max(dpm, d.dp_gas[i]);
      S.dp_gas_bar[m] = dpm / 1e5;
      S.Pi_gas[m] = d.Pi_gas; S.Pi_th[m] = d.Pi_th; S.Pi_bloat[m] = d.Pi_bloat; S.melt_margin[m] = d.melt;
      S.xO2[m] = d.xO2; S.xH2[m] = d.xH2; S.xH2O[m] = d.xH2O; S.xCO[m] = d.xCO; S.xCO2[m] = d.xCO2; S.x_hc[m] = d.x_hc;
      let lnV = 0; for (let i = 0; i < n; i++) lnV += Y[ILV * n + i] * wt[i];
      const ez = Y[NV * n + GEZ];
      S.shrink_xy[m] = 1 - exp(lnV / 3 - ez / 2);
      S.shrink_z[m] = 1 - exp(lnV / 3 + ez);
      S.dewpoint_out[m] = thermo.dewpoint_from_x_h2o(max(d.xH2O, 1e-8));
    }
    const t_h = Float64Array.from(ts, (t) => t / 3600);
    // closure event at the centre node
    let ic = -1;
    for (let m = 0; m < M; m++) if (S.f_cl_center[m] >= 0.5) { ic = m; break; }
    const closed = ic >= 0;
    let exoMax = -Infinity;
    for (let m = 0; m < M; m++) if (S.Tset[m] >= S.Tf[m] - 0.5) exoMax = max(exoMax, S.exo_gen[m]);
    exoMax = max(exoMax, 0);
    const maxOf = (a) => { let v = -Infinity; for (const x of a) v = max(v, x); return v; };
    const minOf = (a) => { let v = Infinity; for (const x of a) v = min(v, x); return v; };
    let rampMax = 0;
    for (let m = 1; m < M - 1; m++) {
      if (S.binder_left[m] > 0.01) {
        const r = abs((S.Tset[m + 1] - S.Tset[m - 1]) / ((ts[m + 1] - ts[m - 1]) / 60));
        rampMax = max(rampMax, r);
      }
    }
    const L = M - 1;
    const kpi = {
      duration_h: t_h[L], rho_final: S.rho_mean[L], rho_center_final: S.rho_center[L],
      shrink_xy_pct: 100 * S.shrink_xy[L], shrink_z_pct: 100 * S.shrink_z[L],
      C_final_ppm: S.C_ppm_mean[L], O_final_ppm: S.O_ppm_mean[L], closed,
      t_close_h: closed ? t_h[ic] : NaN, C_at_close_ppm: closed ? S.C_ppm_center[ic] : NaN,
      O_at_close_ppm: closed ? S.O_ppm_center[ic] : NaN,
      Pi_gas_max: maxOf(S.Pi_gas), Pi_th_max: maxOf(S.Pi_th), exo_max_K: exoMax, Pi_bloat_max: maxOf(S.Pi_bloat),
      melt_margin_min_K: minOf(S.melt_margin), binder_left_final: S.binder_left[L], grain_final_um: S.G_um[L],
      p_trap_final_bar: S.p_trap_bar[L], O_peak_ppm: maxOf(S.O_ppm_mean), C_peak_ppm: maxOf(S.C_ppm_mean),
      iacs: su.iacs(S.rho_mean[L]), debind_ramp_max_Kmin: rampMax,
    };
    kpi.verdict = verdict(kpi, su);
    return { t_h, series: S, kpi, scenario: su.s };
  }

  function verdict(k, su) {
    const item = (value, limit, unit, higherIsBad, label) => {
      const idx = higherIsBad === false ? limit / max(value, 1e-12) : value / limit;
      return { value, limit, unit, index: idx, ok: idx <= 1.0, label };
    };
    const Cc = k.closed ? k.C_at_close_ppm : k.C_final_ppm;
    const Oc = k.closed ? k.O_at_close_ppm : k.O_final_ppm;
    return {
      gas_pressure: item(k.Pi_gas_max, 1.0, "-", true, "Debinding gas pressure / strength (with SF)"),
      thermal_stress: item(k.Pi_th_max, 1.0, "-", true, "Thermal stress / strength"),
      self_heating: item(k.exo_max_K, su.dT_exo, "K", true, "Self-heating above furnace"),
      binder_removed: item(k.binder_left_final, 1e-3, "-", true, "Binder left at end"),
      carbon_at_closure: item(Cc, su.C_spec, "ppm", true, "Carbon when pores close"),
      oxygen_at_closure: item(Oc, su.O_spec, "ppm", true, "Oxide oxygen when pores close"),
      melting: { value: k.melt_margin_min_K, limit: 0, unit: "K", index: 1 - k.melt_margin_min_K / 50,
                 ok: k.melt_margin_min_K >= 0, label: "Margin below Cu-O solidus" },
      bloating: item(max(k.Pi_bloat_max, 0), 1.0, "-", true, "Trapped-gas pressure / sintering stress"),
      density: item(k.rho_final, su.rho_target, "-", false, "Final relative density"),
      debind_guard: item(k.debind_ramp_max_Kmin, su.ramp_guard * 1.02, "K/min", true, "Ramp while binder remains (guard)"),
    };
  }

  // ------------------------------------------------------------------ cycle synthesizer (mirrors synth.py)
  const DT_CTRL = 900.0, DT_HOLD = 1800.0, MAX_ITER = 400;
  const RAMPS = [10.0, 5.0, 3.0, 2.0, 1.0, 0.5, 0.25, 0.1, 0.05, 0.0];
  function Atmos(O2, H2, dp_C) { return { O2: O2 || 0, H2: H2 || 0, dp_C: dp_C == null ? -60 : dp_C }; }
  const atmKey = (a) => [+(a.O2).toFixed(6), +(a.H2).toFixed(4), +(a.dp_C).toFixed(1)].join("|");

  class Runner {
    constructor(scenario, opts) {
      opts = opts || {};
      this.s = Object.assign({}, scenario);
      this.su = new Setup(this.s);
      this.slab = new Slab(this.su, opts.N);
      this.rtol = opts.rtol || 1e-3;
      this.t = 0;
      this.Tset = 25 + T0C;
      this.Y = this.slab.y0(this.Tset, [0, 0, thermo.x_h2o_from_dewpoint(-60)]);
      this.log = [];
      this.h = null;
      this.lastRamp = {};
      this.out = new Float64Array(this.slab.n);
    }
    clone() {
      const c = Object.create(Runner.prototype);
      Object.assign(c, this);
      c.Y = Float64Array.from(this.Y);
      c.log = this.log.slice();
      c.lastRamp = Object.assign({}, this.lastRamp);
      c.lastAtm = Object.assign({}, this.lastAtm || {});
      return c;
    }
    advance(dt, rampKmin, TcapK, atm, exoAbort) {
      const dir = Math.sign(TcapK - this.Tset);
      const Tend = this.Tset + dir * min(abs(TcapK - this.Tset), rampKmin / 60 * dt);
      const [xo2, xh2, xh2o] = inletComposition(Segment(0, 1, 0, atm.O2, atm.H2, atm.dp_C), this.su);
      const ctl = new Controls(this.t, this.t + dt, this.Tset, Tend, xo2, xh2, xh2o);
      const sl = this.slab, N = sl.N;
      let cb = null;
      if (exoAbort != null && Tend >= this.Tset - 1e-9) {
        cb = (t, y) => { let m = -Infinity; for (let i = 0; i < N; i++) m = max(m, y[i]); return m - y[NV * N] > exoAbort; };
      }
      let r;
      try {
        r = ode23s((t, y, o) => sl.evaluate(t, y, ctl, o, false), this.t, this.t + dt, this.Y, sl.atol, this.rtol,
                   { scale: sl.scale, h0: this.h, hmax: 600, callback: cb });
      } catch (e) { return null; }
      if (r.ts[r.ts.length - 1] < this.t + dt - 1e-6) return { Pi_gas: 0, Pi_th: 0, exo: Infinity, melt: Infinity, bloat: 0 };
      let Pg = -Infinity, Pth = -Infinity, exo = -Infinity, melt = Infinity, bloat = -Infinity;
      for (let k = 0; k < r.ys.length; k++) {
        const d = sl.evaluate(r.ts[k], r.ys[k], ctl, this.out, true);
        Pg = max(Pg, d.Pi_gas); Pth = max(Pth, d.Pi_th); melt = min(melt, d.melt); bloat = max(bloat, d.Pi_bloat);
        if (ctl.Tset(r.ts[r.ts.length - 1]) >= d.Tf - 0.5) exo = max(exo, d.exo_gen);
      }
      const L = r.ts.length;
      this.h = L > 1 ? min(max(r.ts[L - 1] - r.ts[L - 2], 1), 600) : null;
      this.t += dt;
      this.Tset = Tend;
      this.Y = r.ys[L - 1];
      return { Pi_gas: Pg, Pi_th: Pth, exo, melt, bloat };
    }
    centre() {
      return this.slab.evaluate(this.t, this.Y, new Controls(this.t, this.t, this.Tset, this.Tset, 0, 0, 0), this.out, true);
    }
    binderLeft() {
      const n = this.slab.N, wt = this.slab.wt, Y = this.Y;
      let s = 0;
      for (let i = 0; i < n; i++) s += (Y[IB1 * n + i] + Y[IB2 * n + i] + Y[IB3 * n + i]) * wt[i];
      return s;
    }
  }

  function okDiag(d, su, margin) {
    if (!d) return [false, "solver"];
    if (d.Pi_gas > margin) return [false, "gas"];
    if (d.Pi_th > margin) return [false, "thermal"];
    if (d.exo > margin * su.dT_exo) return [false, "exo"];
    if (d.melt < -0.5) return [false, "melt"];
    if ((d.bloat || 0) > margin) return [false, "bloat"];
    return [true, ""];
  }

  function stepCtl(run, TcapK, atmOpts, phase, margin, dt, ramps, holdReason) {
    dt = dt || DT_CTRL; ramps = ramps || RAMPS;
    const su = run.su, rampMax = su.s.max_ramp_Kmin;
    const atCap = abs(run.Tset - TcapK) < 1e-6;
    let firstFail = null;
    const last = run.lastRamp[phase];
    if (last != null && !atCap && ramps.indexOf(last) >= 0) ramps = ramps.slice(max(0, ramps.indexOf(last) - 1));
    const lastAtm = (run.lastAtm || {})[phase];
    if (lastAtm != null && atmOpts.length > 1) {
      const keys = atmOpts.map(atmKey), k = keys.indexOf(lastAtm);
      if (k >= 0) atmOpts = atmOpts.slice(max(0, k - 1));
    }
    const exoAbort = phase[0] === "A" || phase[0] === "B" ? margin * su.dT_exo : null;
    for (const atm of atmOpts) {
      for (let r of ramps) {
        if (r > rampMax) continue;
        if (atCap && r > 0) r = 0;
        const trial = run.clone();
        const d = trial.advance(dt, r, TcapK, atm, exoAbort);
        let [ok, why] = okDiag(d, su, margin);
        if (ok && (r > 0 || atm !== atmOpts[atmOpts.length - 1])) {
          const probe = trial.clone();
          const [ok2, why2] = okDiag(probe.advance(dt, 0, TcapK, atmOpts[atmOpts.length - 1], exoAbort), su, margin);
          ok = ok2; if (!ok2) why = why || "lookahead-" + why2;
        }
        if (ok) {
          let limit;
          if (atCap) limit = holdReason || "hold";
          else if (r === min(rampMax, ramps[0]) && atm === atmOpts[0]) limit = ramps[0] < min(rampMax, RAMPS[0]) && phase[0] === "A" ? "guard" : "ramp_max";
          else limit = firstFail || "";
          Object.assign(run, trial);
          if (!atCap) run.lastRamp = Object.assign({}, run.lastRamp, { [phase]: r });
          run.lastAtm = Object.assign({}, run.lastAtm || {}, { [phase]: atmKey(atm) });
          const T0 = run.log.length ? run.log[run.log.length - 1].T1_C : 25;
          run.log.push({ t0: run.t - dt, t1: run.t, T0_C: T0, T1_C: run.Tset - T0C, atm, phase, limit });
          return d;
        }
        if (firstFail == null) firstFail = why;
        if (atCap) break;
      }
    }
    const atm = atmOpts[atmOpts.length - 1];
    const d = run.advance(dt, 0, TcapK, atm);
    const T0 = run.log.length ? run.log[run.log.length - 1].T1_C : 25;
    run.log.push({ t0: run.t - dt, t1: run.t, T0_C: T0, T1_C: run.Tset - T0C, atm, phase, limit: "INFEASIBLE:" + (firstFail || "") });
    return d;
  }

  const tick = () => new Promise((res) => setTimeout(res, 0));

  async function phaseDebind(run, o2cap, margin, prog) {
    const su = run.su, air = su.s.has_air_bleed >= 0.5;
    const levels = o2cap > 0 && air ? [0.21, 0.05, 0.02, 0.005, 0.002, 0.0005].filter((v) => v <= o2cap + 1e-12).concat([0]) : [0];
    const opts = levels.map((v) => Atmos(v, 0, -60));
    const guard = su.ramp_guard, Tend = 600 + T0C;
    while (run.t < 300 * 3600) {
      let ramps = run.binderLeft() > 0.01 ? RAMPS.filter((r) => r <= guard) : RAMPS;
      if (run.binderLeft() > 0.01 && ramps.indexOf(guard) < 0) ramps = [guard].concat(ramps);
      stepCtl(run, Tend, opts, "A debind", margin, DT_CTRL, ramps);
      const lg = run.log[run.log.length - 1];
      if (lg && lg.limit === "" && run.binderLeft() > 0.01 && abs((lg.T1_C - lg.T0_C) / 15 - guard) < 1e-6) lg.limit = "guard";
      if (prog) { prog(run); await tick(); }
      if (run.binderLeft() < 1e-3 && run.Tset >= 450 + T0C) break;
    }
  }
  async function phaseChem(run, TB, margin, prog) {
    const su = run.su;
    const h2 = su.s.h2_max > 0 ? min(0.04, su.s.h2_max) : 0;
    const atm = Atmos(0, h2, su.s.dp_max_C);
    const t0 = run.t;
    while (run.t - t0 < 60 * 3600) {
      const d = run.centre();
      const atT = run.Tset >= TB + T0C - 1e-6;
      if (atT && d.C_ppm[0] <= su.C_spec * 0.5 && d.O_ppm[0] <= min(su.O_spec, 80) * 0.5) return true;
      if (d.f_cl[0] > 0.02) return false;
      stepCtl(run, TB + T0C, [atm], "B chemistry", margin, atT ? DT_HOLD : DT_CTRL, RAMPS, "C/O removal");
      if (prog) { prog(run); await tick(); }
    }
    return false;
  }
  async function phaseDensify(run, margin, prog) {
    const su = run.su, atm = Atmos(0, su.s.h2_max, -60);
    let d = run.centre();
    let O = 0; for (const v of d.O_ppm) O = max(O, v);
    const Tpeak = min(thermo.T_solidus_Cu_O(O + 5) - su.T_margin - 1 - T0C, su.s.T_furnace_max_C);
    let guard = 0;
    while (run.Tset < Tpeak + T0C - 1e-6 && guard++ < MAX_ITER) { stepCtl(run, Tpeak + T0C, [atm], "C densify", margin); if (prog) { prog(run); await tick(); } }
    const th = run.t;
    let lastRho = null;
    while (run.t - th < 8 * 3600) {
      d = run.centre();
      let rho = 0; for (let i = 0; i < run.slab.N; i++) rho += d.rho[i] * run.slab.wt[i];
      if (rho >= su.rho_target) break;
      if (lastRho != null && rho - lastRho < 1e-3 * DT_HOLD / 3600) break;
      lastRho = rho;
      stepCtl(run, Tpeak + T0C, [atm], "C densify", margin, DT_HOLD, [0.0], "densification");
      if (run.log[run.log.length - 1].limit.indexOf("INFEASIBLE") === 0) break;
      if (prog) { prog(run); await tick(); }
    }
  }
  async function phaseCool(run, margin) {
    const su = run.su;
    const red = Atmos(0, min(0.04, su.s.h2_max), -60);
    let guard = 0;
    while (run.Tset > 600 + T0C + 1e-6 && guard++ < MAX_ITER) stepCtl(run, 600 + T0C, [red], "D cool", margin, DT_CTRL, [su.s.max_ramp_Kmin]);
    while (run.Tset > 25 + T0C + 1e-6 && guard++ < 2 * MAX_ITER) stepCtl(run, 25 + T0C, [Atmos()], "D cool", margin, 1800, [su.s.max_ramp_Kmin]);
  }

  function quantise(log, relTol) {
    relTol = relTol == null ? 0.25 : relTol;
    const segs = [];
    let cur = null;
    const toSeg = (c) => {
      const lim = Array.from(c.limits).filter((x) => x).sort().join(",");
      const note = c.phase + (lim ? " [" + lim + "]" : "");
      if (c.hold) return Segment(+c.T1.toFixed(1), 1.0, +(c.dt / 60).toFixed(3), c.atm.O2, c.atm.H2, c.atm.dp_C, note);
      return Segment(+c.T1.toFixed(1), +c.rate.toFixed(4), 0, c.atm.O2, c.atm.H2, c.atm.dp_C, note);
    };
    for (const iv of log) {
      const dT = iv.T1_C - iv.T0_C, dtm = (iv.t1 - iv.t0) / 60, rate = dtm > 0 ? abs(dT) / dtm : 0;
      const hold = abs(dT) < 1e-6, key = atmKey(iv.atm) + "|" + hold + "|" + iv.phase;
      if (cur && cur.key === key && (hold || abs(rate - cur.rate) <= relTol * max(cur.rate, 1e-9))) {
        cur.dT += dT; cur.dt += dtm; cur.rate = hold ? 0 : abs(cur.dT) / cur.dt; cur.T1 = iv.T1_C; cur.limits.add(iv.limit);
      } else {
        if (cur) segs.push(toSeg(cur));
        cur = { key, dT, dt: dtm, rate, T0: iv.T0_C, T1: iv.T1_C, atm: iv.atm, hold, phase: iv.phase, limits: new Set([iv.limit]) };
      }
    }
    if (cur) segs.push(toSeg(cur));
    const out = [];
    for (const sg of segs) {
      const p = out[out.length - 1];
      if (p && sg.ramp_Kmin === 1.0 && sg.hold_h > 0 && p.hold_h === 0 && abs(p.T_end_C - sg.T_end_C) < 1e-6 &&
          p.O2 === sg.O2 && p.H2 === sg.H2 && p.dp_C === sg.dp_C) {
        const lim = sg.note.indexOf("[") >= 0 ? sg.note.split("[")[1].replace("]", "") : "hold";
        p.hold_h = sg.hold_h; p.note += " + hold [" + lim + "]"; continue;
      }
      out.push(sg);
    }
    return { name: "synthesised", T_start_C: 25, segments: out };
  }

  function topologies(s) {
    const t = [["WGS (pyrolyse in N2, gasify in wet H2)", 0.0]];
    if (s.has_air_bleed >= 0.5) t.push(["OX-0.2% (O2-throttled burn)", 0.002], ["OX-2% (O2-throttled burn)", 0.02], ["OX-air", 0.21]);
    return t;
  }

  async function synthesize(scenario, opts) {
    opts = opts || {};
    const margin = opts.margin || 0.8, TBs = opts.T_B_list || [800, 875, 950, 1000];
    const progress = opts.progress || (() => {});
    const topo = topologies(scenario).filter(([nm]) => !opts.topoFilter || opts.topoFilter.some((f) => nm.indexOf(f) >= 0));
    const cands = [];
    let done = 0;
    const total = topo.length * (1 + TBs.length);
    for (const [name, o2cap] of topo) {
      const base = new Runner(scenario, opts);
      await phaseDebind(base, o2cap, margin, (r) => progress({ stage: name + ": debind", frac: done / total, t_h: r.t / 3600, T_C: r.Tset - T0C }));
      done++;
      for (const TB of TBs) {
        const run = base.clone();
        const ok = await phaseChem(run, TB, margin, (r) => progress({ stage: name + ": T_B " + TB, frac: done / total, t_h: r.t / 3600, T_C: r.Tset - T0C }));
        if (!ok) { cands.push({ topology: name, T_B_C: TB, feasible: false, duration_h: run.t / 3600, cycle: null, note: "pores closed before C/O cleared" }); done++; continue; }
        await phaseDensify(run, margin, (r) => progress({ stage: name + ": densify", frac: done / total, t_h: r.t / 3600, T_C: r.Tset - T0C }));
        await phaseCool(run, margin);
        const cyc = quantise(run.log);
        cyc.name = name + " | T_B " + TB + " C";
        const infeasible = run.log.some((iv) => iv.limit.indexOf("INFEASIBLE") === 0);
        cands.push({ topology: name, T_B_C: TB, feasible: !infeasible, duration_h: cycleDurationH(cyc), cycle: cyc,
                     note: infeasible ? "unsafe interval forced" : "", log: run.log });
        done++;
        progress({ stage: "candidate done", frac: done / total });
        await tick();
      }
    }
    const feas = cands.filter((c) => c.feasible && c.cycle);
    let best = null;
    for (const c of feas) if (!best || c.duration_h < best.duration_h) best = c;
    if (best && opts.verify !== false) best.result = simulate(scenario, best.cycle, { rtol: opts.verifyRtol || 1e-3, N: opts.verifyN || opts.N });
    return { best, candidates: cands };
  }

  // ------------------------------------------------------------------ exports
  const Cupola = {
    constants: { R, T0C, P_ATM, NV, NG, IT, IB1, IB2, IB3, IC, IX, IY, ILV, IG, INT, GTF, GO2, GH2, GH2O, GCO, GCO2, GEZ },
    thermo, Setup, Slab, Controls, ode23s, StepFailure, Segment, cycleBoundaries, cycleDurationH, cycleTsetK,
    baselineV0, inletComposition, simulate, postprocess, verdict,
    Runner, Atmos, quantise, topologies, synthesize,
    _util: { pos, clip, smoothstep, sigmoid },
  };
  if (typeof module !== "undefined" && module.exports) module.exports = Cupola;
  else root.Cupola = Cupola;
})(typeof window !== "undefined" ? window : globalThis);
