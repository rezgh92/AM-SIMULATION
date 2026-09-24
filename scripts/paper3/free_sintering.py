"""Virtual dilatometry: free sintering of each material at a constant heating rate after binder
removal, and the characteristic temperatures of the co-firing 'temperature ladder'."""
import json, sys
import numpy as np
from cupola.cycle import Cycle, Segment
from cupola.simulate import simulate
from cupola.cofire.run import cofire_scenario, glass_view
from cupola.cofire.glass import GlassSetup, FilledCopperSetup


def dilatometry(s, setup_cls, rate=5.0, T_end=1060.0, N=6):
    # a debound compact (binder removed beforehand, no char): intrinsic sintering at a constant ramp in dry 4 % H2
    s = dict(s, char_yield=0.0, pre_extracted_frac=0.8, solvent_frac=0.0, w_backbone=0.0)
    s["pre_extracted_frac"] = 1.0
    cyc = Cycle([Segment(T_end, rate, 0.0, 0.0, 0.04, -60.0, "ramp")])
    r = simulate(s, cyc, N=N, rtol=1e-4, setup_cls=setup_cls)
    if not r.ok:
        print("  failed:", r.message[:100])
    S = r.series
    sel = r.t_h >= 0.0
    T = S["Tset"][sel]
    e = 100.0 * S["shrink_xy"][sel]
    rho = S["rho_mean"][sel]
    out = dict(T=T.tolist(), shrink=e.tolist(), rho=rho.tolist())
    if setup_cls is GlassSetup:
        su = GlassSetup(s)
        out["X"] = np.asarray(su.crystal_fraction(S["G_um"][sel])).tolist()
    e0 = e[0]
    tot = e[-1] - e0
    def T_at(f):
        i = np.argmax(e - e0 >= f * max(tot, 1e-9))
        return float(T[i])
    out.update(T05=T_at(0.05), T50=T_at(0.5), T95=T_at(0.95), shrink_final=float(e[-1]), rho_final=float(rho[-1]))
    return out


if __name__ == "__main__":
    base = cofire_scenario()
    res = dict(rate_Kmin=5.0, gc={}, cu={})
    res["gc"]["default"] = dilatometry(glass_view(base), GlassSetup)
    for d in (1.0, 2.0, 3.0, 6.0, 12.0, 20.0):
        for f in (0.0, 0.2, 0.4):
            key = f"d{d:g}_f{f:g}"
            res["cu"][key] = dict(d50=d, filler=f, **dilatometry(dict(base, d50_um=d, cu_filler=f), FilledCopperSetup))
            c = res["cu"][key]
            print(key, "T05 %.0f T50 %.0f T95 %.0f rho %.3f" % (c["T05"], c["T50"], c["T95"], c["rho_final"]), flush=True)
    g = res["gc"]["default"]
    print("GC T05 %.0f T50 %.0f T95 %.0f rho %.3f X_end %.2f" % (g["T05"], g["T50"], g["T95"], g["rho_final"], g["X"][-1]))
    json.dump(res, open(sys.argv[1], "w"))
