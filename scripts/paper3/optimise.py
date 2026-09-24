"""Co-firing design optimisation: copper paste + furnace schedule.

Decision variables (bounds below): copper D50 (log), filler fraction, copper solids loading; burnout
temperature, time and steam fraction; matching-hold temperature and time; heating rate to the peak;
peak temperature and hold.

Objective (epsilon-constraint form): minimise the largest free-strain mismatch between copper and
glass-ceramic (optionally, the final free camber of the reference Cu/GC bilayer), subject to hard
constraints on chemistry, density and damage, and to a cycle-time budget.
Constraint violations enter as a large smooth penalty, so differential evolution always has a
gradient back towards feasibility.

    python scripts/paper3/optimise.py <out.json> <time_budget_h> [maxiter] [popsize] [mismatch|camber] [workers] [min_IACS]
"""
import json, math, sys, time
import numpy as np
from scipy.optimize import differential_evolution

from cupola.cycle import Cycle, Segment
from cupola.cofire.run import cofire_scenario, run_pair, ratio_limit
from cupola.cofire.metrics import cofire_metrics

NAMES = ["log10_d50", "filler", "phi_cu", "T_B", "log10_tB", "x_B", "T_H", "log10_tH", "r_C", "T_C", "t_C"]
BOUNDS = [(0.0, 1.3), (0.0, 0.40), (0.40, 0.60), (650.0, 850.0), (-0.6, 1.3), (0.05, 0.90),
          (820.0, 960.0), (-1.0, 0.7), (1.0, 10.0), (900.0, 1060.0), (0.0, 4.0)]
SPEC = dict(gc_C=100.0, cu_C=200.0, gc_rho=0.97, gc_X=0.80, cu_rho=0.92, Pi_line=1.0, bloat=1.2, melt=0.0, iacs=0.0)
# bloat: closed-pore gas pressure over sintering stress. It settles at 1.04 when pores reach pressure
# equilibrium (saturated back-pressure law), so only values clearly above that mean swelling.


def design(x):
    d = dict(zip(NAMES, x))
    over = dict(d50_um=10 ** d["log10_d50"], cu_filler=d["filler"], phi=d["phi_cu"])
    T_B, t_B, x_B = d["T_B"], 10 ** d["log10_tB"], d["x_B"]
    T_H, t_H = max(d["T_H"], T_B + 10.0), 10 ** d["log10_tH"]
    T_C = max(d["T_C"], T_H)
    xh2_B = x_B / (0.2 * ratio_limit(T_B))
    cyc = Cycle([
        Segment(460.0, 1.0, 0.0, 0.0, 0.0, -60.0, "A pyrolysis, N2"),
        Segment(T_B, 3.0, t_B, 0.0, xh2_B, -60.0, "B steam burnout", x_h2o=x_B),
        Segment(T_H, d["r_C"], t_H, 0.0, 0.04, -60.0, "C1 matching hold, dry 4 % H2"),
        Segment(T_C, d["r_C"], d["t_C"], 0.0, 0.04, -60.0, "C2 peak, dry 4 % H2"),
        Segment(600.0, 5.0, 0.0, 0.0, 0.04, -60.0, "D cool, reducing"),
        Segment(25.0, 5.0, 0.0, 0.0, 0.0, -60.0, "D cool, N2"),
    ], name="optimised co-firing")
    return over, cyc


def evaluate(x, N=6):
    over, cyc = design(x)
    s = cofire_scenario(**over)
    try:
        gc, cu = run_pair(s, cyc, N=N)
        m, _ = cofire_metrics(gc, cu, s)
    except Exception as exc:          # a failed integration is an infeasible design
        return None, str(exc)
    return m, cyc


def violations(m, iacs_min=None):
    iacs_min = SPEC["iacs"] if iacs_min is None else iacs_min
    v = dict(
        gc_C=max(0.0, math.log(max(m["gc_C_close_ppm"], 1e-3) / SPEC["gc_C"])),
        cu_C=max(0.0, math.log(max(m["cu_C_close_ppm"], 1e-3) / SPEC["cu_C"])),
        gc_rho=max(0.0, (SPEC["gc_rho"] - m["gc_rho"]) / 0.01),
        gc_X=max(0.0, (SPEC["gc_X"] - m["gc_X"]) / 0.05),
        cu_rho=max(0.0, (SPEC["cu_rho"] - m["cu_rho"]) / 0.01),
        Pi_line=max(0.0, m["line_Pi_max"] - SPEC["Pi_line"]),
        bloat=max(0.0, m["gc_bloat"] - SPEC["bloat"]),
        melt=max(0.0, -m["cu_melt_margin"] / 5.0),
        iacs=max(0.0, (iacs_min - m["cu_iacs"]) / 2.0),
    )
    return v


OBJECTIVE = "mismatch"      # "mismatch": largest free-strain mismatch; "camber": final free camber


def objective(x, budget_h, kind=None, iacs_min=0.0):
    # everything a worker needs arrives through the arguments: workers re-import this module
    kind = kind or OBJECTIVE
    m, cyc = evaluate(x)
    if m is None or not m["ok"]:
        return 1e6
    v = violations(m, iacs_min)
    over_time = max(0.0, (m["duration_h"] - budget_h) / 1.0)
    pen = sum(v.values()) + over_time
    if kind == "camber":
        f = math.log10(abs(m["kappa_final"]) + 1e-3)
    else:
        f = math.log10(m["mismatch_max_pct"] + 1e-3)
    return f + 10.0 * pen


if __name__ == "__main__":
    out, budget = sys.argv[1], float(sys.argv[2])
    maxiter = int(sys.argv[3]) if len(sys.argv) > 3 else 25
    popsize = int(sys.argv[4]) if len(sys.argv) > 4 else 10
    if len(sys.argv) > 5:
        OBJECTIVE = sys.argv[5]
    workers = int(sys.argv[6]) if len(sys.argv) > 6 else 4
    if len(sys.argv) > 7:                 # optional minimum conductor conductivity, % IACS
        SPEC["iacs"] = float(sys.argv[7])
    t0 = time.time()
    hist = []

    def cb(xk, convergence=None):
        f = objective(xk, budget, OBJECTIVE, SPEC["iacs"])
        hist.append(dict(t=time.time() - t0, f=f, x=list(map(float, xk))))
        print(f"[{time.time()-t0:7.0f}s] f={f:.4f} conv={convergence}", flush=True)

    res = differential_evolution(objective, BOUNDS, args=(budget, OBJECTIVE, SPEC["iacs"]), maxiter=maxiter, popsize=popsize, tol=1e-3,
                                 mutation=(0.5, 1.0), recombination=0.7, seed=7, polish=False, workers=workers,
                                 updating="deferred", callback=cb, init="sobol")
    m, cyc = evaluate(res.x, N=8)
    json.dump(dict(budget_h=budget, objective=OBJECTIVE, spec=SPEC, x=list(map(float, res.x)), names=NAMES, f=float(res.fun), metrics=m,
                   violations=violations(m) if m else None, cycle=cyc.to_dict() if m else None, history=hist,
                   nfev=int(res.nfev), wall_s=time.time() - t0), open(out, "w"), indent=1)
    print(json.dumps(m, indent=1))
