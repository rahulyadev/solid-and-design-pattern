"""Contract tests for the two required runtime probes."""

from context_lifecycle_probe import context_observations
from iterator_lifecycle_probe import iterator_observations


def test_iterator_probe_records_laziness_identity_and_exhaustion() -> None:
    observations = iterator_observations()

    assert observations == {
        "before_first_next": (),
        "first_id": "a-1",
        "after_first_next": ("read:a-1|2|queued",),
        "remaining_ids": ("a-2",),
        "after_exhaustion": (
            "read:a-1|2|queued",
            "read:a-2|5|worker unavailable",
        ),
        "generator_iter_is_self": True,
        "second_pass": (),
        "next_after_exhaustion": "StopIteration",
        "container_iterators_are_distinct": True,
        "container_passes": ((10, 20), (10, 20)),
    }


def test_context_probe_records_all_four_exit_paths() -> None:
    observations = context_observations()

    assert observations == {
        "normal": {
            "trace": ("acquire", "body", "commit", "close"),
            "closed": True,
        },
        "body_failure": {
            "trace": ("acquire", "body", "abort:RuntimeError", "close"),
            "closed": True,
            "same_exception_propagated": True,
        },
        "selective_suppression": ("enter", "body", "exit:KeyError", "continued"),
        "entry_failure": ("enter", "caught"),
    }
