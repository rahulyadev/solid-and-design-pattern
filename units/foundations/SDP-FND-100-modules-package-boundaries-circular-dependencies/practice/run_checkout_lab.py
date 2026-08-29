"""Start the unsolved checkout package from the practice directory on sys.path."""

from decimal import Decimal

from checkout_lab.model import Order, OrderLine
from checkout_lab.service import checkout


def main() -> None:
    """Run one deterministic synthetic checkout after the import boundary is repaired."""

    order = Order("order-7", (OrderLine("sku-book", 2, Decimal("12.50")),))
    result = checkout(order)
    print(f"order_id={result.order_id}")
    print(f"total={result.total}")
    print(f"notification_reference={result.notification_reference}")


if __name__ == "__main__":
    main()
