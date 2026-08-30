"""Show compatible replacements and deliberately incompatible counterexamples."""

from collections.abc import Callable, Mapping
from functools import partial

from catalog_contracts import (
    BlankOnMissingCatalog,
    Catalog,
    ConsumingCatalog,
    DictCatalog,
    LeakyErrorCatalog,
    RestrictedCatalog,
    TupleCatalog,
    UnknownCode,
    label_or_unlisted,
    lookup_twice,
)


def observe(action: Callable[[], object]) -> str:
    """Catch the known demonstration failures; not an application error policy."""
    try:
        return repr(action())
    except (UnknownCode, ValueError, KeyError) as error:
        return type(error).__name__


def run_demo() -> tuple[str, ...]:
    factories: tuple[Callable[[Mapping[str, str]], Catalog], ...] = (
        DictCatalog,
        TupleCatalog,
        RestrictedCatalog,
        BlankOnMissingCatalog,
        ConsumingCatalog,
        LeakyErrorCatalog,
    )
    lines: list[str] = []
    for factory in factories:
        catalog = factory({"x": "parcel", "box": "crate"})
        repeated = observe(partial(lookup_twice, catalog, "x"))
        missing = observe(partial(label_or_unlisted, catalog, "absent"))
        lines.append(f"{type(catalog).__name__}: repeated={repeated}; missing={missing}")
    return tuple(lines)


if __name__ == "__main__":
    print("\n".join(run_demo()))
