"""Authored Domain 5 (AIP-C01) scenario questions with answers and explanations.

Original, scenario-style multiple-choice questions testing evaluation and
troubleshooting reasoning for the AWS Certified Generative AI Developer exam.
Each question has a decisive constraint, four distinct options, one correct
answer, per-option rationales, and a teaching explanation. No proprietary exam
content is reproduced.

Shape per question matches ``content/domain1_questions.py`` so the same
ingestion path consumes all authored domains.
"""

from __future__ import annotations

from typing import Any

QUESTIONS: list[dict[str, Any]] = [
    # --- AIP-5.1 evaluation -------------------------------------------------
    {
        "question_id": "d5-golden-dataset",
        "objective_ids": ["AIP-5.1"],
        "prompt": (
            "A team judges model quality by eyeballing a few outputs after each "
            "change, so results are inconsistent and not comparable over time. "
            "What gives them a repeatable quality measurement?"
        ),
        "scenario_constraint": "Make quality measurable and comparable across changes.",
        "difficulty": "easy",
        "options": [
            (
                "a",
                "A fixed golden dataset with expected answers, scored by defined metrics each run.",
            ),
            ("b", "A fresh handful of random prompts reviewed by whoever is free."),
            ("c", "Trust that newer models are always better."),
            ("d", "Only measure latency, since quality is subjective."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "A fixed golden dataset with expected answers and defined metrics "
            "makes quality repeatable and comparable across changes. Ad hoc "
            "sampling is inconsistent, assuming newness is not measurement, and "
            "latency-only ignores quality entirely."
        ),
        "rationales": {
            "a": (True, "A fixed golden set with metrics is repeatable and comparable."),
            "b": (False, "Random ad hoc review is inconsistent and not comparable."),
            "c": (False, "Assuming newer is better is not a measurement."),
            "d": (False, "Latency-only ignores the quality being evaluated."),
        },
    },
    {
        "question_id": "d5-deterministic-vs-judge",
        "objective_ids": ["AIP-5.1"],
        "prompt": (
            "Some outputs can be checked exactly (valid JSON, correct label), "
            "while others are open-ended summaries needing judgment. How should "
            "the evaluation suite handle both?"
        ),
        "scenario_constraint": "Mix of exactly-checkable and open-ended outputs.",
        "difficulty": "medium",
        "options": [
            (
                "a",
                "Use deterministic checks where exact answers exist and a calibrated model/human judge for open-ended ones.",
            ),
            ("b", "Use a model judge for everything, including exact checks."),
            ("c", "Use exact string matching for the open-ended summaries too."),
            ("d", "Skip evaluating open-ended outputs because they are hard."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Deterministic checks fit exactly-verifiable outputs; a calibrated "
            "judge (model or human) fits open-ended ones. Using a judge for "
            "exact checks adds noise, exact matching breaks on valid paraphrases, "
            "and skipping open-ended evaluation leaves quality unmeasured."
        ),
        "rationales": {
            "a": (True, "Match the method to the output: exact checks vs. calibrated judge."),
            "b": (False, "A judge for exact checks adds unnecessary noise."),
            "c": (False, "Exact matching fails on valid open-ended paraphrases."),
            "d": (False, "Skipping open-ended outputs leaves them unmeasured."),
        },
    },
    {
        "question_id": "d5-judge-calibration",
        "objective_ids": ["AIP-5.1"],
        "prompt": (
            "A team adopts an LLM-as-judge to score answer quality but has not "
            "checked whether its scores agree with human judgment. What must "
            "they do before trusting it?"
        ),
        "scenario_constraint": "Validate the judge before relying on its scores.",
        "difficulty": "hard",
        "options": [
            (
                "a",
                "Calibrate the judge against human-labeled examples and measure agreement before relying on it.",
            ),
            ("b", "Assume the judge is correct because it is an advanced model."),
            ("c", "Use the judge's scores as ground truth immediately."),
            ("d", "Have the judge grade its own prompts to check itself."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "A model judge must be calibrated against human-labeled examples with "
            "measured agreement before its scores are trusted. Assuming "
            "correctness, treating raw scores as ground truth, and self-grading "
            "all skip the needed validation."
        ),
        "rationales": {
            "a": (True, "Calibrating against human labels validates the judge."),
            "b": (False, "Model sophistication is not evidence of agreement."),
            "c": (False, "Unvalidated judge scores are not ground truth."),
            "d": (False, "Self-grading cannot validate the judge."),
        },
    },
    {
        "question_id": "d5-release-quality-gate",
        "objective_ids": ["AIP-5.1", "AIP-2.3"],
        "prompt": (
            "Changes ship to production whenever they pass code review, with no "
            "quality check on model behavior, and regressions reach users. What "
            "should gate releases?"
        ),
        "scenario_constraint": "Stop quality regressions from reaching users at release.",
        "difficulty": "medium",
        "options": [
            (
                "a",
                "An automated evaluation gate on the golden set that must pass before promotion.",
            ),
            ("b", "Code review alone, since it already catches bugs."),
            ("c", "A manual spot check after the change is already live."),
            ("d", "Releasing on a schedule regardless of evaluation."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "An automated evaluation gate on the golden set blocks promotion of "
            "regressions before users see them. Code review does not test model "
            "quality, post-release spot checks are too late, and schedule-based "
            "release ignores quality."
        ),
        "rationales": {
            "a": (True, "An evaluation gate blocks regressions before promotion."),
            "b": (False, "Code review does not measure model-answer quality."),
            "c": (False, "A post-release check is too late to prevent harm."),
            "d": (False, "Scheduled release ignores quality entirely."),
        },
    },
    # --- AIP-5.2 troubleshooting -------------------------------------------
    {
        "question_id": "d5-isolate-variable",
        "objective_ids": ["AIP-5.2"],
        "prompt": (
            "After a change bundling a new prompt, a new model, and new retrieval "
            "settings, quality dropped. You must find which change caused it. "
            "What is the sound approach?"
        ),
        "scenario_constraint": "Several changes shipped together; isolate the culprit.",
        "difficulty": "medium",
        "options": [
            (
                "a",
                "Revert to baseline and reintroduce changes one at a time, measuring after each.",
            ),
            ("b", "Guess which change is to blame and revert only that."),
            ("c", "Revert everything permanently and stop investigating."),
            ("d", "Add a fourth change hoping it offsets the drop."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Reintroducing changes one at a time from a known baseline isolates "
            "the culprit by measurement. Guessing is unreliable, abandoning the "
            "investigation leaves the cause unknown, and stacking another change "
            "confounds the signal further."
        ),
        "rationales": {
            "a": (True, "One-variable-at-a-time from baseline isolates the cause."),
            "b": (False, "Guessing may revert the wrong change."),
            "c": (False, "Abandoning the investigation leaves the cause unknown."),
            "d": (False, "Another change confounds the diagnosis."),
        },
    },
    {
        "question_id": "d5-retrieval-vs-generation",
        "objective_ids": ["AIP-5.2", "AIP-1.5"],
        "prompt": (
            "A RAG assistant gives wrong answers. You must determine whether the "
            "fault is in retrieval (wrong context) or generation (bad use of "
            "good context). What diagnostic step comes first?"
        ),
        "scenario_constraint": "Localize the fault to retrieval vs. generation.",
        "difficulty": "medium",
        "options": [
            (
                "a",
                "Inspect the retrieved passages: if they are wrong it is retrieval; if correct it is generation.",
            ),
            ("b", "Immediately swap the generation model and see if it helps."),
            ("c", "Rewrite the prompt without checking what was retrieved."),
            ("d", "Increase top-k and hope the answer improves."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Inspecting the retrieved context localizes the fault: wrong passages "
            "point to retrieval, correct passages used badly point to generation. "
            "Swapping the model, rewriting the prompt, or bumping top-k blindly "
            "all act before the cause is known."
        ),
        "rationales": {
            "a": (True, "Inspecting retrieved context localizes retrieval vs. generation."),
            "b": (False, "Swapping the model acts before diagnosing."),
            "c": (False, "Rewriting the prompt skips checking retrieval."),
            "d": (False, "Raising top-k is a blind change, not a diagnosis."),
        },
    },
    {
        "question_id": "d5-reproduce-before-fix",
        "objective_ids": ["AIP-5.2"],
        "prompt": (
            "A failure is reported intermittently in production. The team wants "
            "to fix it fast. What should they establish before changing code?"
        ),
        "scenario_constraint": "Intermittent failure; avoid guessing at a fix.",
        "difficulty": "easy",
        "options": [
            ("a", "A reliable reproduction and the evidence (logs/traces) that pin the trigger."),
            ("b", "A speculative fix shipped immediately to see if it helps."),
            ("c", "A broad rewrite of the suspected area."),
            ("d", "A note to wait until the failure becomes constant."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "A reliable reproduction plus pinning evidence lets you fix the real "
            "cause and verify the fix. A speculative fix may mask or miss the "
            "cause, a broad rewrite is risky without a target, and waiting lets "
            "the failure keep harming users."
        ),
        "rationales": {
            "a": (True, "Reproduction + evidence targets the real cause and verifies the fix."),
            "b": (False, "A speculative fix may not address the true cause."),
            "c": (False, "A broad rewrite without a target is risky."),
            "d": (False, "Waiting prolongs user harm."),
        },
    },
    {
        "question_id": "d5-validate-recovery",
        "objective_ids": ["AIP-5.2", "AIP-4.1"],
        "prompt": (
            "After applying a fix for a production incident, what step confirms "
            "the problem is actually resolved rather than merely assumed?"
        ),
        "scenario_constraint": "Confirm recovery with evidence, not assumption.",
        "difficulty": "easy",
        "options": [
            (
                "a",
                "Re-run the reproduction and watch the metrics/traces return to healthy, documenting the result.",
            ),
            ("b", "Close the incident as soon as the code is deployed."),
            ("c", "Assume success because no new complaints arrived in a minute."),
            ("d", "Delete the alarms so the incident cannot reopen."),
        ],
        "correct_option_ids": ["a"],
        "explanation": (
            "Recovery is confirmed by re-running the reproduction and observing "
            "metrics/traces return to healthy, with the result documented. "
            "Deploying is not verifying, brief quiet is not proof, and deleting "
            "alarms hides regressions."
        ),
        "rationales": {
            "a": (True, "Re-running the repro and checking telemetry confirms recovery."),
            "b": (False, "Deployment is not verification of the fix."),
            "c": (False, "A brief lull in complaints is not proof of recovery."),
            "d": (False, "Deleting alarms hides any recurrence."),
        },
    },
]


def question_count() -> int:
    """Return the number of authored Domain 5 questions."""
    return len(QUESTIONS)
