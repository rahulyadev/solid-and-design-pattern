"""Contrast ordinary instance lookup with implicit special-method lookup."""

from __future__ import annotations

from typing import Any, cast


class Batch:
    """Begin without class-level participation in the sized protocol."""


class SizedBatch(Batch):
    """Participate by defining the special method on the type."""

    def __len__(self) -> int:
        return 7


def main() -> None:
    """Record the difference without depending on exception wording."""

    batch = Batch()
    dynamic_batch = cast(Any, batch)
    dynamic_batch.__len__ = lambda: 5

    print(f"ordinary_explicit={dynamic_batch.__len__()}")
    try:
        len(batch)  # type: ignore[arg-type]
    except TypeError:
        print("implicit_instance_override=TypeError")

    sized = SizedBatch()
    print(f"implicit_type_method={len(sized)}")
    print(f"explicit_type_method={type(sized).__len__(sized)}")


if __name__ == "__main__":
    main()
