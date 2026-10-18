"""Deterministic Phase 0 handoff and the acceptance gate.

The acceptance evaluator runs every Phase 0 validator and returns a single
report. It emits an accepted, versioned handoff only when zero blocking issues
remain, and never claims certification readiness.
"""

from __future__ import annotations

from collections.abc import Sequence

from study_core.artifacts import ArtifactEnvelope, build_envelope
from study_core.baseline import BaselineSummary
from study_core.blueprint import ObjectiveManifest, validate_objective_manifest
from study_core.common import StrictModel, ValidationIssue
from study_core.profile import LearnerProfile
from study_core.safety import (
    LabDefinitionHeader,
    LabSafetyPolicy,
    validate_lab_definition,
)
from study_core.seed import QuestionAdmission, validate_seed_bank
from study_core.sources import SourceRegistry, validate_source_registry

HANDOFF_SCHEMA = "Phase0Handoff"
HANDOFF_SCHEMA_VERSION = "v1"


class Phase0Inputs(StrictModel):
    """All inputs required to evaluate the Phase 0 exit gate."""

    blueprint_version: str
    manifest: ObjectiveManifest
    registry: SourceRegistry
    profile: LearnerProfile
    safety_policy: LabSafetyPolicy
    labs: tuple[LabDefinitionHeader, ...]
    seed_prompts: tuple[QuestionAdmission, ...]
    baseline_summary: BaselineSummary


class AcceptanceReport(StrictModel):
    """Outcome of the Phase 0 acceptance gate."""

    accepted: bool
    blockers: tuple[ValidationIssue, ...]
    handoff_version: str | None


def _blocking(issues: Sequence[ValidationIssue]) -> list[ValidationIssue]:
    return [issue for issue in issues if issue.severity.value == "error"]


def evaluate_phase0(inputs: Phase0Inputs) -> AcceptanceReport:
    """Run every Phase 0 validator and decide acceptance.

    Returns a report listing every blocker. Acceptance requires zero blocking
    issues across blueprint, sources, labs, baseline completeness, and seed
    coverage.
    """
    blockers: list[ValidationIssue] = []
    blockers.extend(validate_objective_manifest(inputs.manifest))
    blockers.extend(validate_source_registry(inputs.registry))
    for lab in inputs.labs:
        blockers.extend(validate_lab_definition(lab))
    blockers.extend(validate_seed_bank(inputs.seed_prompts))

    if not inputs.baseline_summary.complete:
        blockers.append(
            ValidationIssue(
                code="baseline.incomplete",
                path="baseline_summary.complete",
                message="baseline strengths/weaknesses/calibration are not fully recorded",
            )
        )

    blocking = _blocking(blockers)
    accepted = len(blocking) == 0
    return AcceptanceReport(
        accepted=accepted,
        blockers=tuple(blockers),
        handoff_version=inputs.blueprint_version if accepted else None,
    )


def build_handoff(inputs: Phase0Inputs, report: AcceptanceReport) -> ArtifactEnvelope:
    """Build the versioned Phase 0 handoff envelope.

    Raises:
        ValueError: when the acceptance gate did not pass. A handoff is never
        produced from a failing gate.
    """
    if not report.accepted or report.handoff_version is None:
        raise ValueError("cannot build a handoff from a failing Phase 0 gate")
    payload = {
        "blueprint_version": inputs.blueprint_version,
        "manifest": inputs.manifest.model_dump(mode="json"),
        "source_registry": inputs.registry.model_dump(mode="json"),
        "learner_profile": inputs.profile.model_dump(mode="json"),
        "lab_safety_policy": inputs.safety_policy.model_dump(mode="json"),
        "labs": [lab.model_dump(mode="json") for lab in inputs.labs],
        "seed_admission": [p.model_dump(mode="json") for p in inputs.seed_prompts],
        "baseline_summary": inputs.baseline_summary.model_dump(mode="json"),
        "certification_readiness_claimed": False,
    }
    return build_envelope(
        schema_name=HANDOFF_SCHEMA,
        schema_version=HANDOFF_SCHEMA_VERSION,
        artifact_version=inputs.blueprint_version,
        provenance="phase0-acceptance-gate",
        payload=payload,
    )
