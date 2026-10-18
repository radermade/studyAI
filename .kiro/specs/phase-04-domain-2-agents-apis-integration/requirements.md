# Requirements Document

## Introduction

**Title:** Phase 4 — Domain 2 Agents, APIs, and Integration  
**Status:** Proposed  
**Scope:** Deliver source-grounded learning, reviewed scored practice, architecture exercises, and Labs 6–7 for AIP-C01 Domain 2 (`AIP-2.1`–`AIP-2.5`), with durable operational evidence and an enforceable mastery exit gate.

## Upstream dependencies

- Phase 0 exit gate: objective/source manifests, learner profile, diagnostic, and AWS lab-safety policy are valid for all Phase 4 objectives and services.
- Phase 1 exit gate: local-first SQLite core, typed models, deterministic grading/review/session services, FTS5, and narrow FastMCP study tools are available.
- Phase 2 exit gate: Learn/Grill/Labs/Review/Knowledge/Progress workflows, durable checkpoint/hint state, explicit evidence statuses, and accessible error states are available.
- Phase 3 handoff: approved model-selection, prompt, retrieval, experiment, evidence, source-review, and mastery contracts are versioned and reusable. Cross-domain evidence from Labs 1–4 is linked but does not replace Phase 4 coverage.
- If an upstream implementation is absent or incompatible, Phase 4 SHALL report the missing contract and block affected publication rather than creating an unreviewed parallel subsystem.

## Out of scope

- Expanding the platform MCP allowlist into a general agent tool surface, raw shell/filesystem/SQL/AWS access, or arbitrary caller-selected tools.
- Hosting a production API, queue, container workload, or model endpoint as part of the local study platform. These are architecture subjects and learner-operated AWS lab patterns.
- Broad AWS mutation by the platform, unattended autonomous agents, or production deployment authorization.
- Async wrappers around synchronous Streamlit/SQLite/boto3 platform code. Lab 7 teaches asynchronous AWS architecture through bounded lab resources and evidence.
- Completing Domains 1, 3, 4, or 5 solely from cross-domain Lab 6 evidence.

## Requirements

### P4-R1 — Domain 2 source and coverage integrity

**User story:** As a learner, I want complete, current Domain 2 material so that agent and integration patterns are grounded in primary sources rather than demos or hype.

#### Acceptance criteria

1. **P4-R1.1:** WHEN Phase 4 content is ingested, THE SYSTEM SHALL require a stable content ID, one or more IDs from `AIP-2.1`–`AIP-2.5`, and complete primary-source URL/title/publisher/retrieval-date/freshness metadata.
2. **P4-R1.2:** WHEN content is approved, THE SYSTEM SHALL preserve separately labeled AWS facts, project recommendations, and learner notes, plus trade-offs, failure modes, and verification methods.
3. **P4-R1.3:** WHEN coverage is audited, THE SYSTEM SHALL report approved concept, scenario, troubleshooting, and hands-on evidence for each Domain 2 objective and identify all missing forms.
4. **P4-R1.4:** IF a source is stale, superseded, unreachable, or conflicting, THEN THE SYSTEM SHALL preserve lineage, block new scored use, and create a review finding.
5. **P4-R1.5:** WHEN cached material is used offline, THE SYSTEM SHALL identify its freshness and any unavailable AWS verification.

### P4-R2 — Bounded agents and tool integration

**User story:** As a learner, I want to build and diagnose bounded agents so that I can use tools safely without treating model output or hidden reasoning as authority.

#### Acceptance criteria

1. **P4-R2.1:** WHEN the learner studies `AIP-2.1`, THE SYSTEM SHALL cover memory, state, sessions, tool selection, single/multi-agent boundaries, specialized-model coordination, structured orchestration patterns, and observable outputs without requiring hidden chain-of-thought.
2. **P4-R2.2:** WHEN an agent design is assessed, THE SYSTEM SHALL require explicit tool schemas, parameter validation, allowlists, least-privilege identity, stopping conditions, step/cost/time limits, timeout, circuit breaker, retry policy, idempotency where applicable, trace correlation, and safe failure behavior.
3. **P4-R2.3:** WHEN an action has material cost, privilege, irreversibility, ambiguity, or low confidence, THE SYSTEM SHALL require an explicit human approval, review, or escalation decision in the design.
4. **P4-R2.4:** IF a tool call is malformed, unauthorized, unavailable, repeated unsafely, or outside policy, THEN THE SYSTEM SHALL require rejection or bounded failure and SHALL preserve sanitized diagnostic evidence.
5. **P4-R2.5:** WHEN MCP is taught, THE SYSTEM SHALL distinguish a bounded lab MCP/tool contract from the platform’s stable study-tool allowlist and SHALL NOT expose raw database, filesystem, Python evaluation, AWS CLI, or shell operations.

### P4-R3 — Model deployment and capacity decisions

**User story:** As a learner, I want to choose deployment patterns from workload evidence so that I can balance quality, capacity, latency, and cost.

#### Acceptance criteria

1. **P4-R3.1:** WHEN the learner studies `AIP-2.2`, THE SYSTEM SHALL compare on-demand invocation, provisioned throughput, batch/asynchronous patterns, and SageMaker endpoints against traffic shape, latency, throughput, availability, customization, operational burden, and cost.
2. **P4-R3.2:** WHEN a capacity scenario is assessed, THE SYSTEM SHALL require reasoning about model loading, accelerator/memory needs, input/output token processing, concurrency, scaling behavior, utilization, quotas, and failure margins.
3. **P4-R3.3:** WHEN a model strategy is proposed, THE SYSTEM SHALL evaluate smaller/specialized models, cascading, and hybrid deployment where they improve the quality/resource balance.
4. **P4-R3.4:** IF required workload assumptions or units are absent or incompatible, THEN THE SYSTEM SHALL mark the decision evidence insufficient rather than calculate a misleading recommendation.

### P4-R4 — Enterprise architecture and delivery controls

**User story:** As a learner, I want to integrate GenAI into enterprise systems with secure delivery controls so that the design can be operated and rolled back safely.

#### Acceptance criteria

1. **P4-R4.1:** WHEN the learner studies `AIP-2.3`, THE SYSTEM SHALL cover legacy, API, event-driven, synchronized, on-premises, edge, cross-environment, regional, and jurisdictional integration patterns.
2. **P4-R4.2:** WHEN an enterprise design is assessed, THE SYSTEM SHALL require justified boundaries for API Gateway, Lambda, EventBridge, queues, and workflow orchestration plus federation, role-based access, least privilege, and model/data authorization.
3. **P4-R4.3:** WHEN a CI/CD design is assessed, THE SYSTEM SHALL require versioned artifacts, security scans, automated evaluation, explicit quality/safety gates, approval where needed, canary criteria, observability, rollback trigger, and rollback procedure.
4. **P4-R4.4:** IF a release gate, canary threshold, or rollback path is undefined, THEN THE SYSTEM SHALL classify the design as incomplete and schedule targeted remediation.
5. **P4-R4.5:** WHEN centralized gateway or shared-service patterns are taught, THE SYSTEM SHALL include tenant/identity propagation, policy enforcement, failure isolation, trace correlation, and regional/data-boundary trade-offs.

### P4-R5 — FM APIs, streaming, asynchronous patterns, and routing

**User story:** As a learner, I want to implement resilient model API patterns so that streaming and long-running workloads remain bounded, observable, and recoverable.

#### Acceptance criteria

1. **P4-R5.1:** WHEN the learner studies `AIP-2.4` and `AIP-2.5`, THE SYSTEM SHALL cover synchronous SDK calls, streaming delivery, asynchronous/queued AWS architectures, long-running requests, token limits, validation, and model failures.
2. **P4-R5.2:** WHEN an API interaction is assessed, THE SYSTEM SHALL require request/response schema validation, deadlines/timeouts, quota handling, bounded exponential backoff with jitter, retry classification, idempotency boundaries, fallback, cancellation/disconnect handling, and trace identifiers.
3. **P4-R5.3:** WHEN routing is assessed, THE SYSTEM SHALL require explicit policy based on content, complexity, capability, authorization/safety, quality, latency, availability, or cost and SHALL require a no-route/fallback outcome.
4. **P4-R5.4:** WHEN application integration is taught, THE SYSTEM SHALL cover accessible interfaces, API-first/no-code patterns, document/business workflows including Bedrock Data Automation use cases, prompt chains, AWS-native orchestration, and appropriate Amazon Q Developer use.
5. **P4-R5.5:** IF throttling, timeout, partial stream, duplicate event, invalid schema, or downstream failure occurs, THEN THE SYSTEM SHALL require evidence-led handling without unbounded retries, duplicate side effects, or false success.
6. **P4-R5.6:** WHEN asynchronous AWS patterns are taught, THE SYSTEM SHALL model them in lab architecture/evidence; the local study platform SHALL remain synchronous unless a separately measured requirement approves otherwise.

### P4-R6 — Observability and evidence-led troubleshooting

**User story:** As a learner, I want to diagnose agent and API failures from logs and traces so that I can find the narrowest justified remediation.

#### Acceptance criteria

1. **P4-R6.1:** WHEN a Phase 4 workflow is observed, THE SYSTEM SHALL teach correlation among request, session, agent step, tool call, model call, event, retry, fallback, and outcome without logging hidden reasoning or sensitive payloads.
2. **P4-R6.2:** WHEN troubleshooting is assessed, THE SYSTEM SHALL require use of sanitized CloudWatch/Logs Insights and X-Ray or equivalent trace evidence to identify root cause before proposing remediation.
3. **P4-R6.3:** WHEN a failure drill is completed, THE SYSTEM SHALL record the injected fault, evidence references, diagnosis, rejected hypotheses, remediation, and validation of recovery.
4. **P4-R6.4:** IF logs or traces are missing, ambiguous, privacy-unsafe, or inconsistent with the claimed cause, THEN THE SYSTEM SHALL mark the proof incomplete or failed.
5. **P4-R6.5:** WHEN telemetry examples are stored, THE SYSTEM SHALL redact credentials, tokens, PII, private prompts/content, tool secrets, request signatures, and answer keys.

### P4-R7 — Questions, Labs 6–7, and lab safety

**User story:** As a learner, I want reviewed questions and realistic integration labs so that my measured competence includes safe failure handling, not just a happy path.

#### Acceptance criteria

1. **P4-R7.1:** WHEN a Domain 2 question is published for scoring, THE SYSTEM SHALL require objective IDs, difficulty, format, material constraint, sources, separate answer/rubric, rationale for every option/criterion, current-source approval, and independent review.
2. **P4-R7.2:** WHEN an unanswered question is delivered, THE SYSTEM SHALL return no answer key, rubric, correctness marker, or hidden mock feedback.
3. **P4-R7.3:** WHEN Lab 6 runs, THE SYSTEM SHALL map it to `AIP-2.1`, `AIP-3.1`, `AIP-4.3`, and `AIP-5.1` and require tool schema, IAM boundary, timeout, trace, human escalation, and an unsafe-tool-call failure drill.
4. **P4-R7.4:** WHEN Lab 7 runs, THE SYSTEM SHALL map it to `AIP-2.3`, `AIP-2.4`, and `AIP-2.5` and require streaming, asynchronous path, retries, routing, enterprise event integration, and traces including throttling and fallback proof.
5. **P4-R7.5:** WHEN either lab is published, THE SYSTEM SHALL require prerequisites, objectives, Mermaid architecture, cost class, Region, learner actions, predictions, allowlisted validation, failure injection, reflection, cleanup, and delayed recall.
6. **P4-R7.6:** BEFORE either lab starts, THE SYSTEM SHALL validate profile/credential-chain availability, Region allowlist, budget/cost acknowledgment, prerequisites, required tags, and cleanup plan without storing credentials.
7. **P4-R7.7:** WHEN checkpoint status changes, THE SYSTEM SHALL require committed evidence for `Verified` and proven absence/terminal deletion state for `Cleaned up`; inconclusive, unavailable, unauthorized, or failed checks SHALL NOT report success.
8. **P4-R7.8:** IF a full solution is revealed, THEN THE SYSTEM SHALL mark completion assisted until later unaided evidence exists.

### P4-R8 — Mastery, exit gate, and downstream handoff

**User story:** As a maintainer, I want an auditable Domain 2 completion decision so that later phases inherit trustworthy agent and integration evidence.

#### Acceptance criteria

1. **P4-R8.1:** WHEN progress is reported, THE SYSTEM SHALL show reviewed concept, scenario, troubleshooting, and hands-on coverage for each of `AIP-2.1`–`AIP-2.5`, plus misconceptions, confidence, lab proof/cleanup, freshness, and readiness risks.
2. **P4-R8.2:** WHEN fresh delayed accuracy is calculated, THE SYSTEM SHALL use only independently reviewed, previously unseen Domain 2 scenario questions attempted in the configured delayed window and SHALL report numerator, denominator, exclusions, and per-objective results.
3. **P4-R8.3:** WHEN exit readiness is evaluated, THE SYSTEM SHALL require at least 80% fresh delayed Domain 2 scenario accuracy and complete four-form coverage for all five objectives.
4. **P4-R8.4:** WHEN exit readiness is evaluated, THE SYSTEM SHALL require passing evidence that the learner identifies unsafe autonomy/integration designs and completes agent/API failure drills from logs/traces without prohibited hint assistance.
5. **P4-R8.5:** WHEN exit readiness is evaluated, THE SYSTEM SHALL require Labs 6–7 proof complete, required cleanup verified, and no unresolved critical source, safety, security, privacy, cost, or evidence failure.
6. **P4-R8.6:** IF any exit condition fails, THEN THE SYSTEM SHALL keep Phase 4 incomplete and create objective-specific remediation and due-review actions.
7. **P4-R8.7:** WHEN all conditions pass, THE SYSTEM SHALL emit a versioned handoff containing artifact/source versions, objective/form coverage, question/review state, lab/evidence IDs, mastery inputs/results, schema/migration/contracts, and open risks for Phases 5–8.
## Glossary

- **Bounded agent:** An agent constrained by typed tools, policy, identity, stopping, step/time/cost limits, and safe failure.
- **Fresh/delayed:** Previously unseen to the learner and attempted after the configured review interval.
- **Idempotency:** Equivalent replay produces no duplicate side effect and returns the prior compatible outcome.
- **Trace-led:** Diagnosis supported by correlated, privacy-safe telemetry rather than guesswork.
- **Unaided:** Completed without answer reveal or procedural/full-solution hint.
