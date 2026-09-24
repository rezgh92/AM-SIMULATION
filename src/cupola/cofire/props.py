"""Thermomechanical properties for the cooling analysis (sources in docs/paper3/lit/materials_dossier.md)."""
import numpy as np

# ---------------------------------------------------------------- copper (annealed, oxygen-free)
CU_E = 117e9          # Pa, Aurubis C10200 datasheet
CU_NU = 0.34          # assumed (polycrystalline copper)
_CU_A_T = np.array([100.0, 200.0, 293.0, 500.0, 800.0, 1100.0])        # K
_CU_A = np.array([10.3, 15.2, 16.5, 18.3, 20.3, 23.7]) * 1e-6          # 1/K, Kaye & Laby (NPL)
CU_YIELD_RT = 69e6    # Pa, soft temper Rp0.2, Aurubis C10200


def cu_alpha(T_C):
    """Instantaneous linear expansivity of copper, 1/K (Kaye & Laby table, interpolated)."""
    return np.interp(np.asarray(T_C) + 273.15, _CU_A_T, _CU_A)


def cu_yield(T_C):
    """Quasi-static yield of annealed copper: room-temperature value scaled by the Johnson-Cook thermal
    softening factor 1 - T*^1.09, T* = (T - 294 K)/(1356 K - 294 K) (Johnson & Cook 1985 constants)."""
    Ts = np.clip((np.asarray(T_C) + 273.15 - 294.0) / (1356.0 - 294.0), 0.0, 1.0)
    return np.maximum(CU_YIELD_RT * (1.0 - Ts ** 1.09), 2e6)


# ---------------------------------------------------------------- cordierite-type glass-ceramic
GC_E = 128e9          # Pa, Cu-co-fired LTCC analogue (Kyocera GL570)
GC_NU = 0.25          # assumed
GC_ALPHA = 3.0e-6     # 1/K, IBM HPGC substrate (Knickerbocker et al. 2002)
GC_STRENGTH = 210e6   # Pa, glass #12 fired in H2/H2O (US 4,234,367)
GC_T_SF = 690.0       # C, strain point (1e13.5 Pa s) of the calibrated glass: below it stresses no longer relax


def gc_alpha(T_C):
    return GC_ALPHA + 0.0 * np.asarray(T_C)
