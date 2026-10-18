# Requirements Document

## Phase 01 Local Study Core

## Introduction

**Status:** Proposed  
**Scope:** Implement the local-first domain, persistence, ingestion, search, session, grading, review, and typed MCP contracts needed for a durable adaptive study loop.

## Upstream Dependencies

- Accepted Phase 0 handoff for objective manifest, source registry, learner profile, AWS safety policy, baseline summary, and seed-content admission schemas.
- All 20 stable task IDs: `AIP-1.1`–`AIP-1.6`, `AIP-2.1`–`AIP-2.5`, `AIP-3.1`–`AIP-3.4`, `AIP-4.1`–`AIP-4.3`, and `AIP-5.1`–`AIP-5.2`.
- Python 3.12, `uv` with committed lockfile, Pydantic v2, SQLite with FTS5, FastMCP local stdio transport, Ruff, and mypy.

## Out of Scope

- Streamlit course/lab workspace, timed mock UI, AWS resource mutation, hosted services, vector search, local LLM generation, and automated question authoring.
- The Phase 2 lab transport tools, except that core lab lifecycle ports and evidence semantics may be prepared as downstream contracts without exposing premature success.
- Certification readiness claims or replacement of official AWS preparation products.

## Glossary

- **Unanswered DTO:** Public question data structurally incapable of carrying answer or rubric fields.
- **Study core:** Transport-independent domain logic and repository contracts in `study_core`.
- **Idempotency ID:** Caller-provided identifier paired with a payload hash to make retries safe.
- **Committed evidence:** State durably written in SQLite before a success response.

## Requirements

### P1-R1 — Reproducible project and dependency boundaries

**User story:** As a maintainer, I want a reproducible Python project with enforced package direction so that the study core stays testable and transport-independent.

#### Acceptance Criteria

1. WHEN the project is installed from its committed lockfile, THE SYSTEM SHALL use Python 3.12 and exact dependency versions through `uv`.
2. WHEN modules are analyzed, THE SYSTEM SHALL enforce that `study_core` imports neither Streamlit, FastMCP, nor boto3 and that `app`, `study_mcp`, `study_aws`, and `scripts` depend inward on `study_core`.
3. WHEN a non-development dependency is added, THE SYSTEM SHALL document its purpose and pin its exact version.
4. IF an unsupported optional LLM, embedding, speech, OCR, queue, hosted database, vector database, container, or frontend dependency is introduced, THE SYSTEM SHALL fail the architecture validation gate.

### P1-R2 — Phase 0 contract ingestion

**User story:** As a study-core operator, I want Phase 0 artifacts validated and normalized so that objectives, sources, learner constraints, safety rules, and baseline data remain authoritative.

#### Acceptance Criteria

1. WHEN Phase 0 artifacts are ingested, THE SYSTEM SHALL validate schema versions and content with Pydantic v2 before any database write.
2. WHEN ingestion succeeds, THE SYSTEM SHALL preserve stable IDs, blueprint version, provenance, UTC timestamps, source freshness, learner unknowns, and safety-policy blocks.
3. IF any required artifact is incompatible, incomplete, or references an unknown objective, THE SYSTEM SHALL roll back the ingestion unit and report validation details.
4. WHEN ingestion is repeated with identical artifact versions, THE SYSTEM SHALL be idempotent and SHALL NOT duplicate objectives, sources, profile versions, or baseline records.
5. IF a later artifact conflicts with immutable historical references, THE SYSTEM SHALL preserve history and report a conflict rather than rewrite recorded attempts.

### P1-R3 — Versioned SQLite persistence

**User story:** As a learner, I want study state to survive process restarts so that sessions and progress are not dependent on chat or UI memory.

#### Acceptance Criteria

1. WHEN any SQLite connection is opened, THE SYSTEM SHALL enable foreign-key enforcement, use WAL mode where supported, configure an explicit busy timeout, and verify foreign keys are active.
2. WHEN migrations run, THE SYSTEM SHALL apply numbered forward migrations transactionally in order and record applied versions without mutating previously applied files.
3. WHEN the schema is initialized, THE SYSTEM SHALL support objectives, source registry, content, questions and separate answer material, sessions, session items, attempts, misconceptions, reviews, learner profiles, baseline records, idempotency events, and FTS5 search data.
4. IF a migration fails, THE SYSTEM SHALL roll it back, preserve the previous usable schema, and report the failing version.
5. WHEN timestamps are persisted, THE SYSTEM SHALL store timezone-aware UTC ISO 8601 values and stable string entity IDs.
6. IF a foreign-key or uniqueness invariant fails, THE SYSTEM SHALL reject the write and SHALL NOT silently coerce or orphan records.

### P1-R4 — Complete attributable seed bank

**User story:** As a learner, I want broad original scenario coverage so that adaptive practice never silently omits an exam task.

#### Acceptance Criteria

1. WHEN seed ingestion is accepted, THE SYSTEM SHALL contain at least two original scenario prompts for each of the 20 task IDs, totaling at least 40 prompts.
2. WHEN a question enters the usable bank, THE SYSTEM SHALL require objective IDs, source metadata, material scenario constraint, difficulty, format, review status, and separate answer/rubric data.
3. WHEN `next_question` returns an unanswered question, THE SYSTEM SHALL omit answer keys, rubrics, correct options, and distractor correctness metadata by construction.
4. IF a question lacks objective/source metadata, has invalid references, or is not admitted for its requested use, THE SYSTEM SHALL exclude it from selection and report content-health status.
5. WHERE a question is used for readiness scoring, THE SYSTEM SHALL require independent review status.

### P1-R5 — Durable session and adaptive selection

**User story:** As a learner, I want resumable focused sessions with traceable selection so that study adapts to due reviews and weaknesses without losing context.

#### Acceptance Criteria

1. WHEN `start_session` receives a valid learner, mode, objective/domain filters, and request ID, THE SYSTEM SHALL create or return one durable session with UTC start time and blueprint version.
2. WHEN `next_question` is requested, THE SYSTEM SHALL select only eligible, attributable questions and SHALL prioritize due reviews, weak objectives, and required coverage using deterministic rules with an injectable random source.
3. IF no eligible question exists, THE SYSTEM SHALL return a typed unavailable/content-gap error rather than fabricate a question or leak answer material.
4. WHEN a process restarts, THE SYSTEM SHALL resume the active session and preserve served items, completed attempts, and pending state.
5. WHEN the same mutating request ID is retried with the same payload, THE SYSTEM SHALL return the committed result without duplicate state; IF the payload differs, THE SYSTEM SHALL return a conflict.

### P1-R6 — Atomic grading, misconceptions, and spaced review

**User story:** As a learner, I want one truthful grading transaction so that my attempt, misconceptions, and review schedule can never disagree.

#### Acceptance Criteria

1. WHEN `grade_and_record` receives a served question, answer, confidence, elapsed time, and event ID, THE SYSTEM SHALL validate the payload and grade against answer material unavailable to the unanswered DTO.
2. WHEN grading commits, THE SYSTEM SHALL atomically write the attempt, update or resolve misconception state, and create or reschedule the review in one short transaction.
3. IF any part of the grading transaction fails, THE SYSTEM SHALL roll back all three effects and SHALL NOT report persistence or grading success.
4. WHEN confidence is recorded, THE SYSTEM SHALL preserve it independently from correctness for later calibration.
5. WHEN scheduling is computed, THE SYSTEM SHALL use deterministic domain logic with an injected timezone-aware clock and SHALL reject impossible state transitions.
6. IF grading cannot be determined from the rubric, THE SYSTEM SHALL return `grading_uncertain` without inventing correctness and SHALL preserve a reviewable record only if the complete transaction commits.

### P1-R7 — Reviews, progress, and truthfulness

**User story:** As a learner, I want due reviews and progress derived from committed evidence so that dashboards cannot overstate mastery.

#### Acceptance Criteria

1. WHEN `get_due_reviews` is called, THE SYSTEM SHALL return committed reviews due at or before the supplied UTC instant, ordered deterministically and filterable by objective/domain.
2. WHEN `get_progress` is called, THE SYSTEM SHALL report evidence-based accuracy, delayed recall, confidence calibration, repeated misconceptions, coverage gaps, and baseline context by task/domain.
3. WHEN an aggregate estimate is provided, THE SYSTEM SHALL label it as an internal estimate, expose its inputs, and SHALL NOT represent it as an AWS score prediction.
4. IF source coverage, question coverage, or independent review is incomplete, THE SYSTEM SHALL surface the gap rather than infer readiness.
5. IF no attempts exist, THE SYSTEM SHALL return an explicit empty-state result rather than zeros that imply measured performance.

### P1-R8 — Local source search with FTS5

**User story:** As a learner, I want fast attributable local search so that I can retrieve relevant material while offline.

#### Acceptance Criteria

1. WHEN source-attributed Markdown content is ingested, THE SYSTEM SHALL normalize metadata and index permitted searchable text in SQLite FTS5.
2. WHEN `search_local_material` receives a validated query, THE SYSTEM SHALL support objective and source/service metadata filters, deterministic pagination, snippets, attribution, retrieval date, and freshness status.
3. IF the query is malformed or exceeds configured limits, THE SYSTEM SHALL return a validation error without executing interpolated SQL.
4. WHEN no result matches, THE SYSTEM SHALL return an explicit empty result and SHALL NOT broaden security or objective filters silently.
5. WHILE offline, THE SYSTEM SHALL serve indexed local results without attempting an external request.

### P1-R9 — Typed FastMCP stdio adapter

**User story:** As a Kiro study client, I want narrow typed MCP tools so that study operations are deterministic without exposing raw storage or shell access.

#### Acceptance Criteria

1. WHEN the local FastMCP stdio server starts, THE SYSTEM SHALL expose exactly the Phase 1 tools `start_session`, `next_question`, `grade_and_record`, `get_due_reviews`, `get_progress`, and `search_local_material` from thin adapters over `study_core`.
2. WHEN a tool receives input or returns output, THE SYSTEM SHALL validate explicit Pydantic v2 request/response models and stable tool names.
3. WHEN a known failure occurs, THE SYSTEM SHALL map it to validation, conflict, unavailable dependency, authorization, not-found, persistence, or internal failure without leaking secrets or answer keys.
4. IF a caller requests SQL, filesystem, Python evaluation, AWS CLI, shell, or unrestricted database access, THE SYSTEM SHALL expose no such tool.
5. WHEN a mutating tool reports success, THE SYSTEM SHALL do so only after its database transaction commits.
6. IF stdio transport disconnects, THE SYSTEM SHALL preserve committed state and make uncommitted operations retry-safe through request/event IDs.

### P1-R10 — Security, privacy, and operational resilience

**User story:** As a learner, I want a secure offline-capable core so that local study does not expose credentials, private prompts, or answer material.

#### Acceptance Criteria

1. WHEN runtime data is created, THE SYSTEM SHALL place it under gitignored `data/` and SHALL keep credentials, secrets, recordings, transcripts, and databases out of version control.
2. WHEN logs are emitted, THE SYSTEM SHALL use structured non-sensitive identifiers and redact credentials, tokens, PII, full private prompts, answer keys, and sensitive retrieved text.
3. WHEN SQL is executed, THE SYSTEM SHALL use parameterized statements and bounded transactions.
4. WHILE AWS or network access is unavailable, THE SYSTEM SHALL keep all Phase 1 study, review, progress, and local-search operations usable.
5. IF the database is busy or unavailable, THE SYSTEM SHALL return a typed recoverable error after bounded handling and SHALL NOT silently discard a write.

### P1-R11 — Phase 1 exit gate

**User story:** As the project owner, I want an executable release gate so that UI work starts only after the local study loop is durable and safe.

#### Acceptance Criteria

1. WHEN Phase 1 is declared complete, THE SYSTEM SHALL demonstrate that a complete grill session survives process restart with no lost attempt data.
2. WHEN Phase 1 is declared complete, THE SYSTEM SHALL verify that no question can be selected without objective and source metadata.
3. WHEN Phase 1 is declared complete, THE SYSTEM SHALL verify that unanswered question responses cannot contain answer keys or grading rubrics.
4. WHEN Phase 1 is declared complete, THE SYSTEM SHALL verify the minimum 40-prompt seed bank covers every one of the 20 task IDs with at least two original scenarios.
5. IF any gate fails, THE SYSTEM SHALL emit blocking evidence and SHALL NOT mark the phase accepted.
6. WHEN all gates pass, THE SYSTEM SHALL publish the stable core/API handoff consumed by Phase 2, including reserved lab lifecycle and read-only validator interfaces without falsely claiming they are already verified.
