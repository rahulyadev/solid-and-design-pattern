"""Synthetic email adapter that imports the service-owned result at runtime."""

from __future__ import annotations

from .service import CheckoutResult


def send_receipt(result: CheckoutResult) -> str:
    """Return a deterministic provider reference without performing network I/O."""

    return f"email:{result.order_id}"
