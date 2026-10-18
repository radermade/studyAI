"""Labs view: split workspace, hint ladder, evidence states, Console companion."""

from __future__ import annotations

import uuid

import streamlit as st
from study_core.bootstrap import StudyRuntime
from study_core.lab_models import CheckpointState
from study_core.lab_service import LabPreconditionError, LabValidationError

from app.components import empty_state, error_state, offline_notice
from app.theme import StatusTone, status_label

_RUN_KEY = "lab_run_id"

_STATE_TONE: dict[CheckpointState, StatusTone] = {
    CheckpointState.NOT_STARTED: StatusTone.NEUTRAL,
    CheckpointState.IN_PROGRESS: StatusTone.PROGRESS,
    CheckpointState.SELF_REPORTED: StatusTone.PROGRESS,
    CheckpointState.VERIFIED: StatusTone.SUCCESS,
    CheckpointState.FAILED: StatusTone.DANGER,
    CheckpointState.CLEANED_UP: StatusTone.SUCCESS,
}

_CONSOLE_URL = "https://console.aws.amazon.com/bedrock/home"


def render(runtime: StudyRuntime, learner: str) -> None:
    """Render the lab workspace."""
    st.subheader("Labs")
    labs = [i for i in runtime.ui.list_curriculum() if i.item_type == "lab"]
    if not labs:
        empty_state("No labs are available yet.")
        return

    if runtime.labs is None:
        offline_notice()

    lab = labs[0]
    st.markdown(f"**{lab.title}**")
    st.caption(f"Objectives: {', '.join(lab.objective_ids)}")

    if st.session_state.get(_RUN_KEY) is None:
        _render_start(runtime, learner, lab.item_id)
        return

    _render_workspace(runtime)


def _render_start(runtime: StudyRuntime, learner: str, lab_id: str) -> None:
    st.write("Before starting, acknowledge cost and cleanup responsibilities.")
    cost = st.checkbox("I acknowledge potential AWS charges.", key="lab_cost")
    cleanup = st.checkbox("I will clean up all resources I create.", key="lab_cleanup")
    if st.button("Start lab", key="lab_start", disabled=not (cost and cleanup)):
        try:
            run = runtime.labs.start_lab(
                learner_id=learner,
                lab_id=lab_id,
                region="us-east-1",
                request_id=f"startlab-{uuid.uuid4().hex}",
                acknowledged_cost=cost,
                acknowledged_cleanup=cleanup,
            )
        except LabPreconditionError as exc:
            error_state(str(exc))
            return
        st.session_state[_RUN_KEY] = run.run_id
        st.rerun()


def _render_workspace(runtime: StudyRuntime) -> None:
    run_id = st.session_state[_RUN_KEY]
    instructions, workspace = st.columns([3, 2])

    with instructions:
        st.markdown("**Instructions**")
        st.write("1. Confirm model access in the AWS Console.")
        st.write("2. Invoke two models with the same prompt and record results.")
        st.link_button("Open AWS Console (new tab)", _CONSOLE_URL)
        _render_hints(runtime, run_id)

    with workspace:
        st.markdown("**Evidence**")
        _render_checkpoints(runtime, run_id)


def _render_hints(runtime: StudyRuntime, run_id: str) -> None:
    st.markdown("**Hints**")
    level = st.radio(
        "Reveal hint level",
        options=[1, 2, 3, 4],
        format_func=lambda n: {
            1: "1. Conceptual nudge",
            2: "2. Service/architecture area",
            3: "3. Procedural guidance",
            4: "4. Full solution (marks run assisted)",
        }[n],
        key="lab_hint_level",
    )
    if st.button("Reveal hint", key="lab_hint_reveal"):
        runtime.labs.reveal_hint(run_id=run_id, step_id="s2", level=int(level))
        st.info(f"Hint {level} recorded.")


def _render_checkpoints(runtime: StudyRuntime, run_id: str) -> None:
    # Checkpoint c1 is validated (read-only AWS); c2 is self-report only.
    states = {cp.checkpoint_id: cp.state for cp in runtime.labs.checkpoint_states(run_id)}
    c1 = states.get("c1-model-access", CheckpointState.NOT_STARTED)
    c2 = states.get("c2-comparison-recorded", CheckpointState.NOT_STARTED)
    st.write(status_label(_STATE_TONE[c1], f"Model access: {c1.value}"))
    st.write(status_label(_STATE_TONE[c2], f"Comparison recorded: {c2.value}"))

    if runtime.labs is not None and st.button("Check model access (read-only)", key="lab_check"):
        try:
            runtime.labs.check(
                run_id=run_id,
                checkpoint_id="c1-model-access",
                event_id=f"check-{uuid.uuid4().hex}",
            )
            st.rerun()
        except LabValidationError as exc:
            error_state(str(exc))
        except Exception:
            error_state("AWS validation is unavailable right now.")

    if st.button("Self-report comparison recorded", key="lab_selfreport"):
        runtime.labs.record_self_report(
            run_id=run_id,
            checkpoint_id="c2-comparison-recorded",
            event_id=f"sr-{uuid.uuid4().hex}",
        )
        st.rerun()

    if st.button("Complete lab", key="lab_complete"):
        try:
            result = runtime.labs.complete_lab(
                run_id=run_id, request_id=f"complete-{uuid.uuid4().hex}"
            )
            kind = "independently" if result.independent else "with hint assistance"
            st.success(f"Lab completed {kind}.")
        except LabPreconditionError as exc:
            error_state(str(exc))
