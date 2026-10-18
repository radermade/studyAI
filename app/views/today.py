"""Today view: due reviews, a recommended next item, and resume."""

from __future__ import annotations

import streamlit as st
from study_core.bootstrap import StudyRuntime

from app.components import empty_state


def render(runtime: StudyRuntime, learner: str) -> None:
    """Render the Today view."""
    st.subheader("Today")
    due = runtime.service.get_due_reviews(learner_id=learner)
    st.metric("Due reviews", len(due.items))

    resume = runtime.ui.get_resume(learner)
    if resume is not None and resume.entity_id:
        st.write(f"Resume: {resume.view} - {resume.entity_id}")
    else:
        empty_state("No session to resume yet. Start in Learn or Grill.")

    curriculum = runtime.ui.list_curriculum()
    statuses = runtime.ui.content_status(learner)
    recommended = next(
        (item for item in curriculum if statuses.get(item.item_id) is None),
        curriculum[0] if curriculum else None,
    )
    if recommended is not None:
        st.write(f"Recommended next: **{recommended.title}**")
