"""Observe registry ordering, sealing, and retained callable state."""

from dataclasses import dataclass
from typing import cast

from dispatch_tools import Event, Handler, RegistryBuilder, RegistrySealed, index_created


@dataclass
class PrefixHandler:
    prefix: str

    def __call__(self, event: Event, /, *, trace_id: str) -> str:
        return f"{trace_id}:{self.prefix}:{event.entity_id}"


def observations() -> dict[str, object]:
    stateful = PrefixHandler("first")
    builder = RegistryBuilder()
    builder.register("record.created", index_created)
    builder.register("record.custom", stateful)
    published = builder.seal()

    before = published["record.custom"](Event("record.custom", "R-5"), trace_id="probe")
    stateful.prefix = "second"
    after = published["record.custom"](Event("record.custom", "R-5"), trace_id="probe")

    try:
        cast(dict[str, Handler], published)["record.extra"] = index_created
    except TypeError as error:
        mapping_write = type(error).__name__
    else:  # pragma: no cover - MappingProxyType always rejects item assignment
        mapping_write = "accepted"

    try:
        builder.register("record.extra", index_created)
    except RegistrySealed as error:
        registration = f"{type(error).__name__}: {error}"
    else:  # pragma: no cover - the builder is sealed above
        registration = "accepted"

    return {
        "names": list(published),
        "mapping_write": mapping_write,
        "post_seal_registration": registration,
        "callable_before": before,
        "callable_after": after,
    }


def main() -> None:
    result = observations()
    names = cast(list[str], result["names"])
    print(f"names: {tuple(names)}")
    print(f"mapping write: {result['mapping_write']}")
    print(f"post-seal registration: {result['post_seal_registration']}")
    print(f"callable state before: {result['callable_before']}")
    print(f"callable state after: {result['callable_after']}")


if __name__ == "__main__":
    main()
