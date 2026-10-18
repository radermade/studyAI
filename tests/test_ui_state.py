"""Tests for durable UI state: curriculum, notes, resume, content status."""

from __future__ import annotations

from study_core.db import DbConnection
from study_core.ui_state import ContentStatus, UiStateService

from tests.conftest import FakeClock


def _ui(connection: DbConnection, clock: FakeClock) -> UiStateService:
    return UiStateService(connection, clock)


def test_curriculum_is_ordered(connection: DbConnection, clock: FakeClock) -> None:
    ui = _ui(connection, clock)
    items = ui.list_curriculum()
    # 20 lessons (one per task) plus 12 authored labs.
    assert len(items) == 32
    orders = [item.display_order for item in items]
    assert orders == sorted(orders)


def test_content_status_round_trip(connection: DbConnection, clock: FakeClock) -> None:
    ui = _ui(connection, clock)
    ui.set_content_status(
        learner_id="L1",
        item_id="lesson-AIP-1.1",
        status=ContentStatus.COMPLETE,
        position=0,
    )
    statuses = ui.content_status("L1")
    assert statuses["lesson-AIP-1.1"] == ContentStatus.COMPLETE


def test_notes_persist(connection: DbConnection, clock: FakeClock) -> None:
    ui = _ui(connection, clock)
    ui.save_note(learner_id="L1", context="lesson:x", text="my note")
    assert ui.get_note(learner_id="L1", context="lesson:x") == "my note"


def test_resume_state(connection: DbConnection, clock: FakeClock) -> None:
    ui = _ui(connection, clock)
    assert ui.get_resume("L1") is None
    ui.set_resume(learner_id="L1", view="Grill", entity_id="AIP-1.2", position=0)
    resume = ui.get_resume("L1")
    assert resume is not None
    assert resume.view == "Grill"
    assert resume.entity_id == "AIP-1.2"


def test_get_lab_definition_is_fully_authored(connection: DbConnection, clock: FakeClock) -> None:
    ui = _ui(connection, clock)
    lab = ui.get_lab_definition("lab-03-knowledge-base-rag")
    assert lab is not None
    assert lab.scenario and lab.cleanup and lab.recall_prompt
    assert len(lab.steps) == 4
    # Every step carries a 4-level hint ladder and a reflection.
    for step in lab.steps:
        assert len(step.hints) == 4
        assert step.reflection
    # The cleanup checkpoint is validated by absence and is mandatory.
    cleanup = [c for c in lab.checkpoints if c.is_cleanup]
    assert cleanup and cleanup[0].validator_id == "s3-bucket-absent"
    assert cleanup[0].mandatory is True


def test_get_lab_definition_unknown_returns_none(
    connection: DbConnection, clock: FakeClock
) -> None:
    ui = _ui(connection, clock)
    assert ui.get_lab_definition("lab-99-nonexistent") is None
