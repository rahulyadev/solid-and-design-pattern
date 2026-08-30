"""Separate a state invariant from a promise over sequences of states."""

import pytest
from alias_history import CountReader, GrowingCount, ResettableCount, never_decreases, run_probe
from hypothesis import given
from hypothesis import strategies as st


@given(amounts=st.lists(st.integers(min_value=0, max_value=10**6), max_size=30))
def test_base_operations_preserve_state_and_history(amounts: list[int]) -> None:
    counter = GrowingCount()
    readings = [counter.value]
    for amount in amounts:
        counter.advance(amount)
        readings.append(counter.value)
    assert counter.value == sum(amounts)
    assert all(value >= 0 for value in readings)
    assert never_decreases(tuple(readings))


def test_rejected_advance_has_no_state_effect() -> None:
    counter = GrowingCount()
    counter.advance(4)
    with pytest.raises(ValueError):
        counter.advance(-1)
    assert counter.value == 4


def test_added_method_is_visible_through_the_existing_reader_alias() -> None:
    writer = ResettableCount()
    reader: CountReader = writer
    writer.advance(3)
    before = reader.value
    writer.reset()
    assert before == 3
    assert reader.value == 0
    assert not never_decreases((before, reader.value))


@pytest.mark.parametrize(
    ("values", "expected"),
    [((), True), ((0,), True), ((0, 0, 3), True), ((0, 3, 0), False), ((5, 4), False)],
)
def test_history_predicate(values: tuple[int, ...], expected: bool) -> None:
    assert never_decreases(values) is expected


def test_observed_sequence() -> None:
    assert run_probe() == (
        "same object: True",
        "readings: (0, 3, 0)",
        "nonnegative states: True",
        "never decreases: False",
    )
