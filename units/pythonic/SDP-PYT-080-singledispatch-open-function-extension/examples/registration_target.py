"""Generic function deliberately extended by the import-order experiment."""

from __future__ import annotations

from dataclasses import dataclass
from functools import singledispatch


@dataclass(frozen=True, slots=True)
class ExternalPayload:
    payload_id: str


@singledispatch
def summarize_external(value: object) -> str:
    return f"unsupported:{type(value).__name__}"
