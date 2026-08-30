"""Characterize the current public contract without prescribing a refactoring."""

from dataclasses import dataclass, field

import pytest
from completion_lab import ArchiveRow, Attendance, publish_completion


@dataclass
class Effects:
    rows: list[ArchiveRow] = field(default_factory=list)
    messages: list[tuple[str, str]] = field(default_factory=list)
    events: list[str] = field(default_factory=list)

    def record(self, row: ArchiveRow) -> None:
        self.events.append("record")
        self.rows.append(row)

    def send(self, participant_id: str, body: str) -> None:
        self.events.append("send")
        self.messages.append((participant_id, body))


def test_exact_bulletin_archive_and_effect_order() -> None:
    effects = Effects()
    body = publish_completion(Attendance("L-17", 3, 4), effects.record, effects.send)
    assert body == "Completion for L-17\nAttendance: 3/4\nResult: complete\nFollow-up: no"
    assert effects.rows == [
        {
            "participant_id": "L-17",
            "attendance": "3/4",
            "eligible": True,
            "needs_follow_up": False,
        }
    ]
    assert effects.messages == [("L-17", body)]
    assert effects.events == ["record", "send"]


@pytest.mark.parametrize(
    ("attended", "scheduled", "eligible", "follow_up"),
    [
        (0, 4, False, True),
        (2, 3, False, True),
        (74, 100, False, True),
        (3, 4, True, False),
        (75, 100, True, False),
        (76, 100, True, False),
        (4, 4, True, False),
        (1, 1, True, False),
    ],
)
def test_attendance_boundaries(
    attended: int,
    scheduled: int,
    eligible: bool,
    follow_up: bool,
) -> None:
    effects = Effects()
    body = publish_completion(Attendance("L-18", attended, scheduled), effects.record, effects.send)
    assert effects.rows[0]["eligible"] is eligible
    assert effects.rows[0]["needs_follow_up"] is follow_up
    assert f"Result: {'complete' if eligible else 'incomplete'}" in body
    assert f"Follow-up: {'yes' if follow_up else 'no'}" in body


@pytest.mark.parametrize(
    ("participant_id", "attended", "scheduled"),
    [("", 1, 4), ("  ", 1, 4), ("L-17", -1, 4), ("L-17", 5, 4), ("L-17", 0, 0), ("L-17", 0, -4)],
)
def test_invalid_attendance(participant_id: str, attended: int, scheduled: int) -> None:
    with pytest.raises(ValueError):
        Attendance(participant_id, attended, scheduled)


def test_record_failure_prevents_sending() -> None:
    effects = Effects()

    def fail_record(row: ArchiveRow) -> None:
        raise OSError("archive unavailable")

    with pytest.raises(OSError, match="archive unavailable"):
        publish_completion(Attendance("L-17", 3, 4), fail_record, effects.send)
    assert effects.messages == []


def test_send_failure_does_not_erase_the_record() -> None:
    effects = Effects()

    def fail_send(participant_id: str, body: str) -> None:
        raise OSError("delivery unavailable")

    with pytest.raises(OSError, match="delivery unavailable"):
        publish_completion(Attendance("L-17", 3, 4), effects.record, fail_send)
    assert len(effects.rows) == 1
    assert effects.rows[0]["participant_id"] == "L-17"


def test_requests_do_not_share_effect_collections() -> None:
    first = Effects()
    second = Effects()
    publish_completion(Attendance("L-17", 3, 4), first.record, first.send)
    publish_completion(Attendance("L-18", 0, 4), second.record, second.send)
    assert first.rows[0]["participant_id"] == "L-17"
    assert second.rows[0]["participant_id"] == "L-18"
    assert len(first.messages) == len(second.messages) == 1
