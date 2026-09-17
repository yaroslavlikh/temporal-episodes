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
Measurement defect found after scoring: 102 of 1,490 gpt-5 answers were empty because hidden
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
the evidence-delivery result. `results/ever/events_full/`.

## 12. HyDE control and its token-matched amendment — 2026-09-16

Protocol and amendment frozen before any generation
(`protocols/original/EVERMEMBENCH_HYDE_TOKEN_MATCHED_AMENDMENT.md`). The amendment was
written because the registered comparison mixed two confounds — 2,456 versus ~1,052 context
tokens and chronological versus ranked order — that the budget and order controls exist to
remove. Experiment C (HyDE at top-10) was left untouched; C2 adds a token- and order-matched
HyDE arm built from C's sealed generations. Accuracy: HyDE 14.0%, raw 14.0%, events 19.3%.
Over matched raw, query-side expansion raises recall by +1.61 pp and precision by +1.18 pp. At a
similar recall (events − HyDE −1.01 pp, CI [−2.20, +0.17]) events deliver +6.68 pp denser
evidence; dominance on both coordinates is not established.
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
2,400 questions, with fewer sources and more gold hits rather than a trade-off, positive in
all nine categories and supported on SocialMemBench. Together these give the manuscript's
separation of the two endpoints: delivery improves, transfer to accuracy is not confirmed. Recompute with
`analysis/verify_evidence_endpoint.py` (offline).

## 15. Editorial verification of the manuscript — 2026-09-17

An offline read-only pass over the sealed artifacts before release; no new generations.
Findings that changed the text:

- **GroupMemBench has no gold evidence.** None of its 745 questions carries source IDs or
  evidence spans, so evidence delivery cannot be measured there. An earlier statement in this
  repository that the Group runner "stored verdicts only" misattributed the gap.
- **Robustness of delivery by project.** Events − RAW precision is positive in each of the
  five EverMemBench projects (+2.50 to +3.61 pp); leaving out any one project keeps the mean
  within +3.11 to +3.39 pp. This is sensitivity on this set, not a new registered endpoint.
- **SocialMemBench intervals** for delivery were recomputed with a network bootstrap
  (10,000 resamples of 43 networks, seed 20260917): flat +0.90 [+0.66, +1.19], versioned
  +0.86 [+0.61, +1.16], episodes +0.34 [+0.15, +0.54].
- **Statistics.** The extreme Wilcoxon p-values of an earlier draft were dropped (the helper
  used then did not average tied ranks); effect sizes and bootstrap intervals do not depend on
  it. The Temporal Duration correction is reported as Bonferroni over nine categories
  (.0402 → about .36, .0479 → about .43); with five projects the exact sign-flip test cannot
  reach p < .05 (minimum .0625).
- **Recall versus accuracy.** Gold annotation has a median of 27 anchors per question
  (IQR 21–37, max 96) against ten returned sources; 316 RAW, 312 EVENTS and 305 EPISODES
  answers are judged correct with zero delivered gold anchors.

`paper/preprint_ru/verify_editorial.py` produced `editorial_verification.json`; the public
checks are in `analysis/verify_evidence_endpoint.py`.

## 16. k-sweep: retrieval depth and accuracy — 2026-09-17

Question: is accuracy insensitive to delivery only at k = 10? Hard budget $1 for paid calls,
sealed directories read only, same answer/judge models, prompts and scoring as the official run.

Phase 1 (offline, 0 API calls). Delivery for RAW and RAW+EVENTS at k = 10, 20, 40 on all
2,400 questions; the k = 10 rows match the sealed per-question metrics exactly. Events − RAW
precision +3.21 / +2.51 / +1.68 pp, all intervals above zero, positive in all five projects at
each k; events never deliver more sources. RAW gold hits per question rise 2.13 → 3.14 → 4.40.

Phase 2 (paid). Stratified sample N = 304 over the nine categories, seed 20260917, sample
and manifest frozen before any call; k = 10 verdicts reused from the sealed runs, k = 20
answered and judged anew. Accuracy RAW 49.01 → 48.68, RAW+EVENTS 49.01 → 48.36; RAW@20 −
RAW@10 −0.33 pp [−4.28, +3.29]; every interval includes zero. Spend $0.7947 with the
OpenRouter fee factor ($0.7225 at list price), booked per call by a budget guard from
`response.usage`. The API usage log shows $0.7118 because 66 identical prompts (no event
document in the top 20) were sent concurrently and the cache logs such payloads once; earlier
parallel runs may undercount usage the same way (not checked).

`results/ever/ksweep/`; recompute with `analysis/verify_ksweep.py` (55 checks, offline).
