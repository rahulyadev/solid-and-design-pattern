import os
import subprocess
import sys
from pathlib import Path

import pytest


@pytest.mark.parametrize("target", ["3.11", "3.14"])
def test_negative_assignment_and_positive_control(tmp_path: Path, target: str) -> None:
    example_dir = Path(__file__).resolve().parent
    env = dict(os.environ, MYPYPATH=str(example_dir))
    env["MYPY_CACHE_DIR"] = str(tmp_path / "mypy")
    fixture = tmp_path / "contract_case.py"
    common = "from stock_contract import StockReader\nfrom boundary_probe import "
    fixture.write_text(common + "CountsCases\nreader: StockReader = CountsCases()\n")
    args = [sys.executable, "-m", "mypy", "--strict", "--python-version", target, str(fixture)]
    positive = subprocess.run(args, env=env, capture_output=True, text=True, check=False)
    assert positive.returncode == 0, positive.stdout + positive.stderr
    fixture.write_text(common + "WrongSignature\nreader: StockReader = WrongSignature()\n")
    negative = subprocess.run(args, env=env, capture_output=True, text=True, check=False)
    assert negative.returncode == 1, negative.stdout + negative.stderr
    assert "[assignment]" in negative.stdout
    assert "Incompatible types in assignment" in negative.stdout
    assert "Found 1 error" in negative.stdout
