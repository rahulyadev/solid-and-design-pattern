"""Characterization tests for the unsolved SDP-FND-020 starter."""

import pytest
from responsibility_lab import CheckoutRequest, RecordedEffects, place_order


def test_regular_checkout_records_each_effect_once() -> None:
    effects = RecordedEffects()
    request = CheckoutRequest(
        order_id="ORD-1",
        customer_id="NEW-1",
        email="new@example.test",
        items=(("book", 500, 2), ("pen", 100, 3)),
        payment_method="card",
    )

    result = place_order(request, effects)

    assert result == {
        "id": "ORD-1",
        "customer_id": "NEW-1",
        "subtotal": 1300,
        "discount": 0,
        "total": 1300,
        "payment_reference": "card:ORD-1:1300",
        "item_count": 5,
    }
    assert effects.orders == [result]
    assert effects.payments == [
        {
            "order_id": "ORD-1",
            "method": "card",
            "amount": 1300,
            "reference": "card:ORD-1:1300",
        }
    ]
    assert effects.receipts == [
        {
            "to": "new@example.test",
            "subject": "Receipt for ORD-1",
            "body": "Paid 1300",
        }
    ]


def test_loyalty_discount_uses_integer_ten_percent() -> None:
    effects = RecordedEffects()
    request = CheckoutRequest(
        order_id="ORD-2",
        customer_id="LOYAL-2",
        email="loyal@example.test",
        items=(("case", 999, 1),),
        payment_method="bank_transfer",
    )

    result = place_order(request, effects)

    assert result["subtotal"] == 999
    assert result["discount"] == 99
    assert result["total"] == 900
    assert result["payment_reference"] == "bank:900:ORD-2"


def test_empty_order_preserves_the_characterized_zero_total() -> None:
    effects = RecordedEffects()
    request = CheckoutRequest(
        order_id="ORD-EMPTY",
        customer_id="NEW-2",
        email="empty@example.test",
        items=(),
        payment_method="card",
    )

    result = place_order(request, effects)

    assert result["subtotal"] == 0
    assert result["total"] == 0
    assert result["item_count"] == 0


def test_unsupported_payment_method_has_no_recorded_effects() -> None:
    effects = RecordedEffects()
    request = CheckoutRequest(
        order_id="ORD-3",
        customer_id="NEW-3",
        email="unknown@example.test",
        items=(("book", 500, 1),),
        payment_method="cash_on_delivery",
    )

    with pytest.raises(ValueError, match="unsupported payment method: cash_on_delivery"):
        place_order(request, effects)

    assert effects.payments == []
    assert effects.orders == []
    assert effects.receipts == []
