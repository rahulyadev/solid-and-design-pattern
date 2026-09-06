"""Test class-hook collaboration, decorator identity, and metaclass phases."""

from __future__ import annotations

import platform
from typing import Any

import pytest
from class_hooks import (
    EVENTS,
    AuditedJob,
    CodedRule,
    DefinitionMeta,
    ShippingRule,
    VersionedDefinition,
    label_definition,
    replace_with_proxy,
)


def test_cooperative_init_subclass_hooks_consume_and_forward_keywords() -> None:
    assert ShippingRule.code == "standard"
    assert ShippingRule.schema_version == 1
    shipping_events = [event for event in EVENTS if event.target == "ShippingRule"]
    assert [event.detail for event in shipping_events] == [
        "schema_version=1",
        "code=standard",
    ]


def test_cooperative_hook_order_follows_super_chain_not_base_list_guessing() -> None:
    before = len(EVENTS)

    class ExpressRule(
        CodedRule,
        VersionedDefinition,
        code="express",
        schema_version=2,
    ):
        pass

    created = EVENTS[before:]
    assert ExpressRule.code == "express"
    assert ExpressRule.schema_version == 2
    assert [event.detail for event in created] == [
        "schema_version=2",
        "code=express",
    ]


def test_reversing_cooperative_bases_changes_the_real_super_chain() -> None:
    before = len(EVENTS)

    class ReverseRule(
        VersionedDefinition,
        CodedRule,
        schema_version=3,
        code="reverse",
    ):
        pass

    assert ReverseRule.code == "reverse"
    assert ReverseRule.schema_version == 3
    assert [event.detail for event in EVENTS[before:]] == [
        "code=reverse",
        "schema_version=3",
    ]


def test_set_name_completes_before_the_parent_subclass_hook() -> None:
    order: list[str] = []

    class Named:
        def __set_name__(self, owner: type[object], name: str) -> None:
            order.append(f"set_name:{owner.__name__}.{name}")

    class Base:
        def __init_subclass__(cls) -> None:
            super().__init_subclass__()
            order.append(f"init_subclass:{cls.__name__}")

    class Child(Base):
        field = Named()

    assert order == ["set_name:Child.field", "init_subclass:Child"]


def test_invalid_hook_keyword_is_rejected_at_definition_time() -> None:
    with pytest.raises(TypeError, match="lowercase"):

        class InvalidRule(CodedRule, code=" Not-Valid "):
            pass


def test_unconsumed_keyword_reaches_object_and_fails() -> None:
    with pytest.raises(TypeError, match="takes no keyword arguments"):

        class InvalidRule(CodedRule, code="valid", unexpected=True):
            pass


def test_in_place_class_decorator_preserves_identity_and_inheritance() -> None:
    class Base:
        pass

    original = type("Concrete", (Base,), {})
    decorated = label_definition("stable")(original)

    assert decorated is original
    assert issubclass(decorated, Base)
    assert decorated.definition_label == "stable"


def test_class_decorators_apply_bottom_up() -> None:
    order: list[str] = []

    def record(label: str) -> Any:
        def decorate(cls: type[Any]) -> type[Any]:
            order.append(label)
            return cls

        return decorate

    @record("outer")
    @record("inner")
    class Decorated:
        pass

    assert order == ["inner", "outer"]
    assert Decorated.__name__ == "Decorated"


def test_class_decorator_is_not_reapplied_to_descendants() -> None:
    before = len(EVENTS)

    @label_definition("base")
    class DecoratedBase:
        pass

    after_base = len(EVENTS)

    class Child(DecoratedBase):
        pass

    assert after_base == before + 1
    assert len(EVENTS) == after_base
    assert Child.definition_label == "base"


def test_replacing_class_decorator_changes_identity_and_adds_an_mro_layer() -> None:
    original = type("Concrete", (), {})
    decorated = replace_with_proxy(original)

    assert decorated is not original
    assert issubclass(decorated, original)
    assert decorated.__mro__[:2] == (decorated, original)
    assert decorated.wrapped_class is original


def test_metaclass_phases_finish_before_class_decorator() -> None:
    audited_events = [event.stage for event in EVENTS if event.target == "AuditedJob"]

    assert audited_events == [
        "prepare",
        "meta_new_before",
        "meta_new_after",
        "meta_init",
        "decorator",
    ]
    assert AuditedJob.definition_label == "audited"


def test_metaclass_call_wraps_instance_new_and_init() -> None:
    before = len(EVENTS)
    job = AuditedJob("nightly")

    assert job.describe() == "AuditedJob:nightly"
    assert [event.stage for event in EVENTS[before:]] == [
        "meta_call",
        "instance_new",
        "instance_init",
    ]


def test_prepare_namespace_can_reject_duplicate_declarations() -> None:
    with pytest.raises(TypeError, match="duplicate class-body name: value"):

        class Invalid(metaclass=DefinitionMeta):
            value = 1
            value = 2


def test_ordinary_type_is_the_default_metaclass() -> None:
    class Ordinary:
        pass

    assert type(Ordinary) is type
    assert isinstance(Ordinary, type)


def test_incompatible_metaclasses_fail_during_selection() -> None:
    class FirstMeta(type):
        pass

    class SecondMeta(type):
        pass

    class First(metaclass=FirstMeta):
        pass

    class Second(metaclass=SecondMeta):
        pass

    with pytest.raises(TypeError, match="metaclass conflict"):

        class Conflict(First, Second):
            pass


@pytest.mark.skipif(
    platform.python_implementation() != "CPython",
    reason="__classcell__ propagation is documented as a CPython implementation detail",
)
def test_dropping_classcell_breaks_zero_argument_super_on_cpython() -> None:
    class DropsClassCell(type):
        def __new__(
            mcls,
            name: str,
            bases: tuple[type[Any], ...],
            namespace: dict[str, Any],
        ) -> type[Any]:
            namespace.pop("__classcell__", None)
            return super().__new__(mcls, name, bases, namespace)

    with pytest.raises(RuntimeError, match="__class__ not set"):

        class Broken(metaclass=DropsClassCell):
            def method(self) -> Any:
                return super()
