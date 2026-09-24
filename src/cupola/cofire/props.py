"""Thermomechanical properties for the cooling analysis (sources in docs/paper3/lit/materials_dossier.md).

Values marked PROVISIONAL are replaced once the verified dossier is in.
"""
import numpy as np

# copper (annealed, polycrystalline)
CU_E = 120e9          # Pa, room temperature
CU_NU = 0.34


def cu_alpha(T_C):
    """Instantaneous linear thermal expansion of copper, 1/K (16.5e-6 at 25 C rising to ~20e-6 at 800 C)."""
    return 16.5e-6 + 4.5e-9 * (np.asarray(T_C) - 25.0)


def cu_yield(T_C):
    """0.2 % yield stress of annealed copper, Pa: ~60 MPa at room temperature falling to ~10 MPa at 700 C."""
    T = np.asarray(T_C)
    return np.clip(60e6 - (50e6 / 675.0) * (T - 25.0), 5e6, 60e6)


# cordierite-type glass-ceramic (PROVISIONAL)
GC_E = 110e9
GC_NU = 0.25
GC_ALPHA = 3.0e-6
GC_T_SF = 700.0       # C, stress-free temperature (residual glass stops relaxing)


def gc_alpha(T_C):
    return GC_ALPHA + 0.0 * np.asarray(T_C)
