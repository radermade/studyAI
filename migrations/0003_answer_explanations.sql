-- Phase 3 content: per-question explanations and per-option rationales.
-- These are private (post-answer) teaching material, kept out of the
-- unanswered-question projection. Immutable once applied.

ALTER TABLE answer_material ADD COLUMN explanation TEXT NOT NULL DEFAULT '';

CREATE TABLE option_rationales (
    question_id TEXT NOT NULL REFERENCES questions(question_id),
    option_id TEXT NOT NULL,
    is_correct INTEGER NOT NULL,
    rationale TEXT NOT NULL,
    PRIMARY KEY (question_id, option_id)
);
