"""Observe binding versus copying. No addresses, timing claims, or private data."""

import json
from collections.abc import Callable
from functools import partial
from typing import TypedDict

Reader = Callable[[], tuple[int, ...]]


class CaptureStep(TypedDict):
    stage: str
    current: list[int]
    original: list[int]
    closure: list[int]
    default: list[int]
    partial: list[int]
    snapshot: list[int]


class LoopObservation(TypedDict):
    configured: list[int]
    late: list[int]
    default: list[int]
    factory: list[int]
    shared_cell: bool
    separate_cells: bool


class Observations(TypedDict):
    capture: list[CaptureStep]
    loop: LoopObservation


def tuple_of(values: list[int]) -> tuple[int, ...]:
    return tuple(values)


def capture_trace() -> list[CaptureStep]:
    values = [2]
    original = values

    def closure_reader() -> tuple[int, ...]:
        return tuple(values)

    def default_reader(saved: list[int] = values) -> tuple[int, ...]:
        return tuple(saved)

    partial_reader: Reader = partial(tuple_of, values)
    snapshot = tuple(values)

    def snapshot_reader() -> tuple[int, ...]:
        return snapshot

    def observe(stage: str) -> CaptureStep:
        return {
            "stage": stage,
            "current": list(values),
            "original": list(original),
            "closure": list(closure_reader()),
            "default": list(default_reader()),
            "partial": list(partial_reader()),
            "snapshot": list(snapshot_reader()),
        }

    steps = [observe("Create readers")]
    values.append(5)
    steps.append(observe("Mutate original list"))
    values = [8]
    steps.append(observe("Rebind outer name"))
    return steps


def fixed_reader(value: int) -> Callable[[], int]:
    def read() -> int:
        return value

    return read


def loop_observation() -> LoopObservation:
    configured = [2, 5, 8]
    late: list[Callable[[], int]] = []
    defaults: list[Callable[[], int]] = []
    for value in configured:

        def late_reader() -> int:
            return value  # noqa: B023 - intentional late-binding experiment

        def default_reader(saved: int = value) -> int:
            return saved

        late.append(late_reader)
        defaults.append(default_reader)

    factories = [fixed_reader(value) for value in configured]
    first_closure = late[0].__closure__
    last_closure = late[-1].__closure__
    first_factory = factories[0].__closure__
    last_factory = factories[-1].__closure__
    assert first_closure and last_closure and first_factory and last_factory
    return {
        "configured": configured,
        "late": [read() for read in late],
        "default": [read() for read in defaults],
        "factory": [read() for read in factories],
        "shared_cell": first_closure[0] is last_closure[0],
        "separate_cells": first_factory[0] is not last_factory[0],
    }


def observations() -> Observations:
    return {"capture": capture_trace(), "loop": loop_observation()}


if __name__ == "__main__":
    print(json.dumps(observations(), indent=2))
