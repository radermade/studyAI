"""Whole-exam readiness evaluation (Phase 8 go/no-go roll-up).

Layers on the per-domain :class:`~study_core.mastery.MasteryEvaluator` and the
scored-session result to produce one auditable readiness decision across all
five AIP-C01 domains. It only reads committed evidence and never mutates.

Readiness is a transparent internal study gate, not a prediction of the
official AWS exam result. Every criterion is exposed so the decision is
auditable, and per-domain scored results stay informational (the exam uses
compensatory scoring).
"""

from __future__ import annotations

from collections.abc import Sequence

from study_core.db import DbConnection
from study_core.mastery import MasteryEvaluator
from study_core.ports import Clock
from study_core.study_models import (
    DomainGateSummary,
    LabMatrixEntry,
    MasteryCriterion,
    ReadinessReport,
)

# Roadmap Phase 8 overall threshold on a fresh full-length mock.
DEFAULT_OVERALL_THRESHOLD = 0.85

_ALL_DOMAINS: tuple[int, ...] = (1, 2, 3, 4, 5)


class ReadinessEvaluator:
    """Compute the whole-exam readiness roll-up from committed evidence."""

    def __init__(
        self,
        conn: DbConnection,
        clock: Clock,
        mastery: MasteryEvaluator,
        *,
        overall_threshold: float = DEFAULT_OVERALL_THRESHOLD,
    ) -> None:
        self._conn = conn
        self._clock = clock
        self._mastery = mastery
        self._threshold = overall_threshold

    def evaluate(self, *, learner_id: str) -> ReadinessReport:
        """Return the readiness report for a learner."""
        gates = tuple(
            DomainGateSummary(
                domain_id=d,
                passed=report.passed,
                grill_accuracy=report.grill_accuracy,
            )
            for d in _ALL_DOMAINS
            for report in (self._mastery.evaluate(learner_id=learner_id, domain_id=d),)
        )
        scored_accuracy, scored_full = self._latest_scored(learner_id)
        open_mis = self._open_misconceptions(learner_id)
        lab_matrix = self._lab_matrix(learner_id)

        criteria = (
            self._gates_criterion(gates),
            self._scored_criterion(scored_accuracy, scored_full),
            self._misconception_criterion(open_mis),
            self._lab_matrix_criterion(lab_matrix),
        )
        ready = all(c.met for c in criteria if c.mandatory)

        return ReadinessReport(
            learner_id=learner_id,
            ready=ready,
            overall_threshold=self._threshold,
            scored_accuracy=scored_accuracy,
            scored_is_full_length=scored_full,
            open_misconceptions=open_mis,
            domain_gates=gates,
            lab_matrix=lab_matrix,
            criteria=criteria,
        )

    # -- criteria ------------------------------------------------------------

    def _gates_criterion(self, gates: Sequence[DomainGateSummary]) -> MasteryCriterion:
        unmet = [g.domain_id for g in gates if not g.passed]
        met = not unmet
        detail = (
            "All five domain exit gates passed."
            if met
            else f"Domain exit gate(s) not yet met: {', '.join(f'D{d}' for d in unmet)}."
        )
        return MasteryCriterion(
            key="domain_gates",
            label="All five domain exit gates passed",
            mandatory=True,
            met=met,
            detail=detail,
        )

    def _scored_criterion(self, accuracy: float | None, full_length: bool) -> MasteryCriterion:
        label = f"Full-length scored accuracy at least {self._threshold:.0%}"
        if accuracy is None:
            return MasteryCriterion(
                key="scored_overall",
                label=label,
                mandatory=True,
                met=False,
                detail="No submitted scored session yet.",
            )
        if not full_length:
            return MasteryCriterion(
                key="scored_overall",
                label=label,
                mandatory=True,
                met=False,
                detail=(
                    f"Latest scored session was not full length "
                    f"(accuracy {accuracy:.0%}); run a full 75-question mock."
                ),
            )
        met = accuracy >= self._threshold
        return MasteryCriterion(
            key="scored_overall",
            label=label,
            mandatory=True,
            met=met,
            detail=f"Latest full-length scored session: {accuracy:.0%} overall.",
        )

    def _misconception_criterion(self, open_total: int) -> MasteryCriterion:
        met = open_total == 0
        detail = (
            "No open misconceptions remain."
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

    def _lab_matrix_criterion(self, matrix: Sequence[LabMatrixEntry]) -> MasteryCriterion:
        total = len(matrix)
        done = [e for e in matrix if e.completed]
        met = total > 0 and len(done) == total
        independent = sum(1 for e in done if e.independent)
        detail = (
            f"{len(done)}/{total} labs completed "
            f"({independent} independent, {len(done) - independent} assisted)."
        )
        return MasteryCriterion(
            key="lab_matrix",
            label="Required lab matrix complete",
            mandatory=True,
            met=met,
            detail=detail,
        )

    # -- evidence reads ------------------------------------------------------

    def _latest_scored(self, learner_id: str) -> tuple[float | None, bool]:
        row = self._conn.execute(
            "SELECT r.percent, r.full_length FROM scored_results r "
            "JOIN scored_sessions s ON s.session_id = r.session_id "
            "WHERE s.learner_id = ? AND s.state = 'submitted' "
            "ORDER BY s.submitted_at DESC LIMIT 1",
            (learner_id,),
        ).fetchone()
        if row is None:
            return (None, False)
        return (float(row["percent"]), bool(row["full_length"]))

    def _open_misconceptions(self, learner_id: str) -> int:
        row = self._conn.execute(
            "SELECT COUNT(*) AS n FROM misconceptions WHERE learner_id = ? AND state = 'open'",
            (learner_id,),
        ).fetchone()
        return int(row["n"]) if row else 0

    def _lab_matrix(self, learner_id: str) -> tuple[LabMatrixEntry, ...]:
        labs = self._conn.execute(
            "SELECT lab_id, title FROM lab_definitions ORDER BY lab_id"
        ).fetchall()
        completed: dict[str, str] = {}
        for row in self._conn.execute(
            "SELECT lab_id, state FROM lab_runs "
            "WHERE learner_id = ? AND state IN ('completed_independent', 'completed_assisted')",
            (learner_id,),
        ).fetchall():
            lab_id = str(row["lab_id"])
            state = str(row["state"])
            # Prefer an independent completion over an assisted one.
            if completed.get(lab_id) != "completed_independent":
                completed[lab_id] = state
        entries: list[LabMatrixEntry] = []
        for row in labs:
            lab_id = str(row["lab_id"])
            final_state = completed.get(lab_id)
            entries.append(
                LabMatrixEntry(
                    lab_id=lab_id,
                    title=str(row["title"]),
                    completed=final_state is not None,
                    independent=final_state == "completed_independent",
                )
            )
        return tuple(entries)
