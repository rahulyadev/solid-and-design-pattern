"""Pin only the documented version distinction demonstrated by the probe."""

from __future__ import annotations

import sys

from annotation_timing_probe import observe_annotation_timing


def test_annotation_timing_matches_the_running_language_version() -> None:
    observed = observe_annotation_timing()

    if sys.version_info >= (3, 14):  # noqa: UP036 - asserts both supported runtimes
        assert observed == [
            f"python={sys.version_info.major}.{sys.version_info.minor}",
            "definition=completed",
            "class_bound=True",
            "has_annotate=True",
            "evaluation=NameError",
        ]
    else:
        assert observed == [
            f"python={sys.version_info.major}.{sys.version_info.minor}",
            "definition=NameError",
            "class_bound=False",
        ]
