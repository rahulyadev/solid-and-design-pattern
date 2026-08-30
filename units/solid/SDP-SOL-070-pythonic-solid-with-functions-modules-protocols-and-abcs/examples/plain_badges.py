"""A stateless module that satisfies BadgeLayout without inheriting it."""

content_type = "text/plain; charset=utf-8"


def render(attendee: str, /, *, event: str) -> str:
    return f"{event}\n{attendee}"
