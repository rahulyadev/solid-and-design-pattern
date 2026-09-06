"""Behavior and lifetime tests for both construction styles."""

from __future__ import annotations

from collections.abc import Callable

import pytest
from factory_method import (
    Alert,
    AlertValidationError,
    BufferedPublisher,
    BufferedTransport,
    ClosedTransportError,
    FramedPublisher,
    Observation,
    Publisher,
    Receipt,
    Transport,
    publish_alert,
)


@pytest.mark.parametrize(
    ("alert_id", "message"),
    [("", "message"), ("é", "message"), ("x" * 41, "message"), ("A-1", "   ")],
)
def test_alert_rejects_invalid_public_input(alert_id: str, message: str) -> None:
    with pytest.raises(AlertValidationError):
        Alert(alert_id, message)


def test_concrete_creator_selects_product_and_keeps_workflow_stable() -> None:
    output: list[str] = []
    events: list[Observation] = []

    receipt = BufferedPublisher(output, events.append).publish(Alert("A-1", " ready "))

    assert receipt == Receipt("A-1", "buffer")
    assert output == ["A-1:ready"]
    assert [event.event for event in events] == [
        "transport.created",
        "transport.sent",
        "transport.closed",
    ]


def test_injected_factory_function_accepts_same_product_contract() -> None:
    output: list[str] = []
    events: list[Observation] = []

    receipt = publish_alert(
        Alert("A-2", "ok"),
        lambda: BufferedTransport(output),
        events.append,
    )

    assert receipt.transport == "buffer"
    assert output == ["A-2:ok"]


def test_second_concrete_creator_changes_product_not_workflow() -> None:
    output: list[str] = []
    events: list[Observation] = []

    receipt = FramedPublisher(output.append, events.append, prefix="OPS").publish(
        Alert("A-2B", "ready")
    )

    assert receipt == Receipt("A-2B", "framed")
    assert output == ["OPS|A-2B|ready"]
    assert [event.event for event in events] == [
        "transport.created",
        "transport.sent",
        "transport.closed",
    ]


def test_closed_product_rejects_further_use() -> None:
    transport = BufferedTransport([])
    transport.close()

    with pytest.raises(ClosedTransportError, match="closed"):
        transport.send(Alert("A-3", "late"))


class TraceTransport:
    def __init__(self, trace: list[str], *, fail: bool = False) -> None:
        self._trace = trace
        self._fail = fail

    @property
    def name(self) -> str:
        return "trace"

    def send(self, alert: Alert) -> Receipt:
        self._trace.append("send")
        if self._fail:
            raise RuntimeError("synthetic send failure")
        return Receipt(alert.alert_id, self.name)

    def close(self) -> None:
        self._trace.append("close")


def test_creator_closes_product_when_send_fails() -> None:
    trace: list[str] = []
    events: list[Observation] = []

    with pytest.raises(RuntimeError, match="synthetic"):
        publish_alert(
            Alert("A-4", "not logged"),
            lambda: TraceTransport(trace, fail=True),
            events.append,
        )

    assert trace == ["send", "close"]
    assert [event.event for event in events] == [
        "transport.created",
        "transport.failed",
        "transport.closed",
    ]
    assert events[1].error_type == "RuntimeError"
    assert all("not logged" not in repr(event) for event in events)


def test_each_call_gets_an_independent_product_lifetime() -> None:
    created: list[TraceTransport] = []

    def factory() -> Transport:
        product = TraceTransport([])
        created.append(product)
        return product

    for alert_id in ("A-5", "A-6"):
        publish_alert(Alert(alert_id, "same"), factory, lambda _event: None)

    assert len(created) == 2
    assert created[0] is not created[1]


def test_observer_failure_after_construction_still_closes_owned_product() -> None:
    trace: list[str] = []

    def broken_observer(_event: Observation) -> None:
        raise RuntimeError("synthetic observer failure")

    with pytest.raises(RuntimeError, match="observer"):
        publish_alert(
            Alert("A-6B", "safe"),
            lambda: TraceTransport(trace),
            broken_observer,
        )

    assert trace == ["close"]


def test_abstract_creator_cannot_be_instantiated() -> None:
    with pytest.raises(TypeError):
        Publisher(lambda _event: None)  # type: ignore[abstract]


def test_product_is_created_before_workflow_uses_it() -> None:
    trace: list[str] = []

    def factory() -> Transport:
        trace.append("create")
        return TraceTransport(trace)

    publish_alert(Alert("A-7", "ordered"), factory, lambda event: trace.append(event.event))

    assert trace == [
        "create",
        "transport.created",
        "send",
        "transport.sent",
        "close",
        "transport.closed",
    ]


def test_observer_contract_is_explicitly_synchronous() -> None:
    calls: list[Observation] = []
    observer: Callable[[Observation], None] = calls.append

    publish_alert(Alert("A-8", "done"), lambda: BufferedTransport([]), observer)

    assert len(calls) == 3
