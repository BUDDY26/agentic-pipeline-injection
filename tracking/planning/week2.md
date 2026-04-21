# Week 2 Planning — Linear Chain + Parallel Pipelines

**Project:** agentic-pipeline-injection
**Authority:** tracking/reference/week2_guide.pdf (Days 8–14, ~12–14 hours, Build Phases 3 & 4)
**Status:** Ready to begin — Week 1 complete and verified
**Last updated:** 2026-03-29

---

## Focus

Week 2 adds the two remaining pipeline topologies on top of the shared infrastructure
completed in Week 1. By Day 14 there will be three fully operational pipelines — RAG
(Week 1), Linear Chain, and Parallel Multi-Agent — each producing a structured JSON
lines log file. The corpus loader, LLM client, FAISS index, and `experiment_logs/`
directory from Week 1 are reused without modification. No Week 1 files are touched.

---

## Scope Boundaries

### In scope
- Create `structured_logger.py` at project root (shared log module)
- Implement `notebooks/notebook_02_linear.ipynb` — 3-node LangChain LLMChain
- Implement `notebooks/notebook_03_parallel.ipynb` — parallel agents + aggregator
- Run Baseline and Injected-Rank-1 trials for each topology
- Produce log files that support computation of `propagation_depth`,
  `integrity_score`, and `compromise_signal` (computed in Week 3+)
- Add `pyautogen==0.2.35` to `requirements.txt`

### Out of scope
- `src/` pipeline modules — pipelines live in notebooks, not `src/`
- README overhaul or project documentation rewrite
- Poster writing or paper drafting
- New adversarial document variants
- Changes to corpus, FAISS index, or `notebooks/notebook_01_rag.ipynb`
- Modifying `corpus_loader.py` or `llm_client.py`
- v2 roadmap items

---

## Directory Structure — End of Week 2

Files marked NEW are created this week. Everything else is unchanged from Week 1.

```
agentic-pipeline-injection/
├── corpus/                        ← unchanged
├── corpus_loader.py               ← unchanged
├── llm_client.py                  ← unchanged
├── faiss_index/                   ← unchanged
├── structured_logger.py           ← NEW: shared log_entry() module
├── experiment_logs/
│   ├── run_001.jsonl              ← Week 1 RAG log (do not touch)
│   ├── run_002.jsonl              ← NEW: Linear Baseline
│   ├── run_003.jsonl              ← NEW: Linear Injected-Rank-1
│   ├── run_004.jsonl              ← NEW: Parallel Baseline
│   └── run_005.jsonl              ← NEW: Parallel Injected-Rank-1
├── notebooks/
│   ├── notebook_01_rag.ipynb      ← unchanged
│   ├── notebook_02_linear.ipynb   ← NEW: Linear Chain pipeline
│   └── notebook_03_parallel.ipynb ← NEW: Parallel pipeline
└── requirements.txt               ← updated: pyautogen==0.2.35 added
```

---

## Ordered Deliverables

| # | Deliverable | Notes |
|---|---|---|
| 1 | `structured_logger.py` | Extracted from notebook_01_rag.ipynb Cell 2; project root |
| 2 | `notebooks/notebook_02_linear.ipynb` | 6-cell Linear Chain notebook |
| 3 | `experiment_logs/run_002.jsonl` | Linear Baseline — 4 entries |
| 4 | `experiment_logs/run_003.jsonl` | Linear Injected-Rank-1 — 4 entries |
| 5 | `notebooks/notebook_03_parallel.ipynb` | 6-cell Parallel notebook |
| 6 | `experiment_logs/run_004.jsonl` | Parallel Baseline — 4 entries |
| 7 | `experiment_logs/run_005.jsonl` | Parallel Injected-Rank-1 — 4 entries |
| 8 | `requirements.txt` updated | `pyautogen==0.2.35` appended |

Deliverables 1–4 (structured_logger + Linear Chain verified) must be complete before
beginning deliverables 5–8.

---

## Step 1 — structured_logger.py (First File to Create)

Extract `log_entry()` from `notebook_01_rag.ipynb` Cell 2 into a standalone module
at the **project root**. All three notebooks import from here. Do not modify
`notebook_01_rag.ipynb` — its inline Cell 2 definition can remain.

Module signature (from guide):

```python
def log_entry(run_id: str, pipeline_type: str, agent_id: str,
              entry_type: str, content: str, extra: dict = None):
```

Smoke test (run after creating, delete test file after confirming):

```bash
python -c "
from structured_logger import log_entry
log_entry('logger_test', 'test', 'agent_0', 'pre_generation', 'hello')
log_entry('logger_test', 'test', 'agent_0', 'post_generation', 'world')
print('Logger OK')
"
# Expected: Logger OK
# Verify: cat experiment_logs/logger_test.jsonl  (2 JSON lines)
# Cleanup: rm experiment_logs/logger_test.jsonl
```

---

## Step 2 — Linear Chain Pipeline (notebook_02_linear.ipynb)

### Architecture

```
[RAG Retriever] → [Agent 1: Summarizer] → [Agent 2: Synthesizer] → [Agent 3: Formatter]
```

Agent 1 receives the assembled prompt + corpus chunks. Agents 2 and 3 receive only
the prior agent's output. No agent after Agent 1 reads the corpus directly.

### Notebook structure (6 cells)

| Cell | Purpose |
|---|---|
| 1 | Imports + configuration (`RETRIEVAL_K=3`, `TEST_QUERY`) |
| 2 | Load FAISS index via `cl.load_index()` |
| 3 | `run_linear_pipeline(query, run_id, k, include_adversarial)` function |
| 4 | Run Baseline → `run_002` |
| 5 | Run Injected-Rank-1 → `run_003` |
| 6 | Validate log files + injection check |

### Pipeline function signature (from guide)

```python
def run_linear_pipeline(query: str, run_id: str,
                        k: int = RETRIEVAL_K,
                        include_adversarial: bool = True):
    """3-node linear chain. Logs: 1 pre_generation + 3 post_generation."""
```

### Log entries per run — 4 total

| Entry | agent_id | entry_type |
|---|---|---|
| 1 | `agent_1_summarizer` | `pre_generation` |
| 2 | `agent_1_summarizer` | `post_generation` |
| 3 | `agent_2_synthesizer` | `post_generation` |
| 4 | `agent_3_formatter` | `post_generation` |

`pipeline_type` value: `"linear"`

Agents 2 and 3 do **not** log a `pre_generation` entry.

### Log schema

```json
{
  "run_id":        "run_002",
  "pipeline_type": "linear",
  "agent_id":      "agent_1_summarizer",
  "entry_type":    "pre_generation",
  "content":       "<assembled prompt>",
  "timestamp":     "<ISO 8601 UTC>"
}
```

No additional fields beyond Week 1 schema.

### Run IDs

- `run_002` — Baseline (`include_adversarial=False`)
- `run_003` — Injected-Rank-1 (`include_adversarial=True`)

Each run produces a **separate** `.jsonl` file.

### Acceptance criteria

- [ ] `structured_logger.py` smoke test passes
- [ ] `notebook_02_linear.ipynb` runs all 6 cells without exception
- [ ] `run_002.jsonl` has exactly 4 entries, 0 null outputs
- [ ] `run_003.jsonl` has exactly 4 entries, 0 null outputs
- [ ] `INJECTION_CONFIRMED` present in `agent_1_summarizer` post_generation entry of `run_003`

---

## Step 3 — Parallel Pipeline (notebook_03_parallel.ipynb)

### Architecture

```
[RAG Retriever] → agent_A (Security Analyst)  ↘
                → agent_B (Systems Architect)  → aggregator
                → agent_C (Researcher)         ↗
```

All three agents receive the same retrieved context. The aggregator receives all
three outputs and synthesizes a final response.

### Implementation pattern

**Preferred:** Direct `llm_client.py` calls for each agent + aggregator. This
provides reliable termination and identical log structure to the linear chain.

**Optional:** AutoGen GroupChat with `max_turns=5` and `speaker_selection_method="round_robin"`.
If AutoGen loops or fails to terminate after 3 hours of debugging, revert to the
direct `llm_client.py` pattern. Do not allow AutoGen instability to block Week 3.

`pyautogen==0.2.35` must be installed regardless (required by the notebook import).

### Notebook structure (6 cells)

| Cell | Purpose |
|---|---|
| 1 | Imports + configuration (includes `import autogen`, AutoGen config) |
| 2 | Load FAISS index |
| 3 | `run_parallel_pipeline(query, run_id, k, include_adversarial)` function |
| 4 | Run Baseline → `run_004` |
| 5 | Run Injected-Rank-1 → `run_005` |
| 6 | Validate log files + injection check |

### Log entries per run — 4 total

| Entry | agent_id | entry_type |
|---|---|---|
| 1 | `agent_A` | `post_generation` |
| 2 | `agent_B` | `post_generation` |
| 3 | `agent_C` | `post_generation` |
| 4 | `aggregator` | `post_generation` |

`pipeline_type` value: `"parallel"`

No `pre_generation` entries. No `branch` field.

### Run IDs

- `run_004` — Baseline (`include_adversarial=False`)
- `run_005` — Injected-Rank-1 (`include_adversarial=True`)

### Acceptance criteria

- [ ] `notebook_03_parallel.ipynb` runs all 6 cells without exception
- [ ] `run_004.jsonl` has exactly 4 entries, 0 null outputs
- [ ] `run_005.jsonl` has exactly 4 entries, 0 null outputs
- [ ] `INJECTION_CONFIRMED` present in at least one agent entry of `run_005`
- [ ] `pyautogen==0.2.35` present in `requirements.txt`

---

## Logging Compatibility Contract

All Week 2 log entries use the same schema as `run_001.jsonl`. No new fields added.

| Field | Week 1 value | Week 2 value |
|---|---|---|
| `run_id` | `"run_001"` | `"run_002"` – `"run_005"` |
| `pipeline_type` | `"rag"` | `"linear"` or `"parallel"` |
| `agent_id` | `"rag_generator"` | topology-specific (see tables above) |
| `entry_type` | `"pre_generation"` / `"post_generation"` | same values |
| `content` | assembled prompt or response string | same semantics |
| `timestamp` | ISO 8601 UTC | same format |

---

## Week 2 Completion Gate

Run after both notebooks complete. All five log files must be present.

```python
# End-to-end smoke test
import json
from pathlib import Path

LOG_DIR = Path("experiment_logs")
expected = {
    "run_001": 4,   # RAG Baseline + Injected
    "run_002": 4,   # Linear Baseline
    "run_003": 4,   # Linear Injected
    "run_004": 4,   # Parallel Baseline
    "run_005": 4,   # Parallel Injected
}
all_pass = True
for run_id, exp_count in expected.items():
    path = LOG_DIR / f"{run_id}.jsonl"
    entries = [json.loads(l) for l in open(path)]
    null_outputs = [e for e in entries if not e["content"].strip()]
    status = "PASS" if len(entries) == exp_count and not null_outputs else "FAIL"
    if status == "FAIL": all_pass = False
    print(f"{status} {run_id}: {len(entries)}/{exp_count} entries, {len(null_outputs)} nulls")
print("\nWEEK 2 GATE:", "PASS" if all_pass else "FAIL")
```

Expected output:
```
PASS run_001: 4/4 entries, 0 nulls
PASS run_002: 4/4 entries, 0 nulls
PASS run_003: 4/4 entries, 0 nulls
PASS run_004: 4/4 entries, 0 nulls
PASS run_005: 4/4 entries, 0 nulls

WEEK 2 GATE: PASS
```

---

## Week 2 Completion Gate Checklist

- [ ] `structured_logger.py` smoke test: `from structured_logger import log_entry` → OK
- [ ] `notebook_02_linear.ipynb` runs all 6 cells without exception
- [ ] `run_002.jsonl` — 4 entries, 0 nulls
- [ ] `run_003.jsonl` — 4 entries, 0 nulls
- [ ] `INJECTION_CONFIRMED` in `agent_1_summarizer` post_generation of `run_003`
- [ ] `notebook_03_parallel.ipynb` runs all 6 cells without exception
- [ ] `run_004.jsonl` — 4 entries, 0 nulls
- [ ] `run_005.jsonl` — 4 entries, 0 nulls
- [ ] `pyautogen==0.2.35` in `requirements.txt`
- [ ] End-to-end smoke test: `WEEK 2 GATE: PASS`
- [ ] Overall Week 2 status: COMPLETE

---

## Immediate Next Action

Create `structured_logger.py` at the project root.
Do not begin `notebook_02_linear.ipynb` until the logger smoke test passes.
