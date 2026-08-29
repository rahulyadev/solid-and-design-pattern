"""Observe normal import reuse, reload, and cache deletion in a controlled module."""

from __future__ import annotations

import importlib
import sys

PROBE_NAME = "module_cache_probe"


def observe_module_cache() -> dict[str, object]:
    """Return identity and execution observations from one isolated cache lifecycle."""

    sys.modules.pop(PROBE_NAME, None)
    first = importlib.import_module(PROBE_NAME)
    first_token = first.TOKEN
    second = importlib.import_module(PROBE_NAME)

    executions_after_second_import = second.EXECUTIONS
    reloaded = importlib.reload(first)
    token_replaced_by_reload = reloaded.TOKEN is not first_token

    old_reference = reloaded
    sys.modules.pop(PROBE_NAME, None)
    fresh = importlib.import_module(PROBE_NAME)
    observation = {
        "same_object_after_second_import": first is second,
        "executions_after_second_import": executions_after_second_import,
        "same_object_after_reload": reloaded is first,
        "executions_after_reload": reloaded.EXECUTIONS,
        "token_replaced_by_reload": token_replaced_by_reload,
        "new_object_after_cache_deletion": fresh is not old_reference,
        "fresh_executions_after_cache_deletion": fresh.EXECUTIONS,
    }
    sys.modules.pop(PROBE_NAME, None)
    return observation


def main() -> None:
    """Print stable observations for the experiment record."""

    for key, value in observe_module_cache().items():
        print(f"{key}={value}")


if __name__ == "__main__":
    main()
