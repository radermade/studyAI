"""Shared, reusable UI components used across views."""

from __future__ import annotations

import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from study_core.ui_state import ContentStatus, CurriculumItem, UiStateService

from app.theme import (
    DEFAULT_PANE_PRESET,
    PANE_PRESETS,
    StatusTone,
    status_badge_html,
    status_label,
)

_STATUS_TONE: dict[ContentStatus, StatusTone] = {
    ContentStatus.NOT_STARTED: StatusTone.NEUTRAL,
    ContentStatus.IN_PROGRESS: StatusTone.PROGRESS,
    ContentStatus.COMPLETE: StatusTone.SUCCESS,
}


def status_badge(tone: StatusTone, text: str) -> None:
    """Render an accessible status badge (color + icon + word + text)."""
    st.markdown(status_badge_html(tone, text), unsafe_allow_html=True)


def curriculum_rail(ui: UiStateService, learner: str, *, due_count: int) -> None:
    """Render the collapsible curriculum rail with status and due-review badge."""
    with st.sidebar:
        st.caption(f"Due reviews: {due_count}")
        statuses = ui.content_status(learner)
        completed = {k for k, v in statuses.items() if v == ContentStatus.COMPLETE}
        for item in ui.list_curriculum():
            status = statuses.get(item.item_id, ContentStatus.NOT_STARTED)
            missing = _missing_prerequisites(item, completed)
            if missing:
                tone = StatusTone.WARNING
                label = f"{item.title} (locked)"
            else:
                tone = _STATUS_TONE[status]
                label = item.title
            status_badge(tone, label)
            if missing:
                st.caption(f"Requires: {', '.join(missing)}")


def _missing_prerequisites(item: CurriculumItem, completed: set[str]) -> list[str]:
    return [prereq for prereq in item.prerequisites if prereq not in completed]


def pane_layout(key: str) -> tuple[DeltaGenerator, DeltaGenerator]:
    """Return (instruction, workspace) columns using a keyboard-selectable preset.

    Pointer users can also drag the Streamlit column divider. On a narrow
    viewport Streamlit stacks the columns automatically, keeping the first
    (instruction) pane before the workspace pane.
    """
    preset = st.radio(
        "Pane layout",
        options=list(PANE_PRESETS),
        index=list(PANE_PRESETS).index(DEFAULT_PANE_PRESET),
        horizontal=True,
        key=f"{key}_pane_preset",
        help="Choose how much width the instruction and workspace panes get.",
    )
    weights = PANE_PRESETS[preset]
    left, right = st.columns(list(weights))
    return left, right


def architecture_diagram(mermaid: str, text_summary: str) -> None:
    """Render a Mermaid diagram with a required text summary alternative.

    The text summary ensures the architecture is understandable without the
    diagram, color, or motion (an accessible, non-proprietary visual).
    """
    st.markdown(f"```mermaid\n{mermaid}\n```")
    with st.expander("Architecture described in text"):
        st.write(text_summary)


def empty_state(message: str) -> None:
    """Render an explicit empty state."""
    st.info(status_label(StatusTone.NEUTRAL, message))


def error_state(message: str) -> None:
    """Render an explicit, non-sensitive error state."""
    st.error(status_label(StatusTone.DANGER, message))


def offline_notice() -> None:
    """Render an explicit offline/unavailable-AWS notice."""
    st.warning(
        status_label(
            StatusTone.WARNING,
            "AWS validation is unavailable; lab checks will show as unavailable.",
        )
    )
