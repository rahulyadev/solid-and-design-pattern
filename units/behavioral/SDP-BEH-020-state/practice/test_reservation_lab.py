"""Baseline behavior only. Passing these does not solve the change request."""

import pytest
from reservation_lab import Station, Status


def test_baseline_cycle() -> None:
    station = Station()
    station.reserve("reader-a")
    station.enter("reader-a")
    station.leave("reader-a")
    assert (station.status, station.owner) == (Status.FREE, None)


@pytest.mark.parametrize("owner", ["", " "])
def test_empty_owner(owner: str) -> None:
    with pytest.raises(ValueError):
        Station().reserve(owner)


def test_wrong_owner_and_repeated_reserve() -> None:
    station = Station()
    station.reserve("reader-a")
    with pytest.raises(ValueError):
        station.reserve("reader-b")
    with pytest.raises(ValueError):
        station.enter("reader-b")
    assert (station.status, station.owner) == (Status.HELD, "reader-a")
    station.enter("reader-a")
    with pytest.raises(ValueError):
        station.leave("reader-b")
    assert (station.status, station.owner) == (Status.OCCUPIED, "reader-a")
