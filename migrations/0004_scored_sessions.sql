-- Phase 2.5: scored sessions, items, answers, results, and misses.
-- Immutable once applied. Server-side scored/unscored flag; UTC timestamps.

CREATE TABLE scored_sessions (
    session_id TEXT PRIMARY KEY,
    learner_id TEXT NOT NULL,
    scope TEXT NOT NULL,                 -- JSON array of domain ids (empty => all available)
    state TEXT NOT NULL,                 -- in_progress | submitted | abandoned
    scored_total INTEGER NOT NULL,
    unscored_total INTEGER NOT NULL,
    full_length INTEGER NOT NULL,
    time_limit_seconds INTEGER,          -- NULL => untimed
    started_at TEXT NOT NULL,
    deadline TEXT,                       -- NULL => untimed
    submitted_at TEXT
);

CREATE TABLE scored_session_items (
    session_id TEXT NOT NULL REFERENCES scored_sessions(session_id),
    position INTEGER NOT NULL,
    question_id TEXT NOT NULL REFERENCES questions(question_id),
    is_scored INTEGER NOT NULL,          -- server-side only; never sent to the UI
    domain_id INTEGER NOT NULL,
    PRIMARY KEY (session_id, position)
);

CREATE TABLE scored_answers (
    session_id TEXT NOT NULL REFERENCES scored_sessions(session_id),
    question_id TEXT NOT NULL REFERENCES questions(question_id),
    selected_option_ids TEXT NOT NULL,   -- JSON array
    answered INTEGER NOT NULL,
    updated_at TEXT NOT NULL,
    PRIMARY KEY (session_id, question_id)
);

CREATE TABLE scored_results (
    session_id TEXT PRIMARY KEY REFERENCES scored_sessions(session_id),
    raw_correct INTEGER NOT NULL,
    scored_total INTEGER NOT NULL,
    percent REAL NOT NULL,
    scaled_estimate INTEGER NOT NULL,
    passed INTEGER NOT NULL,
    per_domain TEXT NOT NULL,            -- JSON [{domain_id, correct, total}, ...]
    full_length INTEGER NOT NULL,
    committed_at TEXT NOT NULL
);

CREATE TABLE scored_misses (
    session_id TEXT NOT NULL REFERENCES scored_sessions(session_id),
    question_id TEXT NOT NULL REFERENCES questions(question_id),
    objective_id TEXT NOT NULL,
    unanswered INTEGER NOT NULL,
    PRIMARY KEY (session_id, question_id)
);

CREATE INDEX idx_scored_sessions_learner ON scored_sessions(learner_id, started_at);
CREATE INDEX idx_scored_items_session ON scored_session_items(session_id, position);
