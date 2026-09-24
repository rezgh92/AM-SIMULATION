"""Graphical abstract: printed part, the order of events, and the matched shrinkage."""
import json, sys, importlib.util, pathlib
import numpy as np
import matplotlib.pyplot as plt
import figstyle as fs

D, O = sys.argv[1], sys.argv[2]
fs.apply()
HERE = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("ov", HERE / "fig_overview.py")
ov = importlib.util.module_from_spec(spec)
sys.argv_saved = sys.argv
spec.loader.exec_module(ov)

S = json.load(open(f"{D}/programme_series.json"))
fig = plt.figure(figsize=(13.3 / 2.54 * 1.5, 5.0 / 2.54 * 1.5))
ax0 = fig.add_axes([0.0, 0.03, 0.24, 0.94], projection="3d")
ov.draw_vehicle(ax0)
cases = (("baseline", "fine Cu, IBM-type programme"), ("optimised", "char-timed release (fragile)"),
         ("robust", "robust paste and programme"))
for k, (lab, title) in enumerate(cases):
    ax = fig.add_axes([0.29 + 0.24 * k, 0.2, 0.2, 0.62])
    s = S[lab]
    t = np.array(s["t_h"])
    ax.plot(t, -100 * np.array(s["eps_cu"]), color=fs.CU, lw=1.6, label="copper")
    ax.plot(t, -100 * np.array(s["eps_gc"]), color=fs.GC, lw=1.6, label="glass-ceramic")
    ax.fill_between(t, -100 * np.array(s["eps_cu"]), -100 * np.array(s["eps_gc"]), color=fs.ORANGE, alpha=0.18, lw=0)
    d = np.max(np.abs(np.array(s["eps_cu"]) - np.array(s["eps_gc"]))) * 100
    ax.text(0.04, 0.96, f"peak mismatch\n{d:.1f} %", transform=ax.transAxes, va="top", fontsize=6.8, color=fs.INK,
            fontweight="bold", linespacing=1.2)
    ax.set_title(title, fontsize=6.6, loc="left")
    ax.set_xlabel("Time (h)", fontsize=6.6)
    ax.set_ylim(0, 32); ax.set_xlim(5, 18)
    ax.tick_params(labelsize=6)
    if k == 0:
        ax.set_ylabel("Free shrinkage (%)", fontsize=6.6)
        ax.legend(loc="lower right", fontsize=6)
    else:
        ax.set_yticklabels([])
fs.save(fig, "graphical_abstract", O)
