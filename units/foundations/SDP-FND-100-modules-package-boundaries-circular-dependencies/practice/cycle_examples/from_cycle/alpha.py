"""Start a failing immediate-name-binding cycle."""

from .beta import BETA_READY

ALPHA_READY = f"alpha saw {BETA_READY}"
