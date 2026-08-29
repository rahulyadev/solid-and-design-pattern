"""Executable surface for the deliberately broken checkout package."""

from decimal import Decimal

from .model import Order, OrderLine
from .service import checkout

order = Order("order-7", (OrderLine("sku-book", 2, Decimal("12.50")),))
result = checkout(order)
print(f"order_id={result.order_id}")
print(f"total={result.total}")
print(f"notification_reference={result.notification_reference}")
