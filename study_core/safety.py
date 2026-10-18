"""AWS lab safety policy and lab-definition admission.

Defines enforceable pre-lab gates and the truthful cleanup-evidence semantics
consumed by later phases. Validators are read-only by construction: only
Get/List/Describe-style actions may be admitted, and resource mutation remains
a learner-operated action out of validator scope.
"""

from __future__ import annotations

from enum import StrEnum

from pydantic import Field, field_validator

from study_core.common import StrictModel, ValidationIssue, is_valid_task_id

# Read-only action verbs permitted for validators in this phase.
_READONLY_PREFIXES = ("Get", "List", "Describe")


class CostClass(StrEnum):
    """Estimated chargeable cost class of a lab."""

    FREE = "free"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"


class CleanupEvidence(StrEnum):
    """Evidence categories for cleanup. Only absence/terminal states verify."""

    NONE = "none"
    SELF_REPORTED = "self_reported"
    VALIDATOR_OBSERVED_PRESENT = "validator_observed_present"
    VALIDATOR_OBSERVED_ABSENT = "validator_observed_absent"
    TERMINAL_DELETION_STATE = "terminal_deletion_state"
    VALIDATOR_FAILED = "validator_failed"


# Cleanup is established only by these two evidence categories.
VERIFYING_CLEANUP_EVIDENCE = frozenset(
    {CleanupEvidence.VALIDATOR_OBSERVED_ABSENT, CleanupEvidence.TERMINAL_DELETION_STATE}
)


class ValidatorPolicy(StrictModel):
    """A read-only validation action permitted during a lab."""

    validator_id: str
    service: str
    action: str
    regions: tuple[str, ...] = Field(min_length=1)
    timeout_seconds: float = Field(gt=0.0, le=60.0)

    @field_validator("action")
    @classmethod
    def _read_only(cls, value: str) -> str:
        if not value.startswith(_READONLY_PREFIXES):
            raise ValueError(f"validator action {value} is not read-only")
        return value


class LabDefinitionHeader(StrictModel):
    """Admission envelope every lab definition must satisfy before it can start."""

    lab_id: str
    objective_ids: tuple[str, ...] = Field(min_length=1)
    prerequisites: tuple[str, ...]
    learning_objectives: tuple[str, ...] = Field(min_length=1)
    architecture: str
    cost_class: CostClass
    regions: tuple[str, ...] = Field(min_length=1)
    steps: tuple[str, ...] = Field(min_length=1)
    prediction_prompts: tuple[str, ...] = Field(min_length=1)
    validators: tuple[ValidatorPolicy, ...]
    failure_injection: str
    reflection: str
    cleanup: str
    delayed_recall: str

    @field_validator("objective_ids")
    @classmethod
    def _valid_objectives(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        for objective_id in value:
            if not is_valid_task_id(objective_id):
                raise ValueError(f"unknown objective id: {objective_id}")
        return value


class LabSafetyPolicy(StrictModel):
    """Versioned AWS lab safety policy."""

    policy_version: str
    dedicated_profile_recommended: bool
    region_allowlist: tuple[str, ...] = Field(min_length=1)
    budget_alert_required: bool
    required_tags: tuple[str, ...]
    read_only_validators_only: bool = True


def validate_lab_definition(lab: LabDefinitionHeader) -> tuple[ValidationIssue, ...]:
    """Return blocking issues that prevent a lab from being admitted.

    A lab is blocked when any required instructional or safety field is empty.
    The Pydantic model enforces presence; this returns an explicit, renderable
    block reason set for the admission report.
    """
    issues: list[ValidationIssue] = []
    required_text = {
        "architecture": lab.architecture,
        "failure_injection": lab.failure_injection,
        "reflection": lab.reflection,
        "cleanup": lab.cleanup,
        "delayed_recall": lab.delayed_recall,
    }
    for field_name, value in required_text.items():
        if not value.strip():
            issues.append(
                ValidationIssue(
                    code="lab.missing_field",
                    path=f"{lab.lab_id}.{field_name}",
                    message=f"lab {lab.lab_id} is missing {field_name}",
                )
            )
    return tuple(issues)


def cleanup_is_verified(evidence: CleanupEvidence) -> bool:
    """Return True only when evidence proves absence or terminal deletion."""
    return evidence in VERIFYING_CLEANUP_EVIDENCE
