"""Characterization only: passing these tests does not complete the new requirements."""

import pytest
from support_queue_lab import Ticket, queue_report, remaining_minutes


@pytest.mark.parametrize(
    ("plan", "urgent", "allowance"),
    [
        ("standard", False, 480),
        ("standard", True, 120),
        ("priority", False, 120),
        ("priority", True, 30),
    ],
)
@pytest.mark.parametrize("offset", [-1, 0, 1])
def test_before_at_and_after_deadline(plan: str, urgent: bool, allowance: int, offset: int) -> None:
    ticket = Ticket("CASE-1", allowance + offset, urgent)
    expected = 1 if offset == -1 else 0
    assert remaining_minutes(ticket, plan) == expected


@pytest.mark.parametrize("plan", ["standard", "priority"])
def test_current_plans_ignore_reopen_count(plan: str) -> None:
    first = Ticket("CASE-1", 10, reopen_count=0)
    reopened = Ticket("CASE-1", 10, reopen_count=7)
    assert remaining_minutes(first, plan) == remaining_minutes(reopened, plan)


def test_report_preserves_input_order_duplicate_references_and_input_values() -> None:
    tickets = (Ticket("B", 0), Ticket("A", 20, True), Ticket("B", 500))
    assert queue_report(tickets, "standard") == (("B", 480), ("A", 100), ("B", 0))
    assert tickets == (Ticket("B", 0), Ticket("A", 20, True), Ticket("B", 500))


@pytest.mark.parametrize("plan", ["standard", "priority"])
def test_empty_report_with_known_plan_is_empty(plan: str) -> None:
    assert queue_report((), plan) == ()


@pytest.mark.parametrize("plan", ["unknown", "STANDARD", " standard", ""])
def test_unknown_plan_is_rejected_even_for_an_empty_report(plan: str) -> None:
    with pytest.raises(ValueError, match="unknown plan"):
        remaining_minutes(Ticket("CASE-1", 0), plan)
    with pytest.raises(ValueError, match="unknown plan"):
        queue_report((), plan)


@pytest.mark.parametrize("reference", ["", " ", "\n\t"])
def test_blank_references_are_rejected(reference: str) -> None:
    with pytest.raises(ValueError, match="reference must be nonblank"):
        Ticket(reference, 0)


@pytest.mark.parametrize(("age", "reopens"), [(-1, 0), (0, -1)])
def test_negative_measurements_are_rejected(age: int, reopens: int) -> None:
    with pytest.raises(ValueError, match="nonnegative"):
        Ticket("CASE-1", age, reopen_count=reopens)


def test_nonblank_reference_is_preserved_without_normalization() -> None:
    assert queue_report((Ticket(" CASE-1 ", 0),), "priority") == ((" CASE-1 ", 120),)
