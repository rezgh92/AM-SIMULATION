"""Verification: instantaneous curvature rate of a sintering Cu / glass-ceramic bilayer plate,
3-D FEM versus the viscous Timoshenko solution (elastic-viscous correspondence)."""
import json, sys, time
import numpy as np
from cupola.cofire.run import cofire_scenario, glass_view
from cupola.cofire.glass import GlassSetup, FilledCopperSetup
from cupola.cofire.mechanics import porous_viscosities, free_strain_rate, timoshenko_factor
from cupola.fem3d.geometry import mesh_from_mask
from cupola.fem3d.cosinter import CoSinter3D
from cupola.constants import RHO_CU


def case(h, L=12.0, t_cu=0.6, t_gc=1.8, T_C=900.0, th_cu=0.30, th_gc=0.40, G_cu=1.5e-6, xi=0.05):
    s = cofire_scenario()
    su_gc, su_cu = GlassSetup(glass_view(s)), FilledCopperSetup(s)
    n = int(round(L / h)); n_cu = int(round(t_cu / h)); n_gc = int(round(t_gc / h))
    mask = np.ones((n, n, n_cu + n_gc), bool)
    mesh = mesh_from_mask(mask, h)
    zc = mesh.p[:, mesh.t].mean(axis=1)[2]
    mat = (zc > n_gc * h * 1e-3).astype(int)          # 0 = glass-ceramic (bottom), 1 = copper (top)
    T = T_C + 273.15
    s3 = CoSinter3D(mesh, mat, [su_gc, su_cu], [th_gc, th_cu], [xi * 1e-6, G_cu], [2600.0, RHO_CU], bc="free")
    v, edot = s3.solve(T, [0.0, 0.0])
    # curvature rate from the vertical velocity of the mid-plane nodes near the centre line y = L/2
    p = s3.p
    vz = s3._vel_nodes(v)[2]
    zmid = p[2].max() / 2
    sel = (np.abs(p[1] - p[1].mean()) < 0.6 * h * 1e-3) & (np.abs(p[2] - p[2][np.argmin(np.abs(p[2] - zmid))]) < 1e-9) \
          & (np.abs(p[0] - p[0].mean()) < 0.3 * L * 1e-3)
    x = p[0, sel] - p[0].mean()
    c = np.polyfit(x, vz[sel], 2)
    kdot_fem = 2.0 * c[0]       # v_z = kdot x^2 / 2 -> concave up (towards the top layer) is positive
    # analytic
    out = {}
    for name, su, th, G in (("gc", su_gc, th_gc, xi * 1e-6), ("cu", su_cu, th_cu, G_cu)):
        eta = float(su.eta0(T, np.array([G]))[0])
        PL = 3.0 * su.gamma / su.r_s * (1.0 - th) ** 2
        Gv, Kv, Ev, nuv, Bv = porous_viscosities(eta, th)
        out[name] = dict(eta=eta, rate=float(free_strain_rate(PL, eta, th)), B=float(Bv), E=float(Ev), nu=float(nuv))
    # layer 1 = copper (top), layer 2 = glass-ceramic
    d_rate = out["gc"]["rate"] - out["cu"]["rate"]
    F = timoshenko_factor(t_cu * 1e-3, t_gc * 1e-3, out["cu"]["B"], out["gc"]["B"])
    kdot_an = F * d_rate
    return dict(h=h, n_el=int(mesh.nelements), kdot_fem=kdot_fem, kdot_analytic=float(kdot_an),
                rel_err=float(kdot_fem / kdot_an - 1.0), props=out)


if __name__ == "__main__":
    res = []
    for h in (0.6, 0.3, 0.2, 0.15):
        t0 = time.time()
        r = case(h)
        r["wall_s"] = round(time.time() - t0, 1)
        print(json.dumps({k: v for k, v in r.items() if k != "props"}), flush=True)
        res.append(r)
    print(json.dumps(res[-1]["props"], indent=1))
    json.dump(res, open(sys.argv[1] if len(sys.argv) > 1 else "verify_bilayer.json", "w"), indent=1)
