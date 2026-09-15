# SocialMemBench — TemporalEpisodes in the frozen official-v1 harness

The RAW/FLAT/VERSIONED rows are immutable results from the frozen 2026-09-11 run. Only RAW+EPISODES is newly generated and scored.

- model: `gpt-4o-mini-2024-07-18`
- embeddings: `text-embedding-3-small`
- retrieval: one cosine top-10 over each condition's corpus
- answer prompt, judge prompt, context packing, provenance expansion: identical code path

## Overall

| condition | MeanQ | MeanN | 95% network CI | evidence precision | evidence recall |
|---|---:|---:|---:|---:|---:|
| RAW | 0.358 | 0.358 | [0.332, 0.382] | 0.124 | 0.675 |
| RAW+FLAT | 0.370 | 0.364 | [0.338, 0.389] | 0.133 | 0.672 |
| RAW+VERSIONED | 0.367 | 0.362 | [0.338, 0.385] | 0.132 | 0.670 |
| RAW+EPISODES | 0.368 | 0.367 | [0.344, 0.390] | 0.127 | 0.685 |

## Paired network deltas

- RAW+EPISODES vs RAW: 22W/3T/18L; delta=+0.010; 95% CI [-0.008, +0.028]
- RAW+EPISODES vs RAW+FLAT: 21W/2T/20L; delta=+0.003; 95% CI [-0.013, +0.022]
- RAW+EPISODES vs RAW+VERSIONED: 24W/1T/18L; delta=+0.006; 95% CI [-0.010, +0.021]

## By question type

| type | n | RAW | FLAT | VERSIONED | EPISODES |
|---|---:|---:|---:|---:|---:|
| Q1 | 249 | 0.306 | 0.325 | 0.320 | 0.314 |
| Q2 | 81 | 0.716 | 0.716 | 0.728 | 0.691 |
| Q3 | 22 | 0.055 | 0.091 | 0.095 | 0.132 |
| Q4 | 80 | 0.825 | 0.838 | 0.838 | 0.863 |
| Q5 | 92 | 0.251 | 0.279 | 0.246 | 0.262 |
| Q6 | 54 | 0.481 | 0.444 | 0.444 | 0.407 |
| Q7 | 181 | 0.298 | 0.307 | 0.308 | 0.309 |
| Q8 | 262 | 0.233 | 0.246 | 0.247 | 0.259 |
| Q9 | 10 | 0.330 | 0.340 | 0.370 | 0.380 |

## Published paper reference

| system | MeanQ |
|---|---:|
| full-context GPT-4o-mini | 0.369 |
| uncompressed raw retrieval | 0.345 |
| subject-mem | 0.321 |
| SMG | 0.213 |
| Graphiti | 0.178 |
| LangMem | 0.162 |
| Mem0 | 0.143 |
| Cognee | 0.120 |

## Protocol guardrails

- The episode snapshot was constructed query-independently and sealed before QA inference.
- Frozen inputs are checksum-verified on every process start.
- This is an internally controlled adapter comparison, not an official leaderboard submission.
