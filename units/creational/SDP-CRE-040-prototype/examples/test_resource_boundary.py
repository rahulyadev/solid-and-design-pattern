from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass

import pytest
from prototype import CompiledRules, GraphNode, QueryDraft
from resource_boundary import Session, materialize


@dataclass
class FakeSession:
    name: str

    def run(self) -> str:
        return self.name


@pytest.mark.parametrize("fail_at", [None, "first", "second", "body"])
def test_resource_ownership_and_partial_cleanup(fail_at: str | None) -> None:
    events: list[str] = []

    @contextmanager
    def acquire(name: str) -> Iterator[Session]:
        events.append("open:" + name)
        if name == fail_at:
            raise RuntimeError("acquisition_failed")
        try:
            yield FakeSession(name)
        finally:
            events.append("close:" + name)

    draft = QueryDraft(
        request_id="a",
        rules=CompiledRules(revision=1, operations=("first", "second")),
        root=GraphNode("query"),
    )

    def use() -> None:
        with materialize(draft, acquire) as sessions:
            assert tuple(session.run() for session in sessions) == ("first", "second")
            if fail_at == "body":
                raise RuntimeError("body_failed")

    if fail_at is None:
        use()
    else:
        with pytest.raises(RuntimeError):
            use()
    expected = {
        None: ["open:first", "open:second", "close:second", "close:first"],
        "first": ["open:first"],
        "second": ["open:first", "open:second", "close:first"],
        "body": ["open:first", "open:second", "close:second", "close:first"],
    }
    assert events == expected[fail_at]
