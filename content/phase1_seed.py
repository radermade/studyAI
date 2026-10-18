"""Phase 1 private answer material and searchable content for seed prompts.

Phase 0 admits public, answer-key-free prompts. Phase 1 adds the private
grading material and local lesson content needed to run the study loop. This
module is the single place that holds answer keys; they are never projected
into unanswered-question DTOs.
"""

from __future__ import annotations

from typing import Any

from study_core.common import ALL_TASK_IDS

from content.aip_c01 import build_seed_prompts
from content.domain1_questions import QUESTIONS as DOMAIN1_QUESTIONS
from content.domain2_questions import QUESTIONS as DOMAIN2_QUESTIONS
from content.domain3_questions import QUESTIONS as DOMAIN3_QUESTIONS
from content.domain4_questions import QUESTIONS as DOMAIN4_QUESTIONS
from content.labs import build_authored_labs, build_lab_curriculum_items

# All authored (non-placeholder) scenario questions across completed domains.
_AUTHORED_QUESTIONS: list[dict[str, Any]] = [
    *DOMAIN1_QUESTIONS,
    *DOMAIN2_QUESTIONS,
    *DOMAIN3_QUESTIONS,
    *DOMAIN4_QUESTIONS,
]

# Objectives with genuine authored coverage: an objective counts as authored
# only when it is the PRIMARY (first) objective of an authored question. A mere
# secondary tag does not create real coverage, so a placeholder for an objective
# that only ever appears as a secondary tag must NOT be suppressed.
_AUTHORED_OBJECTIVES = {q["objective_ids"][0] for q in _AUTHORED_QUESTIONS}

# Four generic options per placeholder question (option "a" is keyed-correct).
# Placeholders remain only for objectives without authored content yet.
_OPTIONS: tuple[tuple[str, str], ...] = (
    ("a", "Choose the design that directly satisfies the stated constraint."),
    ("b", "Choose a design that ignores the decisive constraint."),
    ("c", "Choose a more expensive design with no added benefit here."),
    ("d", "Defer the decision without addressing the constraint."),
)


def _is_placeholder_for_authored(objective_ids: tuple[str, ...]) -> bool:
    """True when a placeholder prompt targets an objective that now has real content."""
    return all(obj in _AUTHORED_OBJECTIVES for obj in objective_ids)


def build_rich_questions() -> list[dict[str, Any]]:
    """Return the authored scenario questions (Domains 1-2) in ingestion shape."""
    return _AUTHORED_QUESTIONS


def build_question_options() -> dict[str, tuple[tuple[str, str], ...]]:
    """Return option sets keyed by question ID (placeholders + authored)."""
    options: dict[str, tuple[tuple[str, str], ...]] = {}
    for prompt in build_seed_prompts():
        if _is_placeholder_for_authored(prompt.objective_ids):
            continue
        options[prompt.question_id] = _OPTIONS
    for question in _AUTHORED_QUESTIONS:
        options[question["question_id"]] = tuple((oid, text) for oid, text in question["options"])
    return options


def build_answer_material() -> dict[str, dict[str, Any]]:
    """Return private answer material keyed by question ID (placeholders + authored)."""
    material: dict[str, dict[str, Any]] = {}
    for prompt in build_seed_prompts():
        if _is_placeholder_for_authored(prompt.objective_ids):
            continue
        material[prompt.question_id] = {
            "correct_option_ids": ["a"],
            "rubric": (
                "Credit the response that names the decisive constraint and the "
                "trade-off that rules out the alternatives."
            ),
            "explanation": "",
            "rationales": {},
        }
    for question in _AUTHORED_QUESTIONS:
        material[question["question_id"]] = {
            "correct_option_ids": question["correct_option_ids"],
            "rubric": question["explanation"],
            "explanation": question["explanation"],
            "rationales": question["rationales"],
        }
    return material


def build_content_units() -> list[dict[str, Any]]:
    """Return searchable local lesson content units, one per task objective."""
    units: list[dict[str, Any]] = []
    for task_id in ALL_TASK_IDS:
        domain = task_id.split("-")[1].split(".")[0]
        units.append(
            {
                "content_id": f"content-{task_id}",
                "title": f"Study note for {task_id}",
                "body": (
                    f"This note summarizes the architecture trade-offs behind {task_id}. "
                    "It distinguishes AWS-documented behavior from project recommendations "
                    "and lists common failure modes and a verification method."
                ),
                "source_ids": [f"aip-c01-domain-{domain}"],
                "objective_ids": [task_id],
                "freshness": "current",
            }
        )
    return units


def build_curriculum() -> list[dict[str, Any]]:
    """Return curriculum items: one lesson per objective plus one sample lab."""
    items: list[dict[str, Any]] = []
    for order, task_id in enumerate(ALL_TASK_IDS, start=1):
        items.append(
            {
                "item_id": f"lesson-{task_id}",
                "item_type": "lesson",
                "title": f"Lesson: {task_id}",
                "display_order": order,
                "objective_ids": [task_id],
                "prerequisites": [],
                "content_ref": f"content-{task_id}",
            }
        )
    items.extend(build_lab_curriculum_items(start_order=len(ALL_TASK_IDS) + 1))
    return items


def build_lab_definitions() -> list[dict[str, Any]]:
    """Return the authored hands-on labs (1-4) for the lab workflow.

    Lab content is authored in ``content/labs.py``; this adapter keeps the
    ingestion call site stable. Later phases append labs 5-12.
    """
    return build_authored_labs()
