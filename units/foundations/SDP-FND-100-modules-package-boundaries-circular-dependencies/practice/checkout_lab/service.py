"""Unsolved application service with a deliberate concrete-adapter import cycle."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from .email_adapter import send_receipt
from .model import Order


@dataclass(frozen=True, slots=True)
class CheckoutResult:
    """The value returned after a synthetic checkout completes."""

    order_id: str
    total: Decimal
    notification_reference: str


def checkout(order: Order) -> CheckoutResult:
    """Construct and send a result through a hard-coded concrete dependency."""

    pending = CheckoutResult(order.order_id, order.total, notification_reference="pending")
    reference = send_receipt(pending)
    return CheckoutResult(order.order_id, order.total, notification_reference=reference)
