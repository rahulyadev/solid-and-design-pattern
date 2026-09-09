"""Consumer-owned units, absence, and failure vocabulary; no vendor imports."""

from dataclasses import dataclass
from typing import Protocol


class StockUnavailable(Exception):
    """The provider could not answer; this is not evidence of zero stock."""


class InvalidStock(Exception):
    """The provider answered outside the agreed boundary contract."""


@dataclass(frozen=True)
class Stock:
    units: int | None

    def __post_init__(self) -> None:
        # bool is an int subclass; counts in this contract exclude it.
        if self.units is not None and (type(self.units) is not int or self.units < 0):
            raise ValueError("units must be a nonnegative integer or None")


class StockReader(Protocol):
    def read(self, sku: str, /) -> Stock:
        """Read once: None means unknown, zero means known empty; never reserve.

        Invalid input raises ValueError before I/O. Known boundary failures use
        StockUnavailable or InvalidStock. Each call is a fresh provider query.
        The reader borrows its provider and does not close it.
        """
        ...


def validate_sku(sku: str) -> None:
    """Exact uppercase ASCII identifier; reject rather than silently normalize."""
    if not 1 <= len(sku) <= 24 or any(
        c not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-" for c in sku
    ):
        raise ValueError("sku must contain 1-24 uppercase ASCII letters, digits, or hyphens")


def availability(reader: StockReader, sku: str, required: int) -> str:
    if type(required) is not int or required <= 0:
        raise ValueError("required must be a positive integer")
    stock = reader.read(sku)
    if stock.units is None:
        return "unknown"
    return "enough" if stock.units >= required else "short"
