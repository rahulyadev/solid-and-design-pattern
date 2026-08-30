"""One stable selection rule and a deliberately small formatting boundary."""

from collections.abc import Callable, Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class Reading:
    station: str
    celsius: int

    def __post_init__(self) -> None:
        if not self.station.strip():
            raise ValueError("station must not be blank")


def select_alerts(readings: Sequence[Reading], cutoff: int) -> tuple[Reading, ...]:
    """Include the cutoff; preserve order and duplicates; do not change inputs."""
    return tuple(reading for reading in readings if reading.celsius >= cutoff)


def build_report(
    readings: Sequence[Reading],
    cutoff: int,
    formatter: Callable[[tuple[Reading, ...]], str],
) -> str:
    """Format one selected snapshot. Formatter failures remain visible to the caller."""
    return formatter(select_alerts(readings, cutoff))
