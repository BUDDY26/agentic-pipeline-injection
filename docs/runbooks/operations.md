# Operations

**Project:** agentic-pipeline-injection

The canonical setup, environment, and reproduction commands live in
[`README.md`](../../README.md). This document is a short operator-facing
reference for routine tasks and common recovery paths.

---

## Quick Reference

| Task | Command |
|------|---------|
| Install dependencies | `pip install -r requirements.txt` |
| Configure environment | `cp .env.example .env` |
| Pull the local LLM | `ollama pull llama3.1:8b` |
| Run the 27-run validation matrix | `python scripts/run_multi_validation.py` |
| Recompute metrics from existing logs | `python scripts/recompute_validation_metrics.py` |
| Regenerate figures from results CSV | `python scripts/generate_figures.py` |

---

## Environment Variables

See `.env.example` for the full list.

| Variable | Purpose | Required |
|----------|---------|----------|
| `OLLAMA_BASE_URL` | Ollama endpoint (default `http://localhost:11434`) | No |
| `GROQ_FALLBACK` | `0` = use Ollama (default); `1` = use Groq | No |
| `GROQ_API_KEY` | Groq API key | Only if `GROQ_FALLBACK=1` |

---

## Prerequisites

- Python 3.11
- Ollama running locally with `llama3.1:8b` pulled

---

## Troubleshooting

**FAISS index missing or modified.** The index under `faiss_index/` is locked
and must not be rebuilt. Rebuilding changes retrieval rank assignments and
invalidates every existing experiment log. If the index files are missing,
restore them from git history rather than re-running `corpus_loader.py`.

**Ollama unreachable.** Confirm `ollama serve` is running and
`OLLAMA_BASE_URL` in `.env` is correct. To fall back to Groq, set
`GROQ_FALLBACK=1` and `GROQ_API_KEY=<key>` in `.env`.

**Validation logs already present.** `scripts/run_multi_validation.py` is
non-destructive: it skips any run whose `experiment_logs/val_*.jsonl` file
already exists. Delete the relevant log file to force a fresh run for that
configuration.
