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
