"""The runnable demo is deterministic and secret-free."""

from __future__ import annotations

import pytest
import run_factory_demo


def test_demo_output(capsys: pytest.CaptureFixture[str]) -> None:
    run_factory_demo.main()
    output = capsys.readouterr().out.splitlines()

    assert output == [
        "class=buffer:A-100:queue depth high",
        "function=buffer:A-101:worker recovered",
        "configured=framed:OPS|A-102|probe stable",
        "events=transport.created,transport.sent,transport.closed",
    ]
