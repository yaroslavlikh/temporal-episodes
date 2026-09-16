# EverMemBench Temporal control v2: chronological order of the same retrieved context

- protocol: `EVERMEMBENCH_CHRONOLOGICAL_ORDER_CONTROL_PROTOCOL_V2.md` sha256 `557f75a9074b0c981be106b11efc25e69f94bdf931cbc09105b6475a144124ca`
- runner sha256: `3378d1904cce3f84a0547b4f98263359ce38ef662c17ddf92e8c41a8848a5503`; inputs sha256 `89b7264be4d401b750e10725cb3361ca6273d4254a707d17ac601fe8cd3b6223`
- references: RAW and RAW+EPISODES from `evermembench_temporal_episodes_official_v1_20260915_021550_MSK`; RAW-token-matched from `evermembench_temporal_budget_control_v1_20260915_021134_MSK`; RAW+EVENTS-token-matched from `evermembench_unlinked_events_control_v1_20260915_022532_MSK`
- questions: 300 Temporal Duration; bootstrap 20000 samples, seed 20260912

## Conditions

| condition | n | accuracy % | context tokens | unique raw sources | order changed | evidence recall % | evidence precision % | answer ms | judge ms | answer markers | judge parse | judge re-requested |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---:|
| RAW | 300 | 12.3 | 1052 | 10.0 | -- | 12.7 | 29.6 | 1115 | -- | `{"[EMPTY]": 0, "[INVALID]": 0, "[FAILED]": 0}` | `{"json": 300}` | 0 |
| RAW-token-matched | 300 | 12.3 | 2458 | 23.8 | -- | 19.1 | 21.5 | 1107 | -- | `{"[EMPTY]": 0, "[INVALID]": 0, "[FAILED]": 0}` | `{"json": 300}` | 0 |
| RAW-token-matched-chrono (primary control) | 300 | 14.0 | 2458 | 23.8 | 1.000 | 19.1 | 21.5 | 1137 | 1108 | `{"[EMPTY]": 0, "[INVALID]": 0, "[FAILED]": 0}` | `{"json": 300}` | 0 |
| RAW-token-matched-chrono-relative (exploratory) | 300 | 8.3 | 2577 | 23.8 | 1.000 | 19.1 | 21.5 | 1141 | 997 | `{"[EMPTY]": 0, "[INVALID]": 0, "[FAILED]": 0}` | `{"json": 300}` | 0 |
| RAW+EVENTS-token-matched | 300 | 17.0 | 2456 | 17.4 | -- | 19.7 | 29.3 | 1039 | -- | `{"[EMPTY]": 0, "[INVALID]": 0, "[FAILED]": 0}` | `{"json": 300}` | 0 |
| RAW+EVENTS-token-matched-chrono | 300 | 19.3 | 2456 | 17.4 | 1.000 | 19.7 | 29.3 | 1160 | 1064 | `{"[EMPTY]": 0, "[INVALID]": 0, "[FAILED]": 0}` | `{"json": 300}` | 0 |
| RAW+EPISODES | 300 | 20.0 | 2460 | 17.4 | -- | 20.5 | 31.1 | 1137 | -- | `{"[EMPTY]": 0, "[INVALID]": 0, "[FAILED]": 0}` | `{"json": 300}` | 0 |

## Paired comparisons (pp)

| role | difference | left % | right % | delta | question 95% CI | McNemar p | left-only / right-only / both correct / both wrong | project 95% CI | per-project deltas | sign-flip p |
|---|---|---:|---:|---:|---|---:|---|---|---|---:|
| **primary** | RAW+EPISODES − RAW-token-matched-chrono | 20.0 | 14.0 | +6.0 | [+1.0, +11.0] | 0.0247 | 38 / 20 / 22 / 220 | [+1.3, +11.0] | 01: -1.7, 02: +8.3, 03: +15.0, 04: +1.7, 05: +6.7 | 0.1875 |
| secondary: ordering, raw | RAW-token-matched-chrono − RAW-token-matched | 14.0 | 12.3 | +1.7 | [-2.0, +5.3] | 0.4869 | 19 / 14 / 23 / 244 | [-1.7, +6.0] | 01: +10.0, 02: +1.7, 03: -3.3, 04: +0.0, 05: +0.0 | 0.7500 |
| secondary: ordering, events | RAW+EVENTS-token-matched-chrono − RAW+EVENTS-token-matched | 19.3 | 17.0 | +2.3 | [-2.0, +6.7] | 0.3713 | 26 / 19 / 32 / 223 | [+1.0, +4.0] | 01: +5.0, 02: +1.7, 03: +1.7, 04: +0.0, 05: +3.3 | 0.1250 |
| secondary: linking beyond ordered events | RAW+EPISODES − RAW+EVENTS-token-matched-chrono | 20.0 | 19.3 | +0.7 | [-4.0, +5.3] | 0.8877 | 26 / 24 / 34 / 216 | [-3.0, +4.3] | 01: -5.0, 02: -3.3, 03: +5.0, 04: +5.0, 05: +1.7 | 0.8125 |
| secondary: events beyond raw, both ordered | RAW+EVENTS-token-matched-chrono − RAW-token-matched-chrono | 19.3 | 14.0 | +5.3 | [+0.7, +10.0] | 0.0402 | 35 / 19 / 23 / 223 | [+0.7, +9.7] | 01: +3.3, 02: +11.7, 03: +10.0, 04: -3.3, 05: +5.0 | 0.1875 |
| exploratory: day offsets | RAW-token-matched-chrono-relative − RAW-token-matched-chrono | 8.3 | 14.0 | -5.7 | [-10.0, -1.7] | 0.0115 | 12 / 29 / 13 / 246 | [-8.3, -3.0] | 01: -10.0, 02: -8.3, 03: -3.3, 04: -5.0, 05: -1.7 | 0.0625 |
| exploratory | RAW+EPISODES − RAW-token-matched-chrono-relative | 20.0 | 8.3 | +11.7 | [+6.7, +16.7] | 0.0000 | 50 / 15 / 10 / 225 | [+7.7, +16.0] | 01: +8.3, 02: +16.7, 03: +18.3, 04: +6.7, 05: +8.3 | 0.0625 |

Sign-flip note: five projects: the smallest attainable two-sided sign-flip p is 0.0625; the project bootstrap has five clusters and is descriptive.

## Per-project accuracy (%)

| project | RAW | RAW-token-matched | RAW-token-matched-chrono | RAW-token-matched-chrono-relative | RAW+EVENTS-token-matched | RAW+EVENTS-token-matched-chrono | RAW+EPISODES |
|---|---:|---:|---:|---:|---:|---:|---:|
| 01 | 11.7 | 5.0 | 15.0 | 5.0 | 13.3 | 18.3 | 13.3 |
| 02 | 11.7 | 13.3 | 15.0 | 6.7 | 25.0 | 26.7 | 23.3 |
| 03 | 13.3 | 13.3 | 10.0 | 6.7 | 18.3 | 20.0 | 25.0 |
| 04 | 11.7 | 16.7 | 16.7 | 11.7 | 13.3 | 13.3 | 18.3 |
| 05 | 13.3 | 13.3 | 13.3 | 11.7 | 15.0 | 18.3 | 20.0 |

## Interpretation rules fixed before new outcomes

- primary 95% CI [+1.0, +11.0]: **the episode gain is not reproduced by chronological ordering of the equal-token raw context**.
- RAW-token-matched-chrono accuracy 14.0%: **supports a contribution of event representation beyond context volume and order**.
- RAW+EPISODES − RAW+EVENTS-token-matched-chrono 95% CI [-4.0, +5.3]: **an independent contribution of episode linking is not established**.

## Cost (new work in this directory)

- API calls: 1691; list-price estimate USD 1.3489
- by model: `{"google/gemini-3-flash-preview": {"calls": 800, "duration_ms": 950224.1431181319, "estimated_usd": 0.2988825, "input_tokens": 404511, "output_tokens": 32209}, "openai/gpt-4.1-mini": {"calls": 891, "duration_ms": 1043277.3562927032, "estimated_usd": 1.0500536, "input_tokens": 2580722, "output_tokens": 11103}}`
- OpenRouter key usage: before 6.2736542, after 7.5897552, delta 1.3161009999999997 (OpenRouter key usage; includes any concurrent use of the same key)
