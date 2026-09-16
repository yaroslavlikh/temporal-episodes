# Experiment log

Substantive experiments that shaped the hypotheses, in chronological order (2026, MSK).
Technical interruptions (rate limits, credit exhaustion, resumed runs) are omitted; they
changed no result. Numbers are recomputed by `analysis/verify_results.py` unless marked.

## Before the external benchmarks

The method grew out of a private group-chat application. Early pilots on that private data
and on a SocialMemBench development subset (20 Q8 questions, gold evidence anchors used to
scope extraction) informed the event contract, quote validation and linking policy. None of
the private data is used for any claim or published here. SocialMemBench is therefore a
development/discovery benchmark for this method, not held-out data.

## 1. SocialMemBench baseline — 2026-09-11

RAW, RAW+FLAT and RAW+VERSIONED under an official-compatible harness (gpt-4o-mini,
text-embedding-3-small, cosine top-10, 1,031 QA, 43 networks). MeanQ 0.358 / 0.370 / 0.367.
`results/social/baseline_raw_flat_versioned/`.

## 2. SocialMemBench TemporalEpisodes, run A — 2026-09-12

Query-independent temporal episodes with hybrid retrieval, MiniLM embeddings and a
400-word context budget. RAW 0.306 vs RAW+EPISODES 0.324 (MeanQ); paired network delta
+0.006, 95% CI [−0.009, +0.020]. `results/social/temporal_episodes_run_a/`.

## 3. SocialMemBench TemporalEpisodes, official-compatible harness — 2026-09-12

The same sealed episodes evaluated in the harness of experiment 1. This harness was chosen as
the primary SocialMemBench comparison after run A had been scored, because it matches the
published protocol. RAW+EPISODES MeanQ 0.368; paired network delta vs RAW +0.010,
95% CI [−0.008, +0.028]; vs RAW+FLAT +0.003 [−0.013, +0.022].
`results/social/temporal_episodes_harness/`.

## 4. External protocol frozen — 2026-09-12

`protocols/original/PAPER_BENCHMARK_PROTOCOL.md` fixed models, retrieval, statistics and
endpoints for GroupMemBench and EverMemBench before any of their answers were generated.
The file labels GroupMemBench the "confirmatory" run with a primary endpoint on
knowledge_update + temporal in the filtered Finance and Technology domains. In practice the
author treated GroupMemBench as a first exploration of how to continue; the protocol text is
published unchanged and results are reported against it as written.

Amendment before any GroupMemBench question was loaded: turn-id namespace restoration in the
quote validator (`protocols/amendments/groupmembench_namespace_fix_20260912/`).

## 5. GroupMemBench — completed 2026-09-14

Primary endpoint: RAW 0.340 vs RAW+EPISODES 0.300; paired delta −0.040, 95% CI
[−0.093, +0.013]; McNemar p = 0.238. All 745 questions: −0.017 [−0.043, +0.007].
Measurement defect found after scoring: 101 of 1,490 gpt-5 answers were empty because hidden
reasoning exhausted the 2,048-token completion cap (RAW 44, RAW+EPISODES 58); empty answers
were scored incorrect. Post-hoc sensitivity excluding pairs with an empty answer: primary
−0.024 [−0.081, +0.024] (not recomputed by the public verifier; per-question data are not
redistributed). Diagnostics: episodes displaced raw messages in the unified top-10 and
nearly doubled input tokens. Aggregates in `results/group/`.

## 6. EverMemBench scoring amendment — 2026-09-14

Before any EverMemBench question was opened, the judge call and label parsing were aligned
with the pinned official evaluator (no `max_tokens`, official JSON parsing, official
multiple-choice parsing) and empty or length-cut judge outputs were set to be re-requested
rather than scored. `protocols/amendments/evermembench_official_scoring_20260914/`.

## 7. EverMemBench — completed 2026-09-15

Primary endpoint (all 2,400 QA): RAW 0.495 vs RAW+EPISODES 0.502; paired delta +0.007,
95% CI [−0.005, +0.020]; McNemar p = 0.256. Macro average over nine tasks: RAW 46.34%,
RAW+EPISODES 47.16%.
Exploratory sub-task analysis (declared secondary slices, nine comparisons): Temporal Duration
(TP, n = 300) 0.123 → 0.200, +0.077, canonical 95% CI [+0.030, +0.127], McNemar p = 0.0032,
positive in all five projects. Style (n = 176), a category unrelated to the temporal hypothesis,
showed a similar gain (+0.080, 95% CI [+0.028, +0.136], p = 0.0066).
The TP effect was discovered in these data. `results/ever/main/`.

## 8. Temporal budget control — 2026-09-15

Protocol frozen and hashed before new predictions
(`protocols/original/EVERMEMBENCH_TEMPORAL_BUDGET_CONTROL_PROTOCOL.md`). Its motivation
paragraph quotes a preliminary 4,000-sample interval for the TP effect, [+0.027, +0.123];
the canonical interval is the one in experiment 7.
Primary: RAW+EPISODES − RAW-token-matched = +0.077, 95% CI [+0.033, +0.120], McNemar
p = 0.0011. RAW-token-matched 0.123 (same as RAW), RAW-count-matched 0.133. Calibration rerun
of RAW+EPISODES: +0.000, per-question agreement 96%. `results/ever/budget_control/`.

## 9. Unlinked events ablation — 2026-09-15

Protocol frozen and hashed before new predictions
(`protocols/original/EVERMEMBENCH_UNLINKED_EVENTS_CONTROL_PROTOCOL.md`). The same 16,859
sealed events as separate documents without chronological linking, matched to RAW+EPISODES
tokens (2,456 vs 2,460) and unique source messages (17.4 vs 17.4).
Primary: RAW+EPISODES − RAW+EVENTS-token-matched = +0.030, 95% CI [−0.013, +0.073],
p = 0.23. Secondary: RAW+EVENTS-token-matched − RAW-token-matched = +0.047,
95% CI [+0.007, +0.087], p = 0.034. The contribution of linking is not resolved by this
sample. `results/ever/unlinked_events_control/`.

## Scope of the conclusions

Experiments 8 and 9 are mechanistic ablations on the same questions where the TP effect was
found; they are not independent replications.

## 10. Chronological order control, v2 — 2026-09-15

Protocol frozen and hashed before new predictions
(`protocols/original/EVERMEMBENCH_CHRONOLOGICAL_ORDER_CONTROL_PROTOCOL_V2.md`). Separates
context *order* from context *content* on the Temporal Duration slice: raw and event
conditions are re-packed in chronological rather than ranked order at a matched token
budget. Chronological order is worth +1.7 pp to raw and +2.3 pp to events; for episodes it
is negative (20.0 → 18.3). All three shifts are single-digit question counts on n = 300 and
are not treated as distinguishable. `results/ever/chronological_order_control/`.

## 11. Full-set unlinked events run (experiment A) — 2026-09-15

The event condition extended from the 300-question slice to all 2,400 questions, over the
same sealed memory. Accuracy 49.83% versus raw 49.46% (+0.38 pp, [−0.8, +1.6], p = .589):
no average gain. This run is also the source of the per-question evidence metrics used for
the dissociation result. `results/ever/events_full/`.

## 12. HyDE control and its token-matched amendment — 2026-09-16

Protocol and amendment frozen before any generation
(`protocols/original/EVERMEMBENCH_HYDE_TOKEN_MATCHED_AMENDMENT.md`). The amendment was
written because the registered comparison mixed two confounds — 2,456 versus ~1,052 context
tokens and chronological versus ranked order — that the budget and order controls exist to
remove. Experiment C (HyDE at top-10) was left untouched; C2 adds a token- and order-matched
HyDE arm built from C's sealed generations. Accuracy: HyDE 14.0%, raw 14.0%, events 19.3%.
Query-side expansion buys recall (+1.61 pp over matched raw) and no precision; events buy
both, and deliver +6.68 pp denser evidence than HyDE at indistinguishable recall.
`results/ever/hyde_raw/`, `results/ever/hyde_token_matched/`.

## 13. GroupMemBench empty-answer repair — 2026-09-16

102 of 1,490 gpt-5 generations came back empty because the output budget was consumed by
hidden reasoning (94% of repair output tokens). All 102 were regenerated from the same
sealed prompts with a larger budget; the other 1,388 answers and verdicts were not touched.
The negative transfer is not an artifact of the empty answers: the registered primary goes
from .340→.300 to .373→.333, delta unchanged at −4.0 pp [−9.3, +1.3], p = .210. The original
protocol result is retained unchanged in `results/group/`; the amendment is in
`results/group/repair_v2/` as aggregates and checksums only, per GroupMemBench's licensing.

## 14. Evidence-delivery endpoint and the registered frontier check — 2026-09-16

Two things happened here, and the order matters.

First, an explanation offered for the Temporal Duration accuracy effect — that accuracy
follows the recall/precision frontier of delivered evidence — was turned into a falsifiable
prediction and registered before computation
(`protocols/original/FRONTIER_MECHANISM_PREDICTION_PROTOCOL.md`, sha256 `0419cccb…`), with
its reading rule and power ceilings fixed in advance. On the 2,100 questions outside the
discovery slice the prediction **failed**: where events deliver strictly better evidence
(n = 650) accuracy gains +0.77 pp, p = .649. Per the registered rule the frontier lost the
status of an explanation. Sensitivity is bounded and stated: 77 discordant pairs in that
stratum, minimum detectable effect ≈ 2.9 pp, so this is an absence of confirmation rather
than a demonstrated zero.

Second, the evidence endpoint itself was analysed paired and per question across the whole
set, and it is the one result that holds: +3.21 pp precision and +0.64 pp recall over all
2,400 questions, by dominance rather than trade-off, positive in all nine categories,
replicated on SocialMemBench and dominating matched HyDE. Together these give the
dissociation the manuscript now reports as its main result. Recompute with
`analysis/verify_evidence_endpoint.py` (24 checks, offline).
