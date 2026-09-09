"""Sequential, non-reentrant teaching proxy. No network or security sandbox."""

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from math import isfinite
from time import monotonic
from typing import Literal

from catalog_contract import Closed, ContractError, Document, Key, OwnedCatalog

Outcome = Literal["hit", "miss", "denied", "error"]


@dataclass(frozen=True)
class Observation:
    outcome: Outcome


@dataclass(frozen=True)
class Entry:
    key: Key
    document: Document
    started_at: float


def ignore_observation(event: Observation) -> None:
    pass


class MemoryCatalog:
    """Synthetic current-value store. The close counter is an ownership test seam."""

    def __init__(self, documents: Mapping[Key, Document]) -> None:
        self._documents = dict(documents)
        self._closed = False
        self.reads = 0
        self.closes = 0

    def read(self, key: Key, /) -> Document:
        if self._closed:
            raise Closed("catalog closed")
        self.reads += 1
        return self._documents[key]

    def put(self, document: Document) -> None:
        if self._closed:
            raise Closed("catalog closed")
        self._documents[document.key] = document

    def close(self) -> None:
        if not self._closed:
            self._closed = True
            self.closes += 1


class CatalogProxy:
    """Own a lazily created catalog and cache at most one successful document.

    Trusted root supplies a fixed principal, a fresh/exclusive factory result, an
    authorizer that returns None or raises, and a finite nondecreasing clock.
    Authorization precedes cache lookup. Ordinary telemetry exceptions are counted
    and suppressed; BaseException subclasses can interrupt a completed operation.
    Callbacks must not re-enter; the busy guard detects sequential reentry only.
    """

    def __init__(
        self,
        principal: str,
        factory: Callable[[], OwnedCatalog],
        authorize: Callable[[str, Key], None],
        *,
        ttl: float,
        clock: Callable[[], float] = monotonic,
        observe: Callable[[Observation], None] = ignore_observation,
    ) -> None:
        if not isfinite(ttl) or ttl <= 0:
            raise ValueError("ttl must be finite and positive")
        self._principal = principal
        self._factory = factory
        self._authorize = authorize
        self._ttl = ttl
        self._clock = clock
        self._observe = observe
        self._target: OwnedCatalog | None = None
        self._entry: Entry | None = None
        self._closed = False
        self._busy = False
        self.observer_failures = 0

    def _require_idle_open(self) -> None:
        if self._closed:
            raise Closed("proxy closed")
        if self._busy:
            raise RuntimeError("proxy does not support reentry")

    def read(self, key: Key, /) -> Document:
        self._require_idle_open()
        self._busy = True
        outcome: Outcome = "error"
        try:
            try:
                self._authorize(self._principal, key)
            except PermissionError:
                outcome = "denied"
                raise
            started = self._clock()
            entry = self._entry
            if entry is not None and entry.key == key and started - entry.started_at < self._ttl:
                outcome = "hit"
                return entry.document
            # A miss discards the old slot, even if the next load fails.
            self._entry = None
            if self._target is None:
                self._target = self._factory()
            document = self._target.read(key)
            if document.key != key:
                raise ContractError("catalog returned a different key")
            self._entry = Entry(key, document, started)
            outcome = "miss"
            return document
        finally:
            try:
                self._emit(Observation(outcome))
            finally:
                self._busy = False

    def _emit(self, event: Observation) -> None:
        try:
            self._observe(event)
        except Exception:
            self.observer_failures += 1

    def invalidate(self) -> None:
        """Owner-only administration by convention; retains the constructed target."""
        self._require_idle_open()
        self._entry = None

    def close(self) -> None:
        """Terminal even if target.close raises; repeated close does not retry it."""
        if self._closed:
            return
        self._require_idle_open()
        self._closed = True
        target, self._target = self._target, None
        self._entry = None
        if target is not None:
            target.close()
