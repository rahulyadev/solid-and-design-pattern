"""Check the two schedules and their explicitly bounded guarantees."""

import pytest
from split_probe import cohesive_schedule, split_schedule


def test_split_check_allows_two_consumers_for_one_token() -> None:
    result = split_schedule(1)
    assert result.accepted == (True, True)
    assert result.remaining == -1


@pytest.mark.parametrize(
    "tokens,accepted,remaining",
    [(0, (False, False), 0), (1, (True, False), 0), (2, (True, True), 0), (3, (True, True), 1)],
)
def test_cohesive_serial_transition_preserves_quota(
    tokens: int, accepted: tuple[bool, bool], remaining: int
) -> None:
    result = cohesive_schedule(tokens)
    assert result.accepted == accepted
    assert result.remaining == remaining


def test_no_capacity_does_not_reproduce_the_split_failure() -> None:
    assert split_schedule(0).remaining == 0
    assert split_schedule(0).accepted == (False, False)


def test_enough_capacity_does_not_reproduce_the_split_failure() -> None:
    assert split_schedule(2) == cohesive_schedule(2)


def test_negative_capacity_is_rejected_by_both_schedules() -> None:
    for run in (split_schedule, cohesive_schedule):
        with pytest.raises(ValueError, match="nonnegative"):
            run(-1)
