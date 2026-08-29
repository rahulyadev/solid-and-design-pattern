"""Correct starter behaviour with deliberately mixed design decisions.

Read practice/README.md and record a prediction before changing this file.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

CENT = Decimal("0.01")


def as_money(value: Decimal) -> Decimal:
    """Return a currency-shaped value using the lab's explicit rounding rule."""
    return value.quantize(CENT, rounding=ROUND_HALF_UP)


@dataclass(frozen=True)
class Address:
    country_code: str

    def __post_init__(self) -> None:
        if len(self.country_code) != 2 or not self.country_code.isalpha():
            raise ValueError("country_code must contain two letters")
        if self.country_code != self.country_code.upper():
            raise ValueError("country_code must be uppercase")


@dataclass(frozen=True)
class Contact:
    email: str

    def __post_init__(self) -> None:
        if not self.email.strip() or "@" not in self.email:
            raise ValueError("email must contain a non-blank address")


@dataclass(frozen=True)
class Account:
    account_id: str
    tier: str
    loyalty_points: int
    contact: Contact
    billing_address: Address

    def __post_init__(self) -> None:
        if not self.account_id.strip():
            raise ValueError("account_id must not be blank")
        if self.tier not in {"STANDARD", "PLUS"}:
            raise ValueError("tier must be STANDARD or PLUS")
        if self.loyalty_points < 0:
            raise ValueError("loyalty_points must not be negative")


@dataclass(frozen=True)
class Customer:
    customer_id: str
    account: Account

    def __post_init__(self) -> None:
        if not self.customer_id.strip():
            raise ValueError("customer_id must not be blank")


@dataclass(frozen=True)
class OrderLine:
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


@dataclass(frozen=True)
class Order:
    order_id: str
    customer: Customer
    lines: tuple[OrderLine, ...]

    def __post_init__(self) -> None:
        if not self.order_id.strip():
            raise ValueError("order_id must not be blank")
        if not self.lines:
            raise ValueError("order must contain at least one line")


class OrderCalculator:
    """Current calculation surface used by the text summary subtype."""

    def total(self, order: Order) -> Decimal:
        subtotal = as_money(
            sum(
                (line.unit_price * line.quantity for line in order.lines),
                start=Decimal("0"),
            )
        )

        if order.customer.account.loyalty_points >= 1_000:
            discount = as_money(subtotal * Decimal("0.10"))
        else:
            discount = Decimal("0.00")

        if order.customer.account.billing_address.country_code == "GB":
            shipping = Decimal("0.00") if subtotal >= Decimal("50.00") else Decimal("5.00")
        else:
            shipping = Decimal("15.00")

        return as_money(subtotal - discount + shipping)


class TextOrderSummary(OrderCalculator):
    """Render the only currently supported representation."""

    def render(self, order: Order) -> str:
        subtotal = as_money(
            sum(
                (line.unit_price * line.quantity for line in order.lines),
                start=Decimal("0"),
            )
        )

        if order.customer.account.loyalty_points >= 1_000:
            discount = as_money(subtotal * Decimal("0.10"))
        else:
            discount = Decimal("0.00")

        if order.customer.account.billing_address.country_code == "GB":
            shipping = Decimal("0.00") if subtotal >= Decimal("50.00") else Decimal("5.00")
        else:
            shipping = Decimal("15.00")

        total = as_money(subtotal - discount + shipping)
        support_lane = (
            "priority" if order.customer.account.loyalty_points >= 1_000 else "standard"
        )

        return "\n".join(
            (
                f"order={order.order_id}",
                f"customer={order.customer.customer_id}",
                f"email={order.customer.account.contact.email}",
                f"tier={order.customer.account.tier}",
                f"country={order.customer.account.billing_address.country_code}",
                f"support={support_lane}",
                f"subtotal={subtotal:.2f}",
                f"discount={discount:.2f}",
                f"shipping={shipping:.2f}",
                f"total={total:.2f}",
            )
        )


def build_order_summary(order: Order, *, representation: str = "text") -> str:
    """Build the one supported representation through the current public API."""
    if representation != "text":
        raise ValueError(f"unsupported representation: {representation}")
    return TextOrderSummary().render(order)


def sample_order() -> Order:
    """Return deterministic data for the manual runner."""
    return Order(
        order_id="order-7",
        customer=Customer(
            customer_id="customer-3",
            account=Account(
                account_id="account-9",
                tier="PLUS",
                loyalty_points=1_200,
                contact=Contact("rahul@example.test"),
                billing_address=Address("GB"),
            ),
        ),
        lines=(
            OrderLine("book", 2, Decimal("25.00")),
            OrderLine("pen", 2, Decimal("5.00")),
        ),
    )


if __name__ == "__main__":
    print(build_order_summary(sample_order()))
