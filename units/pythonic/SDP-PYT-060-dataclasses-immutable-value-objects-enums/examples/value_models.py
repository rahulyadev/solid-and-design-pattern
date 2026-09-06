"""Validated value objects and immutable quote snapshots for SDP-PYT-060."""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum, unique
from typing import TypedDict


@unique
class Currency(Enum):
    """Stable wire values accepted by this synthetic pricing boundary."""

    INR = "INR"
    USD = "USD"


@unique
class QuoteState(Enum):
    """The finite states represented by the snapshot."""

    DRAFT = "draft"
    CONFIRMED = "confirmed"


@dataclass(frozen=True, slots=True, kw_only=True)
class Money:
    """A monetary value stored in minor units; no floating-point rounding is needed."""

    minor_units: int
    currency: Currency

    def __post_init__(self) -> None:
        if isinstance(self.minor_units, bool) or not isinstance(self.minor_units, int):
            raise TypeError("minor_units must be an int, not bool")
        if self.minor_units < 0:
            raise ValueError("minor_units must be non-negative")
        if not isinstance(self.currency, Currency):
            raise TypeError("currency must be a Currency member")

    def times(self, quantity: int) -> Money:
        if isinstance(quantity, bool) or not isinstance(quantity, int):
            raise TypeError("quantity must be an int, not bool")
        if quantity <= 0:
            raise ValueError("quantity must be positive")
        return Money(minor_units=self.minor_units * quantity, currency=self.currency)


@dataclass(frozen=True, slots=True, kw_only=True)
class QuoteLine:
    """One validated line in a quote."""

    sku: str
    quantity: int
    unit_price: Money

    def __post_init__(self) -> None:
        if not self.sku or self.sku != self.sku.strip():
            raise ValueError("sku must be non-empty and have no surrounding whitespace")
        if isinstance(self.quantity, bool) or not isinstance(self.quantity, int):
            raise TypeError("quantity must be an int, not bool")
        if self.quantity <= 0:
            raise ValueError("quantity must be positive")
        if not isinstance(self.unit_price, Money):
            raise TypeError("unit_price must be Money")

    @property
    def subtotal(self) -> Money:
        return self.unit_price.times(self.quantity)


@dataclass(frozen=True, slots=True, kw_only=True)
class Quote:
    """A deeply immutable snapshot because every nested collection is a tuple."""

    quote_id: str
    lines: tuple[QuoteLine, ...]
    state: QuoteState = QuoteState.DRAFT
    revision: int = 1

    def __post_init__(self) -> None:
        if not self.quote_id or self.quote_id != self.quote_id.strip():
            raise ValueError("quote_id must be non-empty and have no surrounding whitespace")
        if not isinstance(self.lines, tuple):
            raise TypeError("lines must be a tuple")
        if not self.lines:
            raise ValueError("a quote must contain at least one line")
        if not all(isinstance(line, QuoteLine) for line in self.lines):
            raise TypeError("every line must be QuoteLine")
        if not isinstance(self.state, QuoteState):
            raise TypeError("state must be a QuoteState member")
        if isinstance(self.revision, bool) or not isinstance(self.revision, int):
            raise TypeError("revision must be an int, not bool")
        if self.revision <= 0:
            raise ValueError("revision must be positive")
        currencies = {line.unit_price.currency for line in self.lines}
        if len(currencies) != 1:
            raise ValueError("all quote lines must use one currency")

    @property
    def total(self) -> Money:
        first_currency = self.lines[0].unit_price.currency
        amount = sum(line.subtotal.minor_units for line in self.lines)
        return Money(minor_units=amount, currency=first_currency)

    def confirm(self) -> Quote:
        if self.state is not QuoteState.DRAFT:
            raise ValueError("only a draft quote can be confirmed")
        return replace(self, state=QuoteState.CONFIRMED, revision=self.revision + 1)


class QuoteLineRecord(TypedDict):
    sku: str
    quantity: int
    unit_minor_units: int
    currency: str


class QuoteRecord(TypedDict):
    quote_id: str
    state: str
    revision: int
    lines: list[QuoteLineRecord]


def quote_from_record(record: QuoteRecord) -> Quote:
    """Validate and normalize one transport record at the boundary."""

    lines = tuple(
        QuoteLine(
            sku=line["sku"],
            quantity=line["quantity"],
            unit_price=Money(
                minor_units=line["unit_minor_units"],
                currency=Currency(line["currency"]),
            ),
        )
        for line in record["lines"]
    )
    return Quote(
        quote_id=record["quote_id"],
        lines=lines,
        state=QuoteState(record["state"]),
        revision=record["revision"],
    )


def quote_to_record(quote: Quote) -> QuoteRecord:
    """Serialize explicitly instead of leaking dataclass implementation details."""

    return {
        "quote_id": quote.quote_id,
        "state": quote.state.value,
        "revision": quote.revision,
        "lines": [
            {
                "sku": line.sku,
                "quantity": line.quantity,
                "unit_minor_units": line.unit_price.minor_units,
                "currency": line.unit_price.currency.value,
            }
            for line in quote.lines
        ],
    }
