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
    fig, axs = plt.subplots(4, 2, figsize=(fs.COL2, 0.95 * fs.COL2), sharex="col",
                            gridspec_kw=dict(hspace=0.16, wspace=0.26, height_ratios=[1.2, 1, 1, 1]))
    atm_col = {"A": "#D2DAE0", "B": "#BFE6D6", "C": "#C8DBF3", "D": "#E6E9EC"}
    for c, r in enumerate(runs):
        S, gc, cu, cyc = r["ser"], r["gc"], r["cu"], r["cyc"]
        t = S["t_h"]
        ax = axs[0, c]
        # atmosphere band from the programme segments
        for (t0, t1, seg, Tf, kind) in cyc.boundaries():
            ax.axvspan(t0 / 3600, t1 / 3600, ymin=0, ymax=0.06, color=atm_col.get(seg.note[:1], "#EEE"), lw=0)
        ax.plot(gc.t_h, gc.series["Tset"], color=fs.INK2, lw=1.0, ls="--", label="set point")
        ax.plot(t, S["T_C"], color=fs.INK, lw=1.3, label="part")
        ax.set_ylim(0, 1100)
        ax.set_ylabel("T (°C)")
        ax.set_title(("(a) baseline: 3 µm Cu, 780 °C steam, 960 °C" if c == 0 else
                      "(b) optimised programme and paste"), fontsize=7, loc="left")
        ax = axs[1, c]
        ax.plot(t, S["rho_gc"], color=fs.GC, lw=1.4, label="glass-ceramic")
        ax.plot(t, S["rho_cu"], color=fs.CU, lw=1.4, label="copper")
        ax.plot(t, S["X_gc"], color=fs.GC, lw=1.0, ls=":", label="crystallised fraction")
        ax.set_ylabel("ρ, X$_c$")
        ax.set_ylim(0, 1.02)
        ax = axs[2, c]
        ax.plot(t, 100 * S["eps_cu"], color=fs.CU, lw=1.4, label="copper")
        ax.plot(t, 100 * S["eps_gc"], color=fs.GC, lw=1.4, label="glass-ceramic")
        ax.fill_between(t, 100 * S["eps_cu"], 100 * S["eps_gc"], color=fs.ORANGE, alpha=0.15, lw=0)
        ax.set_ylabel("Free strain (%)")
        ax = axs[3, c]
        ax.plot(t, np.log10(np.maximum(S["C_gc"], 0.1)), color=fs.GC, lw=1.3, label="C in glass-ceramic")
        ax.plot(t, S["Pi_line"] * 1.0, color=fs.ORANGE, lw=1.1, label="line damage index Π")
        ax.axhline(1.0, color=fs.CRIT, lw=0.7, ls="--")
        ax.set_ylabel("log$_{10}$C (ppm) / Π")
        ax.set_xlabel("Time (h)")
        ax.set_ylim(-1, 4.6)
    for ax in axs[:, 0]:
        ax.yaxis.set_label_coords(-0.1, 0.5)
    axs[0, 1].legend(loc="upper right", fontsize=6)
    axs[1, 1].legend(loc="center right", fontsize=6)
    axs[2, 1].legend(loc="upper right", fontsize=6)
    axs[3, 1].legend(loc="upper right", fontsize=6)
    fs.save(fig, "fig07_programme", O)
    json.dump({r["label"]: r["m"] for r in runs}, open(f"{D}/programme_metrics.json", "w"), indent=1)
    keep = ("t_h", "T_C", "eps_gc", "eps_cu", "rho_gc", "rho_cu", "X_gc", "C_gc", "Pi_line", "kappa")
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


def fig_package():
    runs = [json.load(open(f"{D}/package_{k}.json")) for k in ("baseline", "optimised") if os.path.exists(f"{D}/package_{k}.json")]
    fig = plt.figure(figsize=(fs.COL2, 0.52 * fs.COL2))
    for k, r in enumerate(runs):
        mat = np.array(r["mat"]); theta = np.array(r["theta"]); conn = np.array(r["t_conn"]); p = np.array(r["p"])
        # cut-away: keep elements with y below the centre so the buried copper is visible
        cen = p[conn].mean(axis=1)
        keep = cen[:, 1] <= np.median(cen[:, 1])
        ax = fig.add_subplot(2, 3, 3 * k + 1, projection="3d")
        draw_body(ax, p, conn[keep], theta[keep], mat[keep], (24, -60),
                  f"{'(a)' if k == 0 else '(d)'} {r['label']}: sectioned part", zscale=2.0)
        # copper only
        ax = fig.add_subplot(2, 3, 3 * k + 2, projection="3d")
        cu = mat == 1
        draw_body(ax, p, conn[cu], theta[cu], mat[cu], (32, -60), f"{'(b)' if k == 0 else '(e)'} copper density", zscale=2.0)
        # bottom-surface profile (warpage), magnified
        ax = fig.add_subplot(2, 3, 3 * k + 3)
        p0 = np.array(r["p0"]) * 1e3
        bot = np.isclose(p0[:, 2], p0[:, 2].min())
        yc = np.isclose(p0[:, 1], p0[bot, 1][np.argmin(abs(p0[bot, 1] - np.median(p0[bot, 1])))])
        sel = bot & yc
        x = p[sel, 0]; z = p[sel, 2]
        o = np.argsort(x)
        ax.plot(x[o] - x.mean(), (z[o] - z.min()) * 1e3, color=fs.INK, lw=1.3)
        ax.set_xlabel("x (mm)"); ax.set_ylabel("bottom surface lift (µm)")
        ax.set_title(f"{'(c)' if k == 0 else '(f)'} bow {r['bow_bottom_um']:.0f} µm, shrink {r['shrink_xy_pct']:.1f} %", fontsize=6.8, loc="left")
    fs.save(fig, "fig08_package", O)


# ----------------------------------------------------------------------------- sensitivity
LABELS = {"gc_Tg_C": "glass T$_g$", "gc_fragility": "glass fragility m", "gc_Tp_cryst_C": "crystallisation peak",
          "gc_E_cryst": "crystallisation E", "gc_n_avrami": "Avrami n", "gc_gamma": "glass surface energy",
          "gc_d50_um": "glass D50", "gc_phi": "glass solids loading", "t_half_gasif_h": "char gasification half-life",
          "E_gasif": "gasification E", "char_yield": "char yield", "f_eta": "Cu viscosity factor f$_η$",
          "d50_um": "Cu D50", "cu_filler": "filler fraction"}


def fig_sens():
    d = json.load(open(f"{D}/morris.json"))
    outs = [("log10_gc_C", "log$_{10}$ C at glass closure"), ("gc_rho", "Glass-ceramic density"),
            ("cu_rho", "Copper density"), ("mismatch_max_pct", "Peak shrinkage mismatch"), ("line_Pi_max", "Line damage index")]
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
        ax.errorbar(mu / mx, y, xerr=np.zeros_like(mu), fmt="none")
        ax.plot(sg / mx, y, "o", ms=2.6, color=fs.ORANGE)
        ax.set_title(lab, fontsize=6.6)
        ax.set_xlim(0, 1.25)
        ax.set_xlabel("μ*/max (bars), σ/max (dots)", fontsize=5.8)
        fs.panel(ax, "abcde"[k], x=-0.05 if k else -1.0)
    axs[0].set_yticks(y); axs[0].set_yticklabels([LABELS.get(keys[i], keys[i]) for i in order], fontsize=6.2)
    fs.save(fig, "fig10_sensitivity", O)


if __name__ == "__main__":
    for w in which:
        {"design": fig_design, "programme": fig_programme, "package": fig_package, "sens": fig_sens}[w]()
