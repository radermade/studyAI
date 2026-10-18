"""Progress view: multidimensional, evidence-based, labeled as an estimate."""

from __future__ import annotations

import streamlit as st
from study_core.bootstrap import StudyRuntime


def render(runtime: StudyRuntime, learner: str) -> None:
    """Render the Progress view."""
    st.subheader("Progress")
    report = runtime.service.get_progress(learner_id=learner)
    st.caption(report.note)

    measured = [o for o in report.objectives if o.attempts > 0]
    col1, col2, col3 = st.columns(3)
    col1.metric("Objectives attempted", len(measured))
    col2.metric("Objectives uncovered", len(report.uncovered_objectives))
    total_mis = sum(o.open_misconceptions for o in report.objectives)
    col3.metric("Open misconceptions", total_mis)

    if measured:
        st.write("Per-objective accuracy (measured only):")
        for objective in measured:
            accuracy = f"{objective.accuracy:.0%}" if objective.accuracy is not None else "n/a"
            st.write(
                f"- {objective.objective_id}: {objective.correct}/{objective.attempts} "
                f"({accuracy}), open misconceptions: {objective.open_misconceptions}"
            )
    else:
        st.info("No attempts recorded yet. Practice in Grill to build evidence.")
