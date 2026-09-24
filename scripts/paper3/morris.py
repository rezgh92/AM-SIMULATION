"""Morris elementary-effects screening of the uncertain inputs for the co-firing outcomes."""
import json, sys, time
import numpy as np
from concurrent.futures import ProcessPoolExecutor
from cupola.cycle import Cycle
from cupola.cofire.run import cofire_scenario, run_pair
from cupola.cofire.metrics import cofire_metrics

# (key, lo, hi, log): uncertainty ranges around the calibrated values (Table 1 of the paper). The copper
# paste factors are appended at run time as a manufacturing tolerance around the design being tested.
FACTORS = [
    ("gc_Tg_C", 714.0, 754.0, False), ("gc_fragility", 28.0, 40.0, False), ("gc_Tp_cryst_C", 1000.0, 1080.0, False),
    ("gc_E_cryst", 250.0, 470.0, False), ("gc_n_avrami", 1.5, 3.7, False), ("gc_gamma", 0.24, 0.36, False),
    ("gc_d50_um", 2.0, 7.0, False), ("gc_phi", 0.40, 0.50, False), ("t_half_gasif_h", 0.5, 8.0, True),
    ("E_gasif", 160.0, 240.0, False), ("char_yield", 0.02, 0.10, False), ("f_eta", 0.1, 1.0, True),
]
OUTS = ["log10_gc_C", "gc_rho", "gc_X", "cu_rho", "cu_iacs", "mismatch_max_pct", "kappa_final", "line_Pi_max"]


def value(f, u):
    k, lo, hi, lg = f
    return lo * (hi / lo) ** u if lg else lo + (hi - lo) * u


def run(args):
    u, base, cyc_d, factors = args
    over = dict(base)
    over.update({f[0]: value(f, ui) for f, ui in zip(factors, u)})
    s = cofire_scenario(**over)
    try:
        gc, cu = run_pair(s, Cycle.from_dict(cyc_d), N=6)
        m, _ = cofire_metrics(gc, cu, s)
        m["log10_gc_C"] = float(np.log10(max(m["gc_C_close_ppm"], 1e-3)))
        return [m[o] for o in OUTS]
    except Exception:
        return [np.nan] * len(OUTS)


if __name__ == "__main__":
    out, design_path = sys.argv[1], sys.argv[2]
    r = int(sys.argv[3]) if len(sys.argv) > 3 else 16
    d = json.load(open(design_path))
    base = dict(d50_um=10 ** d["x"][0], cu_filler=d["x"][1], phi=d["x"][2])
    cyc_d = d["cycle"]
    FACTORS = FACTORS + [("d50_um", 0.75 * base["d50_um"], 1.33 * base["d50_um"], True),
                         ("cu_filler", max(base["cu_filler"] - 0.05, 0.0), base["cu_filler"] + 0.05, False)]
    k, p = len(FACTORS), 4
    delta = p / (2.0 * (p - 1))
    rng = np.random.default_rng(3)
    trajs = []
    for _ in range(r):
        x = rng.integers(0, p - 1, size=k) / (p - 1)
        x = np.where(x + delta > 1.0, x - delta, x)
        pts = [x.copy()]
        for i in rng.permutation(k):
            x = x.copy()
            x[i] = x[i] + delta if x[i] + delta <= 1.0 + 1e-9 else x[i] - delta
            pts.append((x.copy(), i))
        trajs.append(pts)
    fixed = {k_: v for k_, v in base.items() if k_ not in [f[0] for f in FACTORS]}
    jobs = []
    for tr in trajs:
        jobs.append((tr[0], fixed, cyc_d, FACTORS))
        for x, i in tr[1:]:
            jobs.append((x, fixed, cyc_d, FACTORS))
    t0 = time.time()
    with ProcessPoolExecutor(4) as ex:
        Y = np.array(list(ex.map(run, jobs)))
    print("runs", len(jobs), "wall", round(time.time() - t0), "s")
    EE = {o: [[] for _ in FACTORS] for o in OUTS}
    j = 0
    for tr in trajs:
        y_prev = Y[j]; x_prev = tr[0]; j += 1
        for x, i in tr[1:]:
            y = Y[j]; j += 1
            step = x[i] - x_prev[i]
            for oi, o in enumerate(OUTS):
                EE[o][i].append((y[oi] - y_prev[oi]) / step)
            y_prev, x_prev = y, x
    res = {}
    for o in OUTS:
        res[o] = [dict(key=f[0], mu_star=float(np.nanmean(np.abs(e))), sigma=float(np.nanstd(e)), mu=float(np.nanmean(e)))
                  for f, e in zip(FACTORS, EE[o])]
    json.dump(dict(factors=[dict(key=f[0], lo=f[1], hi=f[2], log=f[3]) for f in FACTORS], r=r, outputs=OUTS, result=res),
              open(out, "w"), indent=1)
