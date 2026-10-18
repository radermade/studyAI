# Requirements Document

## Introduction

**Title:** Phase 3 — Domain 1 Foundations, RAG, and Prompts  
**Status:** Proposed  
**Scope:** Deliver source-grounded learning, scored practice, and Labs 1–4 for AIP-C01 Domain 1 (`AIP-1.1`–`AIP-1.6`), with durable evidence and an enforceable mastery exit gate.

## Upstream dependencies

Phase 3 implementation SHALL begin only after these roadmap Phase 0–2 contracts exist and their exit gates pass:

- Phase 0: objective manifest containing `AIP-1.1`–`AIP-1.6`, source registry and freshness policy, learner profile, diagnostic record, and AWS lab-safety policy with profile, Region, budget, tagging, and cleanup controls.
- Phase 1: Python/uv project, versioned SQLite store, objective/content/question/session/attempt/misconception/review repositories, FTS5 source search, deterministic scheduling/grading, and typed study MCP operations.
- Phase 2: Streamlit Learn, Grill, Labs, Review, Knowledge, and Progress workflows; durable lab runs; the six-state checkpoint model; hint recording; read-only AWS validation boundary; and accessible evidence/status presentation.
- The roadmap and steering documents remain authoritative where an upstream implementation detail is unresolved. Phase 3 SHALL fail its prerequisite check rather than silently create incompatible replacement contracts.

## Out of scope

- Replacing local SQLite FTS5 with embeddings or a local/hosted vector database. AWS vector technologies are studied inside learner-operated labs only.
- A hosted application API, frontend framework, queue, container platform, local LLM, or async wrapper around blocking platform code.
- Platform-managed creation, update, or deletion of AWS resources. Learners perform documented Console/SDK lab actions; platform validators remain explicitly allowlisted and read-only.
- Production operation of Labs 9–12, completion of Domains 2–5, or claiming AWS exam readiness from Phase 3 alone.
- Copying proprietary course text, screenshots, assets, branding, questions, or trade dress.

## Requirements

### P3-R1 — Domain 1 source and coverage integrity

**User story:** As a learner, I want every Domain 1 topic grounded in current primary sources so that I study the official scope and can distinguish facts from recommendations.

#### Acceptance criteria

1. **P3-R1.1:** WHEN Domain 1 content is ingested, THE SYSTEM SHALL reject any item that lacks a stable content ID, one or more valid IDs from `AIP-1.1`–`AIP-1.6`, source URL, source title, publisher, retrieval date, and freshness status.
2. **P3-R1.2:** WHEN an item is accepted, THE SYSTEM SHALL preserve separately labeled AWS-documented facts, project recommendations, and learner notes, plus trade-offs, failure modes, and a verification method.
3. **P3-R1.3:** WHEN coverage is calculated, THE SYSTEM SHALL report concept, scenario, troubleshooting, and hands-on evidence independently for each of the six objectives and SHALL identify every missing form.
4. **P3-R1.4:** IF a source is stale, superseded, unreachable, or conflicts with another primary source, THEN THE SYSTEM SHALL mark affected material non-current, exclude it from new scored publication, and present the review reason without deleting lineage.
5. **P3-R1.5:** WHEN Phase 3 is offered offline, THE SYSTEM SHALL serve the last approved local material and visibly identify freshness and unavailable external verification.

### P3-R2 — Foundations, architecture, and model-selection learning

**User story:** As a learner, I want realistic architecture and model-selection work so that I can reason from business constraints rather than memorize service names.

#### Acceptance criteria

1. **P3-R2.1:** WHEN the learner studies `AIP-1.1`, THE SYSTEM SHALL provide sourced concept, scenario, troubleshooting, and hands-on material covering business outcomes, risk, latency, scale, data, Region, cost, proof-of-concept evaluation, Well-Architected guidance, and the Generative AI Lens.
2. **P3-R2.2:** WHEN the learner studies `AIP-1.2`, THE SYSTEM SHALL require comparisons across capability, modality, context, quality, responsibility, latency, throughput, availability, customization, and cost.
3. **P3-R2.3:** WHEN an architecture scenario is graded, THE SYSTEM SHALL require a material constraint, a defensible Bedrock-versus-SageMaker or deployment choice, and reasoning about decoupling, fallback, circuit breaking, cross-Region inference, graceful degradation, versioning, rollback, and retirement where applicable.
4. **P3-R2.4:** WHEN customization is assessed, THE SYSTEM SHALL distinguish prompting, retrieval augmentation, fine-tuning, LoRA/adapters, and no-customization choices by evidence, operational burden, reversibility, and risk.
5. **P3-R2.5:** IF a learner selects a service or model without addressing decisive constraints, THEN THE SYSTEM SHALL record the missing concept and schedule targeted review rather than award full credit.

### P3-R3 — Data preparation, vector architecture, and retrieval learning

**User story:** As a learner, I want to design and troubleshoot FM data and retrieval systems so that I can explain quality, freshness, isolation, relevance, latency, and cost trade-offs.

#### Acceptance criteria

1. **P3-R3.1:** WHEN the learner studies `AIP-1.3`, THE SYSTEM SHALL cover text, image, audio, and tabular validation and processing; model-specific request formatting; data quality; normalization; enrichment; classification; extraction; monitoring; and malformed-input diagnosis.
2. **P3-R3.2:** WHEN the learner studies `AIP-1.4`, THE SYSTEM SHALL compare Bedrock Knowledge Bases, OpenSearch Service, Aurora PostgreSQL/pgvector, and supported metadata/vector patterns, including metadata, tenancy, authorization, lifecycle, sharding, indexing, hierarchy, synchronization, update, and deletion decisions.
3. **P3-R3.3:** WHEN the learner studies `AIP-1.5`, THE SYSTEM SHALL cover fixed, semantic, recursive, and hierarchical chunking; embedding selection/dimensions; keyword, semantic, hybrid, filtered, and reranked retrieval; query transformation; and stable API/function/MCP exposure.
4. **P3-R3.4:** WHEN a retrieval experiment is recorded, THE SYSTEM SHALL store the dataset/version, configuration, relevance measure, latency measure, source freshness result, tenant-filter result where applicable, and learner conclusion.
5. **P3-R3.5:** IF citations are missing, stale content is retrieved, tenant filtering fails, or measured relevance/latency is invalid, THEN THE SYSTEM SHALL mark the checkpoint failed and retain diagnostic evidence.
6. **P3-R3.6:** WHEN local study-material search is used, THE SYSTEM SHALL continue to use SQLite FTS5 plus metadata filters; Domain 1 instruction SHALL NOT implicitly authorize a platform vector database.

### P3-R4 — Prompt engineering and governance learning

**User story:** As a learner, I want a governed prompt lifecycle with regression evidence so that I can improve prompts without introducing silent quality or safety regressions.

#### Acceptance criteria

1. **P3-R4.1:** WHEN the learner studies `AIP-1.6`, THE SYSTEM SHALL cover roles, instructions, examples, variables, output schemas, constraints, guardrails, context, clarification, intent, and conversation state.
2. **P3-R4.2:** WHEN a prompt version is recorded, THE SYSTEM SHALL capture a stable prompt ID, immutable version, objective IDs, source lineage, owner, review state, change rationale, test-set version, and predecessor or rollback target.
3. **P3-R4.3:** WHEN a prompt candidate is evaluated, THE SYSTEM SHALL validate structured output and compare named edge cases and regression metrics against an approved baseline before approval.
4. **P3-R4.4:** IF schema checks or an approved quality/safety threshold fails, THEN THE SYSTEM SHALL reject promotion, preserve results, and identify the failing cases.
5. **P3-R4.5:** WHEN chained or conditional workflows are taught, THE SYSTEM SHALL expose bounded inputs/outputs, reusable preprocessing/postprocessing, failure handling, and audit points without treating hidden model reasoning as a contract.

### P3-R5 — Scored question quality and review

**User story:** As a learner, I want original, reviewed questions with useful feedback so that readiness measurements are trustworthy.

#### Acceptance criteria

1. **P3-R5.1:** WHEN a Domain 1 question is ingested, THE SYSTEM SHALL require stable question ID, objective IDs, difficulty, format, material scenario constraint, source references, separate answer/rubric, option or criterion rationales, and review state.
2. **P3-R5.2:** WHEN an unanswered question is delivered, THE SYSTEM SHALL return a payload structurally incapable of carrying answer keys, rubrics, correctness flags, or hidden mock feedback.
3. **P3-R5.3:** IF a question lacks independent review, current source approval, or explanation for each option/criterion, THEN THE SYSTEM SHALL exclude it from readiness scoring.
4. **P3-R5.4:** WHEN an answer is graded, THE SYSTEM SHALL atomically persist the attempt, confidence, elapsed time, misconception updates, and review reschedule before showing recorded success.
5. **P3-R5.5:** WHEN feedback is permitted, THE SYSTEM SHALL show result, decisive requirement, correct trade-off reasoning, why alternatives fail, primary source, and a targeted follow-up.
6. **P3-R5.6:** WHEN coverage is reported, THE SYSTEM SHALL distinguish reviewed scored questions from drafts and SHALL show fresh-question availability for each Domain 1 objective.

### P3-R6 — Labs 1–4 execution, proof, and safety

**User story:** As a learner, I want guided, evidence-based AWS labs so that I gain hands-on skill without confusing clicks or self-reports with verification.

#### Acceptance criteria

1. **P3-R6.1:** WHEN any Phase 3 lab is published, THE SYSTEM SHALL require prerequisites, learning objectives, Mermaid architecture, cost class, Region assumptions, learner-operated steps, prediction prompts, allowlisted validation, failure injection, reflection, cleanup, and delayed recall.
2. **P3-R6.2:** WHEN Lab 1 runs, THE SYSTEM SHALL map it to `AIP-1.1`, `AIP-1.2`, `AIP-2.2`, and `AIP-4.1` and require recorded quality/latency/cost comparison plus selection rationale.
3. **P3-R6.3:** WHEN Lab 2 runs, THE SYSTEM SHALL map it to `AIP-1.6`, `AIP-5.1`, and `AIP-5.2` and require a versioned prompt, schema checks, and regression result.
4. **P3-R6.4:** WHEN Lab 3 runs, THE SYSTEM SHALL map it to `AIP-1.3`, `AIP-1.4`, and `AIP-1.5` and require ingestion, retrieval, citations, and freshness proof.
5. **P3-R6.5:** WHEN Lab 4 runs, THE SYSTEM SHALL map it to `AIP-1.4`, `AIP-1.5`, `AIP-4.2`, `AIP-5.1`, and `AIP-5.2` and require a measured chunk/search/rerank comparison.
6. **P3-R6.6:** BEFORE a lab can start, THE SYSTEM SHALL validate the dedicated AWS profile or standard credential chain, Region allowlist, prerequisites, budget/cost acknowledgment, required ownership/session tags, and cleanup plan without storing credentials.
7. **P3-R6.7:** WHEN a checkpoint is evaluated, THE SYSTEM SHALL use only `Not started`, `In progress`, `Self-reported`, `Verified`, `Failed`, or `Cleaned up`; `Verified` SHALL require committed validator evidence and `Cleaned up` SHALL require verified absence or terminal deletion state.
8. **P3-R6.8:** IF AWS is unavailable, authorization fails, cost consent is absent, or validation is inconclusive, THEN THE SYSTEM SHALL distinguish that failure, preserve progress safely, and SHALL NOT claim verification or cleanup.
9. **P3-R6.9:** WHEN hint level 4 is used, THE SYSTEM SHALL mark completion assisted until the learner later demonstrates the objective unaided.

### P3-R7 — Evidence, mastery, and delayed assessment

**User story:** As a learner, I want transparent Domain 1 mastery evidence so that I know whether I can recall and apply the material independently.

#### Acceptance criteria

1. **P3-R7.1:** WHEN evidence is recorded, THE SYSTEM SHALL link its stable ID to learner, objective IDs, evidence type, source question/content/lab, attempt or lab run, timestamp in UTC, review state, hint assistance, and verification state.
2. **P3-R7.2:** WHEN delayed assessment is scheduled, THE SYSTEM SHALL use the upstream spaced-review contract and SHALL not classify an immediate repeat as delayed evidence.
3. **P3-R7.3:** WHEN fresh delayed accuracy is calculated, THE SYSTEM SHALL include only independently reviewed Domain 1 scenario questions not previously exposed to the learner, attempted in the configured delayed window, and SHALL report numerator, denominator, exclusions, and per-objective results.
4. **P3-R7.4:** WHEN the learner submits retrieval-failure and model-selection explanations, THE SYSTEM SHALL record rubric-based evidence and hint use; only attempts with no answer reveal or procedural/full-solution hint SHALL count as unaided.
5. **P3-R7.5:** IF evidence is insufficient, disputed, stale, or assisted, THEN THE SYSTEM SHALL expose that limitation and SHALL NOT infer mastery from completion percentage.
6. **P3-R7.6:** WHEN progress is shown, THE SYSTEM SHALL include accuracy, delayed recall, confidence calibration, misconceptions, lab proof and cleanup, source freshness, uncovered forms, and readiness risks.

### P3-R8 — Phase 3 exit gate and downstream handoff

**User story:** As a maintainer, I want an auditable exit decision and handoff so that later phases can reuse Domain 1 artifacts without overstating readiness.

#### Acceptance criteria

1. **P3-R8.1:** WHEN exit readiness is evaluated, THE SYSTEM SHALL require approved concept, scenario, troubleshooting, and hands-on evidence for each of `AIP-1.1`–`AIP-1.6`.
2. **P3-R8.2:** WHEN exit readiness is evaluated, THE SYSTEM SHALL require at least 80% fresh delayed Domain 1 scenario accuracy, with the calculation satisfying P3-R7.3.
3. **P3-R8.3:** WHEN exit readiness is evaluated, THE SYSTEM SHALL require passing unaided rubric evidence for both retrieval-failure diagnosis and model-selection trade-off explanation.
4. **P3-R8.4:** WHEN exit readiness is evaluated, THE SYSTEM SHALL require Labs 1–4 proof complete, required cleanup evidence committed, and no unresolved safety-critical or source-integrity failure.
5. **P3-R8.5:** IF any gate fails, THEN THE SYSTEM SHALL mark Phase 3 incomplete and produce objective-specific remediation and due-review actions.
6. **P3-R8.6:** WHEN all gates pass, THE SYSTEM SHALL emit a versioned handoff containing objective coverage, approved source/content/question versions, lab/evidence IDs, mastery calculations, open risks, schema/migration versions, and contracts needed by Phases 4, 6, 7, and 8.
## Glossary

- **Approved:** Current, source-validated, and reviewed for its intended publication role.
- **Delayed:** Attempted after the configured upstream spaced-review interval, not an immediate repeat.
- **Fresh:** Not previously exposed to the learner in question or answer form.
- **Hands-on evidence:** A durable learner action/result linked to an objective; verification state remains explicit.
- **Unaided:** Completed without answer reveal or procedural/full-solution hint.
