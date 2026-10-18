"""Tests for the connection factory and migration runner."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest
from study_core.db import apply_migrations, connect, immediate_transaction
from study_core.errors import PersistenceError

_NOW = datetime(2026, 1, 1, tzinfo=UTC).isoformat()


def test_foreign_keys_enabled(tmp_path: Path) -> None:
    conn = connect(tmp_path / "db.sqlite", 5000)
    assert int(conn.execute("PRAGMA foreign_keys").fetchone()[0]) == 1
    conn.close()


def test_migrations_apply_once_and_are_idempotent(tmp_path: Path) -> None:
    conn = connect(tmp_path / "db.sqlite", 5000)
    first = apply_migrations(conn, now_iso=_NOW)
    second = apply_migrations(conn, now_iso=_NOW)
    # All numbered migrations apply in order on the first run; the second is a no-op.
    assert first == sorted(first)
    assert first[0] == 1
    assert second == []
    conn.close()


def test_checksum_drift_is_refused(tmp_path: Path) -> None:
    conn = connect(tmp_path / "db.sqlite", 5000)
    apply_migrations(conn, now_iso=_NOW)
    conn.execute("UPDATE schema_migrations SET checksum = 'sha256:tampered' WHERE version = 1")
    with pytest.raises(PersistenceError):
        apply_migrations(conn, now_iso=_NOW)
    conn.close()


def test_immediate_transaction_rolls_back_on_error(tmp_path: Path) -> None:
    conn = connect(tmp_path / "db.sqlite", 5000)
    apply_migrations(conn, now_iso=_NOW)
    conn.execute("INSERT INTO blueprints (blueprint_version, created_at) VALUES ('v', ?)", (_NOW,))
    with pytest.raises(RuntimeError), immediate_transaction(conn):
        conn.execute(
            "INSERT INTO blueprints (blueprint_version, created_at) VALUES ('w', ?)",
            (_NOW,),
        )
        raise RuntimeError("boom")
    count = conn.execute("SELECT COUNT(*) FROM blueprints").fetchone()[0]
    assert count == 1
    conn.close()
