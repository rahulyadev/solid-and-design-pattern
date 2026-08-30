"""Run the worked example; this is separate from the unsolved dispatch exercise."""

from alert_formats import json_format, text_format
from alert_policy import Reading, build_report
from coupled_alerts import text_report


def legacy_format(rows: tuple[Reading, ...]) -> str:
    return "\n".join(f"reading={row.station}, temperature={row.celsius} C" for row in rows)


def main() -> None:
    readings = [Reading("east", 29), Reading("roof", 35), Reading("west", 30)]
    original = list(readings)
    baseline = text_report(readings, 30)
    compatible = build_report(readings, 30, legacy_format)
    print(f"legacy output preserved: {baseline == compatible}")
    print("text:")
    print(build_report(readings, 30, text_format))
    print("json:")
    print(build_report(readings, 30, json_format))
    print(f"input unchanged: {readings == original}")


if __name__ == "__main__":
    main()
