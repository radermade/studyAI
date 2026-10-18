"""Grill view: one-question-at-a-time practice with ordered feedback."""

from __future__ import annotations

import time
import uuid
from typing import Any

import streamlit as st
from study_core.bootstrap import StudyRuntime
from study_core.service import ContentGapError
from study_core.study_models import GradeOutcome, SessionMode

from app.components import empty_state, error_state

_SESSION_KEY = "grill_session_id"
_QUESTION_KEY = "grill_question"
_SERVED_AT_KEY = "grill_served_at"


def render(runtime: StudyRuntime, learner: str) -> None:
    """Render the Grill practice loop."""
    st.subheader("Grill")

    if st.session_state.get(_SESSION_KEY) is None:
        if st.button("Start grill session", key="grill_start"):
            session = runtime.service.start_session(
                learner_id=learner,
                mode=SessionMode.GRILL,
                objective_filter=(),
                request_id=f"start-{uuid.uuid4().hex}",
            )
            st.session_state[_SESSION_KEY] = session.session_id
            _serve_next(runtime)
            st.rerun()
        empty_state("Start a session to practice one question at a time.")
        return

    question = st.session_state.get(_QUESTION_KEY)
    if question is None:
        empty_state("No question loaded.")
        return

    st.markdown(f"**{question['prompt']}**")
    st.caption(f"Objectives: {', '.join(question['objective_ids'])}")
    choice = st.radio(
        "Your answer",
        options=[o["option_id"] for o in question["options"]],
        format_func=lambda oid: next(
            o["text"] for o in question["options"] if o["option_id"] == oid
        ),
        key=f"grill_choice_{question['question_id']}",
    )
    confidence = st.slider("Confidence", 0, 100, 50, key="grill_conf")

    if st.button("Submit answer", key="grill_submit"):
        _grade(runtime, question, choice, confidence)


def _serve_next(runtime: StudyRuntime) -> None:
    session_id = st.session_state[_SESSION_KEY]
    try:
        question = runtime.service.next_question(
            session_id=session_id, request_id=f"nq-{uuid.uuid4().hex}"
        )
    except ContentGapError:
        st.session_state[_QUESTION_KEY] = None
        return
    st.session_state[_QUESTION_KEY] = question.model_dump(mode="json")
    st.session_state[_SERVED_AT_KEY] = time.monotonic()


def _grade(
    runtime: StudyRuntime,
    question: dict[str, Any],
    choice: str,
    confidence: int,
) -> None:
    elapsed = max(0.0, time.monotonic() - st.session_state.get(_SERVED_AT_KEY, time.monotonic()))
    try:
        grade = runtime.service.grade_and_record(
            session_id=st.session_state[_SESSION_KEY],
            question_id=question["question_id"],
            selected_option_ids=[choice],
            confidence=confidence,
            elapsed_seconds=elapsed,
            event_id=f"grade-{question['question_id']}-{uuid.uuid4().hex}",
        )
    except Exception:
        error_state("Could not record the attempt. Please retry.")
        return

    # Ordered feedback: result, then reasoning cue, then source, then next action.
    if grade.outcome == GradeOutcome.CORRECT:
        st.success("Correct.")
    elif grade.outcome == GradeOutcome.INCORRECT:
        st.error("Incorrect.")
    else:
        st.warning("Grading uncertain.")
    st.write("Focus on the decisive constraint named in the scenario.")
    st.caption(f"Sources: {', '.join(question['source_ids'])}")
    if grade.next_review_due_at is not None:
        st.caption("A review has been scheduled for this item.")

    if st.button("Next question", key="grill_next"):
        _serve_next(runtime)
        st.rerun()
