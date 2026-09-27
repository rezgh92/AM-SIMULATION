"""3-D co-sintering of a printed RF package test vehicle.

Glass-ceramic block 12 x 12 x 2.4 mm (voxel 0.3 mm, the scale of a 2M30 build) with an embedded
2.5-turn square spiral inductor, a buried ground plane and a through via to a top pad. Both
materials run through the same furnace programme; temperature and carbon histories come from the
two slab simulations. Exports density fields, the deformed surface and warpage for the figures.

    python scripts/paper3/package3d.py <design.json|baseline> <out.json> [voxel_mm]
"""
import json, sys, time
import numpy as np
from skfem import MeshHex

from cupola.constants import RHO_CU, T0C
from cupola.cycle import Cycle
from cupola.cofire.run import cofire_scenario, glass_view, run_pair, Schedule
from cupola.cofire.glass import GlassSetup, FilledCopperSetup
from cupola.fem3d.geometry import mesh_from_mask
from cupola.fem3d.cosinter import CoSinter3D
from cupola.fem3d.driver import surface, node_density


def package_mask(h=0.25, L=10.0, H=2.5):
    """Voxel layout of the printed RF system-in-package test vehicle: -1 void, 0 glass-ceramic, 1 copper.

    Glass-ceramic body L x L x H mm with an open 4 x 4 mm die cavity, 0.75 mm deep, in the top centre.
    Copper, all printed in the same build:
      - die-attach pad on the cavity floor (3 x 3 mm) with a 3 x 3 array of thermal vias (0.5 mm square)
        down to the ground plane;
      - ground plane in the second layer: solid under the die, meshed elsewhere (0.5 mm lines at 1.25 mm
        pitch, the usual rule for large planes in co-fired ceramics);
      - a four-turn solenoid inductor wound about an axis parallel to the surface (0.5 mm wire, 1 mm
        tall, 1 mm pitch) beside the cavity: a three-dimensional conductor that laminated tape cannot
        build without stacks of vias;
      - a buried stripline from the cavity wall to the edge, shielded by two rows of via fences, and a
        via to a 1 mm bond pad on the top face.
    """
    n = int(round(L / h))
    nz = int(round(H / h))
    mat = np.zeros((n, n, nz), dtype=int)
    c = (np.arange(n) + 0.5) * h - L / 2
    X, Y = np.meshgrid(c, c, indexing="ij")
    zc = (np.arange(nz) + 0.5) * h
    lay = lambda z: int(np.clip(np.floor(z / h), 0, nz - 1))
    tol = 1e-9

    def box(x0, x1, y0, y1, k0, k1, v=1):
        sel = (X >= x0 - tol) & (X <= x1 + tol) & (Y >= y0 - tol) & (Y <= y1 + tol)
        for k in range(k0, k1 + 1):
            mat[:, :, k][sel] = v

    k_gnd = lay(0.25 + 0.5 * h)                 # second layer from the bottom
    k_floor = lay(H - 0.75 - 0.5 * h)           # cavity floor layer (top of it at H - 0.75 mm)
    k_line = lay(1.0 + 0.5 * h)                 # stripline layer
    # ground plane: meshed, solid under the die
    mesh = np.zeros_like(X, bool)
    for xc in np.arange(-3.75, 3.76, 1.25):
        mesh |= (np.abs(X - xc) <= 0.25 + tol) & (np.abs(Y) <= 4.0 + tol)
        mesh |= (np.abs(Y - xc) <= 0.25 + tol) & (np.abs(X) <= 4.0 + tol)
    mesh |= (np.abs(X) <= 1.5 + tol) & (np.abs(Y) <= 1.5 + tol)
    mat[:, :, k_gnd][mesh] = 1
    # die-attach pad and thermal vias
    box(-1.5, 1.5, -1.5, 1.5, k_floor, k_floor)
    for xv in (-1.0, 0.0, 1.0):
        for yv in (-1.0, 0.0, 1.0):
            box(xv - 0.25, xv + 0.25, yv - 0.25, yv + 0.25, k_gnd, k_floor)
    # solenoid beside the cavity (x in [-4.25, -2.75]), axis along y
    kb, kt = lay(0.75 + 0.5 * h), lay(1.5 + 0.5 * h)
    xl, xr, w, pitch = -4.25, -2.75, 0.5, 1.0
    for i in range(4):
        y0 = -2.0 + i * pitch
        box(xl - w / 2, xl + w / 2, y0 - w / 2, y0 + w / 2, kb, kt)                    # left post
        box(xl - w / 2, xr + w / 2, y0 - w / 2, y0 + w / 2, kt, kt)                    # top bar
        box(xr - w / 2, xr + w / 2, y0 - w / 2, y0 + pitch / 2 + w / 2, kt, kt)        # jog along the axis
        box(xr - w / 2, xr + w / 2, y0 + pitch / 2 - w / 2, y0 + pitch / 2 + w / 2, kb, kt)   # right post
        box(xl - w / 2, xr + w / 2, y0 + pitch / 2 - w / 2, y0 + pitch / 2 + w / 2, kb, kb)   # bottom bar
        if i < 3:
            box(xl - w / 2, xl + w / 2, y0 + pitch / 2 - w / 2, y0 + pitch + w / 2, kb, kb)   # jog to next turn
    # shielded stripline from the cavity wall to a via and top bond pad
    box(2.25, 4.25, -0.25, 0.25, k_line, k_line)
    for xv in (2.75, 3.5, 4.25):
        for yv in (-1.25, 1.25):
            box(xv - 0.25, xv + 0.25, yv - 0.25, yv + 0.25, k_gnd, nz - 2)
    box(3.75, 4.25, -0.25, 0.25, k_line, nz - 1)
    box(3.5, 4.5, -0.5, 0.5, nz - 1, nz - 1)
    # open die cavity
    box(-2.0, 2.0, -2.0, 2.0, k_floor + 1, nz - 1, v=-1)
    return mat


def build(h):
    mat3 = package_mask(h)
    mesh = mesh_from_mask(mat3 >= 0, h)
    cen = mesh.p[:, mesh.t].mean(axis=1) / (h * 1e-3)
    ix, iy, iz = (np.floor(cen[i]).astype(int) for i in range(3))
    return mesh, mat3[ix, iy, iz]


def histories(r_gc, r_cu):
    t = r_gc.t_h * 3600.0
    T = 0.5 * (r_gc.series["T_center"] + r_gc.series["T_surface"]) + T0C
    C_gc = r_gc.series["C_ppm_mean"]
    C_cu = np.interp(t, r_cu.t_h * 3600.0, r_cu.series["C_ppm_mean"])
    return t, T, C_gc, C_cu


if __name__ == "__main__":
    spec, out = sys.argv[1], sys.argv[2]
    h = float(sys.argv[3]) if len(sys.argv) > 3 else 0.25
    if spec == "baseline":
        over = dict(d50_um=3.0, cu_filler=0.0, phi=0.50)
        cyc = Schedule(T_B=780.0, t_B=4.0, x_B=0.30, T_C=960.0, t_C=1.0).cycle()
        label = "baseline"
    else:
        d = json.load(open(spec))
        over = dict(d50_um=10 ** d["x"][0], cu_filler=d["x"][1], phi=d["x"][2])
        cyc = Cycle.from_dict(d["cycle"])
        label = "robust" if "robust" in spec else "optimised"
    s = cofire_scenario(**over)
    r_gc, r_cu = run_pair(s, cyc, N=8)
    t, T, C_gc, C_cu = histories(r_gc, r_cu)
    # start once both binders are gone and the copper can begin to neck
    bl = np.maximum(r_gc.series["binder_left"], np.interp(t, r_cu.t_h * 3600, r_cu.series["binder_left"]))
    i0 = int(np.argmax((bl < 1e-3) & (T - T0C > 400.0)))
    th_gc = 1.0 - float(r_gc.series["rho_mean"][i0])
    th_cu = 1.0 - float(np.interp(t[i0], r_cu.t_h * 3600, r_cu.series["rho_m_mean"]))
    G_cu = float(np.interp(t[i0], r_cu.t_h * 3600, r_cu.series["G_um"])) * 1e-6
    xi_gc = float(r_gc.series["G_um"][i0]) * 1e-6
    mesh, mat = build(h)
    su_gc, su_cu = GlassSetup(glass_view(s)), FilledCopperSetup(s)
    rho_gc_solid = s.get("gc_rho", 2600.0)
    s3 = CoSinter3D(mesh, mat, [su_gc, su_cu], [th_gc, th_cu], [xi_gc, G_cu], [rho_gc_solid, RHO_CU],
                    mu_f=0.6, gravity=True, bc="setter")
    tt = t[i0:] - t[i0]
    t_wall = time.time()
    last = [0.0]

    def prog(tc, Tc, obj):
        if time.time() - last[0] > 30:
            last[0] = time.time()
            print(f"  t={tc/3600:6.2f} h T={Tc-T0C:6.0f} C  rho_gc={np.mean(1-obj.theta[mat==0]):.3f} "
                  f"rho_cu={np.mean(1-obj.theta[mat==1]):.3f} ({time.time()-t_wall:.0f} s)", flush=True)

    # stop once the glass-ceramic is 98 % dense or 90 % crystallised: the remaining linear shrinkage of the
    # body is then a few tenths of a per cent and its shape is essentially frozen
    X_gc = np.asarray(su_gc.crystal_fraction(r_gc.series["G_um"]))
    done = (X_gc >= 0.9) | (r_gc.series["rho_mean"] >= 0.98)
    i_x = int(np.argmax(done)) if np.any(done) else len(t) - 1
    t_stop = float(t[max(i_x, i0 + 1)] - t[i0])
    frames = s3.run(tt, T[i0:], [C_gc[i0:], C_cu[i0:]], n_frames=30, progress=prog, t_stop=t_stop)
    # export
    m0 = MeshHex(s3.p0, s3.t_conn)
    verts, tris, _ = surface(m0)
    fr = []
    for f in frames:
        mf = MeshHex(f.p, s3.t_conn)
        fr.append(dict(t_h=f.t_h, T_C=f.T_C, rho_gc=float(np.mean(1 - f.theta[mat == 0])),
                       rho_cu=float(np.mean(1 - f.theta[mat == 1]))))
    pF = s3.p
    bottom = np.isclose(s3.p0[2], s3.p0[2].min())
    top = np.isclose(s3.p0[2], s3.p0[2].max())
    res = dict(label=label, h_mm=h, design=over, cycle=cyc.to_dict(), wall_s=time.time() - t_wall,
               t_stop_h=float((t[i0] + t_stop) / 3600), T_stop_C=float(np.interp(t[i0] + t_stop, t, T) - T0C),
               n_el=int(mesh.nelements), mat=mat.tolist(), t_start_h=float(t[i0] / 3600),
               p0=s3.p0.T.tolist(), p=pF.T.tolist(), t_conn=s3.t_conn.T.tolist(),
               theta=s3.theta.tolist(), frames=fr,
               bow_bottom_um=float((pF[2][bottom].max() - pF[2][bottom].min()) * 1e6),
               bow_top_um=float((pF[2][top].max() - pF[2][top].min()) * 1e6),
               shrink_xy_pct=float(100 * (1 - np.ptp(pF[0]) / np.ptp(s3.p0[0]))),
               shrink_z_pct=float(100 * (1 - np.ptp(pF[2]) / np.ptp(s3.p0[2]))))
    json.dump(res, open(out, "w"))
    print(json.dumps({k: v for k, v in res.items() if k in ("label", "n_el", "wall_s", "bow_bottom_um", "bow_top_um",
                                                             "shrink_xy_pct", "shrink_z_pct")}, indent=1))
