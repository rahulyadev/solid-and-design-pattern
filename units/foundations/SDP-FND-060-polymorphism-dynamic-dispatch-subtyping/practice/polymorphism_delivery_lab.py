"""Unsolved SDP-FND-060 starter with nominal subtypes and concrete-type dispatch."""

from __future__ import annotations

from dataclasses import dataclass

VALID_ZONES = frozenset({"metro", "regional", "remote"})


@dataclass(frozen=True, slots=True)
class DeliveryRequest:
    """A validated, immutable request shared by every delivery option."""

    order_id: str
    zone: str
    weight_grams: int
    fragile: bool = False

    def __post_init__(self) -> None:
        if not self.order_id.strip():
            raise ValueError("order_id must not be blank")
        if self.zone not in VALID_ZONES:
            raise ValueError(f"unsupported zone: {self.zone}")
        if self.weight_grams <= 0:
            raise ValueError("weight_grams must be positive")


@dataclass(frozen=True, slots=True)
class DeliveryQuote:
    """One observable quote, including explicit business unavailability."""

    option_code: str
    available: bool
    fee_paise: int | None
    eta_days: int | None
    reason: str | None = None

    def __post_init__(self) -> None:
        if not self.option_code.strip():
            raise ValueError("option_code must not be blank")

        if self.available:
            if self.fee_paise is None or self.fee_paise < 0:
                raise ValueError("an available quote needs a non-negative fee")
            if self.eta_days is None or self.eta_days < 0:
                raise ValueError("an available quote needs a non-negative ETA")
            if self.reason is not None:
                raise ValueError("an available quote must not contain a reason")
            return

        if self.fee_paise is not None or self.eta_days is not None:
            raise ValueError("an unavailable quote must not contain fee or ETA")
        if self.reason is None or not self.reason.strip():
            raise ValueError("an unavailable quote needs a reason")


class DeliveryOption:
    """State the intended operation while leaving its behavioural promise to the lab."""

    code = "unspecified"

    def quote(self, request: DeliveryRequest) -> DeliveryQuote:
        """Return this option's response for a validated request."""

        raise NotImplementedError


class StandardDelivery(DeliveryOption):
    """Quote the ordinary door-delivery option."""

    code = "standard"

    def quote(self, request: DeliveryRequest) -> DeliveryQuote:
        kilograms = (request.weight_grams + 999) // 1000
        zone_surcharge = {
            "metro": 0,
            "regional": 200,
            "remote": 500,
        }[request.zone]
        fragile_surcharge = 150 if request.fragile else 0
        return DeliveryQuote(
            option_code=self.code,
            available=True,
            fee_paise=499 + kilograms * 50 + zone_surcharge + fragile_surcharge,
            eta_days={"metro": 3, "regional": 5, "remote": 8}[request.zone],
        )


class PriorityDelivery(DeliveryOption):
    """Quote a faster option whose current rejection semantics need review."""

    code = "priority"

    def quote(self, request: DeliveryRequest) -> DeliveryQuote:
        if request.zone != "metro":
            raise ValueError("priority delivery is unavailable outside metro")

        kilograms = (request.weight_grams + 999) // 1000
        fragile_surcharge = 250 if request.fragile else 0
        return DeliveryQuote(
            option_code=self.code,
            available=True,
            fee_paise=899 + kilograms * 125 + fragile_surcharge,
            eta_days=1,
        )


class PickupDelivery(DeliveryOption):
    """A newly supplied option that the central dispatcher does not recognize."""

    code = "pickup"

    def quote(self, request: DeliveryRequest) -> DeliveryQuote:
        return DeliveryQuote(
            option_code=self.code,
            available=True,
            fee_paise=0,
            eta_days=0,
        )


def collect_quotes(
    request: DeliveryRequest,
    options: tuple[DeliveryOption, ...],
) -> tuple[DeliveryQuote, ...]:
    """Collect quotes through a deliberately closed concrete-type decision."""

    quotes: list[DeliveryQuote] = []
    for option in options:
        if isinstance(option, StandardDelivery):  # noqa: SIM114 - branch smell is the exercise
            quote = option.quote(request)
        elif isinstance(option, PriorityDelivery):
            quote = option.quote(request)
        else:
            raise TypeError(f"unsupported delivery option: {type(option).__name__}")
        quotes.append(quote)
    return tuple(quotes)


def main() -> None:
    """Run one deterministic happy path and expose the extension bottleneck."""

    request = DeliveryRequest("order-42", "metro", 1_250, fragile=True)
    current = collect_quotes(request, (StandardDelivery(), PriorityDelivery()))
    print(f"current={current}")

    pickup = PickupDelivery()
    print(f"pickup_direct={pickup.quote(request)}")
    try:
        collect_quotes(request, (pickup,))
    except TypeError as error:
        print(f"pickup_catalog={type(error).__name__}: {error}")


if __name__ == "__main__":
    main()
