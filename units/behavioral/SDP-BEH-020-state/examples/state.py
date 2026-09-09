"""A bounded, synchronous review-packet lifecycle; no persistence or delivery."""

from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from typing import ClassVar, Protocol

MAX_PAGES = 20


class Phase(Enum):
    EDITING = "editing"
    SEALED = "sealed"
    RELEASED = "released"
    CANCELLED = "cancelled"


class Event(Enum):
    ADD = "add"
    SEAL = "seal"
    REOPEN = "reopen"
    RELEASE = "release"
    CANCEL = "cancel"


class InvalidTransition(ValueError):
    def __init__(self, phase: Phase, event: Event) -> None:
        self.phase = phase
        self.event = event
        super().__init__(f"{event.value} is forbidden in {phase.value}")


class ReentrantEvent(RuntimeError):
    """An event was attempted while this same context was handling another."""


def _check_pages(pages: int, minimum: int = 0) -> None:
    if type(pages) is not int or not minimum <= pages <= MAX_PAGES:
        raise ValueError(f"pages must be an exact int in {minimum}..{MAX_PAGES}")


class PacketState(Protocol):
    @property
    def phase(self) -> Phase: ...

    @property
    def pages(self) -> int: ...

    def handle(self, event: Event, pages: int, /) -> "PacketState": ...


@dataclass(frozen=True)
class Editing:
    pages: int = 0
    phase: ClassVar[Phase] = Phase.EDITING

    def __post_init__(self) -> None:
        _check_pages(self.pages)

    def handle(self, event: Event, pages: int, /) -> PacketState:
        if event is Event.ADD:
            return Editing(self.pages + pages)
        if event is Event.SEAL:
            return Sealed(self.pages)
        if event is Event.CANCEL:
            return Cancelled(self.pages)
        raise InvalidTransition(self.phase, event)


@dataclass(frozen=True)
class Sealed:
    pages: int
    phase: ClassVar[Phase] = Phase.SEALED

    def __post_init__(self) -> None:
        _check_pages(self.pages, 1)

    def handle(self, event: Event, pages: int, /) -> PacketState:
        if event is Event.REOPEN:
            return Editing(self.pages)
        if event is Event.RELEASE:
            return Released(self.pages)
        if event is Event.CANCEL:
            return Cancelled(self.pages)
        raise InvalidTransition(self.phase, event)


@dataclass(frozen=True)
class Released:
    pages: int
    phase: ClassVar[Phase] = Phase.RELEASED

    def __post_init__(self) -> None:
        _check_pages(self.pages, 1)

    def handle(self, event: Event, pages: int, /) -> PacketState:
        raise InvalidTransition(self.phase, event)


@dataclass(frozen=True)
class Cancelled:
    pages: int
    phase: ClassVar[Phase] = Phase.CANCELLED

    def __post_init__(self) -> None:
        _check_pages(self.pages)

    def handle(self, event: Event, pages: int, /) -> PacketState:
        raise InvalidTransition(self.phase, event)


@dataclass(frozen=True)
class Snapshot:
    phase: Phase
    pages: int
    revision: int


ReleaseGate = Callable[[Snapshot], None]


def allow_release(proposal: Snapshot) -> None:
    """Default local admission rule. It performs no external operation."""


@dataclass(frozen=True)
class _Current:
    state: PacketState
    snapshot: Snapshot


class Packet:
    """One owner must serialize all access. Gates are trusted synchronous callables."""

    def __init__(self, gate: ReleaseGate = allow_release) -> None:
        initial = Editing()
        self._current = _Current(initial, Snapshot(initial.phase, initial.pages, 0))
        self._gate = gate
        self._handling = False

    @property
    def snapshot(self) -> Snapshot:
        return self._current.snapshot

    def handle(self, event: Event, pages: int = 0) -> Snapshot:
        # Reentrancy takes precedence even over validation of a nested request.
        if self._handling:
            raise ReentrantEvent("nested events on the same packet are forbidden")
        if not isinstance(event, Event):
            raise TypeError("event must be an Event member")
        if event is Event.ADD:
            _check_pages(pages, 1)
        elif type(pages) is not int or pages != 0:
            raise ValueError("only ADD accepts a nonzero pages argument")
        self._handling = True
        try:
            before = self._current
            successor = before.state.handle(event, pages)
            proposal = Snapshot(successor.phase, successor.pages, before.snapshot.revision + 1)
            candidate = _Current(successor, proposal)
            if event is Event.RELEASE:
                self._gate(proposal)
            # All ordinary fallible work and callbacks precede this local commit.
            self._current = candidate
            return proposal
        finally:
            self._handling = False
