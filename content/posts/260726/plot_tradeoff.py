#!/usr/bin/env python3
"""Render the stable storage–recall trade-off from the turbovec benchmark."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib-blog-cache")

import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter


COLORS = {
    "float32": "#CBD5E1",
    "2 bit": "#EF4444",
    "3 bit": "#F59E0B",
    "4 bit": "#2563EB",
    "ink": "#172033",
    "muted": "#64748B",
    "grid": "#E2E8F0",
}


def load_results(path: Path) -> tuple[list[str], list[float], list[float], list[float]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    rows = payload["results"]
    labels = ["Float32", *[f"{row['bit_width']} bit" for row in rows]]
    sizes = [payload["dataset"]["float32_mib"], *[row["index_mib"] for row in rows]]
    recalls = [1.0, *[row["recall_at_10"] for row in rows]]
    compression = [1.0, *[row["compression_vs_float32"] for row in rows]]
    return labels, sizes, recalls, compression


def render(input_path: Path, output_path: Path) -> None:
    labels, sizes, recalls, compression = load_results(input_path)
    colors = [COLORS["float32"], COLORS["2 bit"], COLORS["3 bit"], COLORS["4 bit"]]

    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 12,
            "svg.fonttype": "none",
            "svg.hashsalt": "turbovec-space-recall-v1",
            "axes.titleweight": "bold",
            "axes.titlesize": 16,
            "axes.labelcolor": COLORS["muted"],
            "xtick.color": COLORS["muted"],
            "ytick.color": COLORS["muted"],
        }
    )

    fig, (size_ax, recall_ax) = plt.subplots(1, 2, figsize=(13.5, 6.8))
    fig.patch.set_facecolor("#FFFFFF")
    fig.suptitle(
        "Low-bit compression trades storage for nearest-neighbor recall",
        x=0.07,
        y=0.97,
        ha="left",
        fontsize=21,
        fontweight="bold",
        color=COLORS["ink"],
    )
    fig.text(
        0.07,
        0.91,
        "turbovec 0.8.0 · 50,000 × 384 random unit vectors · Recall@10",
        ha="left",
        fontsize=11.5,
        color=COLORS["muted"],
    )

    y_positions = list(range(len(labels)))
    size_ax.barh(y_positions, sizes, color=colors, height=0.62)
    size_ax.set_yticks(y_positions, labels)
    size_ax.invert_yaxis()
    size_ax.set_title("Index size", loc="left", pad=14, color=COLORS["ink"])
    size_ax.set_xlabel("MiB")
    size_ax.grid(axis="x", color=COLORS["grid"], linewidth=0.9)
    size_ax.set_axisbelow(True)
    size_ax.spines[["top", "right", "left"]].set_visible(False)
    size_ax.spines["bottom"].set_color(COLORS["grid"])
    size_ax.tick_params(axis="y", length=0)
    size_ax.set_xlim(0, max(sizes) * 1.18)

    for index, (size, ratio) in enumerate(zip(sizes, compression, strict=True)):
        label = f"{size:.2f} MiB"
        if ratio > 1:
            label += f"  ({ratio:.2f}× smaller)"
        size_ax.text(
            size + max(sizes) * 0.018,
            index,
            label,
            va="center",
            fontsize=10.5,
            color=COLORS["ink"],
        )

    x_positions = list(range(len(labels)))
    recall_ax.plot(
        x_positions,
        recalls,
        color=COLORS["ink"],
        linewidth=2.2,
        marker="o",
        markersize=8,
        zorder=2,
    )
    recall_ax.scatter(x_positions, recalls, c=colors, s=92, zorder=3, edgecolors="#FFFFFF")
    recall_ax.set_xticks(x_positions, labels)
    recall_ax.set_ylim(0.4, 1.04)
    recall_ax.yaxis.set_major_formatter(PercentFormatter(1.0))
    recall_ax.set_title("Recall@10", loc="left", pad=14, color=COLORS["ink"])
    recall_ax.set_ylabel("Exact neighbors retained")
    recall_ax.grid(axis="y", color=COLORS["grid"], linewidth=0.9)
    recall_ax.set_axisbelow(True)
    recall_ax.spines[["top", "right", "left"]].set_visible(False)
    recall_ax.spines["bottom"].set_color(COLORS["grid"])
    recall_ax.tick_params(axis="y", length=0)

    for index, recall in enumerate(recalls):
        recall_ax.annotate(
            f"{recall:.1%}",
            (index, recall),
            xytext=(0, 12 if index != 0 else -20),
            textcoords="offset points",
            ha="center",
            fontsize=10.5,
            fontweight="bold",
            color=COLORS["ink"],
        )

    recall_ax.annotate(
        "+13.25 pp recall\nfor +2.29 MiB",
        xy=(3, recalls[3]),
        xytext=(2.15, 0.91),
        arrowprops={"arrowstyle": "->", "color": COLORS["4 bit"], "lw": 1.5},
        fontsize=10.5,
        color=COLORS["4 bit"],
        fontweight="bold",
        ha="center",
    )

    fig.text(
        0.07,
        0.035,
        "Source: benchmark-results.json. Index size and recall reproduced identically in the rerun; "
        "latency is intentionally omitted because it varied across the shared container.",
        ha="left",
        fontsize=9.5,
        color=COLORS["muted"],
    )
    fig.subplots_adjust(left=0.07, right=0.97, top=0.82, bottom=0.16, wspace=0.34)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(
        output_path,
        dpi=160,
        facecolor=fig.get_facecolor(),
        metadata={"Date": None, "Creator": "plot_tradeoff.py"},
    )
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        type=Path,
        default=Path(__file__).with_name("benchmark-results.json"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).with_name("04-space-recall-tradeoff.svg"),
    )
    args = parser.parse_args()
    render(args.input, args.output)


if __name__ == "__main__":
    main()
