from collections.abc import Sized
from inspect import signature, unwrap
from typing import cast

import pytest
from function_wrappers import order_probe, traced


def test_evaluation_application_and_call_are_different_phases() -> None:
    assert order_probe() == (
        "evaluate:outer",
        "evaluate:inner",
        "apply:inner",
        "apply:outer",
        "enter:outer",
        "enter:inner",
        "body",
        "exit:inner",
        "exit:outer",
    )


def test_typed_wrapper_forwards_positional_and_keyword_arguments() -> None:
    def format_text(text: str, /, *, prefix: str = "") -> str:
        """Describe a notice."""
        return prefix + text

    events: list[str] = []
    wrapped = traced(events, "text")(format_text)
    assert wrapped("ready", prefix="note: ") == "note: ready"
    assert wrapped.__name__ == format_text.__name__
    assert wrapped.__doc__ == format_text.__doc__
    assert unwrap(wrapped) is format_text
    assert signature(wrapped) == signature(format_text)
    assert tuple(signature(wrapped, follow_wrapped=False).parameters) == ("args", "kwargs")
    assert wrapped is not format_text


def test_finally_trace_does_not_claim_success() -> None:
    events: list[str] = []
    failure = ValueError("bad source")

    @traced(events, "text")
    def broken() -> str:
        raise failure

    with pytest.raises(ValueError) as caught:
        broken()
    assert caught.value is failure
    assert events[-2:] == ["enter:text", "exit:text"]


def test_class_decorator_can_return_same_class_without_instance_wrapper() -> None:
    registry: list[type[object]] = []

    def register(cls: type[object]) -> type[object]:
        registry.append(cls)
        return cls

    @register
    class Notice:
        pass

    assert registry == [Notice]
    assert type(Notice()) is Notice


def test_getattr_does_not_supply_implicit_len() -> None:
    class Forward:
        def __getattr__(self, name: str) -> object:
            return getattr([1, 2], name)

    wrapper = Forward()
    assert callable(wrapper.__getattr__("__len__"))
    # Deliberate invalid static assumption: cast does not add a runtime special method.
    with pytest.raises(TypeError):
        len(cast(Sized, wrapper))
