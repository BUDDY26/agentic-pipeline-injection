# Operations

**Project:** agentic-pipeline-injection

The canonical setup, environment, and reproduction commands live in
[`README.md`](../../README.md). This document is a short operator-facing
reference for routine tasks and common recovery paths.

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
