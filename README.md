# studyAI — AWS Certified Generative AI Developer (AIP-C01) study platform

Local-first study platform for the AWS Certified Generative AI Developer – Professional
(AIP-C01) exam. See `.kiro/roadmap/roadmap.md` and `.kiro/specs/` for the full design.

## Quick start

Requires Python 3.12 (provisioned by `uv`) and [uv](https://docs.astral.sh/uv/).

```bash
# 1. Install dependencies
uv sync

# 2. Build the study database (runs migrations and ingests all content)
uv run python -m scripts.phase1 ingest

# 3. Launch the Streamlit workspace
uv run streamlit run app/main.py
```

Then open the printed `Local URL` (default http://localhost:8501).

### All run commands

```bash
# Dependencies
uv sync

# Quality gates
uv run ruff check .
uv run ruff format --check .
uv run mypy study_core study_mcp study_aws app
uv run pytest -q

# Build / rebuild the study database under data/ (gitignored)
uv run python -m scripts.phase1 ingest

# Launch the UI
uv run streamlit run app/main.py

# Local stdio MCP study server (JSON-RPC over stdin/stdout)
uv run python -m study_mcp.server

# Phase 0 handoff tooling (blueprint validation; usually not needed to run the app)
uv run python -m scripts.phase0 build
uv run python -m scripts.phase0 evaluate
```

> Note: `streamlit run` is a long-running process — run it in your own terminal
> rather than a non-interactive script. Stop any stale server before relaunching
> (e.g. `pkill -f "streamlit run"`).

### Studying a different subject (experimental)

The engine is subject-parameterized: the active study subject defaults to AIP-C01
and is resolved from the `STUDYAI_SUBJECT` environment variable. Only AIP-C01 ships
today, so this is a seam for future subjects rather than a user-facing selector.

## Phase 0 — Blueprint, Safety, and Baseline

Phase 0 produces validated, versioned inputs for the study platform rather than a runtime
application. Deterministic commands validate human-authored Markdown/YAML and
machine-readable manifests through Pydantic v2 boundary models, preserve provenance, and
emit a handoff consumed by Phase 1.

### Requirements

- Python 3.12 (provisioned automatically by `uv`)
- [uv](https://docs.astral.sh/uv/)

### Setup

```bash
uv sync
```

### Validation

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest
```

### Build and evaluate the Phase 0 handoff

```bash
uv run python -m scripts.phase0 build
uv run python -m scripts.phase0 evaluate
```

Runtime state (handoff artifacts, baseline responses, the SQLite database) is written
under `data/` and is gitignored. Authored manifests, questions, and labs live under
`content/`.

## Phase 1 — Local Study Core

Phase 1 is the durable, transport-independent study engine over SQLite plus a narrow
local stdio MCP server exposing six study tools.

### Ingest Phase 0 handoff and seed content into the study database

```bash
uv run python -m scripts.phase1 ingest
```

This builds the accepted Phase 0 handoff in memory, applies migrations, and ingests the
blueprint, sources, profile, safety policy, baseline, seed questions (with private answer
material), and searchable content into `data/study.db`.

### Run the local MCP study server

```bash
uv run python -m study_mcp.server
```

The server speaks JSON-RPC over stdio and exposes exactly: `start_session`,
`next_question`, `grade_and_record`, `get_due_reviews`, `get_progress`, and
`search_local_material`. No SQL, filesystem, shell, or AWS capability is exposed, and
unanswered questions never carry answer keys or rubrics.

## The workspace (the UI)

Launch with `uv run streamlit run app/main.py` (after ingesting once) and open the
printed `Local URL` (default http://localhost:8501). The workspace has five views:

- **Grill:** answer one real scenario question at a time with a confidence rating. After
  you submit, you see which option was correct, a rationale for every option, a teaching
  explanation, and the source. Grading, misconceptions, and spaced reviews persist
  through `study_core`. All five domains have authored questions (4 per objective).
- **Scored Session:** an exam-style run that mirrors the real AIP-C01 mechanics —
  officially weighted selection, no feedback until you submit, multiple-choice and
  all-or-nothing multiple-response grading, and a transparent 100–1000 scaled-score
  estimate (pass at 750, compensatory). A full session is 65 scored + 10 unscored = 75
  questions. Sessions are non-accumulating (a new one replaces the prior).
- **Labs:** 12 guided AWS Console walkthroughs with prediction prompts, a progressive
  hint ladder, read-only validator checks, reflections, and evidence-based cleanup.
  `Verified` requires validator evidence; `Cleaned up` requires proven absence — a click
  never establishes either.
- **Review:** scored-session misses first, then committed spaced reviews.
- **Progress:** an evidence-based readiness roll-up (whole-exam go/no-go) plus per-domain
  exit gates and per-objective accuracy, all labeled internal estimates — not AWS scores.

Labs use read-only AWS validators (`study_aws`) via a named profile or the standard
credential chain. If AWS is unconfigured, lab checks show an explicit unavailable state
and every other view still works offline.
