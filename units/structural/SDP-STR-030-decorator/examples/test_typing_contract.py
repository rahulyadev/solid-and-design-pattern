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
        "from text_contract import TextSource\n"
        "from text_components import Bracket, Label, MemoryText, Observed\n"
        "from function_wrappers import traced\n"
        "source: TextSource = Observed(Bracket(Label(MemoryText({}), '')), lambda e: None)\n"
        "def text(key: str, /, *, prefix: str = '') -> str:\n"
        "    return prefix + key\n"
        "wrapped = traced([], 'text')(text)\n"
        "result: str = wrapped('N-1', prefix='note: ')\n"
    )
    good = subprocess.run(args, env=env, capture_output=True, text=True, check=False)
    assert good.returncode == 0, good.stdout + good.stderr
    fixture.write_text(
        "from text_contract import TextSource\n"
        "from function_wrappers import traced\n"
        "class WrongSource:\n"
        "    def render(self, key: str, /) -> bytes:\n"
        "        return b'not text'\n"
        "source: TextSource = WrongSource()\n"
        "def text(key: str, /, *, prefix: str = '') -> str:\n"
        "    return prefix + key\n"
        "wrapped = traced([], 'text')(text)\n"
        "wrapped(123)\n"
    )
    bad = subprocess.run(args, env=env, capture_output=True, text=True, check=False)
    assert bad.returncode == 1, bad.stdout + bad.stderr
    assert "[assignment]" in bad.stdout
    assert "[arg-type]" in bad.stdout
    assert "Found 2 errors" in bad.stdout
