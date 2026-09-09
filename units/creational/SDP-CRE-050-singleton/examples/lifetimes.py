"""Explicit application ownership plus a bounded, resource-free lazy value provider."""

from __future__ import annotations

from collections.abc import Callable, Iterator, Mapping
from contextlib import contextmanager
from dataclasses import dataclass
from threading import RLock
from typing import Generic, Protocol, TypeVar


class Reader(Protocol):
    def lookup(self, key: str) -> str: ...


class OwnedReader(Reader, Protocol):
    def close(self) -> None: ...


@dataclass(frozen=True)
class ReportService:
    reader: Reader

    def render(self, key: str) -> str:
        return f"report:{self.reader.lookup(key)}"


@dataclass(frozen=True)
class Application:
    preview: ReportService
    export: ReportService


@contextmanager
def application(open_reader: Callable[[], OwnedReader]) -> Iterator[Application]:
    """Own one completed acquisition. Callers must stop/join users before exiting."""
    reader = open_reader()
    try:
        yield Application(ReportService(reader), ReportService(reader))
    finally:
        reader.close()


class MemoryReader:
    """Synthetic adapter: defensive snapshot, explicit closure, no real external I/O."""

    def __init__(self, entries: Mapping[str, str], *, revision: str) -> None:
        if not revision.strip():
            raise ValueError("revision required")
        self._entries = dict(entries)
        self.revision = revision
        self.closed = False

    def lookup(self, key: str) -> str:
        if self.closed:
            raise RuntimeError("reader closed")
        return self._entries[key]

    def close(self) -> None:
        self.closed = True


T = TypeVar("T")


class LazyValue(Generic[T]):  # noqa: UP046 — Python 3.11 compatibility
    """One successfully published value per provider; failure retries on a later get.

    Factories must be bounded, resource-free, and must not wait on another thread
    that needs this provider. The lock protects publication, not use of the value.
    """

    def __init__(self, build: Callable[[], T]) -> None:
        self._build = build
        self._lock = RLock()
        self._building = False
        self._box: tuple[T] | None = None

    def get(self) -> T:
        with self._lock:
            if self._box is not None:
                return self._box[0]
            if self._building:
                raise RuntimeError("recursive initialization")
            self._building = True
            try:
                value = self._build()
                self._box = (value,)
                return value
            finally:
                self._building = False
