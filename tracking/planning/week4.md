# Week 4 Planning — Poster Design, Polish, and Rehearsal

**Project:** agentic-pipeline-injection
**Authority:** tracking/reference/timeline_prompt_injection_research.pdf (Days 22–28, ~10–12 hours, Week 4), tracking/reference/agentic_pipeline_injection_template.pdf (Sections 10–11), tracking/reference/abstract_final_v3.pdf, tracking/reference/speaker_reference_chuprov.pdf
**Status:** Week 4 — Ready to Begin (Week 3 complete and verified via audit + gate)
**Last updated:** 2026-03-31

---

## A. Objective

Design and produce a print-ready 36" × 48" portrait research poster for the UTRGV STEM
Research Conference 2026 (April 24, 2026), submit it to the UTRGV Library print queue by
Day 26, and rehearse a 4–5 minute poster walkthrough targeting a non-CS STEM audience.
All poster content must be grounded in the finalized taxonomy table and charts from Week 3.

---

## B. Rationale

Weeks 1–3 produced the complete experimental pipeline: infrastructure, three pipeline
topologies, a metrics module, 9 experiment runs, a taxonomy CSV with quantitative values,
and supporting charts. Week 4 is the final delivery phase — it translates those results
into a conference-ready poster and a rehearsed oral presentation. This is explicitly
defined as the fourth and final week in the project timeline (Days 22–28).

The gap Week 4 addresses: the research findings currently exist only as code outputs
(taxonomy.csv, PNG charts, notebook cells). They must be formatted into a visual poster
with narrative structure, printed physically, and the presenter must be able to explain
the work from memory in under 5 minutes.

---

## C. Scope Boundaries

### In scope
- Design 36" × 48" portrait poster using UTRGV branding colors
- Poster sections: Title/Author, Motivation (trust-violation hook from abstract), System Architecture diagram, Experiment Protocol, Taxonomy Table, Key Findings (2–3 highlighted results), Implications for Practitioners, Acknowledgements
- Finalize all charts and figures at print resolution (300 DPI minimum)
- Confirm taxonomy table is readable from 10 feet — increase font size if needed
- Export final poster as PDF
- Submit poster PDF to UTRGV Library print queue by Day 26
- Keep a local backup copy of the PDF
- Conduct two full rehearsed poster walkthroughs with timer (target: 4–5 minutes)
- Practice the non-technical opening: lead with the trust-violation hook
- Prepare written notes for 3–5 anticipated Q&A responses
- Final accuracy check: verify every number on the poster matches the exported taxonomy.csv
- Confirm no empirical claims exceed what the experiment data supports
- Graduate-level validation: multi-run experiments, reproducibility, control validation, limitations documentation

### Out of scope
- New adversarial document variants
- Defender layer, trust scoring, or model comparison (v2 roadmap)
- Hub-and-spoke topology or CrewAI framework
- SQLite log migration
- Any code changes to existing src/, notebooks/, corpus/, or experiment_logs/ files (new validation scripts are permitted)
- Paper or thesis drafting (post-conference)
- Production deployment

---

## D. Directory Structure — End of Week 4

Files marked NEW are created this week. Everything else is unchanged from Week 3.

```
agentic-pipeline-injection/
├── corpus/                            ← unchanged
├── src/                               ← unchanged
├── structured_logger.py               ← unchanged
├── faiss_index/                       ← unchanged
├── experiment_logs/                   ← unchanged (Week 1–3 logs preserved)
├── notebooks/                         ← unchanged
├── results/
│   ├── taxonomy.csv                   ← unchanged (source of truth for poster numbers)
│   ├── charts/                        ← unchanged (source images for poster figures)
│   └── validation/                    ← NEW directory
│       ├── multi_run_results.csv      ← NEW: aggregated multi-run metrics
│       ├── baseline_stability.csv     ← NEW: baseline consistency verification
│       └── validation_summary.md      ← NEW: reproducibility + control analysis
├── poster/                            ← NEW directory
│   ├── poster_final.pdf               ← NEW: print-ready poster (300 DPI, 36" × 48")
│   └── poster_source.*                ← NEW: editable source file (PowerPoint, Canva, or Illustrator)
├── docs/
│   └── planning/
│       └── week4.md                   ← NEW: this file
├── rehearsal/                         ← NEW directory
│   ├── walkthrough_notes.md           ← NEW: structured 4–5 min walkthrough script
│   └── qa_responses.md                ← NEW: 3–5 anticipated Q&A with prepared answers
└── requirements.txt                   ← unchanged
```

---

## E. Ordered Deliverables

| # | Deliverable | Notes |
|---|---|---|
| 1 | Multi-run validation runs | 3–5 runs per configuration across all 3 topologies |
| 2 | `results/validation/multi_run_results.csv` | Aggregated metrics: mean, std, min, max per topology × config |
| 3 | `results/validation/baseline_stability.csv` | Baseline consistency verification across repeated runs |
| 4 | `results/validation/validation_summary.md` | Reproducibility report + control analysis + limitations |
| 5 | `poster/poster_source.*` | Editable poster file with all sections laid out |
| 6 | Taxonomy table accuracy check | Every number on the poster verified against `results/taxonomy.csv` |
| 7 | Chart resolution verification | All charts confirmed at 300 DPI, readable at poster scale |
| 8 | `poster/poster_final.pdf` | Print-ready PDF export (36" × 48" portrait, 300 DPI) |
| 9 | Library print queue submission | Poster PDF submitted to UTRGV Library by Day 26 |
| 10 | `rehearsal/walkthrough_notes.md` | Structured walkthrough script (4–5 minutes) |
| 11 | `rehearsal/qa_responses.md` | Written answers to 3–5 anticipated questions |
| 12 | Two timed rehearsal completions | Both under 5 minutes, covering all poster sections |

Deliverables 1–4 (validation) must be complete before deliverables 5–8 (poster design).
Deliverables 5–8 (poster design + export) must be complete before deliverable 9 (print submission).
Deliverables 10–11 (rehearsal prep) can begin in parallel with poster polish.
Deliverable 12 (timed rehearsals) must come last.

---

## F. Tasks (Ordered, Execution-Ready)

### Step 1 — Multi-Run Validation (First Execution Step)

**Purpose:** Re-run each pipeline configuration 3–5 times to establish statistical
reliability of the Week 3 single-run results. This is required for graduate-level
rigor — single-run metrics are insufficient to claim consistent behavior.

**Runs to execute:**

| Topology | Config | Existing Run | New Runs (3–5 each) |
|---|---|---|---|
| RAG | Baseline | run_001 | val_rag_baseline_01 – val_rag_baseline_05 |
| RAG | Injected-Rank-1 | run_001 (mixed) | val_rag_rank1_01 – val_rag_rank1_05 |
| RAG | Injected-Rank-3 | run_006 | val_rag_rank3_01 – val_rag_rank3_05 |
| Linear | Baseline | run_002 | val_linear_baseline_01 – val_linear_baseline_05 |
| Linear | Injected-Rank-1 | run_003 | val_linear_rank1_01 – val_linear_rank1_05 |
| Linear | Injected-Rank-3 | run_007 | val_linear_rank3_01 – val_linear_rank3_05 |
| Parallel | Baseline | run_004 | val_parallel_baseline_01 – val_parallel_baseline_05 |
| Parallel | Injected-Rank-1 | run_005 | val_parallel_rank1_01 – val_parallel_rank1_05 |
| Parallel | Injected-Rank-3 | run_008 | val_parallel_rank3_01 – val_parallel_rank3_05 |

**Compute per configuration:**
- Mean `propagation_depth`
- Mean `integrity_score`
- Standard deviation of `integrity_score`
- `compromise_signal` consistency (rate across N runs)
- Identify any outliers (runs where metrics differ > 2σ from mean)

**Constraints:**
- Use the same `TEST_QUERY` and corpus configuration as Weeks 1–3
- Use the same LLM configuration (Ollama llama3.1:8b or Groq fallback)
- Store validation logs separately — do NOT overwrite run_001 through run_008
- Minimum 3 runs per configuration; target 5 if time permits

**Acceptance criteria:**
- [ ] At least 3 completed runs per configuration (9 configs × 3 = 27 minimum runs)
- [ ] `results/validation/multi_run_results.csv` exists with mean, std, min, max per config
- [ ] No configuration has 100% outlier rate (at least 2/3 runs must be consistent)

### Step 2 — Reproducibility + Control Validation

**Purpose:** Verify that repeated runs under identical conditions produce consistent
results, and that baseline runs remain stable (control integrity).

**Reproducibility checks:**
1. Confirm all validation runs used identical inputs (same query, same corpus, same model)
2. Document environment: Python version, Ollama model, Groq fallback status, OS
3. Verify baseline runs: `propagation_depth` must be 0, `integrity_score` must be ≈1.0,
   `compromise_signal` must be False across ALL baseline repetitions
4. If any baseline run deviates, flag as a control failure and investigate

**Control validation:**
1. Compare baseline variance to injected variance
2. Confirm that differences between baseline and injected runs are consistent and
   attributable to injection behavior, not LLM randomness
3. If injected-run variance is high, document as a finding (LLM non-determinism as
   a confound)

**Acceptance criteria:**
- [ ] `results/validation/baseline_stability.csv` shows all baseline runs with `propagation_depth=0`
- [ ] Baseline `integrity_score` standard deviation < 0.05 across repetitions
- [ ] `results/validation/validation_summary.md` documents reproducibility and control analysis

### Step 3 — Limitations Documentation

**Purpose:** Document known limitations of the experimental design for inclusion in the
poster and for academic honesty.

**Required limitations (from project evidence):**
1. **Single model configuration** — All experiments use Ollama llama3.1:8b (4-bit quant)
   or Groq llama3-8b-8192. Results may not generalize to other LLMs.
2. **Limited adversarial variants** — Only body-text injection with a single artifact
   string (`INJECTION_CONFIRMED`). Markup injection, whitespace injection, and Unicode
   injection are out of scope (v2 roadmap).
3. **Paraphrase evasion** — `compromise_signal` Stage 1 relies on literal string matching.
   If the LLM paraphrases the injection instruction, Stage 1 misses it. Stage 2
   (integrity_score divergence) partially mitigates this but may not capture subtle influence.
4. **LLM non-determinism** — Even with identical inputs, LLM outputs may vary across runs.
   Multi-run validation (Step 1) quantifies this variance but cannot eliminate it.
5. **Observed patterns, not universal guarantees** — Results demonstrate behavior under
   controlled conditions with a specific corpus and model. They are not proof of universal
   vulnerability across all agentic systems.

**Acceptance criteria:**
- [ ] All 5 limitations documented in `results/validation/validation_summary.md`
- [ ] Poster includes a "Limitations" or "Scope" callout referencing at least 3 of the 5

### Step 4 — Poster Layout + Content (Days 22–23)

**Purpose:** Create the poster in PowerPoint, Canva, or Adobe Illustrator at 36" × 48" portrait orientation.

**Poster sections (from timeline):**

| Section | Content Source |
|---|---|
| Title / Author block | Abstract title + author info from `abstract_final_v3.pdf` |
| Motivation | Trust-violation hook from abstract paragraph 1 |
| System Architecture diagram | 6-layer architecture from `agentic_pipeline_injection_template.pdf` Section 2 |
| Experiment Protocol | 9-run matrix (3 topologies × 3 corpus configs) from `week3.md` Step 3 |
| Taxonomy Table | `results/taxonomy.csv` — all 7 columns, 3 rows |
| Key Findings | 2–3 highlighted results derived from taxonomy and multi-run validation |
| Multi-Run Validation Summary | Mean ± std for key metrics across repeated runs |
| Limitations | 3+ items from Step 3 limitations list |
| Implications for Practitioners | Drawn from abstract final paragraph + speaker reference Part 4 |
| Acknowledgements | Dr. Sergei Chuprov, UTRGV M.S. Computer Science |

**Branding:** Use UTRGV branding colors.

**Acceptance criteria:**
- [ ] Poster file exists with all sections populated
- [ ] Layout is 36" × 48" portrait
- [ ] Taxonomy table is present with all 7 columns and 3 topology rows
- [ ] At least one chart from `results/charts/` is included
- [ ] Architecture diagram is included
- [ ] Multi-run validation summary is included
- [ ] Limitations section is present

### Step 5 — Polish + Print Submission (Days 24–26)

**Purpose:** Finalize visual quality, verify data accuracy, and submit to the library print queue.

**Tasks:**
1. Confirm all charts and figures are at 300 DPI minimum
2. Confirm the taxonomy table is readable from 10 feet — increase font size if needed
3. Check that all text is clear and jargon is defined
4. Run accuracy check: compare every number on the poster against `results/taxonomy.csv`
5. Verify multi-run numbers on poster match `results/validation/multi_run_results.csv`
6. Export final poster as PDF
7. Submit to UTRGV Library print queue by Day 26
8. Keep a local backup copy of the PDF in `poster/poster_final.pdf`

**Acceptance criteria:**
- [ ] `poster/poster_final.pdf` exists (300 DPI, 36" × 48")
- [ ] Every quantitative value on the poster matches source CSVs exactly
- [ ] All charts are print-resolution (not pixelated at poster scale)
- [ ] Poster PDF submitted to library print queue by Day 26

### Step 6 — Rehearsal + Q&A Prep (Days 27–28)

**Purpose:** Rehearse the poster walkthrough and prepare for anticipated questions.

**Walkthrough structure (from speaker_reference_chuprov.pdf):**
1. Non-technical opening — lead with the trust-violation hook (from abstract)
2. Research question — does pipeline topology change how dangerous injection is?
3. System architecture — 6 layers, 3 pipelines
4. Experiment protocol — 9 runs, controlled corpus, metrics from logs
5. Key findings — taxonomy table as anchor, 2–3 highlighted results
6. Multi-run validation — "we confirmed consistency across N repeated runs"
7. Limitations — acknowledge scope honestly
8. Implications — what a defender would do with this taxonomy

**Q&A preparation (from speaker_reference_chuprov.pdf):**

| Anticipated Question | Source |
|---|---|
| What is prompt injection? How is indirect different from direct? | Speaker ref Part 1 |
| Why study topology instead of just the model? | Speaker ref Part 1 |
| How are you measuring injection success? | Speaker ref Part 3 |
| How do you ensure this is a controlled experiment? | Speaker ref Part 3 |
| What would a defender do with this taxonomy? | Speaker ref Part 4 |

**Acceptance criteria:**
- [ ] `rehearsal/walkthrough_notes.md` exists with structured script
- [ ] `rehearsal/qa_responses.md` exists with 3–5 Q&A pairs
- [ ] Two timed walkthroughs completed, both under 5 minutes
- [ ] Walkthrough covers all poster sections using taxonomy table as anchor

---

## G. Graduate-Level Validation (Multi-Run Requirement)

### Purpose

Single experiment runs (Week 3) demonstrate feasibility but do not establish reliability.
Graduate-level research requires evidence that results are reproducible and not artifacts
of LLM randomness. This section defines the multi-run validation protocol.

### Protocol

- Re-run each pipeline (RAG, Linear, Parallel) under each corpus configuration
  (Baseline, Injected-Rank-1, Injected-Rank-3)
- Minimum: 3 runs per configuration (27 total minimum)
- Target: 5 runs per configuration (45 total) if time permits
- Compute per configuration:
  - Average `propagation_depth`
  - Average `integrity_score`
  - Standard deviation of `integrity_score`
  - `compromise_signal` consistency rate (proportion of runs where signal = True)
- Identify:
  - Variance across runs (is behavior stable or noisy?)
  - Outliers (any run where metrics differ > 2σ from the configuration mean)
  - Stability pattern: do results converge or diverge with more runs?

### Output

- `results/validation/multi_run_results.csv` — one row per run, columns: run_id, topology,
  config, propagation_depth, integrity_score, compromise_signal
- Aggregated summary appended: mean, std, min, max per configuration

---

## H. Reproducibility Check

### Purpose

Confirm that the experimental setup produces consistent results when repeated under
identical conditions. This is a core requirement for any published research.

### Protocol

1. Document execution environment:
   - Python version
   - Ollama model and version (llama3.1:8b, quantization)
   - Groq fallback status (used or not)
   - Operating system
   - FAISS index state (unchanged from Week 1)
2. Verify that all validation runs used:
   - The same `TEST_QUERY` as Weeks 1–3
   - The same corpus (4 benign + 1 adversarial)
   - The same retrieval configuration (`RETRIEVAL_K=3`)
3. Compare validation run results to original Week 3 single-run results
4. Flag any significant deviations (> 2σ from original values)

### Output

- Reproducibility analysis documented in `results/validation/validation_summary.md`

---

## I. Experimental Control Validation

### Purpose

Validate that baseline runs (clean corpus, no adversarial document) remain stable across
repetitions, confirming that observed differences in injected runs are attributable to
injection behavior rather than random LLM variation.

### Protocol

1. Across all baseline repetitions, verify:
   - `propagation_depth` = 0 (every run)
   - `integrity_score` ≈ 1.0 (std < 0.05)
   - `compromise_signal` = False (every run)
2. If any baseline run deviates:
   - Flag as a control failure
   - Investigate root cause (LLM temperature, context overflow, model drift)
   - Document finding regardless of resolution
3. Compare baseline variance to injected-run variance:
   - Injected variance should be meaningfully higher than baseline variance
   - If not, the injection effect may be indistinguishable from noise

### Output

- `results/validation/baseline_stability.csv` — baseline-only runs with all three metrics
- Control analysis documented in `results/validation/validation_summary.md`

---

## J. Limitations

The following limitations apply to the experimental design and must be documented in
both the validation summary and the poster:

1. **Single model configuration** — All experiments use Ollama llama3.1:8b (4-bit quant)
   or Groq llama3-8b-8192. Results may not generalize to other LLMs (GPT-4, Claude,
   Mistral, etc.).

2. **Limited adversarial variants** — Only body-text injection with a single artifact
   string (`INJECTION_CONFIRMED`). Markup injection, whitespace injection, and Unicode
   injection are out of scope (documented in v2 roadmap, template Section 11).

3. **Paraphrase evasion** — `compromise_signal` Stage 1 relies on literal string matching.
   If the LLM paraphrases the injection instruction, Stage 1 misses it. Stage 2
   (integrity_score divergence) partially mitigates this but may not capture all subtle
   influence. This was observed in Linear Chain runs during Week 3.

4. **LLM non-determinism** — Even with identical inputs, LLM outputs may vary across runs
   due to sampling temperature, batching, and hardware differences. Multi-run validation
   quantifies this variance but cannot eliminate it as a confound.

5. **Observed patterns, not universal guarantees** — Results demonstrate behavior under
   controlled conditions with a specific corpus and model. They are not proof of universal
   vulnerability across all agentic systems, corpus sizes, or deployment configurations.

---

## K. Success Criteria

All of the following must be true for Week 4 to be marked COMPLETE:

1. Multi-run validation: ≥ 3 runs per configuration, results aggregated in CSV
2. Baseline stability confirmed: all baseline runs produce `propagation_depth=0`
3. Reproducibility documented in `results/validation/validation_summary.md`
4. Limitations documented (all 5 items)
5. `poster/poster_final.pdf` exists at 36" × 48", 300 DPI
6. Every number on the poster matches source CSVs
7. Poster PDF submitted to UTRGV Library print queue by Day 26
8. `rehearsal/walkthrough_notes.md` and `rehearsal/qa_responses.md` exist
9. Two timed rehearsals completed, both under 5 minutes
10. Presenter can deliver a 4–5 minute explanation including validation findings

---

## L. Validation / Evidence

| Check | How to verify |
|---|---|
| Multi-run CSV exists | `results/validation/multi_run_results.csv` present, ≥ 27 rows |
| Baseline stability | `results/validation/baseline_stability.csv` — all rows show depth=0 |
| Validation summary | `results/validation/validation_summary.md` — reproducibility + control + limitations |
| Poster PDF exists | `poster/poster_final.pdf` present, file size > 1 MB |
| Print resolution | Open PDF at 100% zoom; no pixelation on charts or text |
| Data accuracy | Diff every number on poster against source CSVs — zero mismatches |
| Library submission | Screenshot or confirmation email from UTRGV Library print queue |
| Walkthrough script | `rehearsal/walkthrough_notes.md` covers all poster sections |
| Q&A prep | `rehearsal/qa_responses.md` contains ≥ 3 question-answer pairs |
| Timed rehearsal | Self-timed or recorded; both runs ≤ 5 minutes |

---

## M. Risks / Edge Cases

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Multi-run validation reveals high variance | Medium | High — weakens claims | Report variance honestly; adjust poster claims to reflect uncertainty |
| Baseline instability detected | Low | High — undermines control | Investigate root cause; document as finding; reduce claims if unresolved |
| Poster design takes longer than 2 days | Medium | High — delays print submission | Simplify to single-column layout; readability over aesthetics |
| Library print queue has multi-day turnaround | Medium | High — poster not ready for April 24 | Submit by Day 26 at latest; confirm turnaround before submitting |
| Chart resolution too low at poster scale | Low | Medium — pixelated figures | Re-export from notebook_04 at higher DPI if needed |
| Numbers on poster don't match taxonomy.csv | Low | High — invalidates presentation | Run explicit diff check before exporting final PDF |
| Presenter cannot cover all sections in 5 minutes | Medium | Medium — rushed walkthrough | Cut Experiment Protocol detail if over time; anchor on taxonomy table |
| LLM availability during validation runs | Medium | Medium — blocks validation | Use Groq fallback if Ollama unavailable; document which backend was used |

**Slip recovery (from timeline):**
- If Week 4 slips: simplify poster layout to single-column format; readability over aesthetics
- Hard deadline: do not miss the library print submission; a simple readable poster printed on time is better than a polished poster that misses printing

---

## N. Week 4 Completion Gate

```python
from pathlib import Path
import csv

POSTER_DIR     = Path("poster")
REHEARSAL_DIR  = Path("rehearsal")
RESULTS_DIR    = Path("results")
VALIDATION_DIR = RESULTS_DIR / "validation"

all_pass = True

# 1. Multi-run validation CSV
multi_run = VALIDATION_DIR / "multi_run_results.csv"
if multi_run.exists():
    with open(multi_run) as f:
        rows = list(csv.DictReader(f))
    status = "PASS" if len(rows) >= 27 else "FAIL"
    if status == "FAIL": all_pass = False
    print(f"{status} multi_run_results.csv: {len(rows)} rows (minimum 27)")
else:
    print("FAIL multi_run_results.csv: not found")
    all_pass = False

# 2. Baseline stability CSV
baseline = VALIDATION_DIR / "baseline_stability.csv"
if baseline.exists():
    with open(baseline) as f:
        rows = list(csv.DictReader(f))
    bad = [r for r in rows if r.get("propagation_depth", "0") != "0"]
    status = "PASS" if not bad else "FAIL"
    if status == "FAIL": all_pass = False
    print(f"{status} baseline_stability.csv: {len(rows)} rows, {len(bad)} deviations")
else:
    print("FAIL baseline_stability.csv: not found")
    all_pass = False

# 3. Validation summary
summary = VALIDATION_DIR / "validation_summary.md"
if summary.exists() and summary.stat().st_size > 500:
    print(f"PASS validation_summary.md: {summary.stat().st_size} bytes")
else:
    print("FAIL validation_summary.md: missing or too small")
    all_pass = False

# 4. Poster PDF
poster_pdf = POSTER_DIR / "poster_final.pdf"
if poster_pdf.exists() and poster_pdf.stat().st_size > 1_000_000:
    print(f"PASS poster_final.pdf: {poster_pdf.stat().st_size // 1024} KB")
else:
    print(f"FAIL poster_final.pdf: {'not found' if not poster_pdf.exists() else 'too small'}")
    all_pass = False

# 5. Taxonomy CSV still intact
taxonomy = RESULTS_DIR / "taxonomy.csv"
if taxonomy.exists():
    with open(taxonomy) as f:
        rows = list(csv.DictReader(f))
    if len(rows) == 3:
        print(f"PASS taxonomy.csv: {len(rows)} rows (source of truth intact)")
    else:
        print(f"FAIL taxonomy.csv: expected 3 rows, found {len(rows)}")
        all_pass = False
else:
    print("FAIL taxonomy.csv: not found")
    all_pass = False

# 6. Walkthrough notes
walkthrough = REHEARSAL_DIR / "walkthrough_notes.md"
if walkthrough.exists() and walkthrough.stat().st_size > 100:
    print(f"PASS walkthrough_notes.md: {walkthrough.stat().st_size} bytes")
else:
    print("FAIL walkthrough_notes.md: missing or empty")
    all_pass = False

# 7. Q&A responses
qa = REHEARSAL_DIR / "qa_responses.md"
if qa.exists() and qa.stat().st_size > 100:
    print(f"PASS qa_responses.md: {qa.stat().st_size} bytes")
else:
    print("FAIL qa_responses.md: missing or empty")
    all_pass = False

# 8. Charts still present
charts = list((RESULTS_DIR / "charts").glob("*.png"))
status = "PASS" if len(charts) >= 2 else "FAIL"
if status == "FAIL": all_pass = False
print(f"{status} Charts: {len(charts)} PNG files (poster source images)")

print(f"\nWEEK 4 GATE: {'PASS' if all_pass else 'FAIL'}")
print("Note: library print submission and timed rehearsals must be verified manually")
```

---

## O. Week 4 Completion Checklist

- [ ] Multi-run validation: ≥ 3 runs per configuration (9 configs × 3 = 27 minimum)
- [ ] `results/validation/multi_run_results.csv` with mean, std, min, max per config
- [ ] `results/validation/baseline_stability.csv` — all baselines show depth=0
- [ ] `results/validation/validation_summary.md` — reproducibility + control + limitations
- [ ] All 5 limitations documented
- [ ] Poster source file created (`poster/poster_source.*`)
- [ ] Poster contains all sections (Title, Motivation, Architecture, Protocol, Taxonomy, Findings, Validation Summary, Limitations, Implications, Acknowledgements)
- [ ] Taxonomy table on poster matches `results/taxonomy.csv` exactly
- [ ] All charts at 300 DPI, readable at poster scale
- [ ] `poster/poster_final.pdf` exported (36" × 48" portrait, 300 DPI)
- [ ] Poster PDF submitted to UTRGV Library print queue by Day 26
- [ ] `rehearsal/walkthrough_notes.md` created with structured 4–5 min script
- [ ] `rehearsal/qa_responses.md` created with ≥ 3 Q&A pairs
- [ ] Two timed rehearsals completed, both ≤ 5 minutes
- [ ] Final accuracy check: no empirical claims exceed experiment data
- [ ] End-to-end completion gate: `WEEK 4 GATE: PASS`
- [ ] Overall Week 4 status: COMPLETE

---

## Immediate Next Action

Execute multi-run validation (Step 1): re-run each pipeline configuration 3–5 times,
compute aggregated metrics, and produce `results/validation/multi_run_results.csv`.
Do not begin poster design until validation is complete and documented.
