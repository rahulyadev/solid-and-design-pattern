"""Phase-A characterization only. These tests do not prove a new design exists."""

from collections.abc import Iterator

import pytest
from review_queue_lab import Ticket, choose_reviews


def test_urgent_lane_keeps_input_order_and_duplicates() -> None:
    tickets = (
        Ticket("B", 0, urgent=True),
        Ticket("ignored", 30),
        Ticket("A", 0, urgent=True),
        Ticket("B", 0, urgent=True),
    )
    assert choose_reviews(tickets, "urgent") == ("B", "A", "B")


def test_stale_lane_includes_exact_threshold_regardless_of_urgency() -> None:
    tickets = (
        Ticket("young", 13, urgent=True),
        Ticket("edge", 14),
        Ticket("older", 20, urgent=True),
    )
    assert choose_reviews(tickets, "stale") == ("edge", "older")


@pytest.mark.parametrize("lane", ["urgent", "stale"])
def test_closed_tickets_are_never_selected(lane: str) -> None:
    assert choose_reviews((Ticket("closed", 100, urgent=True, closed=True),), lane) == ()


@pytest.mark.parametrize("lane", ["urgent", "stale"])
def test_empty_known_lane_is_allowed(lane: str) -> None:
    assert choose_reviews((), lane) == ()


@pytest.mark.parametrize("lane", ["", "other", "URGENT"])
def test_unknown_lane_fails_before_input_is_consumed(lane: str) -> None:
    seen: list[str] = []

    def source() -> Iterator[Ticket]:
        seen.append("consumed")
        yield Ticket("A", 30)

    with pytest.raises(ValueError, match=r"^unknown review lane$"):
        choose_reviews(source(), lane)
    assert seen == []


def test_one_pass_iterator_is_supported() -> None:
    source = iter((Ticket("A", 14), Ticket("B", 15)))
    assert choose_reviews(source, "stale") == ("A", "B")
    assert list(source) == []


def test_input_list_is_not_mutated_and_can_be_reused() -> None:
    first = Ticket("A", 14, urgent=True)
    tickets = [first, Ticket("B", 0)]
    before = tickets.copy()
    assert choose_reviews(tickets, "stale") == ("A",)
    assert choose_reviews(tickets, "urgent") == ("A",)
    assert tickets == before
    assert tickets[0] is first


def test_blank_unicode_keys_and_negative_age_are_not_normalized() -> None:
    tickets = (
        Ticket("", -2, urgent=True),
        Ticket("  A  ", 14),
        Ticket("समीक्षा", 15, urgent=True),
    )
    assert choose_reviews(tickets, "urgent") == ("", "समीक्षा")
    assert choose_reviews(tickets, "stale") == ("  A  ", "समीक्षा")


def test_source_failure_is_propagated_without_replacement() -> None:
    failure = OSError("synthetic input failure")

    def source() -> Iterator[Ticket]:
        yield Ticket("A", 14)
        raise failure

    with pytest.raises(OSError) as caught:
        choose_reviews(source(), "stale")
    assert caught.value is failure
