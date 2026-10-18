"""Review view: committed due reviews only."""

from __future__ import annotations

import streamlit as st
from study_core.bootstrap import StudyRuntime

from app.components import empty_state


def render(runtime: StudyRuntime, learner: str) -> None:
    """Render the Review view from committed due reviews."""
    st.subheader("Review")
    page = runtime.service.get_due_reviews(learner_id=learner)
    if not page.items:
        empty_state("No reviews are due. Correct answers schedule future reviews.")
        return
    st.write(f"{len(page.items)} review(s) due:")
    for item in page.items:
        st.write(f"- {item.objective_id} (question {item.question_id}), due {item.due_at:%Y-%m-%d}")
    st.caption("Open Grill to work through due items.")
