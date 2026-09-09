"""Only current baseline behavior; these tests do not solve the target lab."""

import pytest
from sensor_lab import Sensor, sample


def test_baseline_sample() -> None:
    assert sample("north") == "north:ready"


@pytest.mark.parametrize("station", ["", " ", "\t"])
def test_blank_station(station: str) -> None:
    with pytest.raises(ValueError, match="station required"):
        sample(station)


def test_sensor_rejects_use_after_close() -> None:
    sensor = Sensor("north")
    sensor.close()
    with pytest.raises(RuntimeError, match="closed"):
        sensor.read()
