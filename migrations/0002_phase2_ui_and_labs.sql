-- Phase 2 schema: curriculum/UI durability and the lab lifecycle.
-- Immutable once applied. Append-only evidence; no answer material here.

-- Curriculum and durable UI state --------------------------------------------
CREATE TABLE curriculum_items (
    item_id TEXT PRIMARY KEY,
    item_type TEXT NOT NULL,            -- lesson | lab
    title TEXT NOT NULL,
    display_order INTEGER NOT NULL,
    objective_ids TEXT NOT NULL,        -- JSON array
    prerequisites TEXT NOT NULL,        -- JSON array of item_ids
    content_ref TEXT                    -- content_id or lab_id
);

CREATE TABLE learner_content_state (
    learner_id TEXT NOT NULL,
    item_id TEXT NOT NULL REFERENCES curriculum_items(item_id),
    status TEXT NOT NULL,               -- not_started | in_progress | complete
    position INTEGER NOT NULL,
    updated_at TEXT NOT NULL,
    PRIMARY KEY (learner_id, item_id)
);

CREATE TABLE learner_notes (
    learner_id TEXT NOT NULL,
    context TEXT NOT NULL,              -- e.g. lesson:<id> or lab:<run_id>
    text TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    PRIMARY KEY (learner_id, context)
);

CREATE TABLE ui_resume_state (
    learner_id TEXT PRIMARY KEY,
    view TEXT NOT NULL,
    entity_id TEXT,
    position INTEGER NOT NULL,
    updated_at TEXT NOT NULL
);

-- Lab definitions ------------------------------------------------------------
CREATE TABLE lab_definitions (
    lab_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    objective_ids TEXT NOT NULL,        -- JSON array
    cost_class TEXT NOT NULL,
    regions TEXT NOT NULL,              -- JSON array
    architecture TEXT NOT NULL,
    cleanup TEXT NOT NULL
);

CREATE TABLE lab_steps (
    lab_id TEXT NOT NULL REFERENCES lab_definitions(lab_id),
    step_id TEXT NOT NULL,
    display_order INTEGER NOT NULL,
    instruction TEXT NOT NULL,
    prediction_prompt TEXT NOT NULL,
    mandatory INTEGER NOT NULL,
    PRIMARY KEY (lab_id, step_id)
);

CREATE TABLE lab_checkpoints (
    lab_id TEXT NOT NULL REFERENCES lab_definitions(lab_id),
    checkpoint_id TEXT NOT NULL,
    validator_id TEXT,                  -- NULL => self-report only
    is_cleanup INTEGER NOT NULL,
    mandatory INTEGER NOT NULL,
    PRIMARY KEY (lab_id, checkpoint_id)
);

-- Lab runs and append-only evidence ------------------------------------------
CREATE TABLE lab_runs (
    run_id TEXT PRIMARY KEY,
    learner_id TEXT NOT NULL,
    lab_id TEXT NOT NULL REFERENCES lab_definitions(lab_id),
    region TEXT NOT NULL,
    state TEXT NOT NULL,                -- active | paused | completion_pending |
                                        -- completed_independent | completed_assisted |
                                        -- abandoned
    active_step TEXT,
    full_solution_used INTEGER NOT NULL,
    started_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE checkpoint_events (
    event_id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL REFERENCES lab_runs(run_id),
    checkpoint_id TEXT NOT NULL,
    requested_state TEXT NOT NULL,
    evidence_id TEXT,
    committed_at TEXT NOT NULL
);

CREATE TABLE checkpoint_state (
    run_id TEXT NOT NULL REFERENCES lab_runs(run_id),
    checkpoint_id TEXT NOT NULL,
    state TEXT NOT NULL,                -- not_started | in_progress | self_reported |
                                        -- verified | failed | cleaned_up
    updated_at TEXT NOT NULL,
    PRIMARY KEY (run_id, checkpoint_id)
);

CREATE TABLE validation_attempts (
    attempt_id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL REFERENCES lab_runs(run_id),
    checkpoint_id TEXT NOT NULL,
    validator_id TEXT NOT NULL,
    region TEXT NOT NULL,
    outcome TEXT,                       -- set when completed
    started_at TEXT NOT NULL,
    completed_at TEXT
);

CREATE TABLE validation_evidence (
    evidence_id TEXT PRIMARY KEY,
    attempt_id TEXT NOT NULL REFERENCES validation_attempts(attempt_id),
    kind TEXT NOT NULL,                 -- self_report | resource_present |
                                        -- resource_absent | terminal_deletion |
                                        -- validation_failure
    summary TEXT NOT NULL,
    observed_at TEXT NOT NULL
);

CREATE TABLE hint_events (
    event_id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL REFERENCES lab_runs(run_id),
    step_id TEXT NOT NULL,
    level INTEGER NOT NULL,
    revealed_at TEXT NOT NULL
);

CREATE INDEX idx_lab_runs_learner ON lab_runs(learner_id, lab_id);
CREATE INDEX idx_checkpoint_state_run ON checkpoint_state(run_id);
CREATE INDEX idx_hint_events_run ON hint_events(run_id, step_id);
