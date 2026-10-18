"""Domain mastery / exit-gate evaluation from committed study evidence.

The exit gate is a transparent internal study gate, never an AWS score
prediction. It combines three evidence sources already persisted elsewhere:

* grill attempts (per-objective accuracy and coverage) via the attempts table,
* the learner's latest scored session's per-domain result, and
* hands-on lab completion for labs mapped to the domain.

Every criterion is reported with its own pass state and reasoning so the
overall decision is auditable. Scoring is deterministic given the injected
clock; this service only reads and never mutates.
"""

from __future__ import annotations

import json
from collections.abc import Sequence

from study_core.common import domain_of
from study_core.db import DbConnection
from study_core.ports import Clock
from study_core.study_models import (
    DomainMasteryReport,
    MasteryCriterion,
    MasteryObjective,
)

# Roadmap Phase 3+ exit threshold: at least 80% accuracy on fresh scenarios.
DEFAULT_ACCURACY_THRESHOLD = 0.80


class MasteryEvaluator:
    """Compute a domain's exit-gate report from committed evidence (read-only)."""

    def __init__(
        self,
        conn: DbConnection,
        clock: Clock,
        *,
        blueprint_version: str,
        accuracy_threshold: float = DEFAULT_ACCURACY_THRESHOLD,
    ) -> None:
        self._conn = conn
        self._clock = clock
        self._blueprint_version = blueprint_version
        self._threshold = accuracy_threshold

    def evaluate(self, *, learner_id: str, domain_id: int) -> DomainMasteryReport:
        """Return the exit-gate report for one domain and learner."""
        objectives = self._domain_objectives(domain_id)
        obj_views = tuple(self._objective_view(learner_id, oid) for oid in objectives)

        # Count distinct attempts on this domain's questions (a single attempt
        # on a multi-objective question must not be double-counted per objective).
        grill_attempts, grill_correct = self._domain_grill_totals(learner_id, objectives)
        grill_accuracy = (grill_correct / grill_attempts) if grill_attempts else None

        criteria = (
            self._coverage_criterion(obj_views),
            self._accuracy_criterion(grill_accuracy, grill_attempts),
            self._misconception_criterion(obj_views),
            self._lab_criterion(learner_id, domain_id),
            self._scored_criterion(learner_id, domain_id),
        )
        passed = all(c.met for c in criteria if c.mandatory)

        return DomainMasteryReport(
            learner_id=learner_id,
            domain_id=domain_id,
            passed=passed,
            accuracy_threshold=self._threshold,
            grill_attempts=grill_attempts,
            grill_correct=grill_correct,
            grill_accuracy=grill_accuracy,
            objectives=obj_views,
            criteria=criteria,
        )

    # -- objective evidence --------------------------------------------------

    def _domain_objectives(self, domain_id: int) -> list[str]:
        rows = self._conn.execute(
            "SELECT objective_id FROM objectives WHERE blueprint_version = ? ORDER BY objective_id",
            (self._blueprint_version,),
        ).fetchall()
        objectives = [str(r["objective_id"]) for r in rows]
        return [o for o in objectives if _domain_of_safe(o) == domain_id]

    def _domain_grill_totals(self, learner_id: str, objectives: Sequence[str]) -> tuple[int, int]:
        """Return (distinct attempts, distinct correct) on the domain's questions.

        Deduplicates by attempt_id so a question tagged with two of the domain's
        objectives still counts its attempt exactly once.
        """
        if not objectives:
            return (0, 0)
        placeholders = ",".join("?" for _ in objectives)
        row = self._conn.execute(
            "SELECT COUNT(*) AS attempts, "
            "SUM(CASE WHEN outcome = 'correct' THEN 1 ELSE 0 END) AS correct FROM ("
            "  SELECT DISTINCT a.attempt_id, a.outcome FROM attempts a "
            "  JOIN question_objectives qo ON qo.question_id = a.question_id "
            f"  WHERE a.learner_id = ? AND qo.objective_id IN ({placeholders})"
            ")",
            (learner_id, *objectives),
        ).fetchone()
        attempts = int(row["attempts"]) if row else 0
        correct = int(row["correct"] or 0) if row else 0
        return (attempts, correct)

    def _objective_view(self, learner_id: str, objective_id: str) -> MasteryObjective:
        stats = self._conn.execute(
            "SELECT COUNT(*) AS attempts, "
            "SUM(CASE WHEN outcome = 'correct' THEN 1 ELSE 0 END) AS correct "
            "FROM attempts a JOIN question_objectives qo ON qo.question_id = a.question_id "
            "WHERE a.learner_id = ? AND qo.objective_id = ?",
            (learner_id, objective_id),
        ).fetchone()
        attempts = int(stats["attempts"]) if stats else 0
        correct = int(stats["correct"] or 0) if stats else 0
        open_mis = self._conn.execute(
            "SELECT COUNT(*) AS n FROM misconceptions "
            "WHERE learner_id = ? AND objective_id = ? AND state = 'open'",
            (learner_id, objective_id),
        ).fetchone()
        return MasteryObjective(
            objective_id=objective_id,
            attempts=attempts,
            correct=correct,
            accuracy=(correct / attempts) if attempts else None,
            open_misconceptions=int(open_mis["n"]) if open_mis else 0,
            covered=attempts > 0,
        )

    # -- criteria ------------------------------------------------------------

    def _coverage_criterion(self, objectives: Sequence[MasteryObjective]) -> MasteryCriterion:
        uncovered = [o.objective_id for o in objectives if not o.covered]
        met = not uncovered
        detail = (
            "Every objective has grill evidence."
            if met
            else f"No grill attempts yet for: {', '.join(uncovered)}."
        )
        return MasteryCriterion(
            key="coverage",
            label="Every domain objective practiced",
            mandatory=True,
            met=met,
            detail=detail,
        )

    def _accuracy_criterion(self, grill_accuracy: float | None, attempts: int) -> MasteryCriterion:
        if grill_accuracy is None:
            return MasteryCriterion(
                key="accuracy",
                label=f"Grill accuracy at least {self._threshold:.0%}",
                mandatory=True,
                met=False,
                detail="No grill attempts recorded yet.",
            )
        met = grill_accuracy >= self._threshold
        detail = (
            f"Grill accuracy {grill_accuracy:.0%} over {attempts} attempts "
            f"(threshold {self._threshold:.0%})."
        )
        return MasteryCriterion(
            key="accuracy",
            label=f"Grill accuracy at least {self._threshold:.0%}",
            mandatory=True,
            met=met,
            detail=detail,
        )

    def _misconception_criterion(self, objectives: Sequence[MasteryObjective]) -> MasteryCriterion:
        open_total = sum(o.open_misconceptions for o in objectives)
        met = open_total == 0
        detail = (
            "No open misconceptions in this domain."
            if met
            else f"{open_total} open misconception(s) to resolve."
        )
        return MasteryCriterion(
            key="misconceptions",
            label="No open misconceptions",
            mandatory=True,
            met=met,
            detail=detail,
        )

    def _lab_criterion(self, learner_id: str, domain_id: int) -> MasteryCriterion:
        completed = self._completed_domain_labs(learner_id, domain_id)
        total = self._domain_lab_count(domain_id)
        met = len(completed) >= 1
        if total == 0:
            return MasteryCriterion(
                key="hands_on",
                label="At least one hands-on lab completed",
                mandatory=False,
                met=True,
                detail="No labs are mapped to this domain.",
            )
        independent = sum(1 for state in completed.values() if state == "completed_independent")
        detail = (
            f"{len(completed)}/{total} domain lab(s) completed "
            f"({independent} independent, {len(completed) - independent} assisted)."
            if completed
            else f"No domain lab completed yet (of {total} available)."
        )
        return MasteryCriterion(
            key="hands_on",
            label="At least one hands-on lab completed",
            mandatory=True,
            met=met,
            detail=detail,
        )

    def _scored_criterion(self, learner_id: str, domain_id: int) -> MasteryCriterion:
        """Informational: latest scored session's accuracy for this domain."""
        session_id = self._latest_submitted_session(learner_id)
        if session_id is None:
            return MasteryCriterion(
                key="scored_session",
                label=f"Scored-session accuracy at least {self._threshold:.0%}",
                mandatory=False,
                met=False,
                detail="No submitted scored session yet.",
            )
        correct, total = self._scored_domain_result(session_id, domain_id)
        if total == 0:
            return MasteryCriterion(
                key="scored_session",
                label=f"Scored-session accuracy at least {self._threshold:.0%}",
                mandatory=False,
                met=False,
                detail="Latest scored session included no items from this domain.",
            )
        accuracy = correct / total
        met = accuracy >= self._threshold
        return MasteryCriterion(
            key="scored_session",
            label=f"Scored-session accuracy at least {self._threshold:.0%}",
            mandatory=False,
            met=met,
            detail=(
                f"Latest scored session: {correct}/{total} correct in this domain "
                f"({accuracy:.0%})."
            ),
        )

    # -- lab / scored helpers ------------------------------------------------

    def _domain_lab_ids(self, domain_id: int) -> list[str]:
        rows = self._conn.execute("SELECT lab_id, objective_ids FROM lab_definitions").fetchall()
        lab_ids: list[str] = []
        for row in rows:
            objectives = [str(o) for o in json.loads(row["objective_ids"])]
            domains = {_domain_of_safe(o) for o in objectives}
            # A lab belongs to its primary (lowest) objective domain, matching
            # the scored-session convention that each item maps to one domain.
            primary = min((d for d in domains if d is not None), default=None)
            if primary == domain_id:
                lab_ids.append(str(row["lab_id"]))
        return lab_ids

    def _domain_lab_count(self, domain_id: int) -> int:
        return len(self._domain_lab_ids(domain_id))

    def _completed_domain_labs(self, learner_id: str, domain_id: int) -> dict[str, str]:
        lab_ids = self._domain_lab_ids(domain_id)
        if not lab_ids:
            return {}
        placeholders = ",".join("?" for _ in lab_ids)
        rows = self._conn.execute(
            f"SELECT lab_id, state FROM lab_runs "
            f"WHERE learner_id = ? AND lab_id IN ({placeholders}) "
            f"AND state IN ('completed_independent', 'completed_assisted')",
            (learner_id, *lab_ids),
        ).fetchall()
        # Prefer an independent completion over an assisted one for the same lab.
        best: dict[str, str] = {}
        for row in rows:
            lab_id = str(row["lab_id"])
            state = str(row["state"])
            if best.get(lab_id) != "completed_independent":
                best[lab_id] = state
        return best

    def _latest_submitted_session(self, learner_id: str) -> str | None:
        row = self._conn.execute(
            "SELECT session_id FROM scored_sessions "
            "WHERE learner_id = ? AND state = 'submitted' "
            "ORDER BY submitted_at DESC LIMIT 1",
            (learner_id,),
        ).fetchone()
        return str(row["session_id"]) if row else None

    def _scored_domain_result(self, session_id: str, domain_id: int) -> tuple[int, int]:
        row = self._conn.execute(
            "SELECT per_domain FROM scored_results WHERE session_id = ?",
            (session_id,),
        ).fetchone()
        if row is None:
            return (0, 0)
        for bucket in json.loads(row["per_domain"]):
            if int(bucket["domain_id"]) == domain_id:
                return (int(bucket["correct"]), int(bucket["total"]))
        return (0, 0)


def _domain_of_safe(objective_id: str) -> int | None:
    """Return the domain for an objective, or None if the ID is not a task ID."""
    try:
        return domain_of(objective_id)
    except ValueError:
        return None
