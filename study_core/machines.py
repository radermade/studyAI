"""Declared state machines for every stateful entity in study_core.

This is the single place that defines which state transitions are legal. All
services route changes through these machines rather than hand-written checks,
so the rules are consistent and auditable.
"""

from __future__ import annotations

from enum import StrEnum

from study_core.baseline import BaselineState
from study_core.lab_models import (
    CheckpointState,
    EvidenceKind,
    LabRunState,
    evidence_establishes_cleanup,
    evidence_establishes_verified,
)
from study_core.state_machine import StateMachine
from study_core.study_models import ReviewState, SessionState


class ScoredSessionState(StrEnum):
    """Lifecycle of a scored session (stored as strings in SQLite)."""

    IN_PROGRESS = "in_progress"
    SUBMITTED = "submitted"
    ABANDONED = "abandoned"


# --- Study session ---------------------------------------------------------

SESSION_MACHINE: StateMachine[SessionState] = StateMachine(
    name="session",
    initial=SessionState.ACTIVE,
    transitions={
        (SessionState.ACTIVE, SessionState.PAUSED),
        (SessionState.PAUSED, SessionState.ACTIVE),
        (SessionState.ACTIVE, SessionState.COMPLETED),
        (SessionState.ACTIVE, SessionState.ABANDONED),
        (SessionState.PAUSED, SessionState.ABANDONED),
    },
    terminal={SessionState.COMPLETED, SessionState.ABANDONED},
)

# --- Spaced review ---------------------------------------------------------

REVIEW_MACHINE: StateMachine[ReviewState] = StateMachine(
    name="review",
    initial=ReviewState.SCHEDULED,
    transitions={
        (ReviewState.SCHEDULED, ReviewState.SCHEDULED),  # reschedule in place
        (ReviewState.SCHEDULED, ReviewState.RESOLVED),
        (ReviewState.SCHEDULED, ReviewState.SUPERSEDED),
        (ReviewState.RESOLVED, ReviewState.SCHEDULED),  # reopened by later evidence
    },
)

# --- Baseline diagnostic ---------------------------------------------------

BASELINE_MACHINE: StateMachine[BaselineState] = StateMachine(
    name="baseline",
    initial=BaselineState.DRAFT,
    transitions={
        (BaselineState.DRAFT, BaselineState.IN_PROGRESS),
        (BaselineState.IN_PROGRESS, BaselineState.IN_PROGRESS),
        (BaselineState.IN_PROGRESS, BaselineState.INTERRUPTED),
        (BaselineState.INTERRUPTED, BaselineState.IN_PROGRESS),
        (BaselineState.IN_PROGRESS, BaselineState.SUBMITTED),
        (BaselineState.SUBMITTED, BaselineState.SUMMARIZED),
    },
    terminal={BaselineState.SUMMARIZED},
)

# --- Lab run ---------------------------------------------------------------

LAB_RUN_MACHINE: StateMachine[LabRunState] = StateMachine(
    name="lab_run",
    initial=LabRunState.ACTIVE,
    transitions={
        (LabRunState.ACTIVE, LabRunState.PAUSED),
        (LabRunState.PAUSED, LabRunState.ACTIVE),
        (LabRunState.ACTIVE, LabRunState.COMPLETION_PENDING),
        (LabRunState.COMPLETION_PENDING, LabRunState.COMPLETED_INDEPENDENT),
        (LabRunState.COMPLETION_PENDING, LabRunState.COMPLETED_ASSISTED),
        (LabRunState.ACTIVE, LabRunState.COMPLETED_INDEPENDENT),
        (LabRunState.ACTIVE, LabRunState.COMPLETED_ASSISTED),
        (LabRunState.ACTIVE, LabRunState.ABANDONED),
        (LabRunState.PAUSED, LabRunState.ABANDONED),
    },
    terminal={
        LabRunState.COMPLETED_INDEPENDENT,
        LabRunState.COMPLETED_ASSISTED,
        LabRunState.ABANDONED,
    },
)

# --- Checkpoint (the safety-critical machine) ------------------------------
#
# `Verified` and `Cleaned up` are reachable only with the right committed
# evidence; a self-report or click can never reach them. Guards enforce the
# evidence requirement declaratively.

CHECKPOINT_MACHINE: StateMachine[CheckpointState] = StateMachine(
    name="checkpoint",
    initial=CheckpointState.NOT_STARTED,
    transitions={
        (CheckpointState.NOT_STARTED, CheckpointState.IN_PROGRESS),
        (CheckpointState.IN_PROGRESS, CheckpointState.SELF_REPORTED),
        (CheckpointState.IN_PROGRESS, CheckpointState.VERIFIED),
        (CheckpointState.IN_PROGRESS, CheckpointState.FAILED),
        (CheckpointState.SELF_REPORTED, CheckpointState.VERIFIED),
        (CheckpointState.SELF_REPORTED, CheckpointState.FAILED),
        (CheckpointState.FAILED, CheckpointState.IN_PROGRESS),
        (CheckpointState.VERIFIED, CheckpointState.CLEANED_UP),
        (CheckpointState.SELF_REPORTED, CheckpointState.CLEANED_UP),
        # Allow entering IN_PROGRESS from NOT_STARTED repeatedly is covered;
        # cleanup can also begin directly after verification.
        (CheckpointState.VERIFIED, CheckpointState.IN_PROGRESS),
    },
)


def _requires_verifying_evidence(**context: object) -> tuple[bool, str]:
    kind = context.get("evidence_kind")
    if isinstance(kind, EvidenceKind) and evidence_establishes_verified(kind):
        return True, ""
    return False, "VERIFIED requires committed resource-present validator evidence"


def _requires_cleanup_evidence(**context: object) -> tuple[bool, str]:
    kind = context.get("evidence_kind")
    if isinstance(kind, EvidenceKind) and evidence_establishes_cleanup(kind):
        return True, ""
    return False, "CLEANED_UP requires committed absence or terminal-deletion evidence"


# Attach evidence guards to the sensitive transitions.
for _frm in (CheckpointState.IN_PROGRESS, CheckpointState.SELF_REPORTED):
    CHECKPOINT_MACHINE.allow(_frm, CheckpointState.VERIFIED, _requires_verifying_evidence)
for _frm in (CheckpointState.VERIFIED, CheckpointState.SELF_REPORTED):
    CHECKPOINT_MACHINE.allow(_frm, CheckpointState.CLEANED_UP, _requires_cleanup_evidence)


# --- Scored session --------------------------------------------------------

SCORED_SESSION_MACHINE: StateMachine[ScoredSessionState] = StateMachine(
    name="scored_session",
    initial=ScoredSessionState.IN_PROGRESS,
    transitions={
        (ScoredSessionState.IN_PROGRESS, ScoredSessionState.SUBMITTED),
        (ScoredSessionState.IN_PROGRESS, ScoredSessionState.ABANDONED),
    },
    terminal={ScoredSessionState.SUBMITTED, ScoredSessionState.ABANDONED},
)
