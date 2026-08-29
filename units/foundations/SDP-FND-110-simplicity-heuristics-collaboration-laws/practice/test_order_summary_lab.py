"""Stable behaviour and edge cases for the unsolved simplicity lab."""

from __future__ import annotations

from collections.abc import Callable
from decimal import Decimal

import pytest
from order_summary_lab import (
    Account,
    Address,
    Contact,
    Customer,
    Order,
    OrderCalculator,
    OrderLine,
    build_order_summary,
)


def make_order(
    *,
    order_id: str = "order-7",
    customer_id: str = "customer-3",
    tier: str = "PLUS",
    loyalty_points: int = 1_200,
    country_code: str = "GB",
    email: str = "rahul@example.test",
    lines: tuple[OrderLine, ...] | None = None,
) -> Order:
    selected_lines = lines or (
        OrderLine("book", 2, Decimal("25.00")),
        OrderLine("pen", 2, Decimal("5.00")),
    )
    return Order(
        order_id=order_id,
        customer=Customer(
            customer_id=customer_id,
            account=Account(
                account_id="account-9",
                tier=tier,
                loyalty_points=loyalty_points,
                contact=Contact(email),
                billing_address=Address(country_code),
            ),
        ),
        lines=selected_lines,
    )


def test_current_plus_customer_total_has_discount_and_free_shipping() -> None:
    order = make_order()

    assert OrderCalculator().total(order) == Decimal("54.00")


def test_current_text_summary_is_a_stable_public_result() -> None:
    order = make_order()

    assert build_order_summary(order) == "\n".join(
        (
            "order=order-7",
            "customer=customer-3",
            "email=rahul@example.test",
            "tier=PLUS",
            "country=GB",
            "support=priority",
            "subtotal=60.00",
            "discount=6.00",
            "shipping=0.00",
            "total=54.00",
        )
    )


def test_domestic_order_below_threshold_pays_shipping() -> None:
    order = make_order(
        loyalty_points=999,
        lines=(OrderLine("notebook", 1, Decimal("20.00")),),
    )

    assert OrderCalculator().total(order) == Decimal("25.00")
    assert "support=standard" in build_order_summary(order)
    assert "shipping=5.00" in build_order_summary(order)


def test_international_order_pays_international_shipping() -> None:
    order = make_order(country_code="IN")

    assert OrderCalculator().total(order) == Decimal("69.00")
    assert "country=IN" in build_order_summary(order)
    assert "shipping=15.00" in build_order_summary(order)


def test_zero_priced_line_is_valid() -> None:
    order = make_order(
        loyalty_points=0,
        lines=(OrderLine("sample", 1, Decimal("0.00")),),
    )

    assert OrderCalculator().total(order) == Decimal("5.00")
    assert "subtotal=0.00" in build_order_summary(order)


def test_money_rounding_is_explicit_and_stable() -> None:
    order = make_order(
        loyalty_points=1_000,
        lines=(OrderLine("fractional", 3, Decimal("0.335")),),
    )

    assert OrderCalculator().total(order) == Decimal("5.91")
    assert "subtotal=1.01" in build_order_summary(order)
    assert "discount=0.10" in build_order_summary(order)
    assert "total=5.91" in build_order_summary(order)


def test_only_text_representation_exists_today() -> None:
    with pytest.raises(ValueError, match="unsupported representation: json"):
        build_order_summary(make_order(), representation="json")


@pytest.mark.parametrize(
    ("factory", "message"),
    [
        (lambda: Address("GBR"), "country_code must contain two letters"),
        (lambda: Address("gb"), "country_code must be uppercase"),
        (lambda: Contact(" "), "email must contain a non-blank address"),
        (lambda: Contact("missing-at"), "email must contain a non-blank address"),
        (
            lambda: Account(
                "account-1",
                "UNKNOWN",
                0,
                Contact("a@example.test"),
                Address("GB"),
            ),
            "tier must be STANDARD or PLUS",
        ),
        (
            lambda: Account(
                "account-1",
                "STANDARD",
                -1,
                Contact("a@example.test"),
                Address("GB"),
            ),
            "loyalty_points must not be negative",
        ),
        (
            lambda: Customer(
                " ",
                Account(
                    "account-1",
                    "STANDARD",
                    0,
                    Contact("a@example.test"),
                    Address("GB"),
                ),
            ),
            "customer_id must not be blank",
        ),
        (lambda: OrderLine(" ", 1, Decimal("1.00")), "sku must not be blank"),
        (lambda: OrderLine("sku", 0, Decimal("1.00")), "quantity must be positive"),
        (lambda: OrderLine("sku", -1, Decimal("1.00")), "quantity must be positive"),
        (lambda: OrderLine("sku", 1, Decimal("-0.01")), "unit_price must not be negative"),
        (
            lambda: make_order(order_id=" "),
            "order_id must not be blank",
        ),
        (
            lambda: Order(
                "order-1",
                Customer(
                    "customer-1",
                    Account(
                        "account-1",
                        "STANDARD",
                        0,
                        Contact("a@example.test"),
                        Address("GB"),
                    ),
                ),
                (),
            ),
            "order must contain at least one line",
        ),
    ],
)
def test_invalid_values_are_rejected(
    factory: Callable[[], object],
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        factory()
