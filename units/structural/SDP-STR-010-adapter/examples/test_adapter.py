from contextlib import closing

import pytest
from hypothesis import given
from hypothesis import strategies as st
from legacy_warehouse import LegacyWarehouse, WarehouseTimeout
from stock_contract import InvalidStock, Stock, StockReader, StockUnavailable, availability
from warehouse_adapter import WarehouseAdapter, decode_stock


def record(cases: object = 2, pack_size: object = 6) -> dict[str, object]:
    return {"schema": 1, "item": "BOLT", "pack_size": pack_size, "cases": cases}


@pytest.mark.parametrize("cases,expected", [(2, 12), (0, 0), (None, None)])
def test_translation_preserves_meaning(cases: object, expected: int | None) -> None:
    vendor = LegacyWarehouse({"BOLT": record(cases)})
    reader: StockReader = WarehouseAdapter(vendor)
    assert reader.read("BOLT") == Stock(expected)
    assert vendor.calls == ["BOLT"]
    assert not vendor.closed


def test_missing_record_is_unknown() -> None:
    assert WarehouseAdapter(LegacyWarehouse({})).read("BOLT") == Stock(None)


@pytest.mark.parametrize("cases", [True, False, -1, 1_000_001, 2.0, "2", [], {}])
def test_invalid_counts_are_not_coerced(cases: object) -> None:
    with pytest.raises(InvalidStock, match="case count"):
        decode_stock(record(cases), "BOLT")


@pytest.mark.parametrize("pack", [None, True, 0, -1, 1001, 6.0, "6"])
def test_invalid_pack_is_rejected_even_when_count_unknown(pack: object) -> None:
    with pytest.raises(InvalidStock, match="pack size"):
        decode_stock(record(None, pack), "BOLT")


@pytest.mark.parametrize("payload", [[], "", 0, True])
def test_non_record_rejected(payload: object) -> None:
    with pytest.raises(InvalidStock, match="record"):
        decode_stock(payload, "BOLT")


@pytest.mark.parametrize("schema", [None, True, "1", 1.0, 2])
def test_schema_drift_rejected(schema: object) -> None:
    row = record()
    row["schema"] = schema
    with pytest.raises(InvalidStock, match="schema"):
        decode_stock(row, "BOLT")


@pytest.mark.parametrize("field", ["schema", "item", "pack_size", "cases"])
def test_missing_required_field_is_invalid(field: str) -> None:
    row = record()
    del row[field]
    with pytest.raises(InvalidStock):
        decode_stock(row, "BOLT")


def test_wrong_item_cannot_cross_boundary() -> None:
    with pytest.raises(InvalidStock, match="mismatch"):
        decode_stock(record(), "NUT")


def test_extra_metadata_ignored_and_output_does_not_alias_payload() -> None:
    row = record()
    row["vendor_debug"] = {"private": "synthetic"}
    original = dict(row)
    result = decode_stock(row, "BOLT")
    assert row == original
    row["cases"] = 100
    assert result == Stock(12)
    assert not hasattr(result, "vendor_debug")


@given(cases=st.integers(min_value=0, max_value=1_000_000), pack=st.integers(1, 1000))
def test_exact_integer_conversion(cases: int, pack: int) -> None:
    result = decode_stock(record(cases, pack), "BOLT")
    assert result.units == cases * pack


@pytest.mark.parametrize("sku", ["", "bolt", "BOLT ", "A/B", "É", "A" * 25])
def test_invalid_input_fails_before_provider_call(sku: str) -> None:
    vendor = LegacyWarehouse({})
    with pytest.raises(ValueError):
        WarehouseAdapter(vendor).read(sku)
    assert vendor.calls == []


def test_timeout_translation_no_retry_and_next_call_can_recover() -> None:
    vendor = LegacyWarehouse({"BOLT": record()})
    reader = WarehouseAdapter(vendor)
    vendor.fail_next = True
    with pytest.raises(StockUnavailable, match="stock provider unavailable") as failure:
        reader.read("BOLT")
    assert isinstance(failure.value.__cause__, WarehouseTimeout)
    assert "synthetic vendor" not in str(failure.value)
    assert vendor.calls == ["BOLT"]
    assert reader.read("BOLT").units == 12
    assert vendor.calls == ["BOLT", "BOLT"]


def test_unexpected_sdk_bug_is_not_disguised_as_empty_or_unavailable() -> None:
    class BrokenWarehouse(LegacyWarehouse):
        def fetch_cases(self, *, item_code: str) -> object:
            raise TypeError("synthetic SDK bug")

    with pytest.raises(TypeError, match="SDK bug"):
        WarehouseAdapter(BrokenWarehouse({})).read("BOLT")


def test_fresh_reads_and_independent_adapters() -> None:
    row = record()
    first = LegacyWarehouse({"BOLT": row})
    second = LegacyWarehouse({"BOLT": record(9)})
    reader = WarehouseAdapter(first)
    assert reader.read("BOLT").units == 12
    row["cases"] = 0
    assert reader.read("BOLT").units == 0
    assert WarehouseAdapter(second).read("BOLT").units == 54


@pytest.mark.parametrize("fail", [False, True])
def test_owner_closes_on_success_and_body_failure(fail: bool) -> None:
    vendor = LegacyWarehouse({"BOLT": record()})
    reader = WarehouseAdapter(vendor)
    try:
        with closing(vendor):
            reader.read("BOLT")
            assert vendor.close_count == 0
            if fail:
                raise ValueError("body failed")
    except ValueError as error:
        assert str(error) == "body failed"
    assert vendor.close_count == 1
    with pytest.raises(RuntimeError, match="closed"):
        reader.read("BOLT")


@pytest.mark.parametrize(
    "units,expected", [(None, "unknown"), (0, "short"), (10, "enough"), (9, "short")]
)
def test_client_uses_target_contract_without_sdk(units: int | None, expected: str) -> None:
    class FixedReader:
        def read(self, sku: str, /) -> Stock:
            return Stock(units)

    assert availability(FixedReader(), "BOLT", 10) == expected


@pytest.mark.parametrize("required", [0, -1, True])
def test_invalid_demand_does_not_query(required: int) -> None:
    vendor = LegacyWarehouse({})
    with pytest.raises(ValueError):
        availability(WarehouseAdapter(vendor), "BOLT", required)
    assert vendor.calls == []
