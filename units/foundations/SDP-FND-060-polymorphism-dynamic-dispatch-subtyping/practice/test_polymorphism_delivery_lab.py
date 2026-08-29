"""Characterization tests for the unsolved SDP-FND-060 delivery starter."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest
from polymorphism_delivery_lab import (
    DeliveryOption,
    DeliveryQuote,
    DeliveryRequest,
    PickupDelivery,
    PriorityDelivery,
    StandardDelivery,
    collect_quotes,
)


def test_current_catalog_quotes_two_known_runtime_types_in_input_order() -> None:
    request = DeliveryRequest("order-42", "metro", 1_250, fragile=True)

    quotes = collect_quotes(request, (StandardDelivery(), PriorityDelivery()))

    assert quotes == (
        DeliveryQuote("standard", True, 749, 3),
        DeliveryQuote("priority", True, 1_399, 1),
    )


def test_standard_delivery_handles_every_current_zone() -> None:
    option = StandardDelivery()

    quotes = tuple(
        option.quote(DeliveryRequest(f"order-{zone}", zone, 1_000))
        for zone in ("metro", "regional", "remote")
    )

    assert tuple(quote.fee_paise for quote in quotes) == (549, 749, 1_049)
    assert tuple(quote.eta_days for quote in quotes) == (3, 5, 8)


def test_priority_currently_rejects_a_valid_non_metro_request() -> None:
    request = DeliveryRequest("order-remote", "remote", 1_000)

    with pytest.raises(
        ValueError,
        match="priority delivery is unavailable outside metro",
    ):
        PriorityDelivery().quote(request)


def test_new_subclass_works_directly_but_central_dispatch_rejects_it() -> None:
    request = DeliveryRequest("order-42", "metro", 1_250)
    pickup = PickupDelivery()

    assert pickup.quote(request) == DeliveryQuote("pickup", True, 0, 0)
    with pytest.raises(TypeError, match="unsupported delivery option: PickupDelivery"):
        collect_quotes(request, (pickup,))


def test_nominal_relationships_exist_without_proving_behavioural_substitution() -> None:
    assert issubclass(StandardDelivery, DeliveryOption)
    assert issubclass(PriorityDelivery, DeliveryOption)
    assert issubclass(PickupDelivery, DeliveryOption)


def test_request_is_immutable_across_quote_calls() -> None:
    request = DeliveryRequest("order-42", "metro", 1_250)
    before = request

    StandardDelivery().quote(request)

    assert request == before
    with pytest.raises(FrozenInstanceError):
        request.zone = "remote"  # type: ignore[misc]


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"order_id": "", "zone": "metro", "weight_grams": 1}, "order_id must not be blank"),
        (
            {"order_id": "order-1", "zone": "unknown", "weight_grams": 1},
            "unsupported zone: unknown",
        ),
        (
            {"order_id": "order-1", "zone": "metro", "weight_grams": 0},
            "weight_grams must be positive",
        ),
    ],
)
def test_invalid_requests_are_rejected_before_dispatch(
    kwargs: dict[str, str | int],
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        DeliveryRequest(**kwargs)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "quote",
    [
        DeliveryQuote("standard", True, 0, 0),
        DeliveryQuote("priority", False, None, None, "outside service area"),
    ],
)
def test_quote_value_accepts_only_coherent_examples(quote: DeliveryQuote) -> None:
    assert quote.option_code


@pytest.mark.parametrize(
    ("args", "message"),
    [
        (("", True, 0, 0, None), "option_code must not be blank"),
        (("x", True, -1, 1, None), "available quote needs a non-negative fee"),
        (("x", True, 1, -1, None), "available quote needs a non-negative ETA"),
        (("x", True, 1, 1, "why"), "available quote must not contain a reason"),
        (("x", False, 1, None, "why"), "unavailable quote must not contain fee or ETA"),
        (("x", False, None, None, " "), "unavailable quote needs a reason"),
    ],
)
def test_quote_value_rejects_incoherent_states(
    args: tuple[str, bool, int | None, int | None, str | None],
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        DeliveryQuote(*args)
