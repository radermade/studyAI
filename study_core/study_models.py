"""Study-domain value objects and the secure unanswered-question DTO.

`UnansweredQuestion` is structurally incapable of carrying answer keys, rubrics,
or correctness markers: those fields simply do not exist on the type.
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import Field

from study_core.common import StrictModel


class SessionMode(StrEnum):
    """How a study session selects and presents questions."""

    GRILL = "grill"
    REVIEW = "review"


class SessionState(StrEnum):
    """Lifecycle of a session."""

    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


class GradeOutcome(StrEnum):
    """Result of grading an attempt."""

    CORRECT = "correct"
    INCORRECT = "incorrect"
    GRADING_UNCERTAIN = "grading_uncertain"


class ReviewState(StrEnum):
    """Lifecycle of a spaced-review schedule."""

    SCHEDULED = "scheduled"
    RESOLVED = "resolved"
    SUPERSEDED = "superseded"


class QuestionOption(StrictModel):
    """A selectable option shown to the learner (no correctness flag)."""

    option_id: str
    text: str


class UnansweredQuestion(StrictModel):
    """Public question projection. Carries no answer, rubric, or correctness."""

    question_id: str
    prompt: str
    scenario_constraint: str
    question_format: str
    options: tuple[QuestionOption, ...]
    objective_ids: tuple[str, ...]
    source_ids: tuple[str, ...]


class SessionResult(StrictModel):
    """A durable session reference returned to callers."""

    session_id: str
    learner_id: str
    mode: SessionMode
    state: SessionState
    blueprint_version: str
    started_at: datetime


class GradeResult(StrictModel):
    """Committed grading summary."""

    attempt_id: str
    question_id: str
    outcome: GradeOutcome
    confidence: int = Field(ge=0, le=100)
    next_review_due_at: datetime | None


class DueReview(StrictModel):
    """One due review item."""

    review_id: str
    question_id: str
    objective_id: str
    due_at: datetime


class DueReviewPage(StrictModel):
    """A deterministic page of due reviews."""

    items: tuple[DueReview, ...]


class ObjectiveProgress(StrictModel):
    """Evidence-derived progress for a single objective."""

    objective_id: str
    attempts: int
    correct: int
    accuracy: float | None
    mean_confidence: float | None
    open_misconceptions: int


class ProgressReport(StrictModel):
    """Evidence-based progress across objectives.

    `is_estimate` and `inputs` make clear this is an internal estimate and not
    an AWS score prediction.
    """

    learner_id: str
    objectives: tuple[ObjectiveProgress, ...]
    uncovered_objectives: tuple[str, ...]
    is_estimate: bool = True
    note: str = "Internal estimate derived from committed evidence; not an AWS score."


class SearchResult(StrictModel):
    """One attributed local search hit."""

    content_id: str
    title: str
    snippet: str
    objective_ids: tuple[str, ...]
    freshness: str


class SearchPage(StrictModel):
    """A deterministic page of search results."""

    results: tuple[SearchResult, ...]
    offset: int
    has_more: bool
