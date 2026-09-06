from runtime_probe import observe_runtime_protocol


def test_runtime_protocol_recognizes_presence_but_not_signature() -> None:
    recognized, failure = observe_runtime_protocol()

    assert recognized is True
    assert failure == "TypeError"
