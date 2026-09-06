"""Compare eager 3.11 and lazy 3.14 annotation timing without future flags."""

from __future__ import annotations

import sys
from typing import Any

SOURCE = """\
class Config:
    target: MissingType
"""


def observe_annotation_timing() -> list[str]:
    namespace: dict[str, Any] = {}
    code = compile(SOURCE, "annotation_timing_probe", "exec", dont_inherit=True)
    version = f"{sys.version_info.major}.{sys.version_info.minor}"
    try:
        exec(code, namespace)
    except NameError:
        return [
            f"python={version}",
            "definition=NameError",
            "class_bound=False",
        ]

    config = namespace["Config"]
    observations = [
        f"python={version}",
        "definition=completed",
        "class_bound=True",
        f"has_annotate={hasattr(config, '__annotate__')}",
    ]
    try:
        if sys.version_info >= (3, 14):  # noqa: UP036 - compares supported runtimes
            from annotationlib import get_annotations

            get_annotations(config)
        else:
            raise AssertionError("unexpected eager-runtime completion")
    except NameError:
        observations.append("evaluation=NameError")
    return observations


def main() -> None:
    print(*observe_annotation_timing(), sep="\n")


if __name__ == "__main__":
    main()
