# EverMemBench Temporal budget control

- protocol: `EVERMEMBENCH_TEMPORAL_BUDGET_CONTROL_PROTOCOL.md` sha256 `301ea5a7fe3f05342842595c9b55676bc655864e89c9e287202458437312a628`
- runner sha256: `522ad5416c2566139ba4647cf19d288a62e2511bd99d22382348ebe7447c31c6`
- source run: `evermembench_temporal_episodes_official_v1` (sealed RAW and RAW+EPISODES rows)
- questions: 300 Temporal Duration (`TP`); tokens: `o200k_base`

## Conditions

| condition | n | accuracy | mean unique raw sources | mean context tokens | evidence recall | evidence precision |
|---|---:|---:|---:|---:|---:|---:|
| RAW | 300 | 0.123 | 10.0 | 1052 | 0.127 | 0.296 |
| RAW+EPISODES | 300 | 0.200 | 17.4 | 2460 | 0.205 | 0.311 |
| RAW-count-matched | 300 | 0.133 | 17.4 | 1814 | 0.166 | 0.251 |
| RAW-token-matched | 300 | 0.123 | 23.8 | 2458 | 0.191 | 0.215 |
| RAW+EPISODES-rerun | 300 | 0.200 | 17.4 | 2460 | 0.205 | 0.311 |

## Paired comparisons

| role | difference | delta | 95% CI | left-only / right-only | McNemar p |
|---|---|---:|---:|---:|---:|
| **primary** | RAW+EPISODES − RAW-token-matched | +0.077 | [+0.033, +0.120] | 35 / 12 | 0.0011 |
| secondary | RAW+EPISODES − RAW-count-matched | +0.067 | [+0.020, +0.117] | 38 / 18 | 0.0105 |
| secondary | RAW-token-matched − RAW | +0.000 | [-0.037, +0.037] | 16 / 16 | 1.0000 |
| secondary | RAW-count-matched − RAW | +0.010 | [-0.023, +0.043] | 15 / 12 | 0.7011 |
| calibration | RAW+EPISODES-rerun − RAW+EPISODES | +0.000 | [-0.023, +0.023] | 6 / 6 | 1.0000 |
| same-run check | RAW+EPISODES-rerun − RAW-token-matched | +0.077 | [+0.033, +0.123] | 36 / 13 | 0.0014 |

## Pre-registered interpretation

- primary 95% CI [+0.033, +0.120]: **episodes add accuracy beyond an equal-token raw context**.
- calibration: rerun − sealed RAW+EPISODES = +0.000; per-question agreement 96.0%; within the pre-registered noise bounds.

## Cost and latency (new conditions only)

- API calls: 1685; estimated USD (uncached list prices): 1.2525
- usage by model: `{"google/gemini-3-flash-preview": {"calls": 818, "duration_ms": 872936.1118476372, "estimated_usd": 0.306922, "input_tokens": 414218, "output_tokens": 33271}, "openai/gpt-4.1-mini": {"calls": 867, "duration_ms": 976629.9606176326, "estimated_usd": 0.9455688000000001, "input_tokens": 2317126, "output_tokens": 11699}}`
- raw ranking latency: `{"RAW+EPISODES-rerun": {"mean_ms": 11.52143390228351, "n": 300, "p50_ms": 11.322958453092724, "p95_ms": 11.971208348404616}, "RAW-count-matched": {"mean_ms": 11.52143390228351, "n": 300, "p50_ms": 11.322958453092724, "p95_ms": 11.971208348404616}, "RAW-token-matched": {"mean_ms": 11.52143390228351, "n": 300, "p50_ms": 11.322958453092724, "p95_ms": 11.971208348404616}}`
- context selection ms (mean): `{"RAW+EPISODES-rerun": 0.0, "RAW-count-matched": 0.0029626108395556607, "RAW-token-matched": 11.816587755844617}`
- answer wall ms (mean, includes cache hits): `{"RAW+EPISODES-rerun": 1140.1050562725868, "RAW-count-matched": 1128.0330092925578, "RAW-token-matched": 1106.6709255776368}`
- judge: parse `{"json": 900}`, re-requested 0
- results sealed: True
