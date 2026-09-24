"""Consistency check against the IBM glass-ceramic/copper process (US 4,234,367 worked example):
N2 to 200 C, H2/H2O to 450 C, 2.9 K/min to T_hold, 6 h hold at H2/H2O = 1e-4, 0.5 h N2, 2.1 K/min to 960 C, 2 h.
The patent states that 785 C works, 750 C removes carbon too slowly and 830 C traps water and residue."""
import json, sys
import numpy as np
from cupola.cycle import Cycle, Segment
from cupola.simulate import simulate
from cupola.cofire.run import cofire_scenario, glass_view
from cupola.cofire.glass import GlassSetup

X_STEAM = 0.5          # steam fraction of the IBM ambient (not stated in the patent; carrier N2)


def ibm_cycle(T_hold, t_hold=6.0, x_h2o=X_STEAM):
    x_h2 = 1e-4 * x_h2o
    return Cycle([
        Segment(200.0, 2.15, 0.0, 0.0, 0.0, -60.0, "N2"),
        Segment(450.0, 2.15, 0.0, 0.0, 1e-6 * x_h2o, -60.0, "H2/H2O 1e-6", x_h2o=x_h2o),
        Segment(T_hold, 2.9, t_hold, 0.0, x_h2, -60.0, "H2/H2O 1e-4 hold", x_h2o=x_h2o),
        Segment(T_hold, 1.0, 0.5, 0.0, 0.0, -60.0, "N2 purge"),
        Segment(960.0, 2.1, 2.0, 0.0, 0.0, -60.0, "N2 sinter/crystallise"),
        Segment(25.0, 3.8, 0.0, 0.0, 0.0, -60.0, "cool"),
    ], name=f"IBM {T_hold:.0f} C")


if __name__ == "__main__":
    s = glass_view(cofire_scenario())
    su = GlassSetup(s)
    out = []
    for T in (750.0, 785.0, 830.0):
        cyc = ibm_cycle(T)
        r = simulate(s, cyc, N=8, rtol=1e-3, setup_cls=GlassSetup)
        S, k = r.series, r.kpi
        b = cyc.boundaries()
        t_end_hold = b[3][1] / 3600.0          # end of the H2/H2O hold
        i = np.searchsorted(r.t_h, t_end_hold)
        frac = S["shrink_xy"][i] / S["shrink_xy"][-1]
        X = su.crystal_fraction(S["G_um"])
        res = dict(T_hold=T, C_close=k["C_at_close_ppm"] if k["closed"] else k["C_final_ppm"],
                   t_close_h=k["t_close_h"], closed_in_hold=bool(k["closed"] and k["t_close_h"] <= t_end_hold),
                   C_end_hold=float(S["C_ppm_mean"][i]), shrink_frac_burnout=float(frac),
                   rho_final=k["rho_final"], shrink_final_pct=k["shrink_xy_pct"], X_final=float(X[-1]),
                   X_at_900=float(np.interp(900.0, S["Tset"][i:], X[i:])) if S["Tset"][-1] < 2000 else None,
                   bloat=k["Pi_bloat_max"])
        out.append(res)
        print(json.dumps({kk: (round(v, 3) if isinstance(v, float) else v) for kk, v in res.items()}))
    json.dump(dict(x_steam=X_STEAM, runs=out), open(sys.argv[1], "w"), indent=1)
