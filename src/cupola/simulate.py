"""Run a furnace program through the digital coupon and summarise the outcome."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

import numpy as np

from .constants import T0C
from . import thermo
from .cycle import Cycle
from .materials import Setup
from .model1d import Slab, Controls, NV, IT, ILV
from .integrate import ode23s, StepFailure
from .params import defaults


def inlet_composition(seg, su: Setup):
    """Inlet gas for a segment, clipped to what the furnace can actually deliver."""
    x_o2 = min(max(seg.O2, 0.0), 0.2095) if su.s["has_air_bleed"] >= 0.5 else 0.0
    x_o2 = x_o2 + su.x_o2_imp * (1.0 - x_o2 / 0.2095)
    x_h2 = min(max(seg.H2, 0.0), su.s["h2_max"])
    if getattr(seg, "x_h2o", None) is not None:          # steam generator: explicit steam fraction
        return x_o2, x_h2, float(min(max(seg.x_h2o, 0.0), 1.0 - x_h2))
    dp = min(seg.dp_C, su.s["dp_max_C"])
    x_h2o = float(thermo.x_h2o_from_dewpoint(dp)) if dp > -60.0 else float(thermo.x_h2o_from_dewpoint(-60.0))
    return x_o2, x_h2, x_h2o


@dataclass
class Result:
    t_h: np.ndarray
    series: Dict[str, np.ndarray]
    kpi: Dict[str, float]
    cycle: Cycle
    scenario: Dict[str, float]
    n_steps: int = 0
    n_rejected: int = 0
    ok: bool = True
    message: str = ""
    Y: Optional[np.ndarray] = None


def simulate(scenario: Optional[dict] = None, cycle: Optional[Cycle] = None, N: Optional[int] = None,
             rtol: float = 1e-4, keep_states: bool = False, stop_when=None, setup_cls=Setup) -> Result:
    s = dict(defaults()) if scenario is None else dict(scenario)
    su = setup_cls(s)
    slab = Slab(su, N)
    if cycle is None:
        from .cycle import baseline_v0
        cycle = baseline_v0()
    segs = cycle.boundaries()
    x0 = inlet_composition(segs[0][2], su)
    Y = slab.y0(cycle.T_start_C + T0C, x0)
    ts_all, ys_all = [0.0], [Y.copy()]
    nst = nrj = 0
    ok, msg = True, ""
    h = None
    for (t0, t1, seg, T_from, kind) in segs:
        xo2, xh2, xh2o = inlet_composition(seg, su)
        Ta = T_from + T0C
        Tb = seg.T_end_C + T0C
        ctl = Controls(t0, t1, Ta, Tb if kind == "ramp" else Tb, xo2, xh2, xh2o)
        if kind == "hold":
            ctl = Controls(t0, t1, Tb, Tb, xo2, xh2, xh2o)
        f = lambda t, y, _c=ctl: slab.evaluate(t, y, _c)
        cb = None
        if stop_when is not None:
            cb = lambda t, y, _c=ctl: stop_when(slab, t, y, _c)
        try:
            ts, ys, a, b = ode23s(f, t0, t1, Y, slab.atol, rtol=rtol, scale=slab.scale,
                                  h0=h, h_max=max(600.0, 0.02 * (t1 - t0)), callback=cb)
        except StepFailure as exc:
            ok, msg = False, f"integration failed in segment '{seg.note}' ({kind}): {exc}"
            break
        nst += a
        nrj += b
        ts_all.extend(ts[1:])
        ys_all.extend(ys[1:])
        Y = ys[-1]
        h = min(max(ts[-1] - ts[-2], 1.0), 600.0) if len(ts) > 1 else None
        if stop_when is not None and ts[-1] < t1 - 1e-6:
            break
    t = np.array(ts_all)
    Ys = np.array(ys_all)
    series, kpi = postprocess(slab, cycle, t, Ys)
    return Result(t / 3600.0, series, kpi, cycle, s, nst, nrj, ok, msg, Ys if keep_states else None)


def _controls_at(cycle: Cycle, su: Setup, t: float) -> Controls:
    for (t0, t1, seg, T_from, kind) in cycle.boundaries():
        if t <= t1 + 1e-9:
            xo2, xh2, xh2o = inlet_composition(seg, su)
            Ta = (T_from if kind == "ramp" else seg.T_end_C) + T0C
            return Controls(t0, t1, Ta, seg.T_end_C + T0C, xo2, xh2, xh2o)
    seg = cycle.segments[-1]
    xo2, xh2, xh2o = inlet_composition(seg, su)
    return Controls(t, t, seg.T_end_C + T0C, seg.T_end_C + T0C, xo2, xh2, xh2o)


def postprocess(slab: Slab, cycle: Cycle, t: np.ndarray, Ys: np.ndarray):
    su = slab.su
    # one vectorised diagnostic evaluation per segment (controls only enter through the setpoint)
    D = None
    bounds = cycle.boundaries()
    edges = [b[1] for b in bounds]
    seg_of = np.minimum(np.searchsorted(edges, t - 1e-9), len(bounds) - 1)
    for k in np.unique(seg_of):
        idx = np.where(seg_of == k)[0]
        t0_, t1_, seg, T_from, kind = bounds[k]
        ctl = _controls_at(cycle, su, 0.5 * (t0_ + t1_))
        _, d = slab.evaluate(t[idx].mean(), Ys[idx], ctl, diag=True)
        if D is None:
            D = {key: np.empty((len(t),) + np.shape(v)[1:]) for key, v in d.items()}
        for key, v in d.items():
            D[key][idx] = np.broadcast_to(v, (len(idx),) + np.shape(v)[1:])
    D["Tset"] = np.array([cycle.T_set_K(ti) for ti in t])

    def col(key, reduce=None):
        a = D[key]
        if reduce == "center":
            return a[:, 0]
        if reduce == "surface":
            return a[:, -1]
        if reduce == "mean":
            return (a * slab.wt).sum(axis=-1)
        if reduce == "max":
            return a.max(axis=-1)
        return a

    node, glob = slab.split(Ys)
    lnV_mean = (node[:, ILV, :] * slab.wt).sum(axis=-1)
    ez = glob[:, 6]
    shrink_xy = 1.0 - np.exp(lnV_mean / 3.0 - ez / 2.0)
    shrink_z = 1.0 - np.exp(lnV_mean / 3.0 + ez)
    b = col("b")                                   # (M, 3, N)
    binder_left = (b.sum(axis=1) * slab.wt).sum(axis=-1)
    series = dict(
        Tset=col("Tset") - T0C, Tf=col("Tf") - T0C,
        T_center=col("T", "center") - T0C, T_surface=col("T", "surface") - T0C,
        exo=col("exo"), exo_gen=col("exo_gen"), dT_int=col("dT_int"),
        binder_left=binder_left, solvent_left=(b[:, 0, :] * slab.wt).sum(axis=-1) / max(su.b0[0] / su.mb0, 1e-12),
        C_ppm_center=col("C_ppm", "center"), C_ppm_mean=col("C_ppm", "mean"),
        O_ppm_center=col("O_ppm", "center"), O_ppm_mean=col("O_ppm", "mean"),
        rho_center=col("rho", "center"), rho_surface=col("rho", "surface"), rho_mean=col("rho", "mean"),
        rho_m_mean=col("rho_m", "mean"),
        eps_open=col("eps_open", "mean"), f_cl_center=col("f_cl", "center"),
        G_um=col("G_um", "mean"), p_trap_bar=(col("p_g", "center")) / 1e5,
        y_center=col("y", "center"),
        dp_gas_bar=col("dp_gas", "max") / 1e5, Pi_gas=col("Pi_gas"), Pi_th=col("Pi_th"),
        Pi_bloat=col("Pi_bloat"), melt_margin=col("melt_margin"),
        xO2=col("xO2"), xH2=col("xH2"), xH2O=col("xH2O"), xCO=col("xCO"), xCO2=col("xCO2"), x_hc=col("x_hc"),
        shrink_xy=shrink_xy, shrink_z=shrink_z,
    )
    series["dewpoint_out"] = np.array(thermo.dewpoint_from_x_h2o(np.maximum(series["xH2O"], 1e-8)))

    # closure event at the centre node (worst case: longest escape path)
    fc = series["f_cl_center"]
    idx = np.where(fc >= 0.5)[0]
    if idx.size:
        i = idx[0]
        C_close, O_close, t_close = series["C_ppm_center"][i], series["O_ppm_center"][i], t[i] / 3600.0
        closed = True
    else:
        C_close, O_close, t_close, closed = np.nan, np.nan, np.nan, False
    rho_f = series["rho_mean"][-1]
    kpi = dict(
        duration_h=t[-1] / 3600.0,
        rho_final=float(rho_f),
        rho_center_final=float(series["rho_center"][-1]),
        shrink_xy_pct=100 * float(shrink_xy[-1]),
        shrink_z_pct=100 * float(shrink_z[-1]),
        C_final_ppm=float(series["C_ppm_mean"][-1]),
        O_final_ppm=float(series["O_ppm_mean"][-1]),
        closed=bool(closed),
        t_close_h=float(t_close),
        C_at_close_ppm=float(C_close),
        O_at_close_ppm=float(O_close),
        Pi_gas_max=float(np.max(series["Pi_gas"])),
        Pi_th_max=float(np.max(series["Pi_th"])),
        # self-heating only counts while the furnace is heating or holding; during cooling the
        # part simply lags (clean Cu has emissivity ~0.1), which is not an exotherm
        exo_max_K=float(max(0.0, np.max(np.where(series["Tset"] >= series["Tf"] - 0.5, series["exo_gen"], -np.inf)))),
        Pi_bloat_max=float(np.max(series["Pi_bloat"])),
        melt_margin_min_K=float(np.min(series["melt_margin"])),
        binder_left_final=float(binder_left[-1]),
        grain_final_um=float(series["G_um"][-1]),
        p_trap_final_bar=float(series["p_trap_bar"][-1]),
        O_peak_ppm=float(np.max(series["O_ppm_mean"])),
        C_peak_ppm=float(np.max(series["C_ppm_mean"])),
        iacs=float(su.iacs(rho_f)),
    )
    # fastest setpoint ramp while >1 % binder remains (the guard constraint)
    dTs = np.gradient(series["Tset"], t / 60.0) if len(t) > 2 else np.zeros_like(t)
    busy = binder_left > 0.01
    kpi["debind_ramp_max_Kmin"] = float(np.max(np.abs(dTs[busy]))) if np.any(busy) else 0.0
    kpi["verdict"] = verdict(kpi, su)
    return series, kpi


def verdict(k, su: Setup) -> Dict[str, dict]:
    """Traffic-light check of every constraint. Index <= 1 passes."""
    def item(value, limit, unit, higher_is_bad=True, label=""):
        idx = value / limit if higher_is_bad else limit / max(value, 1e-12)
        return dict(value=value, limit=limit, unit=unit, index=idx, ok=bool(idx <= 1.0), label=label)
    out = {
        "gas_pressure": item(k["Pi_gas_max"], 1.0, "-", label="Debinding gas pressure / strength (with SF)"),
        "thermal_stress": item(k["Pi_th_max"], 1.0, "-", label="Thermal stress / strength"),
        "self_heating": item(k["exo_max_K"], su.dT_exo, "K", label="Self-heating above furnace"),
        "binder_removed": item(k["binder_left_final"], 1e-3, "-", label="Binder left at end"),
        "carbon_at_closure": item(k["C_at_close_ppm"] if k["closed"] else k["C_final_ppm"], su.C_spec, "ppm",
                                  label="Carbon when pores close"),
        "oxygen_at_closure": item(k["O_at_close_ppm"] if k["closed"] else k["O_final_ppm"], su.O_spec, "ppm",
                                  label="Oxide oxygen when pores close"),
        "melting": dict(value=k["melt_margin_min_K"], limit=0.0, unit="K",
                        index=1.0 - k["melt_margin_min_K"] / 50.0, ok=bool(k["melt_margin_min_K"] >= 0.0),
                        label="Margin below Cu-O solidus"),
        "bloating": item(max(k["Pi_bloat_max"], 0.0), 1.0, "-", label="Trapped-gas pressure / sintering stress"),
        "density": item(k["rho_final"], su.rho_target, "-", higher_is_bad=False, label="Final relative density"),
        "debind_guard": item(k.get("debind_ramp_max_Kmin", 0.0), su.ramp_guard * 1.02, "K/min",
                             label="Ramp while binder remains (guard)"),
    }
    return out
