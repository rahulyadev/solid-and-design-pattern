"""Child program used to observe that an import cache belongs to one process."""

from __future__ import annotations

import importlib
import json
import os


def main() -> None:
    first = importlib.import_module("lifetime_cache_target")
    second = importlib.import_module("lifetime_cache_target")
    print(
        json.dumps(
            {
                "execution_count": first.execution_count,
                "module_reused": first is second,
                "pid": os.getpid(),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
