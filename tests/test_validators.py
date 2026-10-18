"""Tests for the read-only AWS validator allowlist and fake validator."""

from __future__ import annotations

import pytest
from study_aws.validators import VALIDATOR_ALLOWLIST, AwsReadOnlyValidator, FakeValidator
from study_core.errors import SecurityPolicyError
from study_core.lab_models import EvidenceKind, ValidationRequest


def test_allowlist_is_read_only() -> None:
    for _validator_id, (_service, action) in VALIDATOR_ALLOWLIST.items():
        assert action.startswith(("describe_", "list_", "get_"))


def test_unknown_validator_refused() -> None:
    validator = AwsReadOnlyValidator(factory=_FailFactory())
    with pytest.raises(SecurityPolicyError):
        validator.validate(ValidationRequest(validator_id="delete-everything", region="us-east-1"))


def test_fake_validator_returns_requested_kind() -> None:
    fake = FakeValidator(EvidenceKind.RESOURCE_ABSENT)
    evidence = fake.validate(ValidationRequest(validator_id="s3-bucket-absent", region="us-east-1"))
    assert evidence.kind == EvidenceKind.RESOURCE_ABSENT


def test_fake_validator_still_enforces_allowlist() -> None:
    fake = FakeValidator(EvidenceKind.RESOURCE_PRESENT)
    with pytest.raises(SecurityPolicyError):
        fake.validate(ValidationRequest(validator_id="not-allowed", region="us-east-1"))


def test_s3_bucket_present_interprets_buckets() -> None:
    validator = AwsReadOnlyValidator(factory=_StubS3Factory(buckets=True))
    evidence = validator.validate(
        ValidationRequest(validator_id="s3-bucket-present", region="us-east-1")
    )
    assert evidence.kind == EvidenceKind.RESOURCE_PRESENT


def test_s3_bucket_absent_interprets_no_buckets() -> None:
    validator = AwsReadOnlyValidator(factory=_StubS3Factory(buckets=False))
    evidence = validator.validate(
        ValidationRequest(validator_id="s3-bucket-absent", region="us-east-1")
    )
    assert evidence.kind == EvidenceKind.RESOURCE_ABSENT


class _FailFactory:
    def client(self, service: str, region: str, profile_name: str | None) -> object:
        raise AssertionError("client must not be built for a disallowed validator")


class _StubS3Client:
    def __init__(self, buckets: bool) -> None:
        self._buckets = buckets

    def list_buckets(self) -> dict[str, object]:
        return {"Buckets": [{"Name": "b"}] if self._buckets else []}


class _StubS3Factory:
    def __init__(self, buckets: bool) -> None:
        self._buckets = buckets

    def client(self, service: str, region: str, profile_name: str | None) -> _StubS3Client:
        assert service == "s3"
        return _StubS3Client(self._buckets)
