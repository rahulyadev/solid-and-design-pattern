"""Compare a small conditional baseline with an explicit extension boundary."""

import json
from collections.abc import Callable

from summary_core import Renderer, RunSummary, publish_summary
from summary_formats import LabeledText, json_summary, text_summary
from summary_registry import build_renderers, select_renderer


def publish_by_name(
    summary: RunSummary,
    format_name: str,
    write: Callable[[str], None],
) -> str:
    """A reasonable baseline while the two output formats form a small, stable set."""
    if format_name == "text":
        body = f"completed={summary.completed}; failed={summary.failed}"
    elif format_name == "json":
        body = json.dumps(
            {"completed": summary.completed, "failed": summary.failed},
            sort_keys=True,
            separators=(",", ":"),
        )
    else:
        raise ValueError(f"unsupported format: {format_name}")
    write(body)
    return body


def compact_summary(summary: RunSummary) -> str:
    """An added representation; the core module does not import this function."""
    return f"ok:{summary.completed}/error:{summary.failed}"


def main() -> None:
    summary = RunSummary(completed=4, failed=1)
    baseline_writes: list[str] = []
    print("baseline:", publish_by_name(summary, "text", baseline_writes.append))

    entries: list[tuple[str, Renderer]] = [
        ("text", text_summary),
        ("json", json_summary),
        ("compact", compact_summary),
        ("labels", LabeledText("finished", "errors")),
    ]
    renderers = build_renderers(entries)
    writes: list[str] = []
    for name in renderers:
        selected = select_renderer(name, renderers)
        body = publish_summary(summary, selected, writes.append)
        print(f"{name}: {body}")
    print(f"extension writes: {len(writes)}")


if __name__ == "__main__":
    main()
