"""Material properties and derived constants.

``Setup(scenario)`` turns the display-unit scenario from ``params`` into SI
constants the model uses. Every property function documents its source.
"""
from __future__ import annotations

import math
import numpy as np

from .constants import (R, KB, M_CU, M_O, M_C, RHO_CU, RHO_CU2O, RHO_CHAR, OMEGA_CU,
                        V_CU, V_CU_IN_CU2O, V_CU_IN_CUO, T0C, P_ATM, SLPM_TO_MOLS)
from . import thermo

BETA_REF = 10.0 / 60.0   # K/s - the heating rate at which TGA/TPR peak temperatures are quoted

# Frost & Ashby (1982), Table 4.1, copper
DV0, QV = 2.0e-5, 197_000.0          # lattice diffusion, m^2/s, J/mol
DDB0, QB = 5.0e-15, 104_000.0        # delta*D_b, m^3/s, J/mol
# Grain growth prefactor: dense Cu 5 -> ~30 um in 1 h at 1000 C (ANALOGUE, kG_mult rescales)
KG0 = 1.39e-13                        # m^3/s
THETA_PIN = 0.03                      # porosity scale for pore pinning of grain growth

# Cu oxidation law (DERIVED, scripts/fit_cu_oxidation.py):
#   dX/dt = K(T) (10um/d50)^2 (pO2/0.21 atm)^(1/7) (1-X)/(X+X0)^m
#   K(350 C) = 1.900e-7 1/s, m = 4.304, E fixed (param E_cu_ox, default 100 kJ/mol)
#   X = mol O per mol Cu (0.5 = all Cu2O, 1 = all CuO). Fits Ott (2022) 12.7 um powder at 350 C exactly.
CUOX_K350 = 1.9001e-7
CUOX_M = 4.304
CUOX_X0 = 2.0e-3
CUOX_DREF = 10e-6

# Binder elemental composition (HDDA-like acrylate, C 63.7 / H 8.0 / O 28.3 wt%)
NU_O2_BINDER = 64.2      # mol O2 to burn 1 kg binder completely
N_CO2_BINDER = 53.1      # mol CO2 per kg
N_H2O_BINDER = 40.0      # mol H2O per kg
THORNTON = 13.1e6 / 31.998e-3 * 1e-3   # J per mol O2 consumed (13.1 MJ/kg O2) = 4.09e5 J/mol

DH_CU_OX = 165e3         # J/mol O, Cu -> Cu2O/CuO (exothermic, released)
DH_RED_H2 = 73.2e3       # J/mol, Cu2O + H2 -> 2Cu + H2O(g) (exothermic)
DH_CARBOTHERMIC = 58.1e3 # J/mol, Cu2O + C -> 2Cu + CO (endothermic)
DH_GASIF = 131.3e3       # J/mol, C + H2O -> CO + H2 (endothermic)
DH_CHAR_OX = 393.5e3     # J/mol C, C + O2 -> CO2 (exothermic)

M_SOLVENT = 0.15         # kg/mol, high-boiling solvent
CP_BINDER = 1800.0
CP_CHAR = 1200.0


def kp_from_Tpeak(Tp_K: float, E: float, beta: float = BETA_REF) -> float:
    """First-order rate constant at the DTG peak: k(Tp) = E beta / (R Tp^2)."""
    return E * beta / (R * Tp_K ** 2)


def arrhenius_iso(T, k_ref, E, T_ref):
    """Isokinetic-centred Arrhenius. Keeps (k_ref, E) near-orthogonal for fitting."""
    return k_ref * np.exp(-(E / R) * (1.0 / T - 1.0 / T_ref))


def cp_cu(T):
    """J/(kg K), linear fit 385 J/kg/K at 298 K to 471 at 1273 K."""
    return 360.0 + 0.0870 * T


def k_cu(T):
    """W/(m K), 401 at 300 K falling to ~337 at 1300 K."""
    return 401.0 - 0.064 * (T - 300.0)


def mu_gas(T):
    """Dynamic viscosity of N2-like gas, Pa s (Sutherland-type power fit)."""
    return 1.663e-5 * (T / 273.15) ** 0.7


def D_O2_N2(T, P=P_ATM):
    """Binary diffusivity O2-N2, m^2/s."""
    return 2.02e-5 * (T / 293.15) ** 1.75 * (P_ATM / P)


def lognormal_sigma_from_span(span: float) -> float:
    """Volume-weighted lognormal: span = (d90-d10)/d50 = 2 sinh(1.2816 sigma)."""
    return math.asinh(span / 2.0) / 1.2815516


def smoothstep(x):
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3.0 - 2.0 * x)


def sigmoid(x):
    return 0.5 * (1.0 + np.tanh(0.5 * x))


class Setup:
    """All SI constants for one scenario. Cheap to build; immutable by convention."""

    def __init__(self, s: dict):
        self.s = dict(s)
        g = self.s
        # ---------------- powder
        self.d50 = g["d50_um"] * 1e-6
        sig = lognormal_sigma_from_span(g["span"])
        self.d32 = self.d50 * math.exp(-0.5 * sig ** 2)
        self.r_s = 0.5 * self.d32                       # sintering length scale
        self.G0 = g["grain_ratio"] * self.d50
        # ---------------- composition per m^3 of green part
        self.phi = g["phi"]
        self.rho_b = g["rho_binder"]
        self.mb0 = (1.0 - self.phi) * self.rho_b          # kg binder / m^3
        self.nCu = self.phi * RHO_CU / M_CU               # mol Cu / m^3
        self.mCu = self.phi * RHO_CU
        w1 = g["solvent_frac"]
        wnet = 1.0 - w1
        w3 = wnet * g["w_backbone"]
        w2 = wnet - w3
        self.b0 = np.array([w1, w2, w3]) * self.mb0
        self.chi = np.array([0.0, g["char_yield"], g["char_yield"]])
        self.Mgas = np.array([M_SOLVENT, g["M_vol"], g["M_vol"]])
        # kinetics (TGA peak parameterisation)
        Tp = np.array([g["Tp_solvent_C"], g["Tp_network_C"], g["Tp_backbone_C"]]) + T0C
        E = np.array([g["E_solvent"], g["E_network"], g["E_backbone"]]) * 1e3
        self.Tp, self.E = Tp, E
        self.kp = E * BETA_REF / (R * Tp ** 2)
        # oxidative channel for network components (solvent just evaporates)
        self.Tp_ox = Tp - g["ox_shift_K"]
        self.E_ox = np.full(3, g["E_oxdeg"] * 1e3)
        self.kp_ox = self.E_ox * BETA_REF / (R * self.Tp_ox ** 2)
        self.dHc = g["dHc_MJkg"] * 1e6
        self.dHpyr = g["dHpyr_MJkg"] * 1e6
        # char oxidation
        self.Tp_cox = g["Tp_charox_C"] + T0C
        self.E_cox = 150e3
        self.kp_cox = kp_from_Tpeak(self.Tp_cox, self.E_cox)
        # ---------------- native oxide -> initial X (mol O / mol Cu)
        Sv = 6.0 / self.d32                                  # m^2 per m^3 Cu
        n_ox = Sv * g["native_oxide_nm"] * 1e-9 * RHO_CU2O / (2 * M_CU + M_O)   # mol Cu2O per m^3 Cu
        self.X0 = n_ox / (RHO_CU / M_CU)
        # ---------------- Cu oxidation / reduction
        self.E_cuox = g["E_cu_ox"] * 1e3
        self.Tp_red = g["Tp_reduction_C"] + T0C
        self.E_red = g["E_reduction"] * 1e3
        self.kp_red = kp_from_Tpeak(self.Tp_red, self.E_red)
        # ---------------- carbon
        self.T_ref_g = 800.0 + T0C
        self.x_h2o_ref = float(thermo.x_h2o_from_dewpoint(20.0))
        self.K_inh = 25.0
        self.k_g_ref = math.log(2.0) / (g["t_half_gasif_h"] * 3600.0)
        self.E_g = g["E_gasif"] * 1e3
        self.T_cth = g["T_carbothermic_C"] + T0C
        self.E_cth = 180e3
        self.k_cth_ref = 1e-4
        # ---------------- sintering
        self.gamma = g["gamma_s"]
        self.f_eta = g["f_eta"]
        self.kG = g["kG_mult"] * KG0
        self.rho_close = g["rho_close"]
        self.C_inh = g["C_inhibit_ppm"]
        self.aniso = g["anisotropy"]
        # ---------------- part / load / furnace
        self.L0 = g["half_thickness_mm"] * 1e-3
        self.V_load = g["load_cm3"] * 1e-6
        self.h_conv = g["h_conv"]
        self.ramp_max = g["max_ramp_Kmin"] / 60.0
        self.tau_f = g["furnace_lag_min"] * 60.0
        self.T_f_max = g["T_furnace_max_C"] + T0C
        self.F_in = g["flow_slpm"] * SLPM_TO_MOLS
        self.V_r = g["retort_L"] * 1e-3
        self.x_o2_imp = g["o2_impurity_ppm"] * 1e-6
        # ---------------- binder transport / strength
        self.perm_poly = g["perm_polymer_barrer"] * 3.35e-16     # mol m / (m^2 s Pa)
        self.eps_c = g["eps_perc"]
        self.sig_green = g["sigma_green_MPa"] * 1e6
        self.f_int = g["interlayer_factor"]
        self.Tg = g["Tg_C"] + T0C
        self.r_rub = g["rubbery_ratio"]
        self.k_green = g["k_green"]
        # ---------------- limits
        self.dT_exo = g["dT_exo_max"]
        self.sf_gas = g["sf_gas"]
        self.C_spec = g["C_spec_ppm"]
        self.O_spec = g["O_spec_ppm"]
        self.rho_target = g["rho_target"]
        self.T_margin = g["T_margin_K"] + g["T_uniformity_K"]
        # ---------------- impurities
        self.P_ppm = g["P_ppm"]
        self.P_diss = g["P_dissolved_frac"]

    # --------------------------------------------------------------- composition helpers
    def inorganic_volume(self, X):
        """Solid inorganic volume per m^3 of green part, as a function of X (O/Cu)."""
        X = np.clip(X, 0.0, 1.0)
        v_per_cu = np.where(X <= 0.5,
                            V_CU + (V_CU_IN_CU2O - V_CU) * (X / 0.5),
                            V_CU_IN_CU2O + (V_CU_IN_CUO - V_CU_IN_CU2O) * ((X - 0.5) / 0.5))
        return self.nCu * v_per_cu

    def inorganic_mass(self, X):
        return self.mCu + self.nCu * np.clip(X, 0.0, 1.0) * M_O

    def ppm_of_part(self, kg_per_m3, X):
        """Convert kg/m^3 (per green volume) to ppm of inorganic part mass."""
        return 1e6 * kg_per_m3 / self.inorganic_mass(X)

    def O_ppm(self, X):
        """Oxygen held as oxide, ppm of total inorganic mass."""
        return 1e6 * self.nCu * np.clip(X, 0, 1) * M_O / self.inorganic_mass(X)

    # --------------------------------------------------------------- rate constants
    def k_pyr(self, T):
        """(3, ...) first-order pyrolysis constants."""
        T = np.asarray(T)
        return self.kp[:, None] * np.exp(-(self.E[:, None] / R) * (1.0 / T[None, ...] - 1.0 / self.Tp[:, None])) \
            if T.ndim else self.kp * np.exp(-(self.E / R) * (1.0 / T - 1.0 / self.Tp))

    def k_cu_ox(self, T):
        """Prefactor of the Cu oxidation law at T for this powder (1/s)."""
        return CUOX_K350 * np.exp(-(self.E_cuox / R) * (1.0 / T - 1.0 / (350.0 + T0C))) * (CUOX_DREF / self.d50) ** 2

    def k_red(self, T):
        return self.kp_red * np.exp(-(self.E_red / R) * (1.0 / T - 1.0 / self.Tp_red)) * (10e-6 / self.d32)

    def k_gasif(self, T):
        return self.k_g_ref * np.exp(-(self.E_g / R) * (1.0 / T - 1.0 / self.T_ref_g))

    def k_carbothermic(self, T):
        return self.k_cth_ref * np.exp(-(self.E_cth / R) * (1.0 / T - 1.0 / self.T_cth))

    def k_char_ox(self, T):
        return self.kp_cox * np.exp(-(self.E_cox / R) * (1.0 / T - 1.0 / self.Tp_cox))

    # --------------------------------------------------------------- sintering
    def eta0(self, T, G):
        """Shear viscosity of the porous skeleton's matrix, Pa s (Frost & Ashby diffusional creep).

        eta = kT G^2 / (42 Omega (D_v + pi dD_b / G)) x f_eta.
        """
        Dv = DV0 * np.exp(-QV / (R * T))
        dDb = DDB0 * np.exp(-QB / (R * T))
        return self.f_eta * KB * T * G ** 2 / (42.0 * OMEGA_CU * (Dv + math.pi * dDb / G))

    def kG_rate(self, T):
        return self.kG * np.exp(-QB / (R * T))

    # --------------------------------------------------------------- thermal
    def k_eff(self, T, w_b, rho):
        """Effective conductivity: binder-filled green blending into a sintering skeleton."""
        neck = np.clip((rho - self.phi) / (1.0 - self.phi), 0.0, 1.0) + 0.002
        k_brown = 0.15 + k_cu(T) * neck ** 1.5
        return w_b * self.k_green + (1.0 - w_b) * k_brown

    @staticmethod
    def emissivity(w_dark, theta):
        eps_cu = 0.10 + 0.30 * np.clip(theta, 0.0, 0.5)
        return eps_cu + (0.90 - eps_cu) * np.clip(w_dark, 0.0, 1.0)

    # --------------------------------------------------------------- strength
    def sigma_green(self, T, a_net):
        """Binder-carried tensile strength, Pa."""
        soft = self.r_rub + (1.0 - self.r_rub) * sigmoid((self.Tg - T) / 5.0)
        return self.sig_green * soft * np.clip(1.0 - a_net, 0.0, 1.0) ** 2

    def sigma_brown(self, rho):
        neck = np.clip((rho - self.phi) / (1.0 - self.phi), 0.0, 1.0)
        return 0.3e6 + 60e6 * neck ** 1.5

    def E_green(self, T, a_net):
        soft = self.r_rub + (1.0 - self.r_rub) * sigmoid((self.Tg - T) / 5.0)
        return 10e9 * soft * np.clip(1.0 - a_net, 0.0, 1.0) ** 2 + 0.5e9

    # --------------------------------------------------------------- properties of the finished part
    def iacs(self, rho, O_ppm=0.0):
        """Electrical conductivity estimate, %IACS.

        Porosity: sigma/sigma0 = (1-theta)^1.5 (common empirical form for sintered Cu).
        Phosphorus in solid solution: -0.73 %IACS per 10 ppm (consistent with Cu-DLP ~90-97 %
        and Cu-DHP ~80-85 %IACS). Dissolved O and insoluble C are second order and ignored.
        """
        p_eff = self.P_ppm * self.P_diss
        return max(0.0, 101.0 * float(np.clip(rho, 0, 1)) ** 1.5 - 0.073 * p_eff)
