"""Characterize the original contract without implementing the new partner."""

import pytest
from parcel_label_lab import DispatchNote, LocalLabelDesk, Parcel, prepare_dispatch


def test_synchronous_dispatch_returns_a_ready_label() -> None:
    desk = LocalLabelDesk()
    assert prepare_dispatch(Parcel("PK-7", "North", 250), desk) == DispatchNote(
        "PK-7", "LABEL PK-7 / North / 250g"
    )
    assert desk.daily_total() == 1


@pytest.mark.parametrize("grams", [0, -1, -200])
def test_bad_weight_fails_before_access(grams: int) -> None:
    desk = LocalLabelDesk(offline=True)
    with pytest.raises(ValueError, match="positive"):
        prepare_dispatch(Parcel("PK-7", "North", grams), desk)
    assert desk.issued == []


@pytest.mark.parametrize(
    "reference,destination", [("", "North"), ("  ", "North"), ("PK-7", ""), ("PK-7", "\t")]
)
def test_blank_fields_fail_before_access(reference: str, destination: str) -> None:
    desk = LocalLabelDesk(offline=True)
    with pytest.raises(ValueError, match="blank"):
        prepare_dispatch(Parcel(reference, destination, 1), desk)
    assert desk.issued == []


def test_failure_does_not_produce_a_dispatch_note_or_issue_a_label() -> None:
    desk = LocalLabelDesk(offline=True)
    with pytest.raises(RuntimeError, match=r"^label unavailable$") as caught:
        prepare_dispatch(Parcel("PK-7", "North", 250), desk)
    assert isinstance(caught.value.__cause__, ConnectionError)
    assert desk.issued == []


def test_unicode_and_smallest_weight_are_preserved() -> None:
    parcel = Parcel("पार्सल-1", "दक्षिण", 1)
    assert prepare_dispatch(parcel, LocalLabelDesk()).label == "LABEL पार्सल-1 / दक्षिण / 1g"
    assert parcel == Parcel("पार्सल-1", "दक्षिण", 1)


def test_baseline_repeated_requests_are_not_idempotent() -> None:
    desk = LocalLabelDesk()
    parcel = Parcel("PK-7", "North", 250)
    first = prepare_dispatch(parcel, desk)
    assert prepare_dispatch(parcel, desk) == first
    assert desk.daily_total() == 2


def test_invalid_request_does_not_change_existing_provider_state() -> None:
    desk = LocalLabelDesk()
    prepare_dispatch(Parcel("PK-7", "North", 250), desk)
    before = list(desk.issued)
    with pytest.raises(ValueError):
        prepare_dispatch(Parcel("PK-8", "South", 0), desk)
    assert desk.issued == before
