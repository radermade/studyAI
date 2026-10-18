"""Shared Phase 1 test fixtures: a migrated, ingested study service."""

from __future__ import annotations

from collections.abc import Iterator
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
from content.aip_c01 import BLUEPRINT_VERSION
from content.phase1_seed import (
    build_answer_material,
    build_content_units,
    build_curriculum,
    build_lab_definitions,
    build_question_options,
    build_rich_questions,
)
from scripts.phase0 import assemble_inputs
from study_core.db import DbConnection, apply_migrations, connect
from study_core.handoff import build_handoff, evaluate_phase0
from study_core.ingestion import ingest_handoff
from study_core.ports import SystemRandom
from study_core.scored_service import ScoredSessionService
from study_core.service import StudyService


class FakeClock:
    """A controllable UTC clock."""

    def __init__(self, start: datetime | None = None) -> None:
        self._now = start or datetime(2026, 1, 1, tzinfo=UTC)

    def now_utc(self) -> datetime:
        return self._now

    def advance(self, days: int) -> None:
        self._now = self._now + timedelta(days=days)


class FirstChoiceRandom:
    """Deterministic random source selecting the first element."""

    def choose_index(self, upper_bound: int) -> int:
        if upper_bound <= 0:
            raise ValueError("upper_bound must be positive")
        return 0


@pytest.fixture
def db_path(tmp_path: Path) -> Path:
    return tmp_path / "study.db"


@pytest.fixture
def connection(db_path: Path) -> Iterator[DbConnection]:
    conn = connect(db_path, 5000)
    now_iso = datetime(2026, 1, 1, tzinfo=UTC).isoformat()
    apply_migrations(conn, now_iso=now_iso)
    inputs = assemble_inputs()
    report = evaluate_phase0(inputs)
    handoff = build_handoff(inputs, report)
    ingest_handoff(
        conn,
        handoff,
        now_iso=now_iso,
        answer_material=build_answer_material(),
        question_options=build_question_options(),
        content_units=build_content_units(),
        curriculum=build_curriculum(),
        labs=build_lab_definitions(),
        rich_questions=build_rich_questions(),
    )
    yield conn
    conn.close()


@pytest.fixture
def clock() -> FakeClock:
    return FakeClock()


@pytest.fixture
def service(connection: DbConnection, clock: FakeClock) -> StudyService:
    return StudyService(
        connection,
        clock,
        FirstChoiceRandom(),
        blueprint_version=BLUEPRINT_VERSION,
    )


@pytest.fixture
def scored(connection: DbConnection, clock: FakeClock) -> ScoredSessionService:
    # Seeded random for deterministic selection in tests.
    return ScoredSessionService(connection, clock, SystemRandom(seed=1))
