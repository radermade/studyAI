"""SQLite connection factory and numbered forward-migration runner.

Every connection enables foreign keys (verified), requests WAL mode, and sets a
bounded busy timeout. Migrations are immutable numbered SQL files applied once
in order inside transactions, with checksum drift refused.
"""

from __future__ import annotations

import hashlib
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from study_core.errors import PersistenceError

MIGRATIONS_DIR = Path("migrations")


def connect(database_path: Path, busy_timeout_ms: int) -> sqlite3.Connection:
    """Open a SQLite connection with foreign keys, WAL, and a busy timeout.

    Raises:
        PersistenceError: when foreign-key enforcement cannot be verified.
    """
    database_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(database_path, isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    conn.execute(f"PRAGMA busy_timeout = {int(busy_timeout_ms)}")
    enabled = conn.execute("PRAGMA foreign_keys").fetchone()
    if enabled is None or int(enabled[0]) != 1:
        conn.close()
        raise PersistenceError("foreign keys could not be enabled on the connection")
    return conn


@contextmanager
def immediate_transaction(conn: sqlite3.Connection) -> Iterator[sqlite3.Connection]:
    """Run a short write transaction using BEGIN IMMEDIATE.

    Commits on success and rolls back on any exception. No external (AWS or
    model) call belongs inside this block.
    """
    conn.execute("BEGIN IMMEDIATE")
    try:
        yield conn
    except BaseException:
        conn.execute("ROLLBACK")
        raise
    else:
        conn.execute("COMMIT")


def _checksum(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def _discover_migrations(migrations_dir: Path) -> list[tuple[int, Path]]:
    found: list[tuple[int, Path]] = []
    for path in sorted(migrations_dir.glob("*.sql")):
        prefix = path.name.split("_", 1)[0]
        if not prefix.isdigit():
            raise PersistenceError(f"migration {path.name} has no numeric prefix")
        found.append((int(prefix), path))
    found.sort(key=lambda item: item[0])
    return found


def _ensure_migrations_table(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS schema_migrations (
            version INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            checksum TEXT NOT NULL,
            applied_at TEXT NOT NULL
        )
        """
    )


def apply_migrations(
    conn: sqlite3.Connection,
    migrations_dir: Path = MIGRATIONS_DIR,
    *,
    now_iso: str,
) -> list[int]:
    """Apply pending numbered migrations in order; return applied versions.

    Raises:
        PersistenceError: on missing numeric prefix, checksum drift of an
        already-applied migration, or a failed migration.
    """
    _ensure_migrations_table(conn)
    applied_rows = conn.execute("SELECT version, checksum FROM schema_migrations").fetchall()
    applied: dict[int, str] = {int(row["version"]): str(row["checksum"]) for row in applied_rows}

    newly_applied: list[int] = []
    for version, path in _discover_migrations(migrations_dir):
        sql = path.read_text(encoding="utf-8")
        checksum = _checksum(sql)
        if version in applied:
            if applied[version] != checksum:
                raise PersistenceError(
                    f"migration {version} checksum drift; migrations are immutable"
                )
            continue
        # executescript() manages its own transaction boundaries, so apply the
        # DDL first, then record the version. If the DDL fails, the version is
        # never recorded and the migration can be retried after a fix.
        try:
            conn.executescript(sql)
            conn.execute(
                "INSERT INTO schema_migrations (version, name, checksum, applied_at) "
                "VALUES (?, ?, ?, ?)",
                (version, path.name, checksum, now_iso),
            )
        except sqlite3.Error as exc:
            raise PersistenceError(f"migration {version} failed: {exc}") from exc
        newly_applied.append(version)
    return newly_applied
