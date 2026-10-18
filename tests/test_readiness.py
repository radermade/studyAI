"""Tests for the whole-exam readiness roll-up (Phase 8 go/no-go).

Evidence is seeded directly (grill attempts per objective, a submitted
full-length scored result, completed lab runs) so the readiness decision and
each criterion are deterministic and auditable.
"""

from __future__ import annotations

import itertools

from content.aip_c01 import BLUEPRINT_VERSION
from study_core.db import DbConnection
from study_core.mastery import MasteryEvaluator
from study_core.readiness import ReadinessEvaluator

from tests.conftest import FakeClock

_ALL_OBJECTIVES = tuple(
    f"AIP-{d}.{t}" for d, n in ((1, 6), (2, 5), (3, 4), (4, 3), (5, 2)) for t in range(1, n + 1)
)

_SEQ = itertools.count()


def _readiness(connection: DbConnection, clock: FakeClock) -> ReadinessEvaluator:
    mastery = MasteryEvaluator(connection, clock, blueprint_version=BLUEPRINT_VERSION)
    return ReadinessEvaluator(connection, clock, mastery)


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


def _seed_attempt(
    connection: DbConnection, *, learner_id: str, question_id: str, outcome: str, at_iso: str
) -> None:
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


def _cover_all_domains(connection: DbConnection, learner: str, at_iso: str) -> None:
    for objective in _ALL_OBJECTIVES:
        qid = _one_question_for(connection, objective)
        _seed_attempt(
            connection, learner_id=learner, question_id=qid, outcome="correct", at_iso=at_iso
        )


def _seed_full_length_scored(
    connection: DbConnection, learner: str, percent: float, at_iso: str
) -> None:
    sid = f"scored-{learner}"
    connection.execute(
        "INSERT INTO scored_sessions (session_id, learner_id, scope, state, scored_total, "
        "unscored_total, full_length, time_limit_seconds, started_at, deadline, submitted_at) "
        "VALUES (?, ?, '[]', 'submitted', 65, 10, 1, NULL, ?, NULL, ?)",
        (sid, learner, at_iso, at_iso),
    )
    connection.execute(
        "INSERT INTO scored_results (session_id, raw_correct, scored_total, percent, "
        "scaled_estimate, passed, per_domain, full_length, committed_at) "
        "VALUES (?, ?, 65, ?, ?, 1, '[]', 1, ?)",
        (sid, int(round(percent * 65)), percent, int(100 + 900 * percent), at_iso),
    )


def _complete_all_labs(connection: DbConnection, learner: str, at_iso: str) -> None:
    labs = connection.execute("SELECT lab_id FROM lab_definitions").fetchall()
    for i, row in enumerate(labs):
        connection.execute(
            "INSERT INTO lab_runs (run_id, learner_id, lab_id, region, state, active_step, "
            "full_solution_used, started_at, updated_at) "
            "VALUES (?, ?, ?, 'us-east-1', 'completed_independent', NULL, 0, ?, ?)",
            (f"run-{learner}-{i}", learner, str(row["lab_id"]), at_iso, at_iso),
        )


def test_fresh_learner_not_ready(connection: DbConnection, clock: FakeClock) -> None:
    report = _readiness(connection, clock).evaluate(learner_id="L1")
    assert report.ready is False
    by_key = {c.key: c for c in report.criteria}
    assert by_key["domain_gates"].met is False
    assert by_key["scored_overall"].met is False
    assert by_key["lab_matrix"].met is False
    assert len(report.domain_gates) == 5
    assert report.is_estimate is True


def test_full_evidence_is_ready(connection: DbConnection, clock: FakeClock) -> None:
    at = clock.now_utc().isoformat()
    _cover_all_domains(connection, "L1", at)
    _seed_full_length_scored(connection, "L1", percent=0.90, at_iso=at)
    _complete_all_labs(connection, "L1", at)

    report = _readiness(connection, clock).evaluate(learner_id="L1")
    by_key = {c.key: c for c in report.criteria}
    assert by_key["domain_gates"].met is True
    assert by_key["scored_overall"].met is True
    assert by_key["misconceptions"].met is True
    assert by_key["lab_matrix"].met is True
    assert report.ready is True
    assert all(e.completed for e in report.lab_matrix)


def test_low_scored_accuracy_blocks_readiness(connection: DbConnection, clock: FakeClock) -> None:
    at = clock.now_utc().isoformat()
    _cover_all_domains(connection, "L1", at)
    _complete_all_labs(connection, "L1", at)
    # Below the 85% overall threshold.
    _seed_full_length_scored(connection, "L1", percent=0.80, at_iso=at)

    report = _readiness(connection, clock).evaluate(learner_id="L1")
    by_key = {c.key: c for c in report.criteria}
    assert by_key["scored_overall"].met is False
    assert report.ready is False


def test_incomplete_lab_matrix_blocks_readiness(connection: DbConnection, clock: FakeClock) -> None:
    at = clock.now_utc().isoformat()
    _cover_all_domains(connection, "L1", at)
    _seed_full_length_scored(connection, "L1", percent=0.90, at_iso=at)
    # Complete only the first lab.
    first = connection.execute(
        "SELECT lab_id FROM lab_definitions ORDER BY lab_id LIMIT 1"
    ).fetchone()
    connection.execute(
        "INSERT INTO lab_runs (run_id, learner_id, lab_id, region, state, active_step, "
        "full_solution_used, started_at, updated_at) "
        "VALUES ('run-one', 'L1', ?, 'us-east-1', 'completed_independent', NULL, 0, ?, ?)",
        (str(first["lab_id"]), at, at),
    )
    report = _readiness(connection, clock).evaluate(learner_id="L1")
    by_key = {c.key: c for c in report.criteria}
    assert by_key["lab_matrix"].met is False
    assert report.ready is False


def test_non_full_length_scored_blocks_readiness(
    connection: DbConnection, clock: FakeClock
) -> None:
    at = clock.now_utc().isoformat()
    _cover_all_domains(connection, "L1", at)
    _complete_all_labs(connection, "L1", at)
    # A high score but not a full-length mock must not satisfy readiness.
    sid = "scored-partial-L1"
    connection.execute(
        "INSERT INTO scored_sessions (session_id, learner_id, scope, state, scored_total, "
        "unscored_total, full_length, time_limit_seconds, started_at, deadline, submitted_at) "
        "VALUES (?, 'L1', '[]', 'submitted', 20, 0, 0, NULL, ?, NULL, ?)",
        (sid, at, at),
    )
    connection.execute(
        "INSERT INTO scored_results (session_id, raw_correct, scored_total, percent, "
        "scaled_estimate, passed, per_domain, full_length, committed_at) "
        "VALUES (?, 19, 20, 0.95, 955, 1, '[]', 0, ?)",
        (sid, at),
    )
    report = _readiness(connection, clock).evaluate(learner_id="L1")
    by_key = {c.key: c for c in report.criteria}
    assert by_key["scored_overall"].met is False
    assert "not full length" in by_key["scored_overall"].detail
    assert report.ready is False
