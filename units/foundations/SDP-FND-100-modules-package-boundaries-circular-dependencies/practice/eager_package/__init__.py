"""Deliberately eager package surface for an import-cascade experiment."""

TRACE: list[str] = ["package-init"]

from .public_api import PUBLIC_VALUE as PUBLIC_VALUE  # noqa: E402

__all__ = ["PUBLIC_VALUE"]
