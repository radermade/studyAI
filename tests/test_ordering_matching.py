"""End-to-end tests for ordering and matching questions through the scored path.

Exercises ingestion -> item projection -> answer -> submit -> grade for both new
formats, and confirms the item projection never leaks the answer key.
"""

from __future__ import annotations

from study_core.db import DbConnection
from study_core.ports import SystemRandom
from study_core.scored_service import ScoredSessionService

from tests.conftest import FakeClock


def _service(connection: DbConnection, clock: FakeClock) -> ScoredSessionService:
    return ScoredSessionService(connection, clock, SystemRandom(seed=7))


def _ordering_key(connection: DbConnection, question_id: str) -> list[str]:
    import json

    row = connection.execute(
        "SELECT correct_sequence FROM answer_material WHERE question_id = ?",
        (question_id,),
    ).fetchone()
    return [str(o) for o in json.loads(row["correct_sequence"])]


def _matching_key(connection: DbConnection, question_id: str) -> dict[str, str]:
    rows = connection.execute(
        "SELECT prompt_id, response_id FROM match_answer_keys WHERE question_id = ?",
        (question_id,),
    ).fetchall()
    return {str(r["prompt_id"]): str(r["response_id"]) for r in rows}


def test_ordering_question_is_ingested_and_scored(
    connection: DbConnection, clock: FakeClock
) -> None:
    scored = _service(connection, clock)
    view = scored.start(learner_id="LO")
    pos = _first_item_of_format(scored, view.session_id, view.item_count, "ordering")
    assert pos is not None, "an ordering question should be selected into the session"

    item = scored.current_item(session_id=view.session_id, position=pos)
    # The projection exposes the step options but never the correct sequence.
    assert len(item.options) >= 3
    assert "correct_sequence" not in item.model_dump()

    key = _ordering_key(connection, item.question_id)
    scored.answer(session_id=view.session_id, question_id=item.question_id, selected_option_ids=key)
    scored.submit(session_id=view.session_id, event_id="e-ord")
    misses = {m.question_id for m in scored.misses(session_id=view.session_id)}
    assert item.question_id not in misses


def test_ordering_wrong_order_is_incorrect(connection: DbConnection, clock: FakeClock) -> None:
    scored = _service(connection, clock)
    view = scored.start(learner_id="LO2")
    pos = _first_item_of_format(scored, view.session_id, view.item_count, "ordering")
    assert pos is not None
    item = scored.current_item(session_id=view.session_id, position=pos)
    key = _ordering_key(connection, item.question_id)
    # Right members, reversed order (not a palindrome for 3+ distinct steps).
    scored.answer(
        session_id=view.session_id,
        question_id=item.question_id,
        selected_option_ids=list(reversed(key)),
    )
    scored.submit(session_id=view.session_id, event_id="e-ord2")
    misses = {m.question_id for m in scored.misses(session_id=view.session_id)}
    assert item.question_id in misses


def test_matching_question_is_ingested_and_scored(
    connection: DbConnection, clock: FakeClock
) -> None:
    scored = _service(connection, clock)
    view = scored.start(learner_id="LM")
    pos = _first_item_of_format(scored, view.session_id, view.item_count, "matching")
    assert pos is not None, "a matching question should be selected into the session"

    item = scored.current_item(session_id=view.session_id, position=pos)
    assert len(item.match_prompts) >= 3
    assert len(item.match_responses) >= 3
    assert "match_key" not in item.model_dump()  # the key is never projected

    key = _matching_key(connection, item.question_id)
    scored.answer_match(session_id=view.session_id, question_id=item.question_id, pairs=key)
    scored.submit(session_id=view.session_id, event_id="e-match")
    misses = {m.question_id for m in scored.misses(session_id=view.session_id)}
    assert item.question_id not in misses


def test_matching_one_wrong_pair_is_incorrect(connection: DbConnection, clock: FakeClock) -> None:
    scored = _service(connection, clock)
    view = scored.start(learner_id="LM2")
    pos = _first_item_of_format(scored, view.session_id, view.item_count, "matching")
    assert pos is not None
    item = scored.current_item(session_id=view.session_id, position=pos)
    key = _matching_key(connection, item.question_id)
    response_ids = [r.option_id for r in item.match_responses]
    first = next(iter(key))
    alt = next(r for r in response_ids if r != key[first])
    wrong = {**key, first: alt}  # exactly one pair wrong
    scored.answer_match(session_id=view.session_id, question_id=item.question_id, pairs=wrong)
    scored.submit(session_id=view.session_id, event_id="e-match2")
    misses = {m.question_id for m in scored.misses(session_id=view.session_id)}
    assert item.question_id in misses


def _first_item_of_format(
    scored: ScoredSessionService, session_id: str, total: int, fmt: str
) -> int | None:
    """Return the position of the first SCORED item of the given format.

    Unscored items do not affect the result or the miss list, so the grading
    assertions must target a scored item. `is_scored` is intentionally hidden
    from the item view, so the test reads it from the session table directly.
    """
    scored_positions = {
        int(r["position"])
        for r in scored._conn.execute(
            "SELECT position FROM scored_session_items WHERE session_id = ? AND is_scored = 1",
            (session_id,),
        ).fetchall()
    }
    for pos in range(total):
        if pos not in scored_positions:
            continue
        item = scored.current_item(session_id=session_id, position=pos)
        if item.question_format == fmt:
            return pos
    return None
