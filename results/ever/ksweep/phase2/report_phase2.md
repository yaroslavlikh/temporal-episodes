# k-sweep, phase 2: accuracy at k=10 (sealed) and k=20

EverMemBench, stratified sample N = 304 (sample seed 20260917). k=10 verdicts are the sealed ones; k=20 answers and verdicts are new. Paired question bootstrap, 10,000 resamples, seed 20260917, percentile 95% CI; exact McNemar.

## Accuracy, %

| condition | k=10 | k=20 |
|---|---:|---:|
| RAW | 49.01 | 48.68 |
| RAW+EVENTS | 49.01 | 48.36 |

## Paired differences

| left − right | Δ, pp | 95% CI | left-only correct | right-only correct | discordant | McNemar p |
|---|---:|---|---:|---:|---:|---:|
| RAW+EVENTS@10 − RAW@10 | +0.00 | [-3.62; +3.62] | 15 | 15 | 30 | 1.000 |
| RAW+EVENTS@20 − RAW@20 | -0.33 | [-4.28; +3.62] | 18 | 19 | 37 | 1.000 |
| RAW@20 − RAW@10 | -0.33 | [-4.28; +3.29] | 17 | 18 | 35 | 1.000 |
| RAW+EVENTS@20 − RAW+EVENTS@10 | -0.66 | [-4.93; +3.62] | 20 | 22 | 42 | 0.878 |

## Spend

- actual, from response.usage of every call (BudgetGuard): $0.7947 with fee factor 1.1; $0.7225 at list price
- answer calls sent: 607; logged in api_usage.jsonl: 541; unlogged: 66 (identical payloads sent concurrently)
- api_usage.jsonl alone: 633 rows, $0.7118 with fee
- answers reused from sealed caches: 1
- judge parse branches: {'multiple_choice': 414, 'json': 194}; paid judge attempts: 92

## Identical prompts

- questions whose k=20 prompt is byte-identical in both conditions (no event document in top-20): 66; identical answer text among them: 62
