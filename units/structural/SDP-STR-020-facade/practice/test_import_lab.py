"""Baseline behavior only; these tests do not grade or implement the target."""

import pytest
from import_lab import (
    Capacity,
    FileInfo,
    Inspector,
    build_preflight,
    cli_preview,
    web_preview,
)


@pytest.mark.parametrize("remaining, fits", [(3, False), (4, True), (5, True)])
def test_baseline_clients(remaining: int, fits: bool) -> None:
    inspector = Inspector((FileInfo("sample.txt", 4, True),))
    capacity = Capacity(remaining)
    assert cli_preview(inspector, capacity) == f"files=1; bytes=4; fits={fits}"
    assert web_preview(inspector, capacity) == {"count": 1, "bytes": 4, "fits": fits}


def test_baseline_empty() -> None:
    assert web_preview(Inspector(()), Capacity(0)) == {"count": 0, "bytes": 0, "fits": True}


def test_exercise_starts_unsolved() -> None:
    with pytest.raises(NotImplementedError, match="SDP-STR-020"):
        build_preflight(Inspector(()), Capacity(0))
