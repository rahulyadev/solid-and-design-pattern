"""Reproducible observations for import caching, aliases, and reload."""

from __future__ import annotations

import importlib
import json
import sys
from types import ModuleType
from typing import Protocol, cast

TARGET_NAME = "lifetime_cache_target"


class ProbeModule(Protocol):
    execution_count: int
    marker: object


def _load() -> ProbeModule:
    return cast(ProbeModule, importlib.import_module(TARGET_NAME))


def observe_import_cache() -> dict[str, bool | int]:
    """Run an isolated cache sequence and restore any earlier target binding."""

    previous = sys.modules.pop(TARGET_NAME, None)
    try:
        first = _load()
        first_count = first.execution_count
        imported_alias = first.marker
        second = _load()

        repeat_same_module = first is second
        count_after_repeat = second.execution_count

        reloaded = cast(ProbeModule, importlib.reload(cast(ModuleType, first)))
        reload_same_module = reloaded is first
        count_after_reload = reloaded.execution_count
        alias_still_old = imported_alias is not reloaded.marker

        retained_module = reloaded
        del sys.modules[TARGET_NAME]
        fresh = _load()

        return {
            "first_execution_count": first_count,
            "repeat_returns_same_module": repeat_same_module,
            "execution_count_after_repeat": count_after_repeat,
            "reload_reuses_module": reload_same_module,
            "execution_count_after_reload": count_after_reload,
            "imported_alias_stays_old": alias_still_old,
            "cache_deletion_creates_new_module": fresh is not retained_module,
            "new_module_execution_count": fresh.execution_count,
        }
    finally:
        sys.modules.pop(TARGET_NAME, None)
        if previous is not None:
            sys.modules[TARGET_NAME] = previous


def main() -> None:
    print(json.dumps(observe_import_cache(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
