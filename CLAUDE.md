# CLAUDE.md — Repository Memory File

> **READ THIS FIRST.** This is your operating guide for this repository.
> Do not modify any code, rename any files, or restructure any directories
> until you have completed the Repository Entry Protocol in
> `.claude/skills/entry-protocol.md`.

---

## 1. Project Identity

**Project Name:** `agentic-pipeline-injection`
**Purpose (WHY):** `Indirect prompt injection propagation in agentic AI pipelines`
**Status:** `Active Development`  <!-- Active Development | Maintenance | Portfolio | Archived -->
**Primary Language(s):** `Python 3.11`
**Framework(s):** `None`
**Owner / Portfolio:** `BUDDY26`

---

## 2. Repository Map (WHAT)

```
agentic-pipeline-injection/
├── corpus/                          # Locked research corpus (4 benign + 1 adversarial)
├── corpus_loader.py                 # FAISS index build, load, and retrieval
├── llm_client.py                    # Ollama (primary) + Groq (fallback) LLM interface
├── structured_logger.py             # JSONL structured experiment logger
├── faiss_index/                     # Persisted vector index (locked after Week 1)
├── src/
│   └── metrics.py                   # integrity_score, compromise_signal, propagation_depth
├── notebooks/
│   ├── notebook_01_rag.ipynb        # RAG pipeline topology
│   ├── notebook_02_linear.ipynb     # Linear chain topology
│   ├── notebook_03_parallel.ipynb   # Parallel fan-out topology
│   └── notebook_04_experiments.ipynb # 9-configuration experiment matrix
├── experiment_logs/                 # val_*.jsonl validation logs + pre_audit/ archive
├── results/
│   ├── validation/                  # multi-run validation artifacts (canonical)
│   ├── figures/                     # publication-quality figures (PNG + PDF)
│   └── archive/pre_audit/           # superseded Week 3 taxonomy.csv and charts
├── scripts/
│   ├── run_multi_validation.py      # 27-run validation driver
│   ├── recompute_validation_metrics.py  # Metric recomputation from logs
│   └── generate_figures.py          # Figure generation from results CSV
├── docs/
│   ├── architecture.md
│   ├── implementation-plan.md
│   ├── adr/
│   ├── qa/
│   └── runbooks/
├── tracking/                        # internal planning + progress reports (not public-facing)
├── requirements.txt
└── .env.example
```

**Key Entry Points:**
- `notebooks/notebook_04_experiments.ipynb` — full 9-configuration experiment matrix driver
- `scripts/run_multi_validation.py` — 27-run multi-run validation runner
- `corpus_loader.py` — FAISS index build and retrieval (run once to initialize)

**Configuration Files:**
- `.env.example` — environment variable reference (never commit `.env`); requires `GROQ_API_KEY` for fallback LLM

**Test Suite:**
- `tests/` — pytest, run with `pytest tests/ -v` (no tests implemented; validation performed via experiment methodology)

---

## 3. Rules + Commands (HOW)

### ✅ Allowed Without Asking
- Read any file
- Improve documentation (docstrings, comments, README, CLAUDE.md)
- Fix formatting and style inconsistencies
- Add or improve inline comments
- Add new test files in `tests/`
- Update `.env.example` with new variable names (never values)

### ⚠️ Requires Explicit Approval Before Executing
- Renaming or moving any file or directory
- Changing function signatures or public APIs
- Adding, removing, or upgrading dependencies
- Modifying database schemas or migration files
- Editing files in `src/auth/`, `src/billing/`, or `infra/`
- Deleting any file
- Creating new top-level directories

### 🚫 Never Do
- Commit or push to any branch
- Execute `rm -rf` or any irreversible destructive command
- Modify `.env` files or embed secrets in source code
- Run `DROP TABLE`, truncate databases, or execute destructive SQL
- Merge branches or create releases

### Common Commands
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python src/main.py

# Run tests
pytest tests/ -v

# Run linter + formatter
ruff check src/ && black src/
```

---

## 4. Repository Governance Rules

Documentation is the source of truth for this repository. Code follows documentation — never the reverse.

### External Orchestration Boundary

An external orchestration system (such as Claude Cowork) may determine **what** task is being worked on and **when** work begins. This repository governs **how** implementation is performed. External orchestration does not override repository-level implementation constraints, permission tiers, or the authority hierarchy defined below. If an external system routes a task to this repository, the task is executed under this repository's rules.

### Authority Hierarchy

```
Paper / External Sources
         ↓
   Evidence Ledger
         ↓
 Architecture Document
         ↓
    ADR Decisions
         ↓
 Implementation Plan
         ↓
        Code
```

Each layer is authoritative over everything below it. If code and documentation disagree, documentation wins and the code must be corrected — or an explicit change request must be approved before documentation is updated.

### Layer Responsibilities

| Layer | Location | Role |
|-------|----------|------|
| External sources | Research papers, specs, reports | Primary evidence; facts extracted here are non-negotiable |
| Evidence ledger | `docs/evidence.md` *(if applicable)* | Confirmed facts extracted from external sources; separates evidence from assumptions |
| Architecture | `docs/architecture.md` | System design, component map, data flow |
| ADRs | `docs/adr/*.md` | Binding architectural decisions with documented rationale |
| Implementation plan | `tracking/implementation-plan.md` *(if applicable)* | Coding order, module scope, deliverables |
| Code | `src/` | Implementation — must conform to all layers above |

### Rules

- ADRs are binding once accepted. Do not re-litigate an accepted ADR without creating a superseding one.
- The implementation plan defines what gets built and in what order. Code must follow it.
- An AI assistant must not modify ADRs or the implementation plan automatically.

### Conflict Resolution Protocol

If a conflict is discovered — the plan cannot be followed exactly as written — the assistant must:

1. **Report** the conflict: what the plan specifies vs. what the implementation requires.
2. **Explain** why the current plan cannot be followed exactly.
3. **Propose** a specific, minimal change to the plan or ADR.
4. **Wait** for explicit approval before modifying any documentation.

Do not silently deviate from the plan. Do not edit governance documents without completing this protocol.

---

## 5. Implementation Plan Authority

`tracking/implementation-plan.md` is the authoritative coding guide for this repository when present.

### Status During Coding Passes

The implementation plan is **read-only during coding passes**. It defines what to build and in what order. An AI assistant must not edit it while implementing code — not to mark progress, not to add notes, not to correct phrasing.

### Progress Reporting

Report implementation progress in responses rather than by editing the file:

> "Completed: `src/config.py`, `src/data.py`. Next: `src/env.py`."

### Conflict Protocol

If a true implementation conflict is discovered during a coding pass:

1. **Stop** the current coding pass.
2. **Report** the conflict clearly: plan specification vs. what the code requires.
3. **Propose** a minimal, targeted change to the plan.
4. **Wait** for explicit approval.

Once approved: update the plan first, then update the code to match.

---

## 6. Architecture Summary

This project implements a controlled research framework for studying indirect prompt injection propagation in agentic AI pipelines. A fixed adversarial document is embedded within a FAISS-indexed corpus alongside benign documents; three pipeline topologies (RAG, Linear Chain, Parallel fan-out) retrieve from that corpus and route content through one or more LLM-backed agents. A metrics module scores each run for integrity degradation, propagation depth, and compromise signal presence, and all runs are captured in structured JSONL experiment logs. The system is designed for reproducibility: corpus, index, query, and model configuration are locked across all runs, allowing multi-run validation to isolate injection effects from LLM non-determinism.

> Full system design, component breakdown, and data flow are documented in
> `docs/architecture.md`. Key technical decisions are in `docs/adr/`.

---

## 7. Known Issues / Sharp Edges

- **Pre-audit artifacts are archived, not deleted.** Week 3 pre-audit artifacts have been moved to `experiment_logs/pre_audit/` (original 8 `run_00*.jsonl` logs) and `results/archive/pre_audit/` (superseded `taxonomy.csv` and `charts/`). These are retained for provenance only. The canonical record is `experiment_logs/val_*.jsonl` (27 logs) and `results/validation/` + `results/figures/`. Do not cite pre-audit files as current evidence.
- **FAISS index must not be rebuilt.** `faiss_index/index.faiss` and `faiss_index/index.pkl` were built once in Week 1 and are the reference for every experiment log in the repository. Rebuilding invalidates all prior logs by changing retrieval rank assignments.
- **Stage-1 compromise signal is literal-match only.** `compromise_signal()` in `src/metrics.py` uses regex to detect the known injection string verbatim. Paraphrased payloads are not captured; reported `cs_rate` values are a lower bound on true injection influence. `integrity_score` partially compensates.
- **No automated test suite.** `tests/unit/` and `tests/integration/` exist but contain no test files. Validation is performed entirely via the experiment methodology and the independent-recomputation path (`scripts/recompute_validation_metrics.py`).
- **Internal process docs live in `tracking/`.** Week-by-week planning files and earlier progress reports have been moved out of `docs/` into `tracking/planning/` and `tracking/reports/`. They are not part of the public-facing documentation story.

---

## 8. Skills Available

| Skill | File | Purpose |
|-------|------|---------|
| Entry Protocol | `.claude/skills/entry-protocol.md` | **Run first** — mandatory scan before any changes |
| Code Review | `.claude/skills/code-review.md` | Structured review with severity-labeled findings |
| Refactor Playbook | `.claude/skills/refactor-playbook.md` | Safe, proposal-first refactoring workflow |
| Documentation | `.claude/skills/documentation.md` | Docstrings, README, architecture docs, ADRs |
| QA Checklist | `.claude/skills/qa-checklist.md` | Test coverage + portfolio readiness audit |
| Release Procedure | `.claude/skills/release-procedure.md` | Steps before tagging a version |

---

## 9. Hooks Active

| Hook | Trigger | Action |
|------|---------|--------|
| `post-edit-format` | After editing `.py` / `.ts` / `.js` files | Suggest running formatter |
| `pre-delete-guard` | Before any file deletion | Halt and require explicit confirmation |
| `test-on-core-change` | After editing files in `src/` | Remind to run test suite |
| `block-sensitive-dirs` | Before modifying `auth/`, `billing/`, `infra/`, `migrations/` | Halt and require approval |
| `no-secrets-in-code` | Before writing string literals resembling keys/tokens | Replace with env variable pattern |
| `proposal-before-refactor` | Before renaming, moving, or changing signatures | Write proposal first |

---

## 10. Documentation Index

| Document | Location | Description |
|----------|----------|-------------|
| Architecture Overview | `docs/architecture.md` | Full system design and component breakdown |
| ADR Index | `docs/adr/` | All architectural decision records |
| Operations Runbook | `docs/runbooks/operations.md` | Setup, deployment, and troubleshooting |

---

## 11. Portfolio Context

**Target Audience:** Graduate admissions reviewers (UT Austin MSCS), software engineering employers
**Demonstrates:**
- Multi-agent pipeline design across structurally distinct topologies (RAG, linear chain, parallel fan-out)
- Adversarial robustness analysis: controlled injection protocol with configurable payload rank and reproducible methodology
- Logging and metrics systems: structured JSONL experiment logging, multi-metric scoring (integrity score, compromise signal, propagation depth)
- Reproducible experimentation: locked corpus/index/query/model configuration; 27-run multi-run validation with aggregated statistics and baseline control verification
- Research communication: quantitative taxonomy, visualization charts, validation summary with documented limitations, advisor-facing progress brief

**Key Technical Decisions:** See `docs/adr/` for documented rationale
**Portfolio Repository:** Yes — maintain professional commit history and documentation standards

---

<!-- TEMPLATE-MIRROR:SECTION12:START -->
## 12. Agent Operating Constraints

These are mandatory operating constraints for Claude Code to prevent context loss, silent truncation errors, incorrect edits, incomplete search results, and unsafe multi-file execution. They apply to **all repositories** instantiated from this template.

### 12.1 Dead Code First

Before any structural refactor on large files:

- Remove unused imports, exports, props, and debug logs
- Perform cleanup as a separate change set
- Do NOT combine cleanup and refactor in the same pass

### 12.2 Batched Execution

For tasks touching multiple files:

- Break work into small batches (max ~5 files per batch)
- Complete and verify each batch before continuing
- State the batch plan before starting so the user can confirm grouping

### 12.3 Context Decay Awareness

- Do NOT rely on memory of file contents after long conversations
- Re-read files before editing when uncertain
- If context compaction may have fired, say so explicitly

### 12.4 File Read Limits

- Large files may be silently truncated when read
- Read files in chunks when necessary (state chunk boundaries explicitly)
- Never assume full file visibility from a single read

### 12.5 Tool Result Awareness

- Search results may be incomplete due to truncation
- Re-run searches with narrower scope if results look suspiciously small
- Never treat a small result set as definitively complete without scoped verification

### 12.6 Edit Integrity

For every edit:

1. Read the file immediately before editing
2. Apply the change
3. Re-read the file after editing to confirm the change applied correctly

If a re-read reveals the edit did not apply, diagnose the mismatch before retrying.

### 12.7 No Semantic Assumptions

- Search tools perform text matching only — not semantic code understanding
- Do NOT assume a single search caught all references
- On any rename, signature change, or symbol deletion: check direct calls, type references, string literals, dynamic imports, re-exports, test files, and config files separately

### 12.8 Rule Suspension

If the user explicitly states **"suspend rule X for this session"**, that rule is temporarily inactive until the user says **"restore rules"** or a new session begins. Rules may only be suspended by the user — do not self-suspend a rule because it is inconvenient.

<!-- TEMPLATE-MIRROR:SECTION12:END -->

---

<!-- TEMPLATE-MIRROR:FOOTER:START -->
*Entry protocol completed: `no — run on first session`*
<!-- TEMPLATE-MIRROR:FOOTER:END -->
