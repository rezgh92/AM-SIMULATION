"""Robust co-firing design: the paste and programme must work across the uncertainty of the inputs that
decide the timing, not only at their nominal values.

Scenarios: nominal; A, slow char gasification with a low glass transition (the glass seals before the
char has gone); B, fast gasification with a high glass transition (the copper is released before the
glass is ready). The objective is the worst-case largest free-strain mismatch over the two corners, the
constraints of optimise.py must hold at both (the nominal case, between them, is checked at the end), and the copper must reach a minimum conductivity.

    python scripts/paper3/optimise_robust.py <out.json> <budget_h> <min_IACS> [maxiter] [popsize] [workers]
"""
import json, math, sys, time
import numpy as np
from scipy.optimize import differential_evolution

import optimise as opt
from cupola.cofire.run import cofire_scenario, run_pair
from cupola.cofire.metrics import cofire_metrics

SCENARIOS = {
    "nominal": {},
    "A: slow gasification, low Tg": dict(t_half_gasif_h=4.0, gc_Tg_C=719.0),
    "B: fast gasification, high Tg": dict(t_half_gasif_h=1.0, gc_Tg_C=749.0),
}


SEARCH = [k for k in SCENARIOS if k != "nominal"]   # the corners bound the nominal case; it is checked at the end


def evaluate_all(x, N=5, names=None):
    over, cyc = opt.design(x)
    out = {}
    for name in (names or list(SCENARIOS)):
        sc = SCENARIOS[name]
        s = cofire_scenario(**over, **sc)
        try:
            gc, cu = run_pair(s, cyc, N=N)
            m, _ = cofire_metrics(gc, cu, s)
        except Exception:
            return None, cyc
        if not m["ok"]:
            return None, cyc
        out[name] = m
    return out, cyc


def objective(x, budget_h, iacs_min):
    ms, cyc = evaluate_all(x, names=SEARCH)
    if ms is None:
        return 1e6
    pen = 0.0
    for m in ms.values():
        pen += sum(opt.violations(m, iacs_min).values())
    pen += max(0.0, max(m["duration_h"] for m in ms.values()) - budget_h)
    worst = max(m["mismatch_max_pct"] for m in ms.values())
    return math.log10(worst + 1e-3) + 10.0 * pen


if __name__ == "__main__":
    out, budget, iacs_min = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
    maxiter = int(sys.argv[4]) if len(sys.argv) > 4 else 12
    popsize = int(sys.argv[5]) if len(sys.argv) > 5 else 8
    workers = int(sys.argv[6]) if len(sys.argv) > 6 else 3
    t0 = time.time()
    hist = []

    def cb(xk, convergence=None):
        f = objective(xk, budget, iacs_min)
        hist.append(dict(t=time.time() - t0, f=f, x=list(map(float, xk))))
        print(f"[{time.time()-t0:7.0f}s] f={f:.4f} conv={convergence}", flush=True)

    res = differential_evolution(objective, opt.BOUNDS, args=(budget, iacs_min), maxiter=maxiter, popsize=popsize,
                                 tol=1e-3, mutation=(0.5, 1.0), recombination=0.7, seed=11, polish=False,
                                 workers=workers, updating="deferred", callback=cb, init="sobol")
    ms, cyc = evaluate_all(res.x, N=8)
    spec = dict(opt.SPEC, iacs=iacs_min)
    json.dump(dict(budget_h=budget, objective="worst-case mismatch", spec=spec, scenarios=SCENARIOS,
                   x=list(map(float, res.x)), names=opt.NAMES, f=float(res.fun),
                   metrics=ms["nominal"] if ms else None, metrics_scenarios=ms,
                   violations={k: opt.violations(m, iacs_min) for k, m in ms.items()} if ms else None,
                   cycle=cyc.to_dict(), history=hist, nfev=int(res.nfev), wall_s=time.time() - t0),
              open(out, "w"), indent=1)
    print(json.dumps({k: {kk: round(v, 3) for kk, v in m.items() if isinstance(v, float)} for k, m in ms.items()}, indent=1))
