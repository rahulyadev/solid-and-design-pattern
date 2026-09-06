"""Maintained semantic states for the SDP-PYT-060 interactive visual."""

from __future__ import annotations

from typing import Final

VISUAL_STATES: Final[dict[str, dict[str, object]]] = {
    "raw": {
        "title": "1. Raw boundary record",
        "risk": (
            "Strings, integers, and a list can still describe an unknown state or invalid value."
        ),
        "nodes": ["dict/list", "state='draft'", "amount=750", "currency='INR'"],
        "arrow": "parse and validate once",
    },
    "validated": {
        "title": "2. Validated value graph",
        "risk": (
            "Field rebinding is blocked, and tuples remove the obvious nested-list mutation path."
        ),
        "nodes": ["Quote", "QuoteState.DRAFT", "QuoteLine", "Money(INR, 750)"],
        "arrow": "confirm returns replacement",
    },
    "replacement": {
        "title": "3. New immutable snapshot",
        "risk": "The old draft remains observable; callers must choose which revision to retain.",
        "nodes": ["draft@r1", "confirmed@r2", "shared immutable lines", "explicit wire record"],
        "arrow": "serialize at boundary",
    },
}
