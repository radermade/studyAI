# studyAI — AWS Certified Generative AI Developer (AIP-C01) study platform

Local-first study platform for the AWS Certified Generative AI Developer – Professional
(AIP-C01) exam. See `.kiro/roadmap/roadmap.md` and `.kiro/specs/` for the full design.

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

Runtime state (handoff artifacts, baseline responses) is written under `data/` and is
gitignored. Authored manifests and content live under `content/` and `labs/`.

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

The Streamlit workspace is focused on two things: **Grill** (get quizzed) and **Labs**
(hands-on AWS walkthroughs), with **Review** and **Progress** as the adaptive support
that makes grilling target your weak spots.

### 1. Ingest data (once)

```bash
uv run python -m scripts.phase1 ingest
```

### 2. Launch the workspace

```bash
uv run streamlit run app/main.py
```

Open the printed `Local URL` (default http://localhost:8501). What you can do:

- **Grill:** start a session and answer one real scenario question at a time with a
  confidence rating. After you submit, you see which option was correct, a rationale for
  every option (including why yours was right or wrong), a teaching explanation, and the
  source. Grading, misconceptions, and spaced reviews persist through `study_core`.
  Domain 1 (foundation models, RAG, prompts) has authored questions today; the other
  domains are being filled in.
- **Labs:** start the Bedrock model-comparison walkthrough, open the AWS Console in a new
  tab, run a read-only validator check, use the progressive hint ladder, and complete the
  lab. `Verified` requires validator evidence; `Cleaned up` requires proven absence — a
  click never establishes either.
- **Review:** committed due reviews (correct answers schedule future reviews).
- **Progress:** evidence-based, per-objective view (labeled an internal estimate).

Labs use read-only AWS validators (`study_aws`) via a named profile or the standard
credential chain. If AWS is unconfigured, lab checks show an explicit unavailable state
and every other view still works offline. Mock is a labeled placeholder until Phase 8.
