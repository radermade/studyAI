"""Tests for the state-machine primitive and the declared machines."""

from __future__ import annotations

import pytest
from study_core.lab_models import CheckpointState, EvidenceKind
from study_core.machines import (
    BASELINE_MACHINE,
    CHECKPOINT_MACHINE,
    LAB_RUN_MACHINE,
    REVIEW_MACHINE,
    SCORED_SESSION_MACHINE,
    SESSION_MACHINE,
    ScoredSessionState,
)
from study_core.state_machine import IllegalTransitionError, StateMachine
from study_core.study_models import ReviewState, SessionState


def test_declared_transition_allowed() -> None:
    assert (
        SESSION_MACHINE.assert_transition(SessionState.ACTIVE, SessionState.COMPLETED)
        == SessionState.COMPLETED
    )


def test_undeclared_transition_raises() -> None:
    with pytest.raises(IllegalTransitionError):
        SESSION_MACHINE.assert_transition(SessionState.COMPLETED, SessionState.ACTIVE)


def test_terminal_state_blocks_further_transitions() -> None:
    assert SESSION_MACHINE.is_terminal(SessionState.ABANDONED)
    ok, reason = SESSION_MACHINE.can_transition(SessionState.ABANDONED, SessionState.ACTIVE)
    assert not ok
    assert "terminal" in reason


def test_checkpoint_verified_requires_evidence() -> None:
    # Without evidence, IN_PROGRESS -> VERIFIED is blocked by the guard.
    ok, _ = CHECKPOINT_MACHINE.can_transition(CheckpointState.IN_PROGRESS, CheckpointState.VERIFIED)
    assert not ok
    # With resource-present evidence, it is allowed.
    ok2, _ = CHECKPOINT_MACHINE.can_transition(
        CheckpointState.IN_PROGRESS,
        CheckpointState.VERIFIED,
        evidence_kind=EvidenceKind.RESOURCE_PRESENT,
    )
    assert ok2


def test_checkpoint_cleaned_up_requires_absence_evidence() -> None:
    ok, _ = CHECKPOINT_MACHINE.can_transition(CheckpointState.VERIFIED, CheckpointState.CLEANED_UP)
    assert not ok
    ok2, _ = CHECKPOINT_MACHINE.can_transition(
        CheckpointState.VERIFIED,
        CheckpointState.CLEANED_UP,
        evidence_kind=EvidenceKind.RESOURCE_ABSENT,
    )
    assert ok2
    ok3, _ = CHECKPOINT_MACHINE.can_transition(
        CheckpointState.VERIFIED,
        CheckpointState.CLEANED_UP,
        evidence_kind=EvidenceKind.TERMINAL_DELETION,
    )
    assert ok3


def test_self_report_cannot_reach_verified_without_evidence() -> None:
    ok, _ = CHECKPOINT_MACHINE.can_transition(
        CheckpointState.SELF_REPORTED, CheckpointState.VERIFIED
    )
    assert not ok


def test_lab_run_completion_paths() -> None:
    from study_core.lab_models import LabRunState

    assert LAB_RUN_MACHINE.can_transition(LabRunState.ACTIVE, LabRunState.COMPLETED_INDEPENDENT)[0]
    assert LAB_RUN_MACHINE.can_transition(LabRunState.ACTIVE, LabRunState.COMPLETED_ASSISTED)[0]
    assert LAB_RUN_MACHINE.is_terminal(LabRunState.COMPLETED_INDEPENDENT)
    # Cannot resurrect a completed run.
    ok, _ = LAB_RUN_MACHINE.can_transition(LabRunState.COMPLETED_INDEPENDENT, LabRunState.ACTIVE)
    assert not ok


def test_scored_session_transitions() -> None:
    assert SCORED_SESSION_MACHINE.can_transition(
        ScoredSessionState.IN_PROGRESS, ScoredSessionState.SUBMITTED
    )[0]
    assert SCORED_SESSION_MACHINE.can_transition(
        ScoredSessionState.IN_PROGRESS, ScoredSessionState.ABANDONED
    )[0]
    # A submitted session is terminal.
    assert SCORED_SESSION_MACHINE.is_terminal(ScoredSessionState.SUBMITTED)
    ok, _ = SCORED_SESSION_MACHINE.can_transition(
        ScoredSessionState.SUBMITTED, ScoredSessionState.ABANDONED
    )
    assert not ok


def test_review_reschedule_in_place() -> None:
    assert REVIEW_MACHINE.can_transition(ReviewState.SCHEDULED, ReviewState.SCHEDULED)[0]


def test_baseline_linear_flow() -> None:
    from study_core.baseline import BaselineState

    assert BASELINE_MACHINE.can_transition(BaselineState.DRAFT, BaselineState.IN_PROGRESS)[0]
    assert BASELINE_MACHINE.is_terminal(BaselineState.SUMMARIZED)


def test_guard_on_undeclared_transition_rejected() -> None:
    machine: StateMachine[SessionState] = StateMachine(
        name="x",
        initial=SessionState.ACTIVE,
        transitions={(SessionState.ACTIVE, SessionState.COMPLETED)},
    )
    with pytest.raises(ValueError):
        machine.allow(SessionState.ACTIVE, SessionState.PAUSED, lambda **_: (True, ""))
