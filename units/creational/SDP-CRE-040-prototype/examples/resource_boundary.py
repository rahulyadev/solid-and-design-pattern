"""Acquire new resources after pure cloning; no live resource enters the graph."""

from collections.abc import Callable, Iterator
from contextlib import AbstractContextManager, ExitStack, contextmanager
from typing import Protocol

from prototype import QueryDraft


class Session(Protocol):
    def run(self) -> str: ...


@contextmanager
def materialize(
    draft: QueryDraft, acquire: Callable[[str], AbstractContextManager[Session]]
) -> Iterator[tuple[Session, ...]]:
    """Caller uses sessions only inside with; acquisition owns its own failures."""
    with ExitStack() as stack:
        sessions = tuple(stack.enter_context(acquire(op)) for op in draft.rules.operations)
        yield sessions
