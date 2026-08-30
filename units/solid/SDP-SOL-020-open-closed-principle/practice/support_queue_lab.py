"""Working conditional starter. The extension/refactoring exercise is unsolved."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Ticket:
    reference: str
    age_minutes: int
    urgent: bool = False
    reopen_count: int = 0

    def __post_init__(self) -> None:
        if not self.reference.strip():
            raise ValueError("reference must be nonblank")
        if self.age_minutes < 0 or self.reopen_count < 0:
            raise ValueError("age and reopen count must be nonnegative")


def remaining_minutes(ticket: Ticket, plan: str) -> int:
    if plan == "standard":
        allowance = 120 if ticket.urgent else 480
    elif plan == "priority":
        allowance = 30 if ticket.urgent else 120
    else:
        raise ValueError(f"unknown plan: {plan}")
    return max(0, allowance - ticket.age_minutes)


def queue_report(tickets: tuple[Ticket, ...], plan: str) -> tuple[tuple[str, int], ...]:
    if plan not in ("standard", "priority"):
        raise ValueError(f"unknown plan: {plan}")
    return tuple((ticket.reference, remaining_minutes(ticket, plan)) for ticket in tickets)


def main() -> None:
    tickets = (
        Ticket("CASE-101", age_minutes=15),
        Ticket("CASE-102", age_minutes=40, urgent=True),
        Ticket("CASE-103", age_minutes=500, reopen_count=2),
    )
    for plan in ("standard", "priority"):
        print(f"{plan}: {queue_report(tickets, plan)}")


if __name__ == "__main__":
    main()
