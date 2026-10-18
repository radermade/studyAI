# Implementation Plan

## Overview

Build the scored-session engine, service, persistence, and UI over the existing Phase 1-2
platform. Leaf tasks name outcomes, requirements, and dependencies.

## Prerequisites

- Phase 1 core and Phase 2 focused app (Grill, Labs, Review, Progress) are in place.
- Authored Domain 1 questions with options, correct answers, rationales, and explanations
  exist and are ingested.

## Tasks

- [ ] 1. Selection and scoring engine (pure `study_core`)
  - [ ] 1.1 Implement official-weighted allocation with largest-remainder rounding
    - Outcome: a pure function returns per-domain scored counts (20/17/13/8/7 at 65) and
      scales to a subset of domains preserving relative weights.
    - Requirements: P2.5-R1, P2.5-R2
    - Depends on: Prerequisites
  - [ ] 1.2 Implement item selection with no repeats and unscored activation
    - Outcome: deterministic (injected random) selection fills each domain bucket, adds
      unscored items only above a documented pool threshold, and returns an ordered item
      list with server-side scored/unscored flags; empty eligibility yields a content gap.
    - Requirements: P2.5-R1, P2.5-R2
    - Depends on: 1.1
  - [ ] 1.3 Implement grading and the scaled-score estimate
    - Outcome: pure grading for MC, all-or-nothing MR, and unanswered-as-incorrect; a
      documented linear 100-1000 map; compensatory pass/fail at 750; per-domain breakdown.
    - Requirements: P2.5-R3, P2.5-R4
    - Depends on: Prerequisites
  - [ ] 1.4 Unit-test the engine
    - Outcome: tests cover exact full-length allocation, reduced scaling, no repeats,
      unscored threshold, MC/MR/unanswered grading, score-map endpoints and the 750
      boundary, and compensatory behavior.
    - Requirements: P2.5-R1, P2.5-R2, P2.5-R3, P2.5-R4
    - Depends on: 1.2, 1.3

- [ ] 2. Persistence and service
  - [ ] 2.1 Add migration 0004 for scored sessions, items, answers, and results
    - Outcome: forward-only tables with FKs, UTC timestamps, and JSON scope/per-domain
      fields; migration is immutable and applies in order.
    - Requirements: P2.5-R5, P2.5-R6
    - Depends on: 1.2
  - [ ] 2.2 Implement `ScoredSessionService` start/current_item/answer
    - Outcome: start selects and commits items; current_item returns an answer-free view
      with no scored/unscored flag; answer changes are idempotent per (session, question)
      and rejected after submission.
    - Requirements: P2.5-R1, P2.5-R2, P2.5-R5
    - Depends on: 2.1
  - [ ] 2.3 Implement submit, grading commit, and result persistence
    - Outcome: submit freezes answers, grades, computes the estimate, and commits an
      immutable result and per-item misses in one transaction; expiry auto-submits.
    - Requirements: P2.5-R3, P2.5-R4, P2.5-R5, P2.5-R7
    - Depends on: 1.3, 2.2
  - [ ] 2.4 Implement reset, history, and misses queries
    - Outcome: reset discards in-progress state; history lists past sessions reverse-chrono;
      misses returns the latest session's incorrect/unanswered items grouped by objective.
    - Requirements: P2.5-R6, P2.5-R7
    - Depends on: 2.3
  - [ ] 2.5 Test persistence and service
    - Outcome: tests cover restart durability, idempotent submit, frozen post-submit
      answers, reset, immutable history, and miss recording.
    - Requirements: P2.5-R5, P2.5-R6, P2.5-R7
    - Depends on: 2.4

- [ ] 3. UI: scored session, results, review
  - [ ] 3.1 Add the Scored Session view with scope picker, timer, navigation, and submit
    - Outcome: delayed-feedback flow with one item at a time, answer change, length label,
      and a submit confirmation; no answer material in browser-visible state.
    - Requirements: P2.5-R1, P2.5-R2, P2.5-R5
    - Depends on: 2.3
  - [ ] 3.2 Add the terminal/ASCII results readout
    - Outcome: original monospace PASS/FAIL banner and score summary with text+icon status,
      WCAG contrast, an accessible text equivalent, and the internal-estimate label.
    - Requirements: P2.5-R4, P2.5-R8
    - Depends on: 3.1
  - [ ] 3.3 Extend Review with scored-session misses
    - Outcome: Review lists the latest session's missed items with correct answer, rationale,
      and explanation, grouped by objective, alongside spaced-repetition items.
    - Requirements: P2.5-R7
    - Depends on: 2.4
  - [ ] 3.4 Add reset and history controls
    - Outcome: the learner can reset the active session and view past scored sessions and
      their scores from the UI.
    - Requirements: P2.5-R6
    - Depends on: 2.4, 3.1
  - [ ] 3.5 Wire the Scored Session view into navigation
    - Outcome: the focused app exposes Grill, Scored Session, Labs, Review, Progress.
    - Requirements: P2.5-R9
    - Depends on: 3.1

- [ ] 4. Validation and exit gate
  - [ ] 4.1 Run quality gates and an AppTest end-to-end flow
    - Outcome: Ruff, Ruff format check, mypy, and targeted pytest pass; an AppTest drives
      start -> answer -> submit -> result -> review without exceptions or feedback leakage.
    - Requirements: P2.5-R5, P2.5-R8, P2.5-R9
    - Depends on: 3.2, 3.3, 3.4, 3.5
  - [ ] 4.2 Execute the Phase 2.5 exit gate
    - Outcome: a reproducible run demonstrates official-weighted selection scaled to Domain
      1, correct MC/MR/unanswered grading, a labeled scaled-score estimate with compensatory
      pass/fail, reset and history, and Review of the latest session's misses.
    - Requirements: P2.5-R9
    - Depends on: 4.1

## Notes

- The engine must remain pure and deterministic (injected clock and random source).
- Phase 8 reuses this engine; do not duplicate selection/grading there.
- No answer material, correct options, or scored/unscored flags may reach browser-visible
  state during a session.
