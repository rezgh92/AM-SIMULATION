"""Verification: isothermal viscous densification of the glass-ceramic slab against the closed form
theta(t) = theta0 exp(-9 gamma t / (4 r eta)) (open porosity, Skorohod-Olevsky, Newtonian matrix)."""
import json, sys
import numpy as np
from cupola.cycle import Cycle, Segment
from cupola.simulate import simulate
from cupola.constants import T0C
from cupola.cofire.run import cofire_scenario, glass_view
from cupola.cofire.glass import GlassSetup

out = {"cases": []}
for T_h in (810.0, 830.0, 850.0):
    s = glass_view(cofire_scenario(char_yield=0.0, gc_Tp_cryst_C=1100.0, gc_E_cryst=700.0, pre_extracted_frac=1.0))
    cyc = Cycle([Segment(T_h, 10.0, 6.0, note="hold")])
    for N in (4, 8, 16):
        r = simulate(s, cyc, N=N, rtol=1e-6, setup_cls=GlassSetup)
        su = GlassSetup(s)
        t = r.t_h * 3600.0
        th = 1.0 - r.series["rho_mean"]
        i0 = int(np.argmax(r.series["Tset"] >= T_h - 1e-6)) 
        i0 = int(np.searchsorted(t, t[i0] + 900.0))
        eta = float(su.eta0(T_h + T0C, np.array([1e-9]))[0])
        tau = 4.0 * su.r_s * eta / (9.0 * su.gamma)
        sel = (t >= t[i0]) & (r.series["rho_mean"] < 0.88)
        # closed form along the simulated part temperature: theta = theta0 exp(-int 9 gamma / (4 r eta(T)) dt)
        Tm = 0.5 * (r.series["T_center"] + r.series["T_surface"]) + T0C
        rate = 9.0 * su.gamma / (4.0 * su.r_s * su.eta0(Tm, np.full_like(Tm, 1e-9)))
        ts, rs = t[sel], rate[sel]
        I = np.concatenate([[0.0], np.cumsum(0.5 * (rs[1:] + rs[:-1]) * np.diff(ts))])
        ref = th[i0] * np.exp(-I)
        err = float(np.max(np.abs(th[sel] - ref)))
        out["cases"].append(dict(T=T_h, N=N, tau_s=tau, t_h=(t[sel] / 3600).tolist(), theta=th[sel].tolist(),
                                 theta_ref=ref.tolist(), max_abs_err=err))
        print(T_h, N, "tau %.0f s" % tau, "max |dtheta| %.2e" % err, flush=True)
json.dump(out, open(sys.argv[1], "w"))
