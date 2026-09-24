"""Figure: thermal-mismatch stress and bow on cooling a co-fired Cu / glass-ceramic stack."""
import json, sys
import numpy as np
import matplotlib.pyplot as plt
import figstyle as fs

D, O = sys.argv[1], sys.argv[2]
fs.apply()
d = json.load(open(f"{D}/cooling.json"))
fig, (a, b) = plt.subplots(1, 2, figsize=(fs.COL2, 0.36 * fs.COL2), gridspec_kw=dict(wspace=0.3))
cols = {10.0: fs.BLUE, 50.0: fs.ORANGE, 200.0: fs.AQUA}
for c in d["cases"]:
    if c["h_cu_um"] not in cols:
        continue
    ls = "-" if c["model"] == "plastic" else ":"
    a.plot(c["T"], c["s_cu_MPa"], color=cols[c["h_cu_um"]], ls=ls, lw=1.3)
from cupola.cofire import props
T = np.linspace(25, d["T_sf"], 50)
a.plot(T, props.cu_yield(T) / 1e6, color=fs.INK2, lw=0.8, ls="--")
a.set_xlim(d["T_sf"], 25)
a.set_yscale("symlog", linthresh=100)
a.set_ylim(0, 2500)
a.set_xlabel("Temperature on cooling (°C)")
a.set_ylabel("Mean stress in the copper layer (MPa)")
from matplotlib.lines import Line2D
h = [Line2D([], [], color=cols[k], lw=1.3, label=f"{k:g} µm Cu") for k in cols]
h += [Line2D([], [], color=fs.MUTED, lw=1.3, label="elastic–plastic Cu"), Line2D([], [], color=fs.MUTED, lw=1.3, ls=":", label="elastic Cu"),
      Line2D([], [], color=fs.INK2, lw=0.8, ls="--", label="yield stress")]
a.legend(handles=h, loc="upper right", bbox_to_anchor=(1.0, 0.64), fontsize=6, ncol=2, columnspacing=1.0,
         title="on 1 mm glass-ceramic", title_fontsize=6)
fs.panel(a, "a")
hs = sorted({c["h_cu_um"] for c in d["cases"]})
pl = [next(c["bow_um_20mm"][-1] for c in d["cases"] if c["h_cu_um"] == x and c["model"] == "plastic") for x in hs]
el = [next(c["bow_um_20mm"][-1] for c in d["cases"] if c["h_cu_um"] == x and c["model"] == "elastic") for x in hs]
xx = np.arange(len(hs))
b.bar(xx - 0.2, el, width=0.38, color="#C9D0D5", label="elastic copper")
b.bar(xx + 0.2, pl, width=0.38, color=fs.CU, label="elastic–plastic copper")
for x, v in zip(xx + 0.2, pl):
    b.text(x, v + 6, f"{v:.0f}", ha="center", fontsize=6, color=fs.INK)
b.set_xticks(xx); b.set_xticklabels([f"{x:g}" for x in hs])
b.set_xlabel("Copper plane thickness on 1 mm glass-ceramic (µm)")
b.set_ylabel("Bow over 20 mm after cooling (µm)")
b.legend(loc="upper left", fontsize=6)
fs.panel(b, "b")
fs.save(fig, "fig09_cooling", O)
