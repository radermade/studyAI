"""Progress view: multidimensional, evidence-based, labeled as an estimate."""

from __future__ import annotations

import streamlit as st
from study_core.bootstrap import StudyRuntime
from study_core.study_models import DomainMasteryReport, ReadinessReport

from app.components import status_badge
from app.theme import StatusTone

# Domains with authored content and an enforceable exit gate. The gate is
# per-domain and extensible; domains are added here as their content lands.
_EVALUATED_DOMAINS: tuple[int, ...] = (1, 2, 3, 4, 5)


def render(runtime: StudyRuntime, learner: str) -> None:
    """Render the Progress view."""
    st.subheader("Progress")
    report = runtime.service.get_progress(learner_id=learner)
    st.caption(report.note)

    _render_readiness(runtime, learner)
    _render_exit_gates(runtime, learner)

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


def _render_readiness(runtime: StudyRuntime, learner: str) -> None:
    report: ReadinessReport = runtime.readiness.evaluate(learner_id=learner)
    st.markdown("**Exam readiness (internal estimate)**")
    tone = StatusTone.SUCCESS if report.ready else StatusTone.PROGRESS
    verdict = "READY (internal estimate)" if report.ready else "not yet ready"
    scored = (
        f"{report.scored_accuracy:.0%}" if report.scored_accuracy is not None else "no mock yet"
    )
    status_badge(
        tone,
        f"Overall readiness: {verdict} "
        f"(latest full-length mock: {scored}; threshold {report.overall_threshold:.0%})",
    )
    st.caption(report.note)
    with st.expander("Readiness criteria and required-lab matrix", expanded=not report.ready):
        for criterion in report.criteria:
            icon_tone = StatusTone.SUCCESS if criterion.met else StatusTone.DANGER
            mark = "met" if criterion.met else "not met"
            status_badge(icon_tone, f"{criterion.label}: {mark}")
            st.caption(criterion.detail)
        st.markdown("_Required lab matrix_")
        for entry in report.lab_matrix:
            if entry.completed:
                how = "independent" if entry.independent else "assisted"
                lab_tone = StatusTone.SUCCESS
                text = f"{entry.title}: completed ({how})"
            else:
                lab_tone = StatusTone.NEUTRAL
                text = f"{entry.title}: not completed"
            status_badge(lab_tone, text)
    st.divider()


def _render_exit_gates(runtime: StudyRuntime, learner: str) -> None:
    st.markdown("**Domain exit gates**")
    st.caption(
        "A transparent internal study gate from committed evidence, " "not an AWS score prediction."
    )
    for domain_id in _EVALUATED_DOMAINS:
        gate = runtime.mastery.evaluate(learner_id=learner, domain_id=domain_id)
        _render_gate(domain_id, gate, expanded=domain_id == _EVALUATED_DOMAINS[0])
    st.divider()


def _render_gate(domain_id: int, gate: DomainMasteryReport, *, expanded: bool) -> None:
    tone = StatusTone.SUCCESS if gate.passed else StatusTone.PROGRESS
    verdict = "PASSED" if gate.passed else "not yet met"
    accuracy = f"{gate.grill_accuracy:.0%}" if gate.grill_accuracy is not None else "n/a"
    with st.expander(f"Domain {domain_id} exit gate: {verdict}", expanded=expanded):
        status_badge(
            tone,
            f"Domain {domain_id} gate {verdict} "
            f"(grill accuracy {accuracy} over {gate.grill_attempts} attempts)",
        )
        for criterion in gate.criteria:
            mark = "met" if criterion.met else "not met"
            scope = "required" if criterion.mandatory else "informational"
            icon_tone = StatusTone.SUCCESS if criterion.met else StatusTone.DANGER
            if not criterion.mandatory and not criterion.met:
                icon_tone = StatusTone.NEUTRAL
            status_badge(icon_tone, f"{criterion.label} [{scope}]: {mark}")
            st.caption(criterion.detail)
