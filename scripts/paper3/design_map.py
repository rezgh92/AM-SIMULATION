"""Design maps at a fixed co-firing programme:
(1) copper paste: D50 x filler fraction -> mismatch, camber, line damage, conductivity;
(2) glass: Tg x crystallisation peak -> glass density, crystallinity, carbon at closure, camber."""
import json, sys, time
import numpy as np
from concurrent.futures import ProcessPoolExecutor
from cupola.cycle import Cycle
from cupola.cofire.run import cofire_scenario, run_pair, Schedule
from cupola.cofire.metrics import cofire_metrics


def one(args):
    over, cyc_d = args
    s = cofire_scenario(**over)
    try:
        gc, cu = run_pair(s, Cycle.from_dict(cyc_d), N=6)
        m, _ = cofire_metrics(gc, cu, s)
    except Exception as e:
        m = dict(ok=False, err=str(e))
    return dict(over=over, **m)


if __name__ == "__main__":
    out = sys.argv[1]
    sched = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
    cyc = Schedule(**sched).cycle().to_dict()
    d50s = [1.0, 1.5, 2.0, 3.0, 4.5, 6.0, 9.0, 12.0, 18.0]
    fills = [0.0, 0.1, 0.2, 0.3, 0.4]
    jobs = [(dict(d50_um=d, cu_filler=f), cyc) for d in d50s for f in fills]
    Tgs = [700.0, 730.0, 760.0, 790.0, 820.0, 850.0]
    Tps = [880.0, 920.0, 960.0, 1000.0, 1040.0]
    jobs2 = [(dict(gc_Tg_C=a, gc_Tp_cryst_C=b), cyc) for a in Tgs for b in Tps]
    t0 = time.time()
    with ProcessPoolExecutor(4) as ex:
        r1 = list(ex.map(one, jobs))
        r2 = list(ex.map(one, jobs2))
    print("wall", round(time.time() - t0), "s")
    json.dump(dict(schedule=sched, cycle=cyc, d50=d50s, filler=fills, paste=r1, Tg=Tgs, Tp=Tps, glass=r2), open(out, "w"))
