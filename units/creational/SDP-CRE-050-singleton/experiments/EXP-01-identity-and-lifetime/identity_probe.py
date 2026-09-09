"""Deterministic identity observations; barriers select schedules, not timings."""

from __future__ import annotations

import json
import sys
from concurrent.futures import ThreadPoolExecutor
from contextlib import suppress
from dataclasses import asdict, dataclass
from functools import cache
from pathlib import Path
from threading import Barrier
from typing import ClassVar

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "examples"))
from lifetimes import LazyValue, MemoryReader, application


@dataclass(frozen=True)
class Observation:
    scenario: str
    constructions: int
    same_identity: bool
    detail: str


def observe() -> list[Observation]:
    class Reinitialized:
        cached: ClassVar[Reinitialized | None] = None
        allocations: ClassVar[int] = 0
        initializations: ClassVar[int] = 0

        def __new__(cls, label: str) -> Reinitialized:
            if cls.cached is None:
                cls.cached = super().__new__(cls)
                cls.allocations += 1
            return cls.cached

        def __init__(self, label: str) -> None:
            type(self).initializations += 1
            self.label = label

    first = Reinitialized("first")
    second = Reinitialized("second")
    results = [
        Observation(
            "repeated-init",
            Reinitialized.allocations,
            first is second,
            f"init calls={Reinitialized.initializations}; label={first.label}",
        )
    ]
    rendezvous = Barrier(2, timeout=5)

    @cache
    def cached_value() -> object:
        rendezvous.wait()
        return object()

    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(cached_value) for _ in range(2)]
        values = [future.result(timeout=10) for future in futures]
    results.append(
        Observation(
            "cache-race",
            cached_value.cache_info().misses,
            values[0] is values[1],
            "two overlapping cache misses",
        )
    )
    calls = 0

    def build() -> object:
        nonlocal calls
        calls += 1
        return object()

    lazy = LazyValue(build)
    start = Barrier(2, timeout=5)

    def get() -> object:
        start.wait()
        return lazy.get()

    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(get) for _ in range(2)]
        values = [future.result(timeout=10) for future in futures]
    results.append(
        Observation(
            "locked-provider", calls, values[0] is values[1], "one publication per provider"
        )
    )
    attempts = 0

    def flaky() -> object:
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            raise ValueError("synthetic first failure")
        return object()

    retry = LazyValue(flaky)
    with suppress(ValueError):
        retry.get()
    recovered = retry.get()
    results.append(
        Observation("retry", attempts, recovered is retry.get(), "failed attempt was not published")
    )
    a = MemoryReader({"cover": "green"}, revision="r1")
    b = MemoryReader({"cover": "ochre"}, revision="r2")
    with application(lambda: a) as left, application(lambda: b) as right:
        shared = left.preview.reader is right.preview.reader
        assert left.preview.reader is left.export.reader
        assert right.preview.reader is right.export.reader
    results.append(Observation("two-apps", 2, shared, f"both closed={a.closed and b.closed}"))
    return results


if __name__ == "__main__":
    print(json.dumps([asdict(item) for item in observe()], indent=2))
