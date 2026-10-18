"""Tests for the objective manifest and source registry validators."""

from __future__ import annotations

from content.aip_c01 import build_manifest, build_source_registry
from study_core.blueprint import validate_objective_manifest
from study_core.sources import required_sources_present, validate_source_registry


def test_authored_manifest_is_valid() -> None:
    assert validate_objective_manifest(build_manifest()) == ()


def test_manifest_with_wrong_weight_fails() -> None:
    manifest = build_manifest()
    # Tamper with the first domain's weight via model_copy.
    tampered = manifest.model_copy(
        update={
            "domains": (
                manifest.domains[0].model_copy(update={"weight_percent": 99}),
                *manifest.domains[1:],
            )
        }
    )
    issues = validate_objective_manifest(tampered)
    assert any(issue.code.startswith("domain.weight") for issue in issues)


def test_manifest_missing_objective_fails() -> None:
    manifest = build_manifest()
    # min_length=20 is enforced by the model, so keep 20 entries but duplicate
    # the first objective in place of the dropped last one.
    padded = (*manifest.objectives[:-1], manifest.objectives[0])
    tampered = manifest.model_copy(update={"objectives": padded})
    issues = validate_objective_manifest(tampered)
    codes = {issue.code for issue in issues}
    assert "objective.duplicate" in codes
    assert "objective.missing" in codes


def test_authored_registry_is_valid_and_complete() -> None:
    registry = build_source_registry()
    assert validate_source_registry(registry) == ()
    assert required_sources_present(registry.sources)


def test_registry_missing_required_source_fails() -> None:
    registry = build_source_registry()
    reduced = registry.model_copy(update={"sources": registry.sources[1:]})
    issues = validate_source_registry(reduced)
    assert any(issue.code == "source.missing_required" for issue in issues)
