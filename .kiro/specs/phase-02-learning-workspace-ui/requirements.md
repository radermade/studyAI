# Requirements Document

## Phase 02 Learning Workspace UI

## Introduction

**Status:** Proposed  
**Scope:** Build an original Streamlit multipage learning workspace over Phase 1, including course, grill, review, mock, knowledge, progress, and evidence-based AWS lab workflows.

## Upstream Dependencies

- Accepted Phase 0 blueprint/source/profile/safety contracts and Phase 1 local study-core database, use cases, and six stable MCP tools.
- Phase 1 core/API handoff extended in this phase with `start_lab`, `record_lab_checkpoint`, and `complete_lab` plus typed read-only AWS validator ports.
- Source-attributed Markdown/YAML lesson and lab content that references stable AIP objective IDs.
- AWS Console access is optional and learner-operated; AWS credentials use named profiles or the standard credential chain and are never stored by the application.

## Out of Scope

- Copying KodeKloud branding, wording, screenshots, source code, exact layouts, assets, palette, or trade dress.
- Embedding AWS Console in an iframe, automating away learner-operated console work, or mutating AWS resources through validators.
- Hosted deployment, separate API server, frontend framework, vector database, local model, speech/OCR, or automatic content generation.
- Full 75-question readiness implementation and readiness thresholds reserved for Phase 8, although a truthful mock workspace and delayed-feedback behavior are included.

## Glossary

- **Checkpoint:** A durable lab evidence unit with exactly one explicit state.
- **Verified:** A state supported by committed, sanitized read-only validator evidence.
- **Cleaned up:** A state supported only by observed absence or terminal deletion evidence.
- **Assisted completion:** A lab completion on a run where the full solution was revealed.

## Requirements

### P2-R1 — Eight-view information architecture

**User story:** As a learner, I want one coherent workspace so that daily study, lessons, practice, labs, review, mocks, knowledge, and progress remain connected.

#### Acceptance Criteria

1. WHEN the Streamlit application loads, THE SYSTEM SHALL provide the eight named views Today, Learn, Grill, Labs, Review, Mock, Knowledge, and Progress.
2. WHEN a learner changes views, THE SYSTEM SHALL preserve durable session/lab context and provide a compact current-path, blueprint-version, due-review, and resume context.
3. WHEN a view has no data, stale data, offline dependencies, or unavailable AWS access, THE SYSTEM SHALL render an explicit actionable state rather than a blank or false success.
4. IF a route or entity ID is invalid, THE SYSTEM SHALL recover to a safe view with a typed message and SHALL NOT expose internals or answer material.

### P2-R2 — Persistent curriculum and Today guidance

**User story:** As a learner, I want persistent curriculum context and a focused Today view so that I always know what to resume or do next.

#### Acceptance Criteria

1. WHEN Learn or Labs is displayed on desktop, THE SYSTEM SHALL show a collapsible curriculum rail with domains, modules, lessons, labs, prerequisite locks, completion state, and due-review badges.
2. WHEN Today is displayed, THE SYSTEM SHALL show due reviews, a recommended lesson or lab, session target, resume action, and blockers derived from committed Phase 1 evidence.
3. WHEN curriculum progress is shown, THE SYSTEM SHALL distinguish not started, in progress, complete, and blocked using text/icon as well as color.
4. IF a prerequisite is unmet, THE SYSTEM SHALL explain the dependency and SHALL NOT imply the item is complete or verified.
5. WHEN the viewport is narrow, THE SYSTEM SHALL collapse or relocate the rail without hiding the active learning task.

### P2-R3 — Short source-attributed lesson player

**User story:** As a learner, I want concise lessons tied to practice so that I can learn a concept, test recall, and move directly to relevant work.

#### Acceptance Criteria

1. WHEN a lesson is opened, THE SYSTEM SHALL present short concept, decision/trade-off, example, failure-mode, recall-check, and practice blocks rather than one undifferentiated page.
2. WHEN lesson metadata is shown, THE SYSTEM SHALL expose objective IDs, source title/publisher/URL, retrieval date, freshness, and fact/recommendation/note classification.
3. WHEN the learner chooses linked practice, THE SYSTEM SHALL start or resume a filtered grill or associated lab without losing lesson position or notes.
4. WHEN architecture is illustrated, THE SYSTEM SHALL use maintainable Mermaid content or original accessible visuals and SHALL NOT embed proprietary diagrams.
5. IF content is stale, malformed, or lacks required objective/source metadata, THE SYSTEM SHALL label or block it according to content policy and SHALL NOT silently score it.

### P2-R4 — Durable lab lifecycle tools

**User story:** As a learner and MCP client, I want a durable, idempotent lab lifecycle so that progress and completion survive reruns without false claims.

#### Acceptance Criteria

1. WHEN `start_lab` receives learner ID, lab ID, Region, request ID, and acknowledged prerequisites/cost/cleanup conditions, THE SYSTEM SHALL create or return one durable lab run only if Phase 0 safety gates pass.
2. WHEN `record_lab_checkpoint` receives a run ID, checkpoint ID, requested transition, evidence, and event ID, THE SYSTEM SHALL validate and persist one legal state transition or return a typed conflict.
3. WHEN `complete_lab` is requested, THE SYSTEM SHALL require all mandatory checkpoints and cleanup obligations to satisfy the lab definition and SHALL record whether completion was independent or hint-assisted.
4. WHEN the three lab tools are exposed through FastMCP, THE SYSTEM SHALL use typed Pydantic inputs/outputs, stable names, idempotency IDs, thin adapters, and success only after commit.
5. IF a retry reuses an ID with a different payload, THE SYSTEM SHALL return conflict and SHALL NOT duplicate or overwrite evidence.
6. IF a lab is blocked by missing prerequisites, cost acknowledgement, Region policy, or cleanup definition, THE SYSTEM SHALL refuse to start it with actionable reasons.

### P2-R5 — Split, resizable lab workspace and Console companion

**User story:** As a learner, I want instructions and evidence side by side so that I can operate AWS Console without losing the active step.

#### Acceptance Criteria

1. WHEN Lab mode is opened on desktop, THE SYSTEM SHALL provide a split workspace with a resizable instruction pane and workspace/evidence pane, plus a collapsible curriculum rail.
2. WHEN a lab step is active, THE SYSTEM SHALL show one task, objective, rationale, prediction prompt, hint access, check action, reflection, and cleanup context.
3. WHEN AWS Console access is requested, THE SYSTEM SHALL open an explicit HTTPS Console link in a separate browser tab and SHALL NOT rely on iframe embedding.
4. WHEN Streamlit reruns, the browser refreshes, or focus leaves the app, THE SYSTEM SHALL restore the durable lab run, active step, notes, timer basis, hints used, and checkpoint evidence.
5. WHEN the viewport is narrow, THE SYSTEM SHALL stack panes with the active task before supplemental context and SHALL preserve all actions.
6. IF custom resizing is unavailable in the current Streamlit/browser combination, THE SYSTEM SHALL provide an accessible fixed/stacked fallback without losing content.

### P2-R6 — Evidence-based checkpoints and read-only AWS validation

**User story:** As a learner, I want clear evidence states so that navigation, self-reporting, AWS verification, and cleanup cannot be confused.

#### Acceptance Criteria

1. WHEN a checkpoint is rendered, THE SYSTEM SHALL use exactly one explicit state: Not started, In progress, Self-reported, Verified, Failed, or Cleaned up.
2. WHEN a learner clicks Check, THE SYSTEM SHALL invoke only the checkpoint's typed validator contract with explicit service/action allowlist, Region, bounded timeout, and standard AWS credential chain.
3. WHEN validation succeeds after read-only AWS evidence is obtained, THE SYSTEM SHALL persist sanitized evidence before displaying Verified.
4. IF validation fails, times out, lacks authorization, lacks credentials, or is unavailable, THE SYSTEM SHALL distinguish those outcomes, preserve prior truthful state, and SHALL NOT display Verified.
5. WHEN cleanup is checked, THE SYSTEM SHALL display Cleaned up only after absence or terminal deletion state is confirmed by evidence; a click, navigation, or self-report alone SHALL NOT qualify.
6. WHEN self-report is permitted, THE SYSTEM SHALL label it Self-reported and SHALL NOT convert it to Verified in progress or readiness calculations.
7. IF a validator requests a mutating AWS action or an action outside its allowlist, THE SYSTEM SHALL reject execution and record a security-safe failure without logging credentials or private response content.

### P2-R7 — Progressive hints and learning evidence

**User story:** As a learner, I want hints that escalate gradually so that I can recover while preserving honest evidence of independence.

#### Acceptance Criteria

1. WHEN hints are requested, THE SYSTEM SHALL reveal in order: conceptual nudge, service/architecture area, procedural guidance, then full solution/explanation.
2. WHEN a hint is revealed, THE SYSTEM SHALL durably record level and UTC time before displaying it.
3. WHEN the full solution is used, THE SYSTEM SHALL mark completion as hint-assisted and SHALL require later unassisted repetition before counting independent completion.
4. IF hint persistence fails, THE SYSTEM SHALL report the failure and SHALL NOT reveal the next hint as though usage had been recorded.

### P2-R8 — Grill, Review, and Mock behavior

**User story:** As a learner, I want practice modes with mode-appropriate feedback so that learning is immediate while mock evidence remains uncontaminated.

#### Acceptance Criteria

1. WHEN Grill serves a question, THE SYSTEM SHALL display one unanswered question at a time, record confidence and elapsed time before grading, and keep answer material out of browser-visible pregrade state.
2. WHEN Grill grading commits, THE SYSTEM SHALL present status, decisive requirement, reasoning/trade-off, distractor analysis, primary source, and targeted next action in that order.
3. WHEN Review is displayed, THE SYSTEM SHALL serve committed due reviews and explain empty or blocked states without fabricating due work.
4. WHILE a Mock session is active, THE SYSTEM SHALL hide objective cues where practical, correctness, explanations, and hints until submission.
5. IF grading persistence fails, THE SYSTEM SHALL not show a success state or advance as though the attempt were recorded.
6. WHERE Phase 8 readiness criteria are not implemented, THE SYSTEM SHALL label Mock as practice-capable/incomplete and SHALL NOT claim full exam-readiness validation.

### P2-R9 — Knowledge and evidence-rich Progress views

**User story:** As a learner, I want attributable search and multidimensional progress so that I can investigate gaps without relying on a misleading completion score.

#### Acceptance Criteria

1. WHEN Knowledge is searched, THE SYSTEM SHALL use Phase 1 local FTS5 search with objective/service filters, attribution, freshness indicators, pagination, and explicit empty/error states.
2. WHEN Progress is displayed, THE SYSTEM SHALL present accuracy and delayed recall by domain/task, confidence calibration, repeated misconceptions, due reviews, independent versus hint-assisted labs, verified cleanup, speed/unanswered rate, source freshness, and uncovered tasks where evidence exists.
3. WHEN an aggregate readiness estimate is shown, THE SYSTEM SHALL expose inputs and label it an internal estimate rather than an AWS score prediction.
4. IF evidence is self-reported, stale, absent, or unreviewed, THE SYSTEM SHALL identify that limitation and SHALL NOT render it as verified mastery.

### P2-R10 — Original, accessible, responsive visual system

**User story:** As a learner using varied devices and input methods, I want an original accessible workspace so that study remains usable without copying another product.

#### Acceptance Criteria

1. WHEN UI assets and styles are reviewed, THE SYSTEM SHALL use an original product name, copy, typography, semantic color tokens, icons, component styling, and layout expression with no copied KodeKloud branding/assets/trade dress.
2. WHEN status or correctness is communicated, THE SYSTEM SHALL pair color with text and/or icon and target WCAG 2.2 AA contrast.
3. WHEN interactive controls receive keyboard focus, THE SYSTEM SHALL provide a visible focus indicator and accessible label where Streamlit permits.
4. WHEN validation feedback is shown, THE SYSTEM SHALL associate it with the relevant action/control and communicate actionable text.
5. WHEN reduced motion is requested, THE SYSTEM SHALL not require animation to understand state.
6. WHEN narrow-screen layouts are used, THE SYSTEM SHALL remain operable through stacking/collapsing without horizontal task loss.

### P2-R11 — UI security, privacy, durability, and performance

**User story:** As a learner, I want a responsive interface backed by committed state so that reruns and failures neither leak secrets nor lose meaningful progress.

#### Acceptance Criteria

1. WHEN the UI renders, THE SYSTEM SHALL treat `st.session_state` as a view cache only and SHALL persist meaningful learner actions through `study_core` before success feedback.
2. WHEN widgets are created, THE SYSTEM SHALL use stable keys derived from stable entity IDs and SHALL avoid answer keys, rubrics, credentials, and hidden mock results in browser-visible state.
3. WHEN application code loads or reruns, THE SYSTEM SHALL avoid unbounded I/O and import-time AWS/database side effects and SHALL bound validator/search operations with explicit timeouts or limits.
4. WHEN standard local content and database data are available, THE SYSTEM SHALL render primary navigation and the active view without requiring network access.
5. IF an exception occurs, THE SYSTEM SHALL map it to a recoverable user message, log only sanitized identifiers, and preserve committed state.
6. WHEN AWS credentials are used, THE SYSTEM SHALL rely on named profiles or the standard credential chain and SHALL never persist or display credential material.

### P2-R12 — Phase 2 exit gate

**User story:** As the project owner, I want observable UI release gates so that the learning workspace is useful, durable, truthful, and original before domain expansion.

#### Acceptance Criteria

1. WHEN Phase 2 is declared complete, THE SYSTEM SHALL demonstrate movement from a lesson to associated grill questions and a lab without losing context.
2. WHEN Phase 2 is declared complete, THE SYSTEM SHALL demonstrate that refreshing the app does not lose current session or lab progress.
3. WHEN Phase 2 is declared complete, THE SYSTEM SHALL demonstrate that verified, self-reported, failed, and not-yet-checked steps are visibly and semantically distinct.
4. WHEN Phase 2 is declared complete, THE SYSTEM SHALL demonstrate that cleanup is claimed only from verified absence or terminal deletion evidence.
5. WHEN Phase 2 is declared complete, THE SYSTEM SHALL verify that no KodeKloud logos, copied screenshots, proprietary wording, cloned assets, or brand styling are present.
6. IF any gate fails, THE SYSTEM SHALL emit blocking evidence and SHALL NOT mark Phase 2 accepted.
