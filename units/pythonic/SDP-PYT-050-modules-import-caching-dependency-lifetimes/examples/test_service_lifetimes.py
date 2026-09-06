"""Behavior tests for explicit dependency lifetimes."""

from __future__ import annotations

import pytest
from service_lifetimes import (
    MemorySessionPool,
    RequestServices,
    Settings,
    application_lifespan,
    build_usage_view,
)


def test_application_resource_is_reused_but_request_sessions_are_distinct() -> None:
    pool = MemorySessionPool({"acct": 7})
    settings = Settings("usage-api", monthly_limit=10)

    with application_lifespan(settings, lambda: pool) as application:
        with application.request_scope() as first:
            first_session = first.session
            assert build_usage_view("acct", first).remaining == 3

        with application.request_scope() as second:
            second_session = second.session
            assert build_usage_view("missing", second).used == 0

        assert application.pool is pool
        assert first.settings is second.settings is settings
        assert first_session is not second_session
        assert pool.closed is False

    assert [session.close_calls for session in pool.sessions] == [1, 1]
    assert pool.close_calls == 1


def test_request_failure_closes_session_and_preserves_exception_identity() -> None:
    pool = MemorySessionPool({})
    original = LookupError("synthetic handler failure")

    with (
        application_lifespan(Settings("usage-api", 10), lambda: pool) as application,
        pytest.raises(LookupError) as captured,
        application.request_scope(),
    ):
        raise original

    assert captured.value is original
    assert pool.sessions[0].close_calls == 1
    assert pool.close_calls == 1


def test_application_failure_closes_pool_and_preserves_exception_identity() -> None:
    pool = MemorySessionPool({})
    original = RuntimeError("synthetic startup body failure")

    with (
        pytest.raises(RuntimeError) as captured,
        application_lifespan(Settings("usage-api", 10), lambda: pool),
    ):
        raise original

    assert captured.value is original
    assert pool.close_calls == 1


def test_closed_application_rejects_new_request_scope() -> None:
    pool = MemorySessionPool({})
    with application_lifespan(Settings("usage-api", 10), lambda: pool) as application:
        pass

    with (
        pytest.raises(RuntimeError, match="application runtime is closed"),
        application.request_scope(),
    ):
        pass

    assert pool.sessions == []


def test_invalid_settings_fail_before_pool_factory_is_called() -> None:
    factory_calls = 0

    def factory() -> MemorySessionPool:
        nonlocal factory_calls
        factory_calls += 1
        return MemorySessionPool({})

    with pytest.raises(ValueError, match="monthly_limit must be non-negative"):
        Settings("usage-api", -1)

    assert factory_calls == 0


def test_negative_usage_is_rejected_without_hiding_the_supplied_session() -> None:
    pool = MemorySessionPool({"broken": -1})
    session = pool.open_session()
    services = RequestServices(Settings("usage-api", 10), session)

    with pytest.raises(ValueError, match="usage cannot be negative"):
        build_usage_view("broken", services)

    assert session.closed is False


def test_trace_reconstructs_nested_lifetimes() -> None:
    events: list[str] = []
    pool = MemorySessionPool({})

    with (
        application_lifespan(
            Settings("usage-api", 10),
            lambda: pool,
            trace=events.append,
        ) as application,
        application.request_scope(),
    ):
        events.append("handler")

    assert events == [
        "application:start",
        "request:start",
        "handler",
        "request:stop",
        "application:stop",
    ]
