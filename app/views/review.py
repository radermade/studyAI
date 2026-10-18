"""Review view: what you're missing — scored-session misses and due reviews."""

from __future__ import annotations

import streamlit as st
from study_core.bootstrap import StudyRuntime

from app.components import empty_state


def render(runtime: StudyRuntime, learner: str) -> None:
    """Render missed items from the latest scored session, then due reviews."""
    st.subheader("Review")
    st.caption("Study what you missed. Scored-session misses first, then spaced reviews.")

    _render_scored_misses(runtime, learner)
    st.divider()
    _render_due_reviews(runtime, learner)


def _render_scored_misses(runtime: StudyRuntime, learner: str) -> None:
    st.markdown("### Missed in your last scored session")
    latest = runtime.scored.latest_submitted(learner_id=learner)
    if latest is None:
        empty_state("No scored session yet. Run one from Scored Session.")
        return
    misses = runtime.scored.misses(session_id=latest)
    if not misses:
        st.success("No missed items in your last scored session.")
        return

    # Group misses by objective so weak objectives are visible.
    by_objective: dict[str, int] = {}
    for miss in misses:
        key = miss.objective_ids[0] if miss.objective_ids else "unknown"
        by_objective[key] = by_objective.get(key, 0) + 1
    st.write("Weak objectives: " + ", ".join(f"{k} ({v})" for k, v in sorted(by_objective.items())))

    for miss in misses:
        label = "Unanswered" if miss.unanswered else "Incorrect"
        with st.expander(f"[{label}] {miss.prompt[:80]}..."):
            correct = {oid for oid in miss.correct_option_ids}
            for rationale in miss.option_rationales:
                marker = "correct" if rationale.option_id in correct else "incorrect"
                st.markdown(f"- _({marker})_ {rationale.rationale}")
            if miss.explanation:
                st.info(miss.explanation)


def _render_due_reviews(runtime: StudyRuntime, learner: str) -> None:
    st.markdown("### Spaced reviews due")
    page = runtime.service.get_due_reviews(learner_id=learner)
    if not page.items:
        empty_state("No reviews are due. Correct answers schedule future reviews.")
        return
    st.write(f"{len(page.items)} review(s) due:")
    for item in page.items:
        st.write(f"- {item.objective_id} (question {item.question_id}), due {item.due_at:%Y-%m-%d}")
    st.caption("Open Grill to work through due items.")
