"""Shared primitives: stable IDs, UTC time, typed issues, and base models.

These types form the single versioned boundary every Phase 0 artifact crosses.
All boundary models forbid unknown fields so security-critical records cannot
smuggle unexpected data.
"""

from __future__ import annotations

import hashlib
import random
import re
from collections.abc import Sequence
from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, field_validator

from study_core.subjects import active_subject

# The task-ID shape, task inventory, and domain weights now originate from the
# active Subject (study_core.subjects). These module-level names remain as a
# stable, backward-compatible facade over the active subject so existing call
# sites keep working while the engine becomes subject-capable. A future
# subject-selection screen would change the active subject; it must not require
# editing these constants.
_ACTIVE_SUBJECT = active_subject()

# Objective IDs follow `<prefix>-<domain>.<task>` with domain-specific ranges.
TASK_ID_PATTERN: re.Pattern[str] = _ACTIVE_SUBJECT.task_id_pattern

# Canonical ordered list of the active subject's task IDs.
ALL_TASK_IDS: tuple[str, ...] = _ACTIVE_SUBJECT.all_task_ids

# Official domain weights (percent) for the active subject. Must total 100.
DOMAIN_WEIGHTS: dict[int, int] = dict(_ACTIVE_SUBJECT.domain_weights)


def is_valid_task_id(value: str) -> bool:
    """Return True when `value` is a valid task ID of the active subject."""
    return _ACTIVE_SUBJECT.is_valid_task_id(value)


def domain_of(task_id: str) -> int:
    """Return the domain number for a valid task ID of the active subject.

    Raises ValueError when the task ID is not valid.
    """
    return _ACTIVE_SUBJECT.domain_of(task_id)


def utc_now() -> datetime:
    """Return the current timezone-aware UTC instant."""
    return datetime.now(tz=UTC)


def stable_shuffle[T](items: Sequence[T], *, seed_key: str) -> list[T]:
    """Return a deterministic shuffle of items keyed by a stable string.

    The order is stable for a given `seed_key` (so re-rendering the same item
    does not reshuffle) but varies across different keys. Used to randomize
    answer-option order so the correct answer is not positionally predictable.
    """
    digest = hashlib.sha256(seed_key.encode("utf-8")).hexdigest()
    rng = random.Random(int(digest, 16))
    shuffled = list(items)
    rng.shuffle(shuffled)
    return shuffled


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
