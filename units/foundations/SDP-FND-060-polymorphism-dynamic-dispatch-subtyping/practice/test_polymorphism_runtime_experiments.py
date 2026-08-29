"""Deterministic checks for the SDP-FND-060 observation scripts."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def run_script(filename: str) -> list[str]:
    """Run one neighboring experiment in a fresh interpreter."""

    script = Path(__file__).with_name(filename)
    completed = subprocess.run(
        [sys.executable, str(script)],
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip().splitlines()


def test_receiver_dispatch_observation() -> None:
    assert run_script("receiver_dispatch_experiment.py") == [
        "runtime_type=LoyaltyPricePolicy",
        "dynamic_result=9000",
        "dynamic_trace=PricePolicy.final_price -> LoyaltyPricePolicy.discount",
        "bound_receiver=LoyaltyPricePolicy",
        "bound_function=LoyaltyPricePolicy.discount",
        "explicit_base_result=0",
        "explicit_base_trace=PricePolicy.discount",
    ]


def test_special_method_dispatch_observation() -> None:
    assert run_script("special_method_dispatch_experiment.py") == [
        "ordinary_explicit=5",
        "implicit_instance_override=TypeError",
        "implicit_type_method=7",
        "explicit_type_method=7",
    ]
