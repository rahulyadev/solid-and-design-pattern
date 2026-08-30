"""Protect baseline behaviour, without supplying the new provider or design."""

import pytest
from workshop_report_lab import publishable_slots
from workshop_vendor import PlanningClient


def test_capacity_threshold_and_sort_order() -> None:
    client = PlanningClient({"Monday": [("PM", 8), ("AM", 3), ("EVENING", 5)]})
    assert publishable_slots(client, "Monday", 5) == ("EVENING: 5 seats", "PM: 8 seats")


def test_no_qualifying_slots() -> None:
    client = PlanningClient({"Monday": [("AM", 0), ("PM", 2)]})
    assert publishable_slots(client, "Monday", 3) == ()


def test_empty_and_unknown_days() -> None:
    client = PlanningClient({"Monday": []})
    assert publishable_slots(client, "Monday", 1) == ()
    assert publishable_slots(client, "Friday", 1) == ()


@pytest.mark.parametrize("group_size", [0, -1])
def test_invalid_group_size_precedes_vendor_access(group_size: int) -> None:
    client = PlanningClient({}, offline=True)
    with pytest.raises(ValueError, match="positive"):
        publishable_slots(client, "Monday", group_size)


def test_outage_is_not_an_empty_schedule() -> None:
    with pytest.raises(RuntimeError, match="planning unavailable"):
        publishable_slots(PlanningClient({}, offline=True), "Monday", 2)


def test_snapshot_and_repeated_reports_do_not_mutate_input() -> None:
    days = {"Monday": [("AM", 4)]}
    client = PlanningClient(days)
    days["Monday"].append(("PM", 9))
    expected = ("AM: 4 seats",)
    assert publishable_slots(client, "Monday", 2) == expected
    assert publishable_slots(client, "Monday", 2) == expected
    assert days == {"Monday": [("AM", 4), ("PM", 9)]}


def test_unicode_identifiers_and_duplicate_rows_are_preserved() -> None:
    client = PlanningClient({"Monday": [("कक्षा", 5), ("कक्षा", 5)]})
    assert publishable_slots(client, "Monday", 5) == ("कक्षा: 5 seats", "कक्षा: 5 seats")


def test_negative_vendor_fixture_data_is_rejected() -> None:
    with pytest.raises(ValueError, match="nonnegative"):
        PlanningClient({"Monday": [("AM", -1)]})
