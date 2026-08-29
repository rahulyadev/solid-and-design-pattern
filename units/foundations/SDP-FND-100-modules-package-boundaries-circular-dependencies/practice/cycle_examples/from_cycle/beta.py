"""Request alpha's not-yet-defined name during its import."""

from .alpha import ALPHA_READY

# The unresolved type is the mechanism under observation in this deliberate import cycle.
BETA_READY = f"beta saw {ALPHA_READY}"  # type: ignore[has-type]
