"""An added method can break a history promise without overriding a base method."""

from itertools import pairwise
from typing import Protocol


class CountReader(Protocol):
    """Nonnegative count that never decreases over this object's lifetime."""

    @property
    def value(self) -> int: ...


class GrowingCount:
    def __init__(self) -> None:
        self._value = 0

    @property
    def value(self) -> int:
        return self._value

    def advance(self, amount: int) -> None:
        if amount < 0:
            raise ValueError("amount must be nonnegative")
        self._value += amount


class ResettableCount(GrowingCount):
    """Candidate subtype: existing methods are inherited unchanged."""

    def reset(self) -> None:
        self._value = 0


def never_decreases(values: tuple[int, ...]) -> bool:
    return all(before <= after for before, after in pairwise(values))


def run_probe() -> tuple[str, ...]:
    writer = ResettableCount()
    reader: CountReader = writer
    before = reader.value
    writer.advance(3)
    advanced = reader.value
    writer.reset()
    readings = (before, advanced, reader.value)
    return (
        f"same object: {reader is writer}",
        f"readings: {readings}",
        f"nonnegative states: {all(value >= 0 for value in readings)}",
        f"never decreases: {never_decreases(readings)}",
    )


if __name__ == "__main__":
    print("\n".join(run_probe()))
