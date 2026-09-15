# EverMemBench-Dynamic — RAW vs TemporalEpisodes

- official code: `e10b3d52f0e4cfc5c124ad406b5d95c59c73738b`; official data: `a6b210a32248e841967b7b64a64281d2ff3f669d`
- answer: `openai/gpt-4.1-mini`; judge: `google/gemini-3-flash-preview`; official prompts/provider pinning
- retrieval: `text-embedding-3-large`, unified cosine top-10
- memory builder: `gpt-4o-mini-2024-07-18`, query-independent day-group sessions

## Primary endpoint (all 2,400 QA)

- RAW: 0.495
- RAW+EPISODES: 0.502
- paired delta: +0.007, question bootstrap 95% CI [-0.005, +0.020]
- equal-topic delta: +0.008, topic-cluster bootstrap 95% CI [-0.003, +0.018]
- exact paired McNemar: EP-only=121, RAW-only=103, p=0.255965

## By batch and question form

| slice | n | RAW | EPISODES | delta |
|---|---:|---:|---:|---:|
| topic 01 | 488 | 0.496 | 0.486 | -0.010 |
| topic 02 | 471 | 0.507 | 0.533 | +0.025 |
| topic 03 | 467 | 0.495 | 0.503 | +0.009 |
| topic 04 | 481 | 0.499 | 0.511 | +0.012 |
| topic 05 | 493 | 0.477 | 0.479 | +0.002 |
| multiple_choice | 1638 | 0.566 | 0.565 | -0.001 |
| open_ended | 762 | 0.341 | 0.367 | +0.026 |
| major F | 762 | 0.341 | 0.367 | +0.026 |
| major MA | 1097 | 0.662 | 0.657 | -0.005 |
| major P | 541 | 0.372 | 0.377 | +0.006 |
| minor C | 402 | 0.799 | 0.796 | -0.002 |
| minor MH | 249 | 0.129 | 0.133 | +0.004 |
| minor P | 427 | 0.658 | 0.642 | -0.016 |
| minor SH | 213 | 0.897 | 0.878 | -0.019 |
| minor Skill | 169 | 0.337 | 0.308 | -0.030 |
| minor Style | 176 | 0.301 | 0.381 | +0.080 |
| minor TP | 300 | 0.123 | 0.200 | +0.077 |
| minor Title | 196 | 0.464 | 0.434 | -0.031 |
| minor U | 268 | 0.463 | 0.474 | +0.011 |

## Retrieval provenance

- RAW evidence recall: 0.081
- EPISODES evidence recall: 0.108
- RAW evidence precision: 0.213
- EPISODES evidence precision: 0.224

## Efficiency artifacts

- API calls recorded: 26413
- usage by model: `{"google/gemini-3-flash-preview": {"calls": 1520, "duration_ms": 1540611.198216211, "estimated_usd": 0.5537675, "input_tokens": 733459, "output_tokens": 62346}, "gpt-4o-mini-2024-07-18": {"calls": 20424, "duration_ms": 37854477.566360675, "estimated_usd": 4.7570301, "input_tokens": 20112646, "output_tokens": 2900222}, "openai/gpt-4.1-mini": {"calls": 3970, "duration_ms": 3887079.928832012, "estimated_usd": 3.1162920000000005, "input_tokens": 7713302, "output_tokens": 19357}, "text-embedding-3-large": {"calls": 499, "duration_ms": 465722.1585557563, "estimated_usd": 0.45569797, "input_tokens": 3505369, "output_tokens": 0}}`
- estimated API cost (uncached-rate upper bound, USD): 8.8828
- price snapshot: 2026-09-12; standard uncached list rates; excludes local compute
- retrieval latency by condition: `{"RAW": {"mean_ms": 11.585743567266036, "n": 2400, "p50_ms": 11.280270526185632, "p95_ms": 12.699741340475157}, "RAW+EPISODES": {"mean_ms": 13.696765977947507, "n": 2400, "p50_ms": 13.312812487129122, "p95_ms": 15.038102061953394}}`
- episode snapshot bytes: 12771119

## Protocol guardrails

- Memory was sealed before QA files were opened.
- Both conditions use the same official answer/judge prompts, models and top-k.
- Every derived episode expands to mechanically validated raw evidence.
- This is an adapter evaluation under the official harness, not a leaderboard submission.

## Measurement health

Answer failure markers follow the official answerer and always score WRONG. Judge rows record finish_reason, attempts and which official parser branch produced the verdict; empty or length-cut judge output is re-requested instead of scored (see amendment evermembench_official_scoring_20260914).

- RAW: answer markers `{"[EMPTY]": 0, "[INVALID]": 0, "[FAILED]": 0}`; judge `{"finish_reason": {"cached": 20, "stop": 742}, "open_ended_judged": 762, "parse": {"json": 762}, "re_requested": 0}`
- RAW+EPISODES: answer markers `{"[EMPTY]": 0, "[INVALID]": 0, "[FAILED]": 0}`; judge `{"finish_reason": {"cached": 17, "stop": 745}, "open_ended_judged": 762, "parse": {"json": 762}, "re_requested": 0}`
