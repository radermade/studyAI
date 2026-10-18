"""Shared, reusable UI components used across views."""

from __future__ import annotations

import streamlit as st
from study_core.ui_state import ContentStatus, CurriculumItem, UiStateService

from app.theme import StatusTone, status_label

_STATUS_TONE: dict[ContentStatus, StatusTone] = {
    ContentStatus.NOT_STARTED: StatusTone.NEUTRAL,
    ContentStatus.IN_PROGRESS: StatusTone.PROGRESS,
    ContentStatus.COMPLETE: StatusTone.SUCCESS,
}


def curriculum_rail(
    ui: UiStateService,
    learner: str,
    *,
    due_count: int,
) -> None:
    """Render the collapsible curriculum rail with status and due-review badge."""
    with st.sidebar:
        st.caption(f"Due reviews: {due_count}")
        statuses = ui.content_status(learner)
        completed = {k for k, v in statuses.items() if v == ContentStatus.COMPLETE}
        for item in ui.list_curriculum():
            status = statuses.get(item.item_id, ContentStatus.NOT_STARTED)
            locked = _is_locked(item, completed)
            tone = StatusTone.WARNING if locked else _STATUS_TONE[status]
            text = f"{item.title}" + (" (locked)" if locked else "")
            st.write(status_label(tone, text))


def _is_locked(item: CurriculumItem, completed: set[str]) -> bool:
    return any(prereq not in completed for prereq in item.prerequisites)


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
