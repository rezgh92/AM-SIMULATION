"""Co-firing scenarios and schedules: the same furnace program applied to both materials.

The copper conductor and the glass-ceramic body are simulated as two slabs that share the furnace
setpoint and inlet gas. Their mechanical coupling (shrinkage mismatch, camber, stress) is computed
afterwards from the two free-sintering histories (``mechanics``) or in 3-D (``fem3d.cosinter``).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import numpy as np

from .. import thermo
from ..constants import T0C
from ..cycle import Cycle, Segment
from ..params import defaults
from ..simulate import simulate
from .glass import GlassSetup, FilledCopperSetup, gc_defaults

# co-firing furnace: steam generator, H2 up to 100 %, standard retort otherwise
COFIRE_FURNACE = dict(h2_max=1.0, dp_max_C=60.0, has_air_bleed=0.0, T_furnace_max_C=1100.0,
                      max_ramp_Kmin=10.0, flow_slpm=2.0, retort_L=5.0, h_conv=15.0)
# copper conductor defaults for co-firing (fine powder, thin features)
COFIRE_CU = dict(d50_um=3.0, span=1.2, native_oxide_nm=3.0, phi=0.50, half_thickness_mm=0.15, anisotropy=0.0,
                 cu_filler=0.0)


def cofire_scenario(**over) -> dict:
    s = defaults()
    s.update(gc_defaults())
    s.update(COFIRE_FURNACE)
    s.update(COFIRE_CU)
    s.update(gc_anisotropy=0.0)
    s.update(over)
    return s


def glass_view(s: dict) -> dict:
    return dict(s, anisotropy=s.get("gc_anisotropy", 0.0))


def ratio_limit(T_C: float) -> float:
    """Largest pH2O/pH2 that keeps copper metallic at T (Cu/Cu2O equilibrium)."""
    return float(thermo.h2o_h2_boundary_Cu(T_C + T0C))


@dataclass
class Schedule:
    """Parametric co-firing program (the optimiser's decision variables).

    A  pyrolyse the binder in N2 up to T_A at the guard ramp r_A;
    B  burn out char in steam at T_B for t_B, with H2 set so pH2O/pH2 sits at a fraction s_B of the
       Cu/Cu2O limit (copper stays metallic by construction, steam is as oxidising as that allows);
    C  densify both materials in dry H2/N2 up to T_C, hold t_C;
    D  cool at r_D (reducing gas down to 600 C).
    """
    T_A: float = 460.0
    r_A: float = 1.0
    T_B: float = 780.0
    r_B: float = 3.0
    t_B: float = 2.0
    x_B: float = 0.30
    s_B: float = 0.2
    T_C: float = 960.0
    r_C: float = 5.0
    t_C: float = 1.0
    x_H2_C: float = 0.04
    r_D: float = 5.0
    x_H2_B: Optional[float] = None      # explicit H2 in phase B (e.g. forming gas); overrides s_B

    def cycle(self) -> Cycle:
        xh2_B = self.x_H2_B if self.x_H2_B is not None else self.x_B / (self.s_B * ratio_limit(self.T_B))
        return Cycle([
            Segment(self.T_A, self.r_A, 0.0, 0.0, 0.0, -60.0, "A pyrolysis, N2"),
            Segment(self.T_B, self.r_B, self.t_B, 0.0, xh2_B, -60.0, "B steam burnout", x_h2o=self.x_B),
            Segment(self.T_C, self.r_C, self.t_C, 0.0, self.x_H2_C, -60.0, "C co-sinter, dry H2/N2"),
            Segment(600.0, self.r_D, 0.0, 0.0, self.x_H2_C, -60.0, "D cool, reducing"),
            Segment(25.0, self.r_D, 0.0, 0.0, 0.0, -60.0, "D cool, N2"),
        ], name="co-firing schedule")


def run_pair(s: dict, cyc: Cycle, N: int = 8, rtol: float = 1e-3, keep_states: bool = False):
    """Simulate the glass-ceramic body and the copper conductor through the same program."""
    r_gc = simulate(glass_view(s), cyc, N=N, rtol=rtol, setup_cls=GlassSetup, keep_states=keep_states)
    r_cu = simulate(s, cyc, N=N, rtol=rtol, setup_cls=FilledCopperSetup, keep_states=keep_states)
    return r_gc, r_cu


def crystal_series(r_gc, s: dict) -> np.ndarray:
    su = GlassSetup(glass_view(s))
    return np.asarray(su.crystal_fraction(r_gc.series["G_um"]))
