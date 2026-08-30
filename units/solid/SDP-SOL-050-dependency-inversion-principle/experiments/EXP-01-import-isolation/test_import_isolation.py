"""An executable boundary regression, independent of the parent's module cache."""

from import_isolation import run_probe


def test_policy_can_import_and_execute_without_the_database_driver() -> None:
    concrete, inverted = run_probe()
    assert concrete == "concrete: import blocked (sqlite3)"
    assert inverted.splitlines() == [
        "runtime: policy -> fake.units_available(BOLT)",
        "inverted: {'BOLT': 5}",
    ]
