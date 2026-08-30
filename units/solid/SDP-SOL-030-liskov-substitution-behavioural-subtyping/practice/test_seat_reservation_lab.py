"""Baseline characterization only; learner adds partner contract acceptance tests."""

import pytest
from seat_reservation_lab import NotEnoughSeats, SeatPool


@pytest.mark.parametrize("seats", [[], [1], [9, 4, 7]])
def test_zero_request_is_a_no_op(seats: list[int]) -> None:
    pool = SeatPool(seats)
    assert pool.reserve(0) == ()
    assert pool.available_count == len(seats)
    assert pool.reserve(len(seats)) == tuple(seats)


@pytest.mark.parametrize("count", [0, 1, 2, 3])
def test_success_reserves_exactly_the_requested_seats_in_order(count: int) -> None:
    seats = [9, 4, 7]
    pool = SeatPool(seats)
    assert pool.reserve(count) == tuple(seats[:count])
    assert pool.available_count == 3 - count
    assert pool.reserve(3 - count) == tuple(seats[count:])


@pytest.mark.parametrize("count", [-1, -100])
def test_negative_request_leaves_state_unchanged(count: int) -> None:
    pool = SeatPool([2, 5])
    with pytest.raises(ValueError):
        pool.reserve(count)
    assert pool.available_count == 2
    assert pool.reserve(2) == (2, 5)


@pytest.mark.parametrize("count", [3, 4, 10**6])
def test_failed_reservation_preserves_all_available_seats(count: int) -> None:
    pool = SeatPool([2, 5])
    with pytest.raises(NotEnoughSeats):
        pool.reserve(count)
    assert pool.available_count == 2
    assert pool.reserve(2) == (2, 5)


@pytest.mark.parametrize("seats", [[0], [-1], [2, 2], [1, 0, 3]])
def test_invalid_seat_sets_are_rejected(seats: list[int]) -> None:
    with pytest.raises(ValueError):
        SeatPool(seats)


def test_source_list_changes_cannot_change_the_pool() -> None:
    seats = [11, 13]
    pool = SeatPool(seats)
    seats.clear()
    assert pool.reserve(2) == (11, 13)


def test_successive_reservations_never_reuse_a_seat() -> None:
    pool = SeatPool([11, 13])
    assert pool.reserve(1) == (11,)
    assert pool.reserve(1) == (13,)
    with pytest.raises(NotEnoughSeats):
        pool.reserve(1)
    assert pool.reserve(0) == ()
