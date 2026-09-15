# Temporal Episodes

Reproduction package for a study of **provenance-backed memory for long-lived multi-party
conversations**. Memory is built without access to questions: an LLM extracts events from
bounded chat sessions, every event keeps verbatim quotes that are checked mechanically
against the source messages, and events are linked into append-only temporal episodes.
Episodes are retrieved together with raw messages, and every episode expands into the
messages it cites.

The method is evaluated on three external multi-party benchmarks under their official or
official-compatible harnesses, with controlled ablations. A paper is in preparation.

## Results at a glance

Adding episodes to raw retrieval, paired over the same questions:

| Benchmark | Endpoint | Raw retrieval | + Temporal episodes | Δ, 95% CI |
|---|---|---:|---:|---|
| SocialMemBench | network-weighted mean score, 1,031 QA | 35.8 | 36.7 | +1.0 [−0.8, +2.8] |
| GroupMemBench | knowledge update + temporal, filtered, 150 QA | 34.0 | 30.0 | −4.0 [−9.3, +1.3] |
| EverMemBench-Dynamic | accuracy, 2,400 QA | 49.5 | 50.2 | +0.8 [−0.5, +2.0] |

Overall, episodes did not change accuracy measurably. On EverMemBench Temporal Duration
questions (n = 300), they did:

| Condition (EverMemBench Temporal Duration) | Accuracy |
|---|---:|
| Raw retrieval, top-10 | 12.3 |
| Raw retrieval, same token budget as episodes | 12.3 |
| Unlinked events, same token budget | 17.0 |
| Temporal episodes | 20.0 |

- Episodes vs. raw retrieval at an equal token budget: **+7.7 pp [+3.3, +12.0]**, McNemar
  p = 0.001; a rerun of the episode condition agreed on 96% of questions.
- Unlinked events vs. raw retrieval at an equal token budget: +4.7 pp [+0.7, +8.7].
- Episodes vs. the same events unlinked: +3.0 pp [−1.3, +7.3] — this sample does not resolve
  the contribution of chronological linking.

The Temporal effect was found in the same EverMemBench data used for the controls, so the
controls are mechanistic ablations, not an independent replication. These are adapter
evaluations, not official leaderboard submissions. Every number above is recomputed by
`analysis/verify_results.py`; the full history of experiments is in `EXPERIMENT_LOG.md`.

## Repository layout

```
reproduction/   exact runners, method code and tests that produced the results (see REDACTIONS.md)
analysis/       offline verification, LaTeX tables and figures; published baselines used for comparison
protocols/      analysis protocols and amendments, verbatim
results/        per-question predictions and judgments (SocialMemBench, EverMemBench),
                GroupMemBench aggregates, SHA-256 manifest
paper/          LaTeX sources, tables and figures
```

## Quick start

```bash
python3 -m pip install -r requirements.lock
python3 analysis/verify_results.py     # checksums + every reported statistic, no API calls
python3 analysis/make_tables.py
python3 analysis/make_figures.py
```

Re-running the experiments requires OpenAI and OpenRouter API keys; see `REPRODUCE.md`.

## Licenses

Code is released under the Apache License 2.0 (`LICENSE`). Benchmark data and everything
derived from it remain under the upstream terms: SocialMemBench (CC BY 4.0) and
EverMemBench-Dynamic (Apache 2.0) derived results are included with attribution;
GroupMemBench publishes no license, so only aggregates and checksums are included. See
`THIRD_PARTY.md`.

## Citation

See `CITATION.cff`.
