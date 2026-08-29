"""Stable model tests and defect characterization for the unsolved checkout package."""

from __future__ import annotations

import subprocess
import sys
from decimal import Decimal
from pathlib import Path

import pytest
from checkout_lab.model import Order, OrderLine

PRACTICE_DIR = Path(__file__).resolve().parent


def test_order_total_remains_available_without_importing_the_broken_service() -> None:
    order = Order(
        "order-7",
        (
            OrderLine("sku-book", 2, Decimal("12.50")),
            OrderLine("sku-pen", 3, Decimal("1.25")),
        ),
    )

    assert order.total == Decimal("28.75")


@pytest.mark.parametrize(
    ("line", "message"),
    [
        (lambda: OrderLine(" ", 1, Decimal("1")), "sku must not be blank"),
        (lambda: OrderLine("sku-a", 0, Decimal("1")), "quantity must be positive"),
        (lambda: OrderLine("sku-a", -1, Decimal("1")), "quantity must be positive"),
        (lambda: OrderLine("sku-a", 1, Decimal("-0.01")), "unit_price must not be negative"),
    ],
)
def test_order_line_rejects_invalid_values_today(
    line: object,
    message: str,
) -> None:
    factory = line
    assert callable(factory)
    with pytest.raises(ValueError, match=message):
        factory()


@pytest.mark.parametrize(
    ("order_id", "lines", "message"),
    [
        ("", (OrderLine("sku-a", 1, Decimal("1")),), "order_id must not be blank"),
        ("order-1", (), "order must contain at least one line"),
    ],
)
def test_order_rejects_invalid_values_today(
    order_id: str,
    lines: tuple[OrderLine, ...],
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        Order(order_id, lines)


def test_service_import_exposes_the_deliberate_cycle_today() -> None:
    completed = subprocess.run(
        [sys.executable, "-c", "from checkout_lab.service import checkout"],
        cwd=PRACTICE_DIR,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode != 0
    assert "ImportError" in completed.stderr
    assert "partially initialized module" in completed.stderr
    assert "CheckoutResult" in completed.stderr


def test_package_entrypoint_exposes_the_same_cycle_today() -> None:
    completed = subprocess.run(
        [sys.executable, "-m", "checkout_lab"],
        cwd=PRACTICE_DIR,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode != 0
    assert completed.stdout == ""
    assert "partially initialized module" in completed.stderr
