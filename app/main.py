"""Streamlit entry point: header, curriculum rail, and eight-view routing.

Run with:
    uv run streamlit run app/main.py
"""

from __future__ import annotations

import streamlit as st
from content.aip_c01 import BLUEPRINT_VERSION

from app.components import curriculum_rail
from app.runtime import get_runtime, learner_id
from app.theme import BASE_CSS, PRODUCT_NAME
from app.views import grill, knowledge, labs, learn, mock, progress, review, today

_VIEWS = {
    "Today": today.render,
    "Learn": learn.render,
    "Grill": grill.render,
    "Labs": labs.render,
    "Review": review.render,
    "Mock": mock.render,
    "Knowledge": knowledge.render,
    "Progress": progress.render,
}


def main() -> None:
    """Render the workspace shell and the selected view."""
    st.set_page_config(page_title=PRODUCT_NAME, layout="wide")
    st.markdown(BASE_CSS, unsafe_allow_html=True)

    try:
        runtime = get_runtime()
    except Exception:
        st.error(
            "The study database is not ready. Run `uv run python -m scripts.phase1 ingest` "
            "first, then reload."
        )
        return

    learner = learner_id()
    st.title(PRODUCT_NAME)
    st.caption(f"Exam: AIP-C01 - Blueprint: {BLUEPRINT_VERSION}")

    view_name = st.sidebar.radio("Navigate", options=list(_VIEWS), key="nav_view")
    due = runtime.service.get_due_reviews(learner_id=learner)
    curriculum_rail(runtime.ui, learner, due_count=len(due.items))

    _VIEWS[view_name](runtime, learner)


main()
