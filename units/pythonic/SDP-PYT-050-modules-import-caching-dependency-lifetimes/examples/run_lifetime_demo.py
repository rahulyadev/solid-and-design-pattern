"""Run the explicit lifetime example for SDP-PYT-050."""

from __future__ import annotations

from service_lifetimes import (
    MemorySessionPool,
    Settings,
    application_lifespan,
    build_usage_view,
)


def main() -> None:
    events: list[str] = []
    pool = MemorySessionPool({"acct-1": 7})

    with application_lifespan(
        Settings("usage-api", monthly_limit=10),
        lambda: pool,
        trace=events.append,
    ) as application:
        for account_id in ("acct-1", "acct-2"):
            with application.request_scope() as services:
                view = build_usage_view(account_id, services)
                print(f"{view.account_id}: used={view.used}, remaining={view.remaining}")

    print(f"sessions={len(pool.sessions)}, pool_closed={pool.closed}")
    print(" -> ".join(events))


if __name__ == "__main__":
    main()
