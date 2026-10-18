"""Typed MCP request models and the stable error envelope.

Each tool has an explicit Pydantic request model with `extra="forbid"`. Known
domain failures map to a closed set of error categories.
"""

from __future__ import annotations

from enum import StrEnum

from pydantic import Field
from study_core.common import StrictModel


class ErrorCategory(StrEnum):
    """Closed set of MCP error categories."""

    VALIDATION = "validation"
    CONFLICT = "conflict"
    UNAVAILABLE_DEPENDENCY = "unavailable_dependency"
    AUTHORIZATION = "authorization"
    NOT_FOUND = "not_found"
    PERSISTENCE = "persistence"
    INTERNAL = "internal"


class ErrorEnvelope(StrictModel):
    """A stable, non-sensitive error result."""

    category: ErrorCategory
    message: str


class StartSessionRequest(StrictModel):
    """Request to start or resume a session."""

    learner_id: str = Field(min_length=1)
    mode: str = Field(min_length=1)
    objective_filter: tuple[str, ...] = ()
    request_id: str = Field(min_length=1)


class NextQuestionRequest(StrictModel):
    """Request to serve the next eligible question."""

    session_id: str = Field(min_length=1)
    request_id: str = Field(min_length=1)


class GradeRequest(StrictModel):
    """Request to grade and record one attempt."""

    session_id: str = Field(min_length=1)
    question_id: str = Field(min_length=1)
    selected_option_ids: tuple[str, ...] = ()
    confidence: int = Field(ge=0, le=100)
    elapsed_seconds: float = Field(ge=0.0)
    event_id: str = Field(min_length=1)


class DueReviewRequest(StrictModel):
    """Request for due reviews."""

    learner_id: str = Field(min_length=1)
    objective_filter: tuple[str, ...] = ()


class ProgressRequest(StrictModel):
    """Request for progress."""

    learner_id: str = Field(min_length=1)


class SearchRequest(StrictModel):
    """Request to search local material."""

    query: str = Field(min_length=1)
    objective_filter: tuple[str, ...] = ()
    limit: int = Field(default=20, ge=1)
    offset: int = Field(default=0, ge=0)
