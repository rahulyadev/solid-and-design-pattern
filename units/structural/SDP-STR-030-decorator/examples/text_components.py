"""Original synthetic source and small composition-based decorators."""

from collections.abc import Callable, Mapping
from dataclasses import dataclass, field

from text_contract import Observation, SourceClosed, TextSource


class MemoryText:
    """Owner-managed snapshot with explicit, infallible, idempotent close."""

    def __init__(self, texts: Mapping[str, str]) -> None:
        self._texts = dict(texts)
        self._closed = False
        self.calls = 0
        self.close_count = 0

    def render(self, key: str, /) -> str:
        self.calls += 1
        if self._closed:
            raise SourceClosed("text source is closed")
        return self._texts[key]

    def close(self) -> None:
        if not self._closed:
            self._closed = True
            self.close_count += 1


@dataclass(frozen=True, eq=False)
class Label:
    inner: TextSource
    label: str

    def render(self, key: str, /) -> str:
        return self.label + self.inner.render(key)


@dataclass(frozen=True, eq=False)
class Bracket:
    inner: TextSource

    def render(self, key: str, /) -> str:
        return "[" + self.inner.render(key) + "]"


@dataclass(eq=False)
class Observed:
    """Best-effort diagnostics, never a mandatory audit or security boundary.

    Ordinary observer exceptions are dropped and counted. Control-flow
    BaseExceptions propagate. The synchronous observer must be fast and must
    not call this same observed capability recursively.
    """

    inner: TextSource
    emit: Callable[[Observation], None]
    dropped: int = field(default=0, init=False)

    def _record(self, observation: Observation) -> None:
        try:
            self.emit(observation)
        except Exception:
            self.dropped += 1

    def render(self, key: str, /) -> str:
        try:
            text = self.inner.render(key)
        except Exception:
            self._record(Observation("error", None))
            raise
        self._record(Observation("ok", len(text)))
        return text
