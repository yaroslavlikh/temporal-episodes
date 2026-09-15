# SocialMemBench — full TemporalEpisode run

Query-independent 43-network / 1,031-QA adapter run; not an official leaderboard submission.

- answer/judge/extraction model: `gpt-4o-mini-2024-07-18`
- episode linking and query retrieval embeddings: `paraphrase-multilingual-MiniLM-L12-v2`
- retrieval: hybrid raw top-12 + episode dense top-12 -> unified dense rerank -> 400-word context
- memory: 639 events -> 449 episodes

## Overall

| condition | MeanQ | MeanN | 95% network bootstrap CI | evidence precision | evidence recall | context words |
|---|---:|---:|---:|---:|---:|---:|
| RAW | 0.306 | 0.311 | [0.288, 0.334] | 0.075 | 0.485 | 312.2 |
| RAW+EPISODES | 0.324 | 0.316 | [0.293, 0.339] | 0.078 | 0.521 | 384.2 |

## Paired network result

- RAW+EPISODES vs RAW: 26W/4T/13L networks; mean delta=+0.006; 95% CI [-0.009, +0.020]

## By question type

| type | n | RAW | RAW+EPISODES |
|---|---:|---:|---:|
| Q1 | 249 | 0.219 | 0.237 |
| Q2 | 81 | 0.654 | 0.704 |
| Q3 | 22 | 0.095 | 0.100 |
| Q4 | 80 | 0.775 | 0.762 |
| Q5 | 92 | 0.262 | 0.255 |
| Q6 | 54 | 0.500 | 0.500 |
| Q7 | 181 | 0.278 | 0.271 |
| Q8 | 262 | 0.157 | 0.203 |
| Q9 | 10 | 0.140 | 0.150 |

## API usage and estimated list-price cost

| phase | new API calls | input tokens | output tokens | estimated USD |
|---|---:|---:|---:|---:|
| memory | 947 | 1,038,499 | 132,114 | $0.235 |
| inference | 1946 | 1,988,413 | 183,693 | $0.408 |
| judge | 1525 | 916,168 | 64,742 | $0.176 |
| **total** |  |  |  | **$0.820** |

Prices used: GPT-4o-mini $0.15/M input and $0.60/M output; text-embedding-3-small $0.02/M. Local MiniLM computation is not assigned a dollar price.

## Published paper reference (MeanQ)

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

## Guardrails

- Memory was sealed before QA columns were opened (`qa_read=false` in episodes_meta.json).
- Compare RAW and RAW+EPISODES directly; they share answerer, judge, raw retrieval, and budget.
- Published rows are references from the paper, not reruns or an official leaderboard submission.
