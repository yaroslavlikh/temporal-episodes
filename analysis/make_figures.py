"""Generate the paper figures from published results.

    python3 analysis/make_figures.py      # writes paper/figures/*.pdf and *.png

Static print figures, light surface. Colors: categorical slot 1 (#2a78d6, validated on the
#fcfcfb surface) marks this work; published systems use the muted ink token. Per-condition
confidence intervals in the Temporal figure are percentile bootstraps over questions
(20,000 samples, seed 20260912) and are for display only; paired statistics are in the tables.
"""
from __future__ import annotations

import json
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402
from matplotlib.ticker import FixedLocator, FuncFormatter, NullLocator  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
RESULTS = REPO / "results"
OUT = REPO / "paper" / "figures"
PUBLISHED = json.loads((REPO / "analysis" / "published_baselines.json").read_text())

SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_SECONDARY = "#52514e"
INK_MUTED = "#898781"
GRID = "#e1e0d9"
BASELINE = "#c3c2b7"
OURS = "#2a78d6"
SEED = 20260912

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
    "font.size": 8.5,
    "axes.titlesize": 9.5,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})


def jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def one_decimal(value: float) -> str:
    """Round half up for display, so published 42.55 reads 42.6 rather than float-truncated 42.5."""
    return str(Decimal(str(round(value, 6))).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))


def new_axes(width: float, height: float, value_axis: str):
    fig, ax = plt.subplots(figsize=(width, height))
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(BASELINE)
        ax.spines[side].set_linewidth(0.8)
    ax.tick_params(colors=INK_MUTED, labelcolor=INK_SECONDARY, length=0, pad=4)
    ax.grid(axis=value_axis, color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)
    return fig, ax


def save(fig, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for extension in ("pdf", "png"):
        fig.savefig(OUT / f"{name}.{extension}", dpi=220, facecolor=SURFACE, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {OUT / name}.pdf and .png")


def bootstrap_ci(values: list[int], iterations: int = 20_000) -> tuple[float, float]:
    data = np.asarray(values, dtype=np.float64)
    rng = np.random.default_rng(SEED)
    means = rng.choice(data, size=(iterations, len(data)), replace=True).mean(axis=1)
    return float(np.quantile(means, 0.025)), float(np.quantile(means, 0.975))


def legend_handles(published_label: str) -> list[Patch]:
    return [Patch(color=OURS, label="This work"), Patch(color=INK_MUTED, label=published_label)]


def temporal_controls() -> None:
    main = jsonl(RESULTS / "ever/main/results.jsonl")
    control = jsonl(RESULTS / "ever/budget_control/results.jsonl")
    unlinked = jsonl(RESULTS / "ever/unlinked_events_control/results.jsonl")
    keys = {row["qa_key"] for row in control}
    rows = [row for row in main if row["qa_key"] in keys] + control + unlinked
    conditions = [
        ("Raw retrieval, top-10", "RAW"),
        ("Raw retrieval, equal tokens", "RAW-token-matched"),
        ("Unlinked events, equal tokens", "RAW+EVENTS-token-matched"),
        ("Temporal episodes", "RAW+EPISODES"),
    ]
    labels, means, lows, highs = [], [], [], []
    for label, condition in conditions:
        values = [row["correct"] for row in rows if row["condition"] == condition]
        if len(values) != 300:
            raise RuntimeError(f"{condition}: expected 300 rows, found {len(values)}")
        low, high = bootstrap_ci(values)
        labels.append(label)
        means.append(100 * float(np.mean(values)))
        lows.append(100 * low)
        highs.append(100 * high)

    fig, ax = new_axes(5.0, 2.1, "x")
    y = np.arange(len(labels))[::-1]
    ax.barh(y, means, height=0.46, color=OURS, zorder=2)
    ax.errorbar(means, y, xerr=[np.subtract(means, lows), np.subtract(highs, means)], fmt="none",
                ecolor=INK_SECONDARY, elinewidth=0.9, capsize=2.2, zorder=3)
    for yi, value, high in zip(y, means, highs):
        ax.text(high + 0.7, yi, f"{one_decimal(value)}%", va="center", ha="left", color=INK, fontsize=8)
    ax.set_yticks(y, labels)
    ax.set_xlim(0, 32)
    ax.set_xlabel("Accuracy (%), 95% bootstrap CI", color=INK_SECONDARY)
    ax.set_title("EverMemBench Temporal Duration questions (n = 300)", loc="left", color=INK)
    save(fig, "temporal_controls")


def evermembench_leaderboard() -> None:
    rows = jsonl(RESULTS / "ever/main/results.jsonl")
    minors = list(PUBLISHED["evermembench"]["task_to_minor"].values())

    def macro(condition: str) -> float:
        return 100 * float(np.mean([
            np.mean([row["correct"] for row in rows if row["condition"] == condition and row["minor"] == minor])
            for minor in minors
        ]))

    entries = [(name, values["Average"], False) for name, values in PUBLISHED["evermembench"]["methods"].items()]
    entries += [("Raw retrieval (ours)", macro("RAW"), True),
                ("+ Temporal episodes (ours)", macro("RAW+EPISODES"), True)]
    entries.sort(key=lambda entry: entry[1])

    fig, ax = new_axes(5.0, 2.7, "x")
    y = np.arange(len(entries))
    ax.barh(y, [entry[1] for entry in entries], height=0.52,
            color=[OURS if entry[2] else INK_MUTED for entry in entries], zorder=2)
    for yi, (_name, value, _ours) in zip(y, entries):
        ax.text(value + 0.6, yi, one_decimal(value), va="center", ha="left", color=INK, fontsize=8)
    ax.set_yticks(y, [entry[0] for entry in entries])
    ax.set_xlim(0, 56)
    ax.set_xlabel("Macro accuracy over nine tasks (%)", color=INK_SECONDARY)
    ax.set_title("EverMemBench, answer model GPT-4.1-mini", loc="left", color=INK)
    ax.legend(handles=legend_handles("Published (Hu et al.)"), frameon=False, ncol=2,
              loc="upper left", bbox_to_anchor=(0.0, -0.22), labelcolor=INK_SECONDARY, fontsize=8)
    save(fig, "evermembench_leaderboard")


def groupmembench_cost_accuracy() -> None:
    published = PUBLISHED["groupmembench"]
    aggregates = json.loads((RESULTS / "group/aggregates.json").read_text())
    shared = aggregates["shared_five_categories"]
    counts = published["question_counts"]
    points = []
    for name, info in published["methods"].items():
        if info["ingestion_usd"] is None:
            continue
        correct = sum(round(info["accuracy_pct"][category] / 100 * counts[category]) for category in shared["categories"])
        points.append((name, info["ingestion_usd"], 100 * correct / shared["n"], False))
    average = aggregates["per_domain_average"]
    points += [
        ("Raw retrieval (ours)", average["ingestion_usd_raw"], 100 * shared["RAW_correct"] / shared["n"], True),
        ("+ Temporal episodes (ours)", average["ingestion_usd_episodes"],
         100 * shared["RAW+EPISODES_correct"] / shared["n"], True),
    ]

    fig, ax = new_axes(5.0, 3.0, "y")
    ax.grid(axis="x", color=GRID, linewidth=0.6)
    ax.set_xscale("log")
    ticks = [0.25, 0.5, 1, 2, 5, 10, 20, 50]
    ax.xaxis.set_major_locator(FixedLocator(ticks))
    ax.xaxis.set_minor_locator(NullLocator())
    ax.xaxis.set_major_formatter(FuncFormatter(lambda value, _pos: f"${value:g}"))
    for name, cost, accuracy, ours in points:
        ax.scatter(cost, accuracy, s=60, color=OURS if ours else INK_MUTED, edgecolor=SURFACE, linewidth=1.6, zorder=3)
        ax.annotate(name, (cost, accuracy), xytext=(6, 3), textcoords="offset points", fontsize=7.5, color=INK_SECONDARY)
    ax.set_xlim(0.15, 80)
    ax.set_ylim(8, 46)
    ax.set_xlabel("Memory ingestion cost per domain (USD, log scale)", color=INK_SECONDARY)
    ax.set_ylabel("Accuracy, 606 shared questions (%)", color=INK_SECONDARY)
    ax.set_title("GroupMemBench: accuracy versus ingestion cost (gpt-4o-mini ingestion)", loc="left", color=INK)
    ax.legend(handles=legend_handles("Published (Yang et al.)"), frameon=False, loc="upper left",
              labelcolor=INK_SECONDARY, fontsize=8)
    save(fig, "groupmembench_cost_accuracy")


def main() -> None:
    temporal_controls()
    evermembench_leaderboard()
    groupmembench_cost_accuracy()


if __name__ == "__main__":
    main()
