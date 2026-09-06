"""Worked streaming and resource-lifetime example for SDP-PYT-040.

The example is deliberately framework-independent.  It parses synthetic alert
records lazily, filters them, groups them into bounded batches, and drives the
pipeline while a caller-supplied sink is inside an explicit context.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from itertools import islice
from typing import Protocol

Trace = Callable[[str], None]


def _ignore(_: str) -> None:
    """Default trace callback for examples that do not need observations."""


@dataclass(frozen=True)
class Alert:
    """One parsed synthetic alert record."""

    alert_id: str
    severity: int
    message: str


class AlertSink(Protocol):
    """Small behavioral boundary used by the export operation."""

    def write(self, row: str) -> None: ...

    def close(self) -> None: ...


class MemoryAlertSink:
    """Observable in-memory sink used by the demo and tests."""

    def __init__(self, *, fail_on: str | None = None) -> None:
        self.rows: list[str] = []
        self.closed = False
        self._fail_on = fail_on

    def write(self, row: str) -> None:
        if self.closed:
            raise RuntimeError("sink is closed")
        if row == self._fail_on:
            raise OSError(f"synthetic write failure: {row}")
        self.rows.append(row)

    def close(self) -> None:
        self.closed = True


def parse_alerts(
    lines: Iterable[str],
    *,
    trace: Trace = _ignore,
) -> Iterator[Alert]:
    """Parse pipe-delimited records only as the consumer requests them."""

    for line in lines:
        trace(f"read:{line}")
        alert_id, severity_text, message = line.split("|", 2)
        yield Alert(alert_id, int(severity_text), message)


def important_alerts(
    alerts: Iterable[Alert],
    *,
    minimum_severity: int,
) -> Iterator[Alert]:
    """Yield alerts meeting an explicit severity policy."""

    if minimum_severity < 0:
        raise ValueError("minimum_severity must be non-negative")
    for alert in alerts:
        if alert.severity >= minimum_severity:
            yield alert


def batched(items: Iterable[Alert], size: int) -> Iterator[tuple[Alert, ...]]:
    """Yield non-empty, bounded tuples without materializing the whole input."""

    if size < 1:
        raise ValueError("batch size must be positive")

    iterator = iter(items)
    while batch := tuple(islice(iterator, size)):
        yield batch


@contextmanager
def managed_sink(
    factory: Callable[[], AlertSink],
    *,
    trace: Trace = _ignore,
) -> Iterator[AlertSink]:
    """Acquire, report outcome, and deterministically close one sink."""

    sink = factory()
    trace("acquire")
    try:
        yield sink
    except BaseException as error:
        trace(f"abort:{type(error).__name__}")
        raise
    else:
        trace("commit")
    finally:
        sink.close()
        trace("close")


def export_important_alerts(
    lines: Iterable[str],
    *,
    minimum_severity: int,
    batch_size: int,
    sink_factory: Callable[[], AlertSink],
    trace: Trace = _ignore,
) -> int:
    """Drive a lazy pipeline entirely inside the sink's managed lifetime."""

    written = 0
    alerts = important_alerts(
        parse_alerts(lines, trace=trace),
        minimum_severity=minimum_severity,
    )

    with managed_sink(sink_factory, trace=trace) as sink:
        for batch_number, batch in enumerate(batched(alerts, batch_size), start=1):
            trace(f"batch:{batch_number}:{len(batch)}")
            for alert in batch:
                row = f"{alert.alert_id}:{alert.severity}:{alert.message}"
                sink.write(row)
                trace(f"write:{alert.alert_id}")
                written += 1

    return written
