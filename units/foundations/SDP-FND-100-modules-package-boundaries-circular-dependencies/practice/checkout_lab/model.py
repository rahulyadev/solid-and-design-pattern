"""Stable values that remain importable while the checkout service cycle is broken."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class OrderLine:
    """One validated line in a synthetic order."""

    sku: str
    quantity: int
    unit_price: Decimal

    def __post_init__(self) -> None:
        if not self.sku.strip():
            raise ValueError("sku must not be blank")
        if self.quantity <= 0:
            raise ValueError("quantity must be positive")
        if self.unit_price < 0:
            raise ValueError("unit_price must not be negative")

    @property
    def subtotal(self) -> Decimal:
        """Return the exact decimal subtotal for this line."""

        return self.quantity * self.unit_price


@dataclass(frozen=True, slots=True)
class Order:
    """A small immutable order value used by the boundary exercise."""

    order_id: str
    lines: tuple[OrderLine, ...]

    def __post_init__(self) -> None:
        if not self.order_id.strip():
            raise ValueError("order_id must not be blank")
        if not self.lines:
            raise ValueError("order must contain at least one line")

    @property
    def total(self) -> Decimal:
        """Return the sum of line subtotals."""

        return sum((line.subtotal for line in self.lines), start=Decimal("0"))
