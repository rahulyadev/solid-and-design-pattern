"""Class-hook examples kept separate from the descriptor implementation."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, ClassVar, TypeVar


@dataclass(frozen=True)
class DefinitionEvent:
    stage: str
    target: str
    detail: str


EVENTS: list[DefinitionEvent] = []


def _record(stage: str, target: str, detail: str) -> None:
    EVENTS.append(DefinitionEvent(stage, target, detail))


class CodedRule:
    """Validate metadata inherited by every future rule subclass."""

    code: ClassVar[str]

    def __init_subclass__(cls, /, *, code: str, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        normalized = code.strip().lower()
        if not normalized or normalized != code:
            raise TypeError("code must be non-empty, lowercase, and trimmed")
        cls.code = normalized
        _record("init_subclass", cls.__name__, f"code={normalized}")


class VersionedDefinition:
    """A cooperative sibling hook that consumes only its own keyword."""

    schema_version: ClassVar[int]

    def __init_subclass__(cls, /, *, schema_version: int, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        if schema_version < 1:
            raise TypeError("schema_version must be positive")
        cls.schema_version = schema_version
        _record("init_subclass", cls.__name__, f"schema_version={schema_version}")


class ShippingRule(
    CodedRule,
    VersionedDefinition,
    code="standard",
    schema_version=1,
):
    """Both base hooks run because each forwards unconsumed keywords."""

    def quote(self, item_count: int) -> int:
        return 500 + 25 * item_count


ClassT = TypeVar("ClassT", bound=type[Any])


def label_definition(label: str) -> Callable[[ClassT], ClassT]:
    """Mutate one class and return the identical class object."""

    def decorate(cls: ClassT) -> ClassT:
        cls.definition_label = label
        _record("decorator", cls.__name__, f"label={label}; identity=preserved")
        return cls

    return decorate


def replace_with_proxy(cls: type[Any]) -> type[Any]:
    """Deliberately show the identity cost of a replacing class decorator."""

    original = cls

    class Replacement(cls):  # type: ignore[misc]
        wrapped_class = original

    Replacement.__name__ = cls.__name__
    Replacement.__qualname__ = cls.__qualname__
    Replacement.__module__ = cls.__module__
    _record("decorator", cls.__name__, "identity=replaced")
    return Replacement


class RecordingNamespace(dict[str, Any]):
    """Reject duplicate public declarations during class-body execution."""

    def __setitem__(self, key: str, value: Any) -> None:
        if not key.startswith("__") and key in self:
            raise TypeError(f"duplicate class-body name: {key}")
        super().__setitem__(key, value)


class DefinitionMeta(type):
    """A diagnostic metaclass; ordinary applications should not need it."""

    @classmethod
    def __prepare__(
        mcls,
        name: str,
        bases: tuple[type[Any], ...],
        /,
        **kwargs: Any,
    ) -> RecordingNamespace:
        del mcls, bases, kwargs
        _record("prepare", name, "custom namespace")
        return RecordingNamespace()

    def __new__(
        mcls,
        name: str,
        bases: tuple[type[Any], ...],
        namespace: dict[str, Any],
        **kwargs: Any,
    ) -> DefinitionMeta:
        _record("meta_new_before", name, "class object absent")
        # Passing the complete namespace preserves CPython's optional __classcell__.
        created = super().__new__(mcls, name, bases, namespace, **kwargs)
        _record("meta_new_after", name, "class object created")
        return created

    def __init__(
        cls,
        name: str,
        bases: tuple[type[Any], ...],
        namespace: dict[str, Any],
        **kwargs: Any,
    ) -> None:
        super().__init__(name, bases, namespace, **kwargs)
        _record("meta_init", name, "created class initialized")

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        _record("meta_call", cls.__name__, "instance construction")
        return super().__call__(*args, **kwargs)


@label_definition("audited")
class AuditedJob(metaclass=DefinitionMeta):
    def __new__(cls, name: str) -> AuditedJob:
        _record("instance_new", cls.__name__, name)
        return super().__new__(cls)

    def __init__(self, name: str) -> None:
        _record("instance_init", type(self).__name__, name)
        self.name = name

    def describe(self) -> str:
        return f"{type(self).__name__}:{self.name}"
