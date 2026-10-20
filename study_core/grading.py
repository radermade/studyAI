"""Pure grading logic.

Grading compares a learner's selected options against private answer material.
It returns `grading_uncertain` rather than inventing correctness when the
rubric cannot determine an outcome (for example, an empty answer key).
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence

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


def grade_ordering(
    selected_sequence: Sequence[str],
    correct_sequence: Sequence[str],
) -> GradeOutcome:
    """Grade an ordering answer against the correct ordered sequence.

    All-or-nothing: the learner's ordered list of option ids must equal the
    correct ordered sequence exactly, both in membership and in order. An empty
    key yields `grading_uncertain`.
    """
    if not correct_sequence:
        return GradeOutcome.GRADING_UNCERTAIN
    return (
        GradeOutcome.CORRECT
        if list(selected_sequence) == list(correct_sequence)
        else GradeOutcome.INCORRECT
    )


def grade_matching(
    selected_pairs: Mapping[str, str],
    correct_pairs: Mapping[str, str],
) -> GradeOutcome:
    """Grade a matching answer against the correct prompt->response pairing.

    All-or-nothing: every prompt in the key must be mapped to exactly its
    correct response, with no missing or extra prompts. An empty key yields
    `grading_uncertain`.
    """
    if not correct_pairs:
        return GradeOutcome.GRADING_UNCERTAIN
    return (
        GradeOutcome.CORRECT
        if dict(selected_pairs) == dict(correct_pairs)
        else GradeOutcome.INCORRECT
    )
