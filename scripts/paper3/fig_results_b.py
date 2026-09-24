"""Figures 6-8 and 10: copper-paste design maps, optimised programme, 3-D test vehicle, sensitivity."""
import json, sys, os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.colors import Normalize, LogNorm
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import figstyle as fs

D, O = sys.argv[1], sys.argv[2]
which = sys.argv[3:] or ["design", "programme", "package", "sens"]
fs.apply()


# ----------------------------------------------------------------------------- design maps
def fig_design():
    d = json.load(open(f"{D}/design_map.json"))
    d50 = np.array(d["d50"]); fl = np.array(d["filler"])
    Tg = np.array(d["Tg"]); Tp = np.array(d["Tp"])

    def grid(key, src="paste", xs=None, ys=None, kx="d50_um", ky="cu_filler"):
        xs = d50 if xs is None else xs; ys = fl if ys is None else ys
        Z = np.full((len(ys), len(xs)), np.nan)
        for r in d[src]:
            if not r.get("ok", False):
                continue
            i = int(np.argmin(abs(ys - r["over"][ky]))); j = int(np.argmin(abs(xs - r["over"][kx])))
            Z[i, j] = r[key]
        return Z

    def tf(Z, mode):
        if mode == "log":
            return np.log10(np.maximum(Z, 1e-3))
        return Z

    fig, axs = plt.subplots(2, 4, figsize=(fs.COL2, 0.62 * fs.COL2),
                            gridspec_kw=dict(wspace=0.16, hspace=0.78))
    # row 1: copper paste at the baseline programme
    specs = [("mismatch_max_pct", "Peak free-strain mismatch (%)", fs.SEQ_BLUE, None),
             ("line_Pi_max", "Line damage index Π (log$_{10}$)", fs.SEQ_BLUE, "log"),
             ("cu_rho", "Copper relative density", fs.SEQ_COPPER, None),
             ("cu_iacs", "Copper conductivity (% IACS)", fs.SEQ_COPPER, None)]
    X, Y = np.meshgrid(np.log10(d50), fl * 100)
    rho = grid("cu_rho")
    for k, (key, lab, cmap, mode) in enumerate(specs):
        ax = axs[0, k]
        Z = tf(grid(key), mode)
        pc = ax.pcolormesh(X, Y, Z, cmap=cmap, shading="nearest")
        if key == "line_Pi_max":
            ax.contour(X, Y, Z, levels=[0.0], colors=[fs.ORANGE], linewidths=1.3)
        cs = ax.contour(X, Y, rho, levels=[0.92], colors=[fs.INK], linewidths=0.9, linestyles="--")
        ax.plot(np.log10(3.0), 0.0, marker="o", ms=4.5, mfc="white", mec=fs.INK, mew=0.9, clip_on=False, zorder=6)
        cb = fig.colorbar(pc, ax=ax, orientation="horizontal", pad=0.30, fraction=0.07, aspect=16)
        cb.ax.tick_params(labelsize=5.8); cb.set_label(lab, fontsize=6.2)
        ax.set_xticks(np.log10([1, 2, 3, 6, 12, 18])); ax.set_xticklabels(["1", "2", "3", "6", "12", "18"])
        ax.set_xlabel("Cu D50 (µm)")
        if k:
            ax.set_yticklabels([])
        fs.panel(ax, "abcd"[k], x=-0.04, y=1.05)
    axs[0, 0].set_ylabel("Filler in Cu paste (vol%)")
    # row 2: glass (T_g x crystallisation peak) with the baseline paste and programme
    gspecs = [("gc_C_close_ppm", "C at glass pore closure (ppm, log$_{10}$)", fs.SEQ_BLUE, "log"),
              ("gc_rho", "Glass-ceramic relative density", fs.SEQ_BLUE, None),
              ("gc_X", "Crystallised fraction", fs.SEQ_BLUE, None),
              ("mismatch_max_pct", "Peak free-strain mismatch (%)", fs.SEQ_BLUE, None)]
    XG, YG = np.meshgrid(Tg, Tp)
    for k, (key, lab, cmap, mode) in enumerate(gspecs):
        ax = axs[1, k]
        Z = tf(grid(key, "glass", Tg, Tp, "gc_Tg_C", "gc_Tp_cryst_C"), mode)
        pc = ax.pcolormesh(XG, YG, Z, cmap=cmap, shading="nearest")
        if key == "gc_C_close_ppm":
            ax.contour(XG, YG, Z, levels=[2.0], colors=[fs.ORANGE], linewidths=1.3)
        if key == "gc_rho":
            ax.contour(XG, YG, Z, levels=[0.97], colors=[fs.ORANGE], linewidths=1.3)
        if key == "gc_X":
            ax.contour(XG, YG, Z, levels=[0.8], colors=[fs.ORANGE], linewidths=1.3)
        ax.plot(734.0, 1040.0, marker="D", ms=4.2, mfc="white", mec=fs.INK, mew=0.9, clip_on=False, zorder=6)
        cb = fig.colorbar(pc, ax=ax, orientation="horizontal", pad=0.30, fraction=0.07, aspect=16)
        cb.ax.tick_params(labelsize=5.8); cb.set_label(lab, fontsize=6.2)
        ax.set_xlabel("Glass T$_g$ (°C)")
        if k:
            ax.set_yticklabels([])
        fs.panel(ax, "efgh"[k], x=-0.04, y=1.05)
    axs[1, 0].set_ylabel("Crystallisation peak (°C)")
    fs.save(fig, "fig06_design", O)


# ----------------------------------------------------------------------------- optimised programme
def run_series(opt_path, label):
    from cupola.cycle import Cycle
    from cupola.cofire.run import cofire_scenario, run_pair
    from cupola.cofire.metrics import cofire_metrics
    o = json.load(open(opt_path))
    over = dict(d50_um=10 ** o["x"][0], cu_filler=o["x"][1], phi=o["x"][2])
    s = cofire_scenario(**over)
    cyc = Cycle.from_dict(o["cycle"])
    gc, cu = run_pair(s, cyc, N=8)
    m, ser = cofire_metrics(gc, cu, s)
    return dict(label=label, m=m, ser=ser, gc=gc, cu=cu, cyc=cyc)


def fig_programme():
    from cupola.cofire.run import cofire_scenario, run_pair, Schedule
    from cupola.cofire.metrics import cofire_metrics
    runs = []
    s0 = cofire_scenario(d50_um=3.0, cu_filler=0.0, phi=0.50)
    base = Schedule(T_B=780.0, t_B=4.0, x_B=0.30, T_C=960.0, t_C=1.0).cycle()
    gc, cu = run_pair(s0, base, N=8)
    m, ser = cofire_metrics(gc, cu, s0)
    runs.append(dict(label="baseline", m=m, ser=ser, gc=gc, cu=cu, cyc=base))
    runs.append(run_series(f"{D}/opt_main.json", "optimised"))
    runs.append(run_series(f"{D}/opt_robust.json", "robust"))
    fig, axs = plt.subplots(5, 3, figsize=(fs.COL2, 1.0 * fs.COL2), sharex="col", sharey="row",
                            gridspec_kw=dict(hspace=0.14, wspace=0.08, height_ratios=[1.15, 1, 1, 0.85, 0.7]))
    atm_col = {"A": "#D2DAE0", "B": "#BFE6D6", "C": "#C8DBF3", "D": "#E6E9EC"}
    xo = dict(zip(*[json.load(open(f"{D}/opt_main.json"))[k] for k in ("names", "x")]))
    xr = dict(zip(*[json.load(open(f"{D}/opt_robust.json"))[k] for k in ("names", "x")]))
    titles = ["(a) baseline\n3 µm Cu; burnout 780 °C, 4 h; peak 960 °C",
              f"(b) nominal optimum\n{10 ** xo['log10_d50']:.1f} µm Cu + {100 * xo['filler']:.0f} % filler; "
              f"burnout {xo['T_B']:.0f} °C, {10 ** xo['log10_tB']:.1f} h",
              f"(c) robust design\n{10 ** xr['log10_d50']:.1f} µm Cu + {100 * xr['filler']:.0f} % filler; "
              f"burnout {xr['T_B']:.0f} °C, {10 ** xr['log10_tB']:.1f} h"]
    for c, r in enumerate(runs):
        S, gc, cu, cyc = r["ser"], r["gc"], r["cu"], r["cyc"]
        t = S["t_h"]
        ax = axs[0, c]
        for (t0, t1, seg, Tf, kind) in cyc.boundaries():
            ax.axvspan(t0 / 3600, t1 / 3600, ymin=0, ymax=0.06, color=atm_col.get(seg.note[:1], "#EEE"), lw=0)
        ax.plot(gc.t_h, gc.series["Tset"], color=fs.INK2, lw=1.0, ls="--", label="set point")
        ax.plot(t, S["T_C"], color=fs.INK, lw=1.3, label="part")
        ax.set_ylim(0, 1100)
        ax.set_ylabel("T (°C)")
        ax.set_title(titles[c], fontsize=6.4, loc="left", linespacing=1.25)
        ax = axs[1, c]
        ax.plot(t, S["rho_gc"], color=fs.GC, lw=1.4, label="glass-ceramic")
        ax.plot(t, S["rho_cu"], color=fs.CU, lw=1.4, label="copper")
        ax.plot(t, S["X_gc"], color=fs.GC, lw=1.0, ls=":", label="crystallised fraction")
        ax.set_ylabel("ρ, X$_c$")
        ax.set_ylim(0, 1.02)
        ax = axs[2, c]
        ax.plot(t, 100 * S["eps_cu"], color=fs.CU, lw=1.4, label="copper")
        ax.plot(t, 100 * S["eps_gc"], color=fs.GC, lw=1.4, label="glass-ceramic")
        ax.fill_between(t, 100 * S["eps_cu"], 100 * S["eps_gc"], color=fs.ORANGE, alpha=0.15, lw=0,
                        label="mismatch")
        ax.set_ylabel("Free strain (%)")
        ax = axs[3, c]
        ax.plot(t, np.log10(np.maximum(S["C_gc"], 0.1)), color=fs.GC, lw=1.3, label="glass-ceramic")
        ax.plot(t, np.log10(np.maximum(S["C_cu"], 0.1)), color=fs.CU, lw=1.1, label="copper")
        ax.axhline(2.0, color=fs.MUTED, lw=0.7, ls="--")
        ax.set_ylabel("log$_{10}$ C (ppm)")
        ax.set_ylim(-1.2, 4.8)
        ax = axs[4, c]
        ax.plot(t, S["Pi_line"], color=fs.ORANGE, lw=1.2)
        ax.axhline(1.0, color=fs.CRIT, lw=0.7, ls="--")
        ax.set_ylabel("Π$_{line}$")
        ax.set_ylim(0, 1.9)
        ax.set_xlabel("Time (h)")
    for ax in axs[:, 0]:
        ax.yaxis.set_label_coords(-0.16, 0.5)
    for ax in axs[:, 1:].ravel():
        ax.set_ylabel("")
    axs[0, 0].legend(loc="upper left", fontsize=6)
    axs[1, 0].legend(loc="upper left", fontsize=6)
    axs[2, 0].legend(loc="lower left", fontsize=6)
    axs[3, 2].legend(loc="center right", fontsize=5.8, ncol=1, handlelength=1.2)
    axs[3, 0].text(0.99, 2.12, "100 ppm", transform=axs[3, 0].get_yaxis_transform(), ha="right", va="bottom",
                   fontsize=5.8, color=fs.MUTED)
    axs[4, 0].text(0.99, 1.05, "Π = 1", transform=axs[4, 0].get_yaxis_transform(), ha="right", va="bottom",
                   fontsize=5.8, color=fs.CRIT)
    fs.save(fig, "fig07_programme", O)
    json.dump({r["label"]: r["m"] for r in runs}, open(f"{D}/programme_metrics.json", "w"), indent=1)
    keep = ("t_h", "T_C", "eps_gc", "eps_cu", "rho_gc", "rho_cu", "X_gc", "C_gc", "C_cu", "Pi_line", "kappa")
    json.dump({r["label"]: {k: np.asarray(r["ser"][k]).tolist() for k in keep} for r in runs},
              open(f"{D}/programme_series.json", "w"))


# ----------------------------------------------------------------------------- 3-D test vehicle
def draw_body(ax, p, conn, theta, mat, view, title, zscale=1.0, cmap_gc=fs.SEQ_BLUE, cmap_cu=fs.SEQ_COPPER):
    p = np.asarray(p) * 1e3
    conn = np.asarray(conn)
    # boundary faces of the hex mesh: faces shared by one element only
    faces = [(0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    # skfem MeshHex local node ordering differs; use sorted-node keys to count sharing
    from collections import Counter
    keys = []
    for e, el in enumerate(conn):
        for f in faces:
            keys.append((tuple(sorted(el[list(f)])), e, f))
    cnt = Counter(k for k, _, _ in keys)
    polys, cols = [], []
    for k, e, f in keys:
        if cnt[k] == 1:
            polys.append(p[conn[e][list(f)]])
            rho = 1 - theta[e]
            cols.append(cmap_cu(np.clip((rho - 0.5) / 0.5, 0, 1)) if mat[e] == 1 else cmap_gc(np.clip((rho - 0.4) / 0.6, 0, 1) * 0.55 + 0.05))
    pc = Poly3DCollection(polys, facecolors=cols, edgecolors=(0, 0, 0, 0.08), linewidths=0.1)
    ax.add_collection3d(pc)
    ax.set_xlim(p[:, 0].min(), p[:, 0].max()); ax.set_ylim(p[:, 1].min(), p[:, 1].max()); ax.set_zlim(p[:, 2].min(), p[:, 2].max())
    ax.set_box_aspect((np.ptp(p[:, 0]), np.ptp(p[:, 1]), np.ptp(p[:, 2]) * zscale))
    ax.view_init(*view)
    ax.set_axis_off()
    ax.set_title(title, fontsize=6.8, pad=0)


def top_relief(r):
    """Height of the top surface relative to its mean (µm) on the node grid, and the grid in mm."""
    p0 = np.array(r["p0"]); p = np.array(r["p"])
    top = np.isclose(p0[:, 2], p0[:, 2].max())
    x0, y0 = p0[top, 0], p0[top, 1]
    xs, ys = np.unique(np.round(x0, 9)), np.unique(np.round(y0, 9))
    Z = np.full((len(ys), len(xs)), np.nan)
    ix = np.searchsorted(xs, np.round(x0, 9)); iy = np.searchsorted(ys, np.round(y0, 9))
    Z[iy, ix] = p[top, 2]
    Z = (Z - np.nanmean(Z)) * 1e6
    X = np.zeros_like(Z); Y = np.zeros_like(Z)
    X[iy, ix] = p[top, 0] * 1e3; Y[iy, ix] = p[top, 1] * 1e3
    return X - np.nanmean(X), Y - np.nanmean(Y), Z


def fig_package():
    names = {"baseline": "baseline", "optimised": "nominal optimum", "robust": "robust design"}
    runs = [json.load(open(f"{D}/package_{k}.json")) for k in names if os.path.exists(f"{D}/package_{k}.json")]
    nr = len(runs)
    fig = plt.figure(figsize=(fs.COL2, 0.27 * nr * fs.COL2))
    L = "abcdefghi"
    reliefs = [top_relief(r) for r in runs]
    lim = max(np.nanmax(np.abs(z)) for _, _, z in reliefs)
    for k, r in enumerate(runs):
        mat = np.array(r["mat"]); theta = np.array(r["theta"]); conn = np.array(r["t_conn"]); p = np.array(r["p"])
        cen = p[conn].mean(axis=1)
        keep = cen[:, 1] >= np.median(cen[:, 1])          # cut-away facing the viewer: buried copper visible
        ax = fig.add_subplot(nr, 3, 3 * k + 1, projection="3d")
        draw_body(ax, p, conn[keep], theta[keep], mat[keep], (24, -60),
                  f"({L[3 * k]}) {names[r['label']]}: sectioned part", zscale=2.0)
        ax = fig.add_subplot(nr, 3, 3 * k + 2, projection="3d")
        cu = mat == 1
        rho_cu = 1 - theta[cu]
        draw_body(ax, p, conn[cu], theta[cu], mat[cu], (32, -60),
                  f"({L[3 * k + 1]}) copper, mean ρ = {rho_cu.mean():.3f}", zscale=2.0)
        ax = fig.add_subplot(nr, 3, 3 * k + 3)
        X, Y, Z = reliefs[k]
        pc = ax.pcolormesh(X, Y, Z, cmap=fs.DIVERGE, vmin=-lim, vmax=lim, shading="gouraud")
        ax.set_aspect("equal")
        ax.set_xlabel("x (mm)"); ax.set_ylabel("y (mm)")
        ax.set_title(f"({L[3 * k + 2]}) top surface, range {np.nanmax(Z) - np.nanmin(Z):.0f} µm", fontsize=6.6, loc="left")
        cb = fig.colorbar(pc, ax=ax, fraction=0.046, pad=0.03)
        cb.set_label("height − mean (µm)", fontsize=6.2); cb.ax.tick_params(labelsize=5.8)
    fs.save(fig, "fig08_package", O)


# ----------------------------------------------------------------------------- sensitivity
LABELS = {"gc_Tg_C": "glass T$_g$", "gc_fragility": "glass fragility m", "gc_Tp_cryst_C": "crystallisation peak",
          "gc_E_cryst": "crystallisation E", "gc_n_avrami": "Avrami n", "gc_gamma": "glass surface energy",
          "gc_d50_um": "glass D50", "gc_phi": "glass solids loading", "t_half_gasif_h": "char gasification half-life",
          "E_gasif": "gasification E", "char_yield": "char yield", "f_eta": "Cu viscosity factor f$_η$",
          "d50_um": "Cu D50 tolerance", "cu_filler": "filler tolerance"}


def fig_sens():
    d = json.load(open(f"{D}/morris.json"))
    outs = [("log10_gc_C", "log$_{10}$ C at closure"), ("gc_rho", "Glass-ceramic density"),
            ("cu_rho", "Copper density"), ("mismatch_max_pct", "Peak mismatch"), ("line_Pi_max", "Line damage index")]
    fig, axs = plt.subplots(1, len(outs), figsize=(fs.COL2, 0.42 * fs.COL2), sharey=True, gridspec_kw=dict(wspace=0.1))
    keys = [f["key"] for f in d["factors"]]
    # order factors by their summed normalised importance
    tot = np.zeros(len(keys))
    for o, _ in outs:
        mu = np.array([x["mu_star"] for x in d["result"][o]])
        tot += mu / max(np.nanmax(mu), 1e-12)
    order = np.argsort(tot)
    y = np.arange(len(keys))
    for k, (ax, (o, lab)) in enumerate(zip(axs, outs)):
        mu = np.array([x["mu_star"] for x in d["result"][o]])[order]
        sg = np.array([x["sigma"] for x in d["result"][o]])[order]
        mx = max(np.nanmax(mu), 1e-12)
        ax.barh(y, mu / mx, color=fs.BLUE, height=0.62)
        ax.plot(sg / mx, y, "o", ms=2.6, color=fs.ORANGE)
        ax.set_title(f"({'abcde'[k]}) {lab}", fontsize=6.6, loc="left")
        ax.set_xlim(0, 1.25)
        ax.set_xticks([0, 0.5, 1.0])
    axs[0].set_yticks(y); axs[0].set_yticklabels([LABELS.get(keys[i], keys[i]) for i in order], fontsize=6.2)
    fig.text(0.56, -0.02, "Normalised mean absolute elementary effect μ* (bars) and standard deviation σ (dots)",
             ha="center", fontsize=6.6, color=fs.INK)
    fs.save(fig, "fig10_sensitivity", O)


if __name__ == "__main__":
    for w in which:
        {"design": fig_design, "programme": fig_programme, "package": fig_package, "sens": fig_sens}[w]()
