-- Phase 1 initial schema. Immutable once applied.
-- Stable string IDs; UTC ISO 8601 text timestamps; explicit foreign keys.
-- Public question data and private answer material live in separate tables.

-- Blueprint and objectives ---------------------------------------------------
CREATE TABLE blueprints (
    blueprint_version TEXT PRIMARY KEY,
    created_at TEXT NOT NULL
);

CREATE TABLE domains (
    domain_id INTEGER NOT NULL,
    blueprint_version TEXT NOT NULL REFERENCES blueprints(blueprint_version),
    title TEXT NOT NULL,
    weight_percent INTEGER NOT NULL,
    PRIMARY KEY (domain_id, blueprint_version)
);

CREATE TABLE objectives (
    objective_id TEXT NOT NULL,
    blueprint_version TEXT NOT NULL REFERENCES blueprints(blueprint_version),
    domain_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    status TEXT NOT NULL,
    PRIMARY KEY (objective_id, blueprint_version)
);

-- Sources --------------------------------------------------------------------
CREATE TABLE sources (
    source_id TEXT PRIMARY KEY,
    blueprint_version TEXT NOT NULL REFERENCES blueprints(blueprint_version),
    url TEXT NOT NULL,
    title TEXT NOT NULL,
    publisher TEXT NOT NULL,
    retrieved_at TEXT NOT NULL,
    source_type TEXT NOT NULL,
    freshness TEXT NOT NULL
);

-- Learner, profile, safety, baseline -----------------------------------------
CREATE TABLE learner_profiles (
    learner_id TEXT NOT NULL,
    profile_version TEXT NOT NULL,
    weekly_hours INTEGER NOT NULL,
    experience TEXT NOT NULL,
    target_region TEXT NOT NULL,
    account_type TEXT NOT NULL,
    lab_budget_usd REAL NOT NULL,
    exam_date TEXT,
    exam_date_undecided INTEGER NOT NULL,
    updated_at TEXT NOT NULL,
    PRIMARY KEY (learner_id, profile_version)
);

CREATE TABLE safety_policies (
    policy_version TEXT PRIMARY KEY,
    payload_json TEXT NOT NULL,
    ingested_at TEXT NOT NULL
);

CREATE TABLE baseline_summaries (
    run_id TEXT PRIMARY KEY,
    learner_id TEXT NOT NULL,
    complete INTEGER NOT NULL,
    answered_count INTEGER NOT NULL,
    unanswered_count INTEGER NOT NULL,
    mean_confidence REAL NOT NULL,
    ingested_at TEXT NOT NULL
);

-- Content --------------------------------------------------------------------
CREATE TABLE content_units (
    content_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    source_ids TEXT NOT NULL,       -- JSON array of source IDs
    freshness TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE content_objectives (
    content_id TEXT NOT NULL REFERENCES content_units(content_id),
    objective_id TEXT NOT NULL,
    PRIMARY KEY (content_id, objective_id)
);

-- Questions (public) and answer material (private) ---------------------------
CREATE TABLE questions (
    question_id TEXT PRIMARY KEY,
    prompt TEXT NOT NULL,
    scenario_constraint TEXT NOT NULL,
    difficulty TEXT NOT NULL,
    question_format TEXT NOT NULL,
    source_ids TEXT NOT NULL,       -- JSON array
    review_status TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE question_objectives (
    question_id TEXT NOT NULL REFERENCES questions(question_id),
    objective_id TEXT NOT NULL,
    PRIMARY KEY (question_id, objective_id)
);

CREATE TABLE question_options (
    question_id TEXT NOT NULL REFERENCES questions(question_id),
    option_id TEXT NOT NULL,
    text TEXT NOT NULL,
    PRIMARY KEY (question_id, option_id)
);

-- Private grading material. Deliberately isolated from public question tables.
CREATE TABLE answer_material (
    question_id TEXT PRIMARY KEY REFERENCES questions(question_id),
    correct_option_ids TEXT NOT NULL,   -- JSON array
    rubric TEXT NOT NULL
);

-- Sessions, attempts, misconceptions, reviews --------------------------------
CREATE TABLE sessions (
    session_id TEXT PRIMARY KEY,
    learner_id TEXT NOT NULL,
    mode TEXT NOT NULL,
    objective_filter TEXT NOT NULL,     -- JSON array (possibly empty)
    blueprint_version TEXT NOT NULL,
    state TEXT NOT NULL,
    started_at TEXT NOT NULL
);

CREATE TABLE session_items (
    session_id TEXT NOT NULL REFERENCES sessions(session_id),
    question_id TEXT NOT NULL REFERENCES questions(question_id),
    served_at TEXT NOT NULL,
    PRIMARY KEY (session_id, question_id)
);

CREATE TABLE attempts (
    attempt_id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL REFERENCES sessions(session_id),
    question_id TEXT NOT NULL REFERENCES questions(question_id),
    learner_id TEXT NOT NULL,
    outcome TEXT NOT NULL,              -- correct | incorrect | grading_uncertain
    confidence INTEGER NOT NULL,
    elapsed_seconds REAL NOT NULL,
    committed_at TEXT NOT NULL
);

CREATE TABLE misconceptions (
    misconception_id TEXT PRIMARY KEY,
    learner_id TEXT NOT NULL,
    objective_id TEXT NOT NULL,
    state TEXT NOT NULL,                -- open | resolved
    updated_at TEXT NOT NULL
);

CREATE TABLE reviews (
    review_id TEXT PRIMARY KEY,
    learner_id TEXT NOT NULL,
    question_id TEXT NOT NULL REFERENCES questions(question_id),
    objective_id TEXT NOT NULL,
    due_at TEXT NOT NULL,
    interval_days INTEGER NOT NULL,
    state TEXT NOT NULL,                -- scheduled | resolved | superseded
    policy_version TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

-- Idempotency ----------------------------------------------------------------
CREATE TABLE idempotency_events (
    caller_id TEXT NOT NULL,
    operation TEXT NOT NULL,
    payload_hash TEXT NOT NULL,
    result_json TEXT NOT NULL,
    committed_at TEXT NOT NULL,
    PRIMARY KEY (caller_id, operation)
);

-- FTS5 material index over permitted content fields only.
CREATE VIRTUAL TABLE material_fts USING fts5 (
    content_id UNINDEXED,
    title,
    body,
    objective_ids UNINDEXED,
    freshness UNINDEXED
);

CREATE INDEX idx_reviews_due ON reviews(learner_id, state, due_at);
CREATE INDEX idx_attempts_learner ON attempts(learner_id, question_id);
CREATE INDEX idx_session_items_session ON session_items(session_id);
