"""Working broad-boundary starter. The partner integration remains unsolved."""

from collections.abc import Mapping
from dataclasses import dataclass, replace
from typing import Protocol


@dataclass(frozen=True)
class Station:
    temperature_c: int
    interval_seconds: int = 60
    restarts: int = 0

    def __post_init__(self) -> None:
        if not 1 <= self.interval_seconds <= 3600:
            raise ValueError("interval must be between 1 and 3600 seconds")
        if self.restarts < 0:
            raise ValueError("restarts must be nonnegative")


class StationConsole(Protocol):
    def reading(self, station_id: str, /) -> int: ...

    def configure_interval(self, station_id: str, seconds: int, /) -> None: ...

    def restart(self, station_id: str, /) -> None: ...


class LabConsole:
    def __init__(self, stations: Mapping[str, Station]) -> None:
        self._stations = dict(stations)

    def reading(self, station_id: str, /) -> int:
        return self._stations[station_id].temperature_c

    def configure_interval(self, station_id: str, seconds: int, /) -> None:
        current = self._stations[station_id]
        self._stations[station_id] = replace(current, interval_seconds=seconds)

    def restart(self, station_id: str, /) -> None:
        current = self._stations[station_id]
        self._stations[station_id] = replace(current, restarts=current.restarts + 1)

    def snapshot(self, station_id: str) -> Station:
        return self._stations[station_id]


def temperature_report(
    console: StationConsole, station_ids: tuple[str, ...]
) -> tuple[tuple[str, int], ...]:
    return tuple((station_id, console.reading(station_id)) for station_id in station_ids)


def apply_interval(console: StationConsole, station_id: str, seconds: int) -> None:
    console.configure_interval(station_id, seconds)
    console.restart(station_id)


def main() -> None:
    console = LabConsole({"north": Station(18), "south": Station(0)})
    print(f"report: {temperature_report(console, ('south', 'north', 'south'))}")
    apply_interval(console, "north", 120)
    print(f"after configuration: {console.snapshot('north')}")
    try:
        apply_interval(console, "north", 0)
    except ValueError as error:
        print(f"rejected interval: {error}")
    print(f"after rejection: {console.snapshot('north')}")


if __name__ == "__main__":
    main()
