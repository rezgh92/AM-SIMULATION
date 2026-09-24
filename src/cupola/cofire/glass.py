"""Crystallising glass-ceramic in the same slab model as copper.

The slab (``model1d.Slab``) is material-agnostic once the material supplies its solid volume, heat
capacity, conductivity, strength, sintering viscosity and microstructure evolution. For a glass
powder the physics differs from copper in three places only:

* viscosity   the matrix is a Newtonian melt, eta_g(T) from the MYEGA equation (Mauro et al. 2009),
              parameterised by the glass transition Tg (eta = 1e12 Pa s) and the fragility index m;
* crystals    concurrent crystallisation follows non-isothermal JMAK kinetics. The IG slot of the
              slab carries the extended-volume integral xi = int k_c(T) dt, with k_c parameterised by
              the DSC crystallisation peak at 10 K/min (Kissinger), and X_c = 1 - exp(-xi^n);
              the crystals stiffen the melt as a suspension (Krieger-Dougherty);
* chemistry   there is no metal to oxidise or reduce, so those rates are zero and the IX slot
              stays at 0. Binder pyrolysis, char formation and steam gasification are unchanged.

Everything else (heat transfer, pore gas, trapped gas, retort balances, risk indices) is the
copper code path, which is how the two materials stay consistent.
"""
from __future__ import annotations

import math

import numpy as np

from ..constants import R, T0C, RHO_CHAR
from ..materials import Setup, lognormal_sigma_from_span, sigmoid, BETA_REF
from ..params import Param

LOG_ETA_INF = -3.0          # log10(Pa s), high-temperature limit of silicate melt viscosity (MYEGA)
THETA_UNUSED = 0.0

# ----------------------------------------------------------------------------- parameters
GC_PARAMS = [
    Param("gc_d50_um", 3.0, "um", 0.8, 12.0, "gc_powder", "ANALOGUE", "Glass powder D50",
          "IBM cordierite-type glass powders: 2-7 um (US 4,301,324). Sets the sintering stress (1/r) and the "
          "green permeability (d^2)."),
    Param("gc_span", 1.5, "-", 0.6, 3.0, "gc_powder", "GUESS", "Glass PSD span", ""),
    Param("gc_phi", 0.45, "-", 0.35, 0.60, "gc_powder", "ANALOGUE", "Glass solids loading (vol)",
          "LCM ceramic slurries hold 39-49 vol% solids."),
    Param("gc_rho", 2600.0, "kg/m3", 2400.0, 2800.0, "gc_glass", "ANALOGUE", "Glass density",
          "Dense alpha-cordierite glass-ceramic 2.62 g/cm3 (Yu et al. 2022)."),
    Param("gc_Tg_C", 734.0, "C", 680.0, 820.0, "gc_glass", "DERIVED", "Glass transition (1e12 Pa s)",
          "MYEGA fitted to two IBM statements for the Cu-compatible cordierite glass (US 4,234,367; "
          "US 5,130,067): 6 h at 780 C gives ~40 % of the fired shrinkage with open pores, and an 830 C hold "
          "closes the pores within ~2 h. Checks: 43 K per decade at 800-860 C (Giess 1984: ~40 K); annealing "
          "point below 785 C (patent bound)."),
    Param("gc_fragility", 32.4, "-", 25.0, 60.0, "gc_glass", "DERIVED", "Fragility index m", "Fitted with gc_Tg_C."),
    Param("gc_gamma", 0.36, "J/m2", 0.2, 0.45, "gc_glass", "ANALOGUE", "Glass surface energy",
          "0.36 N/m calculated for the IBM cordierite-type glass (Giess et al. 1984)."),
    Param("gc_Tp_cryst_C", 1040.0, "C", 950.0, 1100.0, "gc_glass", "DERIVED",
          "Crystallisation DSC peak (10 K/min)",
          "Set so that crystallisation begins (5 %) at ~900 C in the IBM firing schedule (US 4,340,436). "
          "Check: the exotherm then spans 978-1066 C, i.e. ~90 K (patent: 80-100 C)."),
    Param("gc_E_cryst", 303.0, "kJ/mol", 250.0, 470.0, "gc_glass", "ANALOGUE", "Crystallisation E",
          "303.5 kJ/mol for IBM-type high-cordierite glass (Watanabe & Giess 1994)."),
    Param("gc_n_avrami", 2.0, "-", 1.0, 3.7, "gc_glass", "GUESS", "Avrami exponent",
          "Not reported for the IBM glass (surface nucleation); 2.8-3.7 for other MAS glasses."),
    Param("gc_X_max", 0.64, "-", 0.45, 0.80, "gc_glass", "ANALOGUE", "Crystal fraction that arrests flow",
          "Maximum packing in the Krieger-Dougherty suspension law."),
    Param("gc_f_eta", 1.0, "-", 0.1, 10.0, "gc_glass", "GUESS", "Glass viscosity factor", "", log=True),
    Param("gc_k", 2.8, "W/m/K", 1.0, 5.0, "gc_glass", "ANALOGUE", "Dense glass-ceramic conductivity",
          "Cu-co-fired LTCC (Kyocera GL570): 2.8 W/m K."),
    Param("gc_sigma_green_MPa", 15.0, "MPa", 5.0, 40.0, "gc_powder", "GUESS", "GC green strength (RT)", ""),
    Param("gc_half_thickness_mm", 2.0, "mm", 0.25, 10.0, "gc_part", "GUESS", "GC critical half-thickness", ""),
    Param("gc_rho_close", 0.92, "-", 0.88, 0.95, "gc_glass", "ANALOGUE", "GC pore closure density", ""),
]
GC_REGISTRY = {p.key: p for p in GC_PARAMS}


def gc_defaults():
    return {k: p.value for k, p in GC_REGISTRY.items()}


# ----------------------------------------------------------------------------- property laws
def myega_log10_eta(T, Tg, m, log_eta_inf=LOG_ETA_INF):
    """log10 viscosity (Pa s), Mauro-Yue-Ellison-Gupta-Allan equation."""
    a = 12.0 - log_eta_inf
    x = Tg / T
    return log_eta_inf + a * x * np.exp((m / a - 1.0) * (x - 1.0))


def krieger_dougherty(X, X_max, intrinsic=2.5, cap=0.999):
    """Relative viscosity of a melt carrying a crystal volume fraction X."""
    r = np.minimum(np.clip(X, 0.0, None) / X_max, cap)
    return (1.0 - r) ** (-intrinsic * X_max)


def jmak_fraction(xi, n):
    return 1.0 - np.exp(-np.power(np.maximum(xi, 0.0), n))


def dsc_peak(kp, Tp, E, n, beta=BETA_REF):
    """Temperature (K) of the maximum of dX/dt for JMAK kinetics k = kp exp(-E/R (1/T - 1/Tp)) at a
    constant heating rate beta (K/s)."""
    T = np.linspace(Tp - 250.0, Tp + 250.0, 5001)
    k = kp * np.exp(-(E / R) * (1.0 / T - 1.0 / Tp))
    xi = np.concatenate([[0.0], np.cumsum(0.5 * (k[1:] + k[:-1]) * np.diff(T))]) / beta
    rate = n * np.power(np.maximum(xi, 1e-300), n - 1.0) * k * np.exp(-xi ** n)
    i = int(np.argmax(rate))
    if 0 < i < len(T) - 1:                       # parabolic refinement
        y0, y1, y2 = rate[i - 1], rate[i], rate[i + 1]
        return T[i] + 0.5 * (y0 - y2) / (y0 - 2 * y1 + y2) * (T[1] - T[0])
    return T[i]


def calibrate_kp(Tp, E, n, beta=BETA_REF):
    """Rate constant at Tp that puts the simulated DSC peak exactly at Tp (Kissinger's estimate
    E beta / (R Tp^2) is exact only for first-order kinetics)."""
    kp = E * beta / (R * Tp ** 2)
    for _ in range(30):
        err = dsc_peak(kp, Tp, E, n, beta) - Tp
        if abs(err) < 0.01:
            break
        # peak moves by ~ -(R Tp^2 / E) d ln kp
        kp *= math.exp(err * E / (R * Tp ** 2))
    return kp


class GlassSetup(Setup):
    """``Setup`` for a crystallising glass-ceramic green body.

    The scenario carries the shared binder, furnace and limit keys of the copper registry plus the
    ``gc_*`` keys above. Keys the glass does not use (oxide, reduction) are simply ignored.
    """

    def __init__(self, s: dict):
        s = dict(s)
        for k, v in gc_defaults().items():
            s.setdefault(k, v)
        mapped = dict(s)
        mapped.update(d50_um=s["gc_d50_um"], span=s["gc_span"], phi=s["gc_phi"], native_oxide_nm=0.0,
                      gamma_s=s["gc_gamma"], rho_close=s["gc_rho_close"],
                      half_thickness_mm=s["gc_half_thickness_mm"], sigma_green_MPa=s["gc_sigma_green_MPa"],
                      k_green=0.8)
        super().__init__(mapped)
        g = self.s
        self.material = "glass-ceramic"
        self.rho_solid = g["gc_rho"]
        self.nCu = 1e-12                             # no metal: every Cu-specific rate vanishes (kept > 0 for divisions)
        self.mCu = self.phi * self.rho_solid
        self.V_solid_eq = self.phi
        self.X0 = 0.0
        self.G0 = 0.0
        self.Tg_glass = g["gc_Tg_C"] + T0C
        self.m_frag = g["gc_fragility"]
        self.f_eta_gc = g["gc_f_eta"]
        self.Tp_c = g["gc_Tp_cryst_C"] + T0C
        self.E_c = g["gc_E_cryst"] * 1e3
        self.n_av = g["gc_n_avrami"]
        self.kp_c = calibrate_kp(self.Tp_c, self.E_c, self.n_av)
        self.X_max = g["gc_X_max"]
        self.k_dense = g["gc_k"]

    # ---------------------------------------------------------------- composition
    def inorganic_volume(self, X):
        return self.phi + 0.0 * np.asarray(X, dtype=float)

    def inorganic_mass(self, X):
        return self.mCu + 0.0 * np.asarray(X, dtype=float)

    def O_ppm(self, X):
        return 0.0 * np.asarray(X, dtype=float)

    # ---------------------------------------------------------------- chemistry (no metal)
    def k_cu_ox(self, T):
        return 0.0 * np.asarray(T, dtype=float)

    def k_red(self, T):
        return 0.0 * np.asarray(T, dtype=float)

    def k_carbothermic(self, T):
        return 0.0 * np.asarray(T, dtype=float)

    # ---------------------------------------------------------------- melt, crystals, sintering
    def eta_glass(self, T):
        # below ~Tg - 150 K the melt is rigid on any process time scale; cap to keep the arithmetic finite
        return self.f_eta_gc * 10.0 ** np.minimum(myega_log10_eta(T, self.Tg_glass, self.m_frag), 25.0)

    def k_cryst(self, T):
        """d xi / dt (1/s); Kissinger-parameterised so the DSC peak sits at Tp_c at 10 K/min."""
        return self.kp_c * np.exp(-(self.E_c / R) * (1.0 / T - 1.0 / self.Tp_c))

    def crystal_fraction(self, xi):
        return jmak_fraction(xi, self.n_av)

    def eta0(self, T, G):
        """Matrix shear viscosity. The slab passes the IG slot (here xi) as G in metres."""
        xi = np.asarray(G) * 1e6
        return self.eta_glass(T) * krieger_dougherty(self.crystal_fraction(xi), self.X_max)

    def dG_dt(self, T, G, theta):
        return self.k_cryst(T) + 0.0 * np.asarray(G)

    def kG_rate(self, T):
        return 0.0 * np.asarray(T, dtype=float)

    def carbon_factor(self, C_ppm):
        """Char particles are rigid inclusions in a Newtonian melt: suspension law on their volume
        fraction of the solid (graphitic char, 1800 kg/m^3)."""
        f = 1e-6 * np.asarray(C_ppm) * self.rho_solid / RHO_CHAR
        f = f / (1.0 + f)
        return krieger_dougherty(f, 0.64)

    # ---------------------------------------------------------------- thermal
    def cp(self, T):
        """Aluminosilicate glass-ceramic, J/(kg K): ~750 at room temperature rising to ~1150 at 1100 K."""
        return np.minimum(730.0 + 0.52 * (np.asarray(T) - 298.15), 1250.0)

    def k_eff(self, T, w_b, rho):
        neck = np.clip((rho - self.phi) / (1.0 - self.phi), 0.0, 1.0) + 0.002
        k_brown = 0.10 + self.k_dense * neck ** 1.5
        return w_b * self.k_green + (1.0 - w_b) * k_brown

    @staticmethod
    def emissivity(w_dark, theta):
        return 0.85 + 0.05 * np.clip(w_dark, 0.0, 1.0)

    def sigma_brown(self, rho):
        neck = np.clip((rho - self.phi) / (1.0 - self.phi), 0.0, 1.0)
        return 0.3e6 + 100e6 * neck ** 1.5

    def melt_margin(self, T, O_ppm):
        return 1000.0 + 0.0 * np.asarray(T)

    def iacs(self, rho, O_ppm=0.0):
        return float("nan")


class FilledCopperSetup(Setup):
    """Copper conductor paste with an inert ceramic filler (a common co-firing retarder).

    ``cu_filler`` is the filler volume fraction of the solids. Rigid filler particles raise the
    matrix viscosity as a suspension (Krieger-Dougherty) and lower the conductivity as insulating
    inclusions (Maxwell-Garnett: sigma/sigma0 = (1 - f)/(1 + f/2)).
    """

    def __init__(self, s: dict):
        super().__init__(s)
        self.f_fill = float(self.s.get("cu_filler", 0.0))

    def eta0(self, T, G):
        return super().eta0(T, G) * krieger_dougherty(self.f_fill, 0.64)

    def iacs(self, rho, O_ppm=0.0):
        f = self.f_fill
        return super().iacs(rho, O_ppm) * (1.0 - f) / (1.0 + 0.5 * f)
