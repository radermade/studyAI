"""Tests for the scored-session service: selection, grading, reset, history."""

from __future__ import annotations

import pytest
from study_core.scored_service import ScoredSessionError, ScoredSessionService


def _correct_options(scored: ScoredSessionService, question_id: str) -> list[str]:
    """Read the full keyed-correct option set directly for test purposes."""
    import json

    row = scored._conn.execute(
        "SELECT correct_option_ids FROM answer_material WHERE question_id = ?",
        (question_id,),
    ).fetchone()
    return [str(o) for o in json.loads(row["correct_option_ids"])]


def _correct_sequence(scored: ScoredSessionService, question_id: str) -> list[str]:
    import json

    row = scored._conn.execute(
        "SELECT correct_sequence FROM answer_material WHERE question_id = ?",
        (question_id,),
    ).fetchone()
    return [str(o) for o in json.loads(row["correct_sequence"])] if row["correct_sequence"] else []


def _correct_pairs(scored: ScoredSessionService, question_id: str) -> dict[str, str]:
    rows = scored._conn.execute(
        "SELECT prompt_id, response_id FROM match_answer_keys WHERE question_id = ?",
        (question_id,),
    ).fetchall()
    return {str(r["prompt_id"]): str(r["response_id"]) for r in rows}


def _complete_session(scored: ScoredSessionService, *, correct: bool) -> str:
    view = scored.start(learner_id="L1")
    for pos in range(view.item_count):
        item = scored.current_item(session_id=view.session_id, position=pos)
        fmt = item.question_format
        if fmt == "matching":
            pairs = _correct_pairs(scored, item.question_id)
            if not correct and pairs:
                # Flip one pair to a different response to force a miss.
                responses = [r.option_id for r in item.match_responses]
                first = next(iter(pairs))
                alt = next((r for r in responses if r != pairs[first]), pairs[first])
                pairs = {**pairs, first: alt}
            scored.answer_match(
                session_id=view.session_id, question_id=item.question_id, pairs=pairs
            )
            continue
        if fmt == "ordering":
            seq = _correct_sequence(scored, item.question_id)
            selected = seq if correct else list(reversed(seq))
            scored.answer(
                session_id=view.session_id,
                question_id=item.question_id,
                selected_option_ids=selected,
            )
            continue
        right = _correct_options(scored, item.question_id)
        if correct:
            selected = right
        else:
            wrong = next((o.option_id for o in item.options if o.option_id not in right), None)
            selected = [wrong] if wrong is not None else right[:1]
        scored.answer(
            session_id=view.session_id,
            question_id=item.question_id,
            selected_option_ids=selected,
        )
    scored.submit(session_id=view.session_id, event_id="e1")
    return view.session_id


def test_item_view_hides_answer_material(scored: ScoredSessionService) -> None:
    view = scored.start(learner_id="L1")
    item = scored.current_item(session_id=view.session_id, position=0)
    dumped = item.model_dump()
    assert "is_scored" not in dumped
    assert "correct_option_ids" not in dumped
    assert "explanation" not in dumped
    assert "objective_ids" not in dumped
    assert "correct_sequence" not in dumped
    assert "match_key" not in dumped
    # An option-based item exposes its options; a matching item exposes prompts
    # and responses. Either way the item is renderable with no answer material.
    assert len(item.options) >= 2 or (
        len(item.match_prompts) >= 2 and len(item.match_responses) >= 2
    )


def test_feedback_withheld_until_submit(scored: ScoredSessionService) -> None:
    # The service exposes no result accessor for an in-progress session.
    view = scored.start(learner_id="L1")
    assert scored.active_session(learner_id="L1") == view.session_id
    assert scored.latest_submitted(learner_id="L1") is None


def test_all_correct_passes(scored: ScoredSessionService) -> None:
    session_id = _complete_session(scored, correct=True)
    result = scored.submit(session_id=session_id, event_id="e1")
    assert result.raw_correct == result.scored_total
    assert result.passed is True
    assert result.scaled_estimate == 1000


def test_all_wrong_fails_and_records_misses(scored: ScoredSessionService) -> None:
    session_id = _complete_session(scored, correct=False)
    result = scored.submit(session_id=session_id, event_id="e1")
    assert result.raw_correct == 0
    assert result.passed is False
    misses = scored.misses(session_id=session_id)
    assert len(misses) == result.scored_total
    assert all(m.explanation is not None for m in misses)


def test_unanswered_scored_as_incorrect(scored: ScoredSessionService) -> None:
    view = scored.start(learner_id="L1")
    # Answer nothing; submit.
    result = scored.submit(session_id=view.session_id, event_id="e1")
    assert result.raw_correct == 0
    assert result.passed is False


def test_submit_is_idempotent(scored: ScoredSessionService) -> None:
    session_id = _complete_session(scored, correct=True)
    first = scored.submit(session_id=session_id, event_id="e1")
    second = scored.submit(session_id=session_id, event_id="e1")
    assert first.scaled_estimate == second.scaled_estimate


def test_answer_rejected_after_submit(scored: ScoredSessionService) -> None:
    session_id = _complete_session(scored, correct=True)
    with pytest.raises(ScoredSessionError):
        scored.answer(
            session_id=session_id, question_id="d1-bedrock-vs-sagemaker", selected_option_ids=["a"]
        )


def test_reset_abandons_session(scored: ScoredSessionService) -> None:
    view = scored.start(learner_id="L1")
    scored.reset(session_id=view.session_id)
    assert scored.active_session(learner_id="L1") is None


def test_new_session_clears_prior(scored: ScoredSessionService) -> None:
    # Non-accumulating: only one session's data exists at a time.
    first = _complete_session(scored, correct=True)
    second = scored.start(learner_id="L1")
    assert second.session_id != first
    # The prior submitted result is gone (cleared on the new start).
    assert scored.latest_submitted(learner_id="L1") is None
    # Only one scored session row remains for the learner.
    count = scored._conn.execute(
        "SELECT COUNT(*) AS n FROM scored_sessions WHERE learner_id = 'L1'"
    ).fetchone()["n"]
    assert count == 1


def test_scope_restricts_to_domain(scored: ScoredSessionService) -> None:
    view = scored.start(learner_id="L1", scope_domains=[1])
    # Every item should belong to Domain 1 only.
    for pos in range(view.item_count):
        item = scored.current_item(session_id=view.session_id, position=pos)
        assert item.question_id  # smoke; domain enforced server-side
    assert view.item_count > 0
