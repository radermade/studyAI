"""Atomic local artifact storage under the gitignored data boundary.

Writes go to a temporary file in the destination directory and are atomically
replaced only after the full payload is written, so a failed write never leaves
a partial or corrupt artifact and prior versions stay intact.
"""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Protocol

from study_core.artifacts import ArtifactEnvelope, canonical_json
from study_core.errors import PersistenceError


class ArtifactStore(Protocol):
    """Narrow protocol for reading and writing versioned artifact envelopes."""

    def write_version(self, envelope: ArtifactEnvelope) -> Path: ...

    def read_version(self, schema_name: str, artifact_version: str) -> ArtifactEnvelope: ...


class FileArtifactStore:
    """Filesystem artifact store rooted under a local (gitignored) directory."""

    def __init__(self, root: Path) -> None:
        self._root = root

    def _path_for(self, schema_name: str, artifact_version: str) -> Path:
        return self._root / schema_name / f"{artifact_version}.json"

    def write_version(self, envelope: ArtifactEnvelope) -> Path:
        """Atomically persist an envelope; prior versions are never mutated.

        Raises:
            PersistenceError: when the atomic write cannot complete.
        """
        envelope.verify()
        target = self._path_for(envelope.schema_name, envelope.artifact_version)
        target.parent.mkdir(parents=True, exist_ok=True)
        body = canonical_json(envelope.model_dump(mode="json"))
        try:
            fd, tmp_name = tempfile.mkstemp(dir=target.parent, suffix=".tmp")
            tmp_path = Path(tmp_name)
            try:
                with os.fdopen(fd, "w", encoding="utf-8") as handle:
                    handle.write(body)
                    handle.flush()
                    os.fsync(handle.fileno())
                os.replace(tmp_path, target)
            except OSError:
                tmp_path.unlink(missing_ok=True)
                raise
        except OSError as exc:
            raise PersistenceError(
                f"failed to write {envelope.schema_name}@{envelope.artifact_version}"
            ) from exc
        return target

    def read_version(self, schema_name: str, artifact_version: str) -> ArtifactEnvelope:
        """Load and verify a previously written envelope.

        Raises:
            PersistenceError: when the artifact is missing or unreadable.
        """
        path = self._path_for(schema_name, artifact_version)
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise PersistenceError(f"failed to read {schema_name}@{artifact_version}") from exc
        envelope = ArtifactEnvelope.model_validate(raw)
        envelope.verify()
        return envelope
