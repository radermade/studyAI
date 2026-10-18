"""Streamlit entry point for the focused Grill + Labs workspace.

Run with:
    uv run streamlit run app/main.py

`streamlit run` puts this file's directory (app/) on sys.path rather than the
project root, so the project root is prepended here before importing project
packages. This makes the app runnable regardless of launch method.
"""

from __future__ import annotations

import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import streamlit as st  # noqa: E402 - import after sys.path setup

from app.runtime import get_runtime, learner_id  # noqa: E402
from app.theme import BASE_CSS, PRODUCT_NAME  # noqa: E402
from app.views import grill, labs, progress, review, scored  # noqa: E402

# Focused experience: practice (Grill), exam simulation (Scored Session), and
# hands-on walkthroughs (Labs). Review and Progress are the adaptive support.
_VIEWS = {
    "Grill": grill.render,
    "Scored Session": scored.render,
    "Labs": labs.render,
    "Review": review.render,
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
            "The study database is not ready. Run "
            "`uv run python -m scripts.phase1 ingest` first, then reload."
        )
        return

    learner = learner_id()
    st.title(PRODUCT_NAME)
    due = runtime.service.get_due_reviews(learner_id=learner)
    st.caption(f"AWS Certified Generative AI Developer (AIP-C01)  -  Due reviews: {len(due.items)}")

    view_name = st.sidebar.radio("Go to", options=list(_VIEWS), key="nav_view")
    st.sidebar.caption("Grill = practice.  Scored Session = exam sim.  Labs = AWS walkthroughs.")
    _VIEWS[view_name](runtime, learner)


main()
