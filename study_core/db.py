"""SQLite connection factory and numbered forward-migration runner.

Every connection enables foreign keys (verified), requests WAL mode, and sets a
bounded busy timeout. Migrations are immutable numbered SQL files applied once
in order inside transactions, with checksum drift refused.
"""

from __future__ import annotations

import hashlib
import sqlite3
import threading
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Protocol

from study_core.errors import PersistenceError

MIGRATIONS_DIR = Path("migrations")


class DbConnection(Protocol):
    """Minimal connection surface used by the study services and migrations."""

    def execute(self, sql: str, parameters: Any = ...) -> sqlite3.Cursor: ...

    def executescript(self, sql: str) -> sqlite3.Cursor: ...

    def close(self) -> None: ...


class LockedConnection:
    """A thread-safe proxy over a SQLite connection.

    Streamlit may run script reruns on different worker threads. This proxy
    permits cross-thread use (`check_same_thread=False`) while serializing all
    access through a single lock, so operations never interleave. It exposes
    only the methods the study services and migration runner use.
    """

    def __init__(self, conn: sqlite3.Connection) -> None:
        self._conn = conn
        self._lock = threading.RLock()

    def execute(self, sql: str, parameters: Any = ()) -> sqlite3.Cursor:
        with self._lock:
            return self._conn.execute(sql, parameters)

    def executescript(self, sql: str) -> sqlite3.Cursor:
        with self._lock:
            return self._conn.executescript(sql)

    def close(self) -> None:
        with self._lock:
            self._conn.close()


def connect(
    database_path: Path,
    busy_timeout_ms: int,
    *,
    allow_cross_thread: bool = False,
) -> DbConnection:
    """Open a SQLite connection with foreign keys, WAL, and a busy timeout.

    Args:
        allow_cross_thread: when True, allow the connection to be used from
            threads other than the one that created it. Streamlit reruns the
            script on different worker threads, so the single-user app sets
            this and serializes access with a lock. Defaults to False for the
            strict single-thread behavior used by the CLI and tests.

    Raises:
        PersistenceError: when foreign-key enforcement cannot be verified.
    """
    database_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(
        database_path, isolation_level=None, check_same_thread=not allow_cross_thread
    )
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    conn.execute(f"PRAGMA busy_timeout = {int(busy_timeout_ms)}")
    enabled = conn.execute("PRAGMA foreign_keys").fetchone()
    if enabled is None or int(enabled[0]) != 1:
        conn.close()
        raise PersistenceError("foreign keys could not be enabled on the connection")
    return LockedConnection(conn) if allow_cross_thread else conn


@contextmanager
def immediate_transaction(conn: DbConnection) -> Iterator[DbConnection]:
    """Run a short write transaction using BEGIN IMMEDIATE.

    Commits on success and rolls back on any exception. No external (AWS or
    model) call belongs inside this block.
    """
    # Hold the connection lock (if any) across the whole transaction so no other
    # thread can interleave between BEGIN and COMMIT.
    lock = getattr(conn, "_lock", None)
    if lock is not None:
        lock.acquire()
    try:
        conn.execute("BEGIN IMMEDIATE")
        try:
            yield conn
        except BaseException:
            conn.execute("ROLLBACK")
            raise
        else:
            conn.execute("COMMIT")
    finally:
        if lock is not None:
            lock.release()


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


def _ensure_migrations_table(conn: DbConnection) -> None:
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
    conn: DbConnection,
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
