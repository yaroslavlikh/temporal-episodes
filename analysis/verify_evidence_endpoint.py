"""Verify the evidence-delivery endpoint and the registered frontier check, offline.

Recomputes every number the manuscript reports for the dissociation result directly from
the published per-question files in results/. No API calls.

    python3 analysis/verify_evidence_endpoint.py

Two endpoints are distinguished throughout:

* evidence recall / precision - computed mechanically from exposed source IDs and gold
  anchors. They never pass through the generator or the judge.
* accuracy - passes through both, and flips on about 4% of questions between reruns of an
  identical condition (see the noise-floor section).

Exit code 0 means every recomputed value matched the manuscript within tolerance.
"""
from __future__ import annotations

import collections
import json
import pathlib
import random
import statistics
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
RESULTS = REPO / "results"
OUT = REPO / "analysis" / "output" / "evidence_endpoint.json"
BOOT, SEED = 20000, 20260912

failures: list[str] = []
checks = 0


def rows(rel: str):
    for line in (RESULTS / rel).open():
        yield json.loads(line)


def load(rel: str, cond: str) -> dict:
    return {r["qa_key"]: r for r in rows(rel) if r.get("condition") == cond}


def boot_ci(x, b=BOOT, seed=SEED):
    rnd = random.Random(seed)
    n = len(x)
    bs = sorted(sum(x[rnd.randrange(n)] for _ in range(n)) / n for _ in range(b))
    return bs[int(0.025 * b)], bs[int(0.975 * b)]


def wilcoxon_p(x):
    """Two-sided Wilcoxon signed-rank with a normal approximation and tie correction."""
    nz = [v for v in x if abs(v) > 1e-12]
    if not nz:
        return 1.0
    order = sorted(range(len(nz)), key=lambda i: abs(nz[i]))
    ranks = [0.0] * len(nz)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and abs(abs(nz[order[j + 1]]) - abs(nz[order[i]])) < 1e-12:
            j += 1
        avg = (i + j) / 2 + 1
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    w = sum(r for r, v in zip(ranks, nz) if v > 0)
    n = len(nz)
    mu = n * (n + 1) / 4
    sigma = (n * (n + 1) * (2 * n + 1) / 24) ** 0.5
    if sigma == 0:
        return 1.0
    z = (w - mu) / sigma
    return max(min(2 * 0.5 * (1 - _erf(abs(z) / 2 ** 0.5)), 1.0), 0.0)


def _erf(x):
    import math
    return math.erf(x)


def paired(a: dict, b: dict, field: str) -> dict:
    ks = sorted(set(a) & set(b))
    x = [a[k][field] - b[k][field] for k in ks]
    m = sum(x) / len(x)
    lo, hi = boot_ci(x)
    return dict(n=len(ks), delta_pp=100 * m, ci=[100 * lo, 100 * hi], p=wilcoxon_p(x),
                better=sum(1 for v in x if v > 1e-12), worse=sum(1 for v in x if v < -1e-12))


def check(label: str, got: float, want: float, tol: float = 0.05) -> None:
    global checks
    checks += 1
    if abs(got - want) > tol:
        failures.append(f"{label}: recomputed {got:.4f}, manuscript {want:.4f}")
    print(f"  {'ok ' if abs(got - want) <= tol else 'FAIL'} {label:52s} {got:+8.3f}  (paper {want:+.3f})")


res: dict = {"_note": "percentage points; recomputed offline from results/"}

# --------------------------------------------------------------- EverMemBench
EV = "ever/main/results.jsonl"
RAW = load(EV, "RAW")
EPI = load(EV, "RAW+EPISODES")
EVE = load("ever/events_full/results.jsonl", "RAW+EVENTS")

print("EverMemBench, all 2,400 questions, paired against RAW")
res["ever"] = {}
for arm, D in (("events", EVE), ("episodes", EPI)):
    res["ever"][arm] = {f: paired(D, RAW, f) for f in ("evidence_precision", "evidence_recall")}
check("events - raw, evidence precision", res["ever"]["events"]["evidence_precision"]["delta_pp"], 3.21)
check("events - raw, evidence recall", res["ever"]["events"]["evidence_recall"]["delta_pp"], 0.64)

# per-category precision delta
cats = collections.defaultdict(list)
for k in sorted(set(EVE) & set(RAW)):
    cats[EVE[k]["minor"]].append(EVE[k]["evidence_precision"] - RAW[k]["evidence_precision"])
res["ever"]["events_precision_by_category"] = {}
print("per-category evidence precision, events - raw")
for c, v in sorted(cats.items()):
    lo, hi = boot_ci(v)
    res["ever"]["events_precision_by_category"][c] = dict(
        n=len(v), delta_pp=100 * sum(v) / len(v), ci=[100 * lo, 100 * hi])
    print(f"    {c:6s} n={len(v):4d}  {100 * sum(v) / len(v):+6.2f}  [{100 * lo:+.2f}, {100 * hi:+.2f}]")
positive = sum(1 for d in res["ever"]["events_precision_by_category"].values() if d["delta_pp"] > 0)
excl_zero = sum(1 for d in res["ever"]["events_precision_by_category"].values() if d["ci"][0] > 0)
checks += 2
if positive != 9:
    failures.append(f"expected 9 positive categories, got {positive}")
if excl_zero != 8:
    failures.append(f"expected 8 categories with CI excluding zero, got {excl_zero}")
print(f"  {'ok ' if positive == 9 else 'FAIL'} sign positive in {positive}/9 categories")
print(f"  {'ok ' if excl_zero == 8 else 'FAIL'} CI excludes zero in {excl_zero}/9 categories")


def exposed(rel: str, cond: str) -> dict:
    return {r["qa_key"]: len(set(r["exposed_source_ids"])) for r in rows(rel)
            if r["condition"] == cond}


sRAW = exposed("ever/main/predictions.jsonl", "RAW")
sEVE = exposed("ever/events_full/predictions.jsonl", "RAW+EVENTS")
sEPI = exposed("ever/main/predictions.jsonl", "RAW+EPISODES")
ks = sorted(set(sRAW) & set(sEVE) & set(sEPI))
gold = lambda D, S, k: D[k]["evidence_precision"] * S[k]  # noqa: E731
gdiff = [gold(EVE, sEVE, k) - gold(RAW, sRAW, k) for k in ks]
lo, hi = boot_ci(gdiff)
res["ever"]["pareto"] = dict(
    sources={"raw": statistics.mean(sRAW[k] for k in ks),
             "events": statistics.mean(sEVE[k] for k in ks),
             "episodes": statistics.mean(sEPI[k] for k in ks)},
    gold_hits={"raw": statistics.mean(gold(RAW, sRAW, k) for k in ks),
               "events": statistics.mean(gold(EVE, sEVE, k) for k in ks),
               "episodes": statistics.mean(gold(EPI, sEPI, k) for k in ks)},
    gold_delta=statistics.mean(gdiff), gold_ci=[lo, hi],
    events_never_more_sources=all(sEVE[k] <= sRAW[k] for k in ks),
    questions_events_strictly_dominate=sum(
        1 for k in ks if gold(EVE, sEVE, k) > gold(RAW, sRAW, k) and sEVE[k] <= sRAW[k]))
print("dominance check (precision could otherwise rise by delivering less)")
check("mean sources, raw", res["ever"]["pareto"]["sources"]["raw"], 10.00)
check("mean sources, events", res["ever"]["pareto"]["sources"]["events"], 9.47)
check("mean gold hits, raw", res["ever"]["pareto"]["gold_hits"]["raw"], 2.129, tol=0.01)
check("mean gold hits, events", res["ever"]["pareto"]["gold_hits"]["events"], 2.245, tol=0.01)
check("gold hits delta", res["ever"]["pareto"]["gold_delta"], 0.117, tol=0.01)
checks += 1
if not res["ever"]["pareto"]["events_never_more_sources"]:
    failures.append("events delivered more sources than raw on at least one question")
print(f"  {'ok ' if res['ever']['pareto']['events_never_more_sources'] else 'FAIL'} "
      f"events never deliver more sources than raw")

# -------------------------------------------------------------- SocialMemBench
print("SocialMemBench, 1,031 questions, paired against RAW")
sd = collections.defaultdict(dict)
for rel in ("social/baseline_raw_flat_versioned/results.jsonl",
            "social/temporal_episodes_harness/episode_results.jsonl"):
    for r in rows(rel):
        sd[r["condition"]][r["qa_key"]] = r
res["social"] = {arm: {f: paired(sd[cond], sd["RAW"], f)
                       for f in ("evidence_precision", "evidence_recall")}
                 for arm, cond in (("flat", "RAW+FLAT"), ("versioned", "RAW+VERSIONED"),
                                   ("episodes", "RAW+EPISODES"))}
check("flat - raw, evidence precision", res["social"]["flat"]["evidence_precision"]["delta_pp"], 0.90)
check("versioned - raw, evidence precision", res["social"]["versioned"]["evidence_precision"]["delta_pp"], 0.86)
check("episodes - raw, evidence precision", res["social"]["episodes"]["evidence_precision"]["delta_pp"], 0.34)
check("episodes - raw, evidence recall", res["social"]["episodes"]["evidence_recall"]["delta_pp"], 0.99)

# ------------------------------------------------- HyDE control, Temporal slice
print("Temporal Duration, matched budget and order, 300 questions")
hd = collections.defaultdict(dict)
for rel in ("ever/hyde_raw/results.jsonl", "ever/hyde_token_matched/results.jsonl",
            "ever/chronological_order_control/results.jsonl"):
    for r in rows(rel):
        if "evidence_precision" in r:
            hd[r["condition"]][r["qa_key"]] = r
res["hyde"] = {
    "events_minus_hyde": {f: paired(hd["RAW+EVENTS-token-matched-chrono"],
                                    hd["HyDE-RAW-token-matched-chrono"], f)
                          for f in ("evidence_precision", "evidence_recall")},
    "hyde_minus_raw": {f: paired(hd["HyDE-RAW-token-matched-chrono"],
                                 hd["RAW-token-matched-chrono"], f)
                       for f in ("evidence_precision", "evidence_recall")},
}
check("events - hyde, evidence precision", res["hyde"]["events_minus_hyde"]["evidence_precision"]["delta_pp"], 6.68)
check("events - hyde, evidence recall", res["hyde"]["events_minus_hyde"]["evidence_recall"]["delta_pp"], -1.01)
check("hyde - raw, evidence precision", res["hyde"]["hyde_minus_raw"]["evidence_precision"]["delta_pp"], 1.18)
check("hyde - raw, evidence recall", res["hyde"]["hyde_minus_raw"]["evidence_recall"]["delta_pp"], 1.61)

# ------------------------------------ noise floor: rerun of an identical condition
print("noise floor: rerun of one identical condition on the same 300 questions")
A = load("ever/budget_control/results.jsonl", "RAW+EPISODES-rerun")
B = load(EV, "RAW+EPISODES")
ks = sorted(set(A) & set(B))
flips = [(A[k]["correct"], B[k]["correct"]) for k in ks]
ev_same = sum(1 for k in ks
              if abs(A[k]["evidence_precision"] - B[k]["evidence_precision"]) < 1e-12
              and abs(A[k]["evidence_recall"] - B[k]["evidence_recall"]) < 1e-12)
res["noise_floor"] = dict(n=len(ks), verdict_flips=sum(1 for a, b in flips if a != b),
                          evidence_identical=ev_same)
check("accuracy verdict flips out of 300", res["noise_floor"]["verdict_flips"], 12, tol=0.5)
check("questions with identical evidence metrics", res["noise_floor"]["evidence_identical"], len(ks), tol=0.5)

# --------------------------- registered frontier check, 2,100 non-discovery QA
print("registered frontier prediction, 2,100 questions outside the discovery slice")


def dominance(re_, pe, rr, pr):
    if (re_ >= rr and pe >= pr) and (re_ > rr or pe > pr):
        return "A"
    if (rr >= re_ and pr >= pe) and (rr > re_ or pr > pe):
        return "B"
    return "C"


strata = {"A": [], "B": [], "C": []}
for k in sorted(set(EVE) & set(RAW)):
    if EVE[k]["minor"] == "TP":
        continue
    s = dominance(EVE[k]["evidence_recall"], EVE[k]["evidence_precision"],
                  RAW[k]["evidence_recall"], RAW[k]["evidence_precision"])
    strata[s].append(EVE[k]["correct"] - RAW[k]["correct"])
res["frontier"] = {}
for s in "ABC":
    d = strata[s]
    lo, hi = boot_ci([float(v) for v in d])
    res["frontier"][s] = dict(n=len(d), delta_pp=100 * sum(d) / len(d), ci=[100 * lo, 100 * hi],
                              wins=sum(1 for v in d if v > 0), losses=sum(1 for v in d if v < 0))
    print(f"    stratum {s}  n={len(d):5d}  delta={100 * sum(d) / len(d):+6.2f} pp  "
          f"[{100 * lo:+.2f}, {100 * hi:+.2f}]  {res['frontier'][s]['wins']}/{res['frontier'][s]['losses']}")
check("stratum A (events dominate) delta", res["frontier"]["A"]["delta_pp"], 0.77, tol=0.1)
check("stratum B (raw dominates) delta", res["frontier"]["B"]["delta_pp"], -2.39, tol=0.1)
check("stratum C (mixed) delta", res["frontier"]["C"]["delta_pp"], -0.24, tol=0.1)
checks += 1
if res["frontier"]["A"]["ci"][0] > 0:
    failures.append("stratum A CI excludes zero; the manuscript reports it as not confirmed")
print(f"  {'ok ' if res['frontier']['A']['ci'][0] <= 0 else 'FAIL'} "
      f"stratum A interval contains zero (prediction not confirmed)")

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(res, indent=2) + "\n")
print(f"\n{checks} checks, {len(failures)} failures; numbers -> {OUT}")
for f in failures:
    print("  FAILED:", f)
sys.exit(1 if failures else 0)
