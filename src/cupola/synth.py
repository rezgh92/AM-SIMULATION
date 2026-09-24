"""Cycle synthesis: the fastest furnace program that keeps every risk index inside its limit.

Minimum-time problems with a monotone path constraint have a simple optimal structure:
ride the most restrictive constraint. The synthesizer does exactly that, as a one-step
model-predictive controller on the digital coupon:

  every control interval (default 15 min) it tries candidate (ramp rate, atmosphere) pairs from
  most to least aggressive, simulates the interval from the current state, and keeps the first
  one whose predicted risk indices stay below ``margin`` x limit.

Phases follow the chemistry, and each ends on a measured event, not a fixed time:
  A  debind      pyrolysis (N2) or O2-throttled oxidation, until binder < 0.1 %
  B  chemistry   forming gas (humidified if available): reduce oxide + gasify char at a hold
                 temperature T_B, until C and O are below spec at the centre node
  C  densify     H2-rich dry gas, ramp to the solidus-limited peak, hold to target density
  D  cool        reducing to 600 C, then inert

An outer enumeration over atmosphere topologies (WGS = never oxidise; OX-x = O2 capped at x)
and over T_B picks the fastest feasible combination. The result is quantised into
furnace segments and re-verified end to end with the full model at tight tolerance.
"""
from __future__ import annotations

import copy
import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import numpy as np

from .constants import T0C
from . import thermo
from .cycle import Cycle, Segment
from .integrate import ode23s, StepFailure
from .materials import Setup
from .model1d import Slab, Controls, NV, IB1, IB3, IC, IX, ILV, GTF
from .params import defaults
from .simulate import simulate, inlet_composition, Result

DT_CTRL = 900.0                    # s, control interval while ramping
DT_HOLD = 1800.0                   # s, check interval while holding for an event
MAX_ITER = 400                     # hard cap on control intervals per phase (never hang on a bad candidate)
RAMPS = [10.0, 5.0, 3.0, 2.0, 1.0, 0.5, 0.25, 0.1, 0.05, 0.0]    # K/min, tried in this order


@dataclass
class Atmos:
    O2: float = 0.0
    H2: float = 0.0
    dp_C: float = -60.0

    def key(self):
        return (round(self.O2, 6), round(self.H2, 4), round(self.dp_C, 1))


@dataclass
class Interval:
    t0: float
    t1: float
    T0_C: float
    T1_C: float
    atm: Atmos
    phase: str
    limit: str          # what bound the choice ("ramp_max", "gas", "exo", "thermal", "spec", ...)


class Runner:
    """Holds the coupon state and advances it interval by interval."""

    def __init__(self, scenario: dict, rtol=1e-3):
        self.s = dict(scenario)
        self.su = Setup(self.s)
        self.slab = Slab(self.su)
        self.rtol = rtol
        self.t = 0.0
        self.Tset = 25.0 + T0C
        self.Y = self.slab.y0(self.Tset, (0.0, 0.0, float(thermo.x_h2o_from_dewpoint(-60.0))))
        self.log: List[Interval] = []
        self.h = None

    def clone(self):
        c = copy.copy(self)
        c.Y = self.Y.copy()
        c.log = list(self.log)
        return c

    def _inlet(self, atm: Atmos):
        seg = Segment(0, 1, 0, atm.O2, atm.H2, atm.dp_C)
        return inlet_composition(seg, self.su)

    def advance(self, dt, ramp_Kmin, T_cap_K, atm: Atmos, exo_abort=None):
        """Integrate one interval; returns diagnostics dict (max risk indices) or None on failure.

        ``exo_abort``: stop as soon as the part runs this many K above the furnace while heating or
        holding. A trial that crosses its self-heating limit is rejected anyway, and integrating a
        thermal runaway to the end of the interval is by far the most expensive thing the
        synthesizer would otherwise do.
        """
        T_end = self.Tset + np.sign(T_cap_K - self.Tset) * min(abs(T_cap_K - self.Tset), ramp_Kmin / 60.0 * dt)
        xo2, xh2, xh2o = self._inlet(atm)
        ctl = Controls(self.t, self.t + dt, self.Tset, T_end, xo2, xh2, xh2o)
        f = lambda t, y: self.slab.evaluate(t, y, ctl)
        N = self.slab.N
        cb = None
        if exo_abort is not None and T_end >= self.Tset - 1e-9:
            cb = lambda t, y: bool(np.max(y[:N]) - y[NV * N] > exo_abort)
        try:
            ts, ys, *_ = ode23s(f, self.t, self.t + dt, self.Y, self.slab.atol, rtol=self.rtol,
                                scale=self.slab.scale, h0=self.h, h_max=600.0, callback=cb)
        except StepFailure:
            return None
        if ts[-1] < self.t + dt - 1e-6:          # aborted: report the violation, do not commit
            return dict(Pi_gas=0.0, Pi_th=0.0, exo=np.inf, melt=np.inf, state=None)
        ys = np.array(ys)
        _, d = self.slab.evaluate(ts[-1], ys, ctl, diag=True)
        heating = np.asarray(d["Tset"]) >= np.asarray(d["Tf"]) - 0.5
        diag = dict(
            Pi_gas=float(np.max(d["Pi_gas"])),
            Pi_th=float(np.max(d["Pi_th"])),
            exo=float(np.max(np.where(heating, d["exo_gen"], -np.inf))) if np.any(heating) else -np.inf,
            melt=float(np.min(d["melt_margin"])),
            state=d,
        )
        self.h = min(max(ts[-1] - ts[-2], 1.0), 600.0) if len(ts) > 1 else None
        self.t += dt
        self.Tset = T_end
        self.Y = ys[-1]
        return diag

    # ------------------------------------------------------------------ state summaries
    def centre(self):
        _, d = self.slab.evaluate(self.t, self.Y, Controls(self.t, self.t, self.Tset, self.Tset, 0, 0, 0),
                                  diag=True)
        return d

    def binder_left(self):
        node, _ = self.slab.split(self.Y)
        return float((node[IB1:IB3 + 1].sum(axis=0) * self.slab.wt).sum())


def _ok(diag, su: Setup, margin):
    if diag is None:
        return False, "solver"
    if diag["Pi_gas"] > margin:
        return False, "gas"
    if diag["Pi_th"] > margin:
        return False, "thermal"
    if diag["exo"] > margin * su.dT_exo:
        return False, "exo"
    if diag["melt"] < -0.5:
        return False, "melt"
    return True, ""


def _step(run: Runner, T_cap_K, atm_options: List[Atmos], phase: str, margin: float, dt=DT_CTRL,
          ramps=RAMPS, hold_reason=""):
    """Advance one interval with the most aggressive safe (ramp, atmosphere).

    Recoverability: a move is accepted only if, after it, holding the setpoint in the gentlest
    atmosphere for one more interval is also safe. Without this two-step horizon a greedy controller
    ramps into states from which every option violates a limit (e.g. solvent flashing off inside a
    still-closed pore network).
    """
    su = run.su
    ramp_max = su.s["max_ramp_Kmin"]
    at_cap = abs(run.Tset - T_cap_K) < 1e-6
    first_fail = None
    # warm start: begin one level above the ramp accepted last time in this phase (a constraint
    # that bound a moment ago almost always still binds), instead of re-trying from the maximum
    last = getattr(run, "_last_ramp", {}).get(phase)
    if last is not None and not at_cap and last in ramps:
        k = ramps.index(last)
        ramps = ramps[max(0, k - 1):]
    # same warm start for the atmosphere (e.g. the O2 level of a throttled burn)
    last_atm = getattr(run, "_last_atm", {}).get(phase)
    if last_atm is not None and len(atm_options) > 1:
        keys = [a.key() for a in atm_options]
        if last_atm in keys:
            atm_options = atm_options[max(0, keys.index(last_atm) - 1):]
    # runaway abort only where exothermic chemistry exists (binder burn, oxide reduction)
    exo_abort = margin * su.dT_exo if phase.startswith(("A", "B")) else None
    for atm in atm_options:
        for r in ramps:
            if r > ramp_max:
                continue
            if at_cap and r > 0:
                r = 0.0
            trial = run.clone()
            diag = trial.advance(dt, r, T_cap_K, atm, exo_abort=exo_abort)
            ok, why = _ok(diag, su, margin)
            if ok and (r > 0 or atm is not atm_options[-1]):
                probe = trial.clone()
                ok, why2 = _ok(probe.advance(dt, 0.0, T_cap_K, atm_options[-1], exo_abort=exo_abort), su, margin)
                why = why or ("lookahead-" + why2 if not ok else "")
            if ok:
                if at_cap:
                    limit = hold_reason or "hold"
                elif r == min(ramp_max, ramps[0]) and atm is atm_options[0]:
                    limit = "guard" if ramps[0] < min(ramp_max, RAMPS[0]) and phase.startswith("A") else "ramp_max"
                else:
                    limit = first_fail or ""
                run.__dict__.update(trial.__dict__)
                if not at_cap:
                    lr = dict(getattr(run, "_last_ramp", {}))
                    lr[phase] = r
                    run._last_ramp = lr
                la = dict(getattr(run, "_last_atm", {}))
                la[phase] = atm.key()
                run._last_atm = la
                T0 = run.log[-1].T1_C if run.log else 25.0
                run.log.append(Interval(run.t - dt, run.t, T0, run.Tset - T0C, atm, phase, limit))
                return diag
            if first_fail is None:
                first_fail = why
            if at_cap:
                break
    # nothing safe: hold in the least aggressive atmosphere (should be rare; flagged)
    atm = atm_options[-1]
    diag = run.advance(dt, 0.0, T_cap_K, atm)
    T0 = run.log[-1].T1_C if run.log else 25.0
    run.log.append(Interval(run.t - dt, run.t, T0, run.Tset - T0C, atm, phase, "INFEASIBLE:" + (first_fail or "")))
    return diag


# ---------------------------------------------------------------------------- phases
def phase_debind(run: Runner, o2_cap: float, margin: float, T_end_C=600.0, max_h=300.0):
    su = run.su
    air = su.s["has_air_bleed"] >= 0.5
    if o2_cap > 0 and air:
        levels = [lv for lv in (0.21, 0.05, 0.02, 0.005, 0.002, 0.0005) if lv <= o2_cap + 1e-12] + [0.0]
    else:
        levels = [0.0]
    opts = [Atmos(O2=lv) for lv in levels]
    guard = su.ramp_guard
    while run.t < max_h * 3600.0:
        ramps = [r for r in RAMPS if r <= guard] if run.binder_left() > 0.01 else RAMPS
        if guard not in ramps and run.binder_left() > 0.01:
            ramps = [guard] + ramps
        diag = _step(run, T_end_C + T0C, opts, "A debind", margin, ramps=ramps)
        if run.log and run.log[-1].limit == "" and run.binder_left() > 0.01 and \
                abs((run.log[-1].T1_C - run.log[-1].T0_C) / 15.0 - guard) < 1e-6:
            run.log[-1].limit = "guard"
        if run.binder_left() < 1e-3 and run.Tset >= 450 + T0C:
            break
        if run.Tset >= T_end_C + T0C - 1e-6 and run.binder_left() < 1e-3:
            break
    return run


def phase_chem(run: Runner, T_B_C: float, margin: float, max_h=60.0):
    """Reduce oxide and remove char before pores close."""
    su = run.su
    h2 = min(0.04, su.s["h2_max"]) if su.s["h2_max"] > 0 else 0.0
    dp = su.s["dp_max_C"]
    atm_wet = Atmos(O2=0.0, H2=h2, dp_C=dp)
    t_start = run.t
    opts = [atm_wet]
    while run.t - t_start < max_h * 3600.0:
        d = run.centre()
        C_c, O_c = float(d["C_ppm"][0]), float(d["O_ppm"][0])
        at_T = run.Tset >= T_B_C + T0C - 1e-6
        if at_T and C_c <= su.C_spec * 0.5 and O_c <= min(su.O_spec, 80.0) * 0.5:
            return True
        if float(d["f_cl"][0]) > 0.02:
            return False               # pores started to close before the chemistry finished
        _step(run, T_B_C + T0C, opts, "B chemistry", margin, hold_reason="C/O removal",
              dt=DT_HOLD if at_T else DT_CTRL)
    return False


def phase_densify(run: Runner, margin: float, max_hold_h=8.0):
    su = run.su
    h2 = su.s["h2_max"]
    atm = Atmos(O2=0.0, H2=h2, dp_C=-60.0)
    d = run.centre()
    O = float(np.max(d["O_ppm"]))
    # 1 K inside the (already conservative) margin, with a 5 ppm oxygen allowance, so numerical noise at
    # the peak cannot read as melting
    T_peak = float(thermo.T_solidus_Cu_O(O + 5.0)) - su.T_margin - 1.0 - T0C
    T_peak = min(T_peak, su.s["T_furnace_max_C"])
    guard = 0
    while run.Tset < T_peak + T0C - 1e-6 and guard < MAX_ITER:
        _step(run, T_peak + T0C, [atm], "C densify", margin)
        guard += 1
    t_hold = run.t
    last_rho = None
    while run.t - t_hold < max_hold_h * 3600.0:
        d = run.centre()
        rho = float(np.sum(d["rho"] * run.slab.wt))
        if rho >= su.rho_target:
            break
        if last_rho is not None and (rho - last_rho) < 1e-3 * DT_HOLD / 3600.0:   # < 0.1 %/h: stalled
            break
        last_rho = rho
        _step(run, T_peak + T0C, [atm], "C densify", margin, ramps=[0.0], hold_reason="densification", dt=DT_HOLD)
    return run


def phase_cool(run: Runner, margin: float):
    su = run.su
    atm_red = Atmos(O2=0.0, H2=min(0.04, su.s["h2_max"]), dp_C=-60.0)
    guard = 0
    while run.Tset > 600 + T0C + 1e-6 and guard < MAX_ITER:
        _step(run, 600 + T0C, [atm_red], "D cool", margin, ramps=[su.s["max_ramp_Kmin"]])
        guard += 1
    while run.Tset > 25 + T0C + 1e-6 and guard < 2 * MAX_ITER:
        _step(run, 25 + T0C, [Atmos()], "D cool", margin, ramps=[su.s["max_ramp_Kmin"]], dt=1800.0)
        guard += 1
    return run


# ---------------------------------------------------------------------------- quantisation
def quantise(log: List[Interval], rel_tol=0.25) -> Cycle:
    """Merge consecutive intervals with the same atmosphere and similar ramp into furnace segments."""
    segs: List[Segment] = []
    cur = None
    for iv in log:
        dT = iv.T1_C - iv.T0_C
        dt_min = (iv.t1 - iv.t0) / 60.0
        rate = abs(dT) / dt_min if dt_min > 0 else 0.0
        is_hold = abs(dT) < 1e-6
        key = (iv.atm.key(), is_hold, iv.phase)
        if cur is not None and cur["key"] == key and (is_hold or abs(rate - cur["rate"]) <= rel_tol * max(cur["rate"], 1e-9)):
            cur["dT"] += dT
            cur["dt"] += dt_min
            cur["rate"] = abs(cur["dT"]) / cur["dt"] if not is_hold else 0.0
            cur["T1"] = iv.T1_C
            cur["limits"].add(iv.limit)
        else:
            if cur is not None:
                segs.append(_to_segment(cur))
            cur = dict(key=key, dT=dT, dt=dt_min, rate=rate, T0=iv.T0_C, T1=iv.T1_C, atm=iv.atm, hold=is_hold,
                       phase=iv.phase, limits={iv.limit})
    if cur is not None:
        segs.append(_to_segment(cur))
    # fold holds into the preceding segment when the atmosphere matches
    out: List[Segment] = []
    for sg in segs:
        if out and sg.ramp_Kmin == 0.0 and out[-1].hold_h == 0.0 and abs(out[-1].T_end_C - sg.T_end_C) < 1e-6 \
                and (out[-1].O2, out[-1].H2, out[-1].dp_C) == (sg.O2, sg.H2, sg.dp_C):
            out[-1].hold_h = sg.hold_h
            lim = sg.note.split("[", 1)[1].rstrip("]") if "[" in sg.note else "hold"
            out[-1].note += f" + hold [{lim}]"
            continue
        out.append(sg)
    return Cycle(out, name="synthesised")


def _to_segment(cur) -> Segment:
    lim = ",".join(sorted(x for x in cur["limits"] if x))
    note = f"{cur['phase']}" + (f" [{lim}]" if lim else "")
    if cur["hold"]:
        return Segment(round(cur["T1"], 1), 1.0, round(cur["dt"] / 60.0, 3), cur["atm"].O2, cur["atm"].H2,
                       cur["atm"].dp_C, note)
    rate = round(cur["rate"], 4)
    return Segment(round(cur["T1"], 1), rate, 0.0, cur["atm"].O2, cur["atm"].H2, cur["atm"].dp_C, note)


# ---------------------------------------------------------------------------- top level
@dataclass
class Candidate:
    topology: str
    T_B_C: float
    feasible: bool
    duration_h: float
    cycle: Optional[Cycle]
    note: str = ""
    result: Optional[Result] = None


@dataclass
class Synthesis:
    best: Optional[Candidate]
    candidates: List[Candidate]
    scenario: dict


def topologies(s: dict) -> Dict[str, float]:
    t = {"WGS (pyrolyse in N2, gasify in wet H2)": 0.0}
    if s["has_air_bleed"] >= 0.5:
        t["OX-0.2% (O2-throttled burn)"] = 0.002
        t["OX-2% (O2-throttled burn)"] = 0.02
        t["OX-air"] = 0.21
    return t


def synthesize(scenario: Optional[dict] = None, margin: float = 0.8, T_B_list=(800.0, 875.0, 950.0, 1000.0),
               topo_filter=None, verify=True, verbose=False) -> Synthesis:
    s = dict(defaults()) if scenario is None else dict(scenario)
    cands: List[Candidate] = []
    for name, o2cap in topologies(s).items():
        if topo_filter and not any(f in name for f in topo_filter):
            continue
        base = Runner(s)
        phase_debind(base, o2cap, margin)
        if verbose:
            print(f"[{name}] debind done at {base.t/3600:.1f} h, T={base.Tset-T0C:.0f} C")
        for TB in T_B_list:
            run = base.clone()
            ok = phase_chem(run, TB, margin)
            if not ok:
                cands.append(Candidate(name, TB, False, run.t / 3600.0, None, "pores closed before C/O cleared"))
                if verbose:
                    print(f"  T_B={TB}: infeasible")
                continue
            phase_densify(run, margin)
            phase_cool(run, margin)
            cyc = quantise(run.log)
            cyc.name = f"{name} | T_B {TB:.0f} C"
            infeasible = any(iv.limit.startswith("INFEASIBLE") for iv in run.log)
            cands.append(Candidate(name, TB, not infeasible, cyc.duration_h(), cyc,
                                   "unsafe interval forced" if infeasible else ""))
            if verbose:
                print(f"  T_B={TB}: {cyc.duration_h():.1f} h, {len(cyc.segments)} segments")
    feas = [c for c in cands if c.feasible and c.cycle is not None]
    best = min(feas, key=lambda c: c.duration_h) if feas else None
    if best is not None and verify:
        best.result = simulate(s, best.cycle, rtol=1e-4)
    return Synthesis(best, cands, s)
