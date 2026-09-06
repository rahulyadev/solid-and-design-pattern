"""Observable singledispatch mechanics without inspecting private internals."""

from __future__ import annotations

import json
from collections.abc import Container, Iterable
from dataclasses import asdict, dataclass
from functools import singledispatch


@dataclass(frozen=True, slots=True)
class MechanicsObservation:
    bool_before_exact_registration: str
    bool_after_exact_registration: str
    selected_after_exact_registration: str
    parameterized_registration_error: str
    ambiguous_abc_error: str


def observe_mechanics() -> MechanicsObservation:
    @singledispatch
    def classify(value: object) -> str:
        del value
        return "object"

    @classify.register
    def classify_int(value: int) -> str:
        del value
        return "int"

    bool_before = classify(True)

    @classify.register
    def classify_bool(value: bool) -> str:
        del value
        return "bool"

    bool_after = classify(True)

    try:
        classify.register(list[int], lambda value: "parameterized")
    except TypeError as error:
        parameterized_error = type(error).__name__
    else:  # pragma: no cover - incompatible with the supported runtimes
        parameterized_error = "no-error"

    class VirtualBoth:
        pass

    Iterable.register(VirtualBoth)
    Container.register(VirtualBoth)

    @singledispatch
    def choose_abc(value: object) -> str:
        del value
        return "object"

    @choose_abc.register(Iterable)
    def choose_iterable(value: object) -> str:
        del value
        return "iterable"

    @choose_abc.register(Container)
    def choose_container(value: object) -> str:
        del value
        return "container"

    try:
        choose_abc(VirtualBoth())
    except RuntimeError as error:
        ambiguous_error = type(error).__name__
    else:  # pragma: no cover - incompatible with the documented ambiguity rule
        ambiguous_error = "no-error"

    return MechanicsObservation(
        bool_before_exact_registration=bool_before,
        bool_after_exact_registration=bool_after,
        selected_after_exact_registration=classify.dispatch(bool).__name__,
        parameterized_registration_error=parameterized_error,
        ambiguous_abc_error=ambiguous_error,
    )


def main() -> None:
    print(json.dumps(asdict(observe_mechanics()), sort_keys=True))


if __name__ == "__main__":
    main()
