#!/usr/bin/env python3
"""Render the benchmark figures used in the E2 report.

Usage:
    python3 plot.py <cpp.json> <node.json> <output-dir>
"""

import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_2 = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
BASELINE = "#c3c2b7"
CPP = "#2a78d6"   # categorical slot 1
NODE = "#eb6834"  # categorical slot 2

plt.rcParams.update({
    "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE,
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "text.color": INK,
    "axes.labelcolor": INK_2,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "axes.edgecolor": BASELINE,
})


def style(ax, xlabel=None, grid_axis="x"):
    for side in ("top", "right", "left" if grid_axis == "x" else "bottom"):
        ax.spines[side].set_visible(False)
    ax.grid(axis=grid_axis, color=GRID, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    ax.tick_params(length=0)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=9.5, labelpad=8)


def title(ax, text, subtitle):
    ax.set_title(text, loc="left", fontsize=13, fontweight="600", color=INK, pad=22)
    ax.text(0, 1.035, subtitle, transform=ax.transAxes, fontsize=9.5, color=INK_2,
            va="bottom")


def load(path):
    d = json.load(open(path))
    return d, {f["file"]: f for f in d["files"]}


LABELS = {
    "pcm16_05s.wav": "PCM 16-bit · 5 s",
    "pcm16_30s.wav": "PCM 16-bit · 30 s",
    "pcm16_180s.wav": "PCM 16-bit · 3 min",
    "pcm16_600s.wav": "PCM 16-bit · 10 min",
    "real_sound_186s.wav": "PCM 16-bit · 3 min (real)",
    "pcm08_30s.wav": "PCM 8-bit · 30 s",
    "pcm24_30s.wav": "PCM 24-bit · 30 s",
    "pcm32_30s.wav": "PCM 32-bit · 30 s",
    "flt32_30s.wav": "float32 · 30 s",
}


def fig_throughput(cpp, node, out):
    order = ["pcm16_05s.wav", "pcm16_30s.wav", "pcm16_180s.wav", "pcm16_600s.wav",
             "real_sound_186s.wav", "pcm08_30s.wav", "pcm24_30s.wav",
             "pcm32_30s.wav", "flt32_30s.wav"]
    labels = [LABELS[n] for n in order]
    c = [cpp[n]["samples"] / cpp[n]["decode"]["median"] / 1000 for n in order]
    n_ = [node[n]["samples"] / node[n]["decode"]["median"] / 1000 for n in order]

    fig, ax = plt.subplots(figsize=(9.5, 6.2))
    y = range(len(order))
    h = 0.34
    gap = 0.02  # 2px surface gap between adjacent fills
    ax.barh([i + h / 2 + gap for i in y], c, height=h, color=CPP, zorder=3, label="C++")
    ax.barh([i - h / 2 - gap for i in y], n_, height=h, color=NODE, zorder=3, label="Node")

    for i, v in zip(y, c):
        ax.text(v + 12, i + h / 2 + gap, f"{v:,.0f}", va="center", fontsize=9, color=INK_2)
    for i, v in zip(y, n_):
        ax.text(v + 12, i - h / 2 - gap, f"{v:,.0f}", va="center", fontsize=9, color=INK_2)

    ax.set_yticks(list(y), labels, fontsize=9.5, color=INK_2)
    ax.invert_yaxis()
    ax.set_xlim(0, max(c) * 1.12)
    style(ax, "Million samples decoded per second — higher is better")
    title(ax, "C++ decodes 2–12× more audio per second than JavaScript",
          "Full decode to normalised float32. Median of 41 repetitions × 3 replicates.")
    leg = ax.legend(frameon=False, loc="lower right", fontsize=9.5)
    for t in leg.get_texts():
        t.set_color(INK_2)
    fig.tight_layout()
    fig.savefig(os.path.join(out, "decode-throughput.png"), dpi=160)
    plt.close(fig)


def fig_scaling(cpp, node, out):
    order = ["pcm16_05s.wav", "pcm16_30s.wav", "pcm16_180s.wav", "pcm16_600s.wav"]
    x = [cpp[n]["samples"] / 1e6 for n in order]
    c = [cpp[n]["decode"]["median"] for n in order]
    n_ = [node[n]["decode"]["median"] for n in order]

    fig, ax = plt.subplots(figsize=(8.4, 5.4))
    ax.plot(x, c, color=CPP, linewidth=2, marker="o", markersize=8,
            markeredgecolor=SURFACE, markeredgewidth=2, zorder=3, label="C++")
    ax.plot(x, n_, color=NODE, linewidth=2, marker="o", markersize=8,
            markeredgecolor=SURFACE, markeredgewidth=2, zorder=3, label="Node")

    ax.annotate("C++", (x[-1], c[-1]), textcoords="offset points", xytext=(10, -4),
                color=CPP, fontsize=10, fontweight="600")
    ax.annotate("Node", (x[-1], n_[-1]), textcoords="offset points", xytext=(10, -4),
                color=NODE, fontsize=10, fontweight="600")
    # Label only where there is room: the two smallest files sit on top of each
    # other at this scale and are read from the table instead.
    for xi, ci, ni in list(zip(x, c, n_))[2:]:
        ax.annotate(f"{ci:.0f} ms", (xi, ci), textcoords="offset points",
                    xytext=(0, -18), ha="center", fontsize=8.5, color=INK_2)
        ax.annotate(f"{ni:.0f} ms", (xi, ni), textcoords="offset points",
                    xytext=(0, 12), ha="center", fontsize=8.5, color=INK_2)

    ax.set_xlim(0, max(x) * 1.16)
    ax.set_ylim(0, max(n_) * 1.15)
    ax.set_ylabel("Decode time (ms)", fontsize=9.5, labelpad=8)
    style(ax, "Millions of samples in the file", grid_axis="y")
    ax.spines["bottom"].set_visible(True)
    title(ax, "Both scale linearly; the gap is a constant factor, not a cliff",
          "PCM 16-bit stereo at 44.1 kHz, 5 s to 10 min. Median of 41 repetitions × 3 replicates.")
    fig.tight_layout()
    fig.savefig(os.path.join(out, "decode-scaling.png"), dpi=160)
    plt.close(fig)


def fig_header(cpp, node, out):
    order = ["pcm16_30s.wav", "flt32_30s.wav", "pcm08_30s.wav",
             "pcm24_30s.wav", "pcm32_30s.wav"]
    labels = [LABELS[n] for n in order]
    c = [cpp[n]["header"]["median"] for n in order]
    n_ = [node[n]["header"]["median"] for n in order]

    fig, ax = plt.subplots(figsize=(9.2, 4.6))
    y = range(len(order))
    h = 0.34
    gap = 0.02
    ax.barh([i + h / 2 + gap for i in y], c, height=h, color=CPP, zorder=3, label="C++")
    ax.barh([i - h / 2 - gap for i in y], n_, height=h, color=NODE, zorder=3, label="Node")
    for i, v in zip(y, c):
        ax.text(v * 1.15, i + h / 2 + gap, f"{v:.3f} ms", va="center", fontsize=9, color=INK_2)
    for i, v in zip(y, n_):
        ax.text(v * 1.15, i - h / 2 - gap, f"{v:.3f} ms", va="center", fontsize=9, color=INK_2)

    ax.set_xscale("log")
    ax.set_xlim(0.001, 8)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}"))
    ax.set_yticks(list(y), labels, fontsize=9.5, color=INK_2)
    ax.invert_yaxis()
    style(ax, "Time to read the header only (ms, log scale) — lower is better")
    title(ax, "readMetadata is only header-only for 16-bit and float32",
          "For 8-, 24- and 32-bit PCM the C++ parser still reads the whole data chunk off disk.")
    leg = ax.legend(frameon=False, loc="upper right", fontsize=9.5)
    for t in leg.get_texts():
        t.set_color(INK_2)
    fig.tight_layout()
    fig.savefig(os.path.join(out, "header-only-latency.png"), dpi=160)
    plt.close(fig)


def main() -> int:
    if len(sys.argv) != 4:
        print(__doc__)
        return 1
    _, cpp = load(sys.argv[1])
    _, node = load(sys.argv[2])
    out = sys.argv[3]
    os.makedirs(out, exist_ok=True)
    fig_throughput(cpp, node, out)
    fig_scaling(cpp, node, out)
    fig_header(cpp, node, out)
    print(f"wrote 3 figures to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
