"""Observe how cooperative super() follows the runtime method resolution order."""

from __future__ import annotations


class TerminalHandler:
    """Terminate the cooperative handling chain."""

    def handle(self, trace: list[str]) -> None:
        trace.append("TerminalHandler")


class RetryLayer(TerminalHandler):
    """Record a synthetic retry layer around the next MRO participant."""

    def handle(self, trace: list[str]) -> None:
        trace.append("RetryLayer.before")
        super().handle(trace)
        trace.append("RetryLayer.after")


class AuditLayer(TerminalHandler):
    """Record a synthetic audit layer around the next MRO participant."""

    def handle(self, trace: list[str]) -> None:
        trace.append("AuditLayer.before")
        super().handle(trace)
        trace.append("AuditLayer.after")


class CombinedHandler(AuditLayer, RetryLayer):
    """Combine two cooperative layers in an explicit base-class order."""


def main() -> None:
    """Print the linearized search order and resulting call trace."""

    trace: list[str] = []
    CombinedHandler().handle(trace)

    print("mro=" + " -> ".join(cls.__name__ for cls in CombinedHandler.__mro__))
    print("trace=" + " -> ".join(trace))


if __name__ == "__main__":
    main()
