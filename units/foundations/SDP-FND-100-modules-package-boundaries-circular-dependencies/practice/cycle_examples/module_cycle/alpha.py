"""Bind beta's partial module object without requesting a later name immediately."""

from . import beta

ALPHA_READY = "alpha-ready"


def read_beta() -> str:
    """Look up beta's value only after both modules have initialized."""

    return beta.BETA_READY
