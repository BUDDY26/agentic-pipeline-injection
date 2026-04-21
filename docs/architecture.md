# Architecture Overview

**Project:** agentic-pipeline-injection
**Last updated:** 2026-04-03

> Update this document whenever the system design changes.
> Keep it in sync with the actual implementation — do not let it drift.

---

## System Overview

This project implements a controlled research framework for studying indirect prompt injection propagation in agentic AI pipelines. A fixed adversarial document is embedded within a FAISS-indexed corpus alongside benign documents; three pipeline topologies (RAG, Linear Chain, Parallel) retrieve from that corpus and route content through one or more LLM-backed agents. A metrics module scores each run for integrity degradation, propagation depth, and compromise signal presence, and all runs are captured in structured JSONL experiment logs. The system is designed for reproducibility: corpus, index, query, and model configuration are locked across all runs, allowing multi-run validation to isolate injection effects from LLM non-determinism.

---

## Component Map

| Component | Location | Responsibility |
|-----------|----------|----------------|
| Corpus layer | `corpus/`, `corpus_loader.py` | Loads 4 benign + 1 adversarial document; chunks text; builds and persists FAISS vector index via sentence-transformers (`all-MiniLM-L6-v2`); exposes `retrieve()` for ranked document lookup |
| LLM interface | `llm_client.py` | Wraps Ollama (`llama3.1:8b`) as primary and Groq (`llama3-8b-8192`) as fallback; exposes single `generate(prompt)` entrypoint |
| Pipeline layer | `notebooks/notebook_01_rag.ipynb`, `notebook_02_linear.ipynb`, `notebook_03_parallel.ipynb` | Implements three injection topologies; each notebook drives retrieval, agent execution, and logging for one topology type |
| Logger | `structured_logger.py` | Writes structured JSONL entries to `experiment_logs/`; captures run_id, pipeline_type, agent_id, entry_type, content, and extra metadata per event |
| Metrics module | `src/metrics.py` | Computes `integrity_score()` (difflib similarity between baseline and injected output), `compromise_signal()` (regex Stage-1 detection plus integrity threshold Stage-2), and propagation depth |
| Experiment runner | `notebooks/notebook_04_experiments.ipynb`, `scripts/run_multi_validation.py` | Executes full 9-configuration matrix (3 topologies × 3 injection ranks) and 27-run multi-run validation; writes results to `results/` |
| Output / taxonomy | `results/validation/multi_run_results.csv`, `results/validation/baseline_stability.csv`, `results/validation/validation_summary.md`, `results/figures/` | Stores aggregated validation metrics, baseline control verification, narrative summary, and publication-quality figures. Superseded pre-audit taxonomy and charts are retained under `results/archive/pre_audit/`. |

---

## Data Flow

1. **Index build** (one-time, Week 1): `corpus_loader.py` loads all corpus documents, chunks them, encodes via sentence-transformers, and writes `faiss_index/index.faiss` + `faiss_index/index.pkl`.
2. **Retrieval**: Each pipeline notebook calls `retrieve(query, k=3)` against the locked FAISS index. The adversarial document ranks at position 1 or 3 depending on the injection configuration; baseline runs retrieve only benign documents.
3. **Agent execution**: Retrieved documents are passed as context to one or more LLM agents via `llm_client.generate()`. Topology determines agent count and routing:
   - RAG: single agent with retrieved context
   - Linear Chain: three sequential agents; output of each becomes input of the next
   - Parallel: three independent agents (Security Analyst, Systems Architect, Researcher) whose outputs are passed to an aggregator agent
4. **Logging**: `structured_logger.log_entry()` writes a JSONL record for each agent invocation to `experiment_logs/`.
5. **Scoring**: `src/metrics.py` reads agent outputs from logs and computes `integrity_score`, `compromise_signal`, and `propagation_depth` for each run.
6. **Aggregation**: `scripts/recompute_validation_metrics.py` collates per-run scores into `results/validation/multi_run_results.csv`; `scripts/generate_figures.py` renders figures into `results/figures/`.

---

## Key Interfaces

| Interface | Signature | Notes |
|-----------|-----------|-------|
| Retrieval | `retrieve(query: str, k: int) -> list[dict]` | Returns ranked document chunks with metadata; FAISS index must be loaded first via `load_index()` |
| LLM generation | `generate(prompt: str) -> str` | Attempts Ollama first; falls back to Groq on connection failure |
| Logging | `log_entry(run_id, pipeline_type, agent_id, entry_type, content, **extra)` | Appends one JSON line to `experiment_logs/{run_id}.jsonl` |
| Integrity score | `integrity_score(baseline: str, injected: str) -> float` | Returns difflib SequenceMatcher ratio; 1.0 = identical, lower = degraded |
| Compromise signal | `compromise_signal(output: str, baseline: str) -> bool` | Stage-1: regex match for injection artifact; Stage-2: integrity below threshold (0.85) |

---

## External Dependencies

| Dependency | Version | Purpose |
|------------|---------|---------|
| faiss-cpu | 1.8.0 | Vector similarity index for corpus retrieval |
| sentence-transformers | 3.0.1 | Document and query embedding (`all-MiniLM-L6-v2`) |
| langchain | 0.2.16 | Agent chain orchestration for Linear and Parallel topologies |
| langchain-groq | 0.1.9 | Groq LLM provider integration |
| groq | 0.9.0 | Groq API client (fallback LLM) |
| python-dotenv | 1.0.1 | Environment variable loading (GROQ_API_KEY) |
| pandas | 2.2.2 | Results aggregation and CSV export |
| jupyter | 1.0.0 | Notebook execution environment |

---

## Architecture Decision Records

Key decisions are documented in [`docs/adr/`](adr/).

| ADR | Title | Status |
|-----|-------|--------|
| [ADR-001](adr/ADR-001-template.md) | Use three pipeline topologies (RAG, Linear Chain, Parallel) | Accepted |

---

## Known Constraints

- **Single model scope:** All runs use `llama3.1:8b` (Ollama local). Results are not generalizable across model families without re-running experiments.
- **Controlled corpus only:** The adversarial payload is a single fixed document (`corpus/adversarial_01_injection.txt`). Findings reflect body-text injection; other injection vectors (metadata, tool outputs) are out of scope.
- **FAISS index is locked:** The index was built once in Week 1 and must not be rebuilt or modified; doing so would invalidate all prior experiment logs and break reproducibility.
- **Stage-1 detection is literal:** `compromise_signal` Stage-1 uses regex matching for the known injection string. Paraphrased or rephrased payloads evade Stage-1 and are only caught by Stage-2 integrity threshold.
