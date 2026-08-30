"""Optional ABC variant for an owned family that shares a rendering skeleton.

The policy still accepts BadgeLayout. External implementations need not inherit
this base. Use a function instead if this shared skeleton is not a requirement.
"""

from abc import ABC, abstractmethod


class FramedBadgeLayout(ABC):
    content_type = "text/plain; charset=utf-8"

    def render(self, attendee: str, /, *, event: str) -> str:
        return f"[{event}]\n{self.name_line(attendee)}"

    @abstractmethod
    def name_line(self, attendee: str, /) -> str:
        """Return a role label and the unchanged attendee name."""
        raise NotImplementedError


class StaffBadgeLayout(FramedBadgeLayout):
    def name_line(self, attendee: str, /) -> str:
        return f"STAFF: {attendee}"


class VisitorBadgeLayout(FramedBadgeLayout):
    def name_line(self, attendee: str, /) -> str:
        return f"VISITOR: {attendee}"
