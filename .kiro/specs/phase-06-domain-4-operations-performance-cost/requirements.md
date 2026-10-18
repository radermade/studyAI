# Requirements Document

## Introduction

**Title:** Phase 6 — Domain 4 Operations, Performance, and Cost

**Status:** Proposed

**Scope:** Deliver complete, source-grounded mastery for AIP-4.1 through AIP-4.3, Lab 9, Lab 10, and the evidence needed to operate and optimize GenAI applications against explicit quality, safety, latency, throughput, availability, privacy, and cost objectives.

## Upstream dependencies

- Phase 0 objective manifest, source registry, learner profile, Region allowlist, lab budget, and AWS safety policy.
- Phase 1 durable SQLite study state, transactional attempts/reviews, source search, sessions, typed MCP contracts, and answer-key separation.
- Phase 2 Learn, Grill, Labs, Review, Knowledge, and Progress workflows; durable lab checkpoints; explicit evidence states.
- Phase 3 model, prompt, RAG, and retrieval artifacts, especially Labs 1, 3, and 4.
- Phase 4 agent, streaming/API, deployment, and enterprise integration artifacts, especially Labs 6 and 7.
- Phase 5 guardrails, privacy, governance, and tenant-isolation controls, especially Labs 5 and 8.

Implementation MUST block affected work when a predecessor contract is absent; this specification does not assert that upstream artifacts already exist.

## Out of scope

- Automated creation, update, or deletion of AWS resources.
- A hosted telemetry platform, queue, vector database, or separate API server.
- Optimization that weakens a safety, privacy, correctness, groundedness, or tenant-isolation control.
- Claims that internal mastery or benchmark results predict an AWS examination score.

## Glossary

- **Floor:** A predeclared minimum acceptable quality, safety, privacy, or reliability result.
- **Fresh scenario:** An independently reviewed item not previously exposed to the learner or through a materially equivalent variant.
- **Verified:** A checkpoint backed by committed successful validator evidence.

## Requirements

### P6-R1 — Source-grounded Domain 4 curriculum and question bank

**User story:** As a learner, I want complete and current Domain 4 material so that every operational decision can be traced to the exam blueprint and primary evidence.

#### Acceptance criteria

1. WHEN Phase 6 content is ingested, THE SYSTEM SHALL require exact objective IDs from `AIP-4.1`, `AIP-4.2`, and `AIP-4.3`, source URL, title, publisher, retrieval date, freshness status, trade-offs, failure modes, and verification method.
2. THE SYSTEM SHALL provide concept, scenario, troubleshooting, and hands-on evidence for each of `AIP-4.1`, `AIP-4.2`, and `AIP-4.3`.
3. WHEN a graded question is admitted, THE SYSTEM SHALL require difficulty, format, meaningful scenario constraints, source references, separate answer/rubric, rationales for every option, review status, and independent review.
4. IF a source is stale, missing, non-primary without justification, or conflicts with the locked blueprint, THEN THE SYSTEM SHALL exclude affected material from readiness scoring and expose the failure.
5. THE SYSTEM SHALL structurally prevent unanswered question payloads from carrying answer keys or grading rubrics.

### P6-R2 — Quality-latency-cost baseline and floors

**User story:** As a learner, I want a repeatable baseline and explicit guardrails so that an apparent optimization is not accepted by sacrificing required behavior.

#### Acceptance criteria

1. BEFORE an optimization experiment starts, THE SYSTEM SHALL persist a versioned baseline containing workload ID, dataset version, configuration, Region, timestamp, sample size, warm-up policy, input/output token counts, latency distribution including p50 and p95, throughput, error rate, availability observation, cost estimate with assumptions, and quality and safety metrics.
2. WHEN an experiment is defined, THE SYSTEM SHALL require explicit numeric quality and safety floors, privacy constraints, cost ceiling or target, and the metric selected for improvement.
3. IF any candidate falls below a declared quality or safety floor, violates privacy or tenant isolation, or exceeds an enforced budget limit, THEN THE SYSTEM SHALL reject it regardless of latency or cost improvement.
4. WHEN benchmark conditions differ from baseline conditions, THE SYSTEM SHALL mark the comparison non-equivalent and prevent an improvement claim until normalized or rerun.
5. THE SYSTEM SHALL label costs as measured or estimated, record pricing date and assumptions, and avoid presenting estimates as billing records.

### P6-R3 — Evidence-first bottleneck diagnosis

**User story:** As an operator, I want to identify the actual bottleneck before changing the system so that remediation is narrow, testable, and justified.

#### Acceptance criteria

1. WHEN a performance or reliability incident is investigated, THE SYSTEM SHALL require a symptom, affected objective/SLO, bounded time window, correlation identifier, evidence from relevant spans or metrics, competing hypotheses, and an identified bottleneck before recommending remediation.
2. THE SYSTEM SHALL distinguish model, token/context, retrieval/index, network/service, queue/concurrency, tool/agent, application, quota/throttle, and data-quality bottleneck classes.
3. IF evidence is insufficient or contradictory, THEN THE SYSTEM SHALL record the diagnosis as uncertain and request the next discriminating measurement rather than assert a root cause.
4. WHEN remediation is tested, THE SYSTEM SHALL compare it with the saved baseline under equivalent conditions and record regressions, limitations, and rollback criteria.
5. THE SYSTEM SHALL reject random parameter or prompt changes that lack a hypothesis and measurable acceptance condition from independent lab proof.

### P6-R4 — Privacy-safe observability and incident response (Lab 9)

**User story:** As a learner, I want realistic observability and incident practice without exposing sensitive content so that I can diagnose GenAI systems responsibly.

#### Acceptance criteria

1. THE SYSTEM SHALL deliver Lab 9 with exact mappings `AIP-2.5`, `AIP-4.3`, and `AIP-5.2` and required proof consisting of a dashboard, alert, and trace-led diagnosis.
2. Lab 9 SHALL include prerequisites, objectives, architecture, estimated cost class, Region assumptions, steps, prediction prompts, progressive hints, read-only validation, failure injection, reflection, cleanup, and delayed recall.
3. WHEN telemetry is collected, THE SYSTEM SHALL record operational, model, retrieval, tool/agent, quality, business, safety, cost, and freshness signals using non-sensitive identifiers and bounded retention.
4. THE SYSTEM SHALL redact credentials, tokens, request signatures, PII, full private prompts, answer keys, and sensitive retrieved content from logs, traces, dashboards, and exported evidence.
5. WHEN an alert is exercised, THE SYSTEM SHALL preserve evidence linking the alert to a trace and an evidence-based diagnosis; IF a dependency is unavailable, THEN THE SYSTEM SHALL distinguish unavailable, authorization, validation, throttling, and internal failures.
6. THE SYSTEM SHALL NOT mark a checkpoint `Verified` before successful allowlisted read-only validation commits its evidence, and SHALL NOT mark `Cleaned up` before absence or terminal deletion state is verified.

### P6-R5 — Cost and performance optimization (Lab 10)

**User story:** As a learner, I want to test multiple optimization levers so that I can choose the best quality-latency-cost trade-off for a constrained workload.

#### Acceptance criteria

1. THE SYSTEM SHALL deliver Lab 10 with exact mappings `AIP-1.2`, `AIP-2.2`, `AIP-2.4`, `AIP-4.1`, and `AIP-4.2` and required proof consisting of a before/after benchmark that preserves the declared quality and safety threshold.
2. Lab 10 SHALL include controlled experiments for input/output token reduction, model selection/routing, cache strategy and invalidation, streaming, batching or concurrency, throughput/capacity, and retrieval/index/query/reranking optimization.
3. WHEN caching is evaluated, THE SYSTEM SHALL require cache key scope, tenant/privacy boundary, TTL, invalidation triggers, stale-response behavior, and evidence that cross-user or cross-tenant disclosure cannot occur.
4. WHEN routing or smaller models are evaluated, THE SYSTEM SHALL measure quality by workload segment and define fallback, circuit-breaker, and graceful-degradation behavior.
5. WHEN throughput is evaluated, THE SYSTEM SHALL record concurrency, token throughput, throttling, retry/backoff, utilization, and saturation evidence without unbounded load or spend.
6. Lab 10 SHALL include prerequisites, architecture, cost class, Region assumptions, prediction prompts, read-only validation, failure injection, reflection, cleanup, and delayed recall.

### P6-R6 — Durable evidence and progress reporting

**User story:** As a learner, I want trustworthy evidence and progress so that I can distinguish completion, independent skill, and unresolved risk.

#### Acceptance criteria

1. WHEN a benchmark, diagnosis, lab checkpoint, or delayed recall result is recorded, THE SYSTEM SHALL persist it transactionally in SQLite with a stable ID, UTC timestamp, provenance, configuration/version links, and idempotent event/request ID where practical.
2. THE SYSTEM SHALL expose `Not started`, `In progress`, `Self-reported`, `Verified`, `Failed`, and `Cleaned up` as distinct lab states and SHALL NOT infer verification from a click or truthy value.
3. THE SYSTEM SHALL distinguish independent completion from hint-assisted completion and record progressive hint usage.
4. THE SYSTEM SHALL present Domain 4 accuracy, delayed recall, confidence calibration, lab proof, cleanup state, benchmark floors, and unresolved evidence gaps without reducing readiness to an opaque score.
5. IF persistence fails, THEN THE SYSTEM SHALL show a recoverable error and SHALL NOT report success.

### P6-R7 — AWS safety, authorization, and cost containment

**User story:** As a learner using an AWS account, I want bounded read-only validation and visible cost controls so that study activity cannot silently create operational or financial risk.

#### Acceptance criteria

1. WHEN AWS validation is requested, THE SYSTEM SHALL use boto3 through a named profile or standard credential chain with explicit Region and service/action allowlist.
2. THE SYSTEM SHALL permit only documented read-only `Describe`, `Get`, and `List` validation operations in this phase and SHALL NOT expose raw SQL, shell, filesystem, Python evaluation, or AWS CLI access.
3. BEFORE a lab begins, THE SYSTEM SHALL confirm prerequisites, allowed Region, expected cost class, budget warning, resource-tag expectations, and cleanup procedure.
4. IF authorization, Region, budget, dependency, or validation preconditions fail, THEN THE SYSTEM SHALL block the affected check, preserve prior state, and provide a non-sensitive recovery action.
5. THE SYSTEM SHALL NOT store AWS credentials, secrets, sensitive prompts, or private AWS payloads in source, Markdown, MCP JSON, SQLite, or example environment files.

### P6-R8 — Phase 6 exit gate and handoff

**User story:** As the program owner, I want an objective completion gate so that Phase 7 starts only with reliable operations evidence.

#### Acceptance criteria

1. WHEN Phase 6 completion is evaluated, THE SYSTEM SHALL require accepted source and question coverage for every task `AIP-4.1` through `AIP-4.3`.
2. THE SYSTEM SHALL require completed Lab 9 proof: dashboard, alert, trace-led diagnosis, required reflections/delayed recall, and verified cleanup where resources were used.
3. THE SYSTEM SHALL require completed Lab 10 proof: equivalent before/after benchmark, optimization decision record, explicit quality and safety floors, and verified cleanup where resources were used.
4. THE SYSTEM SHALL require evidence that no accepted optimization lowered quality or safety below its explicit threshold.
5. THE SYSTEM SHALL require the learner to identify a bottleneck from evidence before selecting a remedy in an independently assessed scenario.
6. THE SYSTEM SHALL require at least 80% accuracy on a fresh, independently reviewed Domain 4 scenario set after delayed review; reused or previously exposed questions SHALL NOT satisfy this gate.
7. IF any gate fails, THEN THE SYSTEM SHALL keep Phase 6 incomplete and produce a weakness-directed remediation list.
8. WHEN all gates pass, THE SYSTEM SHALL emit a versioned Phase 7 handoff containing coverage, baselines, lab evidence references, unresolved low-priority risks, source freshness, and validation results.
