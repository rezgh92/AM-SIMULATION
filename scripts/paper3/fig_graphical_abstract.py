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
ax0 = fig.add_axes([0.0, 0.02, 0.27, 0.96], projection="3d")
ov.draw_vehicle(ax0)
for k, (lab, title) in enumerate((("baseline", "3 µm Cu, IBM-type programme"), ("optimised", "matched paste and programme"))):
    ax = fig.add_axes([0.33 + 0.345 * k, 0.2, 0.29, 0.66])
    s = S[lab]
    t = np.array(s["t_h"])
    ax.plot(t, -100 * np.array(s["eps_cu"]), color=fs.CU, lw=1.6, label="copper")
    ax.plot(t, -100 * np.array(s["eps_gc"]), color=fs.GC, lw=1.6, label="glass-ceramic")
    ax.fill_between(t, -100 * np.array(s["eps_cu"]), -100 * np.array(s["eps_gc"]), color=fs.ORANGE, alpha=0.18, lw=0)
    d = np.max(np.abs(np.array(s["eps_cu"]) - np.array(s["eps_gc"]))) * 100
    ax.text(0.03, 0.95, f"peak mismatch {d:.1f} %", transform=ax.transAxes, va="top", fontsize=7, color=fs.INK,
            fontweight="bold")
    ax.set_title(title, fontsize=7.2, loc="left")
    ax.set_xlabel("Time (h)")
    ax.set_ylim(0, 32)
    if k == 0:
        ax.set_ylabel("Free shrinkage (%)")
        ax.legend(loc="lower right", fontsize=6.4)
fs.save(fig, "graphical_abstract", O)
