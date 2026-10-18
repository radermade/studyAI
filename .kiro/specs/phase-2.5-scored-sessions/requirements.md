# Requirements Document

## Introduction

**Title:** Phase 2.5 — Scored Sessions, Scoring, and Session Management

**Status:** Proposed

**Scope:** Deliver AWS-style scored sessions pulled forward from Phase 8: officially
weighted question selection, exam-accurate grading mechanics, a transparent scaled-score
estimate, delayed feedback, review of missed items, session reset, and session history.
The capability must be usable with the content that exists today (Domain 1 only) and scale
automatically to the full 75-question exam structure as content grows, with no code change.

## Upstream dependencies

- Phase 1 durable SQLite core, sessions/attempts/misconceptions/reviews, typed study
  service, and answer-key separation.
- Phase 2 Streamlit workspace (focused four-view app: Grill, Labs, Review, Progress) and
  the thread-safe runtime.
- Authored questions with objective IDs, options, correct answers, per-option rationales,
  and explanations (Domain 1 exists; more domains arrive in Phases 3-7).

## Out of scope

- The Phase 8 readiness gate (two fresh full mocks, misconception closure, lab matrix,
  official-practice/residual-risk review). Phase 2.5 provides the scored-session engine
  that Phase 8 reuses.
- Reproducing AWS's proprietary scaled-scoring algorithm. The platform computes a
  transparent internal estimate only.
- Reproducing or importing official exam questions, recalled items, or dumps.

## Glossary

- **Scored session:** A delayed-feedback session whose questions are selected by official
  domain weighting and graded under AIP-C01 mechanics.
- **Scored item / unscored item:** A scored item affects the result; an unscored item is
  mixed in unmarked and does not affect the result (models AWS pretest items).
- **Scaled-score estimate:** A transparent internal 100-1000 estimate derived from the raw
  correct count. It is explicitly not an AWS scaled score.
- **Compensatory scoring:** Overall pass/fail; per-domain results are informational only.
- **Full-length session:** 75 questions (65 scored + 10 unscored) across all five domains.

## Requirements

### P2.5-R1 — Official-weighted question selection

**User story:** As a learner, I want scored-session questions chosen the way the real exam
weights its domains so that practice reflects the actual test.

#### Acceptance criteria

1. WHEN a full-length scored session is assembled, THE SYSTEM SHALL select exactly 65
   scored questions distributed across domains by largest-remainder rounding of the
   official weights 31/26/20/12/11, yielding 20/17/13/8/7.
2. WHEN a full-length scored session is assembled, THE SYSTEM SHALL additionally include 10
   unscored questions at randomized, unmarked positions that do not affect the score.
3. WHEN questions are selected, THE SYSTEM SHALL choose randomly within each domain bucket
   with no repeated question in a single session.
4. WHERE one or more domains lack sufficient authored questions, THE SYSTEM SHALL scale the
   session to the available or selected domains while preserving the official relative
   weighting among them, and SHALL label the session "not full-length."
5. WHILE the pool is too small to supply 65 scored plus 10 unscored items, THE SYSTEM SHALL
   set the unscored count to 0 and compute the scored count from available capacity.
6. IF no domain has sufficient reviewed questions to form a session, THEN THE SYSTEM SHALL
   return a typed content-gap result rather than an empty or misleading session.

### P2.5-R2 — Domain scope selection

**User story:** As a learner, I want to choose which domains a scored session covers so I
can drill into what I have studied.

#### Acceptance criteria

1. WHEN starting a scored session, THE SYSTEM SHALL default scope to all domains that
   currently have reviewed questions.
2. WHEN the learner selects a subset of domains, THE SYSTEM SHALL restrict selection to
   those domains and preserve the official relative weighting among them.
3. IF a selected domain has no reviewed questions, THEN THE SYSTEM SHALL exclude it and
   report which domains were excluded.

### P2.5-R3 — Exam-accurate grading mechanics

**User story:** As a learner, I want grading to match the real exam so my score is
meaningful.

#### Acceptance criteria

1. WHEN a multiple-choice item is graded, THE SYSTEM SHALL mark it correct only if the one
   selected option equals the one correct option.
2. WHEN a multiple-response item is graded, THE SYSTEM SHALL mark it correct only if the
   selected set equals the full correct set (all-or-nothing, no partial credit).
3. WHEN an item is left unanswered at submission, THE SYSTEM SHALL score it as incorrect.
4. THE SYSTEM SHALL apply no penalty for guessing beyond scoring a wrong or unanswered item
   as incorrect.
5. WHEN the result is computed, THE SYSTEM SHALL count only scored items toward the score
   and SHALL exclude unscored items from all score totals.

### P2.5-R4 — Transparent scaled-score estimate and pass/fail

**User story:** As a learner, I want a clear score and pass/fail that I understand is an
estimate, not an official AWS score.

#### Acceptance criteria

1. WHEN a scored session is submitted, THE SYSTEM SHALL report raw correct count, scored
   total, and percentage over scored items.
2. THE SYSTEM SHALL compute a transparent internal scaled-score estimate on a 100-1000
   scale from the scored percentage using a documented, deterministic linear mapping.
3. THE SYSTEM SHALL report pass or fail against a 750-equivalent threshold and SHALL label
   the result an internal estimate, explicitly not an official AWS scaled score.
4. THE SYSTEM SHALL present per-domain correct/total as informational strengths and
   weaknesses and SHALL NOT impose per-domain pass gates (compensatory scoring).
5. WHERE the session was not full-length, THE SYSTEM SHALL label the estimate as derived
   from a reduced session and caution against over-interpreting it.

### P2.5-R5 — Delayed feedback

**User story:** As a learner, I want a scored session to feel like an exam, with no answers
revealed until I finish.

#### Acceptance criteria

1. WHILE a scored session is in progress, THE SYSTEM SHALL NOT reveal correctness, correct
   options, rationales, explanations, or the running score.
2. WHILE a scored session is in progress, THE SYSTEM SHALL allow navigating among items and
   changing answers before submission.
3. WHEN the learner submits, THE SYSTEM SHALL freeze all answers, grade the session, and
   only then make feedback and the score available.
4. WHEN time expires on a timed session, THE SYSTEM SHALL auto-submit, scoring unanswered
   items as incorrect.
5. THE SYSTEM SHALL keep answer material out of any browser-visible state during the
   session.

### P2.5-R6 — Single-session, non-accumulating state

**User story:** As a learner, I want temporary, measurable results for my current session,
not an accumulating archive, while not losing an exam to a refresh.

#### Acceptance criteria

1. WHEN the learner resets or abandons the active scored session, THE SYSTEM SHALL discard
   its state and allow a fresh session to start.
2. WHEN a new scored session is started, THE SYSTEM SHALL clear any prior scored-session
   data for the learner so that at most one scored session (in-progress or most-recent
   result) exists at a time.
3. THE SYSTEM SHALL NOT maintain a long-term history of past scored sessions; the platform
   exposes no archive or list of previous sessions.
4. THE SYSTEM SHALL persist the single current session (in-progress or most-recent result)
   through SQLite only so that a browser refresh or app rerun does not lose it mid-exam or
   immediately after submission.
5. IF a persistence operation fails, THEN THE SYSTEM SHALL report a recoverable error and
   SHALL NOT display a success or a fabricated score.

### P2.5-R7 — Review of missed items

**User story:** As a learner, I want Review to show exactly what I missed so I can study
my weak spots.

#### Acceptance criteria

1. WHEN a scored session is submitted, THE SYSTEM SHALL record each incorrect or unanswered
   scored item as a reviewable miss linked to its objective.
2. WHEN the learner opens Review, THE SYSTEM SHALL list the missed items from the most
   recent scored session with each item's correct answer, rationale, and explanation.
3. THE SYSTEM SHALL continue to surface spaced-repetition review items from grill history
   alongside scored-session misses.
4. THE SYSTEM SHALL group or summarize misses by objective so weak objectives are visible.

### P2.5-R8 — Original terminal/ASCII aesthetic (accessible)

**User story:** As a learner, I want a fun terminal-style score readout that is still easy
to read.

#### Acceptance criteria

1. WHEN a scored result is shown, THE SYSTEM SHALL render an original monospace/ASCII-style
   score banner and summary.
2. THE SYSTEM SHALL convey all status and result meaning through text and icons, never
   color or ASCII art alone, and SHALL preserve WCAG 2.2 AA contrast.
3. THE SYSTEM SHALL provide an accessible text equivalent for any ASCII-art banner.
4. THE SYSTEM SHALL use only original art and styling with no copied logos, palette, or
   trade dress.

### P2.5-R9 — Phase 2.5 exit gate

**User story:** As the project owner, I want an objective completion check so the scored
session is correct and honest before further work.

#### Acceptance criteria

1. WHEN Phase 2.5 is declared complete, THE SYSTEM SHALL demonstrate a scored session that
   selects by official weighting (scaled to available domains), grades MC and all-or-nothing
   MR correctly, scores unanswered as incorrect, and withholds feedback until submission.
2. THE SYSTEM SHALL demonstrate a transparent scaled-score estimate and compensatory
   pass/fail labeled as an internal estimate.
3. THE SYSTEM SHALL demonstrate that starting or resetting a session clears the prior one so
   only one scored session's data exists, with no long-term history, while an in-progress
   session survives a refresh.
4. THE SYSTEM SHALL demonstrate Review listing the missed items from the single most recent
   scored session with explanations.
5. IF any gate fails, THEN THE SYSTEM SHALL keep the phase incomplete with blocking evidence.
