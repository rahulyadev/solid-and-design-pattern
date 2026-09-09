"""Characterize only existing behavior; these do not certify the target redesign."""

from legend_lab import build_rows, target_complete


def test_starter_preserves_order_and_empty_text() -> None:
    rows = build_rows(("Check hinge", ""), "Inspection")
    assert [row.describe() for row in rows] == ["0: Check hinge [Inspection]", "1:  [Inspection]"]


def test_empty_batch() -> None:
    assert build_rows((), "Inspection") == []


def test_existing_rows_have_independent_mutable_legends() -> None:
    rows = build_rows(("A", "B"), "Inspection")
    rows[0].legend["label"] = "Changed"
    assert rows[1].describe() == "1: B [Inspection]"


def test_no_learner_solution_is_claimed() -> None:
    assert target_complete() is False
