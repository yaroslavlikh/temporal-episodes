# GroupMemBench pre-outcome implementation amendment

Recorded: `2026-09-12 16:51:28 MSK`, before episode materialization,
question loading, answer generation, judging, or benchmark scoring.

The extractor was prompted with namespaced turn identifiers such as
`Finance|Msg_86`, but frequently echoed only `Msg_86`. The strict validator
therefore rejected otherwise quote-grounded events. No question, answer,
label, retrieval result, or benchmark metric was used to discover or repair
the mismatch.

The correction restores a dropped namespace only when the suffix identifies
exactly one turn inside the current extraction window. The evidence quote
must still be a literal substring of that resolved turn. Ambiguous, unknown,
and quote-mismatched evidence remains rejected. Extraction prompt, model,
temperature, event schema, retrieval, attachment policy, thresholds, answer
model, judge, top-k, and primary endpoint were unchanged.

Audit of the frozen first 2,334 extraction responses (19,784 raw candidates):

- before correction: 81 valid events (0.41%);
- after correction: 15,751 valid events (79.61%);
- remaining rejected: 3,944 without a valid exact evidence quote and 89 with
  an invalid event-type enum;
- no LLM call was made during either audit.

Frozen artifacts:

- `event_extraction_cache_pre_fix.jsonl`: 2,334 rows,
  SHA-256 `7cf2c8aad12a9e2c3cbe51f92cfc0ed39f0a6f71d19c754610cb2274f515cb63`;
- `api_usage_pre_fix.jsonl`: 2,334 rows,
  SHA-256 `405a7f647cceee4fc38fd11b8587969045ac7fc40c98c5a40e59a8d187c9dc8b`;
- corrected `research/temporal_episode_prototype.py` at amendment time:
  SHA-256 `eabdba46f397d0c807f95245f3b9c90006cd485643fa69f8fee37cf03a8d2dc0`.

The cached LLM responses remain valid because the correction is downstream
of generation. Reusing them isolates the validator correction and avoids
introducing a second stochastic extraction sample.
