"""Characterization tests only; the target lifetime refactoring is absent."""

from __future__ import annotations

import fulfillment_lab
import pytest
from fulfillment_lab import AllocationRequest, WarehouseGateway


def test_formats_allocation_and_uses_the_module_gateway(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    gateway = WarehouseGateway("warehouse://test")
    monkeypatch.setattr(fulfillment_lab, "warehouse_gateway", gateway)

    result = fulfillment_lab.allocate_order(AllocationRequest("order-1", "sku|blue", 2))

    assert result == "order-1:sku|blue:2@warehouse://test#session-1"
    assert len(gateway.sessions) == 1
    assert gateway.sessions[0].close_calls == 1
    assert gateway.closed is False


def test_two_calls_reuse_gateway_but_receive_distinct_closed_sessions(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    gateway = WarehouseGateway("warehouse://test")
    monkeypatch.setattr(fulfillment_lab, "warehouse_gateway", gateway)

    first = fulfillment_lab.allocate_order(AllocationRequest("one", "sku", 1))
    second = fulfillment_lab.allocate_order(AllocationRequest("two", "sku", 1))

    assert first.endswith("#session-1")
    assert second.endswith("#session-2")
    assert gateway.sessions[0] is not gateway.sessions[1]
    assert [session.close_calls for session in gateway.sessions] == [1, 1]


def test_invalid_quantity_fails_before_a_session_is_opened(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    gateway = WarehouseGateway("warehouse://test")
    monkeypatch.setattr(fulfillment_lab, "warehouse_gateway", gateway)

    with pytest.raises(ValueError, match="quantity must be positive"):
        fulfillment_lab.allocate_order(AllocationRequest("order", "sku", 0))

    assert gateway.sessions == []


def test_gateway_failure_propagates_and_session_is_closed_once(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    gateway = WarehouseGateway("warehouse://test", fail_sku="broken")
    monkeypatch.setattr(fulfillment_lab, "warehouse_gateway", gateway)

    with pytest.raises(OSError, match="synthetic warehouse failure: broken"):
        fulfillment_lab.allocate_order(AllocationRequest("order", "broken", 1))

    assert len(gateway.sessions) == 1
    assert gateway.sessions[0].close_calls == 1
    assert gateway.closed is False


def test_blank_and_unicode_text_are_preserved(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    gateway = WarehouseGateway("warehouse://test")
    monkeypatch.setattr(fulfillment_lab, "warehouse_gateway", gateway)

    assert fulfillment_lab.allocate_order(AllocationRequest("", "वस्तु", 1)) == (
        ":वस्तु:1@warehouse://test#session-1"
    )
