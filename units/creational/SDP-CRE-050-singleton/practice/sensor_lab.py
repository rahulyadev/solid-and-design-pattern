"""Unsolved baseline: each call opens and closes its own synthetic sensor."""

from dataclasses import dataclass


@dataclass
class Sensor:
    station: str
    closed: bool = False

    def read(self) -> str:
        if self.closed:
            raise RuntimeError("sensor closed")
        return f"{self.station}:ready"

    def close(self) -> None:
        self.closed = True


def sample(station: str) -> str:
    if not station.strip():
        raise ValueError("station required")
    sensor = Sensor(station)
    try:
        return sensor.read()
    finally:
        sensor.close()


if __name__ == "__main__":
    print(sample("north"))
    print("target_complete=False")
