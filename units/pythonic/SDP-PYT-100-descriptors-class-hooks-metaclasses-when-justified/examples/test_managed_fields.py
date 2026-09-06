"""Behavior tests for the descriptor that is actually justified."""

from __future__ import annotations

import pytest
from managed_fields import (
    FieldValidationError,
    HealthCheck,
    ManagedField,
    ServiceEndpoint,
    trimmed_text,
)


def test_descriptor_converts_and_stores_per_instance_values() -> None:
    first = ServiceEndpoint(" catalog ", 8080)
    second = ServiceEndpoint("billing", 9090)

    assert first.authority() == "catalog:8080"
    assert second.authority() == "billing:9090"
    assert vars(first) == {"_managed_name": "catalog", "_managed_port": 8080}


def test_class_access_returns_descriptor_for_introspection() -> None:
    descriptor = ServiceEndpoint.name

    assert isinstance(descriptor, ManagedField)
    assert descriptor.public_name == "name"
    assert descriptor.storage_name == "_managed_name"
    assert vars(ServiceEndpoint)["name"] is descriptor


@pytest.mark.parametrize("raw_name", ["", "   ", 42])
def test_invalid_names_are_rejected(raw_name: object) -> None:
    with pytest.raises(FieldValidationError, match="invalid name"):
        ServiceEndpoint(raw_name, 8080)  # type: ignore[arg-type]


@pytest.mark.parametrize("raw_port", [0, 65_536, True, "8080"])
def test_invalid_ports_are_rejected(raw_port: object) -> None:
    with pytest.raises(FieldValidationError, match="invalid port"):
        ServiceEndpoint("catalog", raw_port)  # type: ignore[arg-type]


def test_assignment_and_deletion_use_the_data_descriptor() -> None:
    endpoint = ServiceEndpoint("catalog", 8080)

    endpoint.port = 8443
    assert endpoint.port == 8443

    del endpoint.port
    with pytest.raises(AttributeError, match="port has not been assigned"):
        _ = endpoint.port


def test_deleting_an_unassigned_field_has_a_clear_error() -> None:
    endpoint = object.__new__(ServiceEndpoint)

    with pytest.raises(AttributeError, match="name has not been assigned"):
        del endpoint.name


def test_a_second_owner_reuses_semantics_without_sharing_values() -> None:
    check = HealthCheck(" /ready ", 30)

    assert check.path == "/ready"
    assert check.interval_seconds == 30
    assert HealthCheck.path.public_name == "path"


def test_one_descriptor_object_cannot_be_rebound_to_a_different_name() -> None:
    shared = ManagedField(trimmed_text)

    with pytest.raises(RuntimeError, match="Error calling __set_name__"):

        class InvalidOwner:
            first = shared
            second = shared


def test_late_attachment_requires_explicit_set_name() -> None:
    field = ManagedField(trimmed_text)

    class LateOwner:
        pass

    LateOwner.name = field  # type: ignore[attr-defined]
    instance = LateOwner()

    with pytest.raises(RuntimeError, match="not attached"):
        field.__set__(instance, "catalog")

    field.__set_name__(LateOwner, "name")
    field.__set__(instance, " catalog ")
    assert field.__get__(instance, LateOwner) == "catalog"


def test_original_conversion_exception_is_chained() -> None:
    with pytest.raises(FieldValidationError) as caught:
        ServiceEndpoint("catalog", "wrong")  # type: ignore[arg-type]

    assert isinstance(caught.value.__cause__, TypeError)
