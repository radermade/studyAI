"""Tests for the study service: sessions, grading, reviews, progress, search."""

from __future__ import annotations

import pytest
from study_core.errors import ConflictError
from study_core.scheduling import next_interval_days
from study_core.service import ContentGapError, NotFoundError, StudyService
from study_core.study_models import GradeOutcome, SessionMode

from tests.conftest import FakeClock


def _start(service: StudyService) -> str:
    session = service.start_session(
        learner_id="L1", mode=SessionMode.GRILL, objective_filter=(), request_id="r1"
    )
    return session.session_id


def test_start_session_is_idempotent(service: StudyService) -> None:
    a = service.start_session(
        learner_id="L1", mode=SessionMode.GRILL, objective_filter=(), request_id="r1"
    )
    b = service.start_session(
        learner_id="L1", mode=SessionMode.GRILL, objective_filter=(), request_id="r1"
    )
    assert a.session_id == b.session_id


def test_start_session_conflict_on_payload_change(service: StudyService) -> None:
    service.start_session(
        learner_id="L1", mode=SessionMode.GRILL, objective_filter=(), request_id="r1"
    )
    with pytest.raises(ConflictError):
        service.start_session(
            learner_id="L2", mode=SessionMode.GRILL, objective_filter=(), request_id="r1"
        )


def test_next_question_returns_no_answer_material(service: StudyService) -> None:
    session_id = _start(service)
    question = service.next_question(session_id=session_id, request_id="nq1")
    dumped = question.model_dump()
    assert "answer" not in dumped
    assert "rubric" not in dumped
    assert "correct_option_ids" not in dumped
    assert len(question.options) == 4


def test_next_question_idempotent(service: StudyService) -> None:
    session_id = _start(service)
    first = service.next_question(session_id=session_id, request_id="nq1")
    second = service.next_question(session_id=session_id, request_id="nq1")
    assert first.question_id == second.question_id


def test_next_question_unknown_session(service: StudyService) -> None:
    with pytest.raises(NotFoundError):
        service.next_question(session_id="missing", request_id="nq1")


def test_objective_filter_restricts_selection(service: StudyService) -> None:
    session = service.start_session(
        learner_id="L1",
        mode=SessionMode.GRILL,
        objective_filter=("AIP-3.2",),
        request_id="r1",
    )
    question = service.next_question(session_id=session.session_id, request_id="nq1")
    assert "AIP-3.2" in question.objective_ids


def test_grade_correct_schedules_review(service: StudyService) -> None:
    session_id = _start(service)
    question = service.next_question(session_id=session_id, request_id="nq1")
    grade = service.grade_and_record(
        session_id=session_id,
        question_id=question.question_id,
        selected_option_ids=["a"],
        confidence=80,
        elapsed_seconds=20.0,
        event_id="e1",
    )
    assert grade.outcome == GradeOutcome.CORRECT
    assert grade.next_review_due_at is not None


def test_grade_incorrect_opens_misconception(service: StudyService) -> None:
    session_id = _start(service)
    question = service.next_question(session_id=session_id, request_id="nq1")
    service.grade_and_record(
        session_id=session_id,
        question_id=question.question_id,
        selected_option_ids=["b"],
        confidence=40,
        elapsed_seconds=20.0,
        event_id="e1",
    )
    progress = service.get_progress(learner_id="L1")
    target = next(o for o in progress.objectives if o.objective_id in question.objective_ids)
    assert target.open_misconceptions >= 1


def test_grade_requires_served_question(service: StudyService) -> None:
    session_id = _start(service)
    with pytest.raises(NotFoundError):
        service.grade_and_record(
            session_id=session_id,
            question_id="seed-AIP-1.1-1",
            selected_option_ids=["a"],
            confidence=50,
            elapsed_seconds=10.0,
            event_id="e1",
        )


def test_grade_idempotent_replay(service: StudyService) -> None:
    session_id = _start(service)
    question = service.next_question(session_id=session_id, request_id="nq1")
    first = service.grade_and_record(
        session_id=session_id,
        question_id=question.question_id,
        selected_option_ids=["a"],
        confidence=80,
        elapsed_seconds=20.0,
        event_id="e1",
    )
    second = service.grade_and_record(
        session_id=session_id,
        question_id=question.question_id,
        selected_option_ids=["a"],
        confidence=80,
        elapsed_seconds=20.0,
        event_id="e1",
    )
    assert first.attempt_id == second.attempt_id


def test_due_reviews_respects_clock(service: StudyService, clock: FakeClock) -> None:
    session_id = _start(service)
    question = service.next_question(session_id=session_id, request_id="nq1")
    service.grade_and_record(
        session_id=session_id,
        question_id=question.question_id,
        selected_option_ids=["a"],
        confidence=80,
        elapsed_seconds=20.0,
        event_id="e1",
    )
    # Correct answer -> 1 day interval; nothing due yet.
    assert service.get_due_reviews(learner_id="L1").items == ()
    clock.advance(2)
    due = service.get_due_reviews(learner_id="L1")
    assert len(due.items) == 1


def test_progress_marks_uncovered(service: StudyService) -> None:
    progress = service.get_progress(learner_id="L1")
    assert len(progress.uncovered_objectives) == 20
    assert progress.is_estimate is True


def test_search_returns_attributed_hits(service: StudyService) -> None:
    page = service.search_local_material(query="architecture", limit=5)
    assert len(page.results) == 5
    assert all(r.objective_ids for r in page.results)


def test_search_rejects_bad_limit(service: StudyService) -> None:
    with pytest.raises(ValueError):
        service.search_local_material(query="architecture", limit=0)


def test_search_empty_query_rejected(service: StudyService) -> None:
    with pytest.raises(ValueError):
        service.search_local_material(query="!!!", limit=5)


def test_no_content_raises_gap(service: StudyService) -> None:
    # Filter to a single objective, drain every eligible question, then the
    # next request must raise a content gap. The count is not hard-coded so the
    # test stays valid as authored coverage for the objective changes.
    session = service.start_session(
        learner_id="L1",
        mode=SessionMode.GRILL,
        objective_filter=("AIP-5.2",),
        request_id="r1",
    )
    with pytest.raises(ContentGapError):
        for i in range(50):  # bounded drain; the pool is far smaller
            service.next_question(session_id=session.session_id, request_id=f"nq{i}")


def test_scheduling_progression() -> None:
    assert next_interval_days(0, GradeOutcome.CORRECT) == 1
    assert next_interval_days(1, GradeOutcome.CORRECT) == 3
    assert next_interval_days(7, GradeOutcome.INCORRECT) == 1
