"""Characterization tests for the unsolved SDP-FND-030 starter."""

import pytest
from acme_carrier import AcmeCarrierClient, AcmeRate, AcmeRequest, AcmeZoneError
from delivery_lab import (
    DeliveryPlan,
    DeliveryRequest,
    DeliveryUnavailable,
    QuoteServiceUnavailable,
    plan_delivery,
)


def make_carrier(*rates: AcmeRate) -> AcmeCarrierClient:
    """Return a carrier serving NORTH with the supplied rates."""

    return AcmeCarrierClient(rates_by_zone={"NORTH": tuple(rates)})


def test_standard_delivery_selects_lowest_price_and_converts_weight() -> None:
    carrier = make_carrier(
        AcmeRate("EXPRESS", charge_minor=1_450, transit_days=2),
        AcmeRate("ECONOMY", charge_minor=825, transit_days=5),
    )

    plan = plan_delivery(
        DeliveryRequest("ORD-1", "NORTH", weight_grams=1_250),
        carrier,
    )

    assert plan == DeliveryPlan("ORD-1", "ECONOMY", price_cents=825, days=5)
    assert carrier.requests == [AcmeRequest("NORTH", mass_kilograms=1.25)]


def test_urgent_delivery_filters_slow_rates() -> None:
    carrier = make_carrier(
        AcmeRate("ECONOMY", charge_minor=500, transit_days=6),
        AcmeRate("PRIORITY", charge_minor=1_100, transit_days=2),
        AcmeRate("SAME_DAY", charge_minor=2_500, transit_days=1),
    )

    plan = plan_delivery(
        DeliveryRequest("ORD-2", "NORTH", weight_grams=600, urgent=True),
        carrier,
    )

    assert plan == DeliveryPlan("ORD-2", "PRIORITY", price_cents=1_100, days=2)


def test_equal_prices_prefer_fewer_days_then_service_name() -> None:
    carrier = make_carrier(
        AcmeRate("ZIPPY", charge_minor=900, transit_days=2),
        AcmeRate("BRISK", charge_minor=900, transit_days=1),
        AcmeRate("ALERT", charge_minor=900, transit_days=1),
    )

    plan = plan_delivery(
        DeliveryRequest("ORD-3", "NORTH", weight_grams=500),
        carrier,
    )

    assert plan.service == "ALERT"


@pytest.mark.parametrize("weight_grams", [0, -1])
def test_invalid_weight_fails_before_carrier_call(weight_grams: int) -> None:
    carrier = make_carrier(AcmeRate("ECONOMY", charge_minor=500, transit_days=4))

    with pytest.raises(ValueError, match="weight_grams must be positive"):
        plan_delivery(
            DeliveryRequest("ORD-4", "NORTH", weight_grams=weight_grams),
            carrier,
        )

    assert carrier.requests == []


def test_unknown_zone_has_stable_application_error() -> None:
    carrier = make_carrier(AcmeRate("ECONOMY", charge_minor=500, transit_days=4))

    with pytest.raises(DeliveryUnavailable, match="no delivery to zone SOUTH") as caught:
        plan_delivery(
            DeliveryRequest("ORD-5", "SOUTH", weight_grams=500),
            carrier,
        )

    assert isinstance(caught.value.__cause__, AcmeZoneError)


def test_timeout_has_distinct_stable_application_error() -> None:
    carrier = AcmeCarrierClient(rates_by_zone={}, timeout_zones={"NORTH"})

    with pytest.raises(
        QuoteServiceUnavailable,
        match="quote service unavailable for NORTH",
    ):
        plan_delivery(
            DeliveryRequest("ORD-6", "NORTH", weight_grams=500),
            carrier,
        )


@pytest.mark.parametrize(
    "rates",
    [
        (),
        (AcmeRate("ECONOMY", charge_minor=500, transit_days=4),),
    ],
)
def test_no_eligible_urgent_rate_is_explicit(
    rates: tuple[AcmeRate, ...],
) -> None:
    carrier = make_carrier(*rates)

    with pytest.raises(DeliveryUnavailable, match="no eligible delivery to zone NORTH"):
        plan_delivery(
            DeliveryRequest("ORD-7", "NORTH", weight_grams=500, urgent=True),
            carrier,
        )
