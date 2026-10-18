"""Durable UI support: curriculum, content progress, notes, and resume state.

Streamlit treats `st.session_state` as a cache only; these use cases persist
meaningful progress through SQLite so a rerun or refresh never loses it.
"""

from __future__ import annotations

import json
from enum import StrEnum

from study_core.common import StrictModel
from study_core.db import DbConnection, immediate_transaction
from study_core.ports import Clock


class ContentStatus(StrEnum):
    """Progress status of a curriculum item for a learner."""

    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETE = "complete"


class CurriculumItem(StrictModel):
    """One lesson or lab node in the curriculum rail."""

    item_id: str
    item_type: str
    title: str
    display_order: int
    objective_ids: tuple[str, ...]
    prerequisites: tuple[str, ...]
    content_ref: str | None


class ResumeState(StrictModel):
    """Where the learner should resume."""

    view: str
    entity_id: str | None
    position: int


class UiStateService:
    """Durable curriculum, progress, notes, and resume operations."""

    def __init__(self, conn: DbConnection, clock: Clock) -> None:
        self._conn = conn
        self._clock = clock

    def list_curriculum(self) -> tuple[CurriculumItem, ...]:
        """Return curriculum items ordered for display."""
        rows = self._conn.execute(
            "SELECT item_id, item_type, title, display_order, objective_ids, prerequisites, "
            "content_ref FROM curriculum_items ORDER BY display_order ASC, item_id ASC"
        ).fetchall()
        return tuple(
            CurriculumItem(
                item_id=str(r["item_id"]),
                item_type=str(r["item_type"]),
                title=str(r["title"]),
                display_order=int(r["display_order"]),
                objective_ids=tuple(json.loads(r["objective_ids"])),
                prerequisites=tuple(json.loads(r["prerequisites"])),
                content_ref=r["content_ref"],
            )
            for r in rows
        )

    def content_status(self, learner_id: str) -> dict[str, ContentStatus]:
        """Return each curriculum item's status for a learner."""
        rows = self._conn.execute(
            "SELECT item_id, status FROM learner_content_state WHERE learner_id = ?",
            (learner_id,),
        ).fetchall()
        return {str(r["item_id"]): ContentStatus(str(r["status"])) for r in rows}

    def set_content_status(
        self, *, learner_id: str, item_id: str, status: ContentStatus, position: int
    ) -> None:
        """Persist a content item's status and position before showing success."""
        now = self._clock.now_utc().isoformat()
        with immediate_transaction(self._conn):
            self._conn.execute(
                "INSERT INTO learner_content_state (learner_id, item_id, status, position, "
                "updated_at) VALUES (?, ?, ?, ?, ?) "
                "ON CONFLICT(learner_id, item_id) DO UPDATE SET status = ?, position = ?, "
                "updated_at = ?",
                (learner_id, item_id, status.value, position, now, status.value, position, now),
            )

    def get_note(self, *, learner_id: str, context: str) -> str:
        """Return the saved note for a context, or empty string."""
        row = self._conn.execute(
            "SELECT text FROM learner_notes WHERE learner_id = ? AND context = ?",
            (learner_id, context),
        ).fetchone()
        return str(row["text"]) if row else ""

    def save_note(self, *, learner_id: str, context: str, text: str) -> None:
        """Persist a note for a context."""
        now = self._clock.now_utc().isoformat()
        with immediate_transaction(self._conn):
            self._conn.execute(
                "INSERT INTO learner_notes (learner_id, context, text, updated_at) "
                "VALUES (?, ?, ?, ?) ON CONFLICT(learner_id, context) "
                "DO UPDATE SET text = ?, updated_at = ?",
                (learner_id, context, text, now, text, now),
            )

    def get_resume(self, learner_id: str) -> ResumeState | None:
        """Return the learner's resume state, if any."""
        row = self._conn.execute(
            "SELECT view, entity_id, position FROM ui_resume_state WHERE learner_id = ?",
            (learner_id,),
        ).fetchone()
        if row is None:
            return None
        return ResumeState(
            view=str(row["view"]),
            entity_id=row["entity_id"],
            position=int(row["position"]),
        )

    def set_resume(
        self, *, learner_id: str, view: str, entity_id: str | None, position: int
    ) -> None:
        """Persist resume state before navigation success is shown."""
        now = self._clock.now_utc().isoformat()
        with immediate_transaction(self._conn):
            self._conn.execute(
                "INSERT INTO ui_resume_state (learner_id, view, entity_id, position, updated_at) "
                "VALUES (?, ?, ?, ?, ?) ON CONFLICT(learner_id) "
                "DO UPDATE SET view = ?, entity_id = ?, position = ?, updated_at = ?",
                (learner_id, view, entity_id, position, now, view, entity_id, position, now),
            )
