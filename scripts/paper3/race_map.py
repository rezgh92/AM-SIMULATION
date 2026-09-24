"""Carbon left in the glass-ceramic when its pores close, over the burnout hold (T_B, t_B)."""
import json, sys, time
import numpy as np
from concurrent.futures import ProcessPoolExecutor
from cupola.cofire.run import cofire_scenario, glass_view, Schedule
from cupola.cofire.glass import GlassSetup
from cupola.simulate import simulate


def one(args):
    T_B, t_B, atm, over = args
    s = glass_view(cofire_scenario(**over))
    if atm == "steam":
        sch = Schedule(T_B=T_B, t_B=t_B, x_B=0.30, s_B=0.2)
    else:   # forming gas through a room-temperature bubbler
        sch = Schedule(T_B=T_B, t_B=t_B, x_B=0.023, x_H2_B=0.04)
    cyc = sch.cycle()
    r = simulate(s, cyc, N=6, rtol=1e-3, setup_cls=GlassSetup)
    k = r.kpi
    C = k["C_at_close_ppm"] if k["closed"] else k["C_final_ppm"]
    # was the glass already closing during the hold? (closure before the end of phase B)
    tB_end = cyc.boundaries()[2][1] / 3600.0 if len(cyc.boundaries()) > 2 else np.nan
    return dict(T_B=T_B, t_B=t_B, atm=atm, C=float(C), rho=float(k["rho_final"]), t_close=float(k["t_close_h"]),
                closed_in_hold=bool(k["closed"] and k["t_close_h"] <= tB_end + 1e-6), ok=r.ok)


if __name__ == "__main__":
    TBs = np.arange(650.0, 891.0, 20.0)
    tBs = np.array([0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 16.0])
    jobs = [(float(a), float(b), atm, {}) for atm in ("steam", "fg") for a in TBs for b in tBs]
    t0 = time.time()
    with ProcessPoolExecutor(4) as ex:
        res = list(ex.map(one, jobs))
    print("runs", len(res), "wall", round(time.time() - t0), "s")
    json.dump(dict(TB=TBs.tolist(), tB=tBs.tolist(), runs=res), open(sys.argv[1], "w"))
