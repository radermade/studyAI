"""Typed, non-secret settings for the local study core.

Settings resolve from explicit arguments and environment variables with
local-first defaults. No secret is read or stored here.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

_DEFAULT_DB_PATH = Path("data") / "study.db"
_DEFAULT_BUSY_TIMEOUT_MS = 5000
_DEFAULT_SEARCH_LIMIT = 20
_DEFAULT_MAX_SEARCH_LIMIT = 100


@dataclass(frozen=True)
class Settings:
    """Resolved runtime settings for the study core."""

    database_path: Path
    busy_timeout_ms: int
    default_search_limit: int
    max_search_limit: int

    @staticmethod
    def from_env(env: dict[str, str] | None = None) -> Settings:
        """Build settings from environment variables with local-first defaults."""
        source = os.environ if env is None else env
        db_path = source.get("STUDYAI_DB_PATH")
        return Settings(
            database_path=Path(db_path) if db_path else _DEFAULT_DB_PATH,
            busy_timeout_ms=int(source.get("STUDYAI_BUSY_TIMEOUT_MS", _DEFAULT_BUSY_TIMEOUT_MS)),
            default_search_limit=int(source.get("STUDYAI_SEARCH_LIMIT", _DEFAULT_SEARCH_LIMIT)),
            max_search_limit=int(source.get("STUDYAI_MAX_SEARCH_LIMIT", _DEFAULT_MAX_SEARCH_LIMIT)),
        )
