# Requirements Document

## Phase 00 Blueprint, Safety, and Baseline

## Introduction

**Status:** Proposed  
**Scope:** Lock the AIP-C01 blueprint, establish attributable source and learner-profile contracts, define AWS lab safety controls, and record a trustworthy baseline diagnostic before study-core implementation.

## Upstream Dependencies

- `.kiro/roadmap/roadmap.md`, especially Phase 0, the knowledge-domain specification, content acceptance criteria, and platform security gates.
- Workspace technology, Python, and learning-UI steering documents.
- Current official AWS AIP-C01 exam guide and domain pages. Network access is required only to refresh or verify source metadata; offline use of a previously verified registry remains supported.
- A learner supplies profile, budget, account, and diagnostic inputs. AWS credentials are not required in this phase.

## Out of Scope

- Adaptive scheduling, question serving, grading automation, MCP transport, Streamlit learning views, or AWS resource mutation.
- Copying official exam questions, exam dumps, or proprietary course material.
- Proving certification readiness from the baseline, provisioning AWS budgets/resources, or validating lab resources.
- Domain lesson authoring beyond source registry and original diagnostic/seed-content contracts.

## Glossary

- **Blueprint:** A versioned set of official exam domains, task IDs, and weights.
- **Admission:** Validation that allows authored content or a lab definition into downstream use.
- **Freshness:** Truthful source-review state independent of network availability.
- **Handoff:** Versioned machine-readable artifacts plus acceptance evidence consumed by Phase 1.

## Requirements

### P0-R1 — Versioned objective manifest

**User story:** As a learner and content maintainer, I want one machine-readable blueprint manifest so that all later study activity can be traced to the current exam tasks.

#### Acceptance Criteria

1. WHEN the manifest is built, THE SYSTEM SHALL include exactly the stable task IDs `AIP-1.1` through `AIP-1.6`, `AIP-2.1` through `AIP-2.5`, `AIP-3.1` through `AIP-3.4`, `AIP-4.1` through `AIP-4.3`, and `AIP-5.1` through `AIP-5.2`.
2. WHEN an objective record is read, THE SYSTEM SHALL expose its task ID, domain ID, title, blueprint version, status, source references, and normalized exam weight context.
3. IF an objective ID is duplicated, malformed, missing, or assigned to the wrong domain, THE SYSTEM SHALL reject the manifest with an actionable validation error and SHALL NOT publish a partial manifest.
4. WHEN domain weights are validated, THE SYSTEM SHALL require 31%, 26%, 20%, 12%, and 11% for Domains 1–5 respectively and a total of 100%.
5. WHEN a future blueprint is adopted, THE SYSTEM SHALL create a new versioned manifest while preserving IDs and historical manifests used by recorded activity.

### P0-R2 — Attributable source registry

**User story:** As a learner, I want every blueprint and study source to be attributable and freshness-aware so that I can distinguish current AWS facts from stale or project-authored guidance.

#### Acceptance Criteria

1. WHEN a source is registered, THE SYSTEM SHALL store a stable source ID, canonical HTTPS URL, title, publisher, retrieval date, source type, applicable objective IDs, freshness status, and blueprint version.
2. WHEN Phase 0 is accepted, THE SYSTEM SHALL include the official AIP-C01 overview, all five official domain pages, and the official certification/preparation page in the registry.
3. IF a source references an unknown objective or uses an invalid retrieval date or URL, THE SYSTEM SHALL reject the record and report the invalid fields.
4. WHEN source content is summarized, THE SYSTEM SHALL label the result as AWS-documented fact, project recommendation, or learner note and SHALL preserve attribution without copying restricted text.
5. WHILE source refresh is unavailable, THE SYSTEM SHALL retain the last verified metadata, mark its freshness accurately, and SHALL NOT claim it was revalidated.

### P0-R3 — Learner profile contract

**User story:** As a learner, I want my constraints captured explicitly so that later study plans and labs fit my schedule, experience, Region, account, and budget.

#### Acceptance Criteria

1. WHEN a profile is created, THE SYSTEM SHALL validate exam date or undecided status, weekly study capacity, AWS experience level, target Region, account type, and lab budget.
2. IF an exam date is in the past, weekly capacity is non-positive, Region is malformed, or budget is negative, THE SYSTEM SHALL reject the profile with field-level guidance.
3. WHEN a profile is updated, THE SYSTEM SHALL preserve a UTC timestamp and stable learner ID without storing AWS credentials, account secrets, or payment data.
4. WHERE a learner declines an optional profile field, THE SYSTEM SHALL represent it explicitly as unknown rather than infer a value.

### P0-R4 — AWS lab safety policy

**User story:** As a learner, I want enforceable pre-lab safety rules so that hands-on study minimizes privilege, cost, and orphaned-resource risk.

#### Acceptance Criteria

1. WHEN a safety policy is created, THE SYSTEM SHALL define a dedicated named-profile recommendation, standard credential-chain use, least-privilege/read-only validator policy, Region allowlist, budget-alert prerequisite, study-session/ownership tag rules, and cleanup evidence rules.
2. WHEN any lab definition is admitted, THE SYSTEM SHALL require prerequisites, learning objectives, architecture context, estimated cost class, Region assumptions, stepwise instructions, prediction prompts, validation, failure injection, reflection, cleanup, and delayed recall.
3. IF a lab lacks prerequisites, expected cost class, Region assumptions, or cleanup procedure, THE SYSTEM SHALL mark it blocked and SHALL NOT permit it to start.
4. WHEN a validator is specified, THE SYSTEM SHALL require an explicit service/action allowlist containing only read-only `Get`, `List`, or `Describe`-style operations unless a later separately approved scope authorizes mutation.
5. WHEN cleanup is reported, THE SYSTEM SHALL distinguish requested, self-reported, verified absent, terminal deletion state, and failed verification; a click or navigation event SHALL NOT establish cleanup.
6. IF credentials, request signatures, tokens, secrets, or sensitive private content appear in policy, evidence, or logs, THE SYSTEM SHALL reject or redact them and surface a security error.

### P0-R5 — Baseline diagnostic contract

**User story:** As a learner, I want a baseline diagnostic across the complete blueprint so that initial strengths, weaknesses, speed, and confidence are measurable.

#### Acceptance Criteria

1. WHEN a baseline begins, THE SYSTEM SHALL identify whether it is an official external pretest record or a local original diagnostic and SHALL bind it to learner, blueprint version, and UTC start time.
2. WHEN a local diagnostic is assembled, THE SYSTEM SHALL sample every one of the 20 task IDs and SHALL use only original or legitimately licensed prompts with source references.
3. WHEN an answer is captured, THE SYSTEM SHALL record response, confidence, elapsed time, objective IDs, and completion state without exposing the answer key before submission.
4. WHEN the baseline is submitted, THE SYSTEM SHALL record per-task/per-domain performance, confidence calibration, unanswered items, and a clear statement that the result is not an AWS score prediction or readiness guarantee.
5. IF a diagnostic is interrupted, THE SYSTEM SHALL preserve completed responses and represent the run as incomplete rather than fabricate scores for unanswered items.
6. IF answer or timing data cannot be durably recorded, THE SYSTEM SHALL report failure and SHALL NOT claim baseline completion.

### P0-R6 — Seed-content admission contract

**User story:** As a content author, I want a precise admission contract for Phase 1 seed questions so that coverage and scoring quality are testable.

#### Acceptance Criteria

1. WHEN Phase 1 seed content is accepted, THE SYSTEM SHALL require at least two original scenario prompts for each of the 20 AIP task IDs, for a minimum of 40 prompts.
2. WHEN a graded prompt is admitted, THE SYSTEM SHALL require stable ID, objective IDs, difficulty, format, material scenario constraint, source references, answer or rubric, distractor rationales where applicable, and review status.
3. WHEN an unanswered prompt payload is produced, THE SYSTEM SHALL be structurally incapable of carrying answer keys, rubrics, correct-option flags, or hidden mock state.
4. IF a prompt lacks attribution, uses an unknown objective, contains unsupported absolute claims, or is unreviewed for readiness scoring, THE SYSTEM SHALL reject it from the scored bank.
5. WHERE authored content uses Markdown and YAML front matter, THE SYSTEM SHALL validate front matter before normalized ingestion.

### P0-R7 — Deterministic handoff artifacts

**User story:** As a Phase 1 implementer, I want validated, stable Phase 0 artifacts so that ingestion does not depend on prose interpretation.

#### Acceptance Criteria

1. WHEN Phase 0 artifacts are exported, THE SYSTEM SHALL provide deterministic machine-readable objective, source, learner-profile, safety-policy, baseline-summary, and seed-admission schemas with explicit schema versions.
2. WHEN the same valid inputs are processed repeatedly, THE SYSTEM SHALL produce semantically equivalent identifiers and normalized values.
3. IF an artifact schema version is unsupported, THE SYSTEM SHALL fail closed with a compatibility error and SHALL preserve the original artifact.
4. WHEN an artifact is changed, THE SYSTEM SHALL preserve provenance, UTC change time, and prior versions needed by downstream records.

### P0-R8 — Security, privacy, and local-first integrity

**User story:** As a learner, I want baseline data protected locally so that preparation does not expose credentials, private AWS data, or sensitive history.

#### Acceptance Criteria

1. WHEN Phase 0 data is persisted, THE SYSTEM SHALL place runtime state under gitignored `data/` storage and SHALL keep authored manifests and schemas free of secrets.
2. WHEN timestamps are stored, THE SYSTEM SHALL use timezone-aware UTC ISO 8601 values.
3. WHEN structured inputs cross ingestion boundaries, THE SYSTEM SHALL validate them with Pydantic v2 models and reject unknown or malformed security-critical fields.
4. WHILE offline, THE SYSTEM SHALL permit profile, manifest, registry, and local diagnostic operations that do not require source refresh.
5. IF a write fails, THE SYSTEM SHALL leave the prior valid artifact intact and SHALL NOT report success.

### P0-R9 — Phase 0 exit gate

**User story:** As the project owner, I want an objective release gate so that Phase 1 starts only from complete, safe, and measurable inputs.

#### Acceptance Criteria

1. WHEN Phase 0 is declared complete, THE SYSTEM SHALL verify that every current official task is represented in the manifest.
2. WHEN Phase 0 is declared complete, THE SYSTEM SHALL verify that no admitted lab can begin without prerequisites, expected cost class, and cleanup procedure.
3. WHEN Phase 0 is declared complete, THE SYSTEM SHALL verify that baseline strengths, weaknesses, and confidence calibration are recorded or explicitly identify an incomplete diagnostic as a blocking condition.
4. IF any exit check fails, THE SYSTEM SHALL report each blocker and SHALL NOT emit a Phase 0 accepted status.
5. WHEN all exit checks pass, THE SYSTEM SHALL emit a versioned handoff summary consumable by Phase 1 without claiming certification readiness.
