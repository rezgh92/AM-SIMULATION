"""Figure 1: (a) the printed test vehicle (glass-ceramic body with buried copper) and
(b) the modelling framework."""
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import importlib.util, pathlib

import figstyle as fs

HERE = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("pk", HERE / "package3d.py")
pk = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pk)


def draw_vehicle(ax):
    h = 0.25
    m = pk.package_mask(h)
    cu = m == 1
    colors = np.empty(m.shape, dtype=object)
    colors[cu] = fs.CU
    ax.voxels(cu, facecolors=colors, edgecolor=(0.35, 0.18, 0.06, 0.25), linewidth=0.1, shade=True)
    n, _, nz = m.shape
    # glass-ceramic body: outline, translucent faces and the open die cavity
    for z in (0, nz):
        ax.plot([0, n, n, 0, 0], [0, 0, n, n, 0], [z] * 5, color=fs.GC, lw=0.6, alpha=0.9)
    for x, y in ((0, 0), (n, 0), (n, n), (0, n)):
        ax.plot([x, x], [y, y], [0, nz], color=fs.GC, lw=0.6, alpha=0.9)
    xx, yy = np.meshgrid([0, n], [0, n])
    ax.plot_surface(xx, yy, np.zeros_like(xx, dtype=float), color=fs.GC, alpha=0.06, linewidth=0)
    void = np.argwhere(m == -1)
    a0, a1 = void[:, 0].min(), void[:, 0].max() + 1
    zf = void[:, 2].min()
    for z, ls in ((nz, "-"), (zf, ":")):
        ax.plot([a0, a1, a1, a0, a0], [a0, a0, a1, a1, a0], [z] * 5, color=fs.GC, lw=0.7, ls=ls)
    for x, y in ((a0, a0), (a1, a0), (a1, a1), (a0, a1)):
        ax.plot([x, x], [y, y], [zf, nz], color=fs.GC, lw=0.6, ls=":")
    ax.text((a0 + a1) / 2, a1, nz + 0.4, "die cavity", color=fs.GC, fontsize=6.0, ha="center", va="bottom")
    ax.set_box_aspect((n, n, nz * 2.2))
    ax.view_init(elev=28, azim=-58)
    ax.set_axis_off()
    ax.text2D(0.02, 0.93, "glass-ceramic package\n10 × 10 × 2.5 mm, open die cavity", transform=ax.transAxes,
              color=fs.GC, fontsize=6.4)
    ax.text2D(0.02, 0.02, "copper: die pad and thermal vias, meshed ground,\nsolenoid, shielded stripline, bond pad",
              transform=ax.transAxes, color=fs.CU, fontsize=6.4)


def box(ax, x, y, w, h, title, body, fc="#F4F6F8", ec=fs.RULE, tc=fs.INK):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.006,rounding_size=0.012",
                                fc=fc, ec=ec, lw=0.7))
    ax.text(x + 0.012, y + h - 0.018, title, fontsize=6.4, fontweight="bold", color=tc, va="top")
    ax.text(x + 0.012, y + h - 0.062, body, fontsize=5.6, color=fs.INK2, va="top", linespacing=1.3)


def arrow(ax, a, b, color=fs.MUTED):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=7, lw=0.8, color=color,
                                 shrinkA=0, shrinkB=0))


def draw_flow(ax):
    ax.set_xlim(-0.012, 1.02)
    ax.set_ylim(0, 1)
    ax.set_axis_off()
    box(ax, 0.00, 0.72, 0.30, 0.26, "Inputs with provenance",
        "powders, loadings, binder\nglass viscosity, crystallisation\ncopper diffusion data\nfurnace and gas limits\nliterature, analogue or calibrated")
    box(ax, 0.35, 0.80, 0.30, 0.18, "Glass-ceramic slab",
        "binder, char, steam gasification\nMYEGA melt + JMAK crystals\nSkorohod-Olevsky sintering", fc="#EEF4FC", ec="#9CC0E8")
    box(ax, 0.35, 0.57, 0.30, 0.18, "Copper slab",
        "binder, char, oxide, reduction\nFrost-Ashby creep + grain growth\nfiller, trapped gas", fc="#FBF1EA", ec="#E4B894")
    box(ax, 0.70, 0.72, 0.30, 0.26, "Shared furnace programme",
        "N$_2$ pyrolysis → steam burnout\n(pH$_2$O/pH$_2$ below Cu/Cu$_2$O)\n→ dry H$_2$/N$_2$ co-sintering\n→ reducing cool")
    box(ax, 0.00, 0.30, 0.30, 0.22, "Co-firing mechanics",
        "porous viscous moduli\nbilayer camber (Timoshenko)\nembedded-line stress (Maxwell)\ncooling with Cu plasticity")
    box(ax, 0.35, 0.30, 0.30, 0.22, "3-D co-sintering FEM",
        "voxel mesh of the printed part\ntwo materials, gravity,\nsetter friction")
    box(ax, 0.70, 0.30, 0.30, 0.22, "Constraints",
        "C at glass closure, Cu metallic\ndensities, crystallinity\ndamage indices, conductivity\nmelting margin, cycle time")
    box(ax, 0.18, 0.06, 0.64, 0.16, "Design outputs",
        "atmosphere and burnout window  ·  copper paste (D50, filler, loading)\n"
        "nominal and robust programmes  ·  sensitivity: what to measure first", fc="#F1F7F4", ec="#9FD4BD")
    arrow(ax, (0.30, 0.86), (0.35, 0.89))
    arrow(ax, (0.30, 0.78), (0.35, 0.66))
    arrow(ax, (0.70, 0.88), (0.65, 0.89))
    arrow(ax, (0.70, 0.80), (0.65, 0.66))
    arrow(ax, (0.42, 0.57), (0.20, 0.52))
    arrow(ax, (0.50, 0.57), (0.50, 0.52))
    arrow(ax, (0.30, 0.41), (0.35, 0.41))
    arrow(ax, (0.65, 0.41), (0.70, 0.41))
    arrow(ax, (0.85, 0.30), (0.70, 0.22))
    arrow(ax, (0.15, 0.30), (0.30, 0.22))
    ax.annotate("", xy=(0.86, 0.72), xytext=(0.86, 0.52),
                arrowprops=dict(arrowstyle="-|>", color=fs.ORANGE, lw=0.9, mutation_scale=7, linestyle="--"))
    ax.text(0.875, 0.60, "optimiser\nadjusts", fontsize=5.8, color=fs.ORANGE, va="center")


if __name__ == "__main__":
    out = sys.argv[1]
    fs.apply()
    fig = plt.figure(figsize=(fs.COL2, 0.42 * fs.COL2))
    ax1 = fig.add_axes([0.0, 0.02, 0.36, 0.96], projection="3d")
    draw_vehicle(ax1)
    ax2 = fig.add_axes([0.38, 0.02, 0.61, 0.96])
    draw_flow(ax2)
    fig.text(0.005, 0.965, "(a)", fontsize=8, fontweight="bold")
    fig.text(0.375, 0.965, "(b)", fontsize=8, fontweight="bold")
    fs.save(fig, "fig01_overview", out)
