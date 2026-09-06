"""Executable descriptor lookup and method-binding observations."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LookupObservation:
    expression: str
    result: str


class DataValue:
    def __set_name__(self, owner: type[object], name: str) -> None:
        self.name = name
        self.storage_name = f"_data_{name}"

    def __get__(self, instance: object | None, owner: type[object] | None = None) -> object:
        if instance is None:
            return self
        return getattr(instance, self.storage_name, "data-default")

    def __set__(self, instance: object, value: object) -> None:
        setattr(instance, self.storage_name, value)

    def __delete__(self, instance: object) -> None:
        delattr(instance, self.storage_name)


class NonDataValue:
    def __set_name__(self, owner: type[object], name: str) -> None:
        self.name = name

    def __get__(self, instance: object | None, owner: type[object] | None = None) -> object:
        if instance is None:
            return self
        return "non-data-default"


class Sample:
    data = DataValue()
    cached = NonDataValue()

    def method(self) -> str:
        return "bound-result"


def observe_lookup() -> list[LookupObservation]:
    sample = Sample()
    sample.__dict__["data"] = "instance-data-shadow-attempt"
    sample.__dict__["cached"] = "instance-cached"

    bound = sample.method
    raw_method = vars(Sample)["method"]
    raw_data = vars(Sample)["data"]
    raw_non_data = vars(Sample)["cached"]

    observations = [
        LookupObservation("sample.data", str(sample.data)),
        LookupObservation("sample.__dict__['data']", str(sample.__dict__["data"])),
        LookupObservation("sample.cached", str(sample.cached)),
        LookupObservation("Sample.data is raw_data", str(Sample.data is raw_data)),
        LookupObservation("Sample.cached is raw_non_data", str(Sample.cached is raw_non_data)),
        LookupObservation(
            "bound.__self__ is sample",
            str(bound.__self__ is sample),  # type: ignore[attr-defined]
        ),
        LookupObservation(
            "bound.__func__ is raw_method",
            str(bound.__func__ is raw_method),  # type: ignore[attr-defined]
        ),
        LookupObservation("bound()", bound()),
    ]
    sample.data = "assigned-through-data-descriptor"
    observations.append(LookupObservation("sample.data after assignment", str(sample.data)))
    del sample.data
    observations.append(LookupObservation("sample.data after deletion", str(sample.data)))
    return observations


def main() -> None:
    for observation in observe_lookup():
        print(f"{observation.expression} -> {observation.result}")


if __name__ == "__main__":
    main()
