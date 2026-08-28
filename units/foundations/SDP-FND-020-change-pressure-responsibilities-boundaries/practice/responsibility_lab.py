"""Unsolved SDP-FND-020 starter: expose mixed checkout responsibilities."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class CheckoutRequest:
    """Transport-neutral input used by the deliberately mixed starter."""

    order_id: str
    customer_id: str
    email: str
    items: tuple[tuple[str, int, int], ...]
    payment_method: str


@dataclass
class RecordedEffects:
    """In-memory substitutes that make starter effects observable."""

    payments: list[dict[str, object]] = field(default_factory=list)
    orders: list[dict[str, object]] = field(default_factory=list)
    receipts: list[dict[str, object]] = field(default_factory=list)


def place_order(
    request: CheckoutRequest,
    effects: RecordedEffects,
) -> dict[str, object]:
    """Place one order while deliberately owning too many changing decisions."""

    subtotal = sum(unit_price * quantity for _, unit_price, quantity in request.items)
    discount = subtotal // 10 if request.customer_id.startswith("LOYAL-") else 0
    total = subtotal - discount

    if request.payment_method == "card":
        payment_reference = f"card:{request.order_id}:{total}"
    elif request.payment_method == "bank_transfer":
        payment_reference = f"bank:{total}:{request.order_id}"
    else:
        raise ValueError(f"unsupported payment method: {request.payment_method}")

    effects.payments.append(
        {
            "order_id": request.order_id,
            "method": request.payment_method,
            "amount": total,
            "reference": payment_reference,
        }
    )

    order_record: dict[str, object] = {
        "id": request.order_id,
        "customer_id": request.customer_id,
        "subtotal": subtotal,
        "discount": discount,
        "total": total,
        "payment_reference": payment_reference,
        "item_count": sum(quantity for _, _, quantity in request.items),
    }
    effects.orders.append(order_record)

    effects.receipts.append(
        {
            "to": request.email,
            "subject": f"Receipt for {request.order_id}",
            "body": f"Paid {total}",
        }
    )
    return order_record


def example_request() -> CheckoutRequest:
    """Return synthetic data for prediction and manual observation."""

    return CheckoutRequest(
        order_id="ORD-100",
        customer_id="LOYAL-7",
        email="learner@example.test",
        items=(("notebook", 700, 2), ("pen", 125, 3)),
        payment_method="card",
    )


def main() -> None:
    """Run the mixed starter once and print all observable outcomes."""

    effects = RecordedEffects()
    result = place_order(example_request(), effects)
    print(f"result: {result}")
    print(f"payments: {effects.payments}")
    print(f"orders: {effects.orders}")
    print(f"receipts: {effects.receipts}")


if __name__ == "__main__":
    main()
