"""Calibrate the sintering viscosity factor f_eta from interrupted sinter runs, without a dilatometer.

Protocol. Print a batch of identical coupons. Run them through the same cycle (the optimised one)
but interrupt it at different temperatures: when the setpoint first reaches the chosen peak, hold
for the chosen time and cool. Measure each coupon with calipers (linear shrinkage) or by Archimedes (relative
density). Three or four coupons spanning early, middle and late densification pin f_eta to about
+-15 %.

f_eta multiplies the Frost-Ashby viscosity. It absorbs everything the diffusion data do not know
about this powder: surface condition, packing, residual carbon, particle shape. It is correlated
with D50 (viscosity scales with grain size squared), so enter the measured D50, span and solids
loading before fitting.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, replace
from typing import Dict, List, Optional, Sequence

import numpy as np
from scipy.optimize import minimize_scalar

from .cycle import Cycle, Segment
from .simulate import simulate

# measurement standard deviations used to weight the misfit
SIGMA = {"rho": 0.01, "shrink_xy": 0.3, "shrink_z": 0.3}
KPI_OF = {"rho": "rho_final", "shrink_xy": "shrink_xy_pct", "shrink_z": "shrink_z_pct"}


@dataclass
class Coupon:
    peak_C: float
    hold_h: float
    value: float            # rho: relative density (0-1); shrink_xy / shrink_z: linear shrinkage in %
    kind: str = "rho"
    sigma: Optional[float] = None


def interrupted_cycle(base: Cycle, peak_C: float, hold_h: float, ramp_Kmin: float = 5.0,
                      cool_Kmin: float = 10.0) -> Cycle:
    """``base`` interrupted the first time its setpoint reaches ``peak_C`` on heating: hold there for
    ``hold_h`` in that segment's gas, then cool. A peak above anything ``base`` reaches is approached
    at ``ramp_Kmin`` in the gas of the hottest segment."""
    segs: List[Segment] = []
    T = base.T_start_C
    for sg in base.segments:
        if sg.T_end_C < T - 1e-9:                      # base starts cooling: the peak lies above it
            break
        if sg.T_end_C >= peak_C - 1e-9:                # this segment reaches the peak
            segs.append(replace(sg, T_end_C=peak_C, hold_h=hold_h, note=f"to {peak_C:.0f} C, hold {hold_h:g} h"))
            break
        segs.append(sg)
        T = sg.T_end_C
    if not segs or segs[-1].T_end_C != peak_C:
        last = segs[-1] if segs else Segment(T, 1.0, H2=0.04)
        segs.append(Segment(peak_C, ramp_Kmin, hold_h, 0.0, last.H2, last.dp_C, f"to {peak_C:.0f} C, hold {hold_h:g} h"))
    gas = segs[-1]
    segs.append(Segment(600.0, cool_Kmin, 0.0, 0.0, gas.H2, -60.0, "cool"))
    segs.append(Segment(25.0, cool_Kmin, 0.0, note="cool"))
    return Cycle(segs, base.T_start_C, name=f"interrupted at {peak_C:.0f} C / {hold_h:g} h")


def predict(scenario: Dict[str, float], base: Cycle, coupons: Sequence[Coupon], f_eta: float,
            N: int = 8, rtol: float = 1e-3) -> np.ndarray:
    s = dict(scenario, f_eta=float(f_eta))
    out = []
    for c in coupons:
        r = simulate(s, interrupted_cycle(base, c.peak_C, c.hold_h), N=N, rtol=rtol)
        out.append(r.kpi[KPI_OF[c.kind]])
    return np.array(out)


def fit_f_eta(scenario: Dict[str, float], base: Cycle, coupons: Sequence[Coupon], N: int = 8,
              rtol: float = 1e-3, bounds=(0.05, 10.0), xatol: float = 0.02) -> dict:
    """Least-squares f_eta (searched in log space) with a curvature-based 1-sigma band."""
    meas = np.array([c.value for c in coupons])
    sig = np.array([c.sigma or SIGMA[c.kind] for c in coupons])
    cache: Dict[float, np.ndarray] = {}

    def chi2(lnf: float) -> float:
        key = round(lnf, 6)
        if key not in cache:
            cache[key] = predict(scenario, base, coupons, math.exp(lnf), N, rtol)
        return float(np.sum(((cache[key] - meas) / sig) ** 2))

    res = minimize_scalar(chi2, bounds=(math.log(bounds[0]), math.log(bounds[1])), method="bounded",
                          options={"xatol": xatol})
    x0, c0 = float(res.x), float(res.fun)
    h = 0.1
    a = (chi2(x0 + h) + chi2(x0 - h) - 2 * c0) / (2 * h * h)
    dx = 1.0 / math.sqrt(a) if a > 0 else float("inf")
    pred = cache[round(x0, 6)]
    return dict(f_eta=math.exp(x0), f_eta_lo=math.exp(x0 - dx), f_eta_hi=math.exp(x0 + dx), chi2=c0,
                dof=max(len(coupons) - 1, 1), predicted=pred.tolist(), measured=meas.tolist(),
                n_sim=len(cache) * len(coupons))


def synthetic_coupons(scenario: Dict[str, float], base: Cycle, f_eta: float, plan=None, N: int = 8,
                      noise: float = 0.0, seed: int = 0) -> List[Coupon]:
    """Coupons the model itself would produce at ``f_eta`` (for testing and for planning runs)."""
    plan = plan or [(950.0, 0.5, "rho"), (1030.0, 0.5, "shrink_xy"), (1060.0, 2.0, "rho")]
    rng = np.random.default_rng(seed)
    cs = [Coupon(T, h, 0.0, k) for T, h, k in plan]
    vals = predict(scenario, base, cs, f_eta, N)
    return [replace(c, value=float(v + noise * SIGMA[c.kind] * rng.standard_normal())) for c, v in zip(cs, vals)]
