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

# Four generic options per question. Option "a" is the keyed-correct answer for
# every seed prompt; this is deliberately simple scaffolding for the local MVP
# and is replaced by domain-authored items in Phases 3-7.
_OPTIONS: tuple[tuple[str, str], ...] = (
    ("a", "Choose the design that directly satisfies the stated constraint."),
    ("b", "Choose a design that ignores the decisive constraint."),
    ("c", "Choose a more expensive design with no added benefit here."),
    ("d", "Defer the decision without addressing the constraint."),
)


def build_question_options() -> dict[str, tuple[tuple[str, str], ...]]:
    """Return option sets keyed by question ID."""
    return {prompt.question_id: _OPTIONS for prompt in build_seed_prompts()}


def build_answer_material() -> dict[str, dict[str, Any]]:
    """Return private answer material keyed by question ID."""
    material: dict[str, dict[str, Any]] = {}
    for prompt in build_seed_prompts():
        material[prompt.question_id] = {
            "correct_option_ids": ["a"],
            "rubric": (
                "Credit the response that names the decisive constraint and the "
                "trade-off that rules out the alternatives."
            ),
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
