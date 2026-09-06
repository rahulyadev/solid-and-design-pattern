"""Behavior and public-mechanics tests for the worked example."""

from collections.abc import Mapping

import pytest
from open_rendering import (
    AuditEvent,
    DispatchObservation,
    HealthSnapshot,
    InvalidPayloadError,
    PrivilegedUserRegistered,
    RenderContext,
    UnsupportedPayloadError,
    UserRegistered,
    render_audit_event,
    render_health_snapshot,
    render_observed,
    render_payload,
    render_text,
    render_user_registered,
    selected_handler_name,
)


@pytest.fixture
def context() -> RenderContext:
    return RenderContext("req-7", "operations")


def test_base_implementation_fails_closed(context: RenderContext) -> None:
    with pytest.raises(UnsupportedPayloadError, match="tuple"):
        render_payload(("unknown",), context=context)


def test_exact_type_selects_specific_handler(context: RenderContext) -> None:
    event = UserRegistered("evt-1", "rahul", "example.test")

    result = render_payload(event, context=context)

    assert result.body == "event=evt-1;actor=rahul;domain=example.test;audience=operations"
    assert render_payload.dispatch(UserRegistered) is render_user_registered


def test_unregistered_subclass_uses_nearest_registered_base(context: RenderContext) -> None:
    event = PrivilegedUserRegistered("evt-2", "sam", "example.test", "admin")

    result = render_payload(event, context=context)

    assert "domain=example.test" in result.body
    assert "role=admin" not in result.body
    assert render_payload.dispatch(PrivilegedUserRegistered) is render_user_registered


def test_more_general_event_uses_event_handler(context: RenderContext) -> None:
    result = render_payload(AuditEvent("evt-3", "scheduler"), context=context)

    assert result.body == "event=evt-3;actor=scheduler;audience=operations"
    assert render_payload.dispatch(AuditEvent) is render_audit_event


@pytest.mark.parametrize(("value", "body"), [("ready", "ready"), (b"ready", "ready")])
def test_union_registration_installs_one_handler_for_both_types(
    value: str | bytes, body: str, context: RenderContext
) -> None:
    assert render_payload(value, context=context).body == body
    assert render_payload.dispatch(type(value)) is render_text


def test_secondary_arguments_do_not_change_selection() -> None:
    value = UserRegistered("evt-4", "lee", "example.test")

    first = render_payload(value, context=RenderContext("req-a", "ops"))
    second = render_payload(value, context=RenderContext("req-b", "security"))

    assert first.request_id == "req-a"
    assert second.request_id == "req-b"
    assert render_payload.dispatch(type(value)) is render_user_registered


def test_parameterized_list_annotation_does_not_filter_runtime_contents(
    context: RenderContext,
) -> None:
    with pytest.raises(InvalidPayloadError, match="only AuditEvent"):
        render_payload(["not an event"], context=context)


def test_list_handler_accepts_valid_events(context: RenderContext) -> None:
    result = render_payload(
        [AuditEvent("evt-5", "worker"), AuditEvent("evt-6", "worker")],
        context=context,
    )

    assert result.body == "events=evt-5,evt-6"


def test_mapping_abc_registration_handles_dict(context: RenderContext) -> None:
    result = render_payload({"count": 2, "state": "ready"}, context=context)

    assert result.body == "count=2,state='ready'"
    assert render_payload.dispatch(dict) is render_payload.registry[Mapping]


def test_functional_registration_and_direct_handler_test(context: RenderContext) -> None:
    snapshot = HealthSnapshot("catalog", True)

    direct = render_health_snapshot(snapshot, context=context)
    dispatched = render_payload(snapshot, context=context)

    assert direct == dispatched
    assert render_payload.dispatch(HealthSnapshot) is render_health_snapshot


def test_register_decorator_keeps_handler_separate_from_generic() -> None:
    assert render_user_registered is not render_payload
    assert render_text is not render_payload


def test_registry_is_public_read_only_mapping() -> None:
    assert render_payload.registry[object] is render_payload.__wrapped__  # type: ignore[attr-defined]
    assert object in render_payload.registry
    assert str in render_payload.registry
    assert bytes in render_payload.registry
    with pytest.raises(TypeError):
        render_payload.registry[str] = render_audit_event  # type: ignore[index]


def test_dispatch_name_can_be_observed_without_running_handler() -> None:
    assert selected_handler_name(PrivilegedUserRegistered) == "render_user_registered"
    assert selected_handler_name(tuple) == "render_payload"


def test_observation_reports_success(context: RenderContext) -> None:
    observations: list[DispatchObservation] = []

    result = render_observed("hello", context=context, observe=observations.append)

    assert result.body == "hello"
    assert observations == [DispatchObservation("str", "render_text", "ok")]


def test_observation_reports_selected_handler_on_failure(context: RenderContext) -> None:
    observations: list[DispatchObservation] = []

    with pytest.raises(UnsupportedPayloadError):
        render_observed(3.14, context=context, observe=observations.append)

    assert observations == [
        DispatchObservation("float", "render_payload", "error:UnsupportedPayloadError")
    ]
