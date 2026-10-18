"""Phase 1 command: ingest the Phase 0 handoff and seed content into SQLite.

Usage:
    python -m scripts.phase1 ingest    # build handoff, migrate, and ingest

Writes the study database under the gitignored `data/` directory.
"""

from __future__ import annotations

import sys

from content.aip_c01 import BLUEPRINT_VERSION
from content.phase1_seed import (
    build_answer_material,
    build_content_units,
    build_question_options,
)
from study_core.common import utc_now
from study_core.db import apply_migrations, connect
from study_core.handoff import build_handoff, evaluate_phase0
from study_core.ingestion import ingest_handoff
from study_core.settings import Settings

from scripts.phase0 import assemble_inputs


def command_ingest() -> int:
    """Build an accepted Phase 0 handoff and ingest it into the study DB."""
    inputs = assemble_inputs()
    report = evaluate_phase0(inputs)
    if not report.accepted:
        print("Phase 0 gate not accepted; cannot ingest.", file=sys.stderr)
        return 1
    handoff = build_handoff(inputs, report)

    settings = Settings.from_env()
    now_iso = utc_now().isoformat()
    conn = connect(settings.database_path, settings.busy_timeout_ms)
    try:
        apply_migrations(conn, now_iso=now_iso)
        ingest_handoff(
            conn,
            handoff,
            now_iso=now_iso,
            answer_material=build_answer_material(),
            question_options=build_question_options(),
            content_units=build_content_units(),
        )
    finally:
        conn.close()
    print(f"Ingested blueprint {BLUEPRINT_VERSION} into {settings.database_path}")
    return 0


def main(argv: list[str]) -> int:
    """CLI entry point."""
    if len(argv) != 1 or argv[0] != "ingest":
        print("usage: python -m scripts.phase1 ingest", file=sys.stderr)
        return 2
    return command_ingest()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
