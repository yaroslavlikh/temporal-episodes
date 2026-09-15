# GroupMemBench — RAW vs TemporalEpisodes

- official source: `e2682e01ff490acfe4fac2940159dce60307dfc9`
- answer/judge: `gpt-5` (official prompts)
- retrieval: `text-embedding-3-large`, unified cosine top-10
- memory builder: `gpt-4o-mini-2024-07-18`, query-independent, chunk=40

## Pre-registered primary endpoint

Filtered Finance+Technology, knowledge_update+temporal combined.

- RAW: 0.340
- RAW+EPISODES: 0.300
- paired delta: -0.040, question bootstrap 95% CI [-0.093, +0.013]
- exact paired McNemar: EP-only=6, RAW-only=12, p=0.237885

## All cells

| split | domain | qtype | n | RAW | EPISODES | delta |
|---|---|---|---:|---:|---:|---:|
| primary/filtered | Finance | multi_hop | 48 | 0.562 | 0.562 | +0.000 |
| primary/filtered | Finance | knowledge_update | 32 | 0.344 | 0.312 | -0.031 |
| primary/filtered | Finance | temporal | 45 | 0.511 | 0.422 | -0.089 |
| primary/filtered | Finance | user_implicit | 15 | 0.600 | 0.667 | +0.067 |
| primary/filtered | Finance | term_ambiguity | 45 | 0.244 | 0.289 | +0.044 |
| primary/filtered | Finance | abstention | 29 | 0.690 | 0.724 | +0.034 |
| primary/filtered | Technology | multi_hop | 41 | 0.317 | 0.293 | -0.024 |
| primary/filtered | Technology | knowledge_update | 36 | 0.222 | 0.250 | +0.028 |
| primary/filtered | Technology | temporal | 37 | 0.243 | 0.189 | -0.054 |
| primary/filtered | Technology | user_implicit | 28 | 0.464 | 0.464 | +0.000 |
| primary/filtered | Technology | term_ambiguity | 43 | 0.279 | 0.209 | -0.070 |
| primary/filtered | Technology | abstention | 28 | 0.821 | 0.786 | -0.036 |
| robustness/unfiltered | Healthcare | multi_hop | 48 | 0.250 | 0.229 | -0.021 |
| robustness/unfiltered | Healthcare | knowledge_update | 17 | 0.353 | 0.176 | -0.176 |
| robustness/unfiltered | Healthcare | temporal | 37 | 0.162 | 0.243 | +0.081 |
| robustness/unfiltered | Healthcare | user_implicit | 2 | 0.500 | 0.500 | +0.000 |
| robustness/unfiltered | Healthcare | term_ambiguity | 7 | 0.143 | 0.000 | -0.143 |
| robustness/unfiltered | Healthcare | abstention | 34 | 0.824 | 0.941 | +0.118 |
| robustness/unfiltered | Manufacturing | multi_hop | 45 | 0.356 | 0.267 | -0.089 |
| robustness/unfiltered | Manufacturing | knowledge_update | 22 | 0.182 | 0.091 | -0.091 |
| robustness/unfiltered | Manufacturing | temporal | 43 | 0.372 | 0.395 | +0.023 |
| robustness/unfiltered | Manufacturing | user_implicit | 4 | 0.250 | 0.000 | -0.250 |
| robustness/unfiltered | Manufacturing | term_ambiguity | 11 | 0.273 | 0.273 | +0.000 |
| robustness/unfiltered | Manufacturing | abstention | 48 | 0.833 | 0.792 | -0.042 |

## Efficiency artifacts

- API calls recorded: 28317
- usage by model: `{"gpt-4o-mini-2024-07-18": {"calls": 24556, "duration_ms": 126704544.49629217, "estimated_usd": 6.69628485, "input_tokens": 29656079, "output_tokens": 3746455}, "gpt-5": {"calls": 2713, "duration_ms": 27821109.808764387, "estimated_usd": 24.93541, "input_tokens": 3267664, "output_tokens": 2085083}, "text-embedding-3-large": {"calls": 1048, "duration_ms": 1720083.6168405367, "estimated_usd": 1.0030066800000002, "input_tokens": 7715436, "output_tokens": 0}}`
- estimated API cost (uncached-rate upper bound, USD): 32.6347
- price snapshot: 2026-09-12; standard uncached list rates; excludes local compute
- retrieval latency by condition: `{"RAW": {"mean_ms": 67.95024553051331, "n": 745, "p50_ms": 62.80708301346749, "p95_ms": 140.32903283368793}, "RAW+EPISODES": {"mean_ms": 78.67583276832089, "n": 745, "p50_ms": 66.74608308821917, "p95_ms": 190.24252495728413}}`
- episode snapshot bytes: 14987700

## Interpretation guardrails

- Finance/Technology are the confirmatory filtered split.
- Healthcare/Manufacturing are unfiltered robustness data and are not pooled into the primary claim.
- Memory was sealed before question files were opened; raw provenance is embedded in every derived passage.
- This is an adapter evaluation under the official harness, not a leaderboard submission.
