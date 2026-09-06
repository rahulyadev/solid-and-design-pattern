"""End-to-end output contract for the Builder demo."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_demo_output_is_stable_and_contains_no_key_reference() -> None:
    script = Path(__file__).with_name("run_builder_demo.py")
    result = subprocess.run(
        [sys.executable, str(script)],
        check=True,
        capture_output=True,
        text=True,
    )

    assert result.stdout.splitlines() == [
        "fluent: customer-export 2 columns jsonl external-transfer",
        "director: daily-activity 2 columns gzip",
        "manifest: 11 entries build",
        "observations: build.succeeded 2",
    ]
    assert "kms/" not in result.stdout
