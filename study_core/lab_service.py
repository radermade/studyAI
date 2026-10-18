"""Lab lifecycle service: start, checkpoint, validation, hints, completion.

Verification uses a two-stage flow so a SQLite transaction is never held open
across an AWS call: commit a validation attempt, call the read-only validator
outside any transaction, then commit the evidence and legal state transition.
"""

from __future__ import annotations

import json
import uuid
from collections.abc import Sequence

from study_core.artifacts import content_hash
from study_core.db import DbConnection, immediate_transaction
from study_core.errors import ConflictError, Phase0Error
from study_core.lab_models import (
    CheckpointState,
    CheckpointView,
    EvidenceKind,
    LabCompletionView,
    LabRunState,
    LabRunView,
    ReadOnlyValidator,
    ValidationRequest,
    evidence_establishes_cleanup,
    evidence_establishes_verified,
)
from study_core.machines import CHECKPOINT_MACHINE, LAB_RUN_MACHINE
from study_core.ports import Clock
from study_core.service import NotFoundError
from study_core.state_machine import IllegalTransitionError

MAX_HINT_LEVEL = 4


class LabPreconditionError(Phase0Error):
    """A lab cannot start because a safety or prerequisite gate failed."""


class LabValidationError(Phase0Error):
    """A requested checkpoint transition is illegal for the given evidence."""


class LabService:
    """Lab lifecycle operations backed by one SQLite connection."""

    def __init__(
        self,
        conn: DbConnection,
        clock: Clock,
        validator: ReadOnlyValidator | None = None,
    ) -> None:
        self._conn = conn
        self._clock = clock
        self._validator = validator

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

    # -- start_lab -----------------------------------------------------------

    def start_lab(
        self,
        *,
        learner_id: str,
        lab_id: str,
        region: str,
        request_id: str,
        acknowledged_cost: bool,
        acknowledged_cleanup: bool,
    ) -> LabRunView:
        """Create or return one durable lab run after safety gates pass."""
        payload_hash = content_hash({"learner": learner_id, "lab": lab_id, "region": region})
        existing = self._idempotent_lookup(request_id, "start_lab", payload_hash)
        if existing is not None:
            return LabRunView.model_validate_json(existing)

        definition = self._conn.execute(
            "SELECT regions FROM lab_definitions WHERE lab_id = ?", (lab_id,)
        ).fetchone()
        if definition is None:
            raise NotFoundError(f"unknown lab {lab_id}")
        allowed_regions = json.loads(definition["regions"])
        if region not in allowed_regions:
            raise LabPreconditionError(f"region {region} not in lab allowlist")
        if not acknowledged_cost or not acknowledged_cleanup:
            raise LabPreconditionError("cost and cleanup must be acknowledged before start")

        now = self._clock.now_utc()
        run_id = f"lab-{uuid.uuid4().hex}"
        view = LabRunView(
            run_id=run_id,
            lab_id=lab_id,
            learner_id=learner_id,
            region=region,
            state=LabRunState.ACTIVE,
            active_step=None,
            full_solution_used=False,
        )
        with immediate_transaction(self._conn):
            self._conn.execute(
                "INSERT INTO lab_runs (run_id, learner_id, lab_id, region, state, active_step, "
                "full_solution_used, started_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, 0, ?, ?)",
                (
                    run_id,
                    learner_id,
                    lab_id,
                    region,
                    LabRunState.ACTIVE.value,
                    None,
                    now.isoformat(),
                    now.isoformat(),
                ),
            )
            self._record_idempotent(request_id, "start_lab", payload_hash, view.model_dump_json())
        return view

    # -- checkpoint transitions ---------------------------------------------

    def record_self_report(
        self, *, run_id: str, checkpoint_id: str, event_id: str
    ) -> CheckpointView:
        """Record a self-reported checkpoint (never Verified or Cleaned up)."""
        return self._transition(
            run_id=run_id,
            checkpoint_id=checkpoint_id,
            target=CheckpointState.SELF_REPORTED,
            event_id=event_id,
            evidence_id=None,
        )

    def check(self, *, run_id: str, checkpoint_id: str, event_id: str) -> CheckpointView:
        """Run the checkpoint's read-only validator and transition on evidence.

        Two-stage: commit the attempt, call the validator outside any
        transaction, then commit evidence and the resulting legal transition.
        """
        payload_hash = content_hash({"run": run_id, "checkpoint": checkpoint_id})
        existing = self._idempotent_lookup(event_id, "check", payload_hash)
        if existing is not None:
            return CheckpointView.model_validate_json(existing)

        run = self._conn.execute(
            "SELECT lab_id, region FROM lab_runs WHERE run_id = ?", (run_id,)
        ).fetchone()
        if run is None:
            raise NotFoundError(f"unknown lab run {run_id}")
        checkpoint = self._conn.execute(
            "SELECT validator_id, is_cleanup FROM lab_checkpoints "
            "WHERE lab_id = ? AND checkpoint_id = ?",
            (str(run["lab_id"]), checkpoint_id),
        ).fetchone()
        if checkpoint is None:
            raise NotFoundError(f"unknown checkpoint {checkpoint_id}")
        validator_id = checkpoint["validator_id"]
        is_cleanup = bool(checkpoint["is_cleanup"])
        if validator_id is None or self._validator is None:
            raise LabValidationError("checkpoint has no validator; use self-report")

        # Stage 1: commit the attempt.
        attempt_id = f"vatt-{uuid.uuid4().hex}"
        now = self._clock.now_utc()
        with immediate_transaction(self._conn):
            self._conn.execute(
                "INSERT INTO validation_attempts (attempt_id, run_id, checkpoint_id, "
                "validator_id, region, outcome, started_at, completed_at) "
                "VALUES (?, ?, ?, ?, ?, NULL, ?, NULL)",
                (
                    attempt_id,
                    run_id,
                    checkpoint_id,
                    str(validator_id),
                    str(run["region"]),
                    now.isoformat(),
                ),
            )

        # Stage 2: call the validator OUTSIDE any transaction.
        request = ValidationRequest(validator_id=str(validator_id), region=str(run["region"]))
        evidence = self._validator.validate(request)

        # Stage 3: commit evidence and the legal transition.
        target = self._target_for_evidence(evidence.kind, is_cleanup)
        completed = self._clock.now_utc()
        evidence_id = f"vev-{uuid.uuid4().hex}"
        with immediate_transaction(self._conn):
            self._conn.execute(
                "UPDATE validation_attempts SET outcome = ?, completed_at = ? "
                "WHERE attempt_id = ?",
                (evidence.kind.value, completed.isoformat(), attempt_id),
            )
            self._conn.execute(
                "INSERT INTO validation_evidence (evidence_id, attempt_id, kind, summary, "
                "observed_at) VALUES (?, ?, ?, ?, ?)",
                (
                    evidence_id,
                    attempt_id,
                    evidence.kind.value,
                    evidence.summary,
                    completed.isoformat(),
                ),
            )
            view = self._write_state(
                run_id,
                checkpoint_id,
                target,
                completed.isoformat(),
                evidence_kind=evidence.kind,
            )
            self._record_idempotent(event_id, "check", payload_hash, view.model_dump_json())
        return view

    @staticmethod
    def _target_for_evidence(kind: EvidenceKind, is_cleanup: bool) -> CheckpointState:
        if is_cleanup:
            if evidence_establishes_cleanup(kind):
                return CheckpointState.CLEANED_UP
            return CheckpointState.FAILED
        if evidence_establishes_verified(kind):
            return CheckpointState.VERIFIED
        return CheckpointState.FAILED

    def _transition(
        self,
        *,
        run_id: str,
        checkpoint_id: str,
        target: CheckpointState,
        event_id: str,
        evidence_id: str | None,
    ) -> CheckpointView:
        payload_hash = content_hash(
            {"run": run_id, "checkpoint": checkpoint_id, "target": target.value}
        )
        existing = self._idempotent_lookup(event_id, "transition", payload_hash)
        if existing is not None:
            return CheckpointView.model_validate_json(existing)
        # No evidence_kind is passed here, so the machine's evidence guards block
        # a self-report path from reaching VERIFIED or CLEANED_UP.
        now = self._clock.now_utc().isoformat()
        with immediate_transaction(self._conn):
            self._conn.execute(
                "INSERT INTO checkpoint_events (event_id, run_id, checkpoint_id, "
                "requested_state, evidence_id, committed_at) VALUES (?, ?, ?, ?, ?, ?)",
                (event_id, run_id, checkpoint_id, target.value, evidence_id, now),
            )
            view = self._write_state(run_id, checkpoint_id, target, now)
            self._record_idempotent(event_id, "transition", payload_hash, view.model_dump_json())
        return view

    def _current_checkpoint_state(self, run_id: str, checkpoint_id: str) -> CheckpointState:
        row = self._conn.execute(
            "SELECT state FROM checkpoint_state WHERE run_id = ? AND checkpoint_id = ?",
            (run_id, checkpoint_id),
        ).fetchone()
        return CheckpointState(str(row["state"])) if row else CheckpointState.NOT_STARTED

    def _write_state(
        self,
        run_id: str,
        checkpoint_id: str,
        state: CheckpointState,
        now_iso: str,
        *,
        evidence_kind: EvidenceKind | None = None,
    ) -> CheckpointView:
        # Enforce legality through the declared checkpoint state machine. The
        # machine is the single authority on which transitions (and evidence)
        # are allowed; a NOT_STARTED->IN_PROGRESS bootstrap is implicit.
        current = self._current_checkpoint_state(run_id, checkpoint_id)
        if current != state:
            if current == CheckpointState.NOT_STARTED and state != CheckpointState.IN_PROGRESS:
                # Bootstrap through IN_PROGRESS so entry transitions are explicit.
                CHECKPOINT_MACHINE.assert_transition(
                    CheckpointState.NOT_STARTED, CheckpointState.IN_PROGRESS
                )
                current = CheckpointState.IN_PROGRESS
            try:
                CHECKPOINT_MACHINE.assert_transition(current, state, evidence_kind=evidence_kind)
            except IllegalTransitionError as exc:
                raise LabValidationError(str(exc)) from exc
        self._conn.execute(
            "INSERT INTO checkpoint_state (run_id, checkpoint_id, state, updated_at) "
            "VALUES (?, ?, ?, ?) ON CONFLICT(run_id, checkpoint_id) "
            "DO UPDATE SET state = ?, updated_at = ?",
            (run_id, checkpoint_id, state.value, now_iso, state.value, now_iso),
        )
        return CheckpointView(run_id=run_id, checkpoint_id=checkpoint_id, state=state)

    # -- hints ---------------------------------------------------------------

    def reveal_hint(self, *, run_id: str, step_id: str, level: int) -> int:
        """Record a hint reveal (committed before the caller shows content).

        Levels are 1..4 and monotonic per run/step. Level 4 marks the run
        as assisted. Returns the committed level.
        """
        if level < 1 or level > MAX_HINT_LEVEL:
            raise ValueError("hint level must be 1..4")
        now = self._clock.now_utc().isoformat()
        with immediate_transaction(self._conn):
            self._conn.execute(
                "INSERT INTO hint_events (event_id, run_id, step_id, level, revealed_at) "
                "VALUES (?, ?, ?, ?, ?)",
                (f"hint-{uuid.uuid4().hex}", run_id, step_id, level, now),
            )
            if level == MAX_HINT_LEVEL:
                self._conn.execute(
                    "UPDATE lab_runs SET full_solution_used = 1, updated_at = ? WHERE run_id = ?",
                    (now, run_id),
                )
        return level

    # -- complete_lab --------------------------------------------------------

    def complete_lab(self, *, run_id: str, request_id: str) -> LabCompletionView:
        """Complete a lab only when mandatory checkpoints and cleanup are satisfied."""
        payload_hash = content_hash({"run": run_id})
        existing = self._idempotent_lookup(request_id, "complete_lab", payload_hash)
        if existing is not None:
            return LabCompletionView.model_validate_json(existing)

        run = self._conn.execute(
            "SELECT lab_id, full_solution_used, state FROM lab_runs WHERE run_id = ?", (run_id,)
        ).fetchone()
        if run is None:
            raise NotFoundError(f"unknown lab run {run_id}")
        lab_id = str(run["lab_id"])
        assisted = bool(run["full_solution_used"])
        current = LabRunState(str(run["state"]))

        unmet = self._unmet_mandatory_checkpoints(run_id, lab_id)
        if unmet:
            raise LabPreconditionError(f"mandatory checkpoints not satisfied: {', '.join(unmet)}")

        final = LabRunState.COMPLETED_ASSISTED if assisted else LabRunState.COMPLETED_INDEPENDENT
        # Validate the lifecycle transition through the declared machine.
        try:
            LAB_RUN_MACHINE.assert_transition(current, final)
        except IllegalTransitionError as exc:
            raise LabPreconditionError(str(exc)) from exc
        view = LabCompletionView(run_id=run_id, state=final, independent=not assisted)
        now = self._clock.now_utc().isoformat()
        with immediate_transaction(self._conn):
            self._conn.execute(
                "UPDATE lab_runs SET state = ?, updated_at = ? WHERE run_id = ?",
                (final.value, now, run_id),
            )
            self._record_idempotent(
                request_id, "complete_lab", payload_hash, view.model_dump_json()
            )
        return view

    def _unmet_mandatory_checkpoints(self, run_id: str, lab_id: str) -> list[str]:
        mandatory = self._conn.execute(
            "SELECT checkpoint_id, is_cleanup FROM lab_checkpoints "
            "WHERE lab_id = ? AND mandatory = 1 ORDER BY checkpoint_id",
            (lab_id,),
        ).fetchall()
        states = {
            str(r["checkpoint_id"]): str(r["state"])
            for r in self._conn.execute(
                "SELECT checkpoint_id, state FROM checkpoint_state WHERE run_id = ?", (run_id,)
            ).fetchall()
        }
        unmet: list[str] = []
        for row in mandatory:
            cid = str(row["checkpoint_id"])
            needed = (
                CheckpointState.CLEANED_UP.value
                if bool(row["is_cleanup"])
                else CheckpointState.VERIFIED.value
            )
            if states.get(cid) != needed:
                unmet.append(cid)
        return unmet

    # -- queries -------------------------------------------------------------

    def checkpoint_states(self, run_id: str) -> Sequence[CheckpointView]:
        """Return current checkpoint states for a run."""
        rows = self._conn.execute(
            "SELECT checkpoint_id, state FROM checkpoint_state WHERE run_id = ? "
            "ORDER BY checkpoint_id",
            (run_id,),
        ).fetchall()
        return tuple(
            CheckpointView(
                run_id=run_id,
                checkpoint_id=str(r["checkpoint_id"]),
                state=CheckpointState(str(r["state"])),
            )
            for r in rows
        )
