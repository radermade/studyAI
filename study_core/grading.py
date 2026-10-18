"""Pure grading logic.

Grading compares a learner's selected options against private answer material.
It returns `grading_uncertain` rather than inventing correctness when the
rubric cannot determine an outcome (for example, an empty answer key).
"""

from __future__ import annotations

from collections.abc import Sequence

from study_core.study_models import GradeOutcome


def grade_selection(
    selected_option_ids: Sequence[str],
    correct_option_ids: Sequence[str],
) -> GradeOutcome:
    """Grade a selection against the correct option set.

    An empty correct set means the item cannot be graded deterministically and
    yields `grading_uncertain`. For multiple-response items every correct option
    must be selected and no incorrect option chosen.
    """
    if not correct_option_ids:
        return GradeOutcome.GRADING_UNCERTAIN
    selected = set(selected_option_ids)
    correct = set(correct_option_ids)
    return GradeOutcome.CORRECT if selected == correct else GradeOutcome.INCORRECT
