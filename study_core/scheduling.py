"""Deterministic, versioned spaced-review scheduling.

Given prior review state, grade outcome, and confidence, compute the next due
instant. The policy is pure: it takes the current UTC time explicitly and
stores its version so later policy changes never rewrite history.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta

from study_core.study_models import GradeOutcome

SCHEDULING_POLICY_VERSION = "sched-v1"

# Expanding intervals (days) for a correctly answered item.
_PROGRESSION_DAYS: tuple[int, ...] = (1, 3, 7, 16, 35)
# Interval reset applied after an incorrect or uncertain outcome.
_RESET_DAYS = 1


@dataclass(frozen=True)
class ScheduleDecision:
    """Result of scheduling: next interval, due instant, and policy version."""

    interval_days: int
    due_at: datetime
    policy_version: str


def next_interval_days(previous_interval_days: int, outcome: GradeOutcome) -> int:
    """Return the next interval in days for a review.

    Correct answers advance along the progression; incorrect or uncertain
    answers reset to the shortest interval.
    """
    if outcome != GradeOutcome.CORRECT:
        return _RESET_DAYS
    for step in _PROGRESSION_DAYS:
        if step > previous_interval_days:
            return step
    return _PROGRESSION_DAYS[-1]


def schedule_review(
    *,
    previous_interval_days: int,
    outcome: GradeOutcome,
    now: datetime,
) -> ScheduleDecision:
    """Compute the next review schedule deterministically from `now`."""
    interval = next_interval_days(previous_interval_days, outcome)
    return ScheduleDecision(
        interval_days=interval,
        due_at=now + timedelta(days=interval),
        policy_version=SCHEDULING_POLICY_VERSION,
    )
