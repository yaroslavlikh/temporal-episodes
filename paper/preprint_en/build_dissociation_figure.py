"""Evidence delivery and accuracy: measured changes, without causal bottleneck claims.

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
    "font.family": "DejaVu Sans", "font.size": 10.2,
    "axes.labelcolor": INK, "axes.titlecolor": INK, "text.color": INK,
    "xtick.color": INK, "ytick.color": INK,
    "axes.spines.top": False, "axes.spines.right": False, "pdf.fonttype": 42,
})

R = json.load(open("/Users/yaroslavlikh/summary_sov/research/figures/evidence_endpoint_results.json"))
CAT = R["ever"]["events_precision_by_category"]
NAME = {"C": "Constraint", "MH": "Multi-hop", "P": "Proactivity", "SH": "Single-hop",
        "Skill": "Skill", "Style": "Style", "TP": "Temporal Dur.", "Title": "Title", "U": "Update"}
# Use unrounded per-category accuracy from the read-only editorial verifier.
verified = json.loads((HERE / "editorial_verification.json").read_text())
ACC = {c: (100 * row['RAW'], 100 * row['EVENTS'])
       for c, row in verified['accuracy_by_category'].items()}

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
a1.set_yticks(list(ys)); a1.set_yticklabels([f"{NAME[c]}  ($n{{=}}${v['n']})" for c, v in items], fontsize=9.4)
a1.set_xlabel("Δ evidence precision, pp  (EVENTS − RAW)")
a1.set_title("A · Precision gain by category", fontsize=10.4, loc="left", weight="bold")
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
                xytext={"C": (-7, -3), "MH": (6, -11)}.get(c, (6, 4)), ha="right" if c == "C" else "left",
                fontsize=8.8, color=INK)
a2.axhline(0, color=INK, lw=.9, alpha=.55)
a2.axvline(0, color=INK, lw=.9, alpha=.3)
a2.set_xlabel("Δ evidence precision, pp")
a2.set_ylabel("Δ accuracy, pp")
a2.set_title("B · The accuracy gain is heterogeneous", fontsize=10.4, loc="left", weight="bold")
a2.set_xlim(-3.2, 9.6)

fig.tight_layout()
fig.savefig(OUT / "dissociation.pdf", bbox_inches="tight", facecolor="white")
fig.savefig(OUT / "dissociation.png", dpi=220, bbox_inches="tight", facecolor="white")
print("wrote figures/dissociation.{pdf,png}")
