from abc_probe import (
    DroppingBuffer,
    MemoryBuffer,
    MissingBuffer,
    creation_outcome,
    virtual_observation,
)


def test_incomplete_nominal_subclass_cannot_be_constructed() -> None:
    assert creation_outcome(MissingBuffer) == "blocked by TypeError"


def test_registration_does_not_supply_members_or_inherited_implementation() -> None:
    assert virtual_observation() == (True, False, False)


def test_overriding_abstract_method_does_not_prove_its_postcondition() -> None:
    buffer = DroppingBuffer()
    buffer.append(b"sample")
    assert buffer.records == []


def test_honest_implementation_preserves_duplicates_and_payload_values() -> None:
    buffer = MemoryBuffer()
    for payload in (b"", b"sample", b"sample"):
        buffer.append(payload)
    assert buffer.records == [b"", b"sample", b"sample"]
