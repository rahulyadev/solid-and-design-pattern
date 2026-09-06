"""A narrow static facade over the intentionally broad runtime generic."""

from __future__ import annotations

from collections.abc import Mapping

from open_rendering import (
    AuditEvent,
    HealthSnapshot,
    RenderContext,
    RenderedPayload,
    render_payload,
)

SupportedPayload = (
    AuditEvent | HealthSnapshot | str | bytes | list[AuditEvent] | Mapping[str, object]
)


def render_known(value: SupportedPayload, *, context: RenderContext) -> RenderedPayload:
    """Give callers a static allow-list while retaining runtime dispatch internally."""

    return render_payload(value, context=context)


def static_conformance_witness() -> RenderedPayload:
    context = RenderContext("req-typing", "test")
    return render_known(HealthSnapshot("catalog", True), context=context)
