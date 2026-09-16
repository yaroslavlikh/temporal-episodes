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
ax.text(.15, 3.12, "ПОЧЕМУ СЫРЫХ СООБЩЕНИЙ НЕДОСТАТОЧНО", fontsize=10.5,
        color=BLUE, weight="bold")
rounded(ax, (.15, 1.72), 2.45, .92, "День 1 · Алексей\n«Я буду на встрече»", fc="#F4F6F8", ec=GRAY)
rounded(ax, (3.05, 1.72), 2.45, .92, "День 18 · Алексей\n«Уезжаю из города»", fc="#F4F6F8", ec=GRAY)
rounded(ax, (7.48, 1.72), 2.75, .92, "Поздний вопрос\n«Будет ли Алексей?»", fc=MINT, ec=GREEN, weight="bold")
arrow(ax, (2.6, 2.18), (3.05, 2.18)); arrow(ax, (5.5, 2.18), (7.48, 2.18), label="лексический разрыв", curve=-.08)
rounded(ax, (1.2, .28), 3.2, .76, "СОБЫТИЕ ДЛЯ ПОИСКА\nплан участия → отменён отъездом", fc=PALE_BLUE, ec=BLUE)
rounded(ax, (6.05, .28), 3.2, .76, "ИСТОЧНИКИ ДЛЯ ОТВЕТА\nавтор · время · дословная цитата", fc=MINT, ec=GREEN)
arrow(ax, (4.4, .66), (6.05, .66), color=GREEN, label="provenance expansion")
arrow(ax, (8.85, 1.72), (7.65, 1.04), color=GREEN, curve=.18)
ax.text(.15, .02, "Derived-текст помогает найти смысл; raw-реплики остаются доказательством.", fontsize=9.2, color=GRAY)
save(fig, "concept")


# Figure 2: complete architecture, arranged as three non-crossing lanes.
fig, ax = plt.subplots(figsize=(10.7, 6.15))
ax.set(xlim=(0, 10.7), ylim=(0, 6.15)); ax.axis("off")
ax.text(.15, 5.88, "A · QUERY-INDEPENDENT INGESTION", fontsize=10.4, color=BLUE, weight="bold")
xs = [.15, 2.25, 4.35, 6.45, 8.55]
texts = ["Raw turns\nID · speaker · time", "Bounded sessions\nby day / group", "Forced extraction\n0–2 events per turn", "Span validation\nID + literal quote", "Immutable events\nindex text + evidence"]
for i, (x, t) in enumerate(zip(xs, texts)):
    rounded(ax, (x, 4.85), 1.75, .72, t, fc="#F4F6F8" if i == 0 else PALE_BLUE, ec=GRAY if i == 0 else BLUE, fs=8.5)
for i in range(4): arrow(ax, (xs[i]+1.75,5.21), (xs[i+1],5.21))

ax.text(.15, 4.48, "B · OPTIONAL TEMPORAL LINKING", fontsize=10.4, color="#A57935", weight="bold")
rounded(ax, (.15, 3.47), 2.25, .72, "New event\nembedding", fc="#FBF8F2", ec="#A57935", fs=8.5)
rounded(ax, (2.83, 3.47), 2.25, .72, "Candidate retrieval\nsemantic top-k = 3", fc="#FBF8F2", ec="#A57935", fs=8.5)
rounded(ax, (5.51, 3.47), 2.25, .72, "LLM resolver\nNEW · REVISE · REAFFIRM · AUGMENT", fc="#FBF8F2", ec="#A57935", fs=6.9)
rounded(ax, (8.19, 3.47), 2.25, .72, "Episode view\nhot = last 5 · cold = all evidence", fc="#FBF8F2", ec="#A57935", fs=7.4)
for a,b in [((2.40,3.83),(2.83,3.83)),((5.08,3.83),(5.51,3.83)),((7.76,3.83),(8.19,3.83))]: arrow(ax,a,b,color="#A57935")
arrow(ax,(9.42,4.85),(9.42,4.19),color="#A57935",ls=":")

ax.text(.15, 3.05, "C · UNIFIED RETRIEVAL + PROVENANCE EXPANSION", fontsize=10.4, color=GREEN, weight="bold")
rounded(ax, (.15, 1.93), 1.55, .76, "Question\nembedding", fc=MINT, ec=GREEN, fs=8.6)
rounded(ax, (2.02, 1.93), 2.18, .76, "One ranked pool\nRAW + EVENTS / EPISODES", fc=MINT, ec=GREEN, fs=7.3, weight="bold")
rounded(ax, (4.52, 1.93), 1.55, .76, "Cosine\ntop-k = 10", fc=MINT, ec=GREEN, fs=8.6)
rounded(ax, (6.39, 1.93), 1.78, .76, "Expand derived hits\n→ unique raw IDs", fc=MINT, ec=GREEN, fs=8.2)
rounded(ax, (8.49, 1.93), 1.95, .76, "Generator context\nderived + dated evidence", fc=MINT, ec=GREEN, fs=8.2)
for a,b in [((1.70,2.31),(2.02,2.31)),((4.20,2.31),(4.52,2.31)),((6.07,2.31),(6.39,2.31)),((8.17,2.31),(8.49,2.31))]: arrow(ax,a,b,color=GREEN)

rounded(ax, (.15, .62), 2.48, .60, "Append-only raw store\noriginal text never replaced", fc="#F4F6F8", ec=GRAY, fs=8.2)
rounded(ax, (3.22, .62), 2.48, .60, "Event index\nsearchable semantic abstraction", fc=PALE_BLUE, ec=BLUE, fs=8.2)
rounded(ax, (6.29, .62), 4.15, .60, "Returned evidence\nsource ID · speaker · timestamp · literal quote", fc=MINT, ec=GREEN, fs=8.2)
arrow(ax,(1.40,1.22),(2.35,1.93),color=GRAY,ls=":",curve=-.12)
arrow(ax,(4.46,1.22),(3.92,1.93),color=BLUE,ls=":",curve=.10)
arrow(ax,(7.29,1.93),(7.29,1.22),color=GREEN,ls=":")
ax.text(.15, .20, "ИНВАРИАНТ · derived representation помогает найти смысл; raw evidence остаётся адресуемым и неизменным.", fontsize=9.1, color=INK, weight="bold")
save(fig, "architecture")


# Figure 3: EverMemBench system-level comparison (reported rows).
systems = ["Temporal Episodes\n(ours)", "RAW (ours)", "MemOS", "Zep", "Full Context", "Mem0", "MemoBase"]
scores = [47.16, 46.34, 42.55, 39.97, 37.44, 37.09, 34.27]
colors = [GREEN, BLUE] + [GRAY] * 5
fig, ax = plt.subplots(figsize=(10.4, 4.3)); y = np.arange(len(systems))
ax.barh(y, scores, color=colors, height=.62)
for i, value in enumerate(scores): ax.text(value + .35, i, f"{value:.2f}%", va="center", weight="bold" if i < 2 else "normal")
ax.set(yticks=y, yticklabels=systems, xlim=(30, 50), xlabel="Macro accuracy по 9 типам вопросов, %")
ax.invert_yaxis(); ax.grid(axis="x", color=LIGHT, linewidth=.8); ax.set_axisbelow(True)
ax.set_title("EverMemBench · полная система в официальном evaluation harness", loc="left", weight="bold")
fig.subplots_adjust(left=.22, bottom=.14, right=.94, top=.88); save(fig, "ever_leaderboard")


# Figure 4: temporal mechanism controls.
labels = ["RAW · top-10", "HyDE-RAW · top-10", "RAW · matched tokens", "RAW · matched + chrono", "HyDE-RAW · matched + chrono", "EVENTS · matched tokens", "EVENTS · matched + chrono", "EPISODES · ranked", "EPISODES · chrono"]
accuracy = [12.33, 12.00, 12.33, 14.00, 14.00, 17.00, 19.33, 20.00, 18.33]
fig, axes = plt.subplots(1, 2, figsize=(10.7, 4.35), gridspec_kw={"width_ratios": [1.35, 1]})
y = np.arange(len(labels)); bar_colors = [GRAY, "#8E77A8", GRAY, BLUE, "#8E77A8", GREEN, GREEN, "#A57935", "#A57935"]
axes[0].barh(y, accuracy, color=bar_colors, height=.61)
for i, v in enumerate(accuracy): axes[0].text(v + .25, i, f"{v:.1f}", va="center", fontsize=8.6)
axes[0].set(yticks=y, yticklabels=labels, xlim=(8, 22), xlabel="Accuracy, %"); axes[0].invert_yaxis(); axes[0].grid(axis="x", color=LIGHT); axes[0].set_axisbelow(True)
axes[0].set_title("A · Temporal Duration (n = 300)", loc="left", weight="bold")
names = ["EVENTS chrono − RAW chrono", "EVENTS chrono − HyDE chrono", "EPISODES chrono − RAW chrono", "EPISODES chrono − EVENTS chrono"]
deltas = [5.33, 5.33, 4.33, -1.00]; intervals = [(0.67, 10.00), (0.33, 10.33), (0.00, 9.00), (-5.00, 3.33)]
for i, (v, (lo, hi)) in enumerate(zip(deltas, intervals)):
    axes[1].errorbar(v, i, xerr=[[v-lo], [hi-v]], fmt="o", markersize=6, color=GREEN if i < 2 else GRAY, capsize=4, linewidth=1.4)
axes[1].axvline(0, color=INK, ls="--", lw=.8); axes[1].set(yticks=np.arange(4), yticklabels=names, xlim=(-6, 11), xlabel="Парная разница, п.п. (95% ДИ)")
axes[1].invert_yaxis(); axes[1].grid(axis="x", color=LIGHT); axes[1].set_axisbelow(True); axes[1].set_title("B · Что остаётся после контролей", loc="left", weight="bold")
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
       xlabel="Парная разница RAW+EPISODES − RAW, п.п. (95% ДИ)")
ax.invert_yaxis(); ax.grid(axis="x", color=LIGHT); ax.set_axisbelow(True)
ax.set_title("Перенос неоднороден, и ни один интервал не исключает ноль", loc="left", weight="bold")
ax.text(.02, -0.30, "Каждая строка — парное сравнение внутри своего бенчмарка; метрика (accuracy / MeanQ) и модели различаются, поэтому строки не сопоставимы между собой по уровню.", transform=ax.transAxes, fontsize=8.0, color=GRAY)
fig.subplots_adjust(bottom=.28, left=.30, right=.97, top=.88); save(fig, "transfer")


# Figure 6: GroupMemBench quality/cost/storage trade-off on common 606 QA.
names = ["Hindsight", "HippoRAG", "A-Mem", "Mem0", "GraphRAG", "MemGPT", "RAW (ours)", "Episodes (ours)"]
acc = np.array([40.4, 33.3, 29.2, 15.5, 12.2, 19.1, 34.7, 32.3]); cost = np.array([32.10, 8.64, 26.13, 18.41, 12.51, .43, .23, 1.92]); storage = np.array([4.25, 5.76, 6.60, .99, 3.00, .69, .37, .41])
fig, ax = plt.subplots(figsize=(10.4, 4.65)); ours = np.array([False]*6 + [True, True]); size = 90 + storage * 55
ax.scatter(cost[~ours], acc[~ours], s=size[~ours], color=GRAY, alpha=.72, edgecolor="white", linewidth=.8); ax.scatter(cost[ours], acc[ours], s=size[ours], color=[BLUE, GREEN], alpha=.95, edgecolor="white", linewidth=1)
offsets = {"Hindsight":(-2.8,1.1),"HippoRAG":(-1.5,-2.1),"A-Mem":(-1.5,1.1),"Mem0":(-1.0,1.0),"GraphRAG":(-1.8,-2.0),"MemGPT":(-.3,1.2),"RAW (ours)":(.5,1.1),"Episodes (ours)":(.7,-2.0)}
for n, xx, yy in zip(names, cost, acc):
    dx, dy = offsets[n]; ax.text(xx+dx, yy+dy, n, fontsize=8.3, weight="bold" if "ours" in n else "normal")
ax.set(xlabel="Ingestion cost, USD per domain", ylabel="Accuracy on common 606 QA, %", xlim=(-1.2,35.5), ylim=(7,45)); ax.grid(color=LIGHT); ax.set_axisbelow(True)
ax.set_title("GroupMemBench · качество, цена построения и объём хранилища", loc="left", weight="bold")
ax.text(.02,.02,"Размер точки ∝ reported storage. Сравнение описательное: harness и модели систем различаются.", transform=ax.transAxes, fontsize=8.4, color=GRAY)
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
