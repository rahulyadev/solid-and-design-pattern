"""Observe what plain Mock, autospec, and a test-double role actually guarantee."""

from __future__ import annotations

from typing import cast
from unittest.mock import Mock, create_autospec


class PaymentPort:
    """A concrete signature used only as an autospec source for this experiment."""

    def charge(self, *, account_id: str, amount_cents: int) -> str:
        raise NotImplementedError


def observe_mock_strictness() -> dict[str, bool | str | int]:
    """Return stable observations without claiming that a spec proves semantics."""

    loose = Mock()
    loose.chagre(account="acct-1", cents=500)

    strict = create_autospec(PaymentPort, instance=True, spec_set=True)
    strict_rejected_typo = False
    try:
        strict.chagre(account="acct-1", cents=500)
    except AttributeError:
        strict_rejected_typo = True

    strict_rejected_wrong_signature = False
    try:
        strict.charge("acct-1", 500)
    except TypeError:
        strict_rejected_wrong_signature = True

    strict.charge.return_value = "pay-42"
    provider_reference = cast(str, strict.charge(account_id="acct-1", amount_cents=500))

    return {
        "loose_created_typo_attribute": loose.chagre.called,
        "strict_rejected_typo": strict_rejected_typo,
        "strict_rejected_wrong_signature": strict_rejected_wrong_signature,
        "stubbed_value": provider_reference,
        "recorded_valid_calls": strict.charge.call_count,
    }


def main() -> None:
    for name, result in observe_mock_strictness().items():
        print(f"{name}={result}")


if __name__ == "__main__":
    main()
