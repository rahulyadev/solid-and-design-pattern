"""Green tests prove that the deliberately invalid implementations are detected."""

import subprocess
import sys

import pytest
from shape_probe import (
    STATIC_SEMANTIC_GAP,
    STATIC_SIGNATURE_MISMATCH,
    ByteCounter,
    UTF8Counter,
    ZeroCounter,
    observe,
    run_probe,
)


@pytest.mark.parametrize("text", ["", "a", "ñ", "नमस्ते", "🙂"])
def test_working_counter_obeys_the_value_contract(text: str) -> None:
    assert UTF8Counter().count(text) == len(text.encode("utf-8"))


def test_compatible_signature_does_not_establish_the_value_contract() -> None:
    counter: ByteCounter = ZeroCounter()
    assert counter.count("ñ") != 2


def test_runtime_shape_alone_accepts_all_three_candidates() -> None:
    assert run_probe() == (
        "UTF8Counter: runtime=True; count('ñ')=2",
        "ZeroCounter: runtime=True; count('ñ')=0",
        "WrongArityCounter: runtime=True; count('ñ')=TypeError",
    )


def test_missing_attribute_is_not_called() -> None:
    assert observe(object()) == "object: runtime=False; not called"


@pytest.mark.parametrize(
    ("source", "expected_code"),
    [(STATIC_SEMANTIC_GAP, 0), (STATIC_SIGNATURE_MISMATCH, 1)],
)
def test_static_checker_distinguishes_signature_but_not_meaning(
    source: str, expected_code: int
) -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "mypy",
            "--strict",
            "--no-incremental",
            "--python-version",
            f"{sys.version_info.major}.{sys.version_info.minor}",
            "--command",
            source,
        ],
        capture_output=True,
        text=True,
        check=False,
        timeout=60,
    )
    assert result.returncode == expected_code, result.stdout + result.stderr
    if expected_code:
        assert "[assignment]" in result.stdout
        assert "WrongArityCounter" in result.stdout
        assert "ByteCounter" in result.stdout
    else:
        assert "Success: no issues found" in result.stdout
