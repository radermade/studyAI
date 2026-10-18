"""Phase 1 seed-content admission contract.

Enforces at least two original attributable scenario prompts for every one of
the 20 task IDs (>= 40 total). Public unanswered prompt payloads are
structurally incapable of carrying answer keys or rubrics; private answer
material lives in a separate model.
"""

from __future__ import annotations

from collections.abc import Sequence
from enum import StrEnum

from pydantic import Field, field_validator

from study_core.common import (
    ALL_TASK_IDS,
    StrictModel,
    ValidationIssue,
    is_valid_task_id,
)

MIN_PROMPTS_PER_TASK = 2
MIN_TOTAL_PROMPTS = 40

# Unsupported absolute terms that disqualify a scored prompt.
_FORBIDDEN_ABSOLUTES = ("always", "never", "guaranteed", "100% of the time")


class QuestionFormat(StrEnum):
    """Supported question formats."""

    MULTIPLE_CHOICE = "multiple_choice"
    MULTIPLE_RESPONSE = "multiple_response"


class Difficulty(StrEnum):
    """Relative difficulty of a prompt."""

    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class ReviewStatus(StrEnum):
    """Independent review state of a prompt."""

    DRAFT = "draft"
    REVIEWED = "reviewed"
    REJECTED = "rejected"


class QuestionAdmission(StrictModel):
    """Public admission metadata for one seed prompt.

    This model carries no answer key, rubric, correct-option flag, or hidden
    mock state. Private grading material is stored separately in Phase 1.
    """

    question_id: str
    objective_ids: tuple[str, ...] = Field(min_length=1)
    prompt: str = Field(min_length=1)
    scenario_constraint: str = Field(min_length=1)
    difficulty: Difficulty
    question_format: QuestionFormat
    source_ids: tuple[str, ...] = Field(min_length=1)
    review_status: ReviewStatus
    original: bool

    @field_validator("objective_ids")
    @classmethod
    def _valid_objectives(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        for objective_id in value:
            if not is_valid_task_id(objective_id):
                raise ValueError(f"unknown objective id: {objective_id}")
        return value


def _has_forbidden_absolute(prompt: QuestionAdmission) -> bool:
    text = f"{prompt.prompt} {prompt.scenario_constraint}".lower()
    return any(term in text for term in _FORBIDDEN_ABSOLUTES)


def validate_seed_bank(prompts: Sequence[QuestionAdmission]) -> tuple[ValidationIssue, ...]:
    """Return blocking issues for a seed bank.

    Enforces originality, per-task minimums, the total minimum, and quality
    blockers (unsupported absolutes). Prompts missing attribution or using
    unknown objectives are rejected by the model before reaching here.
    """
    issues: list[ValidationIssue] = []
    per_task: dict[str, int] = dict.fromkeys(ALL_TASK_IDS, 0)
    scorable = 0

    for prompt in prompts:
        if not prompt.original:
            issues.append(
                ValidationIssue(
                    code="seed.not_original",
                    path=f"{prompt.question_id}.original",
                    message=f"prompt {prompt.question_id} is not original/licensed",
                )
            )
            continue
        if _has_forbidden_absolute(prompt):
            issues.append(
                ValidationIssue(
                    code="seed.absolute_claim",
                    path=f"{prompt.question_id}.prompt",
                    message=f"prompt {prompt.question_id} uses an unsupported absolute",
                )
            )
            continue
        scorable += 1
        for objective_id in prompt.objective_ids:
            per_task[objective_id] = per_task.get(objective_id, 0) + 1

    for task_id, count in per_task.items():
        if count < MIN_PROMPTS_PER_TASK:
            issues.append(
                ValidationIssue(
                    code="seed.insufficient_task_coverage",
                    path=f"seed[{task_id}]",
                    message=(
                        f"task {task_id} has {count} prompts; "
                        f"at least {MIN_PROMPTS_PER_TASK} required"
                    ),
                )
            )
    if scorable < MIN_TOTAL_PROMPTS:
        issues.append(
            ValidationIssue(
                code="seed.insufficient_total",
                path="seed",
                message=f"{scorable} admissible prompts; at least {MIN_TOTAL_PROMPTS} required",
            )
        )
    return tuple(issues)
