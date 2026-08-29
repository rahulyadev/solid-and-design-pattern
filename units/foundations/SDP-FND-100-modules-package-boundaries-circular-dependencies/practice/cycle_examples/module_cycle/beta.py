"""Record what alpha exposes while alpha is only partially initialized."""

from . import alpha

ALPHA_READY_VISIBLE_DURING_BETA_LOAD = hasattr(alpha, "ALPHA_READY")
BETA_READY = "beta-ready"
