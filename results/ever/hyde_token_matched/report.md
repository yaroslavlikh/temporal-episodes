# Final sprint experiment C2: HyDE-RAW-token-matched-chrono

- protocol sha256 `bf278ba6213dccfc904524d1949b5597053175e31f751c2d081903c3f6e25029`; runner sha256 `ad8cfb90f5c818d973a9a4e4f28b5641c341f04641e59a16c3ead00a8c03a3fd`
- questions: 300; answers reused from sealed caches: 0
- Temporal Duration is a post-hoc discovery slice; every TP result here is exploratory.

## Conditions

| condition | n | accuracy % | evidence recall % | evidence precision % | unique sources | context tokens | answer ms |
|---|---:|---:|---:|---:|---:|---:|---:|
| HyDE-RAW-token-matched-chrono | 300 | 14.0 | 20.7 | 22.6 | 24.0 | 2451 | 970 |
| RAW | 300 | 12.3 | 12.7 | 29.6 | 10.0 | -- | 1115 |
| RAW-token-matched-chrono | 300 | 14.0 | 19.1 | 21.5 | 23.8 | 2458 | 1137 |
| RAW+EVENTS-token-matched-chrono | 300 | 19.3 | 19.7 | 29.3 | 17.4 | 2456 | 1160 |
| HyDE-RAW | 300 | 12.0 | 14.1 | 32.4 | 10.0 | 1034 | 961 |

## Paired comparisons (pp)

| difference | delta | question 95% CI | McNemar p | left-only / right-only / both / neither | project 95% CI | per-project | sign-flip p |
|---|---:|---|---:|---|---|---|---:|
| RAW+EVENTS-token-matched-chrono - HyDE-RAW-token-matched-chrono | +5.3 | [+0.3, +10.3] | 0.0479 | 37 / 21 / 21 / 221 | [+3.3, +8.0] | 01: +3.3, 02: +10.0, 03: +3.3, 04: +3.3, 05: +6.7 | 0.0625 |
| HyDE-RAW-token-matched-chrono - RAW-token-matched-chrono | +0.0 | [-4.3, +4.3] | 1.0000 | 22 / 22 / 20 / 236 | [-4.0, +4.0] | 01: +0.0, 02: +1.7, 03: +6.7, 04: -6.7, 05: -1.7 | 1.0000 |
| HyDE-RAW-token-matched-chrono - HyDE-RAW | +2.0 | [-2.3, +6.7] | 0.4709 | 27 / 21 / 15 / 237 | [-1.0, +5.3] | 01: +3.3, 02: +1.7, 03: +8.3, 04: -1.7, 05: -1.7 | 0.5000 |
| HyDE-RAW-token-matched-chrono - RAW | +1.7 | [-2.7, +6.0] | 0.5515 | 25 / 20 / 17 / 238 | [-0.7, +4.0] | 01: +3.3, 02: +5.0, 03: +3.3, 04: -1.7, 05: -1.7 | 0.3750 |

## Cost

- API calls: 467; list-price estimate USD 0.4108
- by model: `{"google/gemini-3-flash-preview": {"calls": 164, "duration_ms": 170035.19049624447, "estimated_usd": 0.062258, "input_tokens": 84406, "output_tokens": 6685}, "openai/gpt-4.1-mini": {"calls": 300, "duration_ms": 290497.96999711543, "estimated_usd": 0.3460480000000001, "input_tokens": 851484, "output_tokens": 3409}, "text-embedding-3-large": {"calls": 3, "duration_ms": 5115.022168145515, "estimated_usd": 0.00251823, "input_tokens": 19371, "output_tokens": 0}}`
- OpenRouter key usage delta: 0.49885840000000137 (OpenRouter key usage; includes any concurrent use of the same key)
