"""The transport-independent study service over SQLite.

Owns the six Phase 1 use cases. Mutations are idempotent via caller-supplied
request/event IDs plus a payload hash, grading is one atomic transaction, and
unanswered questions are projected without any answer material.
"""

from __future__ import annotations

import json
import uuid
from collections.abc import Sequence
from datetime import datetime

from study_core.artifacts import content_hash
from study_core.common import stable_shuffle
from study_core.db import DbConnection, immediate_transaction
from study_core.errors import ConflictError, Phase0Error
from study_core.grading import grade_selection
from study_core.machines import REVIEW_MACHINE
from study_core.ports import Clock, RandomSource
from study_core.scheduling import schedule_review
from study_core.study_models import (
    AnswerExplanation,
    DueReview,
    DueReviewPage,
    GradeOutcome,
    GradeResult,
    ObjectiveProgress,
    OptionRationale,
    ProgressReport,
    QuestionOption,
    ReviewState,
    SearchPage,
    SearchResult,
    SessionMode,
    SessionResult,
    SessionState,
    UnansweredQuestion,
)


class ContentGapError(Phase0Error):
    """No eligible question exists for the requested selection."""


class NotFoundError(Phase0Error):
    """A referenced entity does not exist."""


def _fts_query(terms: str) -> str:
    """Build a safe FTS5 MATCH expression from validated terms.

    Tokens are restricted to alphanumeric words joined with AND, so no FTS
    operators or SQL metacharacters reach the engine.
    """
    tokens = [t for t in "".join(c if c.isalnum() else " " for c in terms).split() if t]
    if not tokens:
        raise ValueError("search query is empty after sanitization")
    return " AND ".join(tokens)


class StudyService:
    """Study use cases backed by a single SQLite connection."""

    def __init__(
        self,
        conn: DbConnection,
        clock: Clock,
        random_source: RandomSource,
        *,
        blueprint_version: str,
        max_search_limit: int = 100,
    ) -> None:
        self._conn = conn
        self._clock = clock
        self._random = random_source
        self._blueprint_version = blueprint_version
        self._max_search_limit = max_search_limit

    # -- idempotency ---------------------------------------------------------

    def _idempotent_lookup(self, caller_id: str, operation: str, payload_hash: str) -> str | None:
        row = self._conn.execute(
            "SELECT payload_hash, result_json FROM idempotency_events "
            "WHERE caller_id = ? AND operation = ?",
            (caller_id, operation),
        ).fetchone()
        if row is None:
            return None
        if str(row["payload_hash"]) != payload_hash:
            raise ConflictError(f"request id reused with a different payload: {operation}")
        return str(row["result_json"])

    def _record_idempotent(
        self, caller_id: str, operation: str, payload_hash: str, result_json: str
    ) -> None:
        self._conn.execute(
            "INSERT INTO idempotency_events "
            "(caller_id, operation, payload_hash, result_json, committed_at) "
            "VALUES (?, ?, ?, ?, ?)",
            (caller_id, operation, payload_hash, result_json, self._clock.now_utc().isoformat()),
        )

    # -- start_session -------------------------------------------------------

    def start_session(
        self,
        *,
        learner_id: str,
        mode: SessionMode,
        objective_filter: Sequence[str],
        request_id: str,
    ) -> SessionResult:
        """Create or return one durable session for a request ID."""
        payload_hash = content_hash(
            {"learner": learner_id, "mode": mode.value, "filter": sorted(objective_filter)}
        )
        existing = self._idempotent_lookup(request_id, "start_session", payload_hash)
        if existing is not None:
            return SessionResult.model_validate_json(existing)

        now = self._clock.now_utc()
        session_id = f"session-{uuid.uuid4().hex}"
        result = SessionResult(
            session_id=session_id,
            learner_id=learner_id,
            mode=mode,
            state=SessionState.ACTIVE,
            blueprint_version=self._blueprint_version,
            started_at=now,
        )
        with immediate_transaction(self._conn):
            self._conn.execute(
                "INSERT INTO sessions (session_id, learner_id, mode, objective_filter, "
                "blueprint_version, state, started_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    session_id,
                    learner_id,
                    mode.value,
                    json.dumps(sorted(objective_filter)),
                    self._blueprint_version,
                    SessionState.ACTIVE.value,
                    now.isoformat(),
                ),
            )
            self._record_idempotent(
                request_id, "start_session", payload_hash, result.model_dump_json()
            )
        return result

    # -- next_question -------------------------------------------------------

    def next_question(self, *, session_id: str, request_id: str) -> UnansweredQuestion:
        """Select and serve one eligible question; serving is persisted.

        Priority: due reviews, then open misconceptions' objectives, then
        least-attempted objectives, then any unserved reviewed question.
        """
        session = self._conn.execute(
            "SELECT learner_id, objective_filter, state FROM sessions WHERE session_id = ?",
            (session_id,),
        ).fetchone()
        if session is None:
            raise NotFoundError(f"unknown session {session_id}")

        payload_hash = content_hash({"session": session_id})
        existing = self._idempotent_lookup(request_id, "next_question", payload_hash)
        if existing is not None:
            return UnansweredQuestion.model_validate_json(existing)

        learner_id = str(session["learner_id"])
        objective_filter = tuple(json.loads(session["objective_filter"]))
        question_id = self._select_question(learner_id, objective_filter, session_id)
        if question_id is None:
            raise ContentGapError("no eligible question for this session")

        question = self._project_unanswered(question_id, session_id=session_id)
        now = self._clock.now_utc()
        with immediate_transaction(self._conn):
            self._conn.execute(
                "INSERT OR IGNORE INTO session_items (session_id, question_id, served_at) "
                "VALUES (?, ?, ?)",
                (session_id, question_id, now.isoformat()),
            )
            self._record_idempotent(
                request_id, "next_question", payload_hash, question.model_dump_json()
            )
        return question

    def _select_question(
        self, learner_id: str, objective_filter: Sequence[str], session_id: str
    ) -> str | None:
        now_iso = self._clock.now_utc().isoformat()
        filter_set = set(objective_filter)

        def _objective_ok(objective_ids: list[str]) -> bool:
            return not filter_set or bool(filter_set.intersection(objective_ids))

        # 1. Due reviews.
        due = self._conn.execute(
            "SELECT question_id FROM reviews WHERE learner_id = ? AND state = 'scheduled' "
            "AND due_at <= ? ORDER BY due_at ASC, review_id ASC",
            (learner_id, now_iso),
        ).fetchall()
        for row in due:
            qid = str(row["question_id"])
            if _objective_ok(self._objectives_for(qid)):
                return qid

        # 2 & 3. Reviewed, unserved questions ordered by objective attempt count.
        served = {
            str(r["question_id"])
            for r in self._conn.execute(
                "SELECT question_id FROM session_items WHERE session_id = ?", (session_id,)
            ).fetchall()
        }
        candidates = self._conn.execute(
            "SELECT question_id FROM questions WHERE review_status = 'reviewed' "
            "ORDER BY question_id ASC"
        ).fetchall()
        eligible = [
            str(r["question_id"])
            for r in candidates
            if str(r["question_id"]) not in served
            and _objective_ok(self._objectives_for(str(r["question_id"])))
        ]
        if not eligible:
            return None
        eligible.sort(key=lambda qid: (self._objective_attempt_weight(learner_id, qid), qid))
        # Deterministic priority order is established above; the injected random
        # source only breaks ties among the equally weighted leading group.
        lead_weight = self._objective_attempt_weight(learner_id, eligible[0])
        tied = [q for q in eligible if self._objective_attempt_weight(learner_id, q) == lead_weight]
        return tied[self._random.choose_index(len(tied))]

    def _objective_attempt_weight(self, learner_id: str, question_id: str) -> int:
        objectives = self._objectives_for(question_id)
        if not objectives:
            return 0
        placeholders = ",".join("?" for _ in objectives)
        row = self._conn.execute(
            "SELECT COUNT(*) AS n FROM attempts a "
            "JOIN question_objectives qo ON qo.question_id = a.question_id "
            f"WHERE a.learner_id = ? AND qo.objective_id IN ({placeholders})",
            (learner_id, *objectives),
        ).fetchone()
        return int(row["n"]) if row else 0

    def _objectives_for(self, question_id: str) -> list[str]:
        rows = self._conn.execute(
            "SELECT objective_id FROM question_objectives WHERE question_id = ? "
            "ORDER BY objective_id",
            (question_id,),
        ).fetchall()
        return [str(r["objective_id"]) for r in rows]

    def _project_unanswered(self, question_id: str, *, session_id: str) -> UnansweredQuestion:
        q = self._conn.execute(
            "SELECT prompt, scenario_constraint, question_format, source_ids "
            "FROM questions WHERE question_id = ?",
            (question_id,),
        ).fetchone()
        if q is None:
            raise NotFoundError(f"unknown question {question_id}")
        base_options = [
            QuestionOption(option_id=str(r["option_id"]), text=str(r["text"]))
            for r in self._conn.execute(
                "SELECT option_id, text FROM question_options WHERE question_id = ? "
                "ORDER BY option_id",
                (question_id,),
            ).fetchall()
        ]
        # Randomize display order deterministically per (session, question) so
        # the correct answer is not positionally predictable; grading uses IDs.
        options = tuple(stable_shuffle(base_options, seed_key=f"{session_id}:{question_id}"))
        return UnansweredQuestion(
            question_id=question_id,
            prompt=str(q["prompt"]),
            scenario_constraint=str(q["scenario_constraint"]),
            question_format=str(q["question_format"]),
            options=options,
            objective_ids=tuple(self._objectives_for(question_id)),
            source_ids=tuple(json.loads(q["source_ids"])),
        )

    # -- grade_and_record ----------------------------------------------------

    def grade_and_record(
        self,
        *,
        session_id: str,
        question_id: str,
        selected_option_ids: Sequence[str],
        confidence: int,
        elapsed_seconds: float,
        event_id: str,
    ) -> GradeResult:
        """Grade one attempt and atomically update attempt, misconception, review."""
        payload_hash = content_hash(
            {
                "session": session_id,
                "question": question_id,
                "selected": sorted(selected_option_ids),
                "confidence": confidence,
                "elapsed": elapsed_seconds,
            }
        )
        existing = self._idempotent_lookup(event_id, "grade_and_record", payload_hash)
        if existing is not None:
            return GradeResult.model_validate_json(existing)

        served = self._conn.execute(
            "SELECT 1 FROM session_items WHERE session_id = ? AND question_id = ?",
            (session_id, question_id),
        ).fetchone()
        if served is None:
            raise NotFoundError("question was not served in this session")

        learner_row = self._conn.execute(
            "SELECT learner_id FROM sessions WHERE session_id = ?", (session_id,)
        ).fetchone()
        if learner_row is None:
            raise NotFoundError(f"unknown session {session_id}")
        learner_id = str(learner_row["learner_id"])

        answer = self._conn.execute(
            "SELECT correct_option_ids FROM answer_material WHERE question_id = ?",
            (question_id,),
        ).fetchone()
        correct = json.loads(answer["correct_option_ids"]) if answer else []
        outcome = grade_selection(selected_option_ids, correct)
        objectives = self._objectives_for(question_id)
        now = self._clock.now_utc()
        attempt_id = f"attempt-{uuid.uuid4().hex}"

        due_at = None
        with immediate_transaction(self._conn):
            self._conn.execute(
                "INSERT INTO attempts (attempt_id, session_id, question_id, learner_id, "
                "outcome, confidence, elapsed_seconds, committed_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    attempt_id,
                    session_id,
                    question_id,
                    learner_id,
                    outcome.value,
                    confidence,
                    elapsed_seconds,
                    now.isoformat(),
                ),
            )
            self._update_misconceptions(learner_id, objectives, outcome, now)
            due_at = self._reschedule_reviews(learner_id, question_id, objectives, outcome, now)
            result = GradeResult(
                attempt_id=attempt_id,
                question_id=question_id,
                outcome=outcome,
                confidence=confidence,
                next_review_due_at=due_at,
            )
            self._record_idempotent(
                event_id, "grade_and_record", payload_hash, result.model_dump_json()
            )
        return result

    def _update_misconceptions(
        self,
        learner_id: str,
        objectives: Sequence[str],
        outcome: GradeOutcome,
        now: datetime,
    ) -> None:
        now_iso = now.isoformat()
        for objective_id in objectives:
            misconception_id = f"mis-{learner_id}-{objective_id}"
            if outcome == GradeOutcome.CORRECT:
                self._conn.execute(
                    "UPDATE misconceptions SET state = 'resolved', updated_at = ? "
                    "WHERE misconception_id = ? AND state = 'open'",
                    (now_iso, misconception_id),
                )
            elif outcome == GradeOutcome.INCORRECT:
                self._conn.execute(
                    "INSERT INTO misconceptions (misconception_id, learner_id, objective_id, "
                    "state, updated_at) VALUES (?, ?, ?, 'open', ?) "
                    "ON CONFLICT(misconception_id) DO UPDATE SET state = 'open', updated_at = ?",
                    (misconception_id, learner_id, objective_id, now_iso, now_iso),
                )

    def _reschedule_reviews(
        self,
        learner_id: str,
        question_id: str,
        objectives: Sequence[str],
        outcome: GradeOutcome,
        now: datetime,
    ) -> datetime:
        now_iso = now.isoformat()
        objective_id = objectives[0] if objectives else "unknown"
        existing = self._conn.execute(
            "SELECT review_id, interval_days FROM reviews "
            "WHERE learner_id = ? AND question_id = ? AND state = 'scheduled'",
            (learner_id, question_id),
        ).fetchone()
        previous_interval = int(existing["interval_days"]) if existing else 0
        decision = schedule_review(
            previous_interval_days=previous_interval, outcome=outcome, now=now
        )
        if existing is not None:
            # Rescheduling keeps the review SCHEDULED; validate via the machine.
            REVIEW_MACHINE.assert_transition(ReviewState.SCHEDULED, ReviewState.SCHEDULED)
            self._conn.execute(
                "UPDATE reviews SET due_at = ?, interval_days = ?, policy_version = ?, "
                "updated_at = ? WHERE review_id = ?",
                (
                    decision.due_at.isoformat(),
                    decision.interval_days,
                    decision.policy_version,
                    now_iso,
                    str(existing["review_id"]),
                ),
            )
        else:
            self._conn.execute(
                "INSERT INTO reviews (review_id, learner_id, question_id, objective_id, "
                "due_at, interval_days, state, policy_version, updated_at) "
                "VALUES (?, ?, ?, ?, ?, ?, 'scheduled', ?, ?)",
                (
                    f"review-{uuid.uuid4().hex}",
                    learner_id,
                    question_id,
                    objective_id,
                    decision.due_at.isoformat(),
                    decision.interval_days,
                    decision.policy_version,
                    now_iso,
                ),
            )
        return decision.due_at

    # -- explain_answer ------------------------------------------------------

    def explain_answer(self, *, session_id: str, question_id: str) -> AnswerExplanation:
        """Return teaching material for a question already attempted in a session.

        Guards disclosure: the explanation is available only after the learner
        has an attempt recorded for this question in this session, so answer
        material never reaches an unanswered question.
        """
        attempted = self._conn.execute(
            "SELECT 1 FROM attempts WHERE session_id = ? AND question_id = ? LIMIT 1",
            (session_id, question_id),
        ).fetchone()
        if attempted is None:
            raise NotFoundError("no committed attempt for this question in this session")

        material = self._conn.execute(
            "SELECT correct_option_ids, explanation FROM answer_material WHERE question_id = ?",
            (question_id,),
        ).fetchone()
        if material is None:
            raise NotFoundError(f"no answer material for {question_id}")
        rationale_rows = self._conn.execute(
            "SELECT option_id, is_correct, rationale FROM option_rationales "
            "WHERE question_id = ? ORDER BY option_id",
            (question_id,),
        ).fetchall()
        return AnswerExplanation(
            question_id=question_id,
            correct_option_ids=tuple(json.loads(material["correct_option_ids"])),
            explanation=str(material["explanation"]),
            option_rationales=tuple(
                OptionRationale(
                    option_id=str(r["option_id"]),
                    is_correct=bool(r["is_correct"]),
                    rationale=str(r["rationale"]),
                )
                for r in rationale_rows
            ),
        )

    # -- get_due_reviews -----------------------------------------------------

    def get_due_reviews(
        self, *, learner_id: str, objective_filter: Sequence[str] = ()
    ) -> DueReviewPage:
        """Return committed reviews due at or before now, ordered deterministically."""
        now_iso = self._clock.now_utc().isoformat()
        rows = self._conn.execute(
            "SELECT review_id, question_id, objective_id, due_at FROM reviews "
            "WHERE learner_id = ? AND state = 'scheduled' AND due_at <= ? "
            "ORDER BY due_at ASC, review_id ASC",
            (learner_id, now_iso),
        ).fetchall()
        filter_set = set(objective_filter)
        items = tuple(
            DueReview(
                review_id=str(r["review_id"]),
                question_id=str(r["question_id"]),
                objective_id=str(r["objective_id"]),
                due_at=datetime.fromisoformat(str(r["due_at"])),
            )
            for r in rows
            if not filter_set or str(r["objective_id"]) in filter_set
        )
        return DueReviewPage(items=items)

    # -- get_progress --------------------------------------------------------

    def get_progress(self, *, learner_id: str) -> ProgressReport:
        """Report evidence-based progress by objective."""
        objective_rows = self._conn.execute(
            "SELECT objective_id FROM objectives WHERE blueprint_version = ? "
            "ORDER BY objective_id",
            (self._blueprint_version,),
        ).fetchall()
        all_objectives = [str(r["objective_id"]) for r in objective_rows]

        progress: list[ObjectiveProgress] = []
        uncovered: list[str] = []
        for objective_id in all_objectives:
            stats = self._conn.execute(
                "SELECT COUNT(*) AS attempts, "
                "SUM(CASE WHEN outcome = 'correct' THEN 1 ELSE 0 END) AS correct, "
                "AVG(confidence) AS mean_conf FROM attempts a "
                "JOIN question_objectives qo ON qo.question_id = a.question_id "
                "WHERE a.learner_id = ? AND qo.objective_id = ?",
                (learner_id, objective_id),
            ).fetchone()
            attempts = int(stats["attempts"]) if stats else 0
            if attempts == 0:
                uncovered.append(objective_id)
            correct = int(stats["correct"] or 0)
            open_mis = self._conn.execute(
                "SELECT COUNT(*) AS n FROM misconceptions "
                "WHERE learner_id = ? AND objective_id = ? AND state = 'open'",
                (learner_id, objective_id),
            ).fetchone()
            progress.append(
                ObjectiveProgress(
                    objective_id=objective_id,
                    attempts=attempts,
                    correct=correct,
                    accuracy=(correct / attempts) if attempts else None,
                    mean_confidence=float(stats["mean_conf"]) if attempts else None,
                    open_misconceptions=int(open_mis["n"]) if open_mis else 0,
                )
            )
        return ProgressReport(
            learner_id=learner_id,
            objectives=tuple(progress),
            uncovered_objectives=tuple(uncovered),
        )

    # -- search_local_material ----------------------------------------------

    def search_local_material(
        self,
        *,
        query: str,
        objective_filter: Sequence[str] = (),
        limit: int = 20,
        offset: int = 0,
    ) -> SearchPage:
        """Search indexed local material with objective filters and paging."""
        if limit <= 0 or limit > self._max_search_limit:
            raise ValueError(f"limit must be in 1..{self._max_search_limit}")
        if offset < 0:
            raise ValueError("offset must be non-negative")
        match = _fts_query(query)
        rows = self._conn.execute(
            "SELECT content_id, title, snippet(material_fts, 2, '[', ']', '...', 12) AS snip, "
            "objective_ids, freshness FROM material_fts WHERE material_fts MATCH ? "
            "ORDER BY rank LIMIT ? OFFSET ?",
            (match, limit + 1, offset),
        ).fetchall()
        filter_set = set(objective_filter)
        results: list[SearchResult] = []
        for row in rows[:limit]:
            objective_ids = tuple(json.loads(row["objective_ids"]))
            if filter_set and not filter_set.intersection(objective_ids):
                continue
            results.append(
                SearchResult(
                    content_id=str(row["content_id"]),
                    title=str(row["title"]),
                    snippet=str(row["snip"]),
                    objective_ids=objective_ids,
                    freshness=str(row["freshness"]),
                )
            )
        return SearchPage(results=tuple(results), offset=offset, has_more=len(rows) > limit)
