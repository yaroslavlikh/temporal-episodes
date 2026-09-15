# EverMemBench Temporal ablation: linked episodes versus unlinked events

- protocol: `EVERMEMBENCH_UNLINKED_EVENTS_CONTROL_PROTOCOL.md` sha256 `ab900c52bb49c63817de12649e1241089a9d63892e9a171723bd955b75bbf405`
- runner sha256: `df0b02827fedd40487bef66eaa659fc81f81a5659f3717ad5e799c756df0746b`
- event index meta sha256: `7c560190ff465b49e0433bfe79836e7ffa6e3b4b6924ca0e88e25d2ebd1f48f1`
- sealed rows: RAW and RAW+EPISODES from `evermembench_temporal_episodes_official_v1`; RAW-token-matched from `evermembench_temporal_budget_control_v1_20260915_021134_MSK`
- questions: 300 Temporal Duration (`TP`); tokens: `o200k_base`

## Conditions

| condition | n | accuracy | mean unique raw sources | mean context tokens | mean derived docs | evidence recall | evidence precision |
|---|---:|---:|---:|---:|---:|---:|---:|
| RAW | 300 | 0.123 | 10.0 | 1052 | 0.0 | 0.127 | 0.296 |
| RAW+EPISODES | 300 | 0.200 | 17.4 | 2460 | 4.0 | 0.205 | 0.311 |
| RAW-token-matched | 300 | 0.123 | 23.8 | 2458 | 0.0 | 0.191 | 0.215 |
| RAW+EVENTS | 300 | 0.163 | 9.2 | 1316 | 4.5 | 0.150 | 0.371 |
| RAW+EVENTS-token-matched | 300 | 0.170 | 17.4 | 2456 | 8.4 | 0.197 | 0.293 |

## Paired comparisons

| role | difference | delta | 95% CI | left-only / right-only | McNemar p |
|---|---|---:|---:|---:|---:|
| **primary** | RAW+EPISODES − RAW+EVENTS-token-matched | +0.030 | [-0.013, +0.073] | 27 / 18 | 0.2327 |
| secondary | RAW+EPISODES − RAW+EVENTS | +0.037 | [-0.007, +0.080] | 29 / 18 | 0.1439 |
| secondary | RAW+EVENTS-token-matched − RAW-token-matched | +0.047 | [+0.007, +0.087] | 26 / 12 | 0.0336 |
| secondary | RAW+EVENTS − RAW | +0.040 | [-0.007, +0.087] | 32 / 20 | 0.1263 |

## Interpretation rule fixed before new outcomes

- primary 95% CI [-0.013, +0.073]: **the linking effect is not distinguishable from event summaries alone**.

## Cost and latency (new work only)

- answer and judge API calls: 1135; estimated USD: 0.7545
- event index embedding calls: 134; estimated USD: 0.0930
- usage by model: `{"google/gemini-3-flash-preview": {"calls": 557, "duration_ms": 581377.8079167241, "estimated_usd": 0.2093695, "input_tokens": 283049, "output_tokens": 22615}, "openai/gpt-4.1-mini": {"calls": 578, "duration_ms": 582264.9859099183, "estimated_usd": 0.545144, "input_tokens": 1328764, "output_tokens": 8524}}`
- unified ranking latency: `{"RAW+EVENTS": {"mean_ms": 15.877429726533592, "n": 300, "p50_ms": 15.21541696274653, "p95_ms": 16.85236486955546}, "RAW+EVENTS-token-matched": {"mean_ms": 15.877429726533592, "n": 300, "p50_ms": 15.21541696274653, "p95_ms": 16.85236486955546}}`
- context selection ms (mean): `{"RAW+EVENTS": 0.0, "RAW+EVENTS-token-matched": 9.578867654393738}`
- judge: parse `{"json": 600}`, re-requested 0
