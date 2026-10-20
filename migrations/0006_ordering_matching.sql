-- Phase 9: ordering and matching question types (AIP-C01 official formats).
-- Immutable once applied.
--
-- Ordering: the question's options are the steps; the correct answer is an
-- ordered sequence of option ids (a subset is allowed when the question uses
-- only some options). The ordered key is stored as a JSON array on
-- answer_material so the existing answer-key plumbing is reused. Grading is
-- all-or-nothing on exact sequence equality.
--
-- Matching: the question carries a list of prompts and a list of responses;
-- the correct answer maps each prompt to exactly one response (responses may
-- repeat or go unused). Grading is all-or-nothing on every pair matching.

-- Ordered correct sequence for ordering questions (JSON array of option ids).
-- NULL/empty for non-ordering questions.
ALTER TABLE answer_material ADD COLUMN correct_sequence TEXT NOT NULL DEFAULT '';

-- Left-hand prompts shown for a matching question.
CREATE TABLE match_prompts (
    question_id TEXT NOT NULL REFERENCES questions(question_id),
    prompt_id TEXT NOT NULL,
    display_order INTEGER NOT NULL,
    text TEXT NOT NULL,
    PRIMARY KEY (question_id, prompt_id)
);

-- Right-hand selectable responses for a matching question. Responses are
-- rendered as the dropdown choices for every prompt.
CREATE TABLE match_responses (
    question_id TEXT NOT NULL REFERENCES questions(question_id),
    response_id TEXT NOT NULL,
    display_order INTEGER NOT NULL,
    text TEXT NOT NULL,
    PRIMARY KEY (question_id, response_id)
);

-- Private correct pairing: the response each prompt must map to. Kept separate
-- from the public prompt/response text so the unanswered projection never
-- carries the key.
CREATE TABLE match_answer_keys (
    question_id TEXT NOT NULL REFERENCES questions(question_id),
    prompt_id TEXT NOT NULL,
    response_id TEXT NOT NULL,
    PRIMARY KEY (question_id, prompt_id)
);

-- Learner's submitted pairing for a matching question within a scored session.
CREATE TABLE scored_match_answers (
    session_id TEXT NOT NULL REFERENCES scored_sessions(session_id),
    question_id TEXT NOT NULL REFERENCES questions(question_id),
    prompt_id TEXT NOT NULL,
    response_id TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    PRIMARY KEY (session_id, question_id, prompt_id)
);
