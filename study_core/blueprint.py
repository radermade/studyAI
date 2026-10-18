"""Versioned AIP-C01 objective manifest and its validation.

The manifest locks the exact set of 20 task IDs and the official domain weights.
It fails as a whole on any malformed, duplicate, misassigned, or missing ID so a
partial manifest is never published.
"""

from __future__ import annotations

from enum import StrEnum

from pydantic import Field

from study_core.common import (
    ALL_TASK_IDS,
    DOMAIN_WEIGHTS,
    StrictModel,
    ValidationIssue,
    domain_of,
    is_valid_task_id,
)


class ObjectiveStatus(StrEnum):
    """Lifecycle status of an objective within a blueprint version."""

    ACTIVE = "active"
    RETIRED = "retired"


class DomainRecord(StrictModel):
    """One exam domain and its official scored weight."""

    domain_id: int = Field(ge=1, le=5)
    title: str
    weight_percent: int = Field(ge=0, le=100)


class ObjectiveRecord(StrictModel):
    """One AIP-C01 task objective bound to a domain and sources."""

    objective_id: str
    domain_id: int = Field(ge=1, le=5)
    title: str
    blueprint_version: str
    status: ObjectiveStatus = ObjectiveStatus.ACTIVE
    source_ids: tuple[str, ...] = ()


class ObjectiveManifest(StrictModel):
    """The complete versioned objective and domain manifest."""

    blueprint_version: str
    domains: tuple[DomainRecord, ...] = Field(min_length=5, max_length=5)
    objectives: tuple[ObjectiveRecord, ...] = Field(min_length=20, max_length=20)


def validate_objective_manifest(manifest: ObjectiveManifest) -> tuple[ValidationIssue, ...]:
    """Return every blocking issue in an objective manifest.

    Enforces the exact 20-ID allowlist, unique IDs, correct domain ownership,
    and official domain weights summing to 100. Returns an empty tuple when the
    manifest is valid as a whole.
    """
    issues: list[ValidationIssue] = []

    # Domain weight checks.
    weights = {domain.domain_id: domain.weight_percent for domain in manifest.domains}
    for domain_id, expected in DOMAIN_WEIGHTS.items():
        actual = weights.get(domain_id)
        if actual != expected:
            issues.append(
                ValidationIssue(
                    code="domain.weight",
                    path=f"domains[{domain_id}].weight_percent",
                    message=f"domain {domain_id} weight {actual} != expected {expected}",
                )
            )
    if sum(weights.values()) != 100:
        issues.append(
            ValidationIssue(
                code="domain.weight_total",
                path="domains",
                message="domain weights must total 100",
            )
        )

    # Objective ID checks.
    seen: set[str] = set()
    for index, objective in enumerate(manifest.objectives):
        path = f"objectives[{index}].objective_id"
        if not is_valid_task_id(objective.objective_id):
            issues.append(
                ValidationIssue(
                    code="objective.invalid_id",
                    path=path,
                    message=f"malformed or unknown objective id {objective.objective_id}",
                )
            )
            continue
        if objective.objective_id in seen:
            issues.append(
                ValidationIssue(
                    code="objective.duplicate",
                    path=path,
                    message=f"duplicate objective id {objective.objective_id}",
                )
            )
        seen.add(objective.objective_id)
        if domain_of(objective.objective_id) != objective.domain_id:
            issues.append(
                ValidationIssue(
                    code="objective.wrong_domain",
                    path=f"objectives[{index}].domain_id",
                    message=f"{objective.objective_id} assigned to wrong domain",
                )
            )

    missing = [task_id for task_id in ALL_TASK_IDS if task_id not in seen]
    for task_id in missing:
        issues.append(
            ValidationIssue(
                code="objective.missing",
                path="objectives",
                message=f"required objective {task_id} is absent",
            )
        )
    return tuple(issues)
