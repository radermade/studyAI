"""Scored-session service: AWS-style exam simulation over SQLite.

Selects questions by official domain weighting (scaled to available content),
withholds feedback until submission, grades under AIP-C01 mechanics, and
persists an immutable result plus per-item misses. The scored/unscored flag and
all answer material stay server-side.
"""

from __future__ import annotations

import json
import sqlite3
import uuid
from collections.abc import Sequence
from datetime import timedelta

from study_core.common import domain_of, stable_shuffle
from study_core.db import DbConnection, immediate_transaction
from study_core.machines import SCORED_SESSION_MACHINE, ScoredSessionState
from study_core.ports import Clock, RandomSource
from study_core.scoring import (
    allocate_scored_counts,
    grade_item,
    summarize,
    unscored_total_for_pool,
)
from study_core.service import ContentGapError, NotFoundError
from study_core.state_machine import IllegalTransitionError
from study_core.study_models import (
    DomainResult,
    GradeOutcome,
    MissedItem,
    OptionRationale,
    QuestionOption,
    ScoredItemView,
    ScoredResult,
    ScoredSessionView,
)

FULL_SCORED_TARGET = 65


class ScoredSessionError(Exception):
    """A scored-session operation was invalid (e.g. answering after submit)."""


class ScoredSessionService:
    """Scored-session lifecycle backed by one SQLite connection."""

    def __init__(
        self,
        conn: DbConnection,
        clock: Clock,
        random_source: RandomSource,
    ) -> None:
        self._conn = conn
        self._clock = clock
        self._random = random_source

    # -- start ---------------------------------------------------------------

    def start(
        self,
        *,
        learner_id: str,
        scope_domains: Sequence[int] = (),
        time_limit_seconds: int | None = None,
    ) -> ScoredSessionView:
        """Select questions by official weighting and start a session."""
        capacity, excluded = self._domain_capacity(scope_domains)
        if not capacity:
            raise ContentGapError("no reviewed questions available for a scored session")

        counts = allocate_scored_counts(
            domain_capacity=capacity, target_scored_total=FULL_SCORED_TARGET
        )
        pool_size = sum(capacity.values())
        unscored_total = unscored_total_for_pool(pool_size)

        scored_items = self._pick_items(counts, exclude=set())
        used = {qid for _, qid in scored_items}
        unscored_items = self._pick_unscored(capacity, unscored_total, exclude=used)

        full_length = (
            sum(counts.values()) == FULL_SCORED_TARGET
            and unscored_total == 10
            and len(capacity) == 5
        )

        session_id = f"scored-{uuid.uuid4().hex}"
        now = self._clock.now_utc()
        deadline = now + timedelta(seconds=time_limit_seconds) if time_limit_seconds else None

        # Interleave scored and unscored items into a shuffled position order.
        ordered = self._interleave(scored_items, unscored_items)
        with immediate_transaction(self._conn):
            # Non-accumulating: a new session clears the learner's prior one so
            # at most one scored session's data exists at a time.
            self._clear_learner_sessions(learner_id)
            self._conn.execute(
                "INSERT INTO scored_sessions (session_id, learner_id, scope, state, "
                "scored_total, unscored_total, full_length, time_limit_seconds, started_at, "
                "deadline, submitted_at) VALUES (?, ?, ?, 'in_progress', ?, ?, ?, ?, ?, ?, NULL)",
                (
                    session_id,
                    learner_id,
                    json.dumps(sorted(scope_domains)),
                    sum(counts.values()),
                    unscored_total,
                    1 if full_length else 0,
                    time_limit_seconds,
                    now.isoformat(),
                    deadline.isoformat() if deadline else None,
                ),
            )
            for position, (is_scored, qid) in enumerate(ordered):
                self._conn.execute(
                    "INSERT INTO scored_session_items (session_id, position, question_id, "
                    "is_scored, domain_id) VALUES (?, ?, ?, ?, ?)",
                    (session_id, position, qid, 1 if is_scored else 0, self._domain_for(qid)),
                )
        return ScoredSessionView(
            session_id=session_id,
            scored_total=sum(counts.values()),
            unscored_total=unscored_total,
            item_count=len(ordered),
            full_length=full_length,
            time_limit_seconds=time_limit_seconds,
            excluded_domains=tuple(sorted(excluded)),
        )

    def _domain_capacity(self, scope_domains: Sequence[int]) -> tuple[dict[int, int], set[int]]:
        """Return reviewed-question capacity per in-scope domain and excluded domains."""
        capacity: dict[int, int] = {}
        # Each question is counted once under its primary (lowest) domain so
        # allocation and selection stay consistent.
        q_domains = self._question_domains()
        for domains in q_domains.values():
            if domains:
                primary = min(domains)
                capacity[primary] = capacity.get(primary, 0) + 1
        requested = set(scope_domains)
        excluded: set[int] = set()
        if requested:
            excluded = {d for d in requested if capacity.get(d, 0) == 0}
            capacity = {d: c for d, c in capacity.items() if d in requested and c > 0}
        else:
            capacity = {d: c for d, c in capacity.items() if c > 0}
        return capacity, excluded

    def _question_domains(self) -> dict[str, set[int]]:
        rows = self._conn.execute(
            "SELECT q.question_id AS qid, qo.objective_id AS oid "
            "FROM questions q JOIN question_objectives qo ON qo.question_id = q.question_id "
            "WHERE q.review_status = 'reviewed'"
        ).fetchall()
        result: dict[str, set[int]] = {}
        for row in rows:
            result.setdefault(str(row["qid"]), set()).add(domain_of(str(row["oid"])))
        return result

    def _domain_for(self, question_id: str) -> int:
        """Return a question's primary (lowest) domain from its objectives."""
        objectives = self._objectives_for(question_id)
        if not objectives:
            raise NotFoundError(f"question {question_id} has no objective")
        return min(domain_of(o) for o in objectives)

    def _questions_in_domain(self, domain_id: int) -> list[str]:
        # A question belongs to the domain of its primary (lowest) objective, so
        # each question is counted and selected under exactly one domain bucket.
        q_domains = self._question_domains()
        qs = sorted(
            qid for qid, domains in q_domains.items() if domains and min(domains) == domain_id
        )
        return qs

    def _pick_items(self, counts: dict[int, int], *, exclude: set[str]) -> list[tuple[bool, str]]:
        picked: list[tuple[bool, str]] = []
        used = set(exclude)
        for domain_id in sorted(counts):
            pool = [q for q in self._questions_in_domain(domain_id) if q not in used]
            take = min(counts[domain_id], len(pool))
            for _ in range(take):
                idx = self._random.choose_index(len(pool))
                qid = pool.pop(idx)
                used.add(qid)
                picked.append((True, qid))
        return picked

    def _pick_unscored(
        self, capacity: dict[int, int], unscored_total: int, *, exclude: set[str]
    ) -> list[tuple[bool, str]]:
        if unscored_total <= 0:
            return []
        used = set(exclude)
        pool = [
            q
            for domain_id in sorted(capacity)
            for q in self._questions_in_domain(domain_id)
            if q not in used
        ]
        picked: list[tuple[bool, str]] = []
        for _ in range(min(unscored_total, len(pool))):
            idx = self._random.choose_index(len(pool))
            qid = pool.pop(idx)
            picked.append((False, qid))
        return picked

    def _interleave(
        self, scored: list[tuple[bool, str]], unscored: list[tuple[bool, str]]
    ) -> list[tuple[bool, str]]:
        combined = [*scored, *unscored]
        # Deterministic shuffle via the injected random source.
        order: list[tuple[bool, str]] = []
        pool = list(combined)
        while pool:
            idx = self._random.choose_index(len(pool))
            order.append(pool.pop(idx))
        return order

    # -- navigation and answering -------------------------------------------

    def current_item(self, *, session_id: str, position: int) -> ScoredItemView:
        """Return the item at a position with no answer material or scored flag."""
        session = self._session_row(session_id)
        item = self._conn.execute(
            "SELECT question_id FROM scored_session_items WHERE session_id = ? AND position = ?",
            (session_id, position),
        ).fetchone()
        if item is None:
            raise NotFoundError(f"no item at position {position}")
        question_id = str(item["question_id"])
        total = int(
            self._conn.execute(
                "SELECT COUNT(*) AS n FROM scored_session_items WHERE session_id = ?",
                (session_id,),
            ).fetchone()["n"]
        )
        q = self._conn.execute(
            "SELECT prompt FROM questions WHERE question_id = ?", (question_id,)
        ).fetchone()
        base_options = [
            QuestionOption(option_id=str(r["option_id"]), text=str(r["text"]))
            for r in self._conn.execute(
                "SELECT option_id, text FROM question_options WHERE question_id = ? "
                "ORDER BY option_id",
                (question_id,),
            ).fetchall()
        ]
        # Shuffle display order deterministically per (session, question) so the
        # correct answer is not positionally predictable, while re-rendering the
        # same item keeps a stable order. Grading uses option IDs, not position.
        options = tuple(stable_shuffle(base_options, seed_key=f"{session_id}:{question_id}"))
        answer = self._conn.execute(
            "SELECT selected_option_ids, answered FROM scored_answers "
            "WHERE session_id = ? AND question_id = ?",
            (session_id, question_id),
        ).fetchone()
        selected = tuple(json.loads(answer["selected_option_ids"])) if answer else ()
        answered = bool(answer["answered"]) if answer else False
        _ = session
        return ScoredItemView(
            session_id=session_id,
            position=position,
            total=total,
            question_id=question_id,
            prompt=str(q["prompt"]),
            options=options,
            selected_option_ids=selected,
            answered=answered,
        )

    def answer(
        self,
        *,
        session_id: str,
        question_id: str,
        selected_option_ids: Sequence[str],
    ) -> None:
        """Record or update an answer; rejected once the session is submitted."""
        session = self._session_row(session_id)
        if str(session["state"]) != "in_progress":
            raise ScoredSessionError("session is not accepting answers")
        now = self._clock.now_utc().isoformat()
        answered = len(selected_option_ids) > 0
        with immediate_transaction(self._conn):
            self._conn.execute(
                "INSERT INTO scored_answers (session_id, question_id, selected_option_ids, "
                "answered, updated_at) VALUES (?, ?, ?, ?, ?) "
                "ON CONFLICT(session_id, question_id) DO UPDATE SET selected_option_ids = ?, "
                "answered = ?, updated_at = ?",
                (
                    session_id,
                    question_id,
                    json.dumps(sorted(selected_option_ids)),
                    1 if answered else 0,
                    now,
                    json.dumps(sorted(selected_option_ids)),
                    1 if answered else 0,
                    now,
                ),
            )

    # -- submit --------------------------------------------------------------

    def submit(self, *, session_id: str, event_id: str) -> ScoredResult:
        """Grade the session, persist an immutable result, and record misses."""
        session = self._session_row(session_id)
        current = ScoredSessionState(str(session["state"]))
        if current == ScoredSessionState.SUBMITTED:
            return self._load_result(session_id)
        try:
            SCORED_SESSION_MACHINE.assert_transition(current, ScoredSessionState.SUBMITTED)
        except IllegalTransitionError as exc:
            raise ScoredSessionError(str(exc)) from exc

        items = self._conn.execute(
            "SELECT question_id, is_scored, domain_id FROM scored_session_items "
            "WHERE session_id = ? ORDER BY position",
            (session_id,),
        ).fetchall()
        answers = {
            str(r["question_id"]): (json.loads(r["selected_option_ids"]), bool(r["answered"]))
            for r in self._conn.execute(
                "SELECT question_id, selected_option_ids, answered FROM scored_answers "
                "WHERE session_id = ?",
                (session_id,),
            ).fetchall()
        }

        per_correct: dict[int, int] = {}
        per_total: dict[int, int] = {}
        misses: list[tuple[str, str, bool]] = []
        for item in items:
            if not bool(item["is_scored"]):
                continue
            qid = str(item["question_id"])
            domain = int(item["domain_id"])
            per_total[domain] = per_total.get(domain, 0) + 1
            correct_ids = self._correct_option_ids(qid)
            selected, answered = answers.get(qid, ([], False))
            outcome = grade_item(selected, correct_ids, answered=answered)
            if outcome == GradeOutcome.CORRECT:
                per_correct[domain] = per_correct.get(domain, 0) + 1
            else:
                misses.append((qid, self._primary_objective(qid), not answered))

        summary = summarize(
            per_domain_correct=per_correct,
            per_domain_total=per_total,
            full_length=bool(session["full_length"]),
        )
        now = self._clock.now_utc().isoformat()
        with immediate_transaction(self._conn):
            self._conn.execute(
                "UPDATE scored_sessions SET state = 'submitted', submitted_at = ? "
                "WHERE session_id = ?",
                (now, session_id),
            )
            self._conn.execute(
                "INSERT OR IGNORE INTO scored_results (session_id, raw_correct, scored_total, "
                "percent, scaled_estimate, passed, per_domain, full_length, committed_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    session_id,
                    summary.raw_correct,
                    summary.scored_total,
                    summary.percent,
                    summary.scaled_estimate,
                    1 if summary.passed else 0,
                    json.dumps(
                        [
                            {"domain_id": b.domain_id, "correct": b.correct, "total": b.total}
                            for b in summary.per_domain
                        ]
                    ),
                    1 if summary.full_length else 0,
                    now,
                ),
            )
            for qid, objective_id, unanswered in misses:
                self._conn.execute(
                    "INSERT OR IGNORE INTO scored_misses (session_id, question_id, "
                    "objective_id, unanswered) VALUES (?, ?, ?, ?)",
                    (session_id, qid, objective_id, 1 if unanswered else 0),
                )
            self._conn.execute(
                "INSERT OR IGNORE INTO idempotency_events "
                "(caller_id, operation, payload_hash, result_json, committed_at) "
                "VALUES (?, 'scored_submit', ?, '', ?)",
                (event_id, session_id, now),
            )
        return self._load_result(session_id)

    # -- reset, history, misses ---------------------------------------------

    def reset(self, *, session_id: str) -> None:
        """Abandon an in-progress session so a fresh one can start."""
        session = self._session_row(session_id)
        current = ScoredSessionState(str(session["state"]))
        try:
            SCORED_SESSION_MACHINE.assert_transition(current, ScoredSessionState.ABANDONED)
        except IllegalTransitionError as exc:
            raise ScoredSessionError(str(exc)) from exc
        with immediate_transaction(self._conn):
            self._conn.execute(
                "UPDATE scored_sessions SET state = 'abandoned' WHERE session_id = ?",
                (session_id,),
            )

    def _clear_learner_sessions(self, learner_id: str) -> None:
        """Delete all of a learner's scored-session data (non-accumulating state).

        Called within a transaction before creating a new session so only one
        session's worth of data ever exists.
        """
        sessions = [
            str(r["session_id"])
            for r in self._conn.execute(
                "SELECT session_id FROM scored_sessions WHERE learner_id = ?",
                (learner_id,),
            ).fetchall()
        ]
        for sid in sessions:
            self._conn.execute("DELETE FROM scored_misses WHERE session_id = ?", (sid,))
            self._conn.execute("DELETE FROM scored_results WHERE session_id = ?", (sid,))
            self._conn.execute("DELETE FROM scored_answers WHERE session_id = ?", (sid,))
            self._conn.execute("DELETE FROM scored_session_items WHERE session_id = ?", (sid,))
            self._conn.execute("DELETE FROM scored_sessions WHERE session_id = ?", (sid,))

    def misses(self, *, session_id: str) -> tuple[MissedItem, ...]:
        """Return the missed items of a submitted session with teaching material."""
        rows = self._conn.execute(
            "SELECT question_id, objective_id, unanswered FROM scored_misses "
            "WHERE session_id = ? ORDER BY objective_id, question_id",
            (session_id,),
        ).fetchall()
        result: list[MissedItem] = []
        for row in rows:
            qid = str(row["question_id"])
            material = self._conn.execute(
                "SELECT correct_option_ids, explanation FROM answer_material "
                "WHERE question_id = ?",
                (qid,),
            ).fetchone()
            prompt = self._conn.execute(
                "SELECT prompt FROM questions WHERE question_id = ?", (qid,)
            ).fetchone()
            rationale_rows = self._conn.execute(
                "SELECT option_id, is_correct, rationale FROM option_rationales "
                "WHERE question_id = ? ORDER BY option_id",
                (qid,),
            ).fetchall()
            result.append(
                MissedItem(
                    question_id=qid,
                    objective_ids=tuple(self._objectives_for(qid)),
                    unanswered=bool(row["unanswered"]),
                    prompt=str(prompt["prompt"]) if prompt else "",
                    correct_option_ids=tuple(
                        json.loads(material["correct_option_ids"]) if material else []
                    ),
                    explanation=str(material["explanation"]) if material else "",
                    option_rationales=tuple(
                        OptionRationale(
                            option_id=str(r["option_id"]),
                            is_correct=bool(r["is_correct"]),
                            rationale=str(r["rationale"]),
                        )
                        for r in rationale_rows
                    ),
                )
            )
        return tuple(result)

    def latest_submitted(self, *, learner_id: str) -> str | None:
        """Return the most recently submitted session id, if any."""
        row = self._conn.execute(
            "SELECT session_id FROM scored_sessions WHERE learner_id = ? AND state = 'submitted' "
            "ORDER BY submitted_at DESC LIMIT 1",
            (learner_id,),
        ).fetchone()
        return str(row["session_id"]) if row else None

    def active_session(self, *, learner_id: str) -> str | None:
        """Return the current in-progress session id, if any."""
        row = self._conn.execute(
            "SELECT session_id FROM scored_sessions WHERE learner_id = ? AND state = 'in_progress' "
            "ORDER BY started_at DESC LIMIT 1",
            (learner_id,),
        ).fetchone()
        return str(row["session_id"]) if row else None

    # -- helpers -------------------------------------------------------------

    def _session_row(self, session_id: str) -> sqlite3.Row:
        row = self._conn.execute(
            "SELECT state, full_length FROM scored_sessions WHERE session_id = ?",
            (session_id,),
        ).fetchone()
        if row is None:
            raise NotFoundError(f"unknown scored session {session_id}")
        assert isinstance(row, sqlite3.Row)
        return row

    def _objectives_for(self, question_id: str) -> list[str]:
        rows = self._conn.execute(
            "SELECT objective_id FROM question_objectives WHERE question_id = ? "
            "ORDER BY objective_id",
            (question_id,),
        ).fetchall()
        return [str(r["objective_id"]) for r in rows]

    def _primary_objective(self, question_id: str) -> str:
        objectives = self._objectives_for(question_id)
        return objectives[0] if objectives else "unknown"

    def _correct_option_ids(self, question_id: str) -> list[str]:
        row = self._conn.execute(
            "SELECT correct_option_ids FROM answer_material WHERE question_id = ?",
            (question_id,),
        ).fetchone()
        return list(json.loads(row["correct_option_ids"])) if row else []

    def _load_result(self, session_id: str) -> ScoredResult:
        row = self._conn.execute(
            "SELECT raw_correct, scored_total, percent, scaled_estimate, passed, per_domain, "
            "full_length FROM scored_results WHERE session_id = ?",
            (session_id,),
        ).fetchone()
        if row is None:
            raise NotFoundError(f"no result for session {session_id}")
        per_domain = tuple(
            DomainResult(domain_id=d["domain_id"], correct=d["correct"], total=d["total"])
            for d in json.loads(row["per_domain"])
        )
        return ScoredResult(
            session_id=session_id,
            raw_correct=int(row["raw_correct"]),
            scored_total=int(row["scored_total"]),
            percent=float(row["percent"]),
            scaled_estimate=int(row["scaled_estimate"]),
            passed=bool(row["passed"]),
            full_length=bool(row["full_length"]),
            per_domain=per_domain,
        )
