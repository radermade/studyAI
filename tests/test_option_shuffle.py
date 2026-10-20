"""Tests that answer options are shuffled so position is not predictable."""

from __future__ import annotations

from study_core.common import stable_shuffle
from study_core.scored_service import ScoredSessionService
from study_core.service import StudyService
from study_core.study_models import SessionMode


def test_stable_shuffle_is_stable_per_key() -> None:
    items = ["a", "b", "c", "d"]
    first = stable_shuffle(items, seed_key="s1:q1")
    again = stable_shuffle(items, seed_key="s1:q1")
    assert first == again  # stable for the same key


def test_stable_shuffle_varies_across_keys() -> None:
    items = [str(i) for i in range(8)]
    orders = {tuple(stable_shuffle(items, seed_key=f"s:{i}")) for i in range(20)}
    # Many distinct orders across different keys (not all identical).
    assert len(orders) > 1


def test_scored_first_option_is_not_always_correct(scored: ScoredSessionService) -> None:
    """Picking the first displayed option every time must not always be correct."""
    view = scored.start(learner_id="L1")
    # Collect the first displayed option id for each item; if the correct answer
    # were always first, grading all-first would score 100%. We assert the
    # displayed first options are not all the stored 'a'.
    first_ids = []
    for pos in range(view.item_count):
        item = scored.current_item(session_id=view.session_id, position=pos)
        # Matching items carry no plain options; only inspect option-based items.
        if item.options:
            first_ids.append(item.options[0].option_id)
    # At least some items should present a non-'a' option first.
    assert any(oid != "a" for oid in first_ids)


def test_grill_grading_uses_ids_not_position(service: StudyService) -> None:
    """Grading must track the chosen option id regardless of display order."""
    session = service.start_session(
        learner_id="L1", mode=SessionMode.GRILL, objective_filter=("AIP-1.1",), request_id="r1"
    )
    question = service.next_question(session_id=session.session_id, request_id="nq1")
    # Pick the displayed first option; its id may not be 'a'.
    first = question.options[0]
    grade = service.grade_and_record(
        session_id=session.session_id,
        question_id=question.question_id,
        selected_option_ids=[first.option_id],
        confidence=50,
        elapsed_seconds=5.0,
        event_id="e1",
    )
    # Whatever the outcome, it must reflect the chosen id, which is exposed via
    # explain_answer's correct set.
    explanation = service.explain_answer(
        session_id=session.session_id, question_id=question.question_id
    )
    expected_correct = first.option_id in explanation.correct_option_ids
    assert (grade.outcome.value == "correct") == expected_correct
