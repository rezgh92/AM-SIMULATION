"""T0 - thermochemical feasibility layer for the Cu-C-O-H system.

No fitted parameter lives here. Every function is a closed-form consequence of
standard Gibbs energies of formation, so everything downstream that asks "is this
atmosphere oxidising?" or "can carbon and oxide coexist?" gets the same answer.

Gibbs energies are linear fits dG = A + B*T (J per reaction as written), valid
roughly 300-1400 K. Sources: Cu2O and H2O lines as used in the research brief and
checked against JANAF 298 K values; CuO from JANAF dH/dS; CO, CO2 standard
Ellingham lines; CH4 from dHf = -74.87 kJ/mol, dSf = -80.8 J/mol/K.
"""
from __future__ import annotations

import numpy as np

from .constants import R, T0C, P_ATM, O_SOLIDUS_PPM, T_EUTECTIC_CU_O, T_MELT_CU

# (A, B) with dG = A + B*T  [J/mol of reaction]
G_LINES = {
    "4Cu+O2=2Cu2O": (-333_400.0, 141.3),
    "2Cu2O+O2=4CuO": (-287_800.0, 204.7),
    "2H2+O2=2H2O": (-492_900.0, 109.6),
    "2C+O2=2CO": (-223_000.0, -175.3),
    "C+O2=CO2": (-394_100.0, -0.8),
    "C+2H2=CH4": (-74_870.0, 80.8),
}


def dG(reaction: str, T):
    A, B = G_LINES[reaction]
    return A + B * np.asarray(T, dtype=float)


# ---------------------------------------------------------------- oxygen potential
def pO2_eq_Cu_Cu2O(T):
    """Equilibrium O2 partial pressure (atm) of 4Cu + O2 = 2Cu2O."""
    return np.exp(dG("4Cu+O2=2Cu2O", T) / (R * np.asarray(T, float)))


def pO2_eq_Cu2O_CuO(T):
    return np.exp(dG("2Cu2O+O2=4CuO", T) / (R * np.asarray(T, float)))


def K_H2O(T):
    """K for H2 + 1/2 O2 = H2O, so pH2O/pH2 = K * sqrt(pO2)."""
    return np.exp(-dG("2H2+O2=2H2O", T) / (2 * R * np.asarray(T, float)))


def pO2_from_H2O_H2(ratio_h2o_h2, T):
    """Equilibrium pO2 (atm) set by a given pH2O/pH2 ratio."""
    return (np.asarray(ratio_h2o_h2, float) / K_H2O(T)) ** 2


def h2o_h2_boundary_Cu(T):
    """pH2O/pH2 at the Cu/Cu2O boundary. Below this ratio the gas reduces Cu2O."""
    return K_H2O(T) * np.sqrt(pO2_eq_Cu_Cu2O(T))


def reducing_margin(ratio_h2o_h2, T):
    """How many times more oxidising the gas could be before Cu2O forms (>1 is reducing)."""
    return h2o_h2_boundary_Cu(T) / np.maximum(np.asarray(ratio_h2o_h2, float), 1e-300)


# ---------------------------------------------------------------- carbon reactions
def dG_carbothermic(T):
    """Cu2O + C = 2Cu + CO, J/mol. Negative above ~350 K: carbon and Cu2O cannot coexist."""
    # = 1/2 (2C+O2=2CO) - 1/2 (4Cu+O2=2Cu2O)
    return 0.5 * dG("2C+O2=2CO", T) - 0.5 * dG("4Cu+O2=2Cu2O", T)


def T_carbothermic_onset():
    """Temperature (K) where dG(Cu2O + C = 2Cu + CO) crosses zero."""
    A = 0.5 * (G_LINES["2C+O2=2CO"][0] - G_LINES["4Cu+O2=2Cu2O"][0])
    B = 0.5 * (G_LINES["2C+O2=2CO"][1] - G_LINES["4Cu+O2=2Cu2O"][1])
    return -A / B


def K_steam_gasification(T):
    """K for C + H2O = CO + H2 (pCO*pH2/pH2O, atm)."""
    dg = 0.5 * dG("2C+O2=2CO", T) - 0.5 * dG("2H2+O2=2H2O", T)
    return np.exp(-dg / (R * np.asarray(T, float)))


def K_methanation(T):
    """K for C + 2H2 = CH4 (pCH4/pH2^2, 1/atm)."""
    return np.exp(-dG("C+2H2=CH4", T) / (R * np.asarray(T, float)))


def K_boudouard(T):
    """K for C + CO2 = 2CO (pCO^2/pCO2, atm)."""
    dg = dG("2C+O2=2CO", T) - dG("C+O2=CO2", T)
    return np.exp(-dg / (R * np.asarray(T, float)))


# ---------------------------------------------------------------- water vapour
def p_sat_water_Pa(Td_C):
    """Arden Buck (1996) saturation vapour pressure, Pa. Over ice below 0 degC."""
    Td = np.asarray(Td_C, dtype=float)
    water = 611.21 * np.exp((18.678 - Td / 234.5) * (Td / (257.14 + Td)))
    ice = 611.15 * np.exp((23.036 - Td / 333.7) * (Td / (279.82 + Td)))
    return np.where(Td >= 0.0, water, ice)


def x_h2o_from_dewpoint(Td_C, P=P_ATM):
    """Mole fraction of H2O in a gas at total pressure P with dew point Td (degC)."""
    return p_sat_water_Pa(Td_C) / P


def dewpoint_from_x_h2o(x, P=P_ATM):
    """Inverse of x_h2o_from_dewpoint, by bisection (vectorised)."""
    x = np.atleast_1d(np.asarray(x, dtype=float))
    lo = np.full_like(x, -90.0)
    hi = np.full_like(x, 100.0)
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        f = x_h2o_from_dewpoint(mid, P) - x
        hi = np.where(f > 0, mid, hi)
        lo = np.where(f > 0, lo, mid)
    out = 0.5 * (lo + hi)
    return out if out.size > 1 else float(out[0])


# ---------------------------------------------------------------- Cu-O melting
def T_solidus_Cu_O(O_ppm):
    """Solidus of Cu with dissolved/segregated oxygen (K).

    Pure Cu melts at 1084.62 degC. Oxygen solubility in solid Cu at the 1066 degC
    eutectic is only ~80 ppm, so any part above ~80 ppm O forms liquid at 1066 degC.
    The 0.39 wt% figure often quoted is the *eutectic liquid composition*, not the
    threshold - using it is non-conservative by ~50x.
    """
    frac = np.clip(np.asarray(O_ppm, float) / O_SOLIDUS_PPM, 0.0, 1.0)
    return T_MELT_CU - (T_MELT_CU - T_EUTECTIC_CU_O) * frac


def dissolved_O_ppm_eq(ratio_h2o_h2, T):
    """Equilibrium dissolved O (ppm by mass) in Cu under an H2/H2O atmosphere.

    Henrian: [O] = [O]_sat * sqrt(pO2 / pO2_eq(Cu/Cu2O)) = [O]_sat * r / r_boundary.
    [O]_sat from N_O = 154 exp(-149600/RT) (atom fraction), converted to mass ppm.
    """
    T = np.asarray(T, float)
    n_sat = 154.0 * np.exp(-149_600.0 / (R * T))
    o_sat_ppm = n_sat * (15.999 / 63.546) * 1e6
    return o_sat_ppm * np.minimum(1.0, np.asarray(ratio_h2o_h2, float) / h2o_h2_boundary_Cu(T))


def summary_table(T_C=(300, 400, 500, 600, 700, 785, 800, 900, 1000, 1066)):
    """Handy table used in docs and tests."""
    rows = []
    for tc in T_C:
        T = tc + T0C
        rows.append(dict(
            T_C=tc,
            pO2_Cu_Cu2O_atm=float(pO2_eq_Cu_Cu2O(T)),
            H2O_H2_boundary=float(h2o_h2_boundary_Cu(T)),
            dG_carbothermic_kJ=float(dG_carbothermic(T)) / 1e3,
            K_steam_gasif=float(K_steam_gasification(T)),
        ))
    return rows
