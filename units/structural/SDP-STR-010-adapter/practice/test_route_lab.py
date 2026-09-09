import pytest
from route_lab import RouteFeed, trip_label


def test_existing_label_and_one_query() -> None:
    feed = RouteFeed({"NORTH": 7})
    assert trip_label(feed, "NORTH") == "NORTH: 7 min"
    assert feed.calls == ["NORTH"]


def test_zero_is_a_valid_old_duration() -> None:
    assert trip_label(RouteFeed({"HERE": 0}), "HERE") == "HERE: 0 min"


def test_unknown_route_preserves_old_error() -> None:
    with pytest.raises(KeyError):
        trip_label(RouteFeed({}), "MISSING")


def test_old_feed_reads_current_state() -> None:
    feed = RouteFeed({"NORTH": 7})
    feed.durations["NORTH"] = 8
    assert trip_label(feed, "NORTH") == "NORTH: 8 min"
