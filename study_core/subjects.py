"""Subject (study blueprint) definitions and the active-subject resolver.

A :class:`Subject` owns the facts that were previously hard-coded for AIP-C01:
the objective-ID shape, the per-domain task inventory, and the official domain
weights. Promoting these to a first-class entity lets the same study engine
drive other certifications or topics without changing core logic.

One subject is active at a time, resolved by :func:`active_subject` (default
AIP-C01, overridable via ``STUDYAI_SUBJECT``). There is intentionally no
subject-selection UI yet; this module is the seam a future selector would use.

This module is pure (stdlib only) and imported by ``study_core.common``, which
re-exports thin, backward-compatible delegations so existing call sites keep
working unchanged.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Subject:
    """One study subject: its ID shape, task inventory, and domain weights.

    Attributes:
        subject_id: Stable short identifier (e.g. ``"aip-c01"``).
        display_name: Human-readable subject name shown in the UI.
        blueprint_version: Versioned blueprint tag (e.g. ``"AIP-C01-2026-10"``).
        id_prefix: Objective-ID prefix before the domain/task numbers
            (e.g. ``"AIP"`` for IDs like ``AIP-1.2``).
        domain_task_counts: Map of domain number -> number of tasks in it.
        domain_weights: Map of domain number -> official weight percent
            (must total 100).
        domain_titles: Human-readable title per domain number.
    """

    subject_id: str
    display_name: str
    blueprint_version: str
    id_prefix: str
    domain_task_counts: dict[int, int]
    domain_weights: dict[int, int]
    domain_titles: dict[int, str] = field(default_factory=dict)

    @property
    def domain_ids(self) -> tuple[int, ...]:
        """The subject's domain numbers in ascending order."""
        return tuple(sorted(self.domain_task_counts))

    def __post_init__(self) -> None:
        if sum(self.domain_weights.values()) != 100:
            raise ValueError(f"domain weights for {self.subject_id} must total 100")
        if set(self.domain_task_counts) != set(self.domain_weights):
            raise ValueError(
                f"domain sets disagree for {self.subject_id}: "
                f"{sorted(self.domain_task_counts)} vs {sorted(self.domain_weights)}"
            )

    @property
    def task_id_pattern(self) -> re.Pattern[str]:
        """Regex matching this subject's objective IDs: ``<prefix>-<domain>.<task>``.

        Domain and task are single digits 1-9, validated in detail by
        :meth:`is_valid_task_id` against the actual per-domain counts.
        """
        prefix = re.escape(self.id_prefix)
        return re.compile(rf"^{prefix}-([1-9])\.([1-9])$")

    @property
    def all_task_ids(self) -> tuple[str, ...]:
        """Canonical ordered list of every task ID in this subject."""
        return tuple(
            f"{self.id_prefix}-{domain}.{task}"
            for domain in sorted(self.domain_task_counts)
            for task in range(1, self.domain_task_counts[domain] + 1)
        )

    def is_valid_task_id(self, value: str) -> bool:
        """Return True when ``value`` is a real task ID in this subject."""
        match = self.task_id_pattern.match(value)
        if match is None:
            return False
        domain = int(match.group(1))
        task = int(match.group(2))
        max_task = self.domain_task_counts.get(domain)
        return max_task is not None and 1 <= task <= max_task

    def domain_of(self, task_id: str) -> int:
        """Return the domain number for a valid task ID of this subject.

        Raises:
            ValueError: when ``task_id`` is not a valid task ID of this subject.
        """
        match = self.task_id_pattern.match(task_id)
        if match is None or not self.is_valid_task_id(task_id):
            raise ValueError(f"invalid task id: {task_id!r}")
        return int(match.group(1))


# The one subject shipped today. Its facts previously lived as module-level
# constants in study_core.common; they now originate here.
AIP_C01 = Subject(
    subject_id="aip-c01",
    display_name="AWS Certified Generative AI Developer (AIP-C01)",
    blueprint_version="AIP-C01-2026-10",
    id_prefix="AIP",
    domain_task_counts={1: 6, 2: 5, 3: 4, 4: 3, 5: 2},
    domain_weights={1: 31, 2: 26, 3: 20, 4: 12, 5: 11},
    domain_titles={
        1: "Foundation Model Integration, Data Management, and Compliance",
        2: "Implementation and Integration",
        3: "AI Safety, Security, and Governance",
        4: "Operational Efficiency and Optimization for GenAI Applications",
        5: "Testing, Validation, and Troubleshooting",
    },
)

# Registry of known subjects, keyed by subject_id. Add subjects here (and author
# their content under content/) to make them selectable later.
_SUBJECTS: dict[str, Subject] = {AIP_C01.subject_id: AIP_C01}

_DEFAULT_SUBJECT_ID = AIP_C01.subject_id


def get_subject(subject_id: str) -> Subject:
    """Return a registered subject by ID, or raise if unknown."""
    try:
        return _SUBJECTS[subject_id]
    except KeyError:
        known = ", ".join(sorted(_SUBJECTS))
        raise ValueError(f"unknown subject {subject_id!r}; known: {known}") from None


def active_subject(env: dict[str, str] | None = None) -> Subject:
    """Return the active study subject.

    Resolves from ``STUDYAI_SUBJECT`` when set, else the default (AIP-C01).
    This is the single seam a future subject-selection screen would drive; the
    engine reads the active subject rather than hard-coding one.
    """
    source = os.environ if env is None else env
    return get_subject(source.get("STUDYAI_SUBJECT", _DEFAULT_SUBJECT_ID))
