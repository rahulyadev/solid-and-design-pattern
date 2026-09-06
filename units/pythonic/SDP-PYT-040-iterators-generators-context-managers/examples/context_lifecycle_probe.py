"""Deterministic context-manager entry and exit observations for SDP-PYT-040."""

from __future__ import annotations

import json
from types import TracebackType
from typing import Any, Literal

from streaming_reports import MemoryAlertSink, managed_sink


class SelectiveSuppressor:
    """Suppress only LookupError subclasses and expose the received exit state."""

    def __init__(self, trace: list[str]) -> None:
        self._trace = trace

    def __enter__(self) -> str:
        self._trace.append("enter")
        return "ready"

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool:
        del exc_value, traceback
        name = "None" if exc_type is None else exc_type.__name__
        self._trace.append(f"exit:{name}")
        return exc_type is not None and issubclass(exc_type, LookupError)


class EnterFailure:
    """Show that exit is unavailable when entry itself fails."""

    def __init__(self, trace: list[str]) -> None:
        self._trace = trace

    def __enter__(self) -> None:
        self._trace.append("enter")
        raise RuntimeError("entry failed")

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> Literal[False]:
        del exc_type, exc_value, traceback
        self._trace.append("exit")
        return False


def context_observations() -> dict[str, Any]:
    """Return success, propagation, suppression, and entry-failure traces."""

    normal_trace: list[str] = []
    normal_sink = MemoryAlertSink()
    with managed_sink(lambda: normal_sink, trace=normal_trace.append) as sink:
        sink.write("normal")
        normal_trace.append("body")

    failure_trace: list[str] = []
    failure_sink = MemoryAlertSink()
    same_error = RuntimeError("body failed")
    propagated_same_instance = False
    try:
        with managed_sink(lambda: failure_sink, trace=failure_trace.append):
            failure_trace.append("body")
            raise same_error
    except RuntimeError as caught:
        propagated_same_instance = caught is same_error

    suppression_trace: list[str] = []
    with SelectiveSuppressor(suppression_trace):
        suppression_trace.append("body")
        raise KeyError("synthetic miss")
    suppression_trace.append("continued")

    entry_trace: list[str] = []
    try:
        with EnterFailure(entry_trace):
            entry_trace.append("unreachable")
    except RuntimeError:
        entry_trace.append("caught")

    return {
        "normal": {
            "trace": tuple(normal_trace),
            "closed": normal_sink.closed,
        },
        "body_failure": {
            "trace": tuple(failure_trace),
            "closed": failure_sink.closed,
            "same_exception_propagated": propagated_same_instance,
        },
        "selective_suppression": tuple(suppression_trace),
        "entry_failure": tuple(entry_trace),
    }


def main() -> None:
    print(json.dumps(context_observations(), ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
