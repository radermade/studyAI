"""Tests for shared primitives: task IDs, UTC handling, and strict models."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError
from study_core.common import (
    ALL_TASK_IDS,
    DOMAIN_WEIGHTS,
    StrictModel,
    domain_of,
    ensure_utc,
    is_valid_task_id,
)


def test_all_task_ids_are_twenty_and_unique() -> None:
    assert len(ALL_TASK_IDS) == 20
    assert len(set(ALL_TASK_IDS)) == 20


def test_domain_weights_total_100() -> None:
    assert sum(DOMAIN_WEIGHTS.values()) == 100


@pytest.mark.parametrize("task_id", ALL_TASK_IDS)
def test_valid_task_ids_pass(task_id: str) -> None:
    assert is_valid_task_id(task_id)


@pytest.mark.parametrize("bad", ["AIP-1.7", "AIP-2.6", "AIP-6.1", "AIP-0.1", "AIP-1", "x"])
def test_invalid_task_ids_fail(bad: str) -> None:
    assert not is_valid_task_id(bad)


def test_domain_of_rejects_invalid() -> None:
    assert domain_of("AIP-3.2") == 3
    with pytest.raises(ValueError):
        domain_of("AIP-9.9")


def test_ensure_utc_rejects_naive() -> None:
    naive = datetime(2026, 1, 1)
    with pytest.raises(ValueError):
        ensure_utc(naive)
    aware = datetime(2026, 1, 1, tzinfo=UTC)
    assert ensure_utc(aware) == aware


def test_strict_model_forbids_unknown_fields() -> None:
    class Example(StrictModel):
        value: int

    with pytest.raises(ValidationError):
        Example.model_validate({"value": 1, "surprise": 2})
