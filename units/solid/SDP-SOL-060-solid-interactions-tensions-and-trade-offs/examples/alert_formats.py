"""Presentation details depend on the policy's data vocabulary."""

import json

from alert_policy import Reading


def text_format(rows: tuple[Reading, ...]) -> str:
    """Human-readable lines, in the selected order; empty input produces empty text."""
    return "\n".join(f"{row.station}: {row.celsius} C" for row in rows)


def json_format(rows: tuple[Reading, ...]) -> str:
    """Machine-readable records, including units in the field name."""
    return json.dumps(
        [{"station": row.station, "celsius": row.celsius} for row in rows],
        ensure_ascii=False,
    )
