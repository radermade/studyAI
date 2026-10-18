"""Tests for the Domain mastery / exit-gate evaluator.

Attempts are seeded directly so grill accuracy and coverage are deterministic;
one end-to-end check confirms the attempts/objective join matches the real
grading path. Lab completion and scored results are driven through their
services so the evaluator reads exactly what production writes.
"""

from __future__ import annotations

import itertools

from content.aip_c01 import BLUEPRINT_VERSION
from study_aws.validators import FakeValidator
from study_core.db import DbConnection
from study_core.lab_models import EvidenceKind
from study_core.lab_service import LabService
from study_core.mastery import MasteryEvaluator
from study_core.service import StudyService
from study_core.study_models import SessionMode

from tests.conftest import FakeClock

_DOMAIN1_OBJECTIVES = (
    "AIP-1.1",
    "AIP-1.2",
    "AIP-1.3",
    "AIP-1.4",
    "AIP-1.5",
    "AIP-1.6",
)


def _evaluator(connection: DbConnection, clock: FakeClock) -> MasteryEvaluator:
    return MasteryEvaluator(connection, clock, blueprint_version=BLUEPRINT_VERSION)


def _one_question_for(connection: DbConnection, objective_id: str) -> str:
    row = connection.execute(
        "SELECT q.question_id FROM questions q "
        "JOIN question_objectives qo ON qo.question_id = q.question_id "
        "WHERE qo.objective_id = ? AND q.review_status = 'reviewed' "
        "AND EXISTS (SELECT 1 FROM option_rationales r WHERE r.question_id = q.question_id) "
        "ORDER BY q.question_id LIMIT 1",
        (objective_id,),
    ).fetchone()
    assert row is not None, f"no authored question for {objective_id}"
    return str(row["question_id"])


_SEQ = itertools.count()


def _seed_attempt(
    connection: DbConnection,
    *,
    learner_id: str,
    question_id: str,
    outcome: str,
    at_iso: str,
) -> None:
    # A session row is required by the FK on attempts.session_id. Each seeded
    # attempt gets a unique id so repeated attempts on the same question insert.
    n = next(_SEQ)
    session_id = f"sess-{learner_id}-{n}"
    connection.execute(
        "INSERT OR IGNORE INTO sessions (session_id, learner_id, mode, objective_filter, "
        "blueprint_version, state, started_at) VALUES (?, ?, 'grill', '[]', ?, 'active', ?)",
        (session_id, learner_id, BLUEPRINT_VERSION, at_iso),
    )
    connection.execute(
        "INSERT INTO attempts (attempt_id, session_id, question_id, learner_id, outcome, "
        "confidence, elapsed_seconds, committed_at) VALUES (?, ?, ?, ?, ?, 80, 5.0, ?)",
        (f"att-{learner_id}-{n}", session_id, question_id, learner_id, outcome, at_iso),
    )


def _cover_all_objectives(
    connection: DbConnection, clock: FakeClock, learner: str, *, correct: int, wrong: int
) -> None:
    """Seed one correct attempt per objective, then extra correct/wrong attempts.

    Covers every Domain 1 objective (so coverage passes), then tops up overall
    accuracy with additional correct and wrong attempts on AIP-1.1.
    """
    at = clock.now_utc().isoformat()
    for objective in _DOMAIN1_OBJECTIVES:
        qid = _one_question_for(connection, objective)
        _seed_attempt(connection, learner_id=learner, question_id=qid, outcome="correct", at_iso=at)
    extra_qid = _one_question_for(connection, "AIP-1.1")
    for i in range(correct):
        _seed_attempt(
            connection,
            learner_id=learner,
            question_id=extra_qid,
            outcome="correct",
            at_iso=f"{at}-c{i}",
        )
    for i in range(wrong):
        _seed_attempt(
            connection,
            learner_id=learner,
            question_id=extra_qid,
            outcome="incorrect",
            at_iso=f"{at}-w{i}",
        )


def test_fresh_learner_gate_not_met(connection: DbConnection, clock: FakeClock) -> None:
    gate = _evaluator(connection, clock).evaluate(learner_id="L1", domain_id=1)
    assert gate.passed is False
    assert gate.grill_attempts == 0
    # Coverage and accuracy must both be unmet with no evidence.
    by_key = {c.key: c for c in gate.criteria}
    assert by_key["coverage"].met is False
    assert by_key["accuracy"].met is False
    assert gate.is_estimate is True


def test_coverage_gap_blocks_gate(connection: DbConnection, clock: FakeClock) -> None:
    at = clock.now_utc().isoformat()
    # Cover only five of six objectives.
    for objective in _DOMAIN1_OBJECTIVES[:-1]:
        qid = _one_question_for(connection, objective)
        _seed_attempt(connection, learner_id="L1", question_id=qid, outcome="correct", at_iso=at)
    gate = _evaluator(connection, clock).evaluate(learner_id="L1", domain_id=1)
    by_key = {c.key: c for c in gate.criteria}
    assert by_key["coverage"].met is False
    assert "AIP-1.6" in by_key["coverage"].detail
    assert gate.passed is False


def test_accuracy_below_threshold_blocks_gate(connection: DbConnection, clock: FakeClock) -> None:
    # 6 correct (coverage) + 1 correct + 4 wrong = 7/11 ~= 64% < 80%.
    _cover_all_objectives(connection, clock, "L1", correct=1, wrong=4)
    gate = _evaluator(connection, clock).evaluate(learner_id="L1", domain_id=1)
    by_key = {c.key: c for c in gate.criteria}
    assert by_key["coverage"].met is True
    assert by_key["accuracy"].met is False
    assert gate.passed is False


def test_gate_passes_with_full_evidence(connection: DbConnection, clock: FakeClock) -> None:
    # 6 correct (coverage) + 4 correct + 0 wrong = 10/10 = 100% >= 80%.
    _cover_all_objectives(connection, clock, "L1", correct=4, wrong=0)
    # Complete a Domain 1 lab independently so the hands-on criterion is met.
    labs = LabService(connection, clock, FakeValidator(EvidenceKind.RESOURCE_PRESENT))
    run = labs.start_lab(
        learner_id="L1",
        lab_id="lab-01-model-comparison",
        region="us-east-1",
        request_id="start1",
        acknowledged_cost=True,
        acknowledged_cleanup=True,
    )
    labs.check(run_id=run.run_id, checkpoint_id="c1-model-access", event_id="chk1")
    labs.complete_lab(run_id=run.run_id, request_id="done1")

    gate = _evaluator(connection, clock).evaluate(learner_id="L1", domain_id=1)
    by_key = {c.key: c for c in gate.criteria}
    assert by_key["coverage"].met is True
    assert by_key["accuracy"].met is True
    assert by_key["misconceptions"].met is True
    assert by_key["hands_on"].met is True
    assert gate.passed is True


def test_open_misconception_blocks_gate(connection: DbConnection, clock: FakeClock) -> None:
    _cover_all_objectives(connection, clock, "L1", correct=4, wrong=0)
    # Open a misconception the way grade_and_record would.
    connection.execute(
        "INSERT INTO misconceptions (misconception_id, learner_id, objective_id, state, "
        "updated_at) VALUES ('mis-L1-AIP-1.3', 'L1', 'AIP-1.3', 'open', ?)",
        (clock.now_utc().isoformat(),),
    )
    gate = _evaluator(connection, clock).evaluate(learner_id="L1", domain_id=1)
    by_key = {c.key: c for c in gate.criteria}
    assert by_key["misconceptions"].met is False
    assert gate.passed is False


def test_scored_criterion_is_informational_not_blocking(
    connection: DbConnection, clock: FakeClock
) -> None:
    # Full grill + lab evidence, but no scored session: the gate still passes
    # because the scored criterion is informational only.
    _cover_all_objectives(connection, clock, "L1", correct=4, wrong=0)
    labs = LabService(connection, clock, FakeValidator(EvidenceKind.RESOURCE_PRESENT))
    run = labs.start_lab(
        learner_id="L1",
        lab_id="lab-01-model-comparison",
        region="us-east-1",
        request_id="s",
        acknowledged_cost=True,
        acknowledged_cleanup=True,
    )
    labs.check(run_id=run.run_id, checkpoint_id="c1-model-access", event_id="c")
    labs.complete_lab(run_id=run.run_id, request_id="d")

    gate = _evaluator(connection, clock).evaluate(learner_id="L1", domain_id=1)
    by_key = {c.key: c for c in gate.criteria}
    assert by_key["scored_session"].mandatory is False
    assert by_key["scored_session"].met is False
    assert gate.passed is True


def test_end_to_end_accuracy_matches_real_grading(
    connection: DbConnection, clock: FakeClock
) -> None:
    # Drive the real grill path once so the attempts/objective join is exercised
    # exactly as production writes it.
    service = StudyService(
        connection,
        clock,
        _FirstChoice(),
        blueprint_version=BLUEPRINT_VERSION,
    )
    session = service.start_session(
        learner_id="L1", mode=SessionMode.GRILL, objective_filter=("AIP-1.1",), request_id="r1"
    )
    question = service.next_question(session_id=session.session_id, request_id="nq1")
    service.grade_and_record(
        session_id=session.session_id,
        question_id=question.question_id,
        selected_option_ids=[question.options[0].option_id],
        confidence=80,
        elapsed_seconds=4.0,
        event_id="e1",
    )
    gate = _evaluator(connection, clock).evaluate(learner_id="L1", domain_id=1)
    assert gate.grill_attempts == 1
    aip11 = next(o for o in gate.objectives if o.objective_id == "AIP-1.1")
    assert aip11.attempts == 1


class _FirstChoice:
    def choose_index(self, upper_bound: int) -> int:
        if upper_bound <= 0:
            raise ValueError("upper_bound must be positive")
        return 0


_DOMAIN2_OBJECTIVES = ("AIP-2.1", "AIP-2.2", "AIP-2.3", "AIP-2.4", "AIP-2.5")


def test_domain2_gate_passes_with_full_evidence(connection: DbConnection, clock: FakeClock) -> None:
    at = clock.now_utc().isoformat()
    # Cover every Domain 2 objective with a correct attempt.
    for objective in _DOMAIN2_OBJECTIVES:
        qid = _one_question_for(connection, objective)
        _seed_attempt(connection, learner_id="L2", question_id=qid, outcome="correct", at_iso=at)
    # Complete the Domain 2 bounded-agent lab independently. The validator
    # reports presence for the create check and absence for the cleanup check.
    labs = LabService(connection, clock, _PresenceThenAbsence())
    run = labs.start_lab(
        learner_id="L2",
        lab_id="lab-06-bounded-agent",
        region="us-east-1",
        request_id="start-d2",
        acknowledged_cost=True,
        acknowledged_cleanup=True,
    )
    labs.check(run_id=run.run_id, checkpoint_id="c1-tool-function-present", event_id="chk-d2")
    labs.record_self_report(
        run_id=run.run_id, checkpoint_id="c2-unsafe-call-rejected", event_id="sr-d2"
    )
    # A cleanup checkpoint is self-reported (deletion requested), then the
    # read-only absence check confirms it, moving it to CLEANED_UP.
    labs.record_self_report(
        run_id=run.run_id, checkpoint_id="c3-tool-function-removed", event_id="sr-clean-d2"
    )
    labs.check(run_id=run.run_id, checkpoint_id="c3-tool-function-removed", event_id="clean-d2")
    labs.complete_lab(run_id=run.run_id, request_id="done-d2")

    gate = _evaluator(connection, clock).evaluate(learner_id="L2", domain_id=2)
    by_key = {c.key: c for c in gate.criteria}
    assert by_key["coverage"].met is True
    assert by_key["accuracy"].met is True
    assert by_key["hands_on"].met is True
    assert gate.passed is True


class _PresenceThenAbsence:
    """Validator fake: resources present on create checks, absent on cleanup.

    Cleanup validator IDs end with ``-absent`` by convention, so the cleanup
    check observes absence (which establishes CLEANED_UP) while create checks
    observe presence (which establishes VERIFIED).
    """

    def validate(self, request: object) -> object:
        from datetime import UTC, datetime

        from study_core.lab_models import EvidenceKind, ValidationEvidence

        validator_id = getattr(request, "validator_id", "")
        kind = (
            EvidenceKind.RESOURCE_ABSENT
            if validator_id.endswith("-absent")
            else EvidenceKind.RESOURCE_PRESENT
        )
        return ValidationEvidence(
            attempt_id="",
            kind=kind,
            observed_at=datetime.now(UTC),
            summary=f"fake:{validator_id}:{kind.value}",
        )
