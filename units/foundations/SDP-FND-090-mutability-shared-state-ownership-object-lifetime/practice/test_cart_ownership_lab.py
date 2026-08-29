"""Characterization tests for the unsolved SDP-FND-090 cart ownership lab."""

from __future__ import annotations

from typing import Any

import pytest
from cart_ownership_lab import CartLine, CartStore


def test_default_constructed_stores_share_one_registry_today() -> None:
    first = CartStore()
    second = CartStore()

    first.add_line("cart-shared", "sku-a", 1)

    assert second.lines("cart-shared")[0].sku == "sku-a"


def test_explicit_registries_isolate_stores_today() -> None:
    first = CartStore(carts={})
    second = CartStore(carts={})

    first.add_line("cart-isolated", "sku-a", 1)

    assert second.lines("cart-isolated") == []


def test_lines_returns_a_live_mutable_alias_today() -> None:
    store = CartStore(carts={})
    exposed = store.lines("cart-live")

    exposed.append(CartLine("sku-bypass", 3, {}))

    assert store.snapshot("cart-live")[0].sku == "sku-bypass"


def test_shallow_snapshot_detaches_outer_list_but_not_lines_today() -> None:
    store = CartStore(carts={})
    store.add_line("cart-copy", "sku-a", 1, {"color": "blue"})
    snapshot = store.snapshot("cart-copy")

    snapshot.clear()
    assert len(store.lines("cart-copy")) == 1

    second_snapshot = store.snapshot("cart-copy")
    second_snapshot[0].quantity = 8
    second_snapshot[0].attributes["color"] = "red"

    assert store.lines("cart-copy")[0].quantity == 8
    assert store.lines("cart-copy")[0].attributes == {"color": "red"}


def test_input_attributes_and_returned_line_remain_aliased_today() -> None:
    store = CartStore(carts={})
    supplied = {"gift_wrap": "no"}

    returned = store.add_line("cart-input", "sku-a", 1, supplied)
    supplied["gift_wrap"] = "yes"
    returned.quantity = 5

    stored = store.lines("cart-input")[0]
    assert stored is returned
    assert stored.attributes is supplied
    assert (stored.quantity, stored.attributes["gift_wrap"]) == (5, "yes")


def test_delete_drops_registry_entry_but_not_an_existing_alias() -> None:
    store = CartStore(carts={})
    store.add_line("cart-delete", "sku-a", 1)
    old_alias = store.lines("cart-delete")

    store.delete("cart-delete")

    assert store.lines("cart-delete") == []
    assert [line.sku for line in old_alias] == ["sku-a"]


@pytest.mark.parametrize(
    ("cart_id", "sku", "quantity", "message"),
    [
        ("", "sku-a", 1, "cart_id must not be blank"),
        ("cart-1", " ", 1, "sku must not be blank"),
        ("cart-1", "sku-a", 0, "quantity must be positive"),
        ("cart-1", "sku-a", -1, "quantity must be positive"),
    ],
)
def test_invalid_additions_do_not_create_a_cart(
    cart_id: str,
    sku: str,
    quantity: int,
    message: str,
) -> None:
    store = CartStore(carts={})

    with pytest.raises(ValueError, match=message):
        store.add_line(cart_id, sku, quantity)

    assert store._carts == {}


@pytest.mark.parametrize("cart_id", ["", "   "])
def test_blank_cart_lookup_is_rejected(cart_id: str) -> None:
    store = CartStore(carts={})

    with pytest.raises(ValueError, match="cart_id must not be blank"):
        store.lines(cart_id)


def test_cart_line_rejects_invalid_constructor_values() -> None:
    invalid_cases: list[tuple[dict[str, Any], str]] = [
        ({"sku": "", "quantity": 1, "attributes": {}}, "sku must not be blank"),
        ({"sku": "sku-a", "quantity": 0, "attributes": {}}, "quantity must be positive"),
    ]

    for kwargs, message in invalid_cases:
        with pytest.raises(ValueError, match=message):
            CartLine(**kwargs)
