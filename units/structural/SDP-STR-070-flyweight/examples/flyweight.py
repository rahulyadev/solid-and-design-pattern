"""Synthetic grayscale tiles; a single-thread-owned, bounded sharing scope."""

from dataclasses import dataclass, field
from typing import final


def bounded(value: int, name: str, low: int, high: int) -> None:
    """Typed callers supply ints; bool is deliberately rejected as a domain value."""
    if isinstance(value, bool) or not low <= value <= high:
        raise ValueError(f"{name} must be an integer in [{low}, {high}]")


@final
@dataclass(frozen=True, slots=True)
class TileKey:
    seed: int
    side: int = 32

    def __post_init__(self) -> None:
        bounded(self.seed, "seed", 0, 65535)
        bounded(self.side, "side", 1, 64)


@final
@dataclass(frozen=True, slots=True, weakref_slot=True)
class Tile:
    key: TileKey
    pixels: bytes = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        key = self.key
        pixels = bytes(
            (key.seed + (key.seed >> 8) * x + 17 * x + 31 * y) % 256
            for y in range(key.side)
            for x in range(key.side)
        )
        object.__setattr__(self, "pixels", pixels)

    def pixel(self, dx: int, dy: int) -> int:
        """Receive per-use offsets; never store the caller's context."""
        bounded(dx, "dx", 0, self.key.side - 1)
        bounded(dy, "dy", 0, self.key.side - 1)
        return self.pixels[dy * self.key.side + dx]


@final
@dataclass(frozen=True, slots=True)
class Pixel:
    placement_id: int
    x: int
    y: int
    shade: int


@final
@dataclass(frozen=True, slots=True)
class PlacedTile:
    placement_id: int
    x: int
    y: int
    tile: Tile

    def __post_init__(self) -> None:
        bounded(self.placement_id, "placement_id", 0, 1_000_000)
        bounded(self.x, "x", -1_000_000, 1_000_000)
        bounded(self.y, "y", -1_000_000, 1_000_000)

    def sample(self, dx: int, dy: int) -> Pixel:
        return Pixel(self.placement_id, self.x + dx, self.y + dy, self.tile.pixel(dx, dy))


class PoolFull(RuntimeError):
    """A new key exceeded the configured number of retained entries."""


@final
class TilePool:
    """Strong ownership until clear/drop; no global singleton or concurrent use."""

    def __init__(self, capacity: int = 64) -> None:
        bounded(capacity, "capacity", 1, 65536)
        self._capacity = capacity
        self._tiles: dict[TileKey, Tile] = {}

    @property
    def size(self) -> int:
        return len(self._tiles)

    def get(self, key: TileKey) -> Tile:
        existing = self._tiles.get(key)
        if existing is not None:
            return existing
        if self.size >= self._capacity:
            raise PoolFull("tile pool capacity reached; new key was not retained")
        tile = Tile(key)
        self._tiles[key] = tile
        return tile

    def clear(self) -> None:
        """Release pool references. Existing placements remain valid."""
        self._tiles.clear()
