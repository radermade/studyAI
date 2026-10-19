"""Tests for the Subject abstraction and active-subject resolution.

These prove the engine is genuinely subject-parameterized: a Subject with a
different ID prefix, domain set, and weights validates and parses correctly,
and the active subject resolves from configuration (default plus override).
"""

from __future__ import annotations

import pytest
from study_core.subjects import AIP_C01, Subject, active_subject, get_subject


def test_aip_c01_task_inventory() -> None:
    assert len(AIP_C01.all_task_ids) == 20
    assert AIP_C01.domain_ids == (1, 2, 3, 4, 5)
    assert AIP_C01.is_valid_task_id("AIP-1.6")
    assert not AIP_C01.is_valid_task_id("AIP-1.7")
    assert AIP_C01.domain_of("AIP-3.2") == 3


def test_aip_c01_weights_total_100() -> None:
    assert sum(AIP_C01.domain_weights.values()) == 100


def test_domain_of_rejects_invalid_for_subject() -> None:
    with pytest.raises(ValueError):
        AIP_C01.domain_of("AIP-9.9")
    with pytest.raises(ValueError):
        AIP_C01.domain_of("XYZ-1.1")


def test_weights_must_total_100() -> None:
    with pytest.raises(ValueError):
        Subject(
            subject_id="bad",
            display_name="Bad",
            blueprint_version="BAD-1",
            id_prefix="BAD",
            domain_task_counts={1: 2, 2: 2},
            domain_weights={1: 40, 2: 40},  # totals 80
        )


def test_domain_sets_must_agree() -> None:
    with pytest.raises(ValueError):
        Subject(
            subject_id="bad",
            display_name="Bad",
            blueprint_version="BAD-1",
            id_prefix="BAD",
            domain_task_counts={1: 2, 2: 2},
            domain_weights={1: 50, 3: 50},  # domain 3 not in task counts
        )


def test_other_shaped_subject_parses() -> None:
    # A different prefix, three domains, different weights: the same logic works.
    other = Subject(
        subject_id="demo-cloud",
        display_name="Demo Cloud Cert",
        blueprint_version="DC-1",
        id_prefix="DC",
        domain_task_counts={1: 2, 2: 3, 3: 1},
        domain_weights={1: 50, 2: 30, 3: 20},
    )
    assert other.all_task_ids == ("DC-1.1", "DC-1.2", "DC-2.1", "DC-2.2", "DC-2.3", "DC-3.1")
    assert other.domain_of("DC-2.3") == 2
    assert other.is_valid_task_id("DC-3.1")
    assert not other.is_valid_task_id("DC-3.2")
    assert not other.is_valid_task_id("AIP-1.1")  # wrong prefix


def test_active_subject_defaults_to_aip() -> None:
    assert active_subject(env={}).subject_id == "aip-c01"


def test_active_subject_honors_env_override() -> None:
    assert active_subject(env={"STUDYAI_SUBJECT": "aip-c01"}).subject_id == "aip-c01"


def test_active_subject_rejects_unknown() -> None:
    with pytest.raises(ValueError):
        active_subject(env={"STUDYAI_SUBJECT": "does-not-exist"})


def test_get_subject_unknown_lists_known() -> None:
    with pytest.raises(ValueError, match="aip-c01"):
        get_subject("nope")
