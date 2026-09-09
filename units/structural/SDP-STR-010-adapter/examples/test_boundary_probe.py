from boundary_probe import observations


def test_controlled_observations() -> None:
    assert observations() == {
        "converted_units": 12,
        "converted_decision": "enough",
        "signature_only_decision": "short",
        "runtime_shape_accepts_wrong_signature": True,
        "actual_call_raises_type_error": True,
    }
