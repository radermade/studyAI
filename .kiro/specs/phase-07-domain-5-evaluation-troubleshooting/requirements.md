# Requirements Document

## Introduction

**Title:** Phase 7 — Domain 5 Evaluation and Troubleshooting

**Status:** Proposed

**Scope:** Deliver complete mastery for `AIP-5.1` and `AIP-5.2`, Lab 11, Lab 12, a calibrated evaluation system, systematic multi-fault troubleshooting, and evidence suitable for release decisions and Phase 8 readiness.

## Upstream dependencies

- Phase 0 blueprint/source lock, learner constraints, AWS safety and budget policy.
- Phase 1 durable questions, attempts, misconceptions, reviews, sessions, source search, typed MCP contracts, and answer-key separation.
- Phase 2 Learn/Grill/Labs/Review/Progress workflows, hint/evidence states, durable resume, and accessibility.
- Phase 3 prompt versions and RAG/retrieval evidence from Labs 2–4.
- Phase 4 agent/API/CI-CD/deployment evidence from Labs 6–7.
- Phase 5 safety, responsible-AI, governance, and multi-tenant controls from Labs 5 and 8.
- Phase 6 immutable benchmark, telemetry, incident, diagnosis, and quality/safety-floor evidence from Labs 9–10.

Unavailable predecessor contracts SHALL block dependent implementation and SHALL NOT be treated as completed.

## Out of scope

- Treating model-based judging as ground truth or exposing hidden model reasoning.
- Production deployments, automated AWS mutation, unrestricted fault injection, or release execution.
- Exam dumps, unreviewed generated questions, or readiness scoring from previously exposed items.
- Random prompt editing without a reproducible hypothesis and comparison.

## Glossary

- **Golden set:** A versioned, reviewed evaluation dataset with declared expected evidence.
- **Calibrated judge:** A model evaluator accepted against blinded independent human labels at a predeclared threshold.
- **Inconclusive:** Evidence insufficient or incomparable for a pass/fail decision.

## Requirements

### P7-R1 — Source-grounded Domain 5 curriculum and question bank

**User story:** As a learner, I want complete, current Domain 5 content so that evaluation and troubleshooting choices are traceable and exam relevant.

#### Acceptance criteria

1. WHEN content is ingested, THE SYSTEM SHALL require `AIP-5.1` or `AIP-5.2`, primary-source metadata, retrieval date, freshness, trade-offs, failure modes, verification, and fact/recommendation/note classification.
2. THE SYSTEM SHALL provide concept, scenario, troubleshooting, and hands-on evidence for both `AIP-5.1` and `AIP-5.2`.
3. WHEN a question is admitted to scoring, THE SYSTEM SHALL require meaningful constraints, difficulty, MCQ/MR or supported format, sources, separate key/rubric, every-option rationale, review state, and independent review.
4. IF source integrity, freshness, review, or objective mapping fails, THEN THE SYSTEM SHALL exclude the item from scored and fresh pools and expose the reason.
5. THE SYSTEM SHALL keep unanswered question DTOs structurally incapable of carrying answer keys or rubrics.

### P7-R2 — Versioned evaluation datasets and deterministic checks

**User story:** As an evaluator, I want stable datasets and deterministic checks so that comparisons and regressions are reproducible.

#### Acceptance criteria

1. WHEN an evaluation dataset is created, THE SYSTEM SHALL version examples, objective/segment labels, provenance, consent/license status, expected evidence, exclusions, split membership, and review status.
2. THE SYSTEM SHALL separate development, calibration, regression, and fresh holdout sets and SHALL prevent holdout answers from appearing in learner-visible or browser-visible state.
3. THE SYSTEM SHALL support deterministic schema, citation, exact/normalized match where appropriate, policy, latency, cost, and tool-contract checks with explicit pass/fail thresholds.
4. WHEN dataset or evaluator versions change, THE SYSTEM SHALL invalidate incomparable prior release decisions or label them non-equivalent.
5. IF data contains credentials, PII, private retrieved content, or unauthorized material, THEN THE SYSTEM SHALL reject or redact it before persistence or evaluation.

### P7-R3 — Multi-method evaluation and calibrated model judging

**User story:** As a learner, I want evaluation to combine complementary methods so that no single noisy metric determines quality.

#### Acceptance criteria

1. THE SYSTEM SHALL evaluate applicable relevance, correctness, groundedness, factuality, consistency, fluency, safety, fairness, business outcome, latency, and cost dimensions using declared metrics and limitations.
2. THE SYSTEM SHALL combine deterministic checks, model-based judging, and human review; missing methods SHALL be explicitly justified per evaluation dimension.
3. BEFORE a model judge contributes to a release gate, THE SYSTEM SHALL compare it against a blinded, independently reviewed human calibration set and record agreement, disagreement categories, bias checks, and an acceptance threshold.
4. IF calibration is below its declared threshold or materially differs across protected/safety-relevant segments, THEN THE SYSTEM SHALL exclude the judge from gating and require human adjudication or recalibration.
5. WHEN judge and human labels disagree on a gate-affecting result, THE SYSTEM SHALL preserve both labels, route the case to adjudication, and SHALL NOT silently overwrite either.
6. THE SYSTEM SHALL record judge model/configuration/prompt version, but SHALL NOT persist hidden reasoning or send private learner/AWS data to an external service without explicit direction.

### P7-R4 — Retrieval and agent evaluation

**User story:** As a learner, I want retrieval and agent behavior measured at their own boundaries so that an end-response score does not hide the failing subsystem.

#### Acceptance criteria

1. THE SYSTEM SHALL measure retrieval relevance, recall at declared cutoffs, ranking quality where labels exist, latency, filter/tenant correctness, citation support, and index/source freshness.
2. THE SYSTEM SHALL measure agent task completion, tool-selection correctness, argument-schema validity, tool success/failure handling, step/tool count, timeout/stop compliance, escalation, safety, latency, and cost.
3. IF tenant isolation, authorization, unsafe-tool, or stop-condition tests fail, THEN THE SYSTEM SHALL fail the release gate regardless of aggregate quality.
4. WHEN a metric lacks sufficient labels or sample size, THE SYSTEM SHALL mark it inconclusive rather than infer success.
5. THE SYSTEM SHALL link subsystem metrics to end-to-end examples, traces, dataset versions, and evaluator versions.

### P7-R5 — Continuous regression and release quality gate (Lab 11)

**User story:** As a release owner, I want a reproducible release gate so that model, prompt, retrieval, or agent changes ship only with acceptable evidence.

#### Acceptance criteria

1. THE SYSTEM SHALL deliver Lab 11 with exact mappings `AIP-1.6`, `AIP-3.4`, and `AIP-5.1` and proof consisting of a golden set, metrics, judge calibration, and deployment decision.
2. Lab 11 SHALL include prerequisites, objectives, architecture, cost class, Region assumptions, steps, predictions, hints, validation, a regression injection, reflection, cleanup, and delayed recall.
3. WHEN a candidate is evaluated, THE SYSTEM SHALL compare it to a versioned baseline on the same eligible dataset and record deterministic, human/calibrated-judge, retrieval/agent where applicable, safety, latency, and cost results.
4. THE SYSTEM SHALL support `pass`, `fail`, and `inconclusive` release decisions with declared hard floors, regression tolerances, limitations, approver, and rollback recommendation.
5. IF any hard safety, privacy, authorization, tenant-isolation, schema, or quality floor fails, THEN THE SYSTEM SHALL produce `fail` regardless of aggregate gains.
6. WHEN a gate is replayed with identical event ID and payload, THE SYSTEM SHALL return the committed result; a mismatched replay SHALL produce a conflict.

### P7-R6 — Systematic hidden multi-fault diagnosis (Lab 12)

**User story:** As a troubleshooter, I want a realistic hidden challenge so that I learn to isolate faults from evidence rather than guess.

#### Acceptance criteria

1. THE SYSTEM SHALL deliver Lab 12 with exact mappings `AIP-4.3` and `AIP-5.2` and proof consisting of evidence-based root causes and minimal remediations.
2. Lab 12 SHALL contain multiple hidden faults spanning the applicable categories of prompt regression, context overflow/truncation, retrieval preprocessing/chunking/embedding/index/filter/ranking/freshness, IAM/API authorization, quota/throttle, request/response schema, timeout/integration, and latency.
3. THE SYSTEM SHALL store the fault manifest and answer rubric separately from the unanswered challenge and learner-visible state.
4. FOR EACH injected fault, THE SYSTEM SHALL require symptom reproduction, evidence, competing hypothesis elimination, root cause, narrow remediation, regression check, and rollback note.
5. IF the learner changes a prompt or configuration without a testable hypothesis and controlled evidence, THEN THE SYSTEM SHALL record the action but SHALL NOT accept it as diagnostic proof.
6. THE SYSTEM SHALL require isolation of every seeded fault; false positives and broad unjustified remediations SHALL remain unresolved.
7. Fault injection and validators SHALL be bounded, reversible, local/synthetic or read-only, and SHALL NOT mutate AWS resources.

### P7-R7 — Evidence, failures, privacy, safety, and cost

**User story:** As a learner, I want trustworthy evaluation evidence with safe failure handling so that conclusions survive review without exposing sensitive data or incurring uncontrolled cost.

#### Acceptance criteria

1. WHEN evaluation, adjudication, release, diagnosis, or lab evidence is recorded, THE SYSTEM SHALL commit stable IDs, UTC timestamps, versions, provenance, limitations, and event IDs transactionally in SQLite before reporting success.
2. THE SYSTEM SHALL distinguish validation, conflict, unavailable dependency, authorization, budget, inconclusive evidence, and internal failure and preserve recoverable state.
3. THE SYSTEM SHALL redact credentials, tokens, PII, full private prompts, answer keys, and sensitive retrieved content from logs, traces, exports, and UI payloads.
4. WHEN AWS validation is used, THE SYSTEM SHALL use standard credentials, explicit Region and allowlisted read-only actions; no raw SQL, shell, Python evaluation, filesystem, or AWS CLI tool SHALL be exposed.
5. BEFORE chargeable evaluation begins, THE SYSTEM SHALL show cost class, bounded sample size, timeout, retry limit, and budget ceiling; exceeding the ceiling SHALL stop further paid work and preserve partial evidence as incomplete.
6. THE SYSTEM SHALL NOT report `Verified`, release `pass`, persistence success, or `Cleaned up` before the corresponding committed evidence or verified absence/terminal deletion state exists.

### P7-R8 — Stakeholder evaluation report

**User story:** As a stakeholder, I want an understandable comparison with limitations so that I can make a decision without mistaking uncertain metrics for facts.

#### Acceptance criteria

1. WHEN an evaluation report is generated, THE SYSTEM SHALL identify baseline/candidate, dataset and evaluator versions, metrics/floors, confidence or sample limitations, disagreements/adjudications, safety/privacy results, latency/cost assumptions, and release decision.
2. THE SYSTEM SHALL distinguish measured results, estimates, human judgments, calibrated model judgments, and project recommendations.
3. THE SYSTEM SHALL include retrieval and agent subsystem findings when applicable and link claims to immutable evidence references.
4. IF evidence is incomplete or incomparable, THEN THE SYSTEM SHALL present `inconclusive` and list required next evidence rather than recommend release.
5. THE SYSTEM SHALL produce a non-sensitive export that excludes private examples, answer keys, hidden faults, and judge reasoning.

### P7-R9 — Phase 7 exit gate and handoff

**User story:** As the program owner, I want an exact completion gate so that exam simulation starts only after evaluation and troubleshooting mastery is demonstrated.

#### Acceptance criteria

1. THE SYSTEM SHALL require accepted source/question coverage for both `AIP-5.1` and `AIP-5.2`.
2. THE SYSTEM SHALL require complete Lab 11 proof: golden set, deterministic and model/human evaluation, accepted judge calibration or documented human-only gate, retrieval/agent metrics where applicable, release decision, delayed recall, and verified cleanup where applicable.
3. THE SYSTEM SHALL require the learner to isolate every Lab 12 seeded fault and propose the narrowest justified remediation with regression evidence.
4. THE SYSTEM SHALL require observed controlled evidence use and SHALL reject ad hoc prompt editing as completion evidence.
5. THE SYSTEM SHALL require at least 80% accuracy on a fresh, independently reviewed Domain 5 scenario set after delayed review.
6. IF any gate fails, THEN THE SYSTEM SHALL keep Phase 7 incomplete and emit targeted remediation.
7. WHEN all gates pass, THE SYSTEM SHALL emit a versioned Phase 8 handoff containing coverage, fresh-item eligibility, evaluation/report evidence, lab/cleanup proof, unresolved low-priority risks, and source freshness without hidden answers or private data.
