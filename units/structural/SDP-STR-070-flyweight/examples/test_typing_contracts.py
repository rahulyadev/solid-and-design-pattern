"""Accept real value clients; reject contract violations without executing them."""

import os
import subprocess
import sys
from pathlib import Path

import pytest

POSITIVE = """from flyweight import Pixel, PlacedTile, Tile, TileKey, TilePool
pool = TilePool(2)
tile: Tile = pool.get(TileKey(7, 4))
result: Pixel = PlacedTile(1, 0, 0, tile).sample(1, 2)
shade: int = tile.pixel(0, 0)
"""
NEGATIVE = """from flyweight import PlacedTile, Tile, TileKey, TilePool
key = TileKey(7, 4)
tile = Tile(key)
key.seed = 9
tile.pixels = b"changed"
Tile(key, pixels=b"injected")
TilePool().get((7, 4))
PlacedTile(1, 0, 0, key)
tile.pixel("0", 0)
wrong: str = tile.pixel(0, 0)
TilePool().size = 9
class MutableTile(Tile):
    pass
"""


@pytest.mark.parametrize("version", ["3.11", "3.14"])
def test_typed_clients(tmp_path: Path, version: str) -> None:
    expected = {
        4: "misc",
        5: "misc",
        6: "call-arg",
        7: "arg-type",
        8: "arg-type",
        9: "arg-type",
        10: "assignment",
        11: "misc",
        12: "misc",
    }
    env = dict(
        os.environ,
        MYPYPATH=str(Path(__file__).resolve().parent),
        MYPY_CACHE_DIR=str(tmp_path / "mypy"),
    )
    for name, source in (("positive", POSITIVE), ("negative", NEGATIVE)):
        path = tmp_path / f"{name}.py"
        path.write_text(source)
        run = subprocess.run(
            [
                sys.executable,
                "-m",
                "mypy",
                "--strict",
                "--python-version",
                version,
                "--show-error-codes",
                "--no-error-summary",
                str(path),
            ],
            capture_output=True,
            text=True,
            env=env,
            check=False,
        )
        if name == "positive":
            assert run.returncode == 0, run.stdout + run.stderr
        else:
            assert run.returncode == 1, run.stdout + run.stderr
            errors = [line for line in run.stdout.splitlines() if ": error:" in line]
            assert len(errors) == len(expected), run.stdout
            for line, code in expected.items():
                assert any(
                    f"negative.py:{line}: error:" in error and f"[{code}]" in error
                    for error in errors
                ), run.stdout
