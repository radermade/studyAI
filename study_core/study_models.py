"""Study-domain value objects and the secure unanswered-question DTO.

`UnansweredQuestion` is structurally incapable of carrying answer keys, rubrics,
or correctness markers: those fields simply do not exist on the type.
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import Field

from study_core.common import StrictModel


class SessionMode(StrEnum):
    """How a study session selects and presents questions."""

    GRILL = "grill"
    REVIEW = "review"


class SessionState(StrEnum):
    """Lifecycle of a session."""

    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


class GradeOutcome(StrEnum):
    """Result of grading an attempt."""

    CORRECT = "correct"
    INCORRECT = "incorrect"
    GRADING_UNCERTAIN = "grading_uncertain"


class ReviewState(StrEnum):
    """Lifecycle of a spaced-review schedule."""

    SCHEDULED = "scheduled"
    RESOLVED = "resolved"
    SUPERSEDED = "superseded"


class QuestionOption(StrictModel):
    """A selectable option shown to the learner (no correctness flag)."""

    option_id: str
    text: str


class UnansweredQuestion(StrictModel):
    """Public question projection. Carries no answer, rubric, or correctness."""

    question_id: str
    prompt: str
    scenario_constraint: str
    question_format: str
    options: tuple[QuestionOption, ...]
    objective_ids: tuple[str, ...]
    source_ids: tuple[str, ...]


class SessionResult(StrictModel):
    """A durable session reference returned to callers."""

    session_id: str
    learner_id: str
    mode: SessionMode
    state: SessionState
    blueprint_version: str
    started_at: datetime


class GradeResult(StrictModel):
    """Committed grading summary."""

    attempt_id: str
    question_id: str
    outcome: GradeOutcome
    confidence: int = Field(ge=0, le=100)
    next_review_due_at: datetime | None


class DueReview(StrictModel):
    """One due review item."""

    review_id: str
    question_id: str
    objective_id: str
    due_at: datetime


class DueReviewPage(StrictModel):
    """A deterministic page of due reviews."""

    items: tuple[DueReview, ...]


class ObjectiveProgress(StrictModel):
    """Evidence-derived progress for a single objective."""

    objective_id: str
    attempts: int
    correct: int
    accuracy: float | None
    mean_confidence: float | None
    open_misconceptions: int


class ProgressReport(StrictModel):
    """Evidence-based progress across objectives.

    `is_estimate` and `inputs` make clear this is an internal estimate and not
    an AWS score prediction.
    """

    learner_id: str
    objectives: tuple[ObjectiveProgress, ...]
    uncovered_objectives: tuple[str, ...]
    is_estimate: bool = True
    note: str = "Internal estimate derived from committed evidence; not an AWS score."


class OptionRationale(StrictModel):
    """Why one option is correct or incorrect (revealed only after answering)."""

    option_id: str
    is_correct: bool
    rationale: str


class AnswerExplanation(StrictModel):
    """Post-answer teaching material for a question.

    Only returned after the learner has committed an attempt, so it never
    leaks into the unanswered-question projection.
    """

    question_id: str
    correct_option_ids: tuple[str, ...]
    explanation: str
    option_rationales: tuple[OptionRationale, ...]


class ScoredSessionView(StrictModel):
    """A started scored session reference (no answer material)."""

    session_id: str
    scored_total: int
    unscored_total: int
    item_count: int
    full_length: bool
    time_limit_seconds: int | None
    excluded_domains: tuple[int, ...]


class ScoredItemView(StrictModel):
    """One scored-session item shown to the learner.

    Carries no correct answer, rationale, explanation, objective, or
    scored/unscored flag, so nothing is leaked during the session.
    """

    session_id: str
    position: int
    total: int
    question_id: str
    prompt: str
    question_format: str
    options: tuple[QuestionOption, ...]
    selected_option_ids: tuple[str, ...]
    answered: bool


class DomainResult(StrictModel):
    """Informational per-domain result (never a per-domain pass gate)."""

    domain_id: int
    correct: int
    total: int


class ScoredResult(StrictModel):
    """The committed result of a scored session, labeled an internal estimate."""

    session_id: str
    raw_correct: int
    scored_total: int
    percent: float
    scaled_estimate: int
    passed: bool
    full_length: bool
    per_domain: tuple[DomainResult, ...]
    estimate_note: str = (
        "Internal estimate only; not an official AWS scaled score. "
        "Pass threshold is a 750-equivalent on a transparent 100-1000 scale."
    )


class MissedItem(StrictModel):
    """A missed scored item with its teaching material, for Review."""

    question_id: str
    objective_ids: tuple[str, ...]
    unanswered: bool
    prompt: str
    correct_option_ids: tuple[str, ...]
    explanation: str
    option_rationales: tuple[OptionRationale, ...]


class SearchResult(StrictModel):
    """One attributed local search hit."""

    content_id: str
    title: str
    snippet: str
    objective_ids: tuple[str, ...]
    freshness: str


class SearchPage(StrictModel):
    """A deterministic page of search results."""

    results: tuple[SearchResult, ...]
    offset: int
    has_more: bool


class MasteryObjective(StrictModel):
    """Per-objective grill evidence inside a domain mastery report."""

    objective_id: str
    attempts: int
    correct: int
    accuracy: float | None
    open_misconceptions: int
    covered: bool


class MasteryCriterion(StrictModel):
    """One named exit-gate criterion with its pass state and reasoning.

    `mandatory` criteria must all pass for the gate to pass; informational
    criteria (e.g. an optional scored session) are shown but never block.
    """

    key: str
    label: str
    mandatory: bool
    met: bool
    detail: str


class DomainMasteryReport(StrictModel):
    """Evidence-based exit-gate evaluation for a single exam domain.

    This is a transparent internal study gate, not an AWS score prediction.
    Every input criterion is exposed so the pass/fail decision is auditable.
    """

    learner_id: str
    domain_id: int
    passed: bool
    accuracy_threshold: float
    grill_attempts: int
    grill_correct: int
    grill_accuracy: float | None
    objectives: tuple[MasteryObjective, ...]
    criteria: tuple[MasteryCriterion, ...]
    is_estimate: bool = True
    note: str = (
        "Internal study exit gate derived from committed evidence; "
        "not an AWS score prediction or exam-readiness guarantee."
    )


class DomainGateSummary(StrictModel):
    """Compact pass/fail summary of one domain's exit gate for the readiness roll-up."""

    domain_id: int
    passed: bool
    grill_accuracy: float | None


class LabMatrixEntry(StrictModel):
    """Completion state of one authored lab for the required-lab matrix."""

    lab_id: str
    title: str
    completed: bool
    independent: bool


class ReadinessReport(StrictModel):
    """Whole-exam readiness roll-up across all five domains.

    A transparent internal go/no-go derived from committed evidence: the five
    domain exit gates, overall scored accuracy, misconception state, and the
    required-lab matrix. It is never a prediction of the official AWS result.
    """

    learner_id: str
    ready: bool
    overall_threshold: float
    scored_accuracy: float | None
    scored_is_full_length: bool
    open_misconceptions: int
    domain_gates: tuple[DomainGateSummary, ...]
    lab_matrix: tuple[LabMatrixEntry, ...]
    criteria: tuple[MasteryCriterion, ...]
    is_estimate: bool = True
    note: str = (
        "Internal readiness estimate from committed evidence; not a prediction "
        "of the official AWS exam result. Complete the official practice exam "
        "as the final external signal."
    )
