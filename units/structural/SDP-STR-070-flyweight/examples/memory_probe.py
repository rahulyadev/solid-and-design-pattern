"""Controlled retained-allocation experiment; each trial uses a fresh child process."""

import argparse
import gc
import json
import platform
import statistics
import subprocess
import sys
import sysconfig
import tracemalloc
from typing import Literal

from flyweight import PlacedTile, Tile, TileKey, TilePool

Mode = Literal["fresh", "explicit", "pooled"]
N = 4000
SIDE = 32
TRIALS = 3


def build(
    mode: Mode, n: int, distinct: int
) -> tuple[list[PlacedTile], TilePool | dict[int, Tile] | None]:
    if not 1 <= distinct <= n <= 65536:
        raise ValueError("require 1 <= distinct <= n <= 65536")
    pool = TilePool(distinct) if mode == "pooled" else None
    catalog = {i: Tile(TileKey(i, SIDE)) for i in range(distinct)} if mode == "explicit" else {}
    placements: list[PlacedTile] = []
    for i in range(n):
        seed = i % distinct
        if pool is not None:
            tile = pool.get(TileKey(seed, SIDE))
        elif mode == "explicit":
            tile = catalog[seed]
        else:
            tile = Tile(TileKey(seed, SIDE))
        placements.append(PlacedTile(i, i, -i, tile))
    owner = pool if pool is not None else catalog if mode == "explicit" else None
    return placements, owner


def measure(mode: Mode, n: int, distinct: int) -> dict[str, int]:
    gc.collect()
    tracemalloc.start(1)
    baseline = tracemalloc.get_traced_memory()[0]
    placements, owner = build(mode, n, distinct)
    retained = tracemalloc.get_traced_memory()[0] - baseline
    # Count only after measuring; the identity set is not charged to the live workload.
    unique = len({id(placed.tile) for placed in placements})
    checksum = sum(placed.sample(1, 2).shade for placed in placements)
    del placements
    gc.collect()
    after_drop = tracemalloc.get_traced_memory()[0] - baseline
    if owner is not None:
        owner.clear()
    gc.collect()
    after_clear = tracemalloc.get_traced_memory()[0] - baseline
    tracemalloc.stop()
    return {
        "retained": retained,
        "after_drop": after_drop,
        "after_clear": after_clear,
        "live_tiles": unique,
        "checksum": checksum,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--child", choices=("fresh", "explicit", "pooled"))
    parser.add_argument("--distinct", type=int, default=8)
    args = parser.parse_args()
    if args.child is not None:
        print(json.dumps(measure(args.child, N, args.distinct)))
        return
    print(f"implementation={sys.implementation.name} version={sys.version}")
    print(
        f"platform={platform.platform()} "
        f"Py_GIL_DISABLED={sysconfig.get_config_var('Py_GIL_DISABLED')}"
    )
    print(f"N={N} side={SIDE} trials={TRIALS} fresh_process_per_trial=True")
    for distinct in (8, N):
        for mode in ("fresh", "explicit", "pooled"):
            rows: list[dict[str, int]] = []
            for _ in range(TRIALS):
                run = subprocess.run(
                    [sys.executable, __file__, "--child", mode, "--distinct", str(distinct)],
                    text=True,
                    capture_output=True,
                    check=True,
                )
                rows.append(json.loads(run.stdout))
            assert len({row["checksum"] for row in rows}) == 1
            retained = [row["retained"] for row in rows]
            print(
                f"K={distinct} mode={mode} live_tiles={rows[0]['live_tiles']} "
                f"checksum={rows[0]['checksum']} retained_bytes={retained} "
                f"median={int(statistics.median(retained))} "
                f"after_drop={[r['after_drop'] for r in rows]} "
                f"after_clear={[r['after_clear'] for r in rows]}"
            )


if __name__ == "__main__":
    main()
