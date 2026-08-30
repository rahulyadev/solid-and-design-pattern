"""Matching a callable Protocol does not establish the non-mutation promise."""

from dataclasses import dataclass
from typing import Protocol


class Maximum(Protocol):
    def __call__(self, readings: list[int], /) -> int:
        """Maximum of nonempty readings; preserve their acquisition order."""
        ...


def preserving_maximum(readings: list[int]) -> int:
    if not readings:
        raise ValueError("readings must not be empty")
    return max(readings)


def sorting_maximum(readings: list[int]) -> int:
    """Intentional semantic violation, despite a compatible signature."""
    if not readings:
        raise ValueError("readings must not be empty")
    readings.sort()
    return readings[-1]


@dataclass(frozen=True)
class Observation:
    maximum: int
    before: tuple[int, ...]
    after: tuple[int, ...]
    latest: int


def observe(operation: Maximum, values: list[int]) -> Observation:
    readings = list(values)
    timeline = readings
    before = tuple(readings)
    result = operation(readings)
    return Observation(result, before, tuple(readings), timeline[-1])


def main() -> None:
    providers: tuple[tuple[str, Maximum], ...] = (
        ("preserving", preserving_maximum),
        ("sorting", sorting_maximum),
    )
    for name, provider in providers:
        result = observe(provider, [30, 10, 20])
        print(
            f"{name}: maximum={result.maximum}; before={result.before}; "
            f"after={result.after}; latest={result.latest}"
        )


if __name__ == "__main__":
    main()
