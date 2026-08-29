"""Contrast actual calls with runtime-checkable Protocol presence checks."""

from __future__ import annotations

from typing import Any, Protocol, cast, runtime_checkable


@runtime_checkable
class SendsText(Protocol):
    """Describe a statically typed operation and opt into a shallow runtime check."""

    def send(self, message: str) -> str:
        """Send text and return a provider reference."""


class CompatibleSender:
    def send(self, message: str) -> str:
        return f"ok:{len(message)}"


class WrongSignatureSender:
    def send(self) -> int:
        return 7


class DynamicSender:
    def __getattr__(self, name: str) -> object:
        if name == "send":
            return lambda message: f"dynamic:{len(message)}"
        raise AttributeError(name)


def main() -> None:
    """Print observations without treating recognition as a contract proof."""

    compatible = CompatibleSender()
    wrong = WrongSignatureSender()
    dynamic = DynamicSender()

    print(f"compatible_call={compatible.send('alert')}")
    print(f"compatible_runtime_protocol={isinstance(compatible, SendsText)}")
    print(f"wrong_runtime_protocol={isinstance(wrong, SendsText)}")
    try:
        cast(Any, wrong).send("alert")
    except TypeError:
        print("wrong_actual_call=TypeError")

    print(f"dynamic_hasattr={hasattr(dynamic, 'send')}")
    print(f"dynamic_call={cast(Any, dynamic).send('alert')}")
    print(f"dynamic_runtime_protocol={isinstance(dynamic, SendsText)}")


if __name__ == "__main__":
    main()
