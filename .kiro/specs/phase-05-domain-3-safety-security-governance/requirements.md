# Requirements Document

## Introduction

**Title:** Phase 5 — Domain 3 Safety, Security, and Governance  
**Status:** Proposed  
**Scope:** Deliver source-grounded learning, independently reviewed scored practice, threat-model and governance artifacts, and Labs 5 and 8 for AIP-C01 Domain 3 (`AIP-3.1`–`AIP-3.4`), with evidence-based control validation and a measurable mastery exit gate.

## Upstream dependencies

- Phase 0: valid objective/source manifests, learner profile/diagnostic, and AWS safety policy with Region/profile/budget/tag/cleanup rules.
- Phase 1: local-first SQLite core, source ingestion/FTS5, sessions, grading, misconceptions, spaced review, typed MCP boundaries, and answer separation.
- Phase 2: accessible Learn/Grill/Labs/Review/Knowledge/Progress UI, durable lab state, six checkpoint statuses, hint records, read-only validator boundary, and explicit offline/error states.
- Phase 3: approved RAG/vector metadata, prompt-governance, evidence, source/review, and Lab 3–4 retrieval contracts.
- Phase 4: approved agent/tool/API identity, policy, observability, trace-drill, evidence, and Lab 6–7 integration contracts.
- Missing or incompatible upstream contracts SHALL block affected Phase 5 work and be reported; Phase 5 SHALL not bypass them with a parallel security store or tool surface.

## Out of scope

- Claiming legal, regulatory, privacy, fairness, or security certification or professional advice.
- Broad AWS mutation, active offensive exploitation, covert monitoring, collection of real PII, or storage of secrets/private prompts/private retrieved content.
- A hosted policy service, SIEM, identity provider, vector database, local model, or new general-purpose API.
- Treating guardrails, prompt instructions, encryption, network isolation, or any single control as complete security.
- Auto-completing Domains 1, 2, or 5 from cross-domain Labs 5/8 evidence.

## Requirements

### P5-R1 — Domain 3 source and coverage integrity

**User story:** As a learner, I want current, attributable safety and governance material so that I can separate AWS-documented behavior from project guidance and policy assumptions.

#### Acceptance criteria

1. **P5-R1.1:** WHEN Phase 5 content is ingested, THE SYSTEM SHALL require a stable content ID, one or more IDs from `AIP-3.1`–`AIP-3.4`, and primary-source URL, title, publisher, retrieval date, and freshness status.
2. **P5-R1.2:** WHEN material is approved, THE SYSTEM SHALL label AWS facts, project recommendations, learner notes, threat assumptions, trade-offs, failure modes, verification methods, and limitations separately.
3. **P5-R1.3:** WHEN coverage is audited, THE SYSTEM SHALL report approved concept, scenario, troubleshooting, and hands-on evidence for each Domain 3 objective and identify missing forms.
4. **P5-R1.4:** IF a source is stale, superseded, unreachable, conflicting, or jurisdiction-specific beyond its stated scope, THEN THE SYSTEM SHALL preserve lineage, block new scored use, and create a review finding.
5. **P5-R1.5:** WHEN cached material is used offline, THE SYSTEM SHALL identify source freshness and unavailable external/control verification.

### P5-R2 — Defense in depth and adversarial safety

**User story:** As a learner, I want to design and test layered safety controls so that direct or indirect adversarial input cannot rely on a single prompt-based defense.

#### Acceptance criteria

1. **P5-R2.1:** WHEN the learner studies `AIP-3.1`, THE SYSTEM SHALL cover preprocessing, identity/policy, model controls, Bedrock Guardrails, retrieval controls, tool controls, postprocessing, structured schemas, grounding/verification, confidence/uncertainty, and API boundaries.
2. **P5-R2.2:** WHEN a threat model is created, THE SYSTEM SHALL include assets, actors, trust boundaries, data flows, direct prompt injection, indirect injection, jailbreaks, adversarial input, data exfiltration, unsafe tool parameters/tool misuse, poisoned retrieval, and control owners.
3. **P5-R2.3:** WHEN an adversarial case is evaluated, THE SYSTEM SHALL record attack category, safe synthetic input reference, expected policy outcome, actual outcome, layer/control decisions, false-positive/false-negative classification, and sanitized evidence.
4. **P5-R2.4:** IF a design relies only on prompt instructions or one control layer, THEN THE SYSTEM SHALL mark it insufficient and require defense-in-depth remediation.
5. **P5-R2.5:** IF an input, retrieved item, model output, or tool proposal violates policy or lacks required grounding/schema, THEN THE SYSTEM SHALL require reject, constrain, verify, or human-escalate behavior before any privileged action or unsafe response.
6. **P5-R2.6:** WHEN adversarial materials are authored, THE SYSTEM SHALL use benign synthetic fixtures and SHALL NOT include live credentials, real private data, destructive payloads, or instructions intended for unauthorized use.

### P5-R3 — Data security, privacy, and tenant isolation

**User story:** As a learner, I want to validate identity-aware data isolation and privacy controls so that one tenant, component, or log path cannot expose another tenant’s information.

#### Acceptance criteria

1. **P5-R3.1:** WHEN the learner studies `AIP-3.2`, THE SYSTEM SHALL cover IAM, VPC endpoints/network isolation, encryption, Lake Formation/data authorization, logging, least privilege, provider data handling/retention, and lifecycle controls.
2. **P5-R3.2:** WHEN PII handling is assessed, THE SYSTEM SHALL require data classification, minimization, detection, masking/redaction/anonymization choice, retention/deletion, access/audit controls, and failure handling using synthetic data.
3. **P5-R3.3:** WHEN multi-tenant RAG is assessed, THE SYSTEM SHALL require tenant identity and authorization to remain bound through retrieval filters, context, memory, caches, logs, model/tool calls, citations, and outputs.
4. **P5-R3.4:** WHEN tenant-isolation tests run, THE SYSTEM SHALL include positive access, cross-tenant denial, missing/forged tenant context, filter bypass, cache/memory bleed, citation leakage, and audit-correlation cases.
5. **P5-R3.5:** IF any cross-tenant result, unredacted sensitive value, unauthorized citation, or identity-binding gap is observed, THEN THE SYSTEM SHALL mark the relevant checkpoint failed, retain sanitized evidence, and block completion until corrected and retested.
6. **P5-R3.6:** WHEN evidence or telemetry is persisted, THE SYSTEM SHALL store only minimized synthetic/sanitized summaries and references, never credentials, request signatures, secrets, real PII, full private prompts, or private retrieved content.

### P5-R4 — Governance, lineage, and auditability

**User story:** As a learner, I want traceable governance controls so that model, prompt, data, retrieval, tool, and human decisions can be reviewed without exposing sensitive content.

#### Acceptance criteria

1. **P5-R4.1:** WHEN the learner studies `AIP-3.3`, THE SYSTEM SHALL cover model/system cards, lineage, metadata, source attribution/citations, decision logs, Glue Data Catalog/tagging patterns, CloudTrail audit records, policy-control mapping, and continuous control monitoring.
2. **P5-R4.2:** WHEN a governance control is recorded, THE SYSTEM SHALL capture stable control ID, policy objective, technical/administrative control, owner, scope, evidence type, test cadence, pass criteria, exception/expiry, and mapped objective IDs.
3. **P5-R4.3:** WHEN lineage is assessed, THE SYSTEM SHALL trace approved source/data version, transformation/index version, prompt/model/guardrail/tool-policy version, invocation or evaluation correlation, output/citation, review decision, and retention state where applicable.
4. **P5-R4.4:** WHEN an audit-trail exercise runs, THE SYSTEM SHALL require enough sanitized, time-correlated evidence to reconstruct who/what/when/where/outcome without storing prohibited sensitive payloads.
5. **P5-R4.5:** IF evidence is missing, timestamps/correlation conflict, an exception is expired, or lineage has an unexplained gap, THEN THE SYSTEM SHALL mark the control unverified and create remediation.
6. **P5-R4.6:** WHEN organizational policy or regulation is discussed, THE SYSTEM SHALL label assumptions and jurisdiction, avoid compliance guarantees, and require qualified review for real-world adoption.

### P5-R5 — Responsible AI, fairness, and human oversight

**User story:** As a learner, I want to evaluate responsible-AI behavior and document limits so that users and reviewers understand uncertainty, disparate outcomes, and when humans must intervene.

#### Acceptance criteria

1. **P5-R5.1:** WHEN the learner studies `AIP-3.4`, THE SYSTEM SHALL cover intended use, limitations, exclusions, evidence/source attribution, uncertainty communication, user-facing explanations, guardrail/policy enforcement, and human-oversight responsibilities.
2. **P5-R5.2:** WHEN a fairness evaluation is recorded, THE SYSTEM SHALL require a versioned synthetic or approved test set, relevant groups/slices, justified metrics and thresholds, sample-size/coverage limits, comparative results, known confounders, and remediation or acceptance decision.
3. **P5-R5.3:** WHEN human oversight is designed, THE SYSTEM SHALL define trigger, decision authority, information shown, response deadline, escalation path, override/appeal, audit record, and fail-safe behavior.
4. **P5-R5.4:** IF evidence is insufficient to support a fairness, safety, or suitability claim, THEN THE SYSTEM SHALL require qualified language and SHALL NOT infer absence of harm from absence of detected failures.
5. **P5-R5.5:** WHEN a responsible-AI report is completed, THE SYSTEM SHALL link the system card, intended use/limits, sources, threat/control summary, fairness results, human oversight, unresolved risks, and review decision.

### P5-R6 — Scored questions and review integrity

**User story:** As a learner, I want original, independently reviewed security questions so that my score reflects defensible reasoning rather than unsafe or stale advice.

#### Acceptance criteria

1. **P5-R6.1:** WHEN a Domain 3 question is ingested, THE SYSTEM SHALL require stable ID, objective IDs, difficulty, format, material constraint, source references, separate answer/rubric, rationale for every option/criterion, and review state.
2. **P5-R6.2:** WHEN a question is used for readiness scoring, THE SYSTEM SHALL require current-source approval and independent review by someone other than its author.
3. **P5-R6.3:** WHEN an unanswered question is delivered, THE SYSTEM SHALL expose no answer key, rubric, correctness marker, hidden mock feedback, or unsafe private fixture.
4. **P5-R6.4:** WHEN an answer is graded, THE SYSTEM SHALL atomically commit attempt, confidence, elapsed time, misconception changes, and review schedule before recorded success.
5. **P5-R6.5:** IF a proposed answer uses unsupported absolutes, single-control security, real sensitive data, unscoped compliance claims, or unverified cleanup, THEN THE SYSTEM SHALL reject or require revision before publication.
6. **P5-R6.6:** WHEN feedback is allowed, THE SYSTEM SHALL explain the decisive threat/control, layered reasoning, why alternatives fail, source, and targeted follow-up without reproducing dangerous or private content.

### P5-R7 — Labs 5 and 8, evidence, safety, and cleanup

**User story:** As a learner, I want safe adversarial and tenant-isolation labs with verifiable evidence so that I can prove controls work and resources are cleaned up.

#### Acceptance criteria

1. **P5-R7.1:** WHEN either lab is published, THE SYSTEM SHALL require prerequisites, objectives, Mermaid architecture, cost class, Region, learner actions, predictions, allowlisted validation, safe failure injection, reflection, cleanup, and delayed recall.
2. **P5-R7.2:** WHEN Lab 5 runs, THE SYSTEM SHALL map it to `AIP-3.1`, `AIP-3.4`, and `AIP-5.1` and require a safe attack set, layered-control outcomes, and false-positive analysis.
3. **P5-R7.3:** WHEN Lab 8 runs, THE SYSTEM SHALL map it to `AIP-1.4`, `AIP-2.3`, `AIP-3.2`, and `AIP-3.3` and require identity-aware retrieval tests and audit evidence, including negative cross-tenant cases.
4. **P5-R7.4:** BEFORE a lab starts, THE SYSTEM SHALL validate the profile/standard credential chain, Region allowlist, prerequisites, cost/budget acknowledgment, required tags, synthetic-data rule, and cleanup plan without storing credentials.
5. **P5-R7.5:** WHEN a checkpoint is evaluated, THE SYSTEM SHALL use the upstream six statuses and require committed allowlisted evidence for `Verified`; self-report or a click SHALL NOT qualify.
6. **P5-R7.6:** WHEN cleanup is evaluated, THE SYSTEM SHALL require read-only evidence of absence or terminal deletion state before `Cleaned up`; a learner action or button click SHALL NOT qualify.
7. **P5-R7.7:** IF authorization, dependency, evidence, isolation, redaction, source-integrity, or cleanup validation fails or is inconclusive, THEN THE SYSTEM SHALL distinguish the condition, preserve sanitized progress, and SHALL NOT claim success.
8. **P5-R7.8:** WHEN the full solution or attack/control answer is revealed, THE SYSTEM SHALL mark completion assisted until later unaided evidence exists.

### P5-R8 — Mastery, exit gate, and downstream handoff

**User story:** As a maintainer, I want an auditable Domain 3 completion decision so that later evaluation and mock phases can trust safety evidence without treating it as certification.

#### Acceptance criteria

1. **P5-R8.1:** WHEN progress is shown, THE SYSTEM SHALL report four-form coverage per Domain 3 objective, delayed accuracy, confidence, misconceptions, independent/assisted lab evidence, cleanup, control validation across identity/data/retrieval/model/tool/output/audit layers, freshness, and risks.
2. **P5-R8.2:** WHEN fresh delayed accuracy is calculated, THE SYSTEM SHALL include only current, independently reviewed, previously unseen Domain 3 scenario questions attempted in the configured delayed window and SHALL report numerator, denominator, exclusions, and per-objective results.
3. **P5-R8.3:** WHEN exit readiness is evaluated, THE SYSTEM SHALL require approved concept, scenario, troubleshooting, and hands-on evidence for `AIP-3.1`–`AIP-3.4` and at least 80% fresh delayed Domain 3 scenario accuracy.
4. **P5-R8.4:** WHEN exit readiness is evaluated, THE SYSTEM SHALL require passing unaided defense-in-depth/threat-model evidence and validated controls at identity, data, retrieval, model, tool, output, and audit layers.
5. **P5-R8.5:** WHEN exit readiness is evaluated, THE SYSTEM SHALL require Labs 5 and 8 proof, verified cleanup where required, governance matrix, data lifecycle/lineage, model/system card, fairness evaluation, and human-oversight plan with no unresolved critical issue.
6. **P5-R8.6:** IF any gate fails, THEN THE SYSTEM SHALL keep Phase 5 incomplete and produce objective/control-specific remediation and due-review actions.
7. **P5-R8.7:** WHEN all gates pass, THE SYSTEM SHALL emit a versioned handoff containing approved artifacts/sources/reviews, coverage, control and lab evidence IDs, mastery inputs/results, limitations, schema/migration/contracts, and open risks for Phases 6–8.
## Glossary

- **Control evidence:** A current, scoped observation showing whether explicit pass criteria were met.
- **Defense in depth:** Independent preventive, detective, responsive, and evidentiary controls across relevant layers.
- **Fresh/delayed:** Previously unseen to the learner and attempted after the configured review interval.
- **Synthetic data:** Artificial data not representing a real person, credential, account, or private source.
- **Unaided:** Completed without answer reveal or procedural/full-solution hint.
