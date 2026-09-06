"""Mutable, stringly typed starter for the independent SDP-PYT-060 lab.

The shared identity, public list, and string state are deliberate design smells.
Preserve the observable contract before refactoring them.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TypedDict

KNOWN_STATUSES = frozenset({"created", "in_transit", "delivered"})


@dataclass
class ShipmentDraft:
    tracking_id: str
    status: str = "created"
    checkpoints: list[str] = field(default_factory=list)
    revision: int = 1


class ShipmentRecord(TypedDict):
    tracking_id: str
    status: str
    checkpoints: list[str]
    revision: int


def apply_scan(shipment: ShipmentDraft, checkpoint: str, next_status: str) -> ShipmentDraft:
    """Apply one scan by mutating and returning the supplied draft."""

    if not shipment.tracking_id or shipment.tracking_id != shipment.tracking_id.strip():
        raise ValueError("tracking_id must be non-empty and trimmed")
    if not checkpoint or checkpoint != checkpoint.strip():
        raise ValueError("checkpoint must be non-empty and trimmed")
    if next_status not in KNOWN_STATUSES:
        raise ValueError(f"unknown status: {next_status}")
    if shipment.status == "delivered":
        raise ValueError("a delivered shipment cannot accept another scan")

    shipment.checkpoints.append(checkpoint)
    shipment.status = next_status
    shipment.revision += 1
    return shipment


def to_record(shipment: ShipmentDraft) -> ShipmentRecord:
    """Return a detached transport record for the legacy object."""

    return {
        "tracking_id": shipment.tracking_id,
        "status": shipment.status,
        "checkpoints": list(shipment.checkpoints),
        "revision": shipment.revision,
    }


def main() -> None:
    shipment = ShipmentDraft("track-1")
    apply_scan(shipment, "hub-north", "in_transit")
    print(to_record(shipment))


if __name__ == "__main__":
    main()
