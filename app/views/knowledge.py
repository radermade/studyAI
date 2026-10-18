"""Knowledge view: local FTS search with objective filters and paging."""

from __future__ import annotations

import streamlit as st
from study_core.bootstrap import StudyRuntime
from study_core.common import ALL_TASK_IDS

from app.components import empty_state, error_state


def render(runtime: StudyRuntime, learner: str) -> None:
    """Render the Knowledge search view."""
    st.subheader("Knowledge")
    query = st.text_input("Search local material", key="kb_query")
    objective = st.selectbox("Filter by objective", options=["(any)", *ALL_TASK_IDS], key="kb_obj")
    if not query:
        empty_state("Enter a query to search indexed local sources.")
        return
    objective_filter = () if objective == "(any)" else (objective,)
    try:
        page = runtime.service.search_local_material(
            query=query, objective_filter=objective_filter, limit=10
        )
    except ValueError:
        error_state("That query could not be parsed. Try plain keywords.")
        return
    if not page.results:
        empty_state("No local material matched.")
        return
    for hit in page.results:
        st.markdown(f"**{hit.title}**")
        st.write(hit.snippet)
        st.caption(f"{', '.join(hit.objective_ids)} - freshness: {hit.freshness}")
