"""Controlled single-dispatch rendering for a synthetic audit boundary.

The generic function owns type-based selection.  The wrapper owns result checks
and observability.  Registrations are deliberately fixed during module import.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from functools import singledispatch


class UnsupportedPayloadError(TypeError):
    """Raised when no supported rendering exists for a runtime type."""


class InvalidPayloadError(ValueError):
    """Raised when a broad runtime type contains invalid application data."""


@dataclass(frozen=True, slots=True)
class RenderContext:
    request_id: str
    audience: str

    def __post_init__(self) -> None:
        for field_name, value in (("request_id", self.request_id), ("audience", self.audience)):
            if not value or value != value.strip():
                raise ValueError(f"{field_name} must be non-empty and trimmed")


@dataclass(frozen=True, slots=True)
class RenderedPayload:
    request_id: str
    media_type: str
    body: str

    def __post_init__(self) -> None:
        if not self.request_id or self.request_id != self.request_id.strip():
            raise ValueError("request_id must be non-empty and trimmed")
        if not self.media_type or self.media_type != self.media_type.strip():
            raise ValueError("media_type must be non-empty and trimmed")
        if not self.body:
            raise ValueError("body must be non-empty")


@dataclass(frozen=True, slots=True)
class AuditEvent:
    event_id: str
    actor: str

    def __post_init__(self) -> None:
        for field_name, value in (("event_id", self.event_id), ("actor", self.actor)):
            if not value or value != value.strip():
                raise ValueError(f"{field_name} must be non-empty and trimmed")


@dataclass(frozen=True, slots=True)
class UserRegistered(AuditEvent):
    email_domain: str

    def __post_init__(self) -> None:
        super(UserRegistered, self).__post_init__()
        if not self.email_domain or self.email_domain != self.email_domain.strip():
            raise ValueError("email_domain must be non-empty and trimmed")


@dataclass(frozen=True, slots=True)
class PrivilegedUserRegistered(UserRegistered):
    role: str

    def __post_init__(self) -> None:
        super(PrivilegedUserRegistered, self).__post_init__()
        if not self.role or self.role != self.role.strip():
            raise ValueError("role must be non-empty and trimmed")


@dataclass(frozen=True, slots=True)
class HealthSnapshot:
    service: str
    healthy: bool

    def __post_init__(self) -> None:
        if not self.service or self.service != self.service.strip():
            raise ValueError("service must be non-empty and trimmed")


@dataclass(frozen=True, slots=True)
class DispatchObservation:
    runtime_type: str
    selected_handler: str
    outcome: str


ObservationSink = Callable[[DispatchObservation], None]


@singledispatch
def render_payload(value: object, *, context: RenderContext) -> RenderedPayload:
    """Render one value, failing closed when no better registration exists."""

    del context
    runtime_type = type(value)
    raise UnsupportedPayloadError(
        f"no renderer registered for {runtime_type.__module__}.{runtime_type.__qualname__}"
    )


@render_payload.register
def render_audit_event(value: AuditEvent, *, context: RenderContext) -> RenderedPayload:
    return RenderedPayload(
        request_id=context.request_id,
        media_type="text/plain",
        body=f"event={value.event_id};actor={value.actor};audience={context.audience}",
    )


@render_payload.register
def render_user_registered(value: UserRegistered, *, context: RenderContext) -> RenderedPayload:
    return RenderedPayload(
        request_id=context.request_id,
        media_type="text/plain",
        body=(
            f"event={value.event_id};actor={value.actor};domain={value.email_domain};"
            f"audience={context.audience}"
        ),
    )


@render_payload.register
def render_text(value: str | bytes, *, context: RenderContext) -> RenderedPayload:
    text = value.decode("utf-8") if isinstance(value, bytes) else value
    if not text:
        raise InvalidPayloadError("text payload must be non-empty")
    return RenderedPayload(context.request_id, "text/plain", text)


@render_payload.register(list)
def render_event_batch(value: list[AuditEvent], *, context: RenderContext) -> RenderedPayload:
    if not value:
        raise InvalidPayloadError("event batch must be non-empty")
    if not all(isinstance(item, AuditEvent) for item in value):
        raise InvalidPayloadError("event batch must contain only AuditEvent values")
    event_ids = ",".join(item.event_id for item in value)
    return RenderedPayload(context.request_id, "text/plain", f"events={event_ids}")


@render_payload.register(Mapping)
def render_mapping(value: Mapping[str, object], *, context: RenderContext) -> RenderedPayload:
    pairs = ",".join(f"{key}={value[key]!r}" for key in sorted(value))
    return RenderedPayload(context.request_id, "text/plain", pairs or "<empty mapping>")


def render_health_snapshot(value: HealthSnapshot, *, context: RenderContext) -> RenderedPayload:
    state = "healthy" if value.healthy else "unhealthy"
    return RenderedPayload(
        context.request_id,
        "text/plain",
        f"service={value.service};state={state};audience={context.audience}",
    )


# Functional registration is useful for a pre-existing named function.
render_payload.register(HealthSnapshot, render_health_snapshot)


def selected_handler_name(value_type: type[object]) -> str:
    """Return the documented dispatch choice without invoking a handler."""

    implementation = render_payload.dispatch(value_type)
    return implementation.__name__


def render_observed(
    value: object,
    *,
    context: RenderContext,
    observe: ObservationSink,
) -> RenderedPayload:
    """Render while exposing selection and outcome at the application boundary."""

    implementation = render_payload.dispatch(type(value))
    selected_handler = implementation.__name__
    runtime_type = type(value).__qualname__
    try:
        result = render_payload(value, context=context)
    except Exception as error:
        observe(
            DispatchObservation(
                runtime_type=runtime_type,
                selected_handler=selected_handler,
                outcome=f"error:{type(error).__name__}",
            )
        )
        raise

    if result.request_id != context.request_id:
        observe(
            DispatchObservation(
                runtime_type=runtime_type,
                selected_handler=selected_handler,
                outcome="error:request-id-mismatch",
            )
        )
        raise RuntimeError("renderer returned a result for another request")

    observe(DispatchObservation(runtime_type, selected_handler, "ok"))
    return result
