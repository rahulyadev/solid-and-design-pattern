"""Domain behavior, canonicalization scope, retention and failure boundaries."""

import gc
import weakref
from dataclasses import FrozenInstanceError

import pytest
from flyweight import Pixel, PlacedTile, PoolFull, Tile, TileKey, TilePool
from hypothesis import given, settings
from hypothesis import strategies as st


@pytest.mark.parametrize("seed", [0, 7, 255, 256, 65535])
@pytest.mark.parametrize("side", [1, 4, 64])
def test_pixel_generation_and_boundary(seed: int, side: int) -> None:
    tile = Tile(TileKey(seed, side))
    assert len(tile.pixels) == side * side
    for dx, dy in ((0, 0), (side - 1, side - 1)):
        assert tile.pixel(dx, dy) == (seed + (seed >> 8) * dx + 17 * dx + 31 * dy) % 256


@pytest.mark.parametrize("seed,side", [(-1, 4), (65536, 4), (1, 0), (1, 65), (True, 4), (1, False)])
def test_invalid_key(seed: int, side: int) -> None:
    with pytest.raises(ValueError):
        TileKey(seed, side)


@pytest.mark.parametrize("capacity", [0, -1, 65537, True])
def test_invalid_capacity(capacity: int) -> None:
    with pytest.raises(ValueError):
        TilePool(capacity)


@pytest.mark.parametrize("dx,dy", [(-1, 0), (0, -1), (4, 0), (0, 4), (True, 0), (0, False)])
def test_invalid_sample(dx: int, dy: int) -> None:
    with pytest.raises(ValueError):
        Tile(TileKey(1, 4)).pixel(dx, dy)


def test_equal_keys_reuse_inside_one_scope() -> None:
    pool = TilePool(1)
    a, b = TileKey(9, 4), TileKey(9, 4)
    assert a == b and a is not b and hash(a) == hash(b)
    assert pool.get(a) is pool.get(b)
    assert pool.size == 1


def test_full_key_separates_variants() -> None:
    pool = TilePool(3)
    tiles = [pool.get(key) for key in (TileKey(0, 4), TileKey(1, 4), TileKey(0, 5))]
    assert len({id(tile) for tile in tiles}) == 3
    assert pool.size == 3
    assert len(tiles[2].pixels) == 25


def test_capacity_failure_preserves_hits_and_contents() -> None:
    pool = TilePool(1)
    old = pool.get(TileKey(1))
    with pytest.raises(PoolFull):
        pool.get(TileKey(2))
    assert pool.size == 1
    assert pool.get(TileKey(1)) is old
    pool.clear()
    assert pool.size == 0
    assert pool.get(TileKey(2)).key == TileKey(2)


def test_direct_and_separate_scope_values_are_substitutable() -> None:
    key = TileKey(7, 4)
    a, b, direct = TilePool().get(key), TilePool().get(key), Tile(key)
    assert a is not b and a is not direct
    assert a == b == direct and hash(a) == hash(b) == hash(direct)
    assert PlacedTile(9, -2, 3, a).sample(1, 2) == PlacedTile(9, -2, 3, direct).sample(1, 2)


def test_clear_ends_identity_scope_without_revoking_borrowers() -> None:
    pool = TilePool()
    old = pool.get(TileKey(7, 4))
    placed = PlacedTile(9, 10, 20, old)
    before = placed.sample(1, 2)
    pool.clear()
    pool.clear()
    new = pool.get(TileKey(7, 4))
    assert new == old and new is not old
    assert placed.sample(1, 2) == before == Pixel(9, 11, 22, 86)


def test_shared_tile_does_not_store_placement_context() -> None:
    tile = TilePool().get(TileKey(7, 4))
    a, b = PlacedTile(1, 0, 0, tile), PlacedTile(2, -5, 30, tile)
    assert a != b
    assert a.sample(1, 2) == Pixel(1, 1, 2, 86)
    assert b.sample(1, 2) == Pixel(2, -4, 32, 86)
    assert a.sample(0, 0) == Pixel(1, 0, 0, 7)


@pytest.mark.parametrize(
    "identity,x,y",
    [(-1, 0, 0), (1_000_001, 0, 0), (0, -1_000_001, 0), (0, 0, 1_000_001), (True, 0, 0)],
)
def test_invalid_placement(identity: int, x: int, y: int) -> None:
    with pytest.raises(ValueError):
        PlacedTile(identity, x, y, Tile(TileKey(0)))


def test_normal_frozen_api_rejects_changes() -> None:
    tile = Tile(TileKey(7))
    with pytest.raises(FrozenInstanceError):
        tile.pixels = b"changed"  # type: ignore[misc]  # Deliberate runtime negative.
    with pytest.raises(FrozenInstanceError):
        tile.key.seed = 8  # type: ignore[misc]  # Deliberate runtime negative.
    with pytest.raises(FrozenInstanceError):
        PlacedTile(1, 0, 0, tile).x = 8  # type: ignore[misc]  # Deliberate runtime negative.


def test_pool_strongly_retains_until_clear_then_live_placement_owns() -> None:
    pool = TilePool()
    tile = pool.get(TileKey(7))
    witness = weakref.ref(tile)
    placed = PlacedTile(1, 0, 0, tile)
    del tile
    gc.collect()
    assert witness() is not None
    pool.clear()
    gc.collect()
    assert witness() is placed.tile
    del placed
    gc.collect()
    assert witness() is None  # Observed after explicit collection, not a finalization deadline.


@settings(max_examples=40, derandomize=True, deadline=None, database=None)
@given(seed=st.integers(0, 65535), side=st.integers(1, 16), x=st.integers(-50, 50))
def test_fresh_and_shared_observations_match(seed: int, side: int, x: int) -> None:
    key = TileKey(seed, side)
    pool = TilePool(1)
    fresh = PlacedTile(3, x, -x, Tile(key))
    shared = PlacedTile(3, x, -x, pool.get(key))
    assert fresh == shared
    assert [fresh.sample(dx, side - 1) for dx in range(side)] == [
        shared.sample(dx, side - 1) for dx in range(side)
    ]
