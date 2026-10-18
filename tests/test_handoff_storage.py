"""Tests for artifact storage, determinism, and the Phase 0 exit gate."""

from __future__ import annotations

from pathlib import Path

import pytest
from content.aip_c01 import build_seed_prompts
from scripts.phase0 import assemble_inputs
from study_core.artifacts import build_envelope, content_hash
from study_core.errors import CompatibilityError
from study_core.handoff import build_handoff, evaluate_phase0
from study_core.storage import FileArtifactStore


def test_authored_inputs_pass_the_gate() -> None:
    report = evaluate_phase0(assemble_inputs())
    assert report.accepted, [i.message for i in report.blockers]
    assert report.handoff_version is not None


def test_gate_blocks_on_insufficient_seed() -> None:
    inputs = assemble_inputs()
    short = build_seed_prompts()[:10]
    broken = inputs.model_copy(update={"seed_prompts": short})
    report = evaluate_phase0(broken)
    assert not report.accepted
    assert any(issue.code.startswith("seed.") for issue in report.blockers)


def test_handoff_refused_on_failing_gate() -> None:
    inputs = assemble_inputs()
    short = build_seed_prompts()[:10]
    broken = inputs.model_copy(update={"seed_prompts": short})
    report = evaluate_phase0(broken)
    with pytest.raises(ValueError):
        build_handoff(broken, report)


def test_handoff_is_deterministic() -> None:
    inputs = assemble_inputs()
    report = evaluate_phase0(inputs)
    first = build_handoff(inputs, report)
    second = build_handoff(inputs, report)
    assert first.content_sha256 == second.content_sha256


def test_envelope_rejects_unsupported_schema() -> None:
    with pytest.raises(CompatibilityError):
        build_envelope(
            schema_name="Nope",
            schema_version="v1",
            artifact_version="1",
            provenance="test",
            payload={},
        )


def test_envelope_detects_hash_mismatch() -> None:
    envelope = build_envelope(
        schema_name="Phase0Handoff",
        schema_version="v1",
        artifact_version="1",
        provenance="test",
        payload={"a": 1},
    )
    tampered = envelope.model_copy(update={"payload": {"a": 2}})
    with pytest.raises(ValueError):
        tampered.verify()


def test_atomic_store_round_trip(tmp_path: Path) -> None:
    store = FileArtifactStore(tmp_path)
    envelope = build_envelope(
        schema_name="Phase0Handoff",
        schema_version="v1",
        artifact_version="1",
        provenance="test",
        payload={"a": 1, "b": [2, 3]},
    )
    path = store.write_version(envelope)
    assert path.exists()
    loaded = store.read_version("Phase0Handoff", "1")
    assert loaded.content_sha256 == content_hash({"a": 1, "b": [2, 3]})
