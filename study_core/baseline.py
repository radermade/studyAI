"""Baseline diagnostic contract.

Captures a trustworthy baseline across the full blueprint. Unanswered responses
cannot expose answer keys; interrupted runs stay explicitly incomplete; and no
output is ever presented as an AWS score prediction.
"""

from __future__ import annotations

from collections.abc import Sequence
from datetime import datetime
from enum import StrEnum

from pydantic import Field, field_validator

from study_core.common import (
    ALL_TASK_IDS,
    StrictModel,
    ValidationIssue,
    ensure_utc,
    is_valid_task_id,
)


class BaselineKind(StrEnum):
    """Whether a baseline is an external pretest record or a local diagnostic."""

    OFFICIAL_EXTERNAL = "official_external"
    LOCAL_ORIGINAL = "local_original"


class BaselineState(StrEnum):
    """Lifecycle state of a baseline run."""

    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    INTERRUPTED = "interrupted"
    SUBMITTED = "submitted"
    SUMMARIZED = "summarized"


class BaselineResponse(StrictModel):
    """One captured response. Carries no answer key by construction."""

    question_id: str
    objective_ids: tuple[str, ...] = Field(min_length=1)
    answered: bool
    confidence: int = Field(ge=0, le=100)
    elapsed_seconds: float = Field(ge=0.0)

    @field_validator("objective_ids")
    @classmethod
    def _valid_objectives(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        for objective_id in value:
            if not is_valid_task_id(objective_id):
                raise ValueError(f"unknown objective id: {objective_id}")
        return value


class BaselineRun(StrictModel):
    """A baseline diagnostic run bound to a learner and blueprint version."""

    run_id: str
    learner_id: str
    kind: BaselineKind
    blueprint_version: str
    started_at: datetime
    state: BaselineState
    responses: tuple[BaselineResponse, ...] = ()

    @field_validator("started_at")
    @classmethod
    def _utc(cls, value: datetime) -> datetime:
        return ensure_utc(value)


class BaselineSummary(StrictModel):
    """Descriptive baseline result. Never an AWS score prediction."""

    run_id: str
    learner_id: str
    complete: bool
    answered_count: int = Field(ge=0)
    unanswered_count: int = Field(ge=0)
    per_task_answered: dict[str, int]
    mean_confidence: float = Field(ge=0.0, le=100.0)
    disclaimer: str = (
        "Baseline results are descriptive only and are not an AWS score "
        "prediction or readiness guarantee."
    )


def covers_all_tasks(responses: Sequence[BaselineResponse]) -> bool:
    """Return True when the responses collectively touch every task ID."""
    covered: set[str] = set()
    for response in responses:
        covered.update(response.objective_ids)
    return all(task_id in covered for task_id in ALL_TASK_IDS)


def summarize_baseline(run: BaselineRun) -> BaselineSummary:
    """Produce a descriptive summary from committed responses.

    An interrupted or unsubmitted run yields `complete=False` and never
    fabricates scores for unanswered items.
    """
    answered = [r for r in run.responses if r.answered]
    unanswered = [r for r in run.responses if not r.answered]
    per_task: dict[str, int] = {}
    for response in answered:
        for objective_id in response.objective_ids:
            per_task[objective_id] = per_task.get(objective_id, 0) + 1
    mean_conf = sum(r.confidence for r in answered) / len(answered) if answered else 0.0
    return BaselineSummary(
        run_id=run.run_id,
        learner_id=run.learner_id,
        complete=run.state == BaselineState.SUBMITTED and covers_all_tasks(run.responses),
        answered_count=len(answered),
        unanswered_count=len(unanswered),
        per_task_answered=per_task,
        mean_confidence=mean_conf,
    )


def validate_local_baseline(run: BaselineRun) -> tuple[ValidationIssue, ...]:
    """Return blocking issues for a local diagnostic run.

    A local baseline must sample every one of the 20 task IDs.
    """
    issues: list[ValidationIssue] = []
    if run.kind != BaselineKind.LOCAL_ORIGINAL:
        return ()
    covered: set[str] = set()
    for response in run.responses:
        covered.update(response.objective_ids)
    for task_id in ALL_TASK_IDS:
        if task_id not in covered:
            issues.append(
                ValidationIssue(
                    code="baseline.task_uncovered",
                    path="responses",
                    message=f"local baseline does not sample {task_id}",
                )
            )
    return tuple(issues)
