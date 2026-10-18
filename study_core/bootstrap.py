"""Wire settings, connection, migrations, and the study service together."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass

from study_core.db import apply_migrations, connect
from study_core.lab_models import ReadOnlyValidator
from study_core.lab_service import LabService
from study_core.ports import Clock, RandomSource, SequenceRandom, SystemClock
from study_core.service import StudyService
from study_core.settings import Settings
from study_core.ui_state import UiStateService


@dataclass
class StudyRuntime:
    """A ready-to-use connection plus the services built over it."""

    connection: sqlite3.Connection
    service: StudyService
    labs: LabService
    ui: UiStateService


def build_runtime(
    settings: Settings,
    *,
    blueprint_version: str,
    clock: Clock | None = None,
    random_source: RandomSource | None = None,
    validator: ReadOnlyValidator | None = None,
) -> StudyRuntime:
    """Open the database, apply migrations, and build the services."""
    resolved_clock = clock if clock is not None else SystemClock()
    resolved_random = random_source if random_source is not None else SequenceRandom()
    conn = connect(settings.database_path, settings.busy_timeout_ms)
    apply_migrations(conn, now_iso=resolved_clock.now_utc().isoformat())
    service = StudyService(
        conn,
        resolved_clock,
        resolved_random,
        blueprint_version=blueprint_version,
        max_search_limit=settings.max_search_limit,
    )
    labs = LabService(conn, resolved_clock, validator)
    ui = UiStateService(conn, resolved_clock)
    return StudyRuntime(connection=conn, service=service, labs=labs, ui=ui)
