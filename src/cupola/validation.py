"""Validation cases against published copper data (as opposed to code verification).

Each case returns (label, measured, predicted, note). Used by tests/test_validation.py and
by scripts/validation_report.py, which writes docs/VALIDATION.md.
"""
from __future__ import annotations

import numpy as np

from .constants import T0C, M_O, M_CU
from .cycle import ifam_reference, cea_reference
from .integrate import ode23s
from .materials import Setup
from .model1d import Slab, Controls, IB1, IB3, IX, GTF, GO2
from .params import scenario
from .simulate import simulate


def cu_compact_oxidation(T_hold_C, d50_um=22.0, phi=0.60, rate_Kmin=1.0, hold_h=4.0):
    """Binder-free Cu compact heated in air (TGA-style), returns mass gain wt% relative to Cu."""
    su = Setup(scenario(d50_um=d50_um, phi=phi, half_thickness_mm=0.5, span=1.5))
    sl = Slab(su)
    Y = sl.y0(25 + T0C, (0.2095, 0.0, 0.012))
    node, glob = sl.split(Y)
    node[IB1:IB3 + 1] = 0.0
    Y = np.concatenate([node.ravel(), glob])
    t_r = (T_hold_C - 25.0) / (rate_Kmin / 60.0)
    X_hist = []
    for (t0, t1, Ta, Tb) in ((0.0, t_r, 25.0, T_hold_C), (t_r, t_r + hold_h * 3600, T_hold_C, T_hold_C)):
        ctl = Controls(t0, t1, Ta + T0C, Tb + T0C, 0.2095, 0.0, 0.012)
        ts, ys, *_ = ode23s(lambda t, y: sl.evaluate(t, y, ctl), t0, t1, Y, sl.atol, rtol=1e-4,
                            scale=sl.scale, h_max=600.0)
        Y = ys[-1]
    node, _ = sl.split(Y)
    X = (node[IX] * sl.wt).sum()
    return 100.0 * X * M_O / M_CU


ROUMANIE_OX = [(400.0, 8.0), (600.0, 14.4), (800.0, 16.8)]   # wt% gain, 1 K/min + 4 h dwell in air


def cea_case(**kw):
    return simulate(scenario(d50_um=22.0, span=1.5, phi=0.60, h2_max=1.0, dp_max_C=20.0, **kw),
                    cea_reference(), rtol=1e-3)


def ifam_case(solvent_debind=True, **kw):
    base = dict(d50_um=16.0, span=1.0, phi=0.52, solvent_frac=0.15, h2_max=1.0, dp_max_C=20.0,
                h_conv=40.0, half_thickness_mm=2.0)
    if solvent_debind:
        base["pre_extracted_frac"] = 0.4
    base.update(kw)
    return simulate(scenario(**base), ifam_reference(), rtol=1e-3)
