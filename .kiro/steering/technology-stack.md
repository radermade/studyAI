---
inclusion: always
---

# Technology and Architecture Steering

## Approved stack

Use the smallest local-first stack that supports the study loop:

- **Language:** Python 3.12.
- **Environment and packages:** `uv` with a committed lockfile. Pin exact dependency versions when dependencies are introduced.
- **Local UI:** Streamlit multipage application.
- **Study protocol:** FastMCP-based local stdio MCP server with explicit typed tools.
- **Persistence:** SQLite with foreign keys, WAL mode, transactional writes, and FTS5 for source search.
- **Validation models:** Pydantic v2 at UI, MCP, ingestion, and AWS boundaries.
- **AWS access:** boto3 using named profiles or the standard AWS credential chain; never custom credential storage.
- **Content:** Markdown plus YAML front matter for human-authored lessons and labs; normalized metadata in SQLite after ingestion.
- **Quality tools:** Ruff for formatting/linting, mypy for static type checking, and pytest when tests are explicitly part of an implementation task.
- **Diagrams:** Mermaid for maintainable architecture diagrams; do not embed proprietary diagrams.

Do not add a frontend framework, separate API server, hosted database, queue, container platform, or vector database until a measured requirement justifies it.

## Repository boundaries

Use these logical packages:

```text
app/                Streamlit pages and presentation components
study_core/         Domain logic with no Streamlit or MCP dependency
study_mcp/          Thin MCP transport adapter over study_core
study_aws/          Allowlisted read-only validators and AWS adapters
content/            Source-attributed lesson material
labs/               Lab definitions and checkpoint metadata
migrations/         Ordered SQLite migration files
scripts/            Deterministic ingestion and maintenance commands
data/               Local runtime state; gitignored
```

Dependency direction is inward:

```text
app ────────┐
study_mcp ──┼──> study_core <── study_aws adapters
scripts ────┘
```

`study_core` must not import Streamlit, FastMCP, or boto3. UI pages and MCP tools coordinate use cases but do not contain scheduling, grading, retrieval, or persistence rules.

## Data architecture

- SQLite is the source of truth for objectives, attempts, misconceptions, reviews, lab runs, and sessions.
- Use stable string IDs for exam objectives and authored content.
- Store timestamps in UTC ISO 8601 form and render local time only in the UI.
- Enable and test foreign-key enforcement for every connection.
- Wrap a graded attempt, misconception update, and review reschedule in one transaction.
- Use numbered forward migrations; never mutate a migration that may have run.
- Keep answer keys and grading rubrics separate from unanswered question payloads.
- Prefer FTS5 plus metadata filters. Add embeddings only after retrieval evaluation demonstrates a material gap.

## MCP architecture

MCP tools must be narrow use-case operations, not raw database or shell access. Use structured models for all inputs and outputs.

Initial allowlist:

- `start_session`
- `next_question`
- `grade_and_record`
- `get_due_reviews`
- `get_progress`
- `search_local_material`
- `start_lab`
- `record_lab_checkpoint`
- `complete_lab`

Requirements:

- Tool names are stable and verb-oriented.
- Mutating tools are idempotent where practical and accept a request/event ID.
- Errors distinguish validation, conflict, unavailable dependency, authorization, and internal failure.
- A tool never reports persistence or AWS verification success before the operation commits.
- Do not expose unrestricted SQL, filesystem, Python evaluation, AWS CLI, or shell tools.

## AWS integration

- Use the normal AWS credential provider chain and a dedicated named study profile.
- Prefer read-only `Describe`, `Get`, and `List` validation operations.
- Every validator has an explicit service/action allowlist and Region input.
- Do not create, update, or delete AWS resources unless a future task explicitly authorizes that capability and documents cost and reversibility.
- Do not log credentials, request signatures, secrets, full sensitive prompts, or retrieved private content.
- Apply study-session and ownership tags to resources created manually during labs where the service supports tags.
- Cleanup confirmation must verify resource absence or terminal deletion state; a clicked delete button is not proof.

## Dependency policy

- Prefer the Python standard library where it remains clear and maintainable.
- Use exact versions and commit `uv.lock`.
- Review unusual package names before installation to reduce typosquatting risk.
- Record why each non-development dependency is required.
- Do not add optional local LLM, embedding, speech, or OCR packages during the MVP.
- External services must not receive source code, credentials, learner history, or private AWS data without explicit user direction.

## Runtime and configuration

- Configuration comes from typed settings, environment variables, and non-secret checked-in defaults.
- Secrets and AWS credentials never appear in source, Markdown content, MCP JSON, SQLite, or `.env.example` values.
- Runtime data, recordings, screenshots, transcripts, and databases belong under `data/` and must be gitignored.
- The application must remain useful offline except for AWS documentation refresh and hands-on AWS labs.
- Long-running Streamlit processes are launched deliberately, not from save hooks.

## Validation expectations

For implementation tasks, run the smallest relevant non-watch checks available:

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy study_core study_mcp study_aws app
```

Run targeted tests only when the task includes or changes tested behavior. Never use watch mode in automated validation.
