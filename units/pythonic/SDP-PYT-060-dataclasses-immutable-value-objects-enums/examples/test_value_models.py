"""Behavior tests for the worked immutable value model."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from enum import Enum

import pytest
from value_models import (
    Currency,
    Money,
    Quote,
    QuoteLine,
    QuoteRecord,
    QuoteState,
    quote_from_record,
    quote_to_record,
)


def money(amount: int, currency: Currency = Currency.INR) -> Money:
    return Money(minor_units=amount, currency=currency)


def line(sku: str = "book", quantity: int = 2, amount: int = 750) -> QuoteLine:
    return QuoteLine(sku=sku, quantity=quantity, unit_price=money(amount))


def quote() -> Quote:
    return Quote(quote_id="quote-1", lines=(line(), line("pen", 3, 125)))


def test_equal_values_have_equal_hashes_and_work_as_mapping_keys() -> None:
    first = money(750)
    second = money(750)

    assert first == second
    assert first is not second
    assert hash(first) == hash(second)
    assert {first: "known"}[second] == "known"


def test_keyword_only_construction_prevents_ambiguous_argument_order() -> None:
    with pytest.raises(TypeError):
        Money(750, Currency.INR)  # type: ignore[misc]


def test_frozen_blocks_field_rebinding() -> None:
    value = money(750)

    with pytest.raises(FrozenInstanceError):
        value.minor_units = 800  # type: ignore[misc]


@pytest.mark.parametrize("amount", [-1, True, 1.5])
def test_money_rejects_invalid_minor_units(amount: object) -> None:
    with pytest.raises((TypeError, ValueError)):
        Money(minor_units=amount, currency=Currency.INR)  # type: ignore[arg-type]


def test_quote_requires_one_currency_and_non_empty_lines() -> None:
    with pytest.raises(ValueError, match="at least one"):
        Quote(quote_id="quote-1", lines=())

    usd_line = QuoteLine(sku="usd", quantity=1, unit_price=money(100, Currency.USD))
    with pytest.raises(ValueError, match="one currency"):
        Quote(quote_id="quote-1", lines=(line(), usd_line))


def test_total_uses_minor_units_and_preserves_currency() -> None:
    total = quote().total

    assert total == money(1_875)


def test_confirmation_returns_a_new_snapshot_and_leaves_draft_unchanged() -> None:
    draft = quote()

    confirmed = draft.confirm()

    assert confirmed is not draft
    assert draft.state is QuoteState.DRAFT
    assert draft.revision == 1
    assert confirmed.state is QuoteState.CONFIRMED
    assert confirmed.revision == 2
    assert confirmed.lines is draft.lines


def test_confirming_an_already_confirmed_quote_is_rejected() -> None:
    with pytest.raises(ValueError, match="only a draft"):
        quote().confirm().confirm()


def test_boundary_parser_converts_wire_strings_and_lists_to_domain_types() -> None:
    record: QuoteRecord = {
        "quote_id": "quote-2",
        "state": "draft",
        "revision": 1,
        "lines": [
            {
                "sku": "वस्तु",
                "quantity": 1,
                "unit_minor_units": 999,
                "currency": "INR",
            }
        ],
    }

    parsed = quote_from_record(record)

    assert parsed.lines[0].sku == "वस्तु"
    assert parsed.state is QuoteState.DRAFT
    assert isinstance(parsed.lines, tuple)
    assert quote_to_record(parsed) == record


def test_unknown_enum_wire_value_fails_at_the_boundary() -> None:
    record: QuoteRecord = {
        "quote_id": "quote-2",
        "state": "waiting",
        "revision": 1,
        "lines": [
            {
                "sku": "book",
                "quantity": 1,
                "unit_minor_units": 999,
                "currency": "INR",
            }
        ],
    }

    with pytest.raises(ValueError, match="waiting"):
        quote_from_record(record)


def test_enum_member_is_not_interchangeable_with_another_enum_type() -> None:
    class ExternalState(Enum):
        DRAFT = "draft"

    state: object = QuoteState.DRAFT
    external_state: object = ExternalState.DRAFT

    assert QuoteState.DRAFT.value == ExternalState.DRAFT.value
    assert state != external_state


def test_quote_rejects_a_list_even_though_frozen_blocks_only_rebinding() -> None:
    with pytest.raises(TypeError, match="tuple"):
        Quote(quote_id="quote-1", lines=[line()])  # type: ignore[arg-type]
