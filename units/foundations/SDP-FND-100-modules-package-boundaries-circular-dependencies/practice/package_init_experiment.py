"""Observe transitive eager work caused by a regular package initializer."""

from __future__ import annotations

import importlib
import sys

PACKAGE_NAME = "eager_package"


def _clear_package() -> None:
    for name in tuple(sys.modules):
        if name == PACKAGE_NAME or name.startswith(f"{PACKAGE_NAME}."):
            sys.modules.pop(name, None)


def observe_package_initializer() -> dict[str, object]:
    """Import one leaf and return the initializer's exact execution trace."""

    _clear_package()
    leaf = importlib.import_module(f"{PACKAGE_NAME}.leaf")
    package = sys.modules[PACKAGE_NAME]
    observation = {
        "requested_leaf_value": leaf.LEAF_VALUE,
        "public_module_loaded_transitively": f"{PACKAGE_NAME}.public_api" in sys.modules,
        "execution_trace": tuple(package.TRACE),
    }
    _clear_package()
    return observation


def main() -> None:
    """Print stable observations for the experiment record."""

    for key, value in observe_package_initializer().items():
        print(f"{key}={value}")


if __name__ == "__main__":
    main()
