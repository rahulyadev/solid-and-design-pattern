"""A reasonable single-format starting point, before format changes are frequent."""

from collections.abc import Sequence

from alert_policy import Reading


def text_report(readings: Sequence[Reading], cutoff: int) -> str:
    return "\n".join(
        f"reading={row.station}, temperature={row.celsius} C"
        for row in readings
        if row.celsius >= cutoff
    )
