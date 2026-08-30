import pytest
from protocol_probe import GoodMaker, IgnoresTitle, StaticMaker, WrongSignature, membership, observe


@pytest.mark.parametrize(
    ("candidate", "expected"),
    [
        (GoodMaker(), (True, "contract kept")),
        (WrongSignature(), (True, "TypeError")),
        (IgnoresTitle(), (True, "contract broken")),
        (object(), (False, "missing member")),
    ],
)
def test_runtime_membership_and_call_are_different_checks(
    candidate: object, expected: tuple[bool, str]
) -> None:
    assert observe(candidate) == expected


def test_ordinary_protocol_does_not_opt_in_to_runtime_membership() -> None:
    with pytest.raises(TypeError):
        membership(GoodMaker(), StaticMaker)
