"""Tests for the pure scored-session selection and scoring engine."""

from __future__ import annotations

from study_core.scoring import (
    PASS_SCALED,
    allocate_scored_counts,
    grade_item,
    passed,
    scaled_score,
    summarize,
    unscored_total_for_pool,
)
from study_core.study_models import GradeOutcome


def test_full_length_allocation_is_20_17_13_8_7() -> None:
    capacity = {1: 100, 2: 100, 3: 100, 4: 100, 5: 100}
    counts = allocate_scored_counts(domain_capacity=capacity, target_scored_total=65)
    assert counts == {1: 20, 2: 17, 3: 13, 4: 8, 5: 7}
    assert sum(counts.values()) == 65


def test_allocation_scales_to_subset_preserving_relative_weight() -> None:
    # Only domains 1 and 2 (weights 31 and 26). 65 target.
    capacity = {1: 100, 2: 100}
    counts = allocate_scored_counts(domain_capacity=capacity, target_scored_total=65)
    assert sum(counts.values()) == 65
    # 31:26 of 65 -> 35.4 / 29.6 -> 35 / 30 after rounding.
    assert counts[1] == 35
    assert counts[2] == 30


def test_allocation_bounded_by_capacity() -> None:
    capacity = {1: 5, 2: 3}
    counts = allocate_scored_counts(domain_capacity=capacity, target_scored_total=65)
    assert counts == {1: 5, 2: 3}


def test_allocation_empty_capacity() -> None:
    assert allocate_scored_counts(domain_capacity={}, target_scored_total=65) == {}


def test_unscored_activation_threshold() -> None:
    assert unscored_total_for_pool(10) == 0
    assert unscored_total_for_pool(75) == 10
    assert unscored_total_for_pool(1000) == 10


def test_grade_multiple_choice() -> None:
    assert grade_item(["a"], ["a"], answered=True) == GradeOutcome.CORRECT
    assert grade_item(["b"], ["a"], answered=True) == GradeOutcome.INCORRECT


def test_grade_multiple_response_all_or_nothing() -> None:
    assert grade_item(["a", "c"], ["a", "c"], answered=True) == GradeOutcome.CORRECT
    # Missing one correct option is incorrect (no partial credit).
    assert grade_item(["a"], ["a", "c"], answered=True) == GradeOutcome.INCORRECT
    # Extra wrong option is incorrect.
    assert grade_item(["a", "c", "d"], ["a", "c"], answered=True) == GradeOutcome.INCORRECT


def test_grade_unanswered_is_incorrect() -> None:
    assert grade_item([], ["a"], answered=False) == GradeOutcome.INCORRECT


def test_grade_ordering_exact_sequence() -> None:
    assert (
        grade_item(
            [],
            [],
            answered=True,
            question_format="ordering",
            selected_sequence=["b", "a", "c"],
            correct_sequence=["b", "a", "c"],
        )
        == GradeOutcome.CORRECT
    )
    # Right members, wrong order -> incorrect (all-or-nothing).
    assert (
        grade_item(
            [],
            [],
            answered=True,
            question_format="ordering",
            selected_sequence=["a", "b", "c"],
            correct_sequence=["b", "a", "c"],
        )
        == GradeOutcome.INCORRECT
    )
    # Unanswered ordering is incorrect.
    assert (
        grade_item(
            [],
            [],
            answered=False,
            question_format="ordering",
            selected_sequence=[],
            correct_sequence=["b", "a", "c"],
        )
        == GradeOutcome.INCORRECT
    )


def test_grade_matching_all_pairs() -> None:
    key = {"p1": "r2", "p2": "r1", "p3": "r2"}
    assert (
        grade_item(
            [],
            [],
            answered=True,
            question_format="matching",
            selected_pairs={"p1": "r2", "p2": "r1", "p3": "r2"},
            correct_pairs=key,
        )
        == GradeOutcome.CORRECT
    )
    # One wrong pair -> incorrect.
    assert (
        grade_item(
            [],
            [],
            answered=True,
            question_format="matching",
            selected_pairs={"p1": "r2", "p2": "r2", "p3": "r2"},
            correct_pairs=key,
        )
        == GradeOutcome.INCORRECT
    )
    # Missing a pair -> incorrect.
    assert (
        grade_item(
            [],
            [],
            answered=True,
            question_format="matching",
            selected_pairs={"p1": "r2", "p2": "r1"},
            correct_pairs=key,
        )
        == GradeOutcome.INCORRECT
    )


def test_scaled_score_endpoints_and_boundary() -> None:
    assert scaled_score(0, 65) == 100
    assert scaled_score(65, 65) == 1000
    # 750 boundary: fraction ~0.7222.
    assert passed(scaled_score(47, 65)) == (scaled_score(47, 65) >= PASS_SCALED)
    assert scaled_score(0, 0) == 100


def test_summary_is_compensatory() -> None:
    # Strong domains carry a weak one: overall can pass despite a 0% domain.
    summary = summarize(
        per_domain_correct={1: 20, 2: 17, 3: 13, 4: 8, 5: 0},
        per_domain_total={1: 20, 2: 17, 3: 13, 4: 8, 5: 7},
        full_length=True,
    )
    assert summary.raw_correct == 58
    assert summary.scored_total == 65
    assert summary.passed is True  # 58/65 ~= 89% -> well above 750
    # Domain 5 shown as weak, but it did not gate the overall pass.
    weak = next(b for b in summary.per_domain if b.domain_id == 5)
    assert weak.correct == 0
