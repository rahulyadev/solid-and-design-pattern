"""Synthetic Acme carrier SDK used by the unsolved SDP-FND-030 lab."""

from __future__ import annotations

from dataclasses import dataclass, field


class AcmeZoneError(Exception):
    """Raised when Acme does not recognize a destination zone."""


class AcmeTimeout(Exception):
    """Raised when the synthetic Acme request exceeds its time budget."""


@dataclass(frozen=True)
class AcmeRequest:
    """Provider-owned request representation."""

    postal_zone_code: str
    mass_kilograms: float


@dataclass(frozen=True)
class AcmeRate:
    """Provider-owned response representation."""

    product_code: str
    charge_minor: int
    transit_days: int


@dataclass
class AcmeCarrierClient:
    """Deterministic in-memory substitute for a concrete carrier client."""

    rates_by_zone: dict[str, tuple[AcmeRate, ...]]
    timeout_zones: set[str] = field(default_factory=set)
    requests: list[AcmeRequest] = field(default_factory=list)

    def fetch_rates(self, request: AcmeRequest) -> tuple[AcmeRate, ...]:
        """Record a request and return configured provider-shaped rates."""

        self.requests.append(request)
        if request.postal_zone_code in self.timeout_zones:
            raise AcmeTimeout(f"Acme timed out for zone {request.postal_zone_code}")
        try:
            return self.rates_by_zone[request.postal_zone_code]
        except KeyError as exc:
            raise AcmeZoneError(
                f"Acme does not serve zone {request.postal_zone_code}"
            ) from exc
