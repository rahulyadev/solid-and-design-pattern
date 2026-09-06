"""Observe cleanup when a related product fails during family acquisition."""

from __future__ import annotations

from contextlib import AbstractContextManager, ExitStack
from dataclasses import dataclass
from typing import Literal, Protocol


class OpenedProduct(Protocol):
    name: str


@dataclass(slots=True)
class TracedProduct:
    name: str
    trace: list[str]

    def __enter__(self) -> TracedProduct:
        self.trace.append(f"{self.name}.open")
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        self.trace.append(f"{self.name}.close")


@dataclass(slots=True)
class FailingProduct:
    name: str
    trace: list[str]

    def __enter__(self) -> FailingProduct:
        self.trace.append(f"{self.name}.open")
        raise RuntimeError(f"{self.name} acquisition failed")

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        self.trace.append(f"{self.name}.close")


@dataclass(frozen=True, slots=True)
class ResourceFamily:
    trace: list[str]
    fail_secondary: bool

    def open_primary(self) -> AbstractContextManager[OpenedProduct]:
        return TracedProduct("primary", self.trace)

    def open_secondary(self) -> AbstractContextManager[OpenedProduct]:
        if self.fail_secondary:
            return FailingProduct("secondary", self.trace)
        return TracedProduct("secondary", self.trace)


def acquire_and_use(factory: ResourceFamily) -> Literal["used"]:
    with ExitStack() as stack:
        primary = stack.enter_context(factory.open_primary())
        secondary = stack.enter_context(factory.open_secondary())
        factory.trace.append(f"use:{primary.name}+{secondary.name}")
        return "used"


def observe(fail_secondary: bool) -> list[str]:
    trace: list[str] = []
    try:
        acquire_and_use(ResourceFamily(trace, fail_secondary))
    except RuntimeError as exc:
        trace.append(f"caught:{type(exc).__name__}")
    return trace


def main() -> None:
    print("success=" + " > ".join(observe(False)))
    print("failure=" + " > ".join(observe(True)))


if __name__ == "__main__":
    main()
