import pytest
from quote_lab import Parcel, basic_quote, build_quote, client_quote


def test_current_baseline() -> None:
    parcel = Parcel(150)
    assert basic_quote(parcel) == 400
    assert client_quote(parcel, discount=False, minimum=False) == 400
    assert client_quote(parcel, discount=True, minimum=True) == 500


@pytest.mark.parametrize("mass", [0, -1])
def test_invalid_parcel(mass: int) -> None:
    with pytest.raises(ValueError, match="positive"):
        Parcel(mass)


def test_exercise_starts_unsolved() -> None:
    with pytest.raises(NotImplementedError, match="unsolved"):
        build_quote()
