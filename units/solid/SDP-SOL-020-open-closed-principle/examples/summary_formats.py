"""Ordinary functions and a configurable callable object implement the same contract."""

import json
from dataclasses import dataclass

from summary_core import RunSummary


def text_summary(summary: RunSummary) -> str:
    return f"completed={summary.completed}; failed={summary.failed}"


def json_summary(summary: RunSummary) -> str:
    return json.dumps(
        {"completed": summary.completed, "failed": summary.failed},
        sort_keys=True,
        separators=(",", ":"),
    )


@dataclass(frozen=True)
class LabeledText:
    """The algorithm stays the same when only its two display labels vary."""

    completed_label: str
    failed_label: str

    def __post_init__(self) -> None:
        if not self.completed_label.strip() or not self.failed_label.strip():
            raise ValueError("labels must be nonblank")

    def __call__(self, summary: RunSummary) -> str:
        return f"{self.completed_label}={summary.completed}; {self.failed_label}={summary.failed}"
