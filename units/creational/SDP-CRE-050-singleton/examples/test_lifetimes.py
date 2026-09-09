from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

import pytest
from lifetimes import LazyValue, MemoryReader, ReportService, application


def test_one_owner_shares_reader_then_closes() -> None:
    reader = MemoryReader({"cover": "green"}, revision="r1")
    with application(lambda: reader) as app:
        assert app.preview.reader is app.export.reader is reader
        assert app.preview.render("cover") == "report:green"
        assert not reader.closed
    assert reader.closed
    with pytest.raises(RuntimeError, match="closed"):
        app.export.render("cover")


def test_independent_apps_in_one_interpreter() -> None:
    a = MemoryReader({"cover": "green"}, revision="r1")
    b = MemoryReader({"cover": "ochre"}, revision="r2")
    with application(lambda: a) as left, application(lambda: b) as right:
        assert left.preview.render("cover") == "report:green"
        assert right.preview.render("cover") == "report:ochre"
        assert left.preview.reader is not right.preview.reader
    assert a.closed and b.closed


def test_body_failure_still_closes() -> None:
    reader = MemoryReader({}, revision="r1")
    with pytest.raises(KeyError), application(lambda: reader) as app:
        app.preview.render("missing")
    assert reader.closed


def test_acquisition_failure_publishes_nothing() -> None:
    published = False

    def fail() -> MemoryReader:
        raise OSError("synthetic acquisition failure")

    with pytest.raises(OSError, match="acquisition failure"), application(fail):
        published = True
    assert not published


def test_snapshot_isolated_from_input_mutation() -> None:
    entries = {"cover": "green"}
    reader = MemoryReader(entries, revision="r1")
    entries["cover"] = "red"
    assert reader.lookup("cover") == "green"


@pytest.mark.parametrize("revision", ["", " ", "\n"])
def test_revision_required(revision: str) -> None:
    with pytest.raises(ValueError, match="revision"):
        MemoryReader({}, revision=revision)


def test_consumer_needs_read_capability_only() -> None:
    class FixedReader:
        def lookup(self, key: str) -> str:
            return "synthetic"

    assert ReportService(FixedReader()).render("anything") == "report:synthetic"


def test_close_failure_retains_original_context() -> None:
    class BrokenClose(MemoryReader):
        def close(self) -> None:
            super().close()
            raise OSError("close failed")

    reader = BrokenClose({}, revision="r1")
    with (
        pytest.raises(OSError, match="close failed") as caught,
        application(lambda: reader) as app,
    ):
        app.preview.render("missing")
    assert isinstance(caught.value.__context__, KeyError)
    assert reader.closed


def test_lazy_retries_after_failure_then_reuses() -> None:
    attempts = 0
    value = object()

    def build() -> object:
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            raise ValueError("temporary")
        return value

    lazy = LazyValue(build)
    with pytest.raises(ValueError, match="temporary"):
        lazy.get()
    assert lazy.get() is value
    assert lazy.get() is value
    assert attempts == 2


def test_lazy_caches_none() -> None:
    calls = 0

    def build() -> None:
        nonlocal calls
        calls += 1

    lazy = LazyValue(build)
    assert lazy.get() is None
    assert lazy.get() is None
    assert calls == 1


def test_recursive_factory_is_rejected_without_poisoning_provider() -> None:
    recursive = True

    def build() -> str:
        if recursive:
            return lazy.get()
        return "ready"

    lazy = LazyValue(build)
    with pytest.raises(RuntimeError, match="recursive"):
        lazy.get()
    recursive = False
    assert lazy.get() == "ready"


def test_base_exception_does_not_leave_building_flag_set() -> None:
    attempts = 0

    def build() -> str:
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            raise KeyboardInterrupt
        return "ready"

    lazy = LazyValue(build)
    with pytest.raises(KeyboardInterrupt):
        lazy.get()
    assert lazy.get() == "ready"


def test_simultaneous_callers_receive_same_published_value() -> None:
    barrier = Barrier(4, timeout=5)
    calls = 0

    def build() -> object:
        nonlocal calls
        calls += 1
        return object()

    lazy = LazyValue(build)

    def use() -> object:
        barrier.wait()
        return lazy.get()

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(use) for _ in range(4)]
        values = [future.result(timeout=10) for future in futures]
    assert calls == 1
    assert all(value is values[0] for value in values)


def test_distinct_providers_have_distinct_values() -> None:
    assert LazyValue(object).get() is not LazyValue(object).get()


def test_factory_and_close_counts_belong_to_one_root() -> None:
    events: list[str] = []

    class TracedReader(MemoryReader):
        def close(self) -> None:
            events.append("close")
            super().close()

    def acquire() -> TracedReader:
        events.append("acquire")
        return TracedReader({"cover": "green"}, revision="r1")

    with application(acquire) as app:
        for _ in range(3):
            assert app.preview.render("cover") == app.export.render("cover")
        assert events == ["acquire"]
    assert events == ["acquire", "close"]


def test_unused_provider_does_not_build() -> None:
    def forbidden() -> object:
        raise AssertionError("unused provider invoked its factory")

    LazyValue(forbidden)


def test_repeated_failures_do_not_become_cached_success() -> None:
    attempts = 0

    def fail() -> object:
        nonlocal attempts
        attempts += 1
        raise OSError("unavailable")

    provider = LazyValue(fail)
    for _ in range(3):
        with pytest.raises(OSError, match="unavailable"):
            provider.get()
    assert attempts == 3


def test_concurrent_callers_can_retry_after_failure() -> None:
    rendezvous = Barrier(2, timeout=5)
    attempts = 0

    def build() -> str:
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            raise OSError("first attempt failed")
        return "ready"

    provider = LazyValue(build)

    def call() -> str:
        rendezvous.wait()
        try:
            return provider.get()
        except OSError:
            return "failed"

    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(call) for _ in range(2)]
        results = [future.result(timeout=10) for future in futures]
    assert sorted(results) == ["failed", "ready"]
    assert provider.get() == "ready"
    assert attempts == 2
