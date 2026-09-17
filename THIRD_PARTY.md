# Third-party benchmarks, data and code

This repository evaluates a memory method on three public benchmarks. Their data, prompts
and code belong to their authors. What we redistribute depends on whether a license
granting redistribution is published.

| Benchmark | Source used (pinned) | License as published | What this repository contains |
|---|---|---|---|
| SocialMemBench | Hugging Face `anon4data/socialmembench`, revision `ea7e4acf502df3eda484d56165ec594d6f4c138f` | CC BY 4.0 (dataset card) | Per-question predictions, judgments and derived memory in `results/social/`, with attribution below |
| EverMemBench-Dynamic (data) | Hugging Face `EverMind-AI/EverMemBench-Dynamic`, revision `a6b210a32248e841967b7b64a64281d2ff3f669d` | Apache 2.0 (dataset card) | Per-question predictions, judgments and derived memory in `results/ever/` (including the k-sweep in `results/ever/ksweep/`: per-question delivery at k = 10/20/40 and k = 20 answers and judgments), with attribution below |
| EverMemBench (evaluation code and prompts) | GitHub `EverMind-AI/EverMemBench`, commit `e10b3d52f0e4cfc5c124ad406b5d95c59c73738b` | No license file found | Nothing copied. Runners fetch the pinned commit and read prompts from it |
| GroupMemBench | GitHub `UCSB-NLP-Chang/GroupMemBench`, commit `e2682e01ff490acfe4fac2940159dce60307dfc9` | No license file found | Aggregate results, metadata and SHA-256 of our per-question files only (`results/group/`, including the repaired amendment in `results/group/repair_v2/`). No questions, answers, prompts, messages or quotes |

"No license file found" means we have no permission to redistribute the material. It does
not mean the authors prohibit reuse; it only limits what we republish.

## Attribution

- SocialMemBench: *SocialMemBench: Are AI Memory Systems Ready for Social Group Settings?*
  arXiv:2605.17789. Dataset: https://huggingface.co/datasets/anon4data/socialmembench (CC BY 4.0).
- EverMemBench: Hu et al., *Evaluating Long-Horizon Memory for Multi-Party Collaborative
  Dialogues*, KDD 2026, arXiv:2602.01313. Dataset:
  https://huggingface.co/datasets/EverMind-AI/EverMemBench-Dynamic (Apache 2.0).
- GroupMemBench: Yang et al., *GroupMemBench: Benchmarking LLM Agent Memory in Multi-Party
  Conversations*, arXiv:2605.14498. Code and data: https://github.com/UCSB-NLP-Chang/GroupMemBench.

Derived files in `results/social/` and `results/ever/` (model answers, judge outputs, extracted
events and episodes with verbatim quotes) contain text from those datasets and remain subject to
the corresponding upstream license.

## Models and services

Answers, judgments, extraction and embeddings were produced through the OpenAI API
(`gpt-4o-mini-2024-07-18`, `gpt-5`, `text-embedding-3-small`, `text-embedding-3-large`) and
OpenRouter (`openai/gpt-4.1-mini`, `google/gemini-3-flash-preview`), plus the local
`sentence-transformers` model `paraphrase-multilingual-MiniLM-L12-v2`. Their outputs are
published here for verification only; use of those services is governed by their own terms.
