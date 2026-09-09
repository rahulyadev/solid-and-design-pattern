import os
import subprocess
import sys
from pathlib import Path

import pytest


@pytest.mark.parametrize("target", ["3.11", "3.14"])
def test_positive_and_negative_contracts(tmp_path: Path, target: str) -> None:
    env = dict(os.environ, MYPYPATH=str(Path(__file__).resolve().parent))
    env["MYPY_CACHE_DIR"] = str(tmp_path / "mypy")
    fixture = tmp_path / "contract_case.py"
    args = [sys.executable, "-m", "mypy", "--strict", "--python-version", target, str(fixture)]
    fixture.write_text(
        "from work_plan import Estimable, Estimate, Task, Group, describe\n"
        "leaf: Estimable = Task('cut', 12)\n"
        "group: Estimable = Group('kit', (Task('cut', 12),))\n"
        "class External:\n"
        "    def estimate(self) -> Estimate:\n"
        "        return Estimate(1, 1)\n"
        "external: Estimable = External()\n"
        "text: str = describe(external)\n"
    )
    good = subprocess.run(args, env=env, capture_output=True, text=True, check=False)
    assert good.returncode == 0, good.stdout + good.stderr
    fixture.write_text(
        "from work_plan import Estimable, Estimate, Task, Group\n"
        "class WrongResult:\n"
        "    def estimate(self) -> int:\n"
        "        return 1\n"
        "class External:\n"
        "    def estimate(self) -> Estimate:\n"
        "        return Estimate(1, 1)\n"
        "wrong: Estimable = WrongResult()\n"
        "missing: Estimable = object()\n"
        "group = Group('kit', (External(),))\n"
        "group.children = ()\n"
        "leaf = Task('cut', 1)\n"
        "leaf.add(Task('tag', 2))\n"
    )
    bad = subprocess.run(args, env=env, capture_output=True, text=True, check=False)
    assert bad.returncode == 1, bad.stdout + bad.stderr
    assert bad.stdout.count("[assignment]") == 2
    assert bad.stdout.count("[arg-type]") == 1
    assert bad.stdout.count("[misc]") == 1  # frozen children assignment
    assert bad.stdout.count("[attr-defined]") == 1  # no child-management operation on a leaf
    assert "Found 5 errors" in bad.stdout
