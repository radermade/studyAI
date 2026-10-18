"""Wire settings, connection, migrations, and the study service together."""

from __future__ import annotations

from dataclasses import dataclass

from study_core.db import DbConnection, apply_migrations, connect
from study_core.lab_models import ReadOnlyValidator
from study_core.lab_service import LabService
from study_core.mastery import MasteryEvaluator
from study_core.ports import (
    Clock,
    RandomSource,
    SequenceRandom,
    SystemClock,
    SystemRandom,
)
from study_core.readiness import ReadinessEvaluator
from study_core.scored_service import ScoredSessionService
from study_core.service import StudyService
from study_core.settings import Settings
from study_core.ui_state import UiStateService


@dataclass
class StudyRuntime:
    """A ready-to-use connection plus the services built over it."""

    connection: DbConnection
    service: StudyService
    labs: LabService
    ui: UiStateService
    scored: ScoredSessionService
    mastery: MasteryEvaluator
    readiness: ReadinessEvaluator


def build_runtime(
    settings: Settings,
    *,
    blueprint_version: str,
    clock: Clock | None = None,
    random_source: RandomSource | None = None,
    scored_random: RandomSource | None = None,
    validator: ReadOnlyValidator | None = None,
    allow_cross_thread: bool = False,
) -> StudyRuntime:
    """Open the database, apply migrations, and build the services.

    Set `allow_cross_thread=True` for the Streamlit app, which reruns the
    script on different worker threads.
    """
    resolved_clock = clock if clock is not None else SystemClock()
    resolved_random = random_source if random_source is not None else SequenceRandom()
    conn = connect(
        settings.database_path,
        settings.busy_timeout_ms,
        allow_cross_thread=allow_cross_thread,
    )
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
    resolved_scored_random = scored_random if scored_random is not None else SystemRandom()
    scored = ScoredSessionService(conn, resolved_clock, resolved_scored_random)
    mastery = MasteryEvaluator(conn, resolved_clock, blueprint_version=blueprint_version)
    readiness = ReadinessEvaluator(conn, resolved_clock, mastery)
    return StudyRuntime(
        connection=conn,
        service=service,
        labs=labs,
        ui=ui,
        scored=scored,
        mastery=mastery,
        readiness=readiness,
    )
