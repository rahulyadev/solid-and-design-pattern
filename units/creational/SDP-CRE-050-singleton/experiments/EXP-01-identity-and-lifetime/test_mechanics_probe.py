from mechanics_probe import observe_mechanics


def test_construction_and_pickle_mechanics_in_fresh_interpreter() -> None:
    assert observe_mechanics() == {
        "child_is_base": True,
        "child_has_child_type": False,
        "child_init_ran": False,
        "failed_object_still_cached": True,
        "partial_state_reachable": True,
        "pickle_preserved_identity": True,
        "live_revision_after_restore": "r1",
        "mutable_init_calls": 1,
    }
