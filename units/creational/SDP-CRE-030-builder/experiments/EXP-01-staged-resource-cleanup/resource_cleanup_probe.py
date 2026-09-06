"""Observe ownership transfer and partial cleanup during staged construction."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from contextlib import ExitStack
from dataclasses import dataclass, field


class AcquisitionError(RuntimeError):
    """A synthetic resource could not be acquired."""


@dataclass(slots=True)
class ProbeResource:
    name: str
    events: list[str]
    fail_on_enter: bool = False
    closed: bool = False

    def __enter__(self) -> ProbeResource:
        if self.fail_on_enter:
            self.events.append(f"open-failed:{self.name}")
            raise AcquisitionError(f"could not acquire {self.name}")
        self.events.append(f"open:{self.name}")
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        self.close()

    def close(self) -> None:
        if not self.closed:
            self.closed = True
            self.events.append(f"close:{self.name}")


@dataclass(slots=True)
class PreparedResources:
    """Final owner of resources transferred out of the construction stack."""

    resources: tuple[ProbeResource, ...]
    _close_all: Callable[[], None] = field(repr=False)
    _closed: bool = False

    def close(self) -> None:
        if not self._closed:
            self._closed = True
            self._close_all()

    def __enter__(self) -> PreparedResources:
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        self.close()


def prepare_resources(
    names: Sequence[str], events: list[str], *, fail_on: str | None = None
) -> PreparedResources:
    """Acquire in order; clean partial state or transfer ownership atomically."""

    with ExitStack() as construction_stack:
        acquired = tuple(
            construction_stack.enter_context(
                ProbeResource(name, events, fail_on_enter=name == fail_on)
            )
            for name in names
        )
        events.append("prepared")
        owner_stack = construction_stack.pop_all()
    return PreparedResources(acquired, owner_stack.close)


def run_probe() -> tuple[list[str], list[str]]:
    success_events: list[str] = []
    with prepare_resources(("schema", "sink"), success_events):
        success_events.append("use")

    failure_events: list[str] = []
    try:
        prepare_resources(("schema", "sink"), failure_events, fail_on="sink")
    except AcquisitionError:
        failure_events.append("rejected")

    return success_events, failure_events


def main() -> None:
    success, failure = run_probe()
    print("success:", " -> ".join(success))
    print("failure:", " -> ".join(failure))


if __name__ == "__main__":
    main()
