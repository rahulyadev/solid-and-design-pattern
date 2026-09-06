"""Observe construction, use, failure, and cleanup order for an owned Product."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ProbeResult:
    success_trace: tuple[str, ...]
    failure_trace: tuple[str, ...]


class ProbeProduct:
    def __init__(self, trace: list[str], *, fail: bool = False) -> None:
        self._trace = trace
        self._fail = fail
        trace.append("construct")

    def use(self) -> None:
        self._trace.append("use")
        if self._fail:
            raise RuntimeError("synthetic failure")

    def close(self) -> None:
        self._trace.append("close")


def run_once(*, fail: bool) -> tuple[str, ...]:
    trace: list[str] = []
    product = ProbeProduct(trace, fail=fail)
    try:
        product.use()
    finally:
        product.close()
    return tuple(trace)


def run_failure() -> tuple[str, ...]:
    trace: list[str] = []
    product = ProbeProduct(trace, fail=True)
    try:
        try:
            product.use()
        finally:
            product.close()
    except RuntimeError as error:
        trace.append("caught:" + type(error).__name__)
    else:  # pragma: no cover - the probe is intentionally configured to fail
        raise AssertionError("failure probe did not fail")
    return tuple(trace)


def observe_lifetimes() -> ProbeResult:
    success = run_once(fail=False)
    return ProbeResult(success, run_failure())


def main() -> None:
    result = observe_lifetimes()
    print("success=" + ">".join(result.success_trace))
    print("failure=" + ">".join(result.failure_trace))


if __name__ == "__main__":
    main()
