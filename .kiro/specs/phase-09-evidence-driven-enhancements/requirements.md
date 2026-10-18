# Requirements Document

## Introduction

**Title:** Phase 9 — Evidence-Driven Optional Enhancements

**Status:** Proposed, optional, dormant by default

**Scope:** Provide an admission and acceptance framework for six independently selectable enhancements: local speech/oral mode, hybrid retrieval, source-freshness automation, screenshot assistance, local question drafting, and calendar/readiness forecasting. No enhancement is selected by default, and none is required for Phase 8 readiness closure.

## Upstream dependencies

- A functioning Phase 1 local-first core and Phase 2 UI contracts.
- The specific baseline subsystem and evidence required by an enhancement.
- Phase 8 closure or a documented decision that the enhancement does not delay Phase 0–8 study delivery.
- Current dependency/security policy, source/question/lab contracts, and data retention rules.

## Out of scope

- Making any enhancement a prerequisite for Phase 8 or certification readiness.
- Cloud speech, hosted embeddings/vector services, external question generation, or transfer of source code, learner history, private AWS data, recordings, screenshots, or content without separate explicit authorization.
- Screenshot-only verification or cleanup proof.
- Automatic admission based on novelty, preference alone, or an unmeasured assumption.
- Installing optional LLM, embedding, speech, OCR, or calendar packages during the MVP.

## Admission threshold defaults

Thresholds are versioned defaults and may be changed only by an approved decision record before measurement, never after results are seen:

| Enhancement | Measured-need default |
|---|---|
| Local speech/oral | An accessibility need explicitly selected by the learner, or median typed-answer time/friction prevents the target study mode in at least 3 of 5 measured sessions |
| Hybrid retrieval | Reviewed FTS5 benchmark has recall@5 `< 0.85` or MRR `< 0.75` on at least 50 representative queries, and metadata/query tuning cannot close the gap |
| Source freshness | More than 5% of active sources breach the configured freshness SLA in two audits, or manual freshness work exceeds 2 hours/month for two months |
| Screenshot assistance | At least 20% of eligible checkpoint attempts across at least 20 attempts have evidence-orientation ambiguity that a screenshot annotation trial can reduce; screenshots remain non-verifying |
| Local question drafting | Reviewed-question supply is at least 20% below the Phase 8 fresh-pool/replenishment plan in two consecutive review cycles despite template/process improvements |
| Calendar forecast | Two or more weekly target misses in a rolling four-week period, or remaining planned effort exceeds available pre-exam capacity under the existing learner profile |

## Glossary

- **Admission:** Approval to trial one optional enhancement after measured need and boundary reviews pass.
- **Dormant:** Unselected, disabled, dependency-free optional state.
- **Baseline path:** The pre-enhancement behavior retained for comparison and rollback.

## Requirements

### P9-R1 — Independent admission governance

**User story:** As the product owner, I want optional work admitted only by measured need so that enhancements do not delay core study outcomes or add unjustified risk.

#### Acceptance criteria

1. THE SYSTEM SHALL represent each enhancement as `Dormant`, `Measuring`, `Admitted`, `Rejected`, `Trial`, `Accepted`, `Rolled back`, or `Retired`, independently of every other enhancement.
2. BEFORE an enhancement becomes `Admitted`, THE SYSTEM SHALL require a versioned baseline, predeclared threshold, representative measurement window/sample, user impact, privacy/data-flow review, security review, cost/budget estimate, dependency/license/maintenance review, offline impact, rollback plan, and named decision owner.
3. IF measured need does not meet the predeclared threshold, expected benefit cannot be tested, Phase 0–8 work would be delayed, or privacy/safety/cost risk is unacceptable, THEN THE SYSTEM SHALL reject or defer that enhancement without affecting any other enhancement.
4. THE SYSTEM SHALL keep all six enhancements unselected by default and SHALL NOT install or activate dependencies for a dormant/rejected enhancement.
5. WHEN an admission decision changes, THE SYSTEM SHALL persist its evidence, rationale, UTC timestamp, policy version, and approver transactionally before activation.
6. Admission of one enhancement SHALL NOT imply admission, implementation, acceptance, or dependency installation for another.

### P9-R2 — Shared optional dependency and experiment controls

**User story:** As a maintainer, I want optional experiments isolated and reversible so that local-first reliability and the approved architecture remain intact.

#### Acceptance criteria

1. WHEN an enhancement is admitted and needs a dependency, THE SYSTEM SHALL document necessity, review package identity/license/security/maintenance, pin the exact version, update and commit `uv.lock`, and isolate the dependency to the selected feature path.
2. THE SYSTEM SHALL prefer the Python standard library and existing dependencies and SHALL NOT add a frontend framework, separate API server, hosted database, queue, container platform, or vector database without a separately measured and approved requirement.
3. BEFORE a trial starts, THE SYSTEM SHALL define baseline/candidate metrics, acceptance and rollback thresholds, time/sample/cost bounds, retention/deletion behavior, and affected users/data.
4. IF a trial breaches safety, privacy, quality, cost, or reliability floors, THEN THE SYSTEM SHALL stop or roll back it and preserve non-sensitive evidence.
5. THE SYSTEM SHALL store recordings, screenshots, transcripts, derived media, and runtime indexes under gitignored `data/` with explicit retention and deletion controls.
6. THE SYSTEM SHALL not transmit project code, credentials, learner history, private AWS data, or private content to external services without explicit user direction and a new approved boundary review.

### P9-R3 — Optional local speech-to-text and oral answer mode

**User story:** As a learner with measured typing/accessibility friction, I want an optional local oral mode so that I can practice explanations without surrendering private recordings.

#### Acceptance criteria

1. WHERE speech/oral mode is independently `Admitted`, THE SYSTEM SHALL process audio locally, disclose model/dependency size and offline capability, and obtain explicit opt-in before microphone capture.
2. THE SYSTEM SHALL show and allow editing of a transcript before submission and SHALL treat transcript confirmation—not raw recognition—as the learner answer.
3. THE SYSTEM SHALL measure word/error correction rate, completion rate, median answer time, oral-rubric outcome, and learner-reported usability against the typed baseline over the admitted sample.
4. THE SYSTEM SHALL accept the enhancement only if the admission friction is reduced by at least 20% or the documented accessibility need is satisfied, while answer quality does not fall more than 5 percentage points and privacy/reliability floors pass.
5. THE SYSTEM SHALL default to no recording retention; IF retention is explicitly enabled, THEN it SHALL use `data/`, show retention duration, and support deletion of audio and transcript derivatives.
6. IF local speech is unavailable or confidence is low, THEN THE SYSTEM SHALL offer typed fallback without losing durable study state or silently submitting text.

### P9-R4 — Optional hybrid lexical/vector retrieval

**User story:** As a learner experiencing measured FTS5 misses, I want optional hybrid retrieval so that relevant local sources are easier to find without replacing the source of truth.

#### Acceptance criteria

1. WHERE hybrid retrieval is independently `Admitted`, THE SYSTEM SHALL retain SQLite/FTS5 plus metadata filtering as the baseline and source of truth and SHALL treat any vector index as rebuildable local derived data.
2. THE SYSTEM SHALL evaluate the same reviewed query set using recall@5, MRR, nDCG where labels support it, latency p95, index size/build time, citation/source correctness, and metadata/tenant filtering.
3. THE SYSTEM SHALL accept hybrid retrieval only if recall@5 improves by at least 10% relative or reaches `0.90`, no required metadata/tenant result regresses, p95 remains within the declared interactive budget, and privacy/cost floors pass.
4. WHEN content changes or is deleted, THE SYSTEM SHALL update or rebuild derived vectors and prove deleted/private content is absent from retrieval.
5. THE SYSTEM SHALL use local exact-pinned embedding dependencies/models approved during admission and SHALL NOT call an external embedding service without separate explicit authorization.
6. IF the vector component is unavailable or stale, THEN THE SYSTEM SHALL degrade to FTS5 and visibly report retrieval mode/freshness rather than return silent partial results.

### P9-R5 — Optional source-freshness automation

**User story:** As a content maintainer with measured freshness burden, I want bounded freshness checks so that stale source risk is detected without silently rewriting authored material.

#### Acceptance criteria

1. WHERE freshness automation is independently `Admitted`, THE SYSTEM SHALL check only registered source URLs using bounded timeouts/rates and record checked-at, status, redirect/change signals, retrieval errors, and review-needed state.
2. THE SYSTEM SHALL NOT automatically replace human-authored lesson/question/lab claims or mark changed content current without review.
3. THE SYSTEM SHALL accept the enhancement only if freshness-SLA breaches or manual effort improve by at least 50% over the baseline, false-positive review rate is at most 10%, and no source access/privacy/cost policy is violated.
4. IF a source is unavailable, redirected across origin, materially changed, or outside policy, THEN THE SYSTEM SHALL preserve the last-known metadata, mark it stale/review-needed, and exclude affected scored content where existing contracts require.
5. Network refresh SHALL be an explicit deterministic maintenance action, not a save hook, and the application SHALL remain useful offline.

### P9-R6 — Optional screenshot-assisted checkpoint evidence

**User story:** As a learner confused about what evidence to inspect, I want local screenshot assistance so that I can orient to a checkpoint while validators remain authoritative.

#### Acceptance criteria

1. WHERE screenshot assistance is independently `Admitted`, THE SYSTEM SHALL require explicit file selection/consent, local processing, visible redaction guidance, and gitignored `data/` storage with retention/deletion controls.
2. THE SYSTEM SHALL label screenshot output as `Assistive` or `Self-reported` only and SHALL NOT use a screenshot, OCR result, visual match, or model interpretation to confer `Verified` or `Cleaned up`.
3. Verification SHALL continue to require successful allowlisted read-only validator evidence; cleanup SHALL continue to require verified absence or terminal deletion state.
4. THE SYSTEM SHALL accept screenshot assistance only if ambiguity falls by at least 30% relative on the admitted trial, false guidance is at most 5%, task completion does not regress, and sensitive-data/privacy checks pass.
5. IF sensitive content is detected or suspected, THEN THE SYSTEM SHALL block analysis/export until the learner redacts or deletes the image; credentials and secrets SHALL never be persisted in derived text.
6. IF OCR/assistance is unavailable, THEN THE SYSTEM SHALL preserve the checkpoint and offer manual instructions without changing evidence state.

### P9-R7 — Optional local question-drafting pipeline

**User story:** As a content author facing a measured fresh-question shortage, I want local drafting assistance so that review capacity is focused without lowering bank integrity.

#### Acceptance criteria

1. WHERE question drafting is independently `Admitted`, THE SYSTEM SHALL operate locally on approved source-attributed material and produce drafts outside the scored bank with `Draft` status.
2. A draft SHALL include objective IDs, source references, meaningful scenario constraint, difficulty/format, separate proposed key/rubric, every-option rationale, uncertainty flags, and generation provenance.
3. THE SYSTEM SHALL prohibit a draft from becoming scored/mock-eligible until source checks, duplication/equivalence checks, safety/licensing review, and independent human review pass.
4. THE SYSTEM SHALL accept the enhancement only if independently accepted draft throughput improves by at least 25% over baseline, reviewer time per accepted item does not increase, rejection reasons are tracked, and zero unreviewed generated items enter scored pools.
5. THE SYSTEM SHALL prevent source text, answer keys, private content, and learner history from being sent to external drafting services without separate explicit authorization.
6. IF drafting quality or duplication fails the declared floor, THEN THE SYSTEM SHALL stop admission to the bank, retain only approved non-sensitive evaluation evidence, and support rollback/removal of generated drafts.

### P9-R8 — Optional calendar integration and readiness forecast

**User story:** As a learner with measured schedule risk, I want an optional forecast so that I can adjust study capacity without mistaking a plan for a guaranteed outcome.

#### Acceptance criteria

1. WHERE calendar/forecast is independently `Admitted`, THE SYSTEM SHALL default to a local schedule using learner-entered availability and SHALL require separate opt-in and boundary review before connecting an external calendar.
2. THE SYSTEM SHALL calculate forecast inputs from remaining objectives/reviews/labs, historical completion pace, available weekly capacity, exam date, uncertainty, and blockers; THE SYSTEM SHALL label output as a planning estimate, not an AWS score or pass prediction.
3. THE SYSTEM SHALL accept the enhancement only if four-week rolling plan error is at most 20% after the minimum trial window or missed-target rate improves by at least 25%, while privacy and usability floors pass.
4. WHEN source data changes, THE SYSTEM SHALL show forecast-as-of time, assumptions, uncertainty range, and reasons for material schedule changes.
5. THE SYSTEM SHALL practice data minimization for calendar details and SHALL NOT persist unrelated event titles, attendees, locations, or descriptions.
6. IF calendar access is unavailable or revoked, THEN THE SYSTEM SHALL fall back to learner-entered availability and preserve study state.

### P9-R9 — Per-enhancement acceptance, rollback, and handoff

**User story:** As the program owner, I want each optional enhancement judged independently so that useful additions can ship without making the entire optional backlog mandatory.

#### Acceptance criteria

1. WHEN an admitted trial ends, THE SYSTEM SHALL compare candidate and baseline against that enhancement’s acceptance, privacy, safety, cost, dependency, reliability, and rollback criteria.
2. IF criteria pass, THEN THE SYSTEM SHALL mark only that enhancement `Accepted` and emit a versioned handoff with evidence, exact pins/lock changes if any, operating limits, retention, and known risks.
3. IF criteria fail or evidence is insufficient, THEN THE SYSTEM SHALL mark only that enhancement `Rolled back`, `Rejected`, or continue `Trial` as justified and restore the baseline path.
4. THE SYSTEM SHALL allow Phase 9 to remain dormant, to end after one accepted enhancement, or to contain any independently admitted subset; unselected enhancements SHALL remain optional and incomplete without being blockers.
5. Acceptance or rollback SHALL NOT alter historical Phase 8 readiness evidence or its gate, except that a separately detected blueprint/source invalidation is handled by the existing readiness freshness contract.
6. THE SYSTEM SHALL run targeted tests plus Ruff, Ruff format check, and mypy for every implemented enhancement and retain acceptance results.
