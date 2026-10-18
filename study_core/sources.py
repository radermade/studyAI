"""Attributable source registry with truthful freshness state.

A source records canonical metadata and a freshness status that is independent
of network availability: a failed refresh never advances `retrieved_at` and
never claims revalidation.
"""

from __future__ import annotations

from collections.abc import Sequence
from datetime import datetime
from enum import StrEnum

from pydantic import Field, field_validator

from study_core.common import StrictModel, ValidationIssue, ensure_utc, is_valid_task_id

# Sources every accepted registry must contain, by stable ID.
REQUIRED_SOURCE_IDS: tuple[str, ...] = (
    "aip-c01-exam-overview",
    "aip-c01-domain-1",
    "aip-c01-domain-2",
    "aip-c01-domain-3",
    "aip-c01-domain-4",
    "aip-c01-domain-5",
    "aip-c01-certification-prep",
)


class Freshness(StrEnum):
    """Truthful source-review state, independent of network availability."""

    CURRENT = "current"
    REVIEW_DUE = "review_due"
    STALE = "stale"
    UNVERIFIED = "unverified"


class SourceType(StrEnum):
    """Classification of a registered source."""

    EXAM_GUIDE = "exam_guide"
    DOMAIN_PAGE = "domain_page"
    CERTIFICATION_PAGE = "certification_page"
    DOCUMENTATION = "documentation"


class SourceRecord(StrictModel):
    """One attributable source with freshness and objective mappings."""

    source_id: str
    url: str
    title: str
    publisher: str
    retrieved_at: datetime
    source_type: SourceType
    objective_ids: tuple[str, ...] = ()
    freshness: Freshness
    blueprint_version: str

    @field_validator("url")
    @classmethod
    def _require_https(cls, value: str) -> str:
        if not value.startswith("https://"):
            raise ValueError("source URL must be a canonical HTTPS URL")
        return value

    @field_validator("retrieved_at")
    @classmethod
    def _utc(cls, value: datetime) -> datetime:
        return ensure_utc(value)

    @field_validator("objective_ids")
    @classmethod
    def _valid_objectives(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        for objective_id in value:
            if not is_valid_task_id(objective_id):
                raise ValueError(f"unknown objective id: {objective_id}")
        return value


class SourceRegistry(StrictModel):
    """A collection of registered sources for one blueprint version."""

    blueprint_version: str
    sources: tuple[SourceRecord, ...] = Field(min_length=1)


def validate_source_registry(registry: SourceRegistry) -> tuple[ValidationIssue, ...]:
    """Return every blocking issue in a source registry.

    Checks mandatory primary sources, unique source IDs, and consistent
    blueprint versioning. Returns an empty tuple when the registry is valid.
    """
    issues: list[ValidationIssue] = []
    seen: set[str] = set()
    for index, source in enumerate(registry.sources):
        if source.source_id in seen:
            issues.append(
                ValidationIssue(
                    code="source.duplicate_id",
                    path=f"sources[{index}].source_id",
                    message=f"duplicate source id {source.source_id}",
                )
            )
        seen.add(source.source_id)
        if source.blueprint_version != registry.blueprint_version:
            issues.append(
                ValidationIssue(
                    code="source.blueprint_mismatch",
                    path=f"sources[{index}].blueprint_version",
                    message="source blueprint version does not match registry",
                )
            )
    missing = [sid for sid in REQUIRED_SOURCE_IDS if sid not in seen]
    for source_id in missing:
        issues.append(
            ValidationIssue(
                code="source.missing_required",
                path="sources",
                message=f"required source {source_id} is absent",
            )
        )
    return tuple(issues)


def required_sources_present(sources: Sequence[SourceRecord]) -> bool:
    """Return True when all mandatory primary sources are registered."""
    present = {source.source_id for source in sources}
    return all(source_id in present for source_id in REQUIRED_SOURCE_IDS)
