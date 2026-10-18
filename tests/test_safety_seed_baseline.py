"""Tests for safety, seed admission, and baseline contracts."""

from __future__ import annotations

import pytest
from content.aip_c01 import (
    build_baseline_run,
    build_labs,
    build_seed_prompts,
)
from pydantic import ValidationError
from study_core.baseline import (
    BaselineState,
    summarize_baseline,
    validate_local_baseline,
)
from study_core.safety import (
    CleanupEvidence,
    CostClass,
    LabDefinitionHeader,
    ValidatorPolicy,
    cleanup_is_verified,
    validate_lab_definition,
)
from study_core.seed import MIN_TOTAL_PROMPTS, validate_seed_bank


def test_authored_labs_admit_cleanly() -> None:
    for lab in build_labs():
        assert validate_lab_definition(lab) == ()


def test_validator_rejects_mutating_action() -> None:
    with pytest.raises(ValidationError):
        ValidatorPolicy(
            validator_id="bad",
            service="bedrock",
            action="DeleteFoundationModel",
            regions=("us-east-1",),
            timeout_seconds=5.0,
        )


def test_lab_missing_cleanup_is_blocked() -> None:
    lab = build_labs()[0]
    tampered = lab.model_copy(update={"cleanup": "   "})
    issues = validate_lab_definition(tampered)
    assert any(issue.code == "lab.missing_field" for issue in issues)


def test_cleanup_evidence_semantics() -> None:
    assert cleanup_is_verified(CleanupEvidence.VALIDATOR_OBSERVED_ABSENT)
    assert cleanup_is_verified(CleanupEvidence.TERMINAL_DELETION_STATE)
    assert not cleanup_is_verified(CleanupEvidence.SELF_REPORTED)
    assert not cleanup_is_verified(CleanupEvidence.VALIDATOR_OBSERVED_PRESENT)


def test_seed_bank_meets_minimums() -> None:
    prompts = build_seed_prompts()
    assert len(prompts) >= MIN_TOTAL_PROMPTS
    assert validate_seed_bank(prompts) == ()


def test_seed_bank_below_two_per_task_fails() -> None:
    prompts = build_seed_prompts()
    # Drop both prompts for the first task to force a coverage failure.
    first_task = prompts[0].objective_ids[0]
    reduced = tuple(p for p in prompts if p.objective_ids[0] != first_task)
    issues = validate_seed_bank(reduced)
    assert any(issue.code == "seed.insufficient_task_coverage" for issue in issues)


def test_seed_absolute_claim_rejected() -> None:
    prompts = list(build_seed_prompts())
    tampered = prompts[0].model_copy(update={"prompt": "This design always works in every case."})
    issues = validate_seed_bank((tampered, *prompts[1:]))
    assert any(issue.code == "seed.absolute_claim" for issue in issues)


def test_local_baseline_covers_all_tasks() -> None:
    run = build_baseline_run()
    assert validate_local_baseline(run) == ()
    summary = summarize_baseline(run)
    assert summary.complete is True
    assert summary.unanswered_count == 0


def test_interrupted_baseline_is_incomplete() -> None:
    run = build_baseline_run()
    interrupted = run.model_copy(update={"state": BaselineState.INTERRUPTED})
    summary = summarize_baseline(interrupted)
    assert summary.complete is False


def test_cost_class_enum_round_trip() -> None:
    assert CostClass("low") is CostClass.LOW


def test_lab_header_requires_objectives() -> None:
    with pytest.raises(ValidationError):
        LabDefinitionHeader(
            lab_id="x",
            objective_ids=(),
            prerequisites=(),
            learning_objectives=("a",),
            architecture="a",
            cost_class=CostClass.FREE,
            regions=("us-east-1",),
            steps=("a",),
            prediction_prompts=("a",),
            validators=(),
            failure_injection="a",
            reflection="a",
            cleanup="a",
            delayed_recall="a",
        )
