"""Lab-domain value objects, checkpoint state machine, and validator port.

`CheckpointState.VERIFIED` is reachable only from committed validator evidence,
and `CLEANED_UP` only from observed absence or a terminal deletion state. A
click, navigation, or self-report can never produce either.
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Protocol

from pydantic import Field

from study_core.common import StrictModel


class CheckpointState(StrEnum):
    """The six explicit checkpoint states."""

    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    SELF_REPORTED = "self_reported"
    VERIFIED = "verified"
    FAILED = "failed"
    CLEANED_UP = "cleaned_up"


class EvidenceKind(StrEnum):
    """Categories of checkpoint evidence."""

    SELF_REPORT = "self_report"
    RESOURCE_PRESENT = "resource_present"
    RESOURCE_ABSENT = "resource_absent"
    TERMINAL_DELETION = "terminal_deletion"
    VALIDATION_FAILURE = "validation_failure"


class LabRunState(StrEnum):
    """Lifecycle of a lab run."""

    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETION_PENDING = "completion_pending"
    COMPLETED_INDEPENDENT = "completed_independent"
    COMPLETED_ASSISTED = "completed_assisted"
    ABANDONED = "abandoned"


# Evidence that can establish VERIFIED and CLEANED_UP respectively.
_VERIFYING_EVIDENCE = frozenset({EvidenceKind.RESOURCE_PRESENT})
_CLEANUP_EVIDENCE = frozenset({EvidenceKind.RESOURCE_ABSENT, EvidenceKind.TERMINAL_DELETION})


class ValidationRequest(StrictModel):
    """A read-only validation request. Carries no credentials."""

    validator_id: str
    region: str
    profile_name: str | None = None
    resource_locator: dict[str, str] = Field(default_factory=dict)
    timeout_seconds: float = Field(default=10.0, gt=0.0, le=60.0)


class ValidationEvidence(StrictModel):
    """Sanitized evidence produced by a validator."""

    attempt_id: str
    kind: EvidenceKind
    observed_at: datetime
    summary: str
    sanitized_attributes: dict[str, str] = Field(default_factory=dict)


class ReadOnlyValidator(Protocol):
    """Port for read-only AWS validation. Implementations never mutate."""

    def validate(self, request: ValidationRequest) -> ValidationEvidence: ...


class LabRunView(StrictModel):
    """A durable lab-run reference returned to callers."""

    run_id: str
    lab_id: str
    learner_id: str
    region: str
    state: LabRunState
    active_step: str | None
    full_solution_used: bool


class CheckpointView(StrictModel):
    """The committed state of one checkpoint."""

    run_id: str
    checkpoint_id: str
    state: CheckpointState


class LabCompletionView(StrictModel):
    """Result of completing a lab."""

    run_id: str
    state: LabRunState
    independent: bool


def evidence_establishes_verified(kind: EvidenceKind) -> bool:
    """Return True when evidence can move a checkpoint to VERIFIED."""
    return kind in _VERIFYING_EVIDENCE


def evidence_establishes_cleanup(kind: EvidenceKind) -> bool:
    """Return True when evidence can move a cleanup checkpoint to CLEANED_UP."""
    return kind in _CLEANUP_EVIDENCE
