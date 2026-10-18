"""Injected dependency ports: clock and random source.

Pure scoring and scheduling functions receive these so they stay deterministic
and testable. Phase 2 reuses the reserved lab and validator ports.
"""

from __future__ import annotations

from datetime import datetime
from typing import Protocol

from study_core.common import utc_now


class Clock(Protocol):
    """Supplies the current UTC instant."""

    def now_utc(self) -> datetime: ...


class RandomSource(Protocol):
    """Supplies a bounded deterministic choice for tie-breaking."""

    def choose_index(self, upper_bound: int) -> int: ...


class SystemClock:
    """Clock backed by the system wall clock in UTC."""

    def now_utc(self) -> datetime:
        return utc_now()


class SequenceRandom:
    """Deterministic RandomSource that always picks the first eligible item.

    Selection order is already deterministic by priority and stable sort; this
    default keeps tie-breaking reproducible without external entropy.
    """

    def choose_index(self, upper_bound: int) -> int:
        if upper_bound <= 0:
            raise ValueError("upper_bound must be positive")
        return 0


class SystemRandom:
    """A real random source for scored-session variety.

    Uses `random.Random`; pass a seed for reproducibility in tests.
    """

    def __init__(self, seed: int | None = None) -> None:
        import random

        self._rng = random.Random(seed)

    def choose_index(self, upper_bound: int) -> int:
        if upper_bound <= 0:
            raise ValueError("upper_bound must be positive")
        return self._rng.randrange(upper_bound)


# ---------------------------------------------------------------------------
# Reserved Phase 2 ports. Declared here so Phase 2 extends stable contracts.
# Phase 1 never instantiates these and never reports verification.
# ---------------------------------------------------------------------------


class ReadOnlyValidator(Protocol):
    """Downstream (Phase 2) read-only AWS validation port."""

    def validate(self, request: object) -> object: ...


class LabService(Protocol):
    """Downstream (Phase 2) lab lifecycle port."""

    def start_lab(self, request: object) -> object: ...

    def record_lab_checkpoint(self, request: object) -> object: ...

    def complete_lab(self, request: object) -> object: ...
