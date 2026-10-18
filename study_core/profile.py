"""Learner profile contract.

Captures study constraints explicitly. Optional fields that the learner
declines are represented as explicit `None` rather than guessed defaults.
Never stores credentials, account secrets, or payment data.
"""

from __future__ import annotations

from datetime import date, datetime
from enum import StrEnum

from pydantic import Field, field_validator

from study_core.common import StrictModel, ensure_utc


class AwsExperience(StrEnum):
    """Self-reported AWS experience level."""

    NONE = "none"
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class AccountType(StrEnum):
    """Type of AWS account available for hands-on labs."""

    NONE = "none"
    PERSONAL = "personal"
    SANDBOX = "sandbox"
    ORGANIZATION = "organization"


# Secret-shaped field names that must never appear in a profile.
_FORBIDDEN_FIELDS = frozenset(
    {
        "aws_access_key_id",
        "aws_secret_access_key",
        "session_token",
        "password",
        "card_number",
    }
)


class LearnerProfile(StrictModel):
    """Versioned, non-secret learner constraints."""

    learner_id: str
    exam_date: date | None = None
    exam_date_undecided: bool = True
    weekly_hours: int = Field(gt=0, le=168)
    experience: AwsExperience
    target_region: str
    account_type: AccountType
    lab_budget_usd: float = Field(ge=0.0)
    updated_at: datetime
    profile_version: str

    @field_validator("updated_at")
    @classmethod
    def _utc(cls, value: datetime) -> datetime:
        return ensure_utc(value)

    @field_validator("target_region")
    @classmethod
    def _region_shape(cls, value: str) -> str:
        # A light structural check; e.g. us-east-1, eu-west-2.
        parts = value.split("-")
        if len(parts) < 3 or not parts[-1].isdigit():
            raise ValueError(f"malformed region: {value}")
        return value

    @field_validator("exam_date")
    @classmethod
    def _not_in_past(cls, value: date | None) -> date | None:
        if value is not None and value < date.today():
            raise ValueError("exam date must not be in the past")
        return value
