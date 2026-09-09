"""Value behavior survives sharing and pool clearing."""

from flyweight import PlacedTile, TileKey, TilePool


def main() -> None:
    pool = TilePool(2)
    first = PlacedTile(10, 100, 200, pool.get(TileKey(7, 4)))
    second = PlacedTile(11, -10, 20, pool.get(TileKey(7, 4)))
    print(f"same tile={first.tile is second.tile}, distinct placements={first != second}")
    print(first.sample(1, 2))
    print(second.sample(1, 2))
    pool.clear()
    replacement = pool.get(TileKey(7, 4))
    print(f"after clear: equal={replacement == first.tile}, same={replacement is first.tile}")
    print(f"old placement still works: {first.sample(1, 2)}")


if __name__ == "__main__":
    main()
