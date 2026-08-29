"""Unsolved SDP-FND-090 lab: make cart-state ownership and lifetime explicit.

The starter deliberately combines several aliasing hazards. Its behavior is deterministic and
characterized by tests, but it is not the recommended design. Preserve the learner's first
attempt before replacing the defective public contracts.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CartLine:
    """A deliberately mutable line whose nested attributes are also shared by reference."""

    sku: str
    quantity: int
    attributes: dict[str, str]

    def __post_init__(self) -> None:
        if not self.sku.strip():
            raise ValueError("sku must not be blank")
        if self.quantity <= 0:
            raise ValueError("quantity must be positive")


class CartStore:
    """Keep carts in a registry whose owner and lifetime are intentionally ambiguous."""

    def __init__(
        self,
        carts: dict[str, list[CartLine]] = {},  # noqa: B006 - deliberate lab defect
    ) -> None:
        self._carts = carts

    def add_line(
        self,
        cart_id: str,
        sku: str,
        quantity: int,
        attributes: dict[str, str] | None = None,
    ) -> CartLine:
        """Add a line while retaining aliases to both the line and its nested attributes."""

        if not cart_id.strip():
            raise ValueError("cart_id must not be blank")
        line = CartLine(
            sku=sku,
            quantity=quantity,
            attributes=attributes if attributes is not None else {},
        )
        self._carts.setdefault(cart_id, []).append(line)
        return line

    def lines(self, cart_id: str) -> list[CartLine]:
        """Return the live internal list, giving every caller mutation authority."""

        if not cart_id.strip():
            raise ValueError("cart_id must not be blank")
        return self._carts.setdefault(cart_id, [])

    def snapshot(self, cart_id: str) -> list[CartLine]:
        """Copy only the outer list; contained mutable lines remain shared."""

        return list(self.lines(cart_id))

    def delete(self, cart_id: str) -> None:
        """Drop the registry entry without invalidating aliases already handed to callers."""

        self._carts.pop(cart_id, None)


def main() -> None:
    """Expose the starter's three ownership defects with deterministic observations."""

    first_store = CartStore()
    second_store = CartStore()
    supplied_attributes = {"gift_wrap": "no"}

    returned_line = first_store.add_line("cart-7", "sku-book", 1, supplied_attributes)
    shallow_snapshot = first_store.snapshot("cart-7")

    second_store.lines("cart-7")[0].quantity = 9
    supplied_attributes["gift_wrap"] = "yes"

    print(f"default_registry_shared={first_store._carts is second_store._carts}")
    print(f"returned_line_quantity={returned_line.quantity}")
    print(f"snapshot_gift_wrap={shallow_snapshot[0].attributes['gift_wrap']}")


if __name__ == "__main__":
    main()
