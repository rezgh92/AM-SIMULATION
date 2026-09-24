"""Figures 2-5: verification, atmosphere window, carbon race map, sintering-temperature ladder."""
import json, sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import figstyle as fs

D = sys.argv[1]      # data dir
O = sys.argv[2]      # figure dir
fs.apply()


def fig_verification():
    vg = json.load(open(f"{D}/verify_glass.json"))
    vb = json.load(open(f"{D}/verify_bilayer.json"))
    fig, (a, b) = plt.subplots(1, 2, figsize=(fs.COL2, 0.36 * fs.COL2), gridspec_kw=dict(wspace=0.32))
    cols = {810.0: fs.BLUE, 830.0: fs.ORANGE, 850.0: fs.AQUA}
    for c in vg["cases"]:
        if c["N"] != 8:
            continue
        t = np.array(c["t_h"]); t = t - t[0]
        a.plot(t, 1 - np.array(c["theta"]), color=cols[c["T"]], lw=1.4, label=f"{c['T']:.0f} °C, slab model")
        k = max(1, len(t) // 12)
        a.plot(t[::k], 1 - np.array(c["theta_ref"])[::k], "o", ms=3.2, mfc="white", mec=cols[c["T"]], mew=0.9)
    a.set_xlabel("Time in isothermal hold (h)")
    a.set_ylabel("Relative density of glass-ceramic")
    a.set_xlim(0, 5.8)
    h1 = [Line2D([], [], color=cols[T], lw=1.4, label=f"{T:.0f} °C") for T in cols]
    h1.append(Line2D([], [], color=fs.MUTED, lw=1.4, label="slab model"))
    h1.append(Line2D([], [], color=fs.MUTED, marker="o", ms=3.2, mfc="white", lw=0, label="closed form"))
    a.legend(handles=h1, loc="lower right")
    errs = [max(c["max_abs_err"] for c in vg["cases"] if c["T"] == T) for T in cols]
    a.text(0.03, 0.97, "max |Δθ| ≤ %.1e" % max(errs), transform=a.transAxes, va="top", fontsize=6.6, color=fs.INK2)
    fs.panel(a, "a")
    h = np.array([r["h"] for r in vb]); e = np.abs([r["rel_err"] for r in vb]) * 100
    b.loglog(h, e, "o-", color=fs.BLUE, ms=4, lw=1.3, label="3-D FEM vs viscous Timoshenko")
    hh = np.array([0.13, 0.7])
    b.loglog(hh, e[-1] * (hh / h[-1]) ** 2, "--", color=fs.MUTED, lw=0.9, label="slope 2")
    for hi, ei, r in zip(h, e, vb):
        b.annotate(f"{r['n_el']/1000:.1f}k el.", (hi, ei), textcoords="offset points", xytext=(5, 3), fontsize=6, color=fs.INK2)
    b.set_xlabel("Voxel size (mm)")
    b.set_ylabel("Error in curvature rate (%)")
    b.set_xlim(0.12, 0.8)
    b.legend(loc="upper left")
    fs.panel(b, "b")
    fs.save(fig, "fig02_verification", O)


def fig_atmosphere():
    d = json.load(open(f"{D}/atmosphere_window.json"))
    T = np.array(d["T_C"]); lr = np.array(d["logr"])
    fig, ax = plt.subplots(figsize=(fs.COL1, 0.95 * fs.COL1))
    hl = np.array(d["half_life_h"]["0.3"])
    cu = np.log10(d["ratio_cu"]); gas = np.log10(d["ratio_gas"])
    TT, LR = np.meshgrid(T, lr)
    ok = (LR < cu[None, :])
    Z = np.where(ok, np.log10(hl), np.nan)
    cs = ax.contourf(TT, LR, Z, levels=np.arange(-1.5, 3.01, 0.5), cmap=fs.SEQ_BLUE.reversed(), extend="both")
    cl = ax.contour(TT, LR, np.log10(hl), levels=[np.log10(0.5), 0, np.log10(4)], colors=[fs.INK2], linewidths=0.6)
    ax.clabel(cl, fmt={np.log10(0.5): "0.5 h", 0.0: "1 h", np.log10(4): "4 h"}, fontsize=5.8,
              manual=[(690, 2.2), (745, 2.2), (790, 2.2)])
    ax.fill_between(T, cu, 8, color="#F4D9CC", lw=0)
    ax.plot(T, cu, color=fs.ORANGE, lw=1.5)
    ax.text(420, 7.25, "Cu oxidises to Cu$_2$O", color="#8A2F0D", fontsize=6.6)
    ax.plot(T, gas, color=fs.MUTED, lw=1.0, ls="--")
    ax.text(484, -1.62, "← C + H$_2$O blocked", fontsize=5.6, color=fs.INK2, va="center")
    p = d["points"]
    ax.plot([400, 900], [np.log10(p["forming_gas_bubbler"]["ratio"])] * 2, color=fs.INK2, lw=0.9)
    ax.text(405, np.log10(p["forming_gas_bubbler"]["ratio"]) + 0.15, "4 % H$_2$ through a +20 °C bubbler", fontsize=5.8, color=fs.INK)
    TB = 780.0; rB = 0.2 * d["ratio_cu"][int(np.argmin(abs(T - TB)))]
    ax.plot(TB, np.log10(rB), "o", ms=5, color=fs.ORANGE, mec="white", mew=0.8, zorder=5)
    ax.annotate("steam burnout\nat 20 % of the Cu limit", (TB, np.log10(rB)), xytext=(560, 5.2), fontsize=5.8,
                arrowprops=dict(arrowstyle="-", color=fs.INK2, lw=0.6), color=fs.INK)
    ax.axvline(875, color="white", lw=1.0, ls=(0, (3, 2)))
    ax.text(882, 1.2, "glass pores\nclose above\n~875 °C", fontsize=5.8, color="white")
    ax.set_xlim(400, 1000); ax.set_ylim(-2, 8)
    ax.set_xlabel("Temperature (°C)")
    ax.set_ylabel("log$_{10}$(p$_{H_2O}$/p$_{H_2}$)")
    cb = fig.colorbar(cs, ax=ax, pad=0.02, fraction=0.05)
    cb.set_label("log$_{10}$ char half-life (h), 30 % steam", fontsize=6.4)
    cb.ax.tick_params(labelsize=6)
    fs.save(fig, "fig03_atmosphere", O)


def fig_race():
    d = json.load(open(f"{D}/race_map.json"))
    TB = np.array(d["TB"]); tB = np.array(d["tB"])
    fig, axs = plt.subplots(1, 2, figsize=(fs.COL2, 0.40 * fs.COL2), sharey=True, gridspec_kw=dict(wspace=0.08))
    titles = {"steam": "30 % steam, H$_2$ at 20 % of Cu/Cu$_2$O limit", "fg": "4 % H$_2$ through a +20 °C bubbler"}
    for ax, atm, L in zip(axs, ("steam", "fg"), "ab"):
        C = np.full((len(tB), len(TB)), np.nan); closed = np.zeros_like(C, dtype=bool)
        for r in d["runs"]:
            if r["atm"] != atm:
                continue
            i = int(np.argmin(abs(tB - r["t_B"]))); j = int(np.argmin(abs(TB - r["T_B"])))
            C[i, j] = r["C"]; closed[i, j] = r["closed_in_hold"]
        Z = np.log10(np.maximum(C, 1.0))
        cs = ax.contourf(TB, np.log10(tB), Z, levels=np.arange(0, 4.6, 0.5), cmap=fs.SEQ_BLUE, extend="both")
        cl = ax.contour(TB, np.log10(tB), Z, levels=[2.0], colors=[fs.ORANGE], linewidths=1.4)
        ii, jj = np.where(closed)
        ax.plot(TB[jj], np.log10(tB[ii]), "x", color=fs.CRIT, ms=3.5, mew=0.9)
        ax.set_title(titles[atm], fontsize=6.8, loc="left")
        ax.set_xlabel("Burnout temperature T$_B$ (°C)")
        ax.set_yticks(np.log10([0.25, 0.5, 1, 2, 4, 8, 16])); ax.set_yticklabels(["0.25", "0.5", "1", "2", "4", "8", "16"])
        fs.panel(ax, L, x=-0.1 if L == "b" else -0.16)
    axs[0].set_ylabel("Burnout hold t$_B$ (h)")
    axs[0].text(760, np.log10(2.6), "100 ppm C", color=fs.ORANGE, fontsize=6.4, rotation=-38)
    axs[1].plot([], [], "x", color=fs.CRIT, label="glass closed during hold")
    axs[1].legend(loc="upper right", fontsize=6)
    cb = fig.colorbar(cs, ax=axs, pad=0.015, fraction=0.03)
    cb.set_label("log$_{10}$ carbon at glass pore closure (ppm)", fontsize=6.4)
    cb.ax.tick_params(labelsize=6)
    fs.save(fig, "fig04_race", O)


def fig_ladder():
    d = json.load(open(f"{D}/free_sintering.json"))
    fig = plt.figure(figsize=(fs.COL2, 0.44 * fs.COL2))
    gsp = fig.add_gridspec(2, 2, width_ratios=[1.15, 1], height_ratios=[3.2, 1], wspace=0.55, hspace=0.12)
    a = fig.add_subplot(gsp[0, 0]); ax2 = fig.add_subplot(gsp[1, 0], sharex=a); b = fig.add_subplot(gsp[:, 1])
    g = d["gc"]["default"]
    a.plot(g["T"], g["shrink"], color=fs.GC, lw=2.0, label="glass-ceramic")
    ax2.plot(g["T"], g["X"], color=fs.GC, lw=1.4)
    ax2.set_ylim(0, 1.05); ax2.set_yticks([0, 0.5, 1])
    ax2.set_ylabel("X$_c$ (glass)")
    ax2.set_xlabel("Temperature (°C), 5 K min$^{-1}$")
    plt.setp(a.get_xticklabels(), visible=False)
    cmap = fs.SEQ_COPPER
    ds = [1.0, 3.0, 6.0, 12.0, 20.0]
    for k, dd in enumerate(ds):
        c = d["cu"][f"d{dd:g}_f0"]
        a.plot(c["T"], c["shrink"], color=cmap(0.25 + 0.75 * k / (len(ds) - 1)), lw=1.2, label=f"Cu {dd:g} µm")
    a.set_xlim(250, 1060); a.set_ylim(0, 25)
    a.set_ylabel("Free linear shrinkage (%)")
    a.legend(loc="upper left", ncol=2, bbox_to_anchor=(0.0, 1.0), columnspacing=1.0)
    fs.panel(a, "a")
    rows = []
    for dd in [1.0, 2.0, 3.0, 6.0, 12.0, 20.0]:
        for f in [0.0, 0.4]:
            c = d["cu"][f"d{dd:g}_f{f:g}"]
            rows.append((f"Cu {dd:g} µm" + (f" + {int(f*100)} % filler" if f else ""), c["T05"], c["T50"], c["T95"], f))
    y = np.arange(len(rows) + 1)
    b.axvspan(g["T05"], g["T95"], color=fs.GC, alpha=0.10, lw=0)
    b.barh(y[-1], g["T95"] - g["T05"], left=g["T05"], height=0.62, color=fs.GC)
    b.plot([g["T50"]] * 2, [y[-1] - 0.31, y[-1] + 0.31], color=fs.INK, lw=1.0)
    for yi, (lab, t5, t50, t95, f) in zip(y[:-1], rows):
        b.barh(yi, t95 - t5, left=t5, height=0.62, color=fs.CU if f == 0 else "#E8B48E")
        b.plot([t50] * 2, [yi - 0.31, yi + 0.31], color=fs.INK, lw=1.0)
    b.set_yticks(y); b.set_yticklabels([r[0] for r in rows] + ["glass-ceramic"], fontsize=6.2)
    b.set_xlabel("5–95 % of shrinkage (°C); tick = 50 %")
    b.set_xlim(250, 1070)
    fs.panel(b, "b", x=-0.52)
    fs.save(fig, "fig05_ladder", O)


if __name__ == "__main__":
    fig_verification()
    fig_atmosphere()
    fig_race()
    fig_ladder()
