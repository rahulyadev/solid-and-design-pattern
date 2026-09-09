import os
import subprocess
import sys
from pathlib import Path

import pytest


@pytest.mark.parametrize("target", ["3.11", "3.14"])
def test_static_port_contract_with_positive_control(tmp_path: Path, target: str) -> None:
    env = dict(os.environ, MYPYPATH=str(Path(__file__).resolve().parent))
    env["MYPY_CACHE_DIR"] = str(tmp_path / "mypy")
    fixture = tmp_path / "port_case.py"
    args = [sys.executable, "-m", "mypy", "--strict", "--python-version", target, str(fixture)]
    fixture.write_text(
        "from report_contracts import Archive, PacketBuilder\n"
        "from report_facade import ReportFacade\n"
        "from report_subsystem import MemoryArchive, MemoryReports, TextRenderer\n"
        "events: list[str] = []\n"
        "archive: Archive = MemoryArchive(events)\n"
        "builder: PacketBuilder = ReportFacade(MemoryReports({}, events), "
        "TextRenderer(events), archive)\n"
    )
    good = subprocess.run(args, env=env, capture_output=True, text=True, check=False)
    assert good.returncode == 0, good.stdout + good.stderr
    fixture.write_text(
        "from report_contracts import Archive\n"
        "class WrongArchive:\n"
        "    def store(self, report_id: str, payload: bytes) -> str:\n"
        "        return 'not a receipt'\n"
        "archive: Archive = WrongArchive()\n"
    )
    bad = subprocess.run(args, env=env, capture_output=True, text=True, check=False)
    assert bad.returncode == 1, bad.stdout + bad.stderr
    assert "[assignment]" in bad.stdout
    assert "Found 1 error" in bad.stdout
