"""Summary metrics of the 3-D package runs: shrinkage, flatness of the top frame, distortion of the cavity
floor and change of the cavity opening, all relative to a uniformly shrunk part."""
import json, sys, os
import numpy as np

D = sys.argv[1]
out = {}
for k in ("baseline", "optimised", "robust"):
    f = f"{D}/package_{k}.json"
    if not os.path.exists(f):
        continue
    r = json.load(open(f))
    p0 = np.array(r["p0"]); p = np.array(r["p"]); h = r["h_mm"] * 1e-3
    mat = np.array(r["mat"]); th = np.array(r["theta"])
    zt = p0[:, 2].max()
    top = np.isclose(p0[:, 2], zt)
    # cavity: top-frame nodes adjacent to the opening, and the floor nodes inside it
    ix = np.round((p0[:, 0] - p0[:, 0].min()) / h).astype(int)
    iy = np.round((p0[:, 1] - p0[:, 1].min()) / h).astype(int)
    colmax = {}
    for n in range(len(p0)):
        key = (ix[n], iy[n])
        if key not in colmax or p0[n, 2] > p0[colmax[key], 2]:
            colmax[key] = n
    upper = np.array(list(colmax.values()))
    floor = upper[p0[upper, 2] < zt - 1e-9]
    if len(floor) == 0:                      # a part without a cavity (earlier test vehicle)
        continue
    s = float(np.sum(p[upper, 2] * p0[upper, 2]) / np.sum(p0[upper, 2] ** 2))
    dev = (p[:, 2] - s * p0[:, 2]) * 1e6
    lx0 = np.ptp(p0[:, 0]); lx = np.ptp(p[:, 0])
    cav0 = np.ptp(p0[floor, 0]); cav = np.ptp(p[floor, 0])
    out[k] = dict(shrink_xy_pct=r["shrink_xy_pct"], shrink_z_pct=r["shrink_z_pct"],
                  frame_range_um=float(np.ptp(p[top, 2]) * 1e6),
                  upper_dev_range_um=float(np.ptp(dev[upper])),
                  floor_minus_frame_um=float(dev[floor].mean() - dev[top].mean()),
                  floor_range_um=float(np.ptp(dev[floor])),
                  cavity_shrink_pct=float(100 * (1 - cav / cav0)), body_shrink_pct=float(100 * (1 - lx / lx0)),
                  rho_gc=float(1 - th[mat == 0].mean()), rho_cu=float(1 - th[mat == 1].mean()),
                  T_stop_C=r.get("T_stop_C"), n_el=r["n_el"])
    print(k, {a: round(b, 2) if isinstance(b, float) else b for a, b in out[k].items()})
json.dump(out, open(f"{D}/package_metrics.json", "w"), indent=1)
