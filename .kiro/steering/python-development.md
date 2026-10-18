---
inclusion: fileMatch
fileMatchPattern: "**/*.py"
---

# Python Development Steering

## Code style

- Target Python 3.12.
- Add complete type annotations to public functions, methods, dataclasses, and module-level collections.
- Prefer small modules organized by capability, not generic `utils.py` files.
- Use `pathlib.Path`, timezone-aware UTC datetimes, enums for closed state sets, and explicit dataclasses or Pydantic models for structured data.
- Use Ruff-compatible formatting and imports.
- Write docstrings for public contracts and non-obvious invariants; do not narrate straightforward code.

## Layering

- Keep business rules in `study_core`, independent of Streamlit, MCP, and boto3.
- Keep Streamlit pages declarative: gather input, call a use case, render the result.
- Keep MCP handlers thin: validate input, invoke one use case, map known errors, return a typed result.
- Hide SQLite and AWS details behind narrow repository or gateway protocols.
- Pass dependencies explicitly; avoid mutable module-level clients, connections, and session state.

## Models and validation

- Use Pydantic models at untrusted boundaries and dataclasses/value objects inside the core where appropriate.
- Reject unknown state transitions and malformed objective IDs rather than silently coercing them.
- Represent persistence and verification state explicitly; never infer `verified` from a truthy string or UI click.
- Keep unanswered question DTOs structurally incapable of carrying answer keys or rubrics.

## Errors and logging

- Define domain-specific exceptions for validation, not-found, conflict, authorization, external-service, and persistence failures.
- Catch exceptions only where the code can recover, add context, or translate layer boundaries.
- Do not use bare `except` or silently return empty results after failures.
- Use structured logging with event names and non-sensitive identifiers.
- Redact credentials, tokens, PII, full private prompts, answer keys, and sensitive retrieved text.
- User-facing messages explain recovery without leaking internals.

## Persistence

- Use parameterized SQL only.
- Enable SQLite foreign keys on each connection.
- Keep writes transactional and short.
- Make event-like writes idempotent using caller-provided IDs or stable uniqueness constraints.
- Treat migration files as immutable after use.
- Do not hold a SQLite transaction open across an AWS or model call.

## AWS code

- Construct boto3 sessions through the standard credential chain and explicit profile/Region parameters.
- Reuse clients within a bounded application session, not as import-time side effects.
- Use botocore retry configuration deliberately and distinguish throttling from authorization and validation errors.
- Keep permitted service actions explicit in code and documentation.
- Validators are read-only unless the user approves a separately scoped implementation task.

## Streamlit state

- Treat `st.session_state` as a view/session cache, never durable learner state.
- Persist meaningful progress synchronously through `study_core` before rendering success.
- Give widgets stable keys derived from stable entity IDs.
- Avoid expensive I/O during module import or every rerun; cache only safe, non-user-specific immutable resources.
- Never cache credentials, boto3 responses containing private data, or answer keys in client-visible state.

## Functions and concurrency

- Prefer synchronous code for the MVP because Streamlit, SQLite, and boto3 are primarily synchronous in this design.
- Do not introduce async wrappers that immediately call blocking code.
- Bound retries, loops, question generation, and external calls with timeouts or attempt limits.
- Keep pure scoring and scheduling functions deterministic by injecting the clock and random source.
