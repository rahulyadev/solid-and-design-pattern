"""Observe how one strong registry reference extends an object's lifetime."""

from __future__ import annotations

import gc
import weakref


class Session:
    """A weak-referenceable synthetic application session."""


def observe_weak_reference() -> dict[str, bool]:
    """Report reachability before and after removing the final strong owner."""

    session = Session()
    observer = weakref.ref(session)
    strong_registry = {"session-7": session}

    del session
    gc.collect()
    alive_while_registered = observer() is not None

    strong_registry.clear()
    gc.collect()
    dead_after_owner_releases = observer() is None

    return {
        "alive_while_strongly_registered": alive_while_registered,
        "dead_after_strong_owner_releases": dead_after_owner_releases,
    }


def main() -> None:
    """Print stable observations for the experiment record."""

    for key, value in observe_weak_reference().items():
        print(f"{key}={value}")


if __name__ == "__main__":
    main()
