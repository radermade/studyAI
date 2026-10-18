"""Grill view: one-question-at-a-time practice with real, ordered feedback."""

from __future__ import annotations

import time
import uuid
from typing import Any

import streamlit as st
from study_core.bootstrap import StudyRuntime
from study_core.service import ContentGapError
from study_core.study_models import GradeOutcome, SessionMode

from app.components import empty_state, error_state, status_badge
from app.theme import StatusTone

_SESSION_KEY = "grill_session_id"
_QUESTION_KEY = "grill_question"
_SERVED_AT_KEY = "grill_served_at"
_FEEDBACK_KEY = "grill_feedback"


def render(runtime: StudyRuntime, learner: str) -> None:
    """Render the Grill practice loop."""
    st.subheader("Grill")
    st.caption("You'll get one scenario question at a time. Answer, then see why.")

    if st.session_state.get(_SESSION_KEY) is None:
        empty_state("Start a session to practice one question at a time.")
        if st.button("Start grill session", key="grill_start"):
            session = runtime.service.start_session(
                learner_id=learner,
                mode=SessionMode.GRILL,
                objective_filter=(),
                request_id=f"start-{uuid.uuid4().hex}",
            )
            st.session_state[_SESSION_KEY] = session.session_id
            st.session_state[_FEEDBACK_KEY] = None
            _serve_next(runtime)
            st.rerun()
        return

    # If the last question was answered, show its feedback and a Next button.
    if st.session_state.get(_FEEDBACK_KEY) is not None:
        _render_feedback(runtime)
        return

    question = st.session_state.get(_QUESTION_KEY)
    if question is None:
        empty_state("No more eligible questions right now. Check Review, or come back later.")
        if st.button("End session", key="grill_end"):
            _reset()
            st.rerun()
        return

    _render_question(runtime, question)


def _render_question(runtime: StudyRuntime, question: dict[str, Any]) -> None:
    st.markdown(f"**{question['prompt']}**")
    choice = st.radio(
        "Select the best answer",
        options=[o["option_id"] for o in question["options"]],
        format_func=lambda oid: next(
            o["text"] for o in question["options"] if o["option_id"] == oid
        ),
        key=f"grill_choice_{question['question_id']}",
    )
    confidence = st.slider("How confident are you? (0-100)", 0, 100, 50, key="grill_conf")
    if st.button("Submit answer", key="grill_submit"):
        _grade(runtime, question, choice, confidence)
        st.rerun()


def _render_feedback(runtime: StudyRuntime) -> None:
    feedback = st.session_state[_FEEDBACK_KEY]
    outcome = feedback["outcome"]

    # 1. Result.
    if outcome == GradeOutcome.CORRECT.value:
        status_badge(StatusTone.SUCCESS, "Correct")
    elif outcome == GradeOutcome.INCORRECT.value:
        status_badge(StatusTone.DANGER, "Incorrect")
    else:
        status_badge(StatusTone.WARNING, "Grading uncertain")

    st.markdown(f"**{feedback['prompt']}**")
    chosen = feedback["chosen_option_id"]
    correct_ids = feedback["correct_option_ids"]

    # 2-4. Per-option reasoning: mark correct answer and explain your choice.
    for option in feedback["options"]:
        oid = option["option_id"]
        rationale = feedback["rationales"].get(oid, "")
        marker = "Correct answer" if oid in correct_ids else "Incorrect"
        you = "  <- your answer" if oid == chosen else ""
        st.markdown(f"- **{option['text']}** _({marker}{you})_")
        if rationale:
            st.caption(rationale)

    # 5. Explanation and source.
    if feedback["explanation"]:
        st.info(feedback["explanation"])
    if feedback["source_ids"]:
        st.caption(f"Source: {', '.join(feedback['source_ids'])}")
    if feedback["review_scheduled"]:
        st.caption("A spaced review has been scheduled for this item.")

    # 6. Next action.
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Next question", key="grill_next"):
            st.session_state[_FEEDBACK_KEY] = None
            _serve_next(runtime)
            st.rerun()
    with col2:
        if st.button("End session", key="grill_end2"):
            _reset()
            st.rerun()


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
    session_id = st.session_state[_SESSION_KEY]
    elapsed = max(0.0, time.monotonic() - st.session_state.get(_SERVED_AT_KEY, time.monotonic()))
    try:
        grade = runtime.service.grade_and_record(
            session_id=session_id,
            question_id=question["question_id"],
            selected_option_ids=[choice],
            confidence=confidence,
            elapsed_seconds=elapsed,
            event_id=f"grade-{question['question_id']}-{uuid.uuid4().hex}",
        )
        explanation = runtime.service.explain_answer(
            session_id=session_id, question_id=question["question_id"]
        )
    except Exception:
        error_state("Could not record the attempt. Please retry.")
        return

    st.session_state[_FEEDBACK_KEY] = {
        "outcome": grade.outcome.value,
        "prompt": question["prompt"],
        "options": question["options"],
        "chosen_option_id": choice,
        "correct_option_ids": list(explanation.correct_option_ids),
        "rationales": {r.option_id: r.rationale for r in explanation.option_rationales},
        "explanation": explanation.explanation,
        "source_ids": question["source_ids"],
        "review_scheduled": grade.next_review_due_at is not None,
    }


def _reset() -> None:
    for key in (_SESSION_KEY, _QUESTION_KEY, _SERVED_AT_KEY, _FEEDBACK_KEY):
        st.session_state.pop(key, None)
