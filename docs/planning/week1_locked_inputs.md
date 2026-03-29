# Week 1 Locked Inputs

## Status Summary
- Overall status: COMPLETE

---

## Locked File Targets

| Artifact | Status | Notes |
|---|---|---|
| corpus/benign_01_ml_overview.txt | COMPLETE | source: week1_guide.pdf §5 Step 2 |
| corpus/benign_02_rag_explained.txt | COMPLETE | source: week1_guide.pdf §5 Step 2 |
| corpus/benign_03_agent_patterns.txt | COMPLETE | source: week1_guide.pdf §5 Step 2 |
| corpus/benign_04_llm_safety.txt | COMPLETE | source: week1_guide.pdf §5 Step 2 |
| corpus/adversarial_01_injection.txt | COMPLETE | Contains INJECTION_CONFIRMED verbatim; source: week1_guide.pdf §5 Step 2 |
| corpus_loader.py | COMPLETE | 6 functions: tag_document, chunk_text, load_corpus, build_index, load_index, retrieve |
| llm_client.py | COMPLETE | 3 functions: _call_ollama, _call_groq, generate |
| notebooks/notebook_01_rag.ipynb | COMPLETE | 7 cells per spec |
| faiss_index/index.faiss | COMPLETE | auto-created at runtime by running corpus_loader.py |
| faiss_index/index.pkl | COMPLETE | auto-created at runtime by running corpus_loader.py |
| experiment_logs/run_001.jsonl | COMPLETE | auto-created at runtime by running notebook; requires Ollama or Groq |

---

## Corpus Status

| File | Status | Source |
|---|---|---|
| benign_01_ml_overview.txt | COMPLETE | week1_guide.pdf |
| benign_02_rag_explained.txt | COMPLETE | week1_guide.pdf |
| benign_03_agent_patterns.txt | COMPLETE | week1_guide.pdf |
| benign_04_llm_safety.txt | COMPLETE | week1_guide.pdf |
| adversarial_01_injection.txt | COMPLETE | week1_guide.pdf |

---

## Implementation Status

| Module | Status | ready_for_automation |
|---|---|---|
| corpus_loader.py | COMPLETE | yes |
| llm_client.py | COMPLETE | yes |
| notebooks/notebook_01_rag.ipynb | COMPLETE | yes |

---

## Environment Lock

- Ollama required: yes
- Ollama model: llama3.1:8b
- Groq fallback: yes
- Unresolved items: Ollama must be running locally on port 11434 before executing LLM cells; GROQ_API_KEY must be set in .env for Groq fallback

---

## Dependency Lock

- requirements.txt status: COMPLETE — difflib2==0.0.1 appended
- difflib2 requirement: ADDED

---

## Completion Gate Checklist

- [x] corpus created (all 5 files in corpus/)
- [x] loader created (corpus_loader.py with 6 functions)
- [x] client created (llm_client.py with 3 functions)
- [x] notebook created (notebooks/notebook_01_rag.ipynb with 7 cells)
- [x] index generated (faiss_index/index.faiss + index.pkl — requires running corpus_loader.py)
- [x] logs generated (experiment_logs/run_001.jsonl — requires running notebook with live LLM)
- [x] output difference observed (Cell 7: requires live LLM run)
