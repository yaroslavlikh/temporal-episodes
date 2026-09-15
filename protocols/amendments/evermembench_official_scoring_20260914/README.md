# EverMemBench-Dynamic pre-outcome scoring amendment

Recorded: `2026-09-14`, while query-independent memory shards were still being
built (extraction cache rows per topic: 01=267, 02=244, 03=232, 04=252, 05=281;
no shard `episodes.jsonl`, no merged snapshot). No question file had been
opened: `predictions.jsonl`, `results.jsonl` and `evaluation_input_manifest.json`
did not exist, and the OpenRouter cache held only the two preflight calls.

## Why

The completed GroupMemBench run produced 101/1490 empty gpt-5 answers: hidden
reasoning exhausted the output cap, and empty output was scored as incorrect
(RAW 44, RAW+EPISODES 58). Auditing the EverMemBench runner against the pinned
official code (`EverMind-AI/EverMemBench@e10b3d52f0e4`) before any QA call found
the same risk plus three deviations from the official harness that the protocol
claims to follow exactly.

## Deviations found and corrected

All changes are in `research/evermembench_parallel_resume.py`, which is not part
of the memory implementation manifest; its SHA-256 is recorded in the sealed
prediction and result metadata as `execution_runner_sha256`.

1. **Judge output cap.** Official `eval/config/pipeline.yaml` sets no `max_tokens`
   for `evaluate`, and `evaluator.py` sends only `temperature: 0` plus provider
   pinning. The runner sent `max_tokens=512` to `google/gemini-3-flash-preview`,
   a thinking model. The judge is now called exactly like the official evaluator.
2. **Judge label parsing.** The runner searched `output.upper()` for the lowercase
   pattern `"label"`, which can never match; any verdict wrapped in a markdown
   code fence would have been scored WRONG. Replaced by a port of the official
   `_parse_judge_response`.
3. **Multiple-choice parsing.** The runner used its own letter parser. Replaced by
   the official two-stage parse: `answerer._parse_mc_answer` at answer time, then
   `evaluator._evaluate_mc` (failure markers `[EMPTY]`/`[INVALID]`/`[FAILED]`
   always score WRONG).
4. **Open-ended empty answers** now carry the official `[EMPTY]` marker. The raw
   model text is kept in `answer_raw`.

## One deliberate difference from the official evaluator

Empty or `finish_reason == "length"` judge content is re-requested up to 5 times
and never cached; if it persists the run stops instead of scoring WRONG. The
official evaluator would score such a response WRONG. Every judge row records
`judge_finish_reason`, `judge_attempts` and `judge_parse`, and the report lists
per-condition counts, so the number of verdicts affected by this difference is
visible (0 re-requests means no difference materialised).

## Unchanged

Memory construction code and its hashes, extraction/attachment model, answer
model, answer prompt and parameters (`temperature 0`, `max_tokens 1000`, as in the
official config), option formatting (verified identical: sorted `"A. text"`
lines), retrieval, top-k, conditions, primary endpoint and statistics.
