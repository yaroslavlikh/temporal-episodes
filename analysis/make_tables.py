"""Generate the LaTeX tables of the paper from verified numbers.

Run analysis/verify_results.py first; it writes analysis/output/numbers.json. GroupMemBench
values come from results/group/aggregates.json, published baselines from
analysis/published_baselines.json.

    python3 analysis/make_tables.py        # writes paper/tables/*.tex
"""
from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
NUMBERS = REPO / "analysis" / "output" / "numbers.json"
GROUP = REPO / "results" / "group" / "aggregates.json"
PUBLISHED = REPO / "analysis" / "published_baselines.json"
OUT = REPO / "paper" / "tables"


def pct(value: float) -> str:
    return f"{100 * value:.1f}"


def signed_pp(value: float) -> str:
    return f"{100 * value:+.1f}".replace("-", "$-$")


def ci_pp(low: float, high: float) -> str:
    return f"[{signed_pp(low)}, {signed_pp(high)}]"


def p_value(value: float) -> str:
    return "$<$0.001" if value < 0.001 else f"{value:.3f}"


def write(name: str, body: list[str]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text("\n".join(body) + "\n")
    print(f"wrote {OUT / name}")


def main() -> None:
    n = json.loads(NUMBERS.read_text())
    group = json.loads(GROUP.read_text())
    published = json.loads(PUBLISHED.read_text())

    # Table 1: overall effect of adding episodes on each benchmark.
    gp = group["primary_endpoint"]
    ga = group["all_questions"]
    write("overall.tex", [
        r"\begin{tabular}{llrrrrl}", r"\toprule",
        r"Benchmark & Endpoint & $n$ & RAW & +Episodes & $\Delta$ (pp) & 95\% CI \\", r"\midrule",
        f"SocialMemBench & MeanN, 43 networks & 1031 & {pct(n['social RAW MeanN'])} & {pct(n['social RAW+EPISODES MeanN'])} & "
        f"{signed_pp(n['social RAW+EPISODES-RAW delta'])} & {ci_pp(n['social RAW+EPISODES-RAW CI low'], n['social RAW+EPISODES-RAW CI high'])} \\\\",
        f"GroupMemBench & update+temporal, filtered & {gp['n']} & {pct(gp['RAW'])} & {pct(gp['RAW+EPISODES'])} & "
        f"{signed_pp(gp['delta'])} & {ci_pp(*gp['ci95'])} \\\\",
        f"GroupMemBench & all questions & {ga['n']} & {pct(ga['RAW'])} & {pct(ga['RAW+EPISODES'])} & "
        f"{signed_pp(ga['delta'])} & {ci_pp(*ga['ci95'])} \\\\",
        f"EverMemBench & all questions & 2400 & {pct(n['ever RAW accuracy'])} & {pct(n['ever EP accuracy'])} & "
        f"{signed_pp(n['ever primary EP-RAW delta'])} & {ci_pp(n['ever primary EP-RAW CI low'], n['ever primary EP-RAW CI high'])} \\\\",
        r"\bottomrule", r"\end{tabular}",
    ])

    # Table 2: EverMemBench tasks against published GPT-4.1-mini memory systems.
    ever = published["evermembench"]
    systems = ["Full Context", "MemoBase", "Mem0", "Zep", "MemOS"]
    tasks = list(ever["task_to_minor"])
    header = " & ".join(["Method"] + tasks + ["Avg."]) + r" \\"
    rows = []
    for system in systems:
        values = ever["methods"][system]
        rows.append(" & ".join([system] + [f"{values[t]:.2f}" for t in tasks] + [f"{values['Average']:.2f}"]) + r" \\")
    for label, key in (("Ours: RAW", "RAW"), ("Ours: +Episodes", "EP")):
        values = [100 * n[f"ever {ever['task_to_minor'][t]} {key}"] for t in tasks]
        rows.append(" & ".join([label] + [f"{v:.2f}" for v in values] + [f"{100 * n[f'ever macro {key}']:.2f}"]) + r" \\")
    write("evermembench_tasks.tex", [
        r"\begin{tabular}{l" + "r" * (len(tasks) + 1) + "}", r"\toprule", header, r"\midrule",
        *rows[:len(systems)], r"\midrule", *rows[len(systems):], r"\bottomrule", r"\end{tabular}",
    ])

    # Table 3: Temporal Duration controls (EverMemBench TP, n = 300).
    conditions = [
        ("RAW, top-10", "control RAW accuracy"),
        ("RAW, token-matched", "control RAW-token-matched accuracy"),
        ("RAW, count-matched", "control RAW-count-matched accuracy"),
        ("Unlinked events, top-10", "unlinked RAW+EVENTS accuracy"),
        ("Unlinked events, token-matched", "unlinked RAW+EVENTS-token-matched accuracy"),
        ("Temporal episodes", "control RAW+EPISODES accuracy"),
    ]
    comparisons = [
        ("Episodes $-$ RAW, token-matched", "control primary EP-token"),
        ("Episodes $-$ unlinked events, token-matched", "unlinked primary EP-events-token"),
        ("Unlinked events $-$ RAW, both token-matched", "unlinked events-token vs RAW-token"),
        ("Episodes rerun $-$ episodes (calibration)", "control rerun-EP"),
    ]
    write("temporal_controls.tex", [
        r"\begin{tabular}{lr}", r"\toprule", r"Condition & Accuracy (\%) \\", r"\midrule",
        *[f"{label} & {pct(n[key])} \\\\" for label, key in conditions],
        r"\midrule", r"Paired comparison & $\Delta$ (pp) [95\% CI], $p$ \\", r"\midrule",
        *[f"{label} & {signed_pp(n[key + ' delta'])} {ci_pp(n[key + ' CI low'], n[key + ' CI high'])}, "
          f"{p_value(n[key + ' McNemar p'])} \\\\" for label, key in comparisons],
        r"\bottomrule", r"\end{tabular}",
    ])

    # Table 4: GroupMemBench accuracy on the five shared categories with cost and storage.
    gb = published["groupmembench"]
    shared = group["shared_five_categories"]
    counts = gb["question_counts"]
    rows = []
    for method, info in gb["methods"].items():
        correct = sum(round(info["accuracy_pct"][c] / 100 * counts[c]) for c in shared["categories"])
        cost = "--" if info["ingestion_usd"] is None else f"{info['ingestion_usd']:.2f}"
        storage = "--" if info["storage_gb"] is None else f"{info['storage_gb']:.2f}"
        rows.append((correct / shared["n"], f"{method} & {pct(correct / shared['n'])} & {cost} & {storage} \\\\"))
    average = group["per_domain_average"]
    rows.append((shared["RAW_correct"] / shared["n"],
                 f"Ours: RAW & {pct(shared['RAW_correct'] / shared['n'])} & {average['ingestion_usd_raw']:.2f} & {average['storage_gb_raw']:.2f} \\\\"))
    rows.append((shared["RAW+EPISODES_correct"] / shared["n"],
                 f"Ours: +Episodes & {pct(shared['RAW+EPISODES_correct'] / shared['n'])} & {average['ingestion_usd_episodes']:.2f} & {average['storage_gb_episodes']:.2f} \\\\"))
    write("groupmembench_shared.tex", [
        r"\begin{tabular}{lrrr}", r"\toprule",
        r"Method & Accuracy, 606 shared (\%) & Ingestion (USD/domain) & Storage (GB/domain) \\", r"\midrule",
        *[line for _, line in sorted(rows, key=lambda item: -item[0])],
        r"\bottomrule", r"\end{tabular}",
    ])


if __name__ == "__main__":
    main()
