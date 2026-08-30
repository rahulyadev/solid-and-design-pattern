"""Caller-owned needs and data. No concrete layout imports and no output I/O."""

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class BadgeRequest:
    attendee: str
    event: str


@dataclass(frozen=True)
class BadgeDocument:
    content_type: str
    body: str


class BadgeLayout(Protocol):
    @property
    def content_type(self) -> str: ...

    def render(self, attendee: str, /, *, event: str) -> str: ...


def prepare_badge(request: BadgeRequest, layout: BadgeLayout) -> BadgeDocument:
    """Build one finished document; do not translate failures into success.

    Valid names/events are nonblank strings; preserve their exact spelling.
    A layout must represent both values, supply the matching content type, and
    leave caller data unchanged. Types cannot prove that semantic promise.
    """
    if not request.attendee.strip() or not request.event.strip():
        raise ValueError("attendee and event must be nonblank")
    content_type = layout.content_type
    if not content_type.strip():
        raise ValueError("layout content type must be nonblank")
    body = layout.render(request.attendee, event=request.event)
    if not body.strip():
        raise ValueError("layout body must be nonblank")
    return BadgeDocument(content_type, body)
