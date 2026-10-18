"""A small, dependency-free state-machine primitive.

Every stateful entity in `study_core` declares its allowed transitions as data
and routes changes through one uniform guard. This replaces ad hoc `if`/UPDATE
logic scattered across services so illegal transitions fail the same way
everywhere and the rules are auditable in one place per machine.

Usage:

    machine = StateMachine(
        name="review",
        initial=ReviewState.SCHEDULED,
        transitions={
            (ReviewState.SCHEDULED, ReviewState.RESOLVED),
            (ReviewState.SCHEDULED, ReviewState.SUPERSEDED),
        },
    )
    machine.assert_transition(current, target)   # raises on illegal moves
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from enum import StrEnum


class IllegalTransitionError(Exception):
    """A requested state transition is not permitted by the machine."""

    def __init__(self, machine: str, current: StrEnum, target: StrEnum, reason: str) -> None:
        self.machine = machine
        self.current = current
        self.target = target
        self.reason = reason
        super().__init__(
            f"[{machine}] illegal transition {current.value} -> {target.value}: {reason}"
        )


class StateMachine[S: StrEnum]:
    """A declarative transition guard over a `StrEnum` of states.

    Transitions are a set of allowed `(from, to)` pairs. An optional per-pair
    guard predicate can impose extra conditions (for example, requiring a
    particular evidence kind). The machine holds no mutable state itself; it
    only validates proposed moves, which keeps it pure and reusable.
    """

    def __init__(
        self,
        *,
        name: str,
        initial: S,
        transitions: Iterable[tuple[S, S]],
        terminal: Iterable[S] = (),
    ) -> None:
        self.name = name
        self.initial = initial
        self._transitions: frozenset[tuple[S, S]] = frozenset(transitions)
        self._terminal: frozenset[S] = frozenset(terminal)
        self._guards: dict[tuple[S, S], Callable[..., tuple[bool, str]]] = {}

    def allow(self, current: S, target: S, guard: Callable[..., tuple[bool, str]]) -> None:
        """Attach a guard predicate to an already-declared transition.

        The guard receives keyword context and returns `(ok, reason)`.
        """
        if (current, target) not in self._transitions:
            raise ValueError(
                f"[{self.name}] cannot guard undeclared transition "
                f"{current.value} -> {target.value}"
            )
        self._guards[(current, target)] = guard

    def can_transition(self, current: S, target: S, **context: object) -> tuple[bool, str]:
        """Return `(ok, reason)` for a proposed transition without raising."""
        if current in self._terminal:
            return False, f"{current.value} is terminal"
        if (current, target) not in self._transitions:
            return False, "transition is not declared"
        guard = self._guards.get((current, target))
        if guard is not None:
            return guard(**context)
        return True, ""

    def assert_transition(self, current: S, target: S, **context: object) -> S:
        """Validate a transition and return the target, or raise.

        Raises:
            IllegalTransitionError: when the transition is undeclared, blocked
            by a guard, or leaves a terminal state.
        """
        ok, reason = self.can_transition(current, target, **context)
        if not ok:
            raise IllegalTransitionError(self.name, current, target, reason)
        return target

    def is_terminal(self, state: S) -> bool:
        """Return True when a state permits no further transitions."""
        return state in self._terminal

    def targets_from(self, current: S) -> frozenset[S]:
        """Return the states reachable in one step from `current`."""
        return frozenset(to for (frm, to) in self._transitions if frm == current)
