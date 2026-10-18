"""Tests for the lab lifecycle: checkpoint truthfulness, hints, completion."""

from __future__ import annotations

import sqlite3

import pytest
from study_aws.validators import FakeValidator
from study_core.lab_models import CheckpointState, EvidenceKind
from study_core.lab_service import (
    LabPreconditionError,
    LabService,
    LabValidationError,
)
from study_core.service import NotFoundError

from tests.conftest import FakeClock


def _lab_service(
    connection: sqlite3.Connection, clock: FakeClock, kind: EvidenceKind
) -> LabService:
    return LabService(connection, clock, FakeValidator(kind, now=clock.now_utc()))


def _start(service: LabService) -> str:
    run = service.start_lab(
        learner_id="L1",
        lab_id="lab-01-model-comparison",
        region="us-east-1",
        request_id="start1",
        acknowledged_cost=True,
        acknowledged_cleanup=True,
    )
    return run.run_id


def test_start_requires_acknowledgements(connection: sqlite3.Connection, clock: FakeClock) -> None:
    service = _lab_service(connection, clock, EvidenceKind.RESOURCE_PRESENT)
    with pytest.raises(LabPreconditionError):
        service.start_lab(
            learner_id="L1",
            lab_id="lab-01-model-comparison",
            region="us-east-1",
            request_id="s",
            acknowledged_cost=False,
            acknowledged_cleanup=True,
        )


def test_start_rejects_region_outside_allowlist(
    connection: sqlite3.Connection, clock: FakeClock
) -> None:
    service = _lab_service(connection, clock, EvidenceKind.RESOURCE_PRESENT)
    with pytest.raises(LabPreconditionError):
        service.start_lab(
            learner_id="L1",
            lab_id="lab-01-model-comparison",
            region="eu-west-1",
            request_id="s",
            acknowledged_cost=True,
            acknowledged_cleanup=True,
        )


def test_start_is_idempotent(connection: sqlite3.Connection, clock: FakeClock) -> None:
    service = _lab_service(connection, clock, EvidenceKind.RESOURCE_PRESENT)
    a = _start(service)
    b = service.start_lab(
        learner_id="L1",
        lab_id="lab-01-model-comparison",
        region="us-east-1",
        request_id="start1",
        acknowledged_cost=True,
        acknowledged_cleanup=True,
    )
    assert a == b.run_id


def test_check_present_evidence_verifies(connection: sqlite3.Connection, clock: FakeClock) -> None:
    service = _lab_service(connection, clock, EvidenceKind.RESOURCE_PRESENT)
    run_id = _start(service)
    view = service.check(run_id=run_id, checkpoint_id="c1-model-access", event_id="chk1")
    assert view.state == CheckpointState.VERIFIED


def test_check_absent_evidence_fails_non_cleanup(
    connection: sqlite3.Connection, clock: FakeClock
) -> None:
    service = _lab_service(connection, clock, EvidenceKind.RESOURCE_ABSENT)
    run_id = _start(service)
    view = service.check(run_id=run_id, checkpoint_id="c1-model-access", event_id="chk1")
    assert view.state == CheckpointState.FAILED


def test_self_report_cannot_verify(connection: sqlite3.Connection, clock: FakeClock) -> None:
    service = _lab_service(connection, clock, EvidenceKind.RESOURCE_PRESENT)
    run_id = _start(service)
    view = service.record_self_report(
        run_id=run_id, checkpoint_id="c2-comparison-recorded", event_id="sr1"
    )
    # A self-report lands in SELF_REPORTED and can never be VERIFIED.
    assert view.state == CheckpointState.SELF_REPORTED


def test_check_without_validator_rejected(connection: sqlite3.Connection, clock: FakeClock) -> None:
    service = LabService(connection, clock, validator=None)
    run_id = _start(service)
    with pytest.raises(LabValidationError):
        service.check(run_id=run_id, checkpoint_id="c1-model-access", event_id="chk1")


def test_complete_requires_mandatory_checkpoint(
    connection: sqlite3.Connection, clock: FakeClock
) -> None:
    service = _lab_service(connection, clock, EvidenceKind.RESOURCE_PRESENT)
    run_id = _start(service)
    with pytest.raises(LabPreconditionError):
        service.complete_lab(run_id=run_id, request_id="done1")


def test_complete_independent_when_no_full_hint(
    connection: sqlite3.Connection, clock: FakeClock
) -> None:
    service = _lab_service(connection, clock, EvidenceKind.RESOURCE_PRESENT)
    run_id = _start(service)
    service.check(run_id=run_id, checkpoint_id="c1-model-access", event_id="chk1")
    result = service.complete_lab(run_id=run_id, request_id="done1")
    assert result.independent is True


def test_full_hint_marks_assisted(connection: sqlite3.Connection, clock: FakeClock) -> None:
    service = _lab_service(connection, clock, EvidenceKind.RESOURCE_PRESENT)
    run_id = _start(service)
    service.check(run_id=run_id, checkpoint_id="c1-model-access", event_id="chk1")
    service.reveal_hint(run_id=run_id, step_id="s2", level=4)
    result = service.complete_lab(run_id=run_id, request_id="done1")
    assert result.independent is False


def test_unknown_lab_run(connection: sqlite3.Connection, clock: FakeClock) -> None:
    service = _lab_service(connection, clock, EvidenceKind.RESOURCE_PRESENT)
    with pytest.raises(NotFoundError):
        service.complete_lab(run_id="missing", request_id="x")


def test_hint_level_bounds(connection: sqlite3.Connection, clock: FakeClock) -> None:
    service = _lab_service(connection, clock, EvidenceKind.RESOURCE_PRESENT)
    run_id = _start(service)
    with pytest.raises(ValueError):
        service.reveal_hint(run_id=run_id, step_id="s2", level=5)
