"""Verify the published results offline.

Checks SHA-256 of every file in results/, sealed row counts and hashes, and recomputes
every statistic reported for the paper with the exact functions from reproduction/research.
No API calls. Exit code 0 means every check passed.

    python3 analysis/verify_results.py
    python3 analysis/verify_results.py --group-local-dir /path/to/groupmembench_run   # optional
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
RESULTS = REPO / "results"
OUTPUT = REPO / "analysis" / "output"
sys.path.insert(0, str(REPO / "reproduction"))

from research import socialmembench_full_run as social  # noqa: E402
from research.paper_benchmark_common import (  # noqa: E402
    clustered_bootstrap, exact_mcnemar, paired_bootstrap, verify_sealed_jsonl,
)

EP, RAW = "RAW+EPISODES", "RAW"
checks = 0
failures: list[str] = []
numbers: dict[str, float] = {}


def jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def mean(values) -> float:
    values = list(values)
    return sum(values) / len(values)


def _fmt(value: float, digits: int) -> str:
    text = f"{value:.{digits}f}"
    return text.lstrip("-") if float(text) == 0 else text


def check(label: str, actual: float, expected: float, digits: int = 3) -> None:
    global checks
    checks += 1
    numbers[label] = actual
    if _fmt(actual, digits) != _fmt(expected, digits):
        failures.append(f"{label}: recomputed {_fmt(actual, digits)} != reported {_fmt(expected, digits)}")


def check_equal(label: str, actual, expected) -> None:
    global checks
    checks += 1
    if actual != expected:
        failures.append(f"{label}: {actual!r} != {expected!r}")


# --------------------------------------------------------------------------
# Integrity
# --------------------------------------------------------------------------

def verify_checksums() -> None:
    for line in (RESULTS / "manifests" / "SHA256SUMS").read_text().splitlines():
        digest, relative = line.split("  ", 1)
        path = RESULTS / relative
        check_equal(f"sha256 {relative}", sha256(path) if path.exists() else "missing", digest)


def verify_sealed() -> None:
    ever = RESULTS / "ever"
    for directory, rows in (("main", 4800), ("budget_control", 900), ("unlinked_events_control", 600)):
        for name in ("predictions", "results"):
            try:
                verify_sealed_jsonl(ever / directory / f"{name}.jsonl", ever / directory / f"{name}_meta.json",
                                    expected_rows=rows)
                check_equal(f"sealed ever/{directory}/{name}", True, True)
            except RuntimeError as error:
                check_equal(f"sealed ever/{directory}/{name}", str(error), "ok")
    episodes_meta = json.loads((ever / "main" / "episodes_meta.json").read_text())
    check_equal("ever episodes sha256", sha256(ever / "main" / "episodes.jsonl"), episodes_meta["episodes_sha256"])

    s = RESULTS / "social"
    for relative, meta_name, field in (
        ("baseline_raw_flat_versioned/predictions.jsonl", "baseline_raw_flat_versioned/predictions_meta.json", "predictions_sha256"),
        ("temporal_episodes_harness/episode_predictions.jsonl", "temporal_episodes_harness/episode_predictions_meta.json", "predictions_sha256"),
        ("temporal_episodes_run_a/predictions.jsonl", "temporal_episodes_run_a/predictions_meta.json", "predictions_sha256"),
        ("temporal_episodes_run_a/episodes.jsonl", "temporal_episodes_run_a/episodes_meta.json", "episodes_sha256"),
    ):
        check_equal(f"sealed social/{relative}", sha256(s / relative), json.loads((s / meta_name).read_text())[field])
    check_equal("social harness uses run A episodes",
                json.loads((s / "temporal_episodes_harness/episode_predictions_meta.json").read_text())["episodes_sha256"],
                json.loads((s / "temporal_episodes_run_a/episodes_meta.json").read_text())["episodes_sha256"])


# --------------------------------------------------------------------------
# SocialMemBench (network-weighted statistics of the official-compatible harness)
# --------------------------------------------------------------------------

def social_block(label: str, rows: list[dict], levels: dict, pairs: dict) -> None:
    for condition, (mean_q, mean_n, low, high, precision, recall) in levels.items():
        selected = [row for row in rows if row["condition"] == condition]
        networks = social._network_means(rows, condition)
        lo, hi = social.bootstrap_network_ci(networks)
        check(f"{label} {condition} MeanQ", mean(r["score"] for r in selected), mean_q)
        check(f"{label} {condition} MeanN", mean(networks.values()), mean_n)
        check(f"{label} {condition} MeanN CI low", lo, low)
        check(f"{label} {condition} MeanN CI high", hi, high)
        check(f"{label} {condition} evidence precision", mean(r["evidence_precision"] for r in selected), precision)
        check(f"{label} {condition} evidence recall", mean(r["evidence_recall"] for r in selected), recall)
    for (left, right), (wins, ties, losses, delta, low, high) in pairs.items():
        left_means, right_means = social._network_means(rows, left), social._network_means(rows, right)
        deltas = [left_means[key] - right_means[key] for key in sorted(left_means)]
        lo, hi = social.bootstrap_paired_ci(rows, left, right)
        check_equal(f"{label} {left}-{right} W/T/L",
                    (sum(d > 0 for d in deltas), sum(d == 0 for d in deltas), sum(d < 0 for d in deltas)),
                    (wins, ties, losses))
        check(f"{label} {left}-{right} delta", mean(deltas), delta)
        check(f"{label} {left}-{right} CI low", lo, low)
        check(f"{label} {left}-{right} CI high", hi, high)


def verify_social() -> None:
    s = RESULTS / "social"
    rows = jsonl(s / "baseline_raw_flat_versioned/results.jsonl") + jsonl(s / "temporal_episodes_harness/episode_results.jsonl")
    check_equal("social harness rows", len(rows), 4124)
    social_block("social", rows, {
        RAW: (0.358, 0.358, 0.332, 0.382, 0.124, 0.675),
        "RAW+FLAT": (0.370, 0.364, 0.338, 0.389, 0.133, 0.672),
        "RAW+VERSIONED": (0.367, 0.362, 0.338, 0.385, 0.132, 0.670),
        EP: (0.368, 0.367, 0.344, 0.390, 0.127, 0.685),
    }, {
        (EP, RAW): (22, 3, 18, 0.010, -0.008, 0.028),
        (EP, "RAW+FLAT"): (21, 2, 20, 0.003, -0.013, 0.022),
        (EP, "RAW+VERSIONED"): (24, 1, 18, 0.006, -0.010, 0.021),
    })
    run_a = jsonl(s / "temporal_episodes_run_a/results.jsonl")
    social_block("social run A", run_a, {
        RAW: (0.306, 0.311, 0.288, 0.334, 0.075, 0.485),
        EP: (0.324, 0.316, 0.293, 0.339, 0.078, 0.521),
    }, {(EP, RAW): (26, 4, 13, 0.006, -0.009, 0.020)})


# --------------------------------------------------------------------------
# EverMemBench and the Temporal controls
# --------------------------------------------------------------------------

def accuracy(rows: list[dict], condition: str, **where) -> float:
    return mean(r["correct"] for r in rows if r["condition"] == condition and all(r[k] == v for k, v in where.items()))


def paired(label: str, rows: list[dict], left: str, right: str, delta: float, low: float, high: float,
           left_only: int, right_only: int, p_value: float, p_digits: int = 4) -> None:
    d, lo, hi = paired_bootstrap(rows, left, right)
    test = exact_mcnemar(rows, left, right)
    check(f"{label} delta", d, delta)
    check(f"{label} CI low", lo, low)
    check(f"{label} CI high", hi, high)
    check_equal(f"{label} discordant", (test["left_only"], test["right_only"]), (left_only, right_only))
    numbers[f"{label} left_only"] = test["left_only"]
    numbers[f"{label} right_only"] = test["right_only"]
    check(f"{label} McNemar p", test["p_value"], p_value, p_digits)


def verify_ever() -> list[dict]:
    rows = jsonl(RESULTS / "ever/main/results.jsonl")
    check("ever RAW accuracy", accuracy(rows, RAW), 0.495)
    check("ever EP accuracy", accuracy(rows, EP), 0.502)
    paired("ever primary EP-RAW", rows, EP, RAW, 0.007, -0.005, 0.020, 121, 103, 0.255965, 6)
    d, lo, hi = clustered_bootstrap(rows, EP, RAW, "topic")
    check("ever equal-topic delta", d, 0.008)
    check("ever equal-topic CI low", lo, -0.003)
    check("ever equal-topic CI high", hi, 0.018)
    for condition, recall, precision in ((RAW, 0.081, 0.213), (EP, 0.108, 0.224)):
        selected = [r for r in rows if r["condition"] == condition]
        check(f"ever {condition} evidence recall", mean(r["evidence_recall"] for r in selected), recall)
        check(f"ever {condition} evidence precision", mean(r["evidence_precision"] for r in selected), precision)
    minors = ("SH", "MH", "TP", "C", "P", "U", "Style", "Skill", "Title")
    expected_minor = {"SH": (0.897, 0.878), "MH": (0.129, 0.133), "TP": (0.123, 0.200), "C": (0.799, 0.796),
                      "P": (0.658, 0.642), "U": (0.463, 0.474), "Style": (0.301, 0.381),
                      "Skill": (0.337, 0.308), "Title": (0.464, 0.434)}
    for minor in minors:
        check(f"ever {minor} RAW", accuracy(rows, RAW, minor=minor), expected_minor[minor][0])
        check(f"ever {minor} EP", accuracy(rows, EP, minor=minor), expected_minor[minor][1])
    check("ever macro RAW", mean(accuracy(rows, RAW, minor=m) for m in minors), 0.4634, 4)
    check("ever macro EP", mean(accuracy(rows, EP, minor=m) for m in minors), 0.4716, 4)
    tp = [r for r in rows if r["minor"] == "TP"]
    # Canonical paired bootstrap (20,000 samples, seed 20260912). The budget-control protocol text quotes
    # a preliminary 4,000-sample estimate, [+0.027, +0.123]; the paper uses this canonical interval.
    paired("ever TP EP-RAW", tp, EP, RAW, 0.077, 0.030, 0.127, 40, 17, 0.0032)
    return rows


def verify_controls(ever_rows: list[dict]) -> None:
    control = jsonl(RESULTS / "ever/budget_control/results.jsonl")
    keys = {r["qa_key"] for r in control}
    check_equal("budget control questions", len(keys), 300)
    rows = [r for r in ever_rows if r["qa_key"] in keys] + control
    for condition, value in ((RAW, 0.123), (EP, 0.200), ("RAW-count-matched", 0.133),
                             ("RAW-token-matched", 0.123), ("RAW+EPISODES-rerun", 0.200)):
        check(f"control {condition} accuracy", accuracy(rows, condition), value)
    paired("control primary EP-token", rows, EP, "RAW-token-matched", 0.077, 0.033, 0.120, 35, 12, 0.0011)
    paired("control EP-count", rows, EP, "RAW-count-matched", 0.067, 0.020, 0.117, 38, 18, 0.0105)
    paired("control token-RAW", rows, "RAW-token-matched", RAW, 0.000, -0.037, 0.037, 16, 16, 1.0)
    paired("control count-RAW", rows, "RAW-count-matched", RAW, 0.010, -0.023, 0.043, 15, 12, 0.7011)
    paired("control rerun-EP", rows, "RAW+EPISODES-rerun", EP, 0.000, -0.023, 0.023, 6, 6, 1.0)
    paired("control rerun-token", rows, "RAW+EPISODES-rerun", "RAW-token-matched", 0.077, 0.033, 0.123, 36, 13, 0.0014)

    unlinked = jsonl(RESULTS / "ever/unlinked_events_control/results.jsonl")
    rows = ([r for r in ever_rows if r["qa_key"] in keys]
            + [r for r in control if r["condition"] == "RAW-token-matched"] + unlinked)
    for condition, value in (("RAW+EVENTS", 0.163), ("RAW+EVENTS-token-matched", 0.170)):
        check(f"unlinked {condition} accuracy", accuracy(rows, condition), value)
    paired("unlinked primary EP-events-token", rows, EP, "RAW+EVENTS-token-matched", 0.030, -0.013, 0.073, 27, 18, 0.2327)
    paired("unlinked EP-events", rows, EP, "RAW+EVENTS", 0.037, -0.007, 0.080, 29, 18, 0.1439)
    paired("unlinked events-token vs RAW-token", rows, "RAW+EVENTS-token-matched", "RAW-token-matched",
           0.047, 0.007, 0.087, 26, 12, 0.0336)
    paired("unlinked events-RAW", rows, "RAW+EVENTS", RAW, 0.040, -0.007, 0.087, 32, 20, 0.1263)


# --------------------------------------------------------------------------
# GroupMemBench (per-question data not redistributed)
# --------------------------------------------------------------------------

def verify_group(local_dir: Path | None) -> None:
    report = (RESULTS / "group/report.md").read_text()
    for line in ("- RAW: 0.340", "- RAW+EPISODES: 0.300",
                 "- paired delta: -0.040, question bootstrap 95% CI [-0.093, +0.013]",
                 "- exact paired McNemar: EP-only=6, RAW-only=12, p=0.237885"):
        check_equal(f"group report line {line!r}", line in report, True)
    numbers.update({"group primary RAW": 0.340, "group primary EP": 0.300, "group primary delta": -0.040,
                    "group primary CI low": -0.093, "group primary CI high": 0.013})
    if local_dir is None:
        return
    withheld = json.loads((RESULTS / "group/withheld_sha256.json").read_text())["files"]
    for name, meta in withheld.items():
        check_equal(f"group withheld {name}", sha256(local_dir / name), meta["sha256"])
    rows = jsonl(local_dir / "results.jsonl")
    primary = [r for r in rows if r["domain"] in ("Finance", "Technology") and r["qtype"] in ("knowledge_update", "temporal")]
    check("group primary RAW (local)", accuracy(primary, RAW), 0.340)
    check("group primary EP (local)", accuracy(primary, EP), 0.300)
    paired("group primary EP-RAW (local)", primary, EP, RAW, -0.040, -0.093, 0.013, 6, 12, 0.237885, 6)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--group-local-dir", type=Path)
    args = parser.parse_args()
    verify_checksums()
    verify_sealed()
    verify_social()
    ever_rows = verify_ever()
    verify_controls(ever_rows)
    verify_group(args.group_local_dir)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / "numbers.json").write_text(json.dumps(numbers, indent=2, sort_keys=True) + "\n")
    for failure in failures:
        print(f"FAIL  {failure}")
    print(f"{checks} checks, {len(failures)} failures; recomputed numbers -> {OUTPUT / 'numbers.json'}")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
