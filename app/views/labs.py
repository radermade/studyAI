"""Labs view: data-driven split workspace with hint ladder and evidence states.

Lab content (steps, prediction prompts, hints, reflections, checkpoints) is
authored in ``content/labs.py`` and read back through
``UiStateService.get_lab_definition``. This view renders whichever lab the
learner selects; it holds no per-lab content of its own.
"""

from __future__ import annotations

import uuid

import streamlit as st
from study_core.bootstrap import StudyRuntime
from study_core.lab_models import CheckpointState
from study_core.lab_service import LabPreconditionError, LabValidationError
from study_core.ui_state import LabDefinitionView, LabStepView

from app.components import (
    architecture_diagram,
    empty_state,
    error_state,
    offline_notice,
    pane_layout,
    status_badge,
)
from app.theme import StatusTone

_RUN_KEY = "lab_run_id"
_LAB_KEY = "lab_selected_id"
_REVEALED_KEY = "lab_hint_revealed"  # dict: step_id -> revealed level

_STATE_TONE: dict[CheckpointState, StatusTone] = {
    CheckpointState.NOT_STARTED: StatusTone.NEUTRAL,
    CheckpointState.IN_PROGRESS: StatusTone.PROGRESS,
    CheckpointState.SELF_REPORTED: StatusTone.PROGRESS,
    CheckpointState.VERIFIED: StatusTone.SUCCESS,
    CheckpointState.FAILED: StatusTone.DANGER,
    CheckpointState.CLEANED_UP: StatusTone.SUCCESS,
}

_HINT_TITLES: tuple[str, ...] = (
    "1. Conceptual nudge",
    "2. Service/architecture area",
    "3. Procedural guidance",
    "4. Full solution (marks run assisted)",
)

_CONSOLE_URL = "https://console.aws.amazon.com/console/home"


def render(runtime: StudyRuntime, learner: str) -> None:
    """Render the lab workspace for the selected authored lab."""
    st.subheader("Labs")
    labs = [i for i in runtime.ui.list_curriculum() if i.item_type == "lab"]
    if not labs:
        empty_state("No labs are available yet.")
        return

    if runtime.labs is None:
        offline_notice()

    options = {item.item_id: item.title for item in labs}
    ids = list(options)
    selected = st.session_state.get(_LAB_KEY, ids[0])
    if selected not in options:
        selected = ids[0]
    chosen = st.selectbox(
        "Lab",
        ids,
        index=ids.index(selected),
        format_func=lambda i: options[i],
        key="lab_picker",
    )
    if chosen != st.session_state.get(_LAB_KEY):
        # Switching labs clears any in-progress run reference and hint state.
        st.session_state[_LAB_KEY] = chosen
        st.session_state.pop(_RUN_KEY, None)
        st.session_state.pop(_REVEALED_KEY, None)
        st.rerun()

    definition = runtime.ui.get_lab_definition(chosen)
    if definition is None:
        error_state("This lab's definition could not be loaded.")
        return

    st.markdown(f"**{definition.title}**")
    st.caption(f"Objectives: {', '.join(definition.objective_ids)}")

    if st.session_state.get(_RUN_KEY) is None:
        _render_start(runtime, learner, definition)
        return

    _render_workspace(runtime, definition)


def _render_start(runtime: StudyRuntime, learner: str, lab: LabDefinitionView) -> None:
    st.write(lab.scenario)
    st.caption(f"Prerequisites: {lab.prerequisites}")
    st.caption(f"Cost class: {lab.cost_class} · {lab.region_note}")
    st.write("Before starting, acknowledge cost and cleanup responsibilities.")
    cost = st.checkbox("I acknowledge potential AWS charges.", key="lab_cost")
    cleanup = st.checkbox("I will clean up all resources I create.", key="lab_cleanup")
    if st.button("Start lab", key="lab_start", disabled=not (cost and cleanup)):
        try:
            run = runtime.labs.start_lab(
                learner_id=learner,
                lab_id=lab.lab_id,
                region=lab.regions[0],
                request_id=f"startlab-{uuid.uuid4().hex}",
                acknowledged_cost=cost,
                acknowledged_cleanup=cleanup,
            )
        except LabPreconditionError as exc:
            error_state(str(exc))
            return
        st.session_state[_RUN_KEY] = run.run_id
        st.session_state[_REVEALED_KEY] = {}
        st.rerun()


def _render_workspace(runtime: StudyRuntime, lab: LabDefinitionView) -> None:
    run_id = st.session_state[_RUN_KEY]
    instructions, workspace = pane_layout("lab")

    with instructions:
        st.markdown("**Scenario**")
        st.write(lab.scenario)
        st.caption(lab.objectives_text)
        architecture_diagram(_ARCHITECTURE_MERMAID, lab.architecture)
        st.link_button("Open AWS Console (new tab)", _CONSOLE_URL)
        st.markdown("**Steps**")
        states = {cp.checkpoint_id: cp.state for cp in runtime.labs.checkpoint_states(run_id)}
        for step in lab.steps:
            _render_step(runtime, run_id, step)

    with workspace:
        st.markdown("**Evidence**")
        _render_checkpoints(runtime, lab, run_id, states)
        st.divider()
        st.markdown("**Cleanup**")
        st.write(lab.cleanup)
        st.markdown("**Delayed recall**")
        st.caption(lab.recall_prompt)


def _render_step(runtime: StudyRuntime, run_id: str, step: LabStepView) -> None:
    tag = " (required)" if step.mandatory else " (optional)"
    with st.expander(f"Step {step.display_order}{tag}", expanded=step.display_order == 1):
        st.write(step.instruction)
        st.caption(f"Predict first: {step.prediction_prompt}")
        _render_step_hints(runtime, run_id, step)
        if step.reflection:
            st.caption(f"Reflect: {step.reflection}")


def _render_step_hints(runtime: StudyRuntime, run_id: str, step: LabStepView) -> None:
    if not step.hints:
        return
    revealed_map: dict[str, int] = dict(st.session_state.get(_REVEALED_KEY, {}))
    revealed = int(revealed_map.get(step.step_id, 0))
    st.markdown("_Hints_")
    for level in range(1, revealed + 1):
        st.write(f"**{_HINT_TITLES[level - 1]}**")
        st.caption(step.hints[level - 1])
    if revealed < len(step.hints):
        next_level = revealed + 1
        warn = " This marks the run as assisted." if next_level == len(step.hints) else ""
        if st.button(f"Reveal hint {next_level}.{warn}", key=f"lab_hint_reveal_{step.step_id}"):
            runtime.labs.reveal_hint(run_id=run_id, step_id=step.step_id, level=next_level)
            revealed_map[step.step_id] = next_level
            st.session_state[_REVEALED_KEY] = revealed_map
            st.rerun()
    else:
        st.caption("All hints revealed for this step.")


def _render_checkpoints(
    runtime: StudyRuntime,
    lab: LabDefinitionView,
    run_id: str,
    states: dict[str, CheckpointState],
) -> None:
    for cp in lab.checkpoints:
        state = states.get(cp.checkpoint_id, CheckpointState.NOT_STARTED)
        kind = "cleanup" if cp.is_cleanup else ("validated" if cp.validator_id else "self-report")
        req = "required" if cp.mandatory else "optional"
        status_badge(_STATE_TONE[state], f"{cp.label} [{kind}, {req}]: {state.value}")

        if cp.validator_id is not None:
            disabled = runtime.labs is None
            if st.button(
                f"Check: {cp.label} (read-only)",
                key=f"lab_check_{cp.checkpoint_id}",
                disabled=disabled,
            ):
                try:
                    runtime.labs.check(
                        run_id=run_id,
                        checkpoint_id=cp.checkpoint_id,
                        event_id=f"check-{uuid.uuid4().hex}",
                    )
                    st.rerun()
                except LabValidationError as exc:
                    error_state(str(exc))
                except Exception:
                    error_state("AWS validation is unavailable right now.")
        else:
            if st.button(
                f"Self-report: {cp.label}",
                key=f"lab_selfreport_{cp.checkpoint_id}",
            ):
                runtime.labs.record_self_report(
                    run_id=run_id,
                    checkpoint_id=cp.checkpoint_id,
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


# Generic flow diagram; each lab's text summary carries the specific detail.
_ARCHITECTURE_MERMAID = (
    "flowchart LR\n"
    "  I[Inputs] --> P[AWS walkthrough steps]\n"
    "  P --> V[Read-only validation]\n"
    "  V --> O[Measured outcome]"
)
