"""Verify the k-sweep (retrieval depth k = 10 / 20 / 40), offline.

Phase 1 recomputes evidence delivery at each k from results/ever/ksweep/per_question.jsonl and
checks that its k=10 rows agree with the sealed per-question metrics of the main runs.
Phase 2 recomputes accuracy on the stratified sample (N = 304): k=10 verdicts come from the
sealed main runs, k=20 verdicts from results/ever/ksweep/phase2/results.jsonl. No API calls.

    python3 analysis/verify_ksweep.py

Exit code 0 means every recomputed value matched the reports within tolerance.
"""
from __future__ import annotations

import collections
import hashlib
import json
import pathlib
import statistics
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
RESULTS = REPO / "results"
KS = RESULTS / "ever" / "ksweep"
OUT = REPO / "analysis" / "output" / "ksweep.json"

failures: list[str] = []
checks = 0


def rows(path: pathlib.Path):
    for line in path.open():
        yield json.loads(line)


def check(label: str, got: float, want: float, tol: float = 0.005) -> None:
    global checks
    checks += 1
    if abs(got - want) > tol:
        failures.append(f"{label}: recomputed {got:.4f}, report {want:.4f}")
    print(f"  {'ok ' if abs(got - want) <= tol else 'FAIL'} {label:52s} {got:+9.3f}  (report {want:+.3f})")


def claim(label: str, ok: bool) -> None:
    global checks
    checks += 1
    if not ok:
        failures.append(label)
    print(f"  {'ok ' if ok else 'FAIL'} {label}")


res: dict = {}

# ------------------------------------------------------------ phase 1: delivery
print("phase 1: evidence delivery, EverMemBench, 2,400 questions")
pq = collections.defaultdict(dict)
for r in rows(KS / "per_question.jsonl"):
    pq[(r["k"], r["condition"])][r["qa_key"]] = r
claim("14,400 rows: 2,400 questions x 3 k x 2 conditions",
      sum(len(v) for v in pq.values()) == 14400 and all(len(v) == 2400 for v in pq.values()))

report = json.loads((KS / "summary.json").read_text())
res["means"] = {}
for k in (10, 20, 40):
    R, E = pq[(k, "RAW")], pq[(k, "RAW+EVENTS")]
    for cond, D in (("RAW", R), ("RAW+EVENTS", E)):
        m = {f: statistics.mean(r[f] for r in D.values()) for f in ("precision", "recall", "gold_hits", "sources")}
        m["precision"] *= 100
        m["recall"] *= 100
        res["means"][f"{cond}@{k}"] = m
        for f in ("precision", "recall", "gold_hits", "sources"):
            check(f"k={k} {cond} mean {f}", m[f], report["means"][str(k)][cond][f], tol=1e-6)
    ks = sorted(R)
    dp = 100 * statistics.mean(E[q]["precision"] - R[q]["precision"] for q in ks)
    dg = statistics.mean(E[q]["gold_hits"] - R[q]["gold_hits"] for q in ks)
    res[f"delta@{k}"] = dict(precision_pp=dp, gold_hits=dg)
    claim(f"k={k}: events never deliver more sources than raw",
          all(E[q]["sources"] <= R[q]["sources"] for q in ks))
    by_project = collections.defaultdict(list)
    for q in ks:
        by_project[R[q]["topic"]].append(E[q]["precision"] - R[q]["precision"])
    claim(f"k={k}: precision gain positive in all five projects",
          len(by_project) == 5 and all(statistics.mean(v) > 0 for v in by_project.values()))
check("k=10 precision delta, pp", res["delta@10"]["precision_pp"], 3.21)
check("k=20 precision delta, pp", res["delta@20"]["precision_pp"], 2.51)
check("k=40 precision delta, pp", res["delta@40"]["precision_pp"], 1.68)
check("k=10 gold hits delta", res["delta@10"]["gold_hits"], 0.117, tol=0.0005)

# k=10 must reproduce the sealed per-question metrics of the main runs
sealed = {"RAW": {r["qa_key"]: r for r in rows(RESULTS / "ever/main/results.jsonl") if r["condition"] == "RAW"},
          "RAW+EVENTS": {r["qa_key"]: r for r in rows(RESULTS / "ever/events_full/results.jsonl")
                         if r["condition"] == "RAW+EVENTS"}}
for cond, S in sealed.items():
    mism = sum(1 for q, r in pq[(10, cond)].items()
               if abs(r["precision"] - S[q]["evidence_precision"]) > 1e-9
               or abs(r["recall"] - S[q]["evidence_recall"]) > 1e-9)
    claim(f"k=10 {cond} matches the sealed run on all 2,400 questions ({mism} mismatches)", mism == 0)

# ------------------------------------------------------------ phase 2: accuracy
print("phase 2: accuracy on the stratified sample")
manifest = json.loads((KS / "phase2/manifest.json").read_text())
order_text = (KS / "phase2/sample_order.json").read_text()
claim("sample_order.json hash matches the manifest frozen before calls",
      hashlib.sha256(order_text.encode()).hexdigest() == manifest["sample_order_sha256"])
sample = manifest["sample_qa_keys"]
claim(f"sample size {len(sample)} == 304, no duplicates", len(sample) == 304 == len(set(sample)))

new = collections.defaultdict(dict)
for r in rows(KS / "phase2/results.jsonl"):
    new[r["condition"]][r["qa_key"]] = r["correct"]
correct = {f"{c}@10": {q: sealed[c][q]["correct"] for q in sample} for c in sealed}
correct.update({f"{c}@20": {q: new[c][q] for q in sample} for c in sealed})
summary = json.loads((KS / "phase2/summary.json").read_text())
res["accuracy"] = {}
for name, D in correct.items():
    acc = 100 * statistics.mean(D.values())
    res["accuracy"][name] = acc
    check(f"accuracy {name}, %", acc, summary["accuracy_percent"][name], tol=1e-9)
for comp in summary["comparisons"]:
    L, Rr = correct[comp["left"]], correct[comp["right"]]
    d = 100 * statistics.mean(L[q] - Rr[q] for q in sample)
    lo = sum(1 for q in sample if L[q] > Rr[q])
    ro = sum(1 for q in sample if L[q] < Rr[q])
    check(f"{comp['left']} - {comp['right']}, pp", d, comp["delta_pp"], tol=1e-9)
    claim(f"{comp['left']} - {comp['right']}: discordant {lo}/{ro}",
          (lo, ro) == (comp["left_only_correct"], comp["right_only_correct"]))
    claim(f"{comp['left']} - {comp['right']}: 95% CI includes zero", comp["ci95"][0] <= 0 <= comp["ci95"][1])

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(res, indent=2) + "\n")
print(f"\n{checks} checks, {len(failures)} failures; numbers -> {OUT}")
for f in failures:
    print("  FAILED:", f)
sys.exit(1 if failures else 0)
