"""Observe why a patch must target the name used by the system under test."""

from __future__ import annotations

import uuid
from unittest.mock import patch
from uuid import UUID, uuid4

FIXED_FROM_MODULE = UUID("11111111-1111-1111-1111-111111111111")
FIXED_IMPORTED_NAME = UUID("22222222-2222-2222-2222-222222222222")


def token_via_imported_name() -> UUID:
    return uuid4()


def token_via_module_lookup() -> UUID:
    return uuid.uuid4()


def observe_patch_lookup() -> dict[str, bool]:
    """Patch each lookup path and report only stable boolean observations."""

    with patch("uuid.uuid4", return_value=FIXED_FROM_MODULE):
        definition_patch_changed_imported_alias = token_via_imported_name() == FIXED_FROM_MODULE
        definition_patch_changed_module_lookup = token_via_module_lookup() == FIXED_FROM_MODULE

    with patch(f"{__name__}.uuid4", return_value=FIXED_IMPORTED_NAME):
        use_site_patch_changed_imported_alias = token_via_imported_name() == FIXED_IMPORTED_NAME

    return {
        "definition_patch_changed_imported_alias": definition_patch_changed_imported_alias,
        "definition_patch_changed_module_lookup": definition_patch_changed_module_lookup,
        "use_site_patch_changed_imported_alias": use_site_patch_changed_imported_alias,
    }


def main() -> None:
    for name, result in observe_patch_lookup().items():
        print(f"{name}={result}")


if __name__ == "__main__":
    main()
