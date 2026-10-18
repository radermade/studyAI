-- Phase 3: richer lab authoring fields for real multi-step walkthroughs.
-- Immutable once applied. Adds narrative/pedagogy columns to lab tables so
-- step hints, reflection, and lab framing live in SQLite, not in the UI.

-- Lab-definition framing: learner-facing scenario, prerequisites text, the
-- objectives narrative, a Region/cost note, and a delayed-recall prompt.
ALTER TABLE lab_definitions ADD COLUMN scenario TEXT NOT NULL DEFAULT '';
ALTER TABLE lab_definitions ADD COLUMN prerequisites TEXT NOT NULL DEFAULT '';
ALTER TABLE lab_definitions ADD COLUMN objectives_text TEXT NOT NULL DEFAULT '';
ALTER TABLE lab_definitions ADD COLUMN region_note TEXT NOT NULL DEFAULT '';
ALTER TABLE lab_definitions ADD COLUMN recall_prompt TEXT NOT NULL DEFAULT '';

-- Per-step pedagogy: a progressive 4-level hint ladder (JSON array of 4
-- strings, concept -> service area -> procedure -> full solution) and a
-- per-step reflection prompt shown after the step's action.
ALTER TABLE lab_steps ADD COLUMN hints_json TEXT NOT NULL DEFAULT '[]';
ALTER TABLE lab_steps ADD COLUMN reflection TEXT NOT NULL DEFAULT '';

-- Checkpoints gain a human label and the step they belong to, so the
-- workspace can render evidence next to the step that produces it.
ALTER TABLE lab_checkpoints ADD COLUMN label TEXT NOT NULL DEFAULT '';
ALTER TABLE lab_checkpoints ADD COLUMN step_id TEXT NOT NULL DEFAULT '';
