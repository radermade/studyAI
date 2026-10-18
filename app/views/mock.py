"""Mock view: a truthful placeholder; full readiness is Phase 8."""

from __future__ import annotations

import streamlit as st
from study_core.bootstrap import StudyRuntime

from app.theme import StatusTone, status_label


def render(runtime: StudyRuntime, learner: str) -> None:
    """Render the Mock view scope notice."""
    st.subheader("Mock")
    st.write(
        status_label(
            StatusTone.WARNING,
            "Timed, blueprint-weighted mock exams with delayed feedback are implemented in "
            "Phase 8. This view is intentionally a practice placeholder and does not yet "
            "produce a readiness result.",
        )
    )
