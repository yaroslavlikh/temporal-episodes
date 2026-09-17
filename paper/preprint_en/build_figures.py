"""Rebuild every paper figure from sealed research artifacts; no API calls."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/private/tmp/event_memory_paper_mpl")

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE / "figures"
OUT.mkdir(exist_ok=True)

BLUE = "#315A87"
GREEN = "#16806A"
MINT = "#EAF5F1"
PALE_BLUE = "#EDF3F8"
INK = "#182636"
GRAY = "#758190"
LIGHT = "#EEF1F4"

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 9.2,
    "axes.labelcolor": INK, "axes.titlecolor": INK, "text.color": INK,
    "xtick.color": INK, "ytick.color": INK,
    "axes.spines.top": False, "axes.spines.right": False,
    "pdf.fonttype": 42, "svg.fonttype": "none",
})


def save(fig: plt.Figure, name: str) -> None:
    fig.savefig(OUT / f"{name}.pdf", bbox_inches="tight", facecolor="white")
    fig.savefig(OUT / f"{name}.png", dpi=220, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def rounded(ax, xy, w, h, text, *, fc=PALE_BLUE, ec=BLUE, fs=9, weight="normal"):
    x, y = xy
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.045,rounding_size=.08",
        facecolor=fc, edgecolor=ec, linewidth=1.15,
    ))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fs, weight=weight, linespacing=1.25)


def arrow(ax, start, end, *, color=GRAY, label=None, curve=0.0, ls="-"):
    ax.add_patch(FancyArrowPatch(
        start, end, arrowstyle="-|>", mutation_scale=11, linewidth=1.05,
        color=color, linestyle=ls, connectionstyle=f"arc3,rad={curve}",
    ))
    if label:
        mx, my = (start[0] + end[0]) / 2, (start[1] + end[1]) / 2
        ax.text(mx, my + .12, label, ha="center", va="bottom", fontsize=7.8, color=color)


# Figure 1: motivation / teaser.
fig, ax = plt.subplots(figsize=(10.5, 3.4))
ax.set(xlim=(0, 10.5), ylim=(0, 3.4)); ax.axis("off")
ax.text(.15, 3.12, "RETRIEVAL ABSTRACTION AND VERIFIABLE SOURCE", fontsize=10.5,
        color=BLUE, weight="bold")
rounded(ax, (.15, 1.72), 2.45, .92, "Day 1 · Alexey\n“I will be at the meeting”", fc="#F4F6F8", ec=GRAY)
rounded(ax, (3.05, 1.72), 2.45, .92, "Day 18 · Alexey\n“I am leaving; I won’t\ncome to the meeting”", fc="#F4F6F8", ec=GRAY)
rounded(ax, (7.48, 1.72), 2.75, .92, "Late question\n“Will Alexey be there?”", fc=MINT, ec=GREEN, weight="bold")
arrow(ax, (2.6, 2.18), (3.05, 2.18)); arrow(ax, (5.5, 2.18), (7.48, 2.18), label="lexical gap", curve=-.08)
rounded(ax, (1.2, .28), 3.2, .76, "EVENT FOR RETRIEVAL\nattendance plan → cancelled", fc=PALE_BLUE, ec=BLUE)
rounded(ax, (6.05, .28), 3.2, .76, "SOURCES FOR THE ANSWER\nauthor · time · verbatim quote", fc=MINT, ec=GREEN)
arrow(ax, (4.4, .66), (6.05, .66), color=GREEN, label="provenance expansion")
arrow(ax, (8.85, 1.72), (7.65, 1.04), color=GREEN, curve=.18)
ax.text(.15, .02, "Derived text helps find the meaning; raw messages remain the evidence.", fontsize=9.2, color=GRAY)
save(fig, "concept")


# Figure 2: ingestion, reverse linking lane, retrieval, explicit index branches.
fig, ax = plt.subplots(figsize=(10.7, 7.0))
ax.set(xlim=(0, 10.7), ylim=(0, 7)); ax.axis("off")
GOLD = "#A57935"
ax.text(.15, 6.72, "A · MEMORY CONSTRUCTION BEFORE ANY QUESTION IS READ", fontsize=10.2, color=BLUE, weight="bold")
xs = [.15, 2.8, 5.45, 8.1]
texts = ["Raw store\nID · author · time · text", "Session → extraction\n0–2 events per turn",
         "Evidence validation\nID + verbatim quote", "Immutable events\ndescription + source pointers"]
for x, text in zip(xs, texts):
    rounded(ax, (x, 5.77), 2.3, .7, text, fs=8.4, fc="#F4F6F8" if x == xs[0] else PALE_BLUE)
for i in range(3):
    arrow(ax, (xs[i]+2.3, 6.12), (xs[i+1], 6.12))
ax.text(.15, 5.40, "B · OPTIONAL LINKING · PROCESSED IN TIME ORDER", fontsize=10.2, color=GOLD, weight="bold")
texts = ["Episode: append-only\nhot: last 5 events\ncold: all source pointers",
         "LLM resolver\nNEW / REVISE /\nREAFFIRM / AUGMENT",
         "Episode search · top-k = 3\n0.6 · hot + 0.4 · last\nfilter: conversation network",
         "New event\nlocal MiniLM\nembedding"]
for x, text in zip(xs, texts):
    rounded(ax, (x, 4.27), 2.3, .82, text, fc="#FBF8F2", ec=GOLD, fs=7.8)
arrow(ax, (9.25, 5.77), (9.25, 5.09), color=GOLD)
for i in (3, 2, 1):
    arrow(ax, (xs[i], 4.68), (xs[i-1]+2.3, 4.68), color=GOLD)
ax.text(3.94, 4.01, "empty pool / invalid choice / confidence < 0.5 → NEW", fontsize=7.8, color=GOLD, ha="center")

ax.text(.15, 3.61, "C · SHARED INDEX AND RETURN TO PRIMARY MESSAGES", fontsize=10.2, color=GREEN, weight="bold")
rounded(ax, (.15, 2.62), 2.3, .65, "RAW index\noriginal text", fc="#F4F6F8", ec=GRAY, fs=8.2)
rounded(ax, (2.8, 2.62), 2.3, .65, "EVENTS index\nself-contained description", fs=8.2)
rounded(ax, (5.45, 2.62), 2.3, .65, "EPISODES index\nhot-view description", fc="#FBF8F2", ec=GOLD, fs=8.2)
ax.text(8.24, 2.96, "Condition:\nRAW / RAW+EVENTS /\nRAW+EPISODES", fontsize=8.1, ha="left", va="center", color=GRAY)

rounded(ax, (.15, 1.30), 2.3, .73, "Question → embedding\nbenchmark adapter", fc=MINT, ec=GREEN, fs=8.4)
rounded(ax, (2.8, 1.30), 2.3, .73, "Single ranked pool\ncosine · top-k = 10", fc=MINT, ec=GREEN, fs=8.4, weight="bold")
rounded(ax, (5.45, 1.30), 2.3, .73, "Provenance expansion\nderived hit → raw sources\nsource ID deduplication", fc=MINT, ec=GREEN, fs=8.0)
rounded(ax, (8.1, 1.30), 2.3, .73, "Generator context\nderived + sources\nauthor · time · text", fc=MINT, ec=GREEN, fs=8.0)
for i in range(3):
    arrow(ax, (xs[i]+2.3, 1.665), (xs[i+1], 1.665), color=GREEN)
arrow(ax, (1.30, 2.62), (3.04, 2.03), color=GRAY, ls=":")
arrow(ax, (3.95, 2.62), (3.95, 2.03), color=BLUE, ls=":")
arrow(ax, (6.60, 2.62), (4.83, 2.03), color=GOLD, ls=":")
# Evidence is read from the preserved original store, not from rewritten descriptions.
ax.plot([.15, .04, .04, 6.6, 6.6], [6.12, 6.12, .76, .76, 1.25], color=GRAY, ls=":", lw=.9)
arrow(ax, (6.6, 1.05), (6.6, 1.30), color=GRAY, ls=":")
ax.text(3.7, .48, "Raw store → original messages at immutable addresses", fontsize=8.1, color=GRAY, ha="center")
ax.text(.15, .09, "INVARIANT · the description may change; the primary history and the evidence address are preserved.", fontsize=9.1, color=INK, weight="bold")
save(fig, "architecture")


# Figure 3: EverMemBench system-level comparison (reported rows).
systems = ["EPISODES (ours)", "RAW (ours)", "MemOS", "Zep", "Full Context", "Mem0", "MemoBase"]
scores = [47.16, 46.34, 42.55, 39.97, 37.44, 37.09, 34.27]
colors = [GREEN, BLUE] + [GRAY] * 5
fig, ax = plt.subplots(figsize=(10.4, 4.3)); y = np.arange(len(systems))
ax.barh(y, scores, color=colors, height=.62)
for i, value in enumerate(scores): ax.text(value + .35, i, f"{value:.2f}%", va="center", weight="bold" if i < 2 else "normal")
ax.set(yticks=y, yticklabels=systems, xlim=(0, 52), xlabel="Macro accuracy over 9 question types, %")
ax.invert_yaxis(); ax.grid(axis="x", color=LIGHT, linewidth=.8); ax.set_axisbelow(True)
ax.set_title("EverMemBench · our adapter results and published systems", loc="left", weight="bold")
fig.subplots_adjust(left=.22, bottom=.14, right=.94, top=.88); save(fig, "ever_leaderboard")


# Figure 4: temporal mechanism controls.
labels = ["RAW · top-10", "HyDE-RAW · top-10", "RAW · matched tokens", "RAW · matched + chrono", "HyDE-RAW · matched + chrono", "EVENTS · matched tokens", "EVENTS · matched + chrono", "EPISODES · ranked", "EPISODES · chrono"]
accuracy = [12.33, 12.00, 12.33, 14.00, 14.00, 17.00, 19.33, 20.00, 18.33]
fig, axes = plt.subplots(1, 2, figsize=(10.7, 4.35), gridspec_kw={"width_ratios": [1.35, 1]})
y = np.arange(len(labels)); bar_colors = [GRAY, "#8E77A8", GRAY, BLUE, "#8E77A8", GREEN, GREEN, "#A57935", "#A57935"]
axes[0].barh(y, accuracy, color=bar_colors, height=.61)
for i, v in enumerate(accuracy): axes[0].text(v + .25, i, f"{v:.1f}", va="center", fontsize=8.6)
axes[0].set(yticks=y, yticklabels=labels, xlim=(0, 23), xlabel="Accuracy, %"); axes[0].invert_yaxis(); axes[0].grid(axis="x", color=LIGHT); axes[0].set_axisbelow(True)
axes[0].set_title("A · Temporal Duration (n = 300)", loc="left", weight="bold")
names = ["EVENTS chrono − RAW chrono", "EVENTS chrono − HyDE chrono", "EPISODES chrono − RAW chrono", "EPISODES chrono − EVENTS chrono"]
deltas = [5.33, 5.33, 4.33, -1.00]; intervals = [(0.67, 10.00), (0.33, 10.33), (0.00, 9.00), (-5.00, 3.33)]
for i, (v, (lo, hi)) in enumerate(zip(deltas, intervals)):
    axes[1].errorbar(v, i, xerr=[[v-lo], [hi-v]], fmt="o", markersize=6, color=GREEN if i < 2 else GRAY, capsize=4, linewidth=1.4)
axes[1].axvline(0, color=INK, ls="--", lw=.8); axes[1].set(yticks=np.arange(4), yticklabels=names, xlim=(-6, 11), xlabel="Paired difference, pp (95% CI)")
axes[1].invert_yaxis(); axes[1].grid(axis="x", color=LIGHT); axes[1].set_axisbelow(True); axes[1].set_title("B · What remains after the controls", loc="left", weight="bold")
fig.tight_layout(w_pad=2.5); save(fig, "temporal_controls")


# Figure 5: transfer across benchmarks, as paired within-benchmark deltas.
rows = [
    ("EverMemBench · 2 400 QA", 0.75, (-0.50, 2.00)),
    ("SocialMemBench · 1 031 QA", 1.00, (-0.80, 2.80)),
    ("GroupMemBench · 745 QA", -1.61, (-4.00, 0.80)),
    ("GroupMemBench · registered primary, n = 150", -4.00, (-9.30, 1.30)),
]
fig, ax = plt.subplots(figsize=(9.8, 3.6))
for i, (_, v, (lo, hi)) in enumerate(rows):
    ax.errorbar(v, i, xerr=[[v - lo], [hi - v]], fmt="o", markersize=6,
                color=GREEN if v > 0 else BLUE, capsize=4, linewidth=1.4)
    ax.text(hi + .35, i, f"{v:+.2f}", va="center", fontsize=8.8, color=GRAY)
ax.axvline(0, color=INK, ls="--", lw=.8)
ax.set(yticks=np.arange(len(rows)), yticklabels=[r[0] for r in rows], xlim=(-10.5, 4.5),
       xlabel="Paired difference RAW+EPISODES − RAW, pp (95% CI)")
ax.invert_yaxis(); ax.grid(axis="x", color=LIGHT); ax.set_axisbelow(True)
ax.set_title("Added effect of episodes: transfer across benchmarks", loc="left", weight="bold")
ax.text(.02, -0.30, "Paired comparisons within each dataset. Models and metrics differ;\nrows show the added effect, not the absolute level of the systems.", transform=ax.transAxes, fontsize=8.0, color=GRAY)
fig.subplots_adjust(bottom=.28, left=.30, right=.97, top=.88); save(fig, "transfer")


# Figure 6: GroupMemBench quality/cost/storage trade-off on common 606 QA.
names = ["Hindsight", "HippoRAG", "A-Mem", "Mem0", "GraphRAG", "MemGPT", "RAW (ours)", "EPISODES (ours)"]
acc = np.array([40.4, 33.3, 29.2, 15.5, 12.2, 19.1, 34.7, 32.3]); cost = np.array([32.10, 8.64, 26.13, 18.41, 12.51, .43, .23, 1.92]); storage = np.array([4.25, 5.76, 6.60, .99, 3.00, .69, .37, .41])
fig, ax = plt.subplots(figsize=(10.4, 4.65)); ours = np.array([False]*6 + [True, True]); size = 90 + storage * 55
ax.scatter(cost[~ours], acc[~ours], s=size[~ours], color=GRAY, alpha=.72, edgecolor="white", linewidth=.8); ax.scatter(cost[ours], acc[ours], s=size[ours], color=[BLUE, GREEN], alpha=.95, edgecolor="white", linewidth=1)
offsets = {"Hindsight":(-5.2,-.4),"HippoRAG":(-1.6,2.2),"A-Mem":(-4.3,-.4),"Mem0":(-1.0,1.0),"GraphRAG":(-1.8,-2.0),"MemGPT":(-.3,1.2),"RAW (ours)":(.5,1.1),"EPISODES (ours)":(.4,-2.6)}
for n, xx, yy in zip(names, cost, acc):
    dx, dy = offsets[n]; ax.text(xx+dx, yy+dy, n, fontsize=9.4, weight="bold" if "ours" in n else "normal")
ax.set(xlabel="Memory construction cost, $ per domain", ylabel="Accuracy on 606 non-abstention QA, %", xlim=(-1.2,35.5), ylim=(7,45)); ax.grid(color=LIGHT); ax.set_axisbelow(True)
ax.set_title("GroupMemBench · quality, construction cost and storage size", loc="left", weight="bold")
ax.text(.02,.02,"Point size ∝ reported storage. Descriptive comparison: harnesses and models differ.", transform=ax.transAxes, fontsize=9.2, color=GRAY)
save(fig, "efficiency")


sources = [
    ROOT / ".research_runs/frozen/final_sprint_A_events_full_v1_20260915_233142_MSK/run/summary.json",
    ROOT / ".research_runs/frozen/final_sprint_B2_episodes_chrono_v1_20260915_232910_MSK/run/summary.json",
    ROOT / ".research_runs/frozen/final_sprint_C_hyde_raw_v1_20260916_024144_MSK/run/summary.json",
    ROOT / ".research_runs/frozen/final_sprint_C2_hyde_token_matched_v1_20260916_024306_MSK/run/summary.json",
    ROOT / ".research_runs/evermembench_temporal_episodes_official_v1/report.md",
    ROOT / ".research_runs/groupmembench_temporal_episodes_official_v1/report.md",
    ROOT / ".research_runs/final_sprint_D_groupmembench_repair_v2/report.md",
    ROOT / ".research_runs/final_sprint_D_groupmembench_repair_v2/results_v2_meta.json",
    ROOT / ".research_runs/socialmembench_temporal_episodes_official_harness_v1/report.md",
]
manifest = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
(HERE / "figure_sources.json").write_text(json.dumps(manifest, indent=2) + "\n")
print("Generated six publication figures from sealed/local reports.")
