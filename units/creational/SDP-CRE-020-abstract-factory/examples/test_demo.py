"""Smoke test the learner-facing demo output."""

from __future__ import annotations

import pytest
from run_abstract_factory_demo import main


def test_demo_output(capsys: pytest.CaptureFixture[str]) -> None:
    main()
    output = capsys.readouterr().out
    assert "family=json-v1; delivery_id=json:EVT-7; accepted=True" in output
    assert "family=pipe-v1; delivery_id=pipe:EVT-7; accepted=True" in output
    assert output.count("delivery.succeeded") == 2
