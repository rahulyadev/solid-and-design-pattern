"""Compile independently authored clients; assert specific failures, never execute bad clients."""

import os
import subprocess
import sys
from pathlib import Path

import pytest

POSITIVE = """from bridge import Artifact, Encoder, InventoryReport, JsonEncoder, Table
class External:
    def encode(self, table: Table, /) -> Artifact:
        return JsonEncoder().encode(table)
encoder: Encoder = External()
report = InventoryReport(encoder)
result: Artifact = report.render(())
"""
NEGATIVE = """from bridge import Artifact, Encoder, InventoryReport, JsonEncoder, Table
class WrongResult:
    def encode(self, table: Table, /) -> str:
        return "lost media type"
class MissingMember:
    def write(self, table: Table) -> Artifact:
        return Artifact("text/plain", "")
class ExtraArgument:
    def encode(self, table: Table, destination: str) -> Artifact:
        return Artifact("text/plain", destination)
a: Encoder = WrongResult()
b: Encoder = MissingMember()
c: Encoder = ExtraArgument()
report = InventoryReport(JsonEncoder())
report.encoder = JsonEncoder()
report.encoder.close()
report.render([])
"""


@pytest.mark.parametrize("version", ["3.11", "3.14"])
def test_positive_and_negative_client_contracts(tmp_path: Path, version: str) -> None:
    examples = Path(__file__).resolve().parent
    env = dict(os.environ, MYPYPATH=str(examples), MYPY_CACHE_DIR=str(tmp_path / "mypy"))
    expected = {
        11: "assignment",
        12: "assignment",
        13: "assignment",
        15: "misc",
        16: "attr-defined",
        17: "arg-type",
    }
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
            text=True,
            capture_output=True,
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
