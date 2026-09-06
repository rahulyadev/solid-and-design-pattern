"""Prove lookup precedence and method binding with maintained observations."""

from __future__ import annotations

from lookup_probe import DataValue, NonDataValue, Sample, observe_lookup


def test_data_descriptor_beats_same_named_instance_entry() -> None:
    sample = Sample()
    sample.__dict__["data"] = "shadow-attempt"

    assert sample.data == "data-default"
    assert sample.__dict__["data"] == "shadow-attempt"


def test_instance_entry_beats_non_data_descriptor() -> None:
    sample = Sample()
    sample.__dict__["cached"] = "cached-result"

    assert sample.cached == "cached-result"


def test_class_access_passes_no_instance_and_returns_descriptor() -> None:
    assert isinstance(Sample.data, DataValue)
    assert isinstance(Sample.cached, NonDataValue)
    assert Sample.data is vars(Sample)["data"]
    assert Sample.cached is vars(Sample)["cached"]


def test_function_is_a_non_data_descriptor_that_binds_an_instance() -> None:
    sample = Sample()
    bound = sample.method

    assert bound.__self__ is sample
    assert bound.__func__ is vars(Sample)["method"]
    assert bound() == "bound-result"


def test_instance_dictionary_can_shadow_a_method() -> None:
    sample = Sample()
    sample.__dict__["method"] = lambda: "shadowed"

    assert sample.method() == "shadowed"


def test_probe_observations_remain_exact() -> None:
    assert [(item.expression, item.result) for item in observe_lookup()] == [
        ("sample.data", "data-default"),
        ("sample.__dict__['data']", "instance-data-shadow-attempt"),
        ("sample.cached", "instance-cached"),
        ("Sample.data is raw_data", "True"),
        ("Sample.cached is raw_non_data", "True"),
        ("bound.__self__ is sample", "True"),
        ("bound.__func__ is raw_method", "True"),
        ("bound()", "bound-result"),
        ("sample.data after assignment", "assigned-through-data-descriptor"),
        ("sample.data after deletion", "data-default"),
    ]
