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
    items.append(
        {
            "item_id": "lab-01-model-comparison",
            "item_type": "lab",
            "title": "Lab 1: Bedrock model comparison",
            "display_order": len(ALL_TASK_IDS) + 1,
            "objective_ids": ["AIP-1.1", "AIP-1.2", "AIP-2.2", "AIP-4.1"],
            "prerequisites": ["lesson-AIP-1.2"],
            "content_ref": "lab-01-model-comparison",
        }
    )
    return items


def build_lab_definitions() -> list[dict[str, Any]]:
    """Return one fully-formed sample lab (Lab 1) for the Phase 2 lab workflow.

    Phases 3-7 author the remaining labs; Phase 2 only needs a working lifecycle.
    """
    return [
        {
            "lab_id": "lab-01-model-comparison",
            "title": "Lab 1: Bedrock model comparison",
            "objective_ids": ["AIP-1.1", "AIP-1.2", "AIP-2.2", "AIP-4.1"],
            "cost_class": "low",
            "regions": ["us-east-1"],
            "architecture": (
                "Invoke multiple Bedrock foundation models and compare quality, "
                "latency, and cost for one representative prompt."
            ),
            "cleanup": "No persistent resources are created; confirm none remain.",
            "steps": [
                {
                    "step_id": "s1",
                    "display_order": 1,
                    "instruction": "Open the Bedrock console and confirm model access.",
                    "prediction_prompt": "Which models will appear for your account/region?",
                    "mandatory": True,
                },
                {
                    "step_id": "s2",
                    "display_order": 2,
                    "instruction": "Invoke two models with the same prompt and record results.",
                    "prediction_prompt": "Predict which model is faster and which is cheaper.",
                    "mandatory": True,
                },
            ],
            "checkpoints": [
                {
                    "checkpoint_id": "c1-model-access",
                    "validator_id": "bedrock-models-present",
                    "is_cleanup": False,
                    "mandatory": True,
                },
                {
                    "checkpoint_id": "c2-comparison-recorded",
                    "validator_id": None,
                    "is_cleanup": False,
                    "mandatory": False,
                },
            ],
        }
    ]
