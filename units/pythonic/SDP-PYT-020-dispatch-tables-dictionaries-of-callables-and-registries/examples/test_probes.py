"""Checks for the two documented maintainer experiments."""

from exception_boundary_probe import observations as exception_observations
from registry_lifecycle_probe import observations as lifecycle_observations


def test_exception_boundary_observations() -> None:
    assert exception_observations() == {
        "broad": "UnknownEventType: unsupported event type: record.broken",
        "controlled": "KeyError: 'payload.customer_id'; same=True",
    }


def test_registry_lifecycle_observations() -> None:
    assert lifecycle_observations() == {
        "names": ["record.created", "record.custom"],
        "mapping_write": "TypeError",
        "post_seal_registration": "RegistrySealed: registry is sealed",
        "callable_before": "probe:first:R-5",
        "callable_after": "probe:second:R-5",
    }
