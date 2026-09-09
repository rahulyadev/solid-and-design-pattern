"""The small, synchronous capability clients and decorators share."""

from dataclasses import dataclass
from typing import Literal, Protocol


class SourceClosed(RuntimeError):
    """The owner closed the source before this operation."""


class TextSource(Protocol):
    def render(self, key: str, /) -> str:
        """Render configured plain text; unknown keys raise KeyError.

        Callers accept configured presentation, not exact unformatted storage text.
        Implementations do not consume keys or own the caller's resource lifetime.
        The worked wrappers delegate once and preserve underlying exceptions.
        Optional observations are permitted. No escaping or delivery is promised.
        """
        ...


@dataclass(frozen=True)
class Observation:
    outcome: Literal["ok", "error"]
    characters: int | None
