"""Phase 0 command: build and evaluate the acceptance gate and handoff.

Usage:
    python -m scripts.phase0 evaluate   # run the gate and print blockers
    python -m scripts.phase0 build      # evaluate, then write the handoff

Runtime artifacts are written under the gitignored `data/` directory.
"""

from __future__ import annotations

import sys
from pathlib import Path

from content.aip_c01 import (
    BLUEPRINT_VERSION,
    build_baseline_run,
    build_labs,
    build_manifest,
    build_profile,
    build_safety_policy,
    build_seed_prompts,
    build_source_registry,
)
from study_core.baseline import summarize_baseline
from study_core.handoff import (
    AcceptanceReport,
    Phase0Inputs,
    build_handoff,
    evaluate_phase0,
)
from study_core.storage import FileArtifactStore

DATA_ROOT = Path("data") / "phase0"


def assemble_inputs() -> Phase0Inputs:
    """Assemble all Phase 0 inputs from authored content."""
    return Phase0Inputs(
        blueprint_version=BLUEPRINT_VERSION,
        manifest=build_manifest(),
        registry=build_source_registry(),
        profile=build_profile(),
        safety_policy=build_safety_policy(),
        labs=build_labs(),
        seed_prompts=build_seed_prompts(),
        baseline_summary=summarize_baseline(build_baseline_run()),
    )


def _print_report(report: AcceptanceReport) -> None:
    if report.accepted:
        print(f"Phase 0 ACCEPTED (handoff version {report.handoff_version})")
        return
    print(f"Phase 0 NOT accepted: {len(report.blockers)} blocker(s)")
    for issue in report.blockers:
        print(f"  [{issue.code}] {issue.path}: {issue.message}")


def command_evaluate() -> int:
    """Run the acceptance gate and print the report."""
    report = evaluate_phase0(assemble_inputs())
    _print_report(report)
    return 0 if report.accepted else 1


def command_build() -> int:
    """Evaluate the gate and, on acceptance, write the handoff artifact."""
    inputs = assemble_inputs()
    report = evaluate_phase0(inputs)
    _print_report(report)
    if not report.accepted:
        return 1
    envelope = build_handoff(inputs, report)
    store = FileArtifactStore(DATA_ROOT)
    path = store.write_version(envelope)
    print(f"Wrote handoff: {path}")
    return 0


def main(argv: list[str]) -> int:
    """CLI entry point."""
    if len(argv) != 1 or argv[0] not in {"evaluate", "build"}:
        print("usage: python -m scripts.phase0 {evaluate|build}", file=sys.stderr)
        return 2
    return command_evaluate() if argv[0] == "evaluate" else command_build()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
