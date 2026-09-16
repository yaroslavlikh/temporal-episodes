# Final sprint experiment B2: RAW+EPISODES-chrono

- protocol sha256 `bf278ba6213dccfc904524d1949b5597053175e31f751c2d081903c3f6e25029`; runner sha256 `37f36b07879f88f7c2654136e79262bb1d1269e209b6b2adb128bd1e1dfeff4e`
- questions: 300; answers reused from sealed caches: 14
- Temporal Duration is a post-hoc discovery slice; every TP result here is exploratory.

## Conditions

| condition | n | accuracy % | evidence recall % | evidence precision % | unique sources | context tokens | answer ms |
|---|---:|---:|---:|---:|---:|---:|---:|
| RAW+EPISODES-chrono | 300 | 18.3 | 20.5 | 31.1 | 17.4 | 2460 | 1122 |
| RAW | 300 | 12.3 | 12.7 | 29.6 | 10.0 | -- | 1115 |
| RAW+EPISODES | 300 | 20.0 | 20.5 | 31.1 | 17.4 | -- | 1137 |
| RAW-token-matched-chrono | 300 | 14.0 | 19.1 | 21.5 | 23.8 | 2458 | 1137 |
| RAW+EVENTS-token-matched-chrono | 300 | 19.3 | 19.7 | 29.3 | 17.4 | 2456 | 1160 |

## Paired comparisons (pp)

| difference | delta | question 95% CI | McNemar p | left-only / right-only / both / neither | project 95% CI | per-project | sign-flip p |
|---|---:|---|---:|---|---|---|---:|
| RAW+EPISODES-chrono - RAW+EPISODES | -1.7 | [-5.7, +2.3] | 0.5224 | 17 / 22 / 38 / 223 | [-4.3, +1.7] | 01: +5.0, 02: -1.7, 03: -5.0, 04: -5.0, 05: -1.7 | 0.4375 |
| RAW+EPISODES-chrono - RAW+EVENTS-token-matched-chrono | -1.0 | [-5.0, +3.3] | 0.7552 | 19 / 22 / 36 / 223 | [-3.0, +0.0] | 01: +0.0, 02: -5.0, 03: +0.0, 04: +0.0, 05: +0.0 | 1.0000 |
| RAW+EPISODES-chrono - RAW-token-matched-chrono | +4.3 | [+0.0, +9.0] | 0.0854 | 31 / 18 / 24 / 227 | [+0.0, +8.0] | 01: +3.3, 02: +6.7, 03: +10.0, 04: -3.3, 05: +5.0 | 0.1875 |

## Cost

- API calls: 407; list-price estimate USD 0.3883
- by model: `{"google/gemini-3-flash-preview": {"calls": 121, "duration_ms": 135606.93812335376, "estimated_usd": 0.0477275, "input_tokens": 65089, "output_tokens": 5061}, "openai/gpt-4.1-mini": {"calls": 286, "duration_ms": 336034.19075068086, "estimated_usd": 0.3405492, "input_tokens": 833909, "output_tokens": 4366}}`
- OpenRouter key usage delta: 0.3795181999999997 (OpenRouter key usage; includes any concurrent use of the same key)
