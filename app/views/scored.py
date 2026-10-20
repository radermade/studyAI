"""Scored Session view: AWS-style exam simulation with delayed feedback.

One item at a time, no feedback until submission, then an original terminal
score readout and a review of every missed item. Supports reset and history.
"""

from __future__ import annotations

import uuid
from collections.abc import Callable

import streamlit as st
from study_core.bootstrap import StudyRuntime
from study_core.common import ALL_TASK_IDS
from study_core.service import ContentGapError
from study_core.study_models import ScoredItemView

from app.components import empty_state, error_state, status_badge
from app.theme import StatusTone, score_banner, score_readout

_POS_KEY = "scored_position"

_DOMAIN_LABELS = {
    1: "D1 Foundation models, data, compliance",
    2: "D2 Implementation and integration",
    3: "D3 Safety, security, governance",
    4: "D4 Operations and optimization",
    5: "D5 Testing and troubleshooting",
}


def render(runtime: StudyRuntime, learner: str) -> None:
    """Render the scored-session flow."""
    st.subheader("Scored Session")
    st.caption(
        "Exam-style: officially weighted questions, no feedback until you submit, "
        "then a scaled-score estimate. Internal estimate only, not an AWS score."
    )

    active = runtime.scored.active_session(learner_id=learner)
    if active is None:
        _render_start(runtime, learner)
        _render_latest_result(runtime, learner)
        return

    _render_session(runtime, learner, active)


def _render_start(runtime: StudyRuntime, learner: str) -> None:
    all_domains = sorted({int(t.split("-")[1].split(".")[0]) for t in ALL_TASK_IDS})
    chosen = st.multiselect(
        "Domains (leave empty for all available)",
        options=all_domains,
        format_func=lambda d: _DOMAIN_LABELS.get(d, f"Domain {d}"),
        key="scored_scope",
    )
    timed = st.checkbox("Timed (3 minutes per question)", key="scored_timed")
    if st.button("Start scored session", key="scored_start"):
        try:
            view = runtime.scored.start(
                learner_id=learner,
                scope_domains=chosen,
                time_limit_seconds=(180 * 40 if timed else None),
            )
        except ContentGapError:
            error_state("No reviewed questions are available for that scope yet.")
            return
        st.session_state[_POS_KEY] = 0
        if not view.full_length:
            st.info(
                f"Not full-length: {view.scored_total} scored "
                f"question(s) from available content."
            )
        st.rerun()


def _render_session(runtime: StudyRuntime, learner: str, session_id: str) -> None:
    position = int(st.session_state.get(_POS_KEY, 0))
    item = runtime.scored.current_item(session_id=session_id, position=position)

    st.progress((position + 1) / item.total, text=f"Question {position + 1} of {item.total}")
    st.markdown(f"**{item.prompt}**")

    # Render the answer widget appropriate to the question format. Each branch
    # produces a `commit` callable that persists the current selection.
    commit = _render_answer_widget(runtime, session_id, position, item)

    nav1, nav2, nav3 = st.columns(3)
    with nav1:
        if st.button("Save & previous", key="scored_prev", disabled=position == 0):
            commit()
            st.session_state[_POS_KEY] = position - 1
            st.rerun()
    with nav2:
        if st.button("Save & next", key="scored_next", disabled=position >= item.total - 1):
            commit()
            st.session_state[_POS_KEY] = position + 1
            st.rerun()
    with nav3:
        if st.button("Save answer", key="scored_save"):
            commit()
            st.toast("Answer saved.")

    st.divider()
    sub1, sub2 = st.columns(2)
    with sub1:
        if st.button("Submit session", key="scored_submit", type="primary"):
            commit()
            runtime.scored.submit(session_id=session_id, event_id=f"submit-{uuid.uuid4().hex}")
            st.session_state.pop(_POS_KEY, None)
            st.rerun()
    with sub2:
        if st.button("Reset / abandon", key="scored_reset"):
            runtime.scored.reset(session_id=session_id)
            st.session_state.pop(_POS_KEY, None)
            st.rerun()


def _render_answer_widget(
    runtime: StudyRuntime,
    session_id: str,
    position: int,
    item: ScoredItemView,
) -> Callable[[], None]:
    """Render the format-specific answer widget; return a commit callable."""
    fmt = item.question_format
    key = f"{session_id}_{position}"

    if fmt == "matching":
        st.caption("Match each item on the left to one option (all pairs must be correct).")
        prior = dict(item.selected_pairs)
        response_ids = [r.option_id for r in item.match_responses]
        response_text = {r.option_id: r.text for r in item.match_responses}
        pairs: dict[str, str] = {}
        for prompt in item.match_prompts:
            default = prior.get(prompt.option_id)
            index = response_ids.index(default) if default in response_ids else None
            chosen = st.selectbox(
                prompt.text,
                options=response_ids,
                index=index,
                format_func=lambda rid: response_text[rid],
                placeholder="Select a match...",
                key=f"scored_match_{key}_{prompt.option_id}",
            )
            if chosen is not None:
                pairs[prompt.option_id] = chosen

        def commit_match() -> None:
            runtime.scored.answer_match(
                session_id=session_id, question_id=item.question_id, pairs=pairs
            )

        return commit_match

    if fmt == "ordering":
        st.caption("Put the steps in the correct order (the whole sequence must be right).")
        option_ids = [o.option_id for o in item.options]
        option_text = {o.option_id: o.text for o in item.options}
        n = len(option_ids)
        prior_seq = list(item.selected_option_ids)
        ordered: list[str] = []
        for slot in range(n):
            default = prior_seq[slot] if slot < len(prior_seq) else None
            index = option_ids.index(default) if default in option_ids else None
            chosen = st.selectbox(
                f"Step {slot + 1}",
                options=option_ids,
                index=index,
                format_func=lambda oid: option_text[oid],
                placeholder="Select a step...",
                key=f"scored_order_{key}_{slot}",
            )
            if chosen is not None:
                ordered.append(chosen)
        if len(set(ordered)) != len(ordered):
            st.warning("Each step may be used only once; fix duplicates before submitting.")

        def commit_order() -> None:
            # Only persist a full, duplicate-free ordering; otherwise store empty.
            valid = len(ordered) == n and len(set(ordered)) == n
            runtime.scored.answer(
                session_id=session_id,
                question_id=item.question_id,
                selected_option_ids=ordered if valid else [],
            )

        return commit_order

    if fmt == "multiple_response":
        st.caption("Select ALL that apply (multiple-response: graded all-or-nothing).")
        prior_ids = set(item.selected_option_ids)
        chosen_ids = [
            o.option_id
            for o in item.options
            if st.checkbox(
                o.text,
                value=o.option_id in prior_ids,
                key=f"scored_choice_{key}_{o.option_id}",
            )
        ]

        def commit_multi() -> None:
            runtime.scored.answer(
                session_id=session_id, question_id=item.question_id, selected_option_ids=chosen_ids
            )

        return commit_multi

    # Default: single-answer multiple choice.
    default_opt = item.selected_option_ids[0] if item.selected_option_ids else None
    opt_ids = [o.option_id for o in item.options]
    idx = opt_ids.index(default_opt) if default_opt in opt_ids else None
    choice = st.radio(
        "Your answer",
        options=opt_ids,
        index=idx,
        format_func=lambda oid: next(o.text for o in item.options if o.option_id == oid),
        key=f"scored_choice_{key}",
    )

    def commit_single() -> None:
        runtime.scored.answer(
            session_id=session_id,
            question_id=item.question_id,
            selected_option_ids=[choice] if choice is not None else [],
        )

    return commit_single


def _render_latest_result(runtime: StudyRuntime, learner: str) -> None:
    # Non-accumulating: show only the single most recent result, if any.
    latest = runtime.scored.latest_submitted(learner_id=learner)
    if latest is not None:
        _render_result(runtime, latest)
    else:
        empty_state("No scored session yet. Start one above.")


def _render_result(runtime: StudyRuntime, session_id: str) -> None:
    result = runtime.scored.submit(session_id=session_id, event_id=f"view-{session_id}")
    st.markdown("### Most recent result")
    status_badge(
        StatusTone.SUCCESS if result.passed else StatusTone.DANGER,
        "PASS" if result.passed else "FAIL",
    )
    # Decorative ASCII banner plus the accessible text readout.
    st.code(score_banner(result.passed), language="text")
    st.code(
        score_readout(
            passed=result.passed,
            raw_correct=result.raw_correct,
            scored_total=result.scored_total,
            percent=result.percent,
            scaled_estimate=result.scaled_estimate,
        ),
        language="text",
    )
    st.caption(result.estimate_note)
    if not result.full_length:
        st.caption("Reduced session — interpret the estimate with caution.")

    st.markdown("**Per-domain (informational — scoring is compensatory):**")
    for d in result.per_domain:
        st.write(f"- {_DOMAIN_LABELS.get(d.domain_id, d.domain_id)}: {d.correct}/{d.total}")

    misses = runtime.scored.misses(session_id=session_id)
    if misses:
        st.markdown(f"**Missed {len(misses)} item(s) — open Review to study them.**")
    else:
        empty_state("No missed items in this session.")
