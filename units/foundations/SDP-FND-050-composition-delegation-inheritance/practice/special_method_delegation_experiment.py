"""Observe the boundary of __getattr__-based delegation for special methods."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any


class DelegatingList:
    """Forward missing ordinary attributes to a contained list."""

    def __init__(self, values: list[int]) -> None:
        self._values = values

    def __getattr__(self, name: str) -> Any:
        return getattr(self._values, name)

    def snapshot(self) -> tuple[int, ...]:
        return tuple(self._values)


def outcome(operation: Callable[[], object]) -> str:
    """Return a stable result category for one deliberate lookup attempt."""

    try:
        result = operation()
    except TypeError as exc:
        return type(exc).__name__
    return repr(result)


def main() -> None:
    """Compare explicit ordinary lookup with implicit special-method lookup."""

    wrapper = DelegatingList([10, 20])
    wrapper.append(30)

    print(f"explicit_append={wrapper.snapshot()!r}")
    print(f"explicit_count={wrapper.count(20)!r}")
    print(f"implicit_len={outcome(lambda: len(wrapper))}")
    print(f"implicit_getitem={outcome(lambda: wrapper[0])}")  # type: ignore[index]


if __name__ == "__main__":
    main()
