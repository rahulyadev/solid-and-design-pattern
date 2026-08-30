"""A configured layout instance; JSON details stay outside badge policy."""

import json
from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True)
class JsonBadgeLayout:
    indent: int | None = None
    content_type: ClassVar[str] = "application/json"

    def __post_init__(self) -> None:
        if self.indent is not None and self.indent < 0:
            raise ValueError("indent must be nonnegative or None")

    def render(self, attendee: str, /, *, event: str) -> str:
        return json.dumps(
            {"event": event, "attendee": attendee},
            ensure_ascii=False,
            indent=self.indent,
        )
