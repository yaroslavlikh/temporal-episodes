# SocialMemBench — full 43-network run

Official-compatible evaluation of this project's adapter (not an official leaderboard submission).

- QA: 1,031
- networks: 43
- model: `gpt-4o-mini-2024-07-18`
- embeddings: `text-embedding-3-small`
- retrieval: cosine top-10

## Overall

| condition | MeanQ | MeanN | network-bootstrap 95% CI | evidence recall |
|---|---:|---:|---:|---:|
| RAW | 0.358 | 0.358 | [0.332, 0.382] | 0.675 |
| RAW+FLAT | 0.370 | 0.364 | [0.338, 0.389] | 0.672 |
| RAW+VERSIONED | 0.367 | 0.362 | [0.338, 0.385] | 0.670 |

## By question type

| type | n | RAW | RAW+FLAT | RAW+VERSIONED |
|---|---:|---:|---:|---:|
| Q1 | 249 | 0.306 | 0.325 | 0.320 |
| Q2 | 81 | 0.716 | 0.716 | 0.728 |
| Q3 | 22 | 0.055 | 0.091 | 0.095 |
| Q4 | 80 | 0.825 | 0.838 | 0.838 |
| Q5 | 92 | 0.251 | 0.279 | 0.246 |
| Q6 | 54 | 0.481 | 0.444 | 0.444 |
| Q7 | 181 | 0.298 | 0.307 | 0.308 |
| Q8 | 262 | 0.233 | 0.246 | 0.247 |
| Q9 | 10 | 0.330 | 0.340 | 0.370 |

## By network tier

| tier | n QA | RAW | RAW+FLAT | RAW+VERSIONED |
|---|---:|---:|---:|---:|
| small | 264 | 0.361 | 0.364 | 0.359 |
| medium | 346 | 0.348 | 0.367 | 0.360 |
| large | 421 | 0.363 | 0.375 | 0.378 |

## Paired network-level deltas

- RAW+VERSIONED vs RAW: 22W/3T/18L networks; mean delta=+0.004, 95% CI [-0.008, +0.016]
- RAW+VERSIONED vs RAW+FLAT: 16W/7T/20L networks; mean delta=-0.002, 95% CI [-0.015, +0.011]

## Published paper reference (MeanQ)

These are paper values, not reruns in this repository.

| condition | MeanQ |
|---|---:|
| full-context GPT-4o-mini | 0.369 |
| uncompressed raw retrieval | 0.345 |
| subject-mem | 0.321 |
| SMG | 0.213 |
| Graphiti | 0.178 |
| LangMem | 0.162 |
| Mem0 | 0.143 |
| Cognee | 0.120 |

## Interpretation guardrails

- Compare our three rows directly: they are a controlled ablation sharing extraction and retrieval.
- Comparison with published systems is informative but not an official submission until the authors' harness is accessible again.
- Evidence recall is secondary and measures exposed raw provenance against gold anchors; it is not part of the paper's primary score.
