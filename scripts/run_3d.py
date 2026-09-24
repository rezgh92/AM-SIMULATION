"""Run a 3-D geometry through a cycle and export it for the dashboard.

    python scripts/run_3d.py <geometry> <cycle.json | v0> <voxel_mm> <out.json>
"""
import json, sys, time
from pathlib import Path
from cupola.params import defaults
from cupola.materials import Setup
from cupola.cycle import Cycle, baseline_v0
from cupola.simulate import simulate
from cupola.fem3d.driver import run_geometry, summarise, export


def main():
    geom, cyc_arg, h, out = sys.argv[1], sys.argv[2], float(sys.argv[3]), Path(sys.argv[4])
    s = defaults()
    cyc = baseline_v0() if cyc_arg == "v0" else Cycle.from_dict(json.loads(Path(cyc_arg).read_text()))
    r = simulate(s, cyc, rtol=1e-4)
    print(f"1-D: rho {r.kpi['rho_final']:.4f} shrink {r.kpi['shrink_xy_pct']:.2f}/{r.kpi['shrink_z_pct']:.2f} %", flush=True)
    t = time.time()
    s3, frames, info, t0 = run_geometry(geom, r, Setup(s), h=h, n_frames=24)
    sm = summarise(s3, info)
    sm.update(cycle=cyc.name or cyc_arg, duration_h=cyc.duration_h(), wall_s=round(time.time() - t),
              rho_1d=r.kpi["rho_final"], shrink_1d_xy=r.kpi["shrink_xy_pct"], shrink_1d_z=r.kpi["shrink_z_pct"])
    export(s3, frames, info, sm, out, t0)
    print(json.dumps(sm, indent=1), flush=True)


if __name__ == "__main__":
    main()
