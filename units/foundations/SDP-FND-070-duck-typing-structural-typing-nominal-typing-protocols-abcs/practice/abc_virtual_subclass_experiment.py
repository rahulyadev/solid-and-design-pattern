"""Observe direct, registered, and unverified ABC relationships."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, cast


class SendsTextABC(ABC):
    """Define a nominal contract and one inherited convenience method."""

    @abstractmethod
    def send(self, message: str) -> str:
        """Send text and return a provider reference."""

    def boundary_label(self) -> str:
        return "sends-text"


class NominalSender(SendsTextABC):
    def send(self, message: str) -> str:
        return f"nominal:{len(message)}"


class RegisteredSender:
    def send(self, message: str) -> str:
        return f"registered:{len(message)}"


class RegisteredButIncomplete:
    pass


SendsTextABC.register(RegisteredSender)
SendsTextABC.register(RegisteredButIncomplete)


def main() -> None:
    """Print only language-level recognition and inheritance observations."""

    nominal = NominalSender()
    registered = RegisteredSender()
    incomplete = RegisteredButIncomplete()

    print(f"nominal_isinstance={isinstance(nominal, SendsTextABC)}")
    print(f"nominal_in_mro={SendsTextABC in NominalSender.__mro__}")
    print(f"nominal_default={nominal.boundary_label()}")
    print(f"registered_isinstance={isinstance(registered, SendsTextABC)}")
    print(f"registered_in_mro={SendsTextABC in RegisteredSender.__mro__}")
    print(f"registered_has_default={hasattr(registered, 'boundary_label')}")
    print(f"registered_call={registered.send('alert')}")
    print(f"incomplete_isinstance={isinstance(incomplete, SendsTextABC)}")
    try:
        cast(Any, incomplete).send("alert")
    except AttributeError:
        print("incomplete_actual_call=AttributeError")


if __name__ == "__main__":
    main()
