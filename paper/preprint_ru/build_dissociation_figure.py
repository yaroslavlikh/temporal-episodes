"""Dissociation figure: evidence delivery improves everywhere, accuracy does not follow.

Offline; reads the sealed evidence-endpoint JSON and the published slice table.
"""
from __future__ import annotations
import json, os
from pathlib import Path
os.environ.setdefault("MPLCONFIGDIR", "/private/tmp/event_memory_paper_mpl")
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
OUT = HERE / "figures"; OUT.mkdir(exist_ok=True)
BLUE, GREEN, INK, GRAY = "#315A87", "#16806A", "#182636", "#758190"
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 9.2,
    "axes.labelcolor": INK, "axes.titlecolor": INK, "text.color": INK,
    "xtick.color": INK, "ytick.color": INK,
    "axes.spines.top": False, "axes.spines.right": False, "pdf.fonttype": 42,
})

R = json.load(open("/Users/yaroslavlikh/summary_sov/research/figures/evidence_endpoint_results.json"))
CAT = R["ever"]["events_precision_by_category"]
NAME = {"C": "Constraint", "MH": "Multi-hop", "P": "Proactivity", "SH": "Single-hop",
        "Skill": "Skill", "Style": "Style", "TP": "Temporal Dur.", "Title": "Title", "U": "Update"}
# accuracy RAW -> EVENTS, appendix A of the manuscript
ACC = {"C": (79.9, 79.1), "MH": (12.9, 13.3), "P": (65.8, 64.6), "SH": (89.7, 89.7),
       "Skill": (33.7, 32.0), "Style": (30.1, 33.5), "TP": (12.3, 16.3),
       "Title": (46.4, 45.9), "U": (46.3, 47.0)}

fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.4, 3.9), gridspec_kw={"width_ratios": [1.05, 1]})

# ---- A: evidence precision delta with CIs, sorted
items = sorted(CAT.items(), key=lambda kv: kv[1]["delta_pp"])
ys = range(len(items))
for y, (c, v) in zip(ys, items):
    lo, hi = v["ci"]
    crosses = lo <= 0 <= hi
    col = GRAY if crosses else GREEN
    a1.plot([lo, hi], [y, y], color=col, lw=2.1, solid_capstyle="round", alpha=.55)
    a1.plot([v["delta_pp"]], [y], "o", color=col, ms=5.4, zorder=3)
a1.axvline(0, color=INK, lw=.9, alpha=.55)
a1.set_yticks(list(ys)); a1.set_yticklabels([f"{NAME[c]}  ($n{{=}}${v['n']})" for c, v in items], fontsize=8.4)
a1.set_xlabel("Δ evidence precision, п.п.  (EVENTS − RAW)")
a1.set_title("A · Доставка свидетельств: подтверждено везде", fontsize=9.6, loc="left", weight="bold")
a1.margins(y=.06)

# ---- B: dissociation scatter
for c, v in CAT.items():
    dx = v["delta_pp"]; dy = ACC[c][1] - ACC[c][0]
    disc = (c == "TP")
    a2.scatter([dx], [dy], s=58 if disc else 44,
               facecolor="white" if disc else (BLUE if dy >= 0 else "#B4553F"),
               edgecolor=BLUE if not disc else "#B4553F",
               linewidth=1.6 if disc else .6, zorder=3, alpha=.95)
    a2.annotate(NAME[c] + (" *" if disc else ""), (dx, dy), textcoords="offset points",
                xytext=(6, 4), fontsize=7.7, color=INK)
a2.axhline(0, color=INK, lw=.9, alpha=.55)
a2.axvline(0, color=INK, lw=.9, alpha=.3)
a2.set_xlabel("Δ evidence precision, п.п.")
a2.set_ylabel("Δ accuracy, п.п.")
a2.set_title("B · В ответ это не переходит", fontsize=9.6, loc="left", weight="bold")
a2.text(.98, .10, r"precision: $\rho=+0{,}63$  ($p=.07$)", transform=a2.transAxes,
        ha="right", fontsize=8.4, color=GRAY)
a2.text(.98, .03, r"F1: $\rho=-0{,}07$   —  ни одна не значима", transform=a2.transAxes,
        ha="right", fontsize=8.4, color=GRAY)
a2.set_xlim(-0.6, 9.6)

fig.text(.005, -.045,
         "Слева: парная разница по 2400 вопросам, question bootstrap 95% ДИ; серым — единственная категория, "
         "чей интервал накрывает ноль.\nСправа: та же ось X против сдвига accuracy. "
         "Категория с наибольшим приростом доставки (Single-hop) стоит у потолка accuracy и не выигрывает.",
         fontsize=7.6, color=GRAY, va="top")
fig.tight_layout()
fig.savefig(OUT / "dissociation.pdf", bbox_inches="tight", facecolor="white")
fig.savefig(OUT / "dissociation.png", dpi=220, bbox_inches="tight", facecolor="white")
print("wrote figures/dissociation.{pdf,png}")
