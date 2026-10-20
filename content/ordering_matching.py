"""Aggregated ordering and matching question banks across all domains.

Each domain's ordering/matching questions live in their own
``content/domainN_ordering_matching.py`` module; this module concatenates them
into one list consumed by the ingestion seed.
"""

from __future__ import annotations

from typing import Any

from content.domain1_ordering_matching import QUESTIONS as _D1
from content.domain2_ordering_matching import QUESTIONS as _D2
from content.domain3_ordering_matching import QUESTIONS as _D3
from content.domain4_ordering_matching import QUESTIONS as _D4
from content.domain5_ordering_matching import QUESTIONS as _D5

ORDERING_MATCHING_QUESTIONS: list[dict[str, Any]] = [*_D1, *_D2, *_D3, *_D4, *_D5]


def question_count() -> int:
    """Return the total number of authored ordering/matching questions."""
    return len(ORDERING_MATCHING_QUESTIONS)
