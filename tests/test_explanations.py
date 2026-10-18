"""Tests for authored Domain 1 questions and post-answer explanations."""

from __future__ import annotations

import pytest
from content.domain1_questions import QUESTIONS
from study_core.service import NotFoundError, StudyService
from study_core.study_models import SessionMode


def test_authored_questions_are_well_formed() -> None:
    for q in QUESTIONS:
        option_ids = {oid for oid, _ in q["options"]}
        assert len(option_ids) == len(q["options"]), f"duplicate option in {q['question_id']}"
        assert q["correct_option_ids"], f"no correct answer in {q['question_id']}"
        for cid in q["correct_option_ids"]:
            assert cid in option_ids, f"correct id not an option in {q['question_id']}"
        # Every option has a rationale and the correct ones are flagged correct.
        for oid in option_ids:
            is_correct, rationale = q["rationales"][oid]
            assert rationale, f"empty rationale for {q['question_id']}/{oid}"
            assert is_correct == (oid in q["correct_option_ids"])
        assert q["explanation"], f"no explanation in {q['question_id']}"


def _answer_first(service: StudyService) -> tuple[str, str]:
    session = service.start_session(
        learner_id="L1", mode=SessionMode.GRILL, objective_filter=(), request_id="r1"
    )
    question = service.next_question(session_id=session.session_id, request_id="nq1")
    service.grade_and_record(
        session_id=session.session_id,
        question_id=question.question_id,
        selected_option_ids=[question.options[0].option_id],
        confidence=50,
        elapsed_seconds=10.0,
        event_id="e1",
    )
    return session.session_id, question.question_id


def test_explanation_available_after_answering(service: StudyService) -> None:
    session_id, question_id = _answer_first(service)
    explanation = service.explain_answer(session_id=session_id, question_id=question_id)
    assert explanation.correct_option_ids
    assert explanation.explanation
    assert explanation.option_rationales


def test_explanation_requires_prior_attempt(service: StudyService) -> None:
    session = service.start_session(
        learner_id="L1", mode=SessionMode.GRILL, objective_filter=(), request_id="r1"
    )
    with pytest.raises(NotFoundError):
        service.explain_answer(session_id=session.session_id, question_id="d1-bedrock-vs-sagemaker")


def test_served_question_hides_answer(service: StudyService) -> None:
    session = service.start_session(
        learner_id="L1", mode=SessionMode.GRILL, objective_filter=(), request_id="r1"
    )
    question = service.next_question(session_id=session.session_id, request_id="nq1")
    dumped = question.model_dump()
    assert "correct_option_ids" not in dumped
    assert "explanation" not in dumped
    assert len(question.options) >= 2
