"""Typed domain errors that are safe to render and never leak secrets."""

from __future__ import annotations

from collections.abc import Sequence

from study_core.common import ValidationIssue


class Phase0Error(Exception):
    """Base class for Phase 0 domain errors."""


class ContractValidationError(Phase0Error):
    """Malformed or incomplete input crossed a boundary."""

    def __init__(self, issues: Sequence[ValidationIssue]) -> None:
        self.issues: tuple[ValidationIssue, ...] = tuple(issues)
        summary = "; ".join(f"{issue.path}: {issue.message}" for issue in self.issues)
        super().__init__(summary or "contract validation failed")


class CompatibilityError(Phase0Error):
    """An artifact declared an unsupported schema version."""


class ConflictError(Phase0Error):
    """An immutable ID or version collision was detected."""


class SourceUnavailableError(Phase0Error):
    """A source refresh failed; prior verified metadata is preserved."""


class PersistenceError(Phase0Error):
    """An atomic artifact write failed; prior state is intact."""


class SecurityPolicyError(Phase0Error):
    """Secret-like data or a prohibited validator action was found."""
