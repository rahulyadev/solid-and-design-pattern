"""Behavioral contract, transition matrix, failure boundaries and bounded traces."""

from collections.abc import Callable
from dataclasses import FrozenInstanceError
from typing import cast

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st
from observe_boundary import observe
from state import (
    MAX_PAGES,
    Cancelled,
    Editing,
    Event,
    InvalidTransition,
    Packet,
    PacketState,
    Phase,
    ReentrantEvent,
    Released,
    Sealed,
    Snapshot,
)

# Independent observable specification: no concrete-state types in this matrix.
EDGES = {
    (Phase.EDITING, Event.ADD): Phase.EDITING,
    (Phase.EDITING, Event.SEAL): Phase.SEALED,
    (Phase.EDITING, Event.CANCEL): Phase.CANCELLED,
    (Phase.SEALED, Event.REOPEN): Phase.EDITING,
    (Phase.SEALED, Event.RELEASE): Phase.RELEASED,
    (Phase.SEALED, Event.CANCEL): Phase.CANCELLED,
}


def at_phase(phase: Phase, gate: Callable[[Snapshot], None]) -> Packet:
    packet = Packet(gate)
    packet.handle(Event.ADD, 2)
    if phase in (Phase.SEALED, Phase.RELEASED):
        packet.handle(Event.SEAL)
    if phase is Phase.RELEASED:
        packet.handle(Event.RELEASE)
    if phase is Phase.CANCELLED:
        packet.handle(Event.CANCEL)
    return packet


@pytest.mark.parametrize("phase", list(Phase))
@pytest.mark.parametrize("event", list(Event))
def test_entire_transition_matrix(phase: Phase, event: Event) -> None:
    calls: list[Snapshot] = []
    packet = at_phase(phase, calls.append)
    calls.clear()
    before = packet.snapshot
    target = EDGES.get((phase, event))
    if target is None:
        with pytest.raises(InvalidTransition) as caught:
            packet.handle(event, 1 if event is Event.ADD else 0)
        assert caught.value.phase is phase
        assert caught.value.event is event
        assert packet.snapshot is before
        assert calls == []
    else:
        result = packet.handle(event, 1 if event is Event.ADD else 0)
        assert result is packet.snapshot
        assert result == Snapshot(target, 3 if event is Event.ADD else 2, before.revision + 1)
        assert calls == ([result] if event is Event.RELEASE else [])


def test_initial_empty_and_maximum_pages() -> None:
    packet = Packet()
    before = packet.snapshot
    assert before == Snapshot(Phase.EDITING, 0, 0)
    with pytest.raises(ValueError, match="pages"):
        packet.handle(Event.SEAL)
    assert packet.snapshot is before
    packet.handle(Event.ADD, MAX_PAGES)
    full = packet.snapshot
    with pytest.raises(ValueError, match="pages"):
        packet.handle(Event.ADD, 1)
    assert packet.snapshot is full
    packet.handle(Event.SEAL)
    assert packet.handle(Event.RELEASE) == Snapshot(Phase.RELEASED, 20, 3)


@pytest.mark.parametrize("value", [True, False, -1, 0, 21, 1.0, "1", None])
def test_bad_add_arguments_leave_snapshot_identical(value: object) -> None:
    packet = Packet()
    before = packet.snapshot
    with pytest.raises(ValueError):
        packet.handle(Event.ADD, cast(int, value))
    assert packet.snapshot is before


@pytest.mark.parametrize("event", [Event.SEAL, Event.REOPEN, Event.RELEASE, Event.CANCEL])
@pytest.mark.parametrize("value", [True, 1, -1, 0.0, None])
def test_non_add_arguments_are_checked_before_dispatch(event: Event, value: object) -> None:
    packet = Packet()
    before = packet.snapshot
    with pytest.raises(ValueError, match="only ADD"):
        packet.handle(event, cast(int, value))
    assert packet.snapshot is before


@pytest.mark.parametrize("value", ["add", 1, None, True])
def test_bad_event(value: object) -> None:
    packet = Packet()
    with pytest.raises(TypeError, match="Event"):
        packet.handle(cast(Event, value))
    assert packet.snapshot.revision == 0


@pytest.mark.parametrize("state_type", [Editing, Sealed, Released, Cancelled])
@pytest.mark.parametrize("value", [True, -1, 21, 1.0])
def test_state_value_construction(state_type: type[PacketState], value: object) -> None:
    # A separate constructor contract is tested through precise callable typing below.
    constructor = cast(Callable[[int], PacketState], state_type)
    with pytest.raises(ValueError):
        constructor(cast(int, value))


def test_empty_cancellation_and_nonempty_state_guards() -> None:
    assert Packet().handle(Event.CANCEL) == Snapshot(Phase.CANCELLED, 0, 1)
    with pytest.raises(ValueError):
        Sealed(0)
    with pytest.raises(ValueError):
        Released(0)


def test_gate_failure_preserves_identity_and_clears_busy_flag() -> None:
    error = RuntimeError("synthetic gate failure")
    calls: list[Snapshot] = []

    def fail_once(proposal: Snapshot) -> None:
        calls.append(proposal)
        if len(calls) == 1:
            raise error

    packet = at_phase(Phase.SEALED, fail_once)
    before = packet.snapshot
    with pytest.raises(RuntimeError) as caught:
        packet.handle(Event.RELEASE)
    assert caught.value is error
    assert packet.snapshot is before
    assert len(calls) == 1  # No automatic retry.
    result = packet.handle(Event.RELEASE)
    assert len(calls) == 2
    assert calls[0] == calls[1] == result
    assert result.revision == before.revision + 1


def test_gate_reads_old_state_and_receives_proposal() -> None:
    observed: list[tuple[Snapshot, Snapshot]] = []

    def inspect(proposal: Snapshot) -> None:
        observed.append((packet.snapshot, proposal))

    packet = at_phase(Phase.SEALED, inspect)
    before = packet.snapshot
    result = packet.handle(Event.RELEASE)
    assert observed == [(before, result)]
    assert before.phase is Phase.SEALED
    assert result.phase is Phase.RELEASED


def test_uncaught_reentrancy_aborts_outer_transition() -> None:
    def reenter(proposal: Snapshot) -> None:
        packet.handle(Event.CANCEL)

    packet = at_phase(Phase.SEALED, reenter)
    before = packet.snapshot
    with pytest.raises(ReentrantEvent):
        packet.handle(Event.RELEASE)
    assert packet.snapshot is before
    assert packet.handle(Event.REOPEN).phase is Phase.EDITING


def test_gate_may_catch_reentrancy_and_allow_outer_release() -> None:
    def catch_nested(proposal: Snapshot) -> None:
        with pytest.raises(ReentrantEvent):
            packet.handle(Event.CANCEL)

    packet = at_phase(Phase.SEALED, catch_nested)
    assert packet.handle(Event.RELEASE).phase is Phase.RELEASED


def test_other_context_is_independent() -> None:
    other = Packet()

    def touch_other(proposal: Snapshot) -> None:
        other.handle(Event.ADD, 4)

    packet = at_phase(Phase.SEALED, touch_other)
    saved = packet.snapshot
    packet.handle(Event.RELEASE)
    assert other.snapshot == Snapshot(Phase.EDITING, 4, 1)
    assert saved == Snapshot(Phase.SEALED, 2, 2)
    field_name = "pages"
    with pytest.raises(FrozenInstanceError):
        setattr(saved, field_name, 8)


def test_base_exception_also_clears_guard() -> None:
    failure = KeyboardInterrupt("synthetic")

    def stop(proposal: Snapshot) -> None:
        raise failure

    packet = at_phase(Phase.SEALED, stop)
    before = packet.snapshot
    with pytest.raises(KeyboardInterrupt) as caught:
        packet.handle(Event.RELEASE)
    assert caught.value is failure
    assert packet.snapshot is before
    assert packet.handle(Event.CANCEL).phase is Phase.CANCELLED


@settings(max_examples=100, derandomize=True)
@given(st.lists(st.sampled_from(list(Event)), max_size=60))
def test_bounded_event_sequences_against_model(events: list[Event]) -> None:
    packet = Packet()
    phase, pages, revision = Phase.EDITING, 0, 0
    for event in events:
        before = packet.snapshot
        target = EDGES.get((phase, event))
        guard_fails = (event is Event.SEAL and pages == 0) or (
            phase is Phase.EDITING and event is Event.ADD and pages == MAX_PAGES
        )
        if target is None or guard_fails:
            with pytest.raises(ValueError):
                packet.handle(event, 1 if event is Event.ADD else 0)
            assert packet.snapshot is before
        else:
            phase = target
            pages += event is Event.ADD
            revision += 1
            assert packet.handle(event, 1 if event is Event.ADD else 0) == Snapshot(
                phase, pages, revision
            )


@pytest.mark.parametrize(
    ("mode", "effects", "error", "phase", "revision", "same"),
    [
        ("success", [3], "none", "released", 3, False),
        ("fail_before", [], "GateFailure", "sealed", 2, True),
        ("fail_after", [3], "GateFailure", "sealed", 2, True),
        ("reenter", [], "ReentrantEvent", "sealed", 2, True),
    ],
)
def test_observation_contract(
    mode: str, effects: list[int], error: str, phase: str, revision: int, same: bool
) -> None:
    assert observe(mode) == (
        f"{mode}: seen=['sealed->released'], effects={effects}, error={error}, "
        f"state={phase}, rev={revision}, same_snapshot={same}"
    )
