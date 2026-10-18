"""Shared primitives: stable IDs, UTC time, typed issues, and base models.

These types form the single versioned boundary every Phase 0 artifact crosses.
All boundary models forbid unknown fields so security-critical records cannot
smuggle unexpected data.
"""

from __future__ import annotations

import re
from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, field_validator

# AIP-C01 task IDs follow `AIP-<domain>.<task>` with domain-specific ranges.
# Domains and their valid task counts: 1->6, 2->5, 3->4, 4->3, 5->2.
TASK_ID_PATTERN = re.compile(r"^AIP-([1-5])\.([1-9])$")
_DOMAIN_TASK_COUNTS: dict[int, int] = {1: 6, 2: 5, 3: 4, 4: 3, 5: 2}

# Canonical ordered list of the 20 current AIP-C01 task IDs.
ALL_TASK_IDS: tuple[str, ...] = tuple(
    f"AIP-{domain}.{task}"
    for domain in sorted(_DOMAIN_TASK_COUNTS)
    for task in range(1, _DOMAIN_TASK_COUNTS[domain] + 1)
)

# Official domain weights (percent). Must total 100.
DOMAIN_WEIGHTS: dict[int, int] = {1: 31, 2: 26, 3: 20, 4: 12, 5: 11}


def is_valid_task_id(value: str) -> bool:
    """Return True when `value` is one of the 20 current AIP-C01 task IDs."""
    match = TASK_ID_PATTERN.match(value)
    if match is None:
        return False
    domain = int(match.group(1))
    task = int(match.group(2))
    max_task = _DOMAIN_TASK_COUNTS.get(domain)
    return max_task is not None and 1 <= task <= max_task


def domain_of(task_id: str) -> int:
    """Return the domain number for a valid task ID.

    Raises ValueError when the task ID is not valid.
    """
    match = TASK_ID_PATTERN.match(task_id)
    if match is None or not is_valid_task_id(task_id):
        raise ValueError(f"invalid task id: {task_id!r}")
    return int(match.group(1))


def utc_now() -> datetime:
    """Return the current timezone-aware UTC instant."""
    return datetime.now(tz=UTC)


def ensure_utc(value: datetime) -> datetime:
    """Normalize a datetime to timezone-aware UTC.

    Naive datetimes are rejected so provenance timestamps remain unambiguous.
    """
    if value.tzinfo is None:
        raise ValueError("timestamp must be timezone-aware")
    return value.astimezone(UTC)


class Severity(StrEnum):
    """Severity of a validation issue."""

    ERROR = "error"
    WARNING = "warning"


class ValidationIssue(BaseModel):
    """A single structured problem found while validating an artifact."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    code: str
    path: str
    message: str
    severity: Severity = Severity.ERROR


class StrictModel(BaseModel):
    """Base for all boundary models: immutable and closed to unknown fields."""

    model_config = ConfigDict(frozen=True, extra="forbid")


class TimestampedModel(StrictModel):
    """A boundary model carrying a mandatory UTC creation timestamp."""

    @field_validator("*", mode="before")
    @classmethod
    def _reject_naive_datetimes(cls, value: object) -> object:
        if isinstance(value, datetime) and value.tzinfo is None:
            raise ValueError("timestamp must be timezone-aware")
        return value
