"""Legacy starter for the independent SDP-PYT-050 practice lab.

The import-time application object and hidden lookup are intentional smells.
Preserve observable behavior before changing their lifetime and ownership.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AllocationRequest:
    order_id: str
    sku: str
    quantity: int


class AllocationSession:
    """Synthetic request resource; it performs no external I/O."""

    def __init__(self, endpoint: str, number: int, *, fail_sku: str | None = None) -> None:
        self.endpoint = endpoint
        self.number = number
        self.closed = False
        self.close_calls = 0
        self._fail_sku = fail_sku

    def allocate(self, request: AllocationRequest) -> str:
        if self.closed:
            raise RuntimeError("allocation session is closed")
        if request.sku == self._fail_sku:
            raise OSError(f"synthetic warehouse failure: {request.sku}")
        return (
            f"{request.order_id}:{request.sku}:{request.quantity}"
            f"@{self.endpoint}#session-{self.number}"
        )

    def close(self) -> None:
        self.close_calls += 1
        self.closed = True


class WarehouseGateway:
    """Synthetic application resource created implicitly by the legacy module."""

    def __init__(self, endpoint: str, *, fail_sku: str | None = None) -> None:
        self.endpoint = endpoint
        self.fail_sku = fail_sku
        self.sessions: list[AllocationSession] = []
        self.closed = False
        self.close_calls = 0

    def open_session(self) -> AllocationSession:
        if self.closed:
            raise RuntimeError("warehouse gateway is closed")
        session = AllocationSession(
            self.endpoint,
            len(self.sessions) + 1,
            fail_sku=self.fail_sku,
        )
        self.sessions.append(session)
        return session

    def close(self) -> None:
        self.close_calls += 1
        self.closed = True


# Deliberate legacy design: importing this module constructs live application state.
warehouse_gateway = WarehouseGateway("warehouse://primary")


def allocate_order(request: AllocationRequest) -> str:
    """Allocate through the hidden module dependency and a per-call session."""

    if request.quantity <= 0:
        raise ValueError("quantity must be positive")

    session = warehouse_gateway.open_session()
    try:
        return session.allocate(request)
    finally:
        session.close()


def main() -> None:
    print(allocate_order(AllocationRequest("order-1", "sku-1", 2)))


if __name__ == "__main__":
    main()
