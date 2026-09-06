"""Explicit application and request lifetimes for SDP-PYT-050.

The module declares types and factories but deliberately creates no live resource
at import time.  The composition root chooses when the application starts.
"""

from __future__ import annotations

from collections.abc import Callable, Iterator, Mapping
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Protocol

Trace = Callable[[str], None]


def _ignore(_message: str) -> None:
    """Default trace callback."""


class UsageSession(Protocol):
    """Small request-scoped capability used by the service."""

    def read_usage(self, account_id: str) -> int: ...

    def close(self) -> None: ...


class SessionPool(Protocol):
    """Application-scoped owner that can create request sessions."""

    def open_session(self) -> UsageSession: ...

    def close(self) -> None: ...


@dataclass(frozen=True)
class Settings:
    application_name: str
    monthly_limit: int

    def __post_init__(self) -> None:
        if self.monthly_limit < 0:
            raise ValueError("monthly_limit must be non-negative")


@dataclass(frozen=True)
class UsageView:
    account_id: str
    used: int
    remaining: int


@dataclass(frozen=True)
class RequestServices:
    settings: Settings
    session: UsageSession


class ApplicationRuntime:
    """Explicit owner of objects shared for one application run."""

    def __init__(
        self,
        settings: Settings,
        pool: SessionPool,
        *,
        trace: Trace = _ignore,
    ) -> None:
        self.settings = settings
        self.pool = pool
        self._trace = trace
        self._closed = False

    @property
    def closed(self) -> bool:
        return self._closed

    @contextmanager
    def request_scope(self) -> Iterator[RequestServices]:
        """Open one request session and close it on every body exit."""

        if self._closed:
            raise RuntimeError("application runtime is closed")

        session = self.pool.open_session()
        try:
            self._trace("request:start")
            yield RequestServices(self.settings, session)
        finally:
            session.close()
            self._trace("request:stop")

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        self.pool.close()


@contextmanager
def application_lifespan(
    settings: Settings,
    pool_factory: Callable[[], SessionPool],
    *,
    trace: Trace = _ignore,
) -> Iterator[ApplicationRuntime]:
    """Own one application runtime from startup through deterministic shutdown."""

    pool = pool_factory()
    runtime = ApplicationRuntime(settings, pool, trace=trace)
    try:
        trace("application:start")
        yield runtime
    finally:
        runtime.close()
        trace("application:stop")


def build_usage_view(account_id: str, services: RequestServices) -> UsageView:
    """Application policy with every live dependency passed explicitly."""

    used = services.session.read_usage(account_id)
    if used < 0:
        raise ValueError("usage cannot be negative")
    remaining = max(0, services.settings.monthly_limit - used)
    return UsageView(account_id, used, remaining)


class MemoryUsageSession:
    """Observable synthetic session; no database or network is involved."""

    def __init__(self, usage: Mapping[str, int], number: int) -> None:
        self._usage = usage
        self.number = number
        self.closed = False
        self.close_calls = 0

    def read_usage(self, account_id: str) -> int:
        if self.closed:
            raise RuntimeError("session is closed")
        return self._usage.get(account_id, 0)

    def close(self) -> None:
        self.close_calls += 1
        self.closed = True


class MemorySessionPool:
    """Observable application resource used by the example and its tests."""

    def __init__(self, usage: Mapping[str, int]) -> None:
        self._usage = dict(usage)
        self.sessions: list[MemoryUsageSession] = []
        self.closed = False
        self.close_calls = 0

    def open_session(self) -> MemoryUsageSession:
        if self.closed:
            raise RuntimeError("pool is closed")
        session = MemoryUsageSession(self._usage, len(self.sessions) + 1)
        self.sessions.append(session)
        return session

    def close(self) -> None:
        self.close_calls += 1
        self.closed = True
