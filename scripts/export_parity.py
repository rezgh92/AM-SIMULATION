"""Reference data for the JS parity test: RHS values on real trajectory states, plus full runs."""
import json, sys
import numpy as np
from pathlib import Path
from cupola.params import defaults, scenario
from cupola.simulate import simulate, _controls_at
from cupola.cycle import baseline_v0, Cycle, Segment
from cupola.materials import Setup
from cupola.model1d import Slab

out = {"rhs": [], "runs": []}
# ---- RHS cases from states along the v0 trajectory
s = defaults()
r = simulate(s, baseline_v0(), rtol=1e-3, keep_states=True)
su = Setup(s); sl = Slab(su)
idx = np.linspace(0, len(r.t_h) - 1, 40).astype(int)
for i in idx:
    t = r.t_h[i] * 3600
    ctl = _controls_at(baseline_v0(), su, t)
    dY = sl.evaluate(t, r.Y[i], ctl)
    _, d = sl.evaluate(t, r.Y[i], ctl, diag=True)
    out["rhs"].append(dict(t=t, Y=r.Y[i].tolist(), ctl=[ctl.t0, ctl.t1, ctl.Ta, ctl.Tb, ctl.xO2_in, ctl.xH2_in, ctl.xH2O_in],
                           dY=dY.tolist(), Pi_gas=float(d["Pi_gas"]), exo=float(d["exo"]), melt=float(d["melt_margin"].min())))
out["scenario"] = s
# ---- full runs
runs = [
    ("v0_default", defaults(), baseline_v0().to_dict()),
    ("short_ox_22um", scenario(d50_um=22.0, span=1.5, h2_max=1.0, half_thickness_mm=1.5),
     Cycle([Segment(400, 2.0, 2.0, 0.21, 0, 10), Segment(700, 5, 1.0, 0, 0.04, 20), Segment(1050, 5, 2.0, 0, 1.0, -60),
            Segment(25, 10, 0, 0, 0.04, -60)]).to_dict()),
]
for name, sc, cyc in runs:
    rr = simulate(sc, Cycle.from_dict(cyc), rtol=1e-3)
    k = {kk: (v if not isinstance(v, (np.floating, float)) else float(v)) for kk, v in rr.kpi.items() if kk != "verdict"}
    grid = np.linspace(0, rr.t_h[-1], 60)
    ser = {key: np.interp(grid, rr.t_h, rr.series[key]).tolist() for key in
           ("T_center", "binder_left", "C_ppm_mean", "O_ppm_mean", "rho_mean", "xO2", "xH2O", "Pi_gas")}
    out["runs"].append(dict(name=name, scenario=sc, cycle=cyc, kpi=k, grid=grid.tolist(), series=ser))
p = Path(__file__).resolve().parents[1] / "dashboard" / "engine" / "parity_ref.json"
def clean(o):
    if isinstance(o, dict):
        return {k: clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    if isinstance(o, float) and not np.isfinite(o):
        return None
    return o
p.write_text(json.dumps(clean(out), allow_nan=False))
print("wrote", p)
