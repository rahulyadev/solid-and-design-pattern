import pytest
from failure_probe import observe
from report_contracts import (
    LoadError,
    PacketUnavailable,
    Receipt,
    RenderError,
    Snapshot,
    Stage,
    StoreError,
    WriteOutcome,
)
from report_facade import ReportFacade, build_packet
from report_subsystem import MemoryArchive, MemoryReports, TextRenderer


def make_facade(
    events: list[str], archive: MemoryArchive, *, fail_render: bool = False
) -> ReportFacade:
    return ReportFacade(
        MemoryReports({"WEEK-1": Snapshot(("open=3",))}, events),
        TextRenderer(events, fail=fail_render),
        archive,
    )


def test_success_order_receipt_and_content() -> None:
    events: list[str] = []
    archive = MemoryArchive(events)
    receipt = make_facade(events, archive).build("WEEK-1")
    assert receipt == Receipt("WEEK-1/1", 14)
    assert archive.read(receipt.key) == b"REPORT\nopen=3\n"
    assert events == ["load", "render", "store"]
    assert archive.close_count == 0


def test_injected_function_has_same_task_contract() -> None:
    events: list[str] = []
    archive = MemoryArchive(events)
    receipt = build_packet(
        "WEEK-1",
        reader=MemoryReports({"WEEK-1": Snapshot(())}, events),
        renderer=TextRenderer(events),
        archive=archive,
    )
    assert archive.read(receipt.key) == b"REPORT\n\n"
    assert receipt.byte_count == 8


@pytest.mark.parametrize("report_id", ["", "week", "A B", "A/B", "A\n", "É", "A" * 25])
def test_invalid_identifier_prevents_all_subsystem_calls(report_id: str) -> None:
    events: list[str] = []
    archive = MemoryArchive(events)
    with pytest.raises(ValueError, match="report_id"):
        make_facade(events, archive).build(report_id)
    assert events == []
    assert archive.keys() == ()


@pytest.mark.parametrize("report_id", ["A", "0", "-", "A" * 24])
def test_identifier_boundaries(report_id: str) -> None:
    events: list[str] = []
    archive = MemoryArchive(events)
    facade = ReportFacade(
        MemoryReports({report_id: Snapshot(())}, events), TextRenderer(events), archive
    )
    assert facade.build(report_id).key == f"{report_id}/1"


@pytest.mark.parametrize(
    "scenario, stage, write, steps, cause",
    [
        ("missing", Stage.LOAD, WriteOutcome.NOT_ATTEMPTED, ["load"], LoadError),
        ("render", Stage.RENDER, WriteOutcome.NOT_ATTEMPTED, ["load", "render"], RenderError),
        ("store", Stage.STORE, WriteOutcome.UNKNOWN, ["load", "render", "store"], StoreError),
    ],
)
def test_known_failure_stops_and_preserves_cause(
    scenario: str, stage: Stage, write: WriteOutcome, steps: list[str], cause: type[Exception]
) -> None:
    events: list[str] = []
    archive = MemoryArchive(events, fail_before_write=scenario == "store")
    facade = make_facade(events, archive, fail_render=scenario == "render")
    with pytest.raises(PacketUnavailable) as caught:
        facade.build("MISSING" if scenario == "missing" else "WEEK-1")
    assert caught.value.stage is stage
    assert caught.value.write_outcome is write
    assert isinstance(caught.value.__cause__, cause)
    assert events == steps
    assert archive.keys() == ()
    assert archive.close_count == 0


def test_lost_ack_is_unknown_and_no_automatic_retry() -> None:
    events: list[str] = []
    archive = MemoryArchive(events, lose_ack=True)
    with pytest.raises(PacketUnavailable) as caught:
        make_facade(events, archive).build("WEEK-1")
    assert caught.value.write_outcome is WriteOutcome.UNKNOWN
    assert archive.keys() == ("WEEK-1/1",)
    assert events.count("store") == 1


def test_blind_manual_retry_creates_another_object() -> None:
    events: list[str] = []
    archive = MemoryArchive(events, lose_ack=True)
    facade = make_facade(events, archive)
    for _ in range(2):
        with pytest.raises(PacketUnavailable):
            facade.build("WEEK-1")
    assert archive.keys() == ("WEEK-1/1", "WEEK-1/2")
    assert events == ["load", "render", "store"] * 2


class BuggyRenderer:
    def render(self, snapshot: Snapshot) -> bytes:
        raise TypeError("internal bug")


def test_programming_error_is_not_disguised_as_availability() -> None:
    events: list[str] = []
    archive = MemoryArchive(events)
    facade = ReportFacade(MemoryReports({"WEEK-1": Snapshot(())}, events), BuggyRenderer(), archive)
    with pytest.raises(TypeError, match="internal bug"):
        facade.build("WEEK-1")
    assert archive.keys() == ()


def test_dependencies_are_borrowed_and_lower_level_access_remains() -> None:
    events: list[str] = []
    archive = MemoryArchive(events)
    facade = make_facade(events, archive)
    first = facade.build("WEEK-1")
    second = facade.build("WEEK-1")
    assert archive.keys() == (first.key, second.key)
    assert archive.close_count == 0
    archive.close()
    assert archive.close_count == 1
    with pytest.raises(RuntimeError, match="closed"):
        facade.build("WEEK-1")


def test_instances_with_separate_dependencies_are_isolated() -> None:
    first_events: list[str] = []
    second_events: list[str] = []
    first = MemoryArchive(first_events)
    second = MemoryArchive(second_events)
    make_facade(first_events, first).build("WEEK-1")
    assert second.keys() == ()
    assert second_events == []


@pytest.mark.parametrize(
    "scenario, outcome, stores, objects, steps",
    [
        ("success", "acknowledged", 1, 1, "load,render,store"),
        ("missing", "load:not_attempted", 0, 0, "load"),
        ("render", "render:not_attempted", 0, 0, "load,render"),
        ("store_before", "store:unknown", 1, 0, "load,render,store"),
        ("lost_ack", "store:unknown", 1, 1, "load,render,store"),
    ],
)
def test_probe_contract(scenario: str, outcome: str, stores: int, objects: int, steps: str) -> None:
    assert observe(scenario) == (scenario, outcome, stores, objects, steps)
