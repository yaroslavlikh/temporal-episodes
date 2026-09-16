# Final sprint experiment A: RAW+EVENTS

- protocol sha256 `bf278ba6213dccfc904524d1949b5597053175e31f751c2d081903c3f6e25029`; runner sha256 `37f36b07879f88f7c2654136e79262bb1d1269e209b6b2adb128bd1e1dfeff4e`
- questions: 2400; answers reused from sealed caches: 1068
- Temporal Duration is a post-hoc discovery slice; every TP result here is exploratory.

## Conditions

| condition | n | accuracy % | evidence recall % | evidence precision % | unique sources | context tokens | answer ms |
|---|---:|---:|---:|---:|---:|---:|---:|
| RAW+EVENTS | 2400 | 49.8 | 8.7 | 24.5 | 9.5 | 1177 | 578 |
| RAW | 2400 | 49.5 | 8.1 | 21.3 | 10.0 | -- | 991 |
| RAW+EPISODES | 2400 | 50.2 | 10.8 | 22.4 | 12.4 | -- | 1018 |

## Paired comparisons (pp)

| difference | delta | question 95% CI | McNemar p | left-only / right-only / both / neither | project 95% CI | per-project | sign-flip p |
|---|---:|---|---:|---|---|---|---:|
| RAW+EVENTS - RAW | +0.4 | [-0.8, +1.6] | 0.5889 | 114 / 105 / 1082 / 1099 | [-0.1, +0.9] | 01: -0.4, 02: +0.6, 03: +0.9, 04: -0.2, 05: +1.0 | 0.2500 |
| RAW+EVENTS - RAW+EPISODES | -0.4 | [-1.5, +0.8] | 0.5727 | 96 / 105 / 1100 / 1099 | [-1.3, +0.6] | 01: +0.6, 02: -1.9, 03: +0.0, 04: -1.5, 05: +0.8 | 0.5000 |

## By official category (RAW+EVENTS vs RAW)

| category | n | RAW % | RAW+EPISODES % | RAW+EVENTS % | delta vs RAW | 95% CI | McNemar p |
|---|---:|---:|---:|---:|---:|---|---:|
| C | 402 | 79.9 | 79.6 | 79.1 | -0.7 | [-2.5, +1.0] | 0.5811 |
| MH | 249 | 12.9 | 13.3 | 13.3 | +0.4 | [-3.6, +4.4] | 1.0000 |
| P | 427 | 65.8 | 64.2 | 64.6 | -1.2 | [-3.3, +0.7] | 0.3593 |
| SH | 213 | 89.7 | 87.8 | 89.7 | +0.0 | [-3.8, +3.8] | 1.0000 |
| Skill | 169 | 33.7 | 30.8 | 32.0 | -1.8 | [-6.5, +3.0] | 0.6072 |
| Style | 176 | 30.1 | 38.1 | 33.5 | +3.4 | [-1.7, +8.5] | 0.2632 |
| TP (post-hoc slice) | 300 | 12.3 | 20.0 | 16.3 | +4.0 | [-0.7, +8.7] | 0.1263 |
| Title | 196 | 46.4 | 43.4 | 45.9 | -0.5 | [-5.1, +4.1] | 1.0000 |
| U | 268 | 46.3 | 47.4 | 47.0 | +0.7 | [-3.4, +5.2] | 0.8642 |

| RAW+EVENTS - RAW, all except TP | -0.1 | [-1.3, +1.1] | 0.8771 | 82 / 85 / 1065 / 868 | [-0.7, +0.5] | 01: -0.7, 02: -0.7, 03: -0.5, 04: +0.0, 05: +1.2 | 0.6250 |

## Cost

- API calls: 1532; list-price estimate USD 1.0382
- by model: `{"google/gemini-3-flash-preview": {"calls": 200, "duration_ms": 235412.01895708218, "estimated_usd": 0.075966, "input_tokens": 95880, "output_tokens": 9342}, "openai/gpt-4.1-mini": {"calls": 1332, "duration_ms": 1385144.261486712, "estimated_usd": 0.9622352000000001, "input_tokens": 2385768, "output_tokens": 4955}}`
- OpenRouter key usage delta: 1.019027200000001 (OpenRouter key usage; includes any concurrent use of the same key)
