# ADR-001: Use Three Pipeline Topologies (RAG, Linear Chain, Parallel)

**Date:** 2026-03-27
**Status:** Accepted
**Author:** BUDDY26

---

## Context

The research question is whether indirect prompt injection propagates differently across structurally distinct agentic pipeline architectures. To answer this, the experiment framework needs to cover topologies that differ in how context flows between agents — specifically, how many agents see retrieved content, whether agent outputs are chained sequentially or combined in parallel, and how many hops an injected payload must traverse before appearing in final output.

Three candidate topology classes were identified as representative of patterns common in production agentic systems: retrieval-augmented generation (RAG), sequential multi-agent chains, and parallel fan-out with aggregation. These three patterns produce meaningfully different propagation paths and depth profiles, making them suitable for comparative injection analysis.

The research also required that all topologies share a common corpus, retrieval mechanism, LLM backend, and injection protocol so that topology structure — not implementation variation — is the independent variable under study.

---

## Decision

Implement exactly three pipeline topologies:

1. **RAG (Retrieval-Augmented Generation):** A single agent receives FAISS-retrieved documents as context and generates a response. Injection occurs if an adversarial document is retrieved and influences the output.

2. **Linear Chain:** Three sequential agents where the output of each agent becomes the input context for the next. Injection propagates forward through the chain; propagation depth reflects how many agents downstream of the first are influenced.

3. **Parallel Fan-Out:** Two independent agents each receive retrieved context simultaneously, and their outputs are concatenated and passed to a single aggregator agent. Injection can influence both parallel branches and the aggregator, yielding the highest possible propagation depth in this framework.

All three topologies use the same FAISS index, corpus, test query, LLM client, structured logger, and injection rank configurations (baseline, rank-1, rank-3).

---

## Rationale

These three topologies were chosen because they represent structurally distinct propagation graphs. RAG has depth 0–1 (single agent, no downstream chain). Linear Chain has depth up to 3 (full chain traversal). Parallel has depth up to 4 (both branches plus aggregator). This spread enables the key research finding: propagation depth is topology-determined, not stochastic, and structural architecture is the primary risk variable.

A single topology would not support comparative analysis. More than three topologies within the project scope would exceed the available timeline without adding qualitatively distinct propagation structures.

---

## Alternatives Considered

| Alternative | Reason Rejected |
|-------------|----------------|
| Single topology (RAG only) | Does not support cross-topology comparison; cannot isolate structural effects |
| Four or more topologies (e.g., adding a tree or hierarchical topology) | Would exceed Week 2 implementation timeline; the three chosen topologies already capture the key structural variation (depth 0–1, full chain, parallel fan-out) |
| Tool-use or function-calling topology | Outside scope of current research; introduces additional variables (tool routing, output parsing) that are not controlled for in the current framework |
| Separate LLM backends per topology | Would conflate model effects with topology effects; single shared LLM client required for experimental validity |

---

## Consequences

### Positive
- Three topologies provide sufficient structural variation to support comparative injection propagation analysis
- Shared infrastructure (corpus, index, LLM client, logger) keeps the topology structure as the isolated independent variable
- Propagation depth range (0–4) is wide enough to produce statistically distinct results across configurations
- Framework is extensible: a fourth topology can be added in a future study without breaking existing results

### Negative
- Results are limited to three topology types; generalization to other architectures (tree-based, event-driven, tool-using) requires additional research
- Linear Chain at depth 3 does not distinguish between injection that degrades at hop 2 versus hop 3; finer-grained per-hop logging would require per-agent output capture

### Risks
- If the LLM paraphrases the injected payload, Stage-1 compromise signal detection will under-count injection; Stage-2 integrity threshold partially compensates but may also miss subtle degradation
- Single model (llama3.1:8b) limits generalizability; topology-specific vulnerability patterns may not hold for other model sizes or families

---

## Review Trigger

This decision should be revisited if: (1) a future study adds a fourth topology type, (2) the research question is extended to tool-using or event-driven pipelines, or (3) the metrics module is extended to support per-hop propagation tracking requiring topology changes.
