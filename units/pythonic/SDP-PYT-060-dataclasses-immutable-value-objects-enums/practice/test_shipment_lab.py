"""Characterization tests only; the target refactoring is intentionally absent."""

from __future__ import annotations

import pytest
from shipment_lab import ShipmentDraft, apply_scan, to_record


def test_scan_mutates_and_returns_the_same_legacy_object() -> None:
    shipment = ShipmentDraft("track-1")

    result = apply_scan(shipment, "hub|north", "in_transit")

    assert result is shipment
    assert to_record(shipment) == {
        "tracking_id": "track-1",
        "status": "in_transit",
        "checkpoints": ["hub|north"],
        "revision": 2,
    }


def test_each_draft_receives_an_independent_checkpoint_list() -> None:
    first = ShipmentDraft("first")
    second = ShipmentDraft("second")

    apply_scan(first, "hub-a", "in_transit")

    assert first.checkpoints == ["hub-a"]
    assert second.checkpoints == []
    assert first.checkpoints is not second.checkpoints


def test_unicode_and_punctuation_are_preserved() -> None:
    shipment = ShipmentDraft("पार्सल:१")

    apply_scan(shipment, "केंद्र|दिल्ली", "delivered")

    assert to_record(shipment)["checkpoints"] == ["केंद्र|दिल्ली"]


@pytest.mark.parametrize(
    ("tracking_id", "checkpoint", "status", "message"),
    [
        ("", "hub", "in_transit", "tracking_id"),
        (" track ", "hub", "in_transit", "tracking_id"),
        ("track", "", "in_transit", "checkpoint"),
        ("track", " hub ", "in_transit", "checkpoint"),
        ("track", "hub", "waiting", "unknown status"),
    ],
)
def test_invalid_scan_is_rejected_without_partial_mutation(
    tracking_id: str,
    checkpoint: str,
    status: str,
    message: str,
) -> None:
    shipment = ShipmentDraft(tracking_id)

    with pytest.raises(ValueError, match=message):
        apply_scan(shipment, checkpoint, status)

    assert shipment.status == "created"
    assert shipment.checkpoints == []
    assert shipment.revision == 1


def test_delivered_shipment_rejects_later_scan_without_mutation() -> None:
    shipment = ShipmentDraft("track-1")
    apply_scan(shipment, "door", "delivered")
    before = to_record(shipment)

    with pytest.raises(ValueError, match="delivered"):
        apply_scan(shipment, "after-door", "delivered")

    assert to_record(shipment) == before


def test_transport_record_does_not_share_the_mutable_list() -> None:
    shipment = ShipmentDraft("track-1")
    apply_scan(shipment, "hub", "in_transit")

    record = to_record(shipment)
    record["checkpoints"].append("external-change")

    assert shipment.checkpoints == ["hub"]
