"""Thin local stdio MCP adapter over `study_core`.

Exposes exactly the six Phase 1 study tools. Handlers validate a typed request,
invoke one use case, and map known domain errors to stable error envelopes.
No SQL, filesystem, shell, or AWS capability is exposed.
"""
