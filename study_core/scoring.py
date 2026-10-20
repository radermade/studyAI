"""Pure scored-session selection and scoring (AIP-C01 mechanics).

No I/O here: these functions decide domain allocation, grade answers, and map a
raw percentage to a transparent 100-1000 scaled-score estimate. They are
deterministic given their inputs so they are fully unit-testable.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from study_core.common import DOMAIN_WEIGHTS
from study_core.grading import grade_matching, grade_ordering
from study_core.study_models import GradeOutcome

# Official full-length structure.
FULL_SCORED_TOTAL = 65
FULL_UNSCORED_TOTAL = 10
FULL_TOTAL = FULL_SCORED_TOTAL + FULL_UNSCORED_TOTAL

# Scaled-score estimate bounds and pass threshold.
SCALE_MIN = 100
SCALE_MAX = 1000
PASS_SCALED = 750

# The pool must comfortably exceed a full scored set before unscored items are
# meaningful; until then unscored_total is 0.
UNSCORED_ACTIVATION_MIN_POOL = FULL_TOTAL


def allocate_scored_counts(
    *,
    domain_capacity: Mapping[int, int],
    target_scored_total: int,
) -> dict[int, int]:
    """Allocate scored items per domain by official weight, bounded by capacity.

    Uses largest-remainder rounding over the official weights of the domains
    that have capacity, then caps each domain at its available question count
    and redistributes any shortfall to domains that still have room.

    Args:
        domain_capacity: available reviewed question count per domain id.
        target_scored_total: desired number of scored items (e.g. 65).

    Returns:
        A mapping of domain id to scored-item count. The total equals
        min(target_scored_total, sum of capacities).
    """
    eligible = {d: c for d, c in domain_capacity.items() if c > 0}
    if not eligible:
        return {}
    achievable = min(target_scored_total, sum(eligible.values()))
    weight_sum = sum(DOMAIN_WEIGHTS[d] for d in eligible)

    # Ideal (fractional) share per domain, then largest-remainder rounding.
    ideals = {d: achievable * DOMAIN_WEIGHTS[d] / weight_sum for d in eligible}
    floors = {d: int(ideals[d]) for d in eligible}
    allocated = sum(floors.values())
    remainder = achievable - allocated
    # Hand out the remaining seats to the largest fractional parts.
    by_frac = sorted(
        eligible,
        key=lambda d: (ideals[d] - floors[d], DOMAIN_WEIGHTS[d]),
        reverse=True,
    )
    counts = dict(floors)
    for d in by_frac[:remainder]:
        counts[d] += 1

    # Cap at capacity and redistribute any overflow to domains with headroom.
    _rebalance_to_capacity(counts, eligible)
    return {d: c for d, c in counts.items() if c > 0}


def _rebalance_to_capacity(counts: dict[int, int], capacity: Mapping[int, int]) -> None:
    overflow = 0
    for d in list(counts):
        if counts[d] > capacity[d]:
            overflow += counts[d] - capacity[d]
            counts[d] = capacity[d]
    # Redistribute overflow to domains with remaining headroom, by weight order.
    while overflow > 0:
        room = [d for d in counts if counts[d] < capacity[d]]
        if not room:
            break
        room.sort(key=lambda d: DOMAIN_WEIGHTS[d], reverse=True)
        for d in room:
            if overflow == 0:
                break
            counts[d] += 1
            overflow -= 1


def unscored_total_for_pool(pool_size: int) -> int:
    """Return how many unscored items to include given the reviewed pool size."""
    return FULL_UNSCORED_TOTAL if pool_size >= UNSCORED_ACTIVATION_MIN_POOL else 0


def grade_item(
    selected_option_ids: Sequence[str],
    correct_option_ids: Sequence[str],
    *,
    answered: bool,
    question_format: str = "multiple_choice",
    selected_sequence: Sequence[str] | None = None,
    correct_sequence: Sequence[str] | None = None,
    selected_pairs: Mapping[str, str] | None = None,
    correct_pairs: Mapping[str, str] | None = None,
) -> GradeOutcome:
    """Grade one item under AIP-C01 mechanics, dispatching by question type.

    All four types are all-or-nothing; an unanswered item is always incorrect.

    - multiple_choice / multiple_response: the selected option set must equal
      the correct option set.
    - ordering: the selected ordered sequence must equal the correct sequence.
    - matching: the selected prompt->response pairing must equal the key.
    """
    if not answered:
        return GradeOutcome.INCORRECT
    if question_format == "ordering":
        return grade_ordering(selected_sequence or (), correct_sequence or ())
    if question_format == "matching":
        return grade_matching(selected_pairs or {}, correct_pairs or {})
    if not correct_option_ids:
        return GradeOutcome.GRADING_UNCERTAIN
    return (
        GradeOutcome.CORRECT
        if set(selected_option_ids) == set(correct_option_ids)
        else GradeOutcome.INCORRECT
    )


def scaled_score(raw_correct: int, scored_total: int) -> int:
    """Map a raw correct count to the transparent 100-1000 scaled estimate.

    Linear: 0% -> 100, 100% -> 1000. This is an internal estimate, not AWS's
    proprietary scaled score.
    """
    if scored_total <= 0:
        return SCALE_MIN
    fraction = max(0.0, min(1.0, raw_correct / scored_total))
    return round(SCALE_MIN + (SCALE_MAX - SCALE_MIN) * fraction)


def passed(scaled: int) -> bool:
    """Return True when a scaled estimate meets the 750 pass threshold."""
    return scaled >= PASS_SCALED


@dataclass(frozen=True)
class DomainBreakdown:
    """Informational per-domain performance (never a per-domain gate)."""

    domain_id: int
    correct: int
    total: int


@dataclass(frozen=True)
class ScoreSummary:
    """The computed result of a scored session."""

    raw_correct: int
    scored_total: int
    percent: float
    scaled_estimate: int
    passed: bool
    per_domain: tuple[DomainBreakdown, ...]
    full_length: bool


def summarize(
    *,
    per_domain_correct: Mapping[int, int],
    per_domain_total: Mapping[int, int],
    full_length: bool,
) -> ScoreSummary:
    """Build a compensatory score summary from per-domain correct/total counts."""
    raw_correct = sum(per_domain_correct.values())
    scored_total = sum(per_domain_total.values())
    percent = (raw_correct / scored_total) if scored_total else 0.0
    scaled = scaled_score(raw_correct, scored_total)
    breakdown = tuple(
        DomainBreakdown(
            domain_id=d,
            correct=per_domain_correct.get(d, 0),
            total=per_domain_total[d],
        )
        for d in sorted(per_domain_total)
    )
    return ScoreSummary(
        raw_correct=raw_correct,
        scored_total=scored_total,
        percent=percent,
        scaled_estimate=scaled,
        passed=passed(scaled),
        per_domain=breakdown,
        full_length=full_length,
    )
