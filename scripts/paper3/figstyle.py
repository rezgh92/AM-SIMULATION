"""Shared figure style for the co-firing paper (Elsevier column widths, vector PDF output)."""
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

MM = 1 / 25.4
COL1 = 90 * MM          # single column
COL15 = 140 * MM
COL2 = 190 * MM         # full width

# categorical order (validated palette): blue, orange, aqua, yellow; greys for references
BLUE, ORANGE, AQUA, YELLOW = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"
INK, INK2, MUTED, RULE = "#15181B", "#3B444B", "#6B757D", "#C9D0D5"
CU = "#B4622D"          # copper, used only where the material itself is meant
GC = "#2a78d6"
CRIT = "#d03b3b"
GOOD = "#0ca30c"

SEQ_BLUE = LinearSegmentedColormap.from_list("seq_blue", ["#F2F6FB", "#C7DAF3", "#7FAEE6", "#2a78d6", "#123F7A"])
SEQ_COPPER = LinearSegmentedColormap.from_list("seq_cu", ["#F6E3D3", "#E4A77A", "#BF6A33", "#6B2E0E"])
DIVERGE = LinearSegmentedColormap.from_list("div", ["#123F7A", "#2a78d6", "#E9ECEE", "#eb6834", "#8A2F0D"])


def apply():
    mpl.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Liberation Sans", "Arial", "DejaVu Sans"],
        "mathtext.fontset": "custom",
        "mathtext.rm": "Liberation Sans",
        "mathtext.it": "Liberation Sans:italic",
        "mathtext.bf": "Liberation Sans:bold",
        "mathtext.cal": "Liberation Sans:italic",
        "mathtext.sf": "Liberation Sans",
        "font.size": 7.5,
        "axes.titlesize": 7.5,
        "axes.labelsize": 7.5,
        "xtick.labelsize": 6.8,
        "ytick.labelsize": 6.8,
        "legend.fontsize": 6.6,
        "axes.linewidth": 0.6,
        "axes.edgecolor": INK2,
        "axes.labelcolor": INK,
        "xtick.color": INK2,
        "ytick.color": INK2,
        "xtick.major.width": 0.6,
        "ytick.major.width": 0.6,
        "xtick.major.size": 2.5,
        "ytick.major.size": 2.5,
        "xtick.direction": "out",
        "ytick.direction": "out",
        "lines.linewidth": 1.3,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "legend.frameon": False,
        "legend.handlelength": 1.6,
        "savefig.dpi": 600,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.02,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "axes.grid": False,
        "figure.dpi": 150,
    })


def panel(ax, letter, x=-0.16, y=1.04):
    ax.text(x, y, f"({letter})", transform=ax.transAxes, fontsize=8, fontweight="bold", va="bottom", ha="left", color=INK)


def save(fig, name, outdir):
    fig.savefig(f"{outdir}/{name}.pdf")
    fig.savefig(f"{outdir}/{name}.png", dpi=300)
    plt.close(fig)
