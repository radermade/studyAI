# Requirements Document

## Introduction

**Title:** Phase 8 — Exam Simulation and Readiness Closure

**Status:** Proposed

**Scope:** Deliver secure, durable, blueprint-weighted 75-question MCQ/MR mock sessions, the `/aip-mock` coaching skill, weakness-directed closure, and an evidence-based final readiness review spanning all 20 AIP-C01 tasks.

## Upstream dependencies

- Phase 0 locked blueprint/source registry, learner profile, exam date, baseline, and safety policy.
- Phase 1 durable questions, attempts, sessions, misconceptions, reviews, progress, and answer-key separation.
- Phase 2 Mock/Review/Progress UI, durable resume, accessibility, and delayed-feedback behavior.
- Phase 3 accepted coverage for `AIP-1.1`–`AIP-1.6` and Labs 1–4.
- Phase 4 accepted coverage for `AIP-2.1`–`AIP-2.5` and Labs 6–7.
- Phase 5 accepted coverage for `AIP-3.1`–`AIP-3.4` and Labs 5 and 8.
- Phase 6 accepted coverage for `AIP-4.1`–`AIP-4.3` and Labs 9–10.
- Phase 7 accepted coverage for `AIP-5.1`–`AIP-5.2` and Labs 11–12.

Absent or failed upstream gates SHALL remain visible blockers. Phase 8 does not certify upstream work by assumption.

## Out of scope

- Predicting AWS scaled scores, pass probability, or certification outcome.
- Exam dumps, recalled live exam content, copied proprietary practice questions, or automated acquisition of official results.
- Immediate correctness, hints, sources, objective labels, or answer explanations during an active mock.
- Scheduling or purchasing an examination on the learner’s behalf.

## Glossary

- **Fresh form:** A mock whose items and equivalence families have not been exposed to the learner.
- **Readiness:** A transparent internal study estimate, not an AWS score or outcome prediction.
- **MR:** A multiple-response item requiring the declared number of selections.

## Requirements

### P8-R1 — Complete 20-task blueprint and source integrity

**User story:** As a learner, I want every exam task represented by reviewed material so that mock performance cannot hide a coverage gap.

#### Acceptance criteria

1. THE SYSTEM SHALL require accepted source and question coverage for exactly these 20 tasks: `AIP-1.1`, `AIP-1.2`, `AIP-1.3`, `AIP-1.4`, `AIP-1.5`, `AIP-1.6`, `AIP-2.1`, `AIP-2.2`, `AIP-2.3`, `AIP-2.4`, `AIP-2.5`, `AIP-3.1`, `AIP-3.2`, `AIP-3.3`, `AIP-3.4`, `AIP-4.1`, `AIP-4.2`, `AIP-4.3`, `AIP-5.1`, and `AIP-5.2`.
2. WHEN a question enters a mock-eligible pool, THE SYSTEM SHALL require exact objective IDs, difficulty, MCQ or MR format, meaningful scenario constraints, source references/freshness, separate answer/rubric, every-option rationale, and independent review.
3. IF a source is stale, objective mapping is invalid, review is incomplete, or licensing/provenance is unacceptable, THEN THE SYSTEM SHALL exclude the question from mock selection and report the coverage deficit.
4. THE SYSTEM SHALL distinguish AWS-documented facts, project recommendations, and learner notes and SHALL NOT admit exam dumps or unsupported absolute claims.
5. THE SYSTEM SHALL revalidate the active exam code and blueprint version before readiness closure and SHALL invalidate incompatible mock blueprints rather than silently remap them.

### P8-R2 — Blueprint-weighted 75-question assembly

**User story:** As a learner, I want full mocks to reflect the published domain emphasis while still covering every domain.

#### Acceptance criteria

1. WHEN a full mock is assembled, THE SYSTEM SHALL select exactly 75 eligible questions using target weights Domain 1 `31%`, Domain 2 `26%`, Domain 3 `20%`, Domain 4 `12%`, Domain 5 `11%`.
2. THE SYSTEM SHALL use a documented largest-remainder allocation of 23/20/15/9/8 questions for Domains 1/2/3/4/5 respectively, totaling 75 and minimizing integer rounding error.
3. THE SYSTEM SHALL include both multiple-choice and multiple-response behavior according to reviewed item metadata and SHALL clearly state the number of selections required for MR items without revealing correctness.
4. THE SYSTEM SHALL distribute questions across all 20 tasks subject to pool capacity and SHALL block assembly with an explicit deficit if any task lacks eligible coverage.
5. WHEN multiple mocks are assembled, THE SYSTEM SHALL use deterministic seeded selection for auditability while preventing the seed, keys, and selection internals from learner-visible state during the session.
6. THE SYSTEM SHALL prevent duplicate questions within a mock and materially equivalent duplicates across the two readiness mocks.

### P8-R3 — Timed, durable, delayed-feedback mock session

**User story:** As a learner, I want a realistic timed session that survives interruption so that performance reflects exam execution rather than UI failures.

#### Acceptance criteria

1. WHEN a learner starts a mock, THE SYSTEM SHALL persist the immutable form, blueprint version, start/deadline timestamps in UTC, per-item order, and session status before rendering the first item.
2. THE SYSTEM SHALL enforce one configured full-session time limit, display remaining time accessibly, record answer changes, confidence, elapsed time, unanswered status, and final submission transactionally.
3. DURING an active mock, THE SYSTEM SHALL hide correctness, explanations, hints, sources, objective IDs, rubrics, aggregate score, and answer keys.
4. IF the app reruns or restarts, THEN THE SYSTEM SHALL restore the durable session and compute remaining time from persisted timestamps rather than reset the timer.
5. WHEN time expires, THE SYSTEM SHALL atomically finalize recorded answers and mark unanswered items; IF finalization fails, THEN THE SYSTEM SHALL not display a result until recovery commits.
6. WHEN the learner submits, THE SYSTEM SHALL prevent further answer mutation and only then make grading and feedback eligible.

### P8-R4 — Correct grading and post-submission feedback

**User story:** As a learner, I want accurate delayed feedback so that I can learn from mistakes without contaminating the live simulation.

#### Acceptance criteria

1. WHEN a submitted mock is graded, THE SYSTEM SHALL apply reviewed MCQ/MR scoring rules consistently and record overall, domain, task, confidence-calibration, timing, and unanswered metrics.
2. THE SYSTEM SHALL grade and record attempts, update misconceptions, and reschedule reviews in one transaction per graded attempt/event.
3. AFTER successful finalization and grading, THE SYSTEM SHALL show decisive requirements, correct reasoning, distractor analysis, primary sources, and targeted follow-up without exposing private authoring notes.
4. IF grading data is missing, conflicting, or unreviewed, THEN THE SYSTEM SHALL mark the item unscorable, exclude it from denominators, flag the form for review, and SHALL NOT fabricate a result.
5. THE SYSTEM SHALL preserve the submitted form and grading-version provenance so later question edits do not rewrite historical results.

### P8-R5 — `/aip-mock` skill and safe interfaces

**User story:** As a learner using Kiro, I want a dedicated mock skill so that I can start, resume, submit, and review simulations through stable operations.

#### Acceptance criteria

1. THE SYSTEM SHALL provide `/aip-mock` with operations to check eligibility, start or resume a mock, present an answer-safe question, record an answer/confidence, submit, and retrieve post-submission results.
2. THE SKILL SHALL coordinate typed core use cases and SHALL NOT contain selection, timing, grading, readiness, or persistence rules.
3. THE SKILL SHALL NOT expose raw SQL, filesystem, shell, Python evaluation, answer keys, hidden objectives during a mock, or unrestricted AWS tools.
4. WHEN a mutating operation is replayed with the same request/event ID and payload, THE SYSTEM SHALL return the committed result; a mismatched replay SHALL return a conflict.
5. THE SYSTEM SHALL distinguish validation, conflict, unavailable dependency, expired session, authorization, persistence, and internal failures without claiming success before commit.

### P8-R6 — Freshness and two-mock readiness thresholds

**User story:** As a learner, I want readiness based on fresh forms so that memorized practice does not masquerade as mastery.

#### Acceptance criteria

1. THE SYSTEM SHALL classify a readiness question as fresh only when it and any materially equivalent variant have not been exposed to the learner in practice, review, lab, prior mock, authoring, or feedback.
2. THE SYSTEM SHALL reserve two independently reviewed full forms with disjoint/materially non-equivalent questions and SHALL prevent preview before use.
3. FOR EACH of the two readiness mocks, THE SYSTEM SHALL require at least `85%` overall and at least `80%` in each of the five domains.
4. IF either form fails any overall or domain threshold, contains an invalid item that compromises the allocated form, or is not fresh, THEN THE SYSTEM SHALL not satisfy the readiness gate and SHALL prescribe remediation before another fresh attempt.
5. THE SYSTEM SHALL retain form/version/freshness evidence sufficient to audit both threshold decisions without exposing reserved content.

### P8-R7 — Weakness-directed review and misconception closure

**User story:** As a learner, I want a focused remediation plan so that errors, overconfidence, slow reasoning, and missing lab evidence lead to specific work.

#### Acceptance criteria

1. AFTER mock grading, THE SYSTEM SHALL generate prioritized review actions from incorrect/unanswered items, task/domain accuracy, confidence error, elapsed time, repeated misconceptions, delayed recall, source freshness, and lab evidence.
2. THE SYSTEM SHALL identify high-priority misconceptions using versioned severity rules and link each to evidence, objective IDs, due review, and closure criterion.
3. THE SYSTEM SHALL require no unresolved high-priority misconception before readiness closure.
4. WHEN a misconception is closed, THE SYSTEM SHALL require successful delayed recall or fresh evidence; viewing an explanation or self-report alone SHALL NOT close it.
5. THE SYSTEM SHALL distinguish independent versus hint-assisted lab completion and SHALL not treat assisted proof as independent mastery without later unaided evidence.

### P8-R8 — Required lab and cleanup matrix closure

**User story:** As a learner, I want all hands-on evidence and cleanup verified so that readiness includes practical competence and account hygiene.

#### Acceptance criteria

1. THE SYSTEM SHALL require accepted proof for all roadmap-required Labs 1 through 12, including their exact objective mappings and proof artifacts.
2. THE SYSTEM SHALL require every applicable lab checkpoint to have valid committed evidence and every learner-created chargeable resource to have verified cleanup evidence.
3. THE SYSTEM SHALL NOT infer `Verified` from a click, navigation, screenshot, self-report, or truthy value; successful validator evidence is required.
4. THE SYSTEM SHALL NOT infer `Cleaned up` from an attempted deletion or screenshot; verified absence or terminal deletion state is required.
5. IF AWS is unavailable or authorization fails, THEN THE SYSTEM SHALL retain the checkpoint as blocked/self-reported as applicable and SHALL NOT waive the cleanup gate.

### P8-R9 — Readiness reporting, privacy, safety, and evidence

**User story:** As a learner, I want a transparent readiness summary that protects my data and does not overclaim what internal metrics mean.

#### Acceptance criteria

1. THE SYSTEM SHALL label readiness as an internal estimate and SHALL NOT present it as an AWS score, scaled-score prediction, pass probability, or guarantee.
2. THE SYSTEM SHALL expose the estimate inputs: two mock results, per-domain/task accuracy, confidence calibration, speed/unanswered rate, delayed recall, misconception status, lab independence/evidence, cleanup, and source/blueprint freshness.
3. WHEN mock or gate state changes, THE SYSTEM SHALL persist stable IDs, UTC timestamps, provenance, versions, and event IDs transactionally before showing success.
4. THE SYSTEM SHALL redact credentials, PII, private notes/prompts, answer keys, reserved items, and sensitive AWS content from logs, exports, and browser-visible state.
5. THE SYSTEM SHALL remain useful offline except for official resources/AWS labs and SHALL not transmit learner history or private data externally without explicit direction.
6. IF required evidence is missing or contradictory, THEN THE SYSTEM SHALL show `Not ready` or `Evidence incomplete` with blockers rather than interpolate a positive estimate.

### P8-R10 — Official practice result and residual-risk review

**User story:** As a learner, I want to incorporate the official practice exam and remaining risks so that my final scheduling decision is informed but remains mine.

#### Acceptance criteria

1. THE SYSTEM SHALL allow the learner to record an official AWS practice exam completion date, result/score as reported, optional domain feedback, provenance note, and consented minimal evidence without storing credentials or scraping protected content.
2. THE SYSTEM SHALL label the official result as externally reported and SHALL not treat it as locally verified unless a supported verification method exists.
3. WHEN final review is requested, THE SYSTEM SHALL combine official result, internal evidence, source freshness, unresolved low-priority risks, exam timing, and known limitations into a residual-risk review.
4. THE SYSTEM SHALL require the official practice result and residual-risk review before final readiness closure, but SHALL leave the exam scheduling/sitting decision to the learner.
5. THE SYSTEM SHALL not store official exam questions, answer recollections, or proprietary report content beyond minimal learner-entered outcome metadata.

### P8-R11 — Exact Phase 8 exit gate and handoff

**User story:** As the program owner, I want an exact final gate so that readiness closure is auditable and optional enhancements cannot redefine success.

#### Acceptance criteria

1. THE SYSTEM SHALL require two fresh 75-question mocks, each at least 85% overall and 80% in every domain.
2. THE SYSTEM SHALL require no unresolved high-priority misconception.
3. THE SYSTEM SHALL require all Labs 1–12 proof complete and all applicable cleanup verified.
4. THE SYSTEM SHALL require current coverage of all 20 AIP tasks and a current blueprint/source review.
5. THE SYSTEM SHALL require the official practice result and documented residual-risk review.
6. IF any criterion fails, THEN THE SYSTEM SHALL keep readiness open and emit prioritized remediation without predicting an AWS outcome.
7. WHEN all criteria pass, THE SYSTEM SHALL persist a versioned readiness-closure record with evidence references, limitations, and learner acknowledgment.
8. Phase 9 optional enhancements SHALL NOT be prerequisites for, alter, or retroactively invalidate this gate unless a future blueprint change invalidates the underlying evidence.
