"""The stable publication workflow and the contract its renderers share."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class RunSummary:
    completed: int
    failed: int

    def __post_init__(self) -> None:
        if self.completed < 0 or self.failed < 0:
            raise ValueError("counts must be nonnegative")


class Renderer(Protocol):
    """Render both counts as nonblank text, without publishing or changing the input."""

    def __call__(self, summary: RunSummary, /) -> str: ...


def publish_summary(
    summary: RunSummary,
    render: Renderer,
    write: Callable[[str], None],
) -> str:
    """Render once, reject blank output, then write once; propagate collaborator errors."""
    body = render(summary)
    if not body.strip():
        raise ValueError("renderer returned blank output")
    write(body)
    return body
