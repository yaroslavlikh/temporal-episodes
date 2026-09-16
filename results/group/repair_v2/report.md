# Final sprint experiment D: GroupMemBench empty-answer repair (v2)

- source run `groupmembench_temporal_episodes_official_v1` (read only); runner sha256 `62df0718a94a303c091545a54196d4d3cc69145500cd810f972deca0fcfefa54`

## Repair outcome

| condition | original empty | repaired | still failed |
|---|---:|---:|---:|
| RAW | 44 | 44 | 0 |
| RAW+EPISODES | 58 | 58 | 0 |

## Endpoints

| endpoint | answers | n | RAW % | RAW+EPISODES % | delta [95% CI] | EP-only / RAW-only | McNemar p |
|---|---|---:|---:|---:|---|---:|---:|
| primary: F+T, update+temporal | original (protocol primary) | 150 | 34.0 | 30.0 | -4.0 [-9.3, +1.3] | 6 / 12 | 0.2379 |
| primary: F+T, update+temporal | repaired v2 | 150 | 37.3 | 33.3 | -4.0 [-9.3, +1.3] | 5 / 11 | 0.2101 |
| all questions | original (protocol primary) | 745 | 42.0 | 40.3 | -1.7 [-4.3, +0.7] | 39 / 52 | 0.2082 |
| all questions | repaired v2 | 745 | 43.1 | 41.5 | -1.6 [-4.0, +0.8] | 39 / 51 | 0.2461 |
