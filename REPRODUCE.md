# Reproducing the results

There are two levels. Verifying the published numbers needs no API keys and takes about a
minute. Re-running the experiments calls paid APIs and does not reproduce model outputs
byte for byte (hosted models are not fully deterministic), so re-runs should agree
statistically, not exactly.

## 1. Verify the published numbers (offline)

```bash
python3 -m pip install -r requirements.lock
python3 analysis/verify_results.py
```

The script checks the SHA-256 of every file in `results/` against
`results/manifests/SHA256SUMS`, checks sealed row counts and hashes, and recomputes every
reported statistic with the exact functions in `reproduction/research/`. Exit code 0 means
all checks passed; recomputed values are written to `analysis/output/numbers.json`.

GroupMemBench per-question files are not redistributed (see `THIRD_PARTY.md`). The verifier
checks the published aggregates; anyone holding the per-question files can pass
`--group-local-dir` to check their SHA-256 against `results/group/withheld_sha256.json` and
recompute the primary endpoint.

Tables and figures for the paper are generated from the same data:

```bash
python3 analysis/make_tables.py
python3 analysis/make_figures.py
```

## 2. Re-run the experiments

Setup:

```bash
python3 -m pip install -r requirements.lock
cd reproduction
printf 'OPENAI_API_KEY=...\nLLM_API_KEY=...\n' > .env   # LLM_API_KEY is an OpenRouter key
```

All commands below run from `reproduction/`. Runners keep resumable caches and sealed
outputs in `reproduction/.research_runs/`. Exit code 75 means a rate limit; rerun the same
command to resume.

### SocialMemBench

```bash
python3 fetch_socialmembench.py --data-dir /tmp/socialmembench     # pinned revision, SHA-256 checked
python3 -m research.socialmembench_full_run --all                  # RAW, RAW+FLAT, RAW+VERSIONED
python3 -m research.freeze_socialmembench_full_run                 # read-only copy the harness expects
python3 -m research.socialmembench_episode_full_run --all          # builds episodes; run A
python3 -m research.socialmembench_episode_official_harness --all  # RAW+EPISODES in the harness of run 1
```

The runners' built-in download uses `<name>.parquet` at the pinned revision, which now returns
404; `fetch_socialmembench.py` downloads the same files from `<name>/train/0000.parquet`.

### GroupMemBench

```bash
python3 -m research.groupmembench_episode_run --prepare-memory      # clones the pinned official commit
python3 -m research.groupmembench_parallel_resume --all --workers 16
```

`research.paper_runs --group` runs the same pipeline sequentially. Answers and judgments use
gpt-5 with a 2,048-token completion cap; in the published run 101 of 1,490 answers were empty
because hidden reasoning exhausted that cap.

### EverMemBench-Dynamic

```bash
python3 -m research.evermembench_parallel_resume --all --memory-workers 5 --answer-workers 16 --judge-workers 4
```

With 32 judge workers OpenRouter may return 402 (`in_flight_budget_exhausted`) because the judge
is called without `max_tokens`; fewer workers avoid it.

### Temporal controls

```bash
python3 -m research.evermembench_temporal_budget_control --verify     # offline reconstruction checks
python3 -m research.evermembench_temporal_budget_control --smoke
python3 -m research.evermembench_temporal_budget_control --all --judge-workers 4

python3 -m research.evermembench_unlinked_events_control --build-index
python3 -m research.evermembench_unlinked_events_control --verify
python3 -m research.evermembench_unlinked_events_control --smoke
python3 -m research.evermembench_unlinked_events_control --all
```

The unlinked-events runner reads the frozen budget control from
`.research_runs/frozen/evermembench_temporal_budget_control_v1_20260915_021134_MSK`. After
freezing your own control (`research.paper_benchmark_common.freeze_run`), create a symlink with
that name or edit the `CONTROL_FROZEN` constant.

## Cost and duration of the published runs

Estimated from recorded token usage at uncached list prices (2026-09-12 snapshot).

| Run | API cost | Notes |
|---|---:|---|
| SocialMemBench run A (memory, answers, judge; gpt-4o-mini) | $0.82 | usage not recorded for the baseline and harness runs |
| GroupMemBench (memory gpt-4o-mini $6.70, embeddings $1.00, gpt-5 answers $22.04, judge $2.89) | $32.63 | memory ≈ 35 API-hours when linking runs sequentially |
| EverMemBench-Dynamic (memory $4.76, embeddings $0.46, answers $3.12, judge $0.55) | $8.88 | about 2.5 h wall clock with five parallel topic shards |
| Temporal budget control | $1.25 | a few minutes |
| Unlinked events ablation (+ $0.09 event embeddings) | $0.75 | a few minutes |

## Known differences from the original workspace

- `reproduction/REDACTIONS.md` lists the only edits to the published code: one docstring
  example and neutral test fixture names. Because the docstring edit changes a file hash,
  `verify_episode_snapshot` against the original sealed manifests reports a mismatch for
  `research/temporal_episode_prototype.py`; its executable code is unchanged.
- Protocol files are also kept in `reproduction/research/` because the runners hash or read them
  from that location; `protocols/` holds the same files for readers.
- `test_paper_external_benchmarks.py` needs the official GroupMemBench and EverMemBench sources
  in `reproduction/.research_runs/official_sources/`, which the runners download on first use.
