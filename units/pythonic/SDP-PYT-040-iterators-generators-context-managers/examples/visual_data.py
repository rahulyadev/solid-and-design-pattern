"""Python-owned observation data embedded in the SDP-PYT-040 visual."""

from __future__ import annotations

from typing import Any

from context_lifecycle_probe import context_observations
from iterator_lifecycle_probe import iterator_observations


def visual_observations() -> dict[str, Any]:
    return {
        "iteration": iterator_observations(),
        "context": context_observations(),
    }
