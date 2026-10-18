"""Thin handlers mapping typed requests to study-core use cases.

Each handler validates one request model, invokes one use case, and maps known
domain errors to a stable `ErrorEnvelope`. Handlers contain no business rules.
"""

from __future__ import annotations

from typing import Any

from pydantic import ValidationError
from study_core.errors import ConflictError, Phase0Error
from study_core.service import ContentGapError, NotFoundError, StudyService
from study_core.study_models import SessionMode

from study_mcp.contracts import (
    DueReviewRequest,
    ErrorCategory,
    ErrorEnvelope,
    GradeRequest,
    NextQuestionRequest,
    ProgressRequest,
    SearchRequest,
    StartSessionRequest,
)

# Stable tool names. This set is the complete Phase 1 allowlist.
TOOL_NAMES: tuple[str, ...] = (
    "start_session",
    "next_question",
    "grade_and_record",
    "get_due_reviews",
    "get_progress",
    "search_local_material",
)


def _error(category: ErrorCategory, message: str) -> dict[str, Any]:
    return {"error": ErrorEnvelope(category=category, message=message).model_dump(mode="json")}


def _map_domain_error(exc: Exception) -> dict[str, Any]:
    if isinstance(exc, ValidationError):
        return _error(ErrorCategory.VALIDATION, "invalid request payload")
    if isinstance(exc, ConflictError):
        return _error(ErrorCategory.CONFLICT, str(exc))
    if isinstance(exc, NotFoundError):
        return _error(ErrorCategory.NOT_FOUND, str(exc))
    if isinstance(exc, ContentGapError):
        return _error(ErrorCategory.UNAVAILABLE_DEPENDENCY, str(exc))
    if isinstance(exc, ValueError):
        return _error(ErrorCategory.VALIDATION, str(exc))
    if isinstance(exc, Phase0Error):
        return _error(ErrorCategory.PERSISTENCE, str(exc))
    raise exc


class ToolRouter:
    """Routes a tool name and raw arguments to the matching use case."""

    def __init__(self, service: StudyService) -> None:
        self._service = service

    def call(self, tool: str, arguments: dict[str, Any]) -> dict[str, Any]:
        """Dispatch one tool call and return a JSON-safe result or error."""
        if tool not in TOOL_NAMES:
            return _error(ErrorCategory.VALIDATION, f"unknown tool: {tool}")
        try:
            return self._dispatch(tool, arguments)
        except (ValidationError, Phase0Error, ValueError) as exc:
            return _map_domain_error(exc)

    def _dispatch(self, tool: str, arguments: dict[str, Any]) -> dict[str, Any]:
        if tool == "start_session":
            req = StartSessionRequest.model_validate(arguments)
            result = self._service.start_session(
                learner_id=req.learner_id,
                mode=SessionMode(req.mode),
                objective_filter=req.objective_filter,
                request_id=req.request_id,
            )
            return {"result": result.model_dump(mode="json")}
        if tool == "next_question":
            req_nq = NextQuestionRequest.model_validate(arguments)
            question = self._service.next_question(
                session_id=req_nq.session_id, request_id=req_nq.request_id
            )
            return {"result": question.model_dump(mode="json")}
        if tool == "grade_and_record":
            req_g = GradeRequest.model_validate(arguments)
            grade = self._service.grade_and_record(
                session_id=req_g.session_id,
                question_id=req_g.question_id,
                selected_option_ids=req_g.selected_option_ids,
                confidence=req_g.confidence,
                elapsed_seconds=req_g.elapsed_seconds,
                event_id=req_g.event_id,
            )
            return {"result": grade.model_dump(mode="json")}
        if tool == "get_due_reviews":
            req_d = DueReviewRequest.model_validate(arguments)
            page = self._service.get_due_reviews(
                learner_id=req_d.learner_id, objective_filter=req_d.objective_filter
            )
            return {"result": page.model_dump(mode="json")}
        if tool == "get_progress":
            req_p = ProgressRequest.model_validate(arguments)
            report = self._service.get_progress(learner_id=req_p.learner_id)
            return {"result": report.model_dump(mode="json")}
        # search_local_material
        req_s = SearchRequest.model_validate(arguments)
        search = self._service.search_local_material(
            query=req_s.query,
            objective_filter=req_s.objective_filter,
            limit=req_s.limit,
            offset=req_s.offset,
        )
        return {"result": search.model_dump(mode="json")}
