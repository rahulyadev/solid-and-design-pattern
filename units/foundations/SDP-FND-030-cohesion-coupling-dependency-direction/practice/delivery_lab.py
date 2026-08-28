"""Unsolved SDP-FND-030 starter with policy coupled to one carrier schema."""

from __future__ import annotations

from dataclasses import dataclass

from acme_carrier import (
    AcmeCarrierClient,
    AcmeRequest,
    AcmeTimeout,
    AcmeZoneError,
)


class DeliveryUnavailable(LookupError):
    """Raised when no delivery plan can satisfy the request."""


class QuoteServiceUnavailable(RuntimeError):
    """Raised when the quote mechanism cannot currently answer."""


@dataclass(frozen=True)
class DeliveryRequest:
    """Application-owned input to delivery planning."""

    order_id: str
    zone: str
    weight_grams: int
    urgent: bool = False


@dataclass(frozen=True)
class DeliveryPlan:
    """Application-owned result of delivery planning."""

    order_id: str
    service: str
    price_cents: int
    days: int


def plan_delivery(
    request: DeliveryRequest,
    carrier: AcmeCarrierClient,
) -> DeliveryPlan:
    """Mix stable selection policy with deliberately Acme-specific translation."""

    if request.weight_grams <= 0:
        raise ValueError("weight_grams must be positive")

    acme_request = AcmeRequest(
        postal_zone_code=request.zone,
        mass_kilograms=request.weight_grams / 1_000,
    )
    try:
        rates = carrier.fetch_rates(acme_request)
    except AcmeZoneError as exc:
        raise DeliveryUnavailable(f"no delivery to zone {request.zone}") from exc
    except AcmeTimeout as exc:
        raise QuoteServiceUnavailable(f"quote service unavailable for {request.zone}") from exc

    eligible = [rate for rate in rates if not request.urgent or rate.transit_days <= 2]
    if not eligible:
        raise DeliveryUnavailable(f"no eligible delivery to zone {request.zone}")

    selected = min(
        eligible,
        key=lambda rate: (rate.charge_minor, rate.transit_days, rate.product_code),
    )
    return DeliveryPlan(
        order_id=request.order_id,
        service=selected.product_code,
        price_cents=selected.charge_minor,
        days=selected.transit_days,
    )


def example_carrier() -> AcmeCarrierClient:
    """Build a synthetic carrier for prediction and manual observation."""

    from acme_carrier import AcmeRate

    return AcmeCarrierClient(
        rates_by_zone={
            "NORTH": (
                AcmeRate("ECONOMY", charge_minor=825, transit_days=5),
                AcmeRate("EXPRESS", charge_minor=1_450, transit_days=2),
            )
        }
    )


def main() -> None:
    """Run one standard and one urgent request against the mixed starter."""

    carrier = example_carrier()
    standard = plan_delivery(
        DeliveryRequest("ORD-100", "NORTH", weight_grams=1_250),
        carrier,
    )
    urgent = plan_delivery(
        DeliveryRequest("ORD-101", "NORTH", weight_grams=750, urgent=True),
        carrier,
    )
    print(f"standard: {standard}")
    print(f"urgent: {urgent}")
    print(f"Acme requests: {carrier.requests}")


if __name__ == "__main__":
    main()
