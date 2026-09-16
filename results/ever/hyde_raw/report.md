# Final sprint experiment C: HyDE-RAW

- protocol sha256 `bf278ba6213dccfc904524d1949b5597053175e31f751c2d081903c3f6e25029`; runner sha256 `ad8cfb90f5c818d973a9a4e4f28b5641c341f04641e59a16c3ead00a8c03a3fd`
- questions: 300; answers reused from sealed caches: 0
- Temporal Duration is a post-hoc discovery slice; every TP result here is exploratory.

## Conditions

| condition | n | accuracy % | evidence recall % | evidence precision % | unique sources | context tokens | answer ms |
|---|---:|---:|---:|---:|---:|---:|---:|
| HyDE-RAW | 300 | 12.0 | 14.1 | 32.4 | 10.0 | 1034 | 961 |
| RAW | 300 | 12.3 | 12.7 | 29.6 | 10.0 | -- | 1115 |
| RAW-token-matched-chrono | 300 | 14.0 | 19.1 | 21.5 | 23.8 | 2458 | 1137 |
| RAW+EVENTS-token-matched-chrono | 300 | 19.3 | 19.7 | 29.3 | 17.4 | 2456 | 1160 |

## Paired comparisons (pp)

| difference | delta | question 95% CI | McNemar p | left-only / right-only / both / neither | project 95% CI | per-project | sign-flip p |
|---|---:|---|---:|---|---|---|---:|
| HyDE-RAW - RAW | -0.3 | [-4.7, +4.0] | 1.0000 | 22 / 23 / 14 / 241 | [-3.0, +2.0] | 01: +0.0, 02: +3.3, 03: -5.0, 04: +0.0, 05: +0.0 | 1.0000 |
| RAW+EVENTS-token-matched-chrono - HyDE-RAW | +7.3 | [+2.3, +12.7] | 0.0092 | 44 / 22 / 14 / 220 | [+4.0, +10.7] | 01: +6.7, 02: +11.7, 03: +11.7, 04: +1.7, 05: +5.0 | 0.0625 |
| RAW+EVENTS-token-matched-chrono - RAW | +7.0 | [+2.0, +12.0] | 0.0086 | 40 / 19 / 18 / 223 | [+3.7, +11.3] | 01: +6.7, 02: +15.0, 03: +6.7, 04: +1.7, 05: +5.0 | 0.0625 |

## Cost

- API calls: 797; list-price estimate USD 0.2973
- by model: `{"google/gemini-3-flash-preview": {"calls": 194, "duration_ms": 193800.90171226766, "estimated_usd": 0.0737065, "input_tokens": 99899, "output_tokens": 7919}, "openai/gpt-4.1-mini": {"calls": 600, "duration_ms": 704455.9158419725, "estimated_usd": 0.22109840000000003, "input_tokens": 459878, "output_tokens": 23217}, "text-embedding-3-large": {"calls": 3, "duration_ms": 6215.191041002981, "estimated_usd": 0.00251823, "input_tokens": 19371, "output_tokens": 0}}`
- OpenRouter key usage delta: 0.5442360999999991 (OpenRouter key usage; includes any concurrent use of the same key)
