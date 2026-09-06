"""Behavior tests for the worked SDP-PYT-040 example."""

from __future__ import annotations

from collections.abc import Iterator

import pytest
from streaming_reports import (
    Alert,
    MemoryAlertSink,
    batched,
    export_important_alerts,
    important_alerts,
    managed_sink,
    parse_alerts,
)


def test_parse_alerts_is_lazy_and_preserves_message_separators() -> None:
    trace: list[str] = []
    pipeline = parse_alerts(["a-1|4|alpha|beta"], trace=trace.append)

    assert trace == []
    assert next(pipeline) == Alert("a-1", 4, "alpha|beta")
    assert trace == ["read:a-1|4|alpha|beta"]


def test_parse_failure_occurs_only_when_bad_input_is_requested() -> None:
    pipeline = parse_alerts(["a-1|2|ok", "bad"])

    assert next(pipeline) == Alert("a-1", 2, "ok")
    with pytest.raises(ValueError):
        next(pipeline)


def test_important_alerts_preserves_order_and_duplicates() -> None:
    repeated = Alert("a-2", 5, "repeat")
    alerts = [Alert("a-1", 1, "low"), repeated, repeated]

    assert tuple(important_alerts(alerts, minimum_severity=4)) == (repeated, repeated)


def test_generator_body_validation_is_deferred_until_iteration() -> None:
    pipeline = important_alerts([], minimum_severity=-1)

    with pytest.raises(ValueError, match="minimum_severity must be non-negative"):
        next(pipeline)


def test_batched_supports_one_pass_input_and_a_short_final_batch() -> None:
    source = iter(
        [
            Alert("a-1", 1, "one"),
            Alert("a-2", 2, "two"),
            Alert("a-3", 3, "three"),
        ]
    )

    assert tuple(batched(source, 2)) == (
        (Alert("a-1", 1, "one"), Alert("a-2", 2, "two")),
        (Alert("a-3", 3, "three"),),
    )
    assert tuple(source) == ()


def test_batched_does_not_read_past_the_requested_first_batch() -> None:
    consumed: list[int] = []

    def source() -> Iterator[Alert]:
        for number in range(4):
            consumed.append(number)
            yield Alert(f"a-{number}", number, "message")

    batches = batched(source(), 2)

    assert tuple(alert.alert_id for alert in next(batches)) == ("a-0", "a-1")
    assert consumed == [0, 1]


def test_batched_rejects_non_positive_size_when_iteration_starts() -> None:
    pipeline = batched([], 0)

    with pytest.raises(ValueError, match="batch size must be positive"):
        next(pipeline)


def test_managed_sink_reports_success_and_closes() -> None:
    sink = MemoryAlertSink()
    trace: list[str] = []

    with managed_sink(lambda: sink, trace=trace.append) as active:
        active.write("row")
        trace.append("body")

    assert sink.rows == ["row"]
    assert sink.closed is True
    assert trace == ["acquire", "body", "commit", "close"]


def test_managed_sink_preserves_body_exception_identity_and_closes() -> None:
    sink = MemoryAlertSink()
    trace: list[str] = []
    original = RuntimeError("boom")

    with (
        pytest.raises(RuntimeError) as captured,
        managed_sink(lambda: sink, trace=trace.append),
    ):
        raise original

    assert captured.value is original
    assert sink.closed is True
    assert trace == ["acquire", "abort:RuntimeError", "close"]


def test_factory_failure_happens_before_acquisition_is_reported() -> None:
    trace: list[str] = []
    original = RuntimeError("factory failed")

    def fail() -> MemoryAlertSink:
        raise original

    with pytest.raises(RuntimeError) as captured, managed_sink(fail, trace=trace.append):
        pytest.fail("body must not run")

    assert captured.value is original
    assert trace == []


def test_export_drives_pipeline_inside_resource_lifetime() -> None:
    trace: list[str] = []
    sink = MemoryAlertSink()

    count = export_important_alerts(
        ["a-1|1|low", "a-2|5|high", "a-3|4|also high"],
        minimum_severity=4,
        batch_size=1,
        sink_factory=lambda: sink,
        trace=trace.append,
    )

    assert count == 2
    assert sink.rows == ["a-2:5:high", "a-3:4:also high"]
    assert sink.closed is True
    assert trace == [
        "acquire",
        "read:a-1|1|low",
        "read:a-2|5|high",
        "batch:1:1",
        "write:a-2",
        "read:a-3|4|also high",
        "batch:2:1",
        "write:a-3",
        "commit",
        "close",
    ]


def test_parse_failure_closes_sink_and_propagates() -> None:
    trace: list[str] = []
    sink = MemoryAlertSink()

    with pytest.raises(ValueError):
        export_important_alerts(
            ["a-1|5|valid", "bad"],
            minimum_severity=4,
            batch_size=2,
            sink_factory=lambda: sink,
            trace=trace.append,
        )

    assert sink.closed is True
    assert trace[-2:] == ["abort:ValueError", "close"]


def test_sink_failure_closes_sink_without_relabeling_error() -> None:
    row = "a-1:5:high"
    sink = MemoryAlertSink(fail_on=row)

    with pytest.raises(OSError, match=f"synthetic write failure: {row}"):
        export_important_alerts(
            ["a-1|5|high"],
            minimum_severity=4,
            batch_size=1,
            sink_factory=lambda: sink,
        )

    assert sink.closed is True


def test_memory_sink_rejects_write_after_close() -> None:
    sink = MemoryAlertSink()
    sink.close()

    with pytest.raises(RuntimeError, match="sink is closed"):
        sink.write("late")
