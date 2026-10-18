"""Versioned artifact envelopes and canonical serialization.

Every Phase 0 artifact is wrapped in an envelope that records its schema name,
schema version, artifact version, content hash, provenance, and creation time.
Serialization is canonical so repeated builds from identical inputs are
byte-for-byte identical and change detection via hash is reliable.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from typing import Any

from pydantic import Field

from study_core.common import StrictModel, utc_now
from study_core.errors import CompatibilityError

# Supported schema versions. An artifact declaring any other version fails closed.
SUPPORTED_SCHEMA_VERSIONS: dict[str, frozenset[str]] = {
    "ObjectiveManifest": frozenset({"v1"}),
    "SourceRegistry": frozenset({"v1"}),
    "LearnerProfile": frozenset({"v1"}),
    "LabSafetyPolicy": frozenset({"v1"}),
    "BaselineSummary": frozenset({"v1"}),
    "QuestionAdmission": frozenset({"v1"}),
    "Phase0Handoff": frozenset({"v1"}),
}


def canonical_json(payload: Any) -> str:
    """Serialize a JSON-compatible payload deterministically."""
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def content_hash(payload: Any) -> str:
    """Return a stable SHA-256 hash of a JSON-compatible payload."""
    digest = hashlib.sha256(canonical_json(payload).encode("utf-8"))
    return f"sha256:{digest.hexdigest()}"


class ArtifactEnvelope(StrictModel):
    """Immutable wrapper giving every artifact a stable version identity."""

    schema_name: str
    schema_version: str
    artifact_version: str
    content_sha256: str
    provenance: str
    created_at: datetime = Field(default_factory=utc_now)
    payload: dict[str, Any]

    def verify(self) -> None:
        """Validate schema-version support and payload-hash integrity.

        Raises:
            CompatibilityError: when the schema version is unsupported.
            ValueError: when the recorded hash does not match the payload.
        """
        supported = SUPPORTED_SCHEMA_VERSIONS.get(self.schema_name)
        if supported is None or self.schema_version not in supported:
            raise CompatibilityError(f"unsupported schema {self.schema_name}@{self.schema_version}")
        expected = content_hash(self.payload)
        if expected != self.content_sha256:
            raise ValueError("artifact content hash mismatch")


def build_envelope(
    *,
    schema_name: str,
    schema_version: str,
    artifact_version: str,
    provenance: str,
    payload: dict[str, Any],
    created_at: datetime | None = None,
) -> ArtifactEnvelope:
    """Construct a verified envelope with a computed content hash."""
    supported = SUPPORTED_SCHEMA_VERSIONS.get(schema_name)
    if supported is None or schema_version not in supported:
        raise CompatibilityError(f"unsupported schema {schema_name}@{schema_version}")
    return ArtifactEnvelope(
        schema_name=schema_name,
        schema_version=schema_version,
        artifact_version=artifact_version,
        content_sha256=content_hash(payload),
        provenance=provenance,
        created_at=created_at if created_at is not None else utc_now(),
        payload=payload,
    )
