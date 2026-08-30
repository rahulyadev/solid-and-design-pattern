"""Unsolved SDP-SOL-010 starter with correct current behaviour and mixed policies."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import TypedDict


@dataclass(frozen=True)
class Attendance:
    participant_id: str
    attended: int
    scheduled: int

    def __post_init__(self) -> None:
        if not self.participant_id.strip():
            raise ValueError("participant_id must not be blank")
        if self.scheduled <= 0:
            raise ValueError("scheduled must be positive")
        if not 0 <= self.attended <= self.scheduled:
            raise ValueError("attended must be between zero and scheduled")


class ArchiveRow(TypedDict):
    participant_id: str
    attendance: str
    eligible: bool
    needs_follow_up: bool


def publish_completion(
    attendance: Attendance,
    record: Callable[[ArchiveRow], None],
    send: Callable[[str, str], None],
) -> str:
    """Record one result, then send its bulletin; propagate callback errors."""
    eligible = attendance.attended * 100 >= 75 * attendance.scheduled
    needs_follow_up = attendance.attended * 100 < 75 * attendance.scheduled
    result = "complete" if eligible else "incomplete"
    follow_up = "yes" if needs_follow_up else "no"
    body = (
        f"Completion for {attendance.participant_id}\n"
        f"Attendance: {attendance.attended}/{attendance.scheduled}\n"
        f"Result: {result}\n"
        f"Follow-up: {follow_up}"
    )
    row: ArchiveRow = {
        "participant_id": attendance.participant_id,
        "attendance": f"{attendance.attended}/{attendance.scheduled}",
        "eligible": eligible,
        "needs_follow_up": needs_follow_up,
    }
    record(row)
    send(attendance.participant_id, body)
    return body


def main() -> None:
    saved: list[ArchiveRow] = []
    messages: list[tuple[str, str]] = []

    def send(participant_id: str, body: str) -> None:
        messages.append((participant_id, body))

    body = publish_completion(Attendance("L-17", 3, 4), saved.append, send)
    print(body)
    print(f"archive: {saved}")
    print(f"sent: {len(messages)}")


if __name__ == "__main__":
    main()
