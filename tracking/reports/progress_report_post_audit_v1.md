# agentic-pipeline-injection — Progress Report
**Post-Audit v1 (Revised)**
Date: 2026-04-08

---

## 1. Project Overview

This project implements and evaluates the propagation of indirect prompt injection attacks in agentic AI pipelines. The study examines how adversarial instructions embedded in retrieved content influence downstream model outputs across three pipeline topologies: RAG-based retrieval, linear multi-agent chains, and parallel agent systems with aggregation.

The system is designed as a controlled experimental framework. It produces deterministic, reproducible results and includes structured logging of retrieval and generation steps, with metrics for analyzing propagation behavior and compromise signals. The target deliverable is a research poster for presentation at the UTRGV STEM Research Conference on April 24, 2026.

## 2. Initial Progress — Weeks 1–3 and Early Week 4

The initial implementation served as a foundational layer for the experimental system. The system produced outputs and appeared complete at the end of Week 3; however, subsequent investigation revealed that it did not meet the evidentiary standard required for research-level defensibility. During Weeks 1 through 3, the following components were established:

- Pipeline implementations for all three topologies (RAG, Linear, Parallel).
- A corpus of benign and adversarial documents with injection instructions.
- An initial metrics module defining compromise_signal and propagation_depth.
- A retrieval system integrated with Ollama (llama3.1:8b) for local execution.
- Experiment notebooks (notebook_01 through notebook_04) covering all pipeline variants.
- A preliminary experimental run producing initial results across 9 configurations.

Early Week 4 work produced multi-run validation artifacts and a reproducibility analysis. These outputs confirmed that the pipeline architecture was structurally operational. However, the Week 3 gate did not include verification of determinism, retrieval rank correctness, or metric definition alignment. These gaps were discovered through subsequent investigation and required targeted correction before the system could be considered defensible.

## 3. Audit Findings

A formal audit identified that the initial system, while operationally functional, was not defensible as a research instrument. The deficiencies were not assumed upfront; they were discovered through investigation. As a direct consequence, the results produced by the initial experimental run could not be used as the validated basis for the research findings, and a full re-execution under corrected conditions was required. Four structural issues were identified:

- **Determinism not enforced:** LLM temperature was not fixed at 0, introducing the possibility of non-deterministic outputs across repeated runs. Results produced under this condition cannot be verified as reproducible.

- **Retrieval rank not logged:** Pre-generation log entries did not consistently capture rank, score, label, and document_id for retrieved chunks, making it impossible to verify which document was retrieved at which rank position. This is a core experimental variable and its absence undermines result traceability.

- **Stage 2 ambiguity:** The compromise_signal function retained a Stage 2 behavioral divergence check that was inconsistently applied and not aligned with the defined experimental design, creating ambiguity in what the metric was actually measuring.

- **Propagation definition unclear:** The propagation_depth metric did not have a formally stated definition aligned with its implementation. The relationship between hop count, index, and literal-match inclusion was ambiguous, making the metric uninterpretable without correction.

The architecture and pipeline structure established in Weeks 1–3 remained usable as the basis for re-execution. However, the experimental record from the initial run was superseded in full. No results from the pre-remediation run are used as research findings in this report.

## 4. Remediation Actions

The system was refined and re-executed under controlled conditions. Four targeted remediations (REM-01 through REM-04) were applied to address each identified issue:

| ID | Area | Action Taken |
|----|------|-------------|
| REM-01 | Deterministic Execution | Enforced temperature = 0 across all LLM paths (Ollama and Groq). Confirmed via code inspection and byte-identical log files across repeated runs. |
| REM-02 | Retrieval Rank Logging | Verified that retrieved_chunks (rank, score, label, document_id) are logged in pre_generation entries for all three pipeline topologies. |
| REM-03 | Stage 2 Retirement | Removed behavioral divergence check (Stage 2) from compromise_signal(). Function locked to Stage 1 only: artifact string matching via regex. |
| REM-04 | Propagation Definition Alignment | Redefined propagation_depth() to return the index of the last compromised hop (not a count). Literal-match inclusion confirmed via OR condition in code. |

All remediations were applied to the production codebase (llm_client.py, src/metrics.py, scripts/run_multi_validation.py, scripts/recompute_validation_metrics.py) and verified via code inspection before re-execution.

## 5. Re-Execution Results

Following remediation, the experiment was re-executed in full across all nine configurations. The corrected run was completed on 2026-04-06 using Ollama (llama3.1:8b) with temperature fixed at 0. These results supersede those of the initial experimental run (completed 2026-04-01), which was conducted prior to remediation and is not used as the basis for research findings.

- Total runs: 27 (9 configurations × 3 runs each).
- Configurations: RAG, Linear, and Parallel topologies × Baseline, Rank-1, and Rank-3 injection conditions.
- Propagation depth: deterministic across all runs (std = 0), confirming topology-determined behavior.
- Baseline behavior: all 9 baseline rows produced depth = 0, score = 1.0, cs = False.
- Rank logging: adversarial documents confirmed at the correct rank position in all injected runs.
- Stage 1 compromise signal rate (cs_rate) for Parallel-Rank-1: 0.3333 (1 of 3 runs triggered). Note: this value reflects the corrected run and differs from the pre-fix run, which recorded cs_rate = 1.00 under non-deterministic conditions.
- Linear-Rank-1 cs_rate: 1.00 (artifact execution confirmed in all 3 runs).

All 27 JSONL log files were produced and retained. Results were compiled into results/validation/multi_run_results.csv (27 per-run rows + 9 aggregate rows). Byte-identical log files across repeated runs confirmed that determinism held throughout.

## 6. Formal Audit Outcome

A structured post-run audit was executed on 2026-04-08 under control rules, operating in read-only mode against the corrected experimental artifacts. The audit covered five sections:

| Audit Section | Result | Evidence |
|---------------|--------|----------|
| Log Completeness | PASS | 27 val_*.jsonl files confirmed (9 configs × 3 runs). All non-empty. |
| Rank Logging | PASS | retrieved_chunks with rank, score, label, document_id verified in all injected logs. |
| Stage 2 Absence | PASS | compromise_signal() confirmed as Stage 1 only in code and all call sites. |
| Propagation Alignment | PASS | Docstring and implementation confirmed: last compromised hop index, literal-match included. |
| Results Consistency | PASS | All 9 baseline rows: depth=0, score=1.0, cs=False. Row count verified (37 total). |

Overall Result: PASS — No blocking items. Audit record logged to tracking/post_run_audit_2026-04-08.md.

One non-blocking item was flagged: results/validation/validation_summary.md reflects the pre-fix (2026-04-01) run and contains metrics inconsistent with the corrected experiment. This document requires rewrite before poster finalization and does not affect the validity of the corrected experimental record.

## 7. Current System Status

The current version represents a validated experimental baseline and is the first version of the system that meets the evidentiary standard required for research presentation. The system state as of 2026-04-08 is as follows:

- **Experiment:** v1 corrected — 27-run validation complete, deterministic execution confirmed.
- **Metrics:** Stage 1 only compromise_signal locked. Propagation depth defined as last compromised hop index. Self-comparison baseline for integrity_score confirmed.
- **Logging:** Retrieval rank, score, label, and document_id verified across all 27 JSONL logs.
- **Audit:** Formal post-run audit PASS. All five sections cleared. No blocking issues.
- **Pending:** validation_summary.md rewrite required. Poster directory not yet created.

## 8. Forward Positioning

This version is suitable for further testing, refinement, and final presentation. The corrected experimental system provides a stable, defensible foundation from which poster development and final results communication can proceed with confidence.

The primary evidentiary record is complete: code, logs, metrics, and audit outputs are consistent and traceable. One remaining documentation task — the rewrite of validation_summary.md — must be completed before the full record is internally consistent. The pipeline architecture supports re-execution under alternative configurations if needed. All control constraints are in place to prevent scope drift during the poster phase.

The immediate next step is Week 4 Step 4: Poster Layout and Content, beginning with a rewrite of validation_summary.md to align the human-readable summary with the corrected experimental record. The conference submission deadline is April 24, 2026.

---

*Report generated: 2026-04-08 | Version: Post-Audit v1 (Revised) | Status: Post-Audit PASS | Next: Week 4 Step 4*
