"""Read-only AWS validators plus a deterministic fake for tests/offline use.

The allowlist maps each validator ID to one read-only boto3 (service, action).
Any attempt to use an action outside the allowlist is refused before a call is
made. Results are sanitized to a presence/absence signal and a short summary.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Protocol

from study_core.common import utc_now
from study_core.errors import SecurityPolicyError
from study_core.lab_models import (
    EvidenceKind,
    ValidationEvidence,
    ValidationRequest,
)

# validator_id -> (service, read-only action). Actions are Describe/List/Get only.
VALIDATOR_ALLOWLIST: dict[str, tuple[str, str]] = {
    "bedrock-models-present": ("bedrock", "list_foundation_models"),
    "s3-bucket-present": ("s3", "list_buckets"),
    "s3-bucket-absent": ("s3", "list_buckets"),
    "lambda-function-present": ("lambda", "list_functions"),
    "lambda-function-absent": ("lambda", "list_functions"),
    "apigateway-api-present": ("apigateway", "get_rest_apis"),
    "apigateway-api-absent": ("apigateway", "get_rest_apis"),
}

_READONLY_PREFIXES = ("describe_", "list_", "get_")


class BotoClientFactory(Protocol):
    """Builds a boto3 client for a service and region (standard credentials)."""

    def client(self, service: str, region: str, profile_name: str | None) -> Any: ...


class DefaultBotoClientFactory:
    """Creates boto3 clients via a named profile or the standard chain."""

    def client(self, service: str, region: str, profile_name: str | None) -> Any:
        import boto3  # imported lazily so offline/test paths need no AWS

        session = boto3.Session(profile_name=profile_name) if profile_name else boto3.Session()
        return session.client(service, region_name=region)


def _assert_read_only(validator_id: str) -> tuple[str, str]:
    mapping = VALIDATOR_ALLOWLIST.get(validator_id)
    if mapping is None:
        raise SecurityPolicyError(f"validator {validator_id} is not allowlisted")
    _service, action = mapping
    if not action.startswith(_READONLY_PREFIXES):
        raise SecurityPolicyError(f"validator {validator_id} action is not read-only")
    return mapping


class AwsReadOnlyValidator:
    """Executes exactly one allowlisted read-only call and sanitizes the result."""

    def __init__(self, factory: BotoClientFactory | None = None) -> None:
        self._factory = factory if factory is not None else DefaultBotoClientFactory()

    def validate(self, request: ValidationRequest) -> ValidationEvidence:
        """Call the allowlisted read-only action and return sanitized evidence."""
        service, action = _assert_read_only(request.validator_id)
        client = self._factory.client(service, request.region, request.profile_name)
        method = getattr(client, action)
        response = method()
        present = _interpret_presence(request.validator_id, response)
        kind = EvidenceKind.RESOURCE_PRESENT if present else EvidenceKind.RESOURCE_ABSENT
        return ValidationEvidence(
            attempt_id="",  # assigned by the caller before persistence
            kind=kind,
            observed_at=utc_now(),
            summary=f"{service}:{action} observed {'present' if present else 'absent'}",
        )


def _interpret_presence(validator_id: str, response: dict[str, Any]) -> bool:
    """Map a read-only response to a presence boolean without storing payloads."""
    if validator_id == "bedrock-models-present":
        return bool(response.get("modelSummaries"))
    if validator_id in ("s3-bucket-present", "s3-bucket-absent"):
        return bool(response.get("Buckets"))
    if validator_id in ("lambda-function-present", "lambda-function-absent"):
        return bool(response.get("Functions"))
    if validator_id in ("apigateway-api-present", "apigateway-api-absent"):
        return bool(response.get("items"))
    return False


class FakeValidator:
    """Deterministic validator for tests and offline runs."""

    def __init__(self, kind: EvidenceKind, *, now: datetime | None = None) -> None:
        self._kind = kind
        self._now = now

    def validate(self, request: ValidationRequest) -> ValidationEvidence:
        _assert_read_only(request.validator_id)
        return ValidationEvidence(
            attempt_id="",
            kind=self._kind,
            observed_at=self._now if self._now is not None else utc_now(),
            summary=f"fake:{request.validator_id}:{self._kind.value}",
        )
