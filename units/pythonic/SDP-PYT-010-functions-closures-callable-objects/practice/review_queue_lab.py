"""Runnable legacy baseline. The requested callable refactoring is unsolved."""

from collections.abc import Iterable
from dataclasses import dataclass


@dataclass(frozen=True)
class Ticket:
    key: str
    age_days: int
    urgent: bool = False
    closed: bool = False


def choose_reviews(tickets: Iterable[Ticket], lane: str) -> tuple[str, ...]:
    """Existing public API: preserve these observations during phase A."""
    if lane not in ("urgent", "stale"):
        raise ValueError("unknown review lane")
    selected: list[str] = []
    for ticket in tickets:
        if ticket.closed:
            continue
        if lane == "urgent":
            if ticket.urgent:
                selected.append(ticket.key)
        elif ticket.age_days >= 14:
            selected.append(ticket.key)
    return tuple(selected)


if __name__ == "__main__":
    sample = (
        Ticket("T-3", 1, urgent=True),
        Ticket("T-1", 14),
        Ticket("T-2", 30, urgent=True, closed=True),
        Ticket("T-3", 1, urgent=True),
    )
    print("urgent:", choose_reviews(sample, "urgent"))
    print("stale:", choose_reviews(sample, "stale"))
