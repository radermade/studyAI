"""Learn view: curriculum selection and a short, blocked lesson player."""

from __future__ import annotations

import streamlit as st
from study_core.bootstrap import StudyRuntime
from study_core.ui_state import ContentStatus

from app.components import empty_state


def render(runtime: StudyRuntime, learner: str) -> None:
    """Render the Learn view with a short, block-structured lesson player."""
    st.subheader("Learn")
    lessons = [i for i in runtime.ui.list_curriculum() if i.item_type == "lesson"]
    if not lessons:
        empty_state("No lessons are available yet.")
        return

    titles = {item.item_id: item.title for item in lessons}
    selected = st.selectbox(
        "Lesson", options=list(titles), format_func=lambda i: titles[i], key="learn_lesson"
    )
    item = next(i for i in lessons if i.item_id == selected)
    objective = item.objective_ids[0]

    content = runtime.service.search_local_material(
        query=objective.replace("AIP-", "").replace(".", " "), limit=1
    )
    st.markdown(f"**Objective:** {', '.join(item.objective_ids)}")

    # Short, differentiated blocks rather than one long page. Authored domain
    # content (Phases 3-7) fills these; the structure stays stable.
    st.markdown("### Concept")
    if content.results:
        hit = content.results[0]
        st.write(hit.snippet)
        st.caption(f"Source freshness: {hit.freshness} - {', '.join(hit.objective_ids)}")
    else:
        empty_state("No source content indexed for this objective.")

    st.markdown("### Decision and trade-off")
    st.write(
        "Identify the decisive constraint for this objective and the trade-off that "
        "rules out tempting alternatives."
    )

    st.markdown("### Common failure mode")
    st.write("Note where this choice typically goes wrong under production load or scale.")

    st.markdown("### Recall check")
    st.text_input(
        "In one sentence, state the decisive constraint for this objective.",
        key=f"recall-{item.item_id}",
    )

    st.markdown("### Your notes")
    note_key = f"note-lesson-{item.item_id}"
    existing_note = runtime.ui.get_note(learner_id=learner, context=f"lesson:{item.item_id}")
    note = st.text_area("Notes", value=existing_note, key=note_key, label_visibility="collapsed")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Save note", key=f"save-{item.item_id}"):
            runtime.ui.save_note(learner_id=learner, context=f"lesson:{item.item_id}", text=note)
            st.success("Note saved.")
    with col2:
        if st.button("Mark complete & practice", key=f"complete-{item.item_id}"):
            runtime.ui.set_content_status(
                learner_id=learner,
                item_id=item.item_id,
                status=ContentStatus.COMPLETE,
                position=0,
            )
            runtime.ui.set_resume(learner_id=learner, view="Grill", entity_id=objective, position=0)
            st.success("Marked complete. Open Grill to practice this objective.")
