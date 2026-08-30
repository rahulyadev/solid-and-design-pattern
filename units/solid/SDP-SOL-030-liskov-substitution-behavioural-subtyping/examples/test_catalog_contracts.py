"""Shared contract tests plus explicit witnesses against teaching counterexamples."""

from collections.abc import Callable, Mapping

import pytest
from catalog_contracts import (
    BlankOnMissingCatalog,
    Catalog,
    ConsumingCatalog,
    DictCatalog,
    LeakyErrorCatalog,
    RestrictedCatalog,
    TupleCatalog,
    UnknownCode,
    label_or_unlisted,
    lookup_twice,
)
from hypothesis import given
from hypothesis import strategies as st
from run_catalog_demo import run_demo


@pytest.mark.parametrize("factory", [DictCatalog, TupleCatalog])
@pytest.mark.parametrize("code", ["", " ", "x", "box", " Box ", "पुस्तक"])
def test_every_string_code_can_be_looked_up_repeatedly(
    factory: Callable[[Mapping[str, str]], Catalog], code: str
) -> None:
    assert lookup_twice(factory({code: "exact value"}), code) == ("exact value", "exact value")


@pytest.mark.parametrize("factory", [DictCatalog, TupleCatalog])
@pytest.mark.parametrize("value", ["", " ", "\n", "  label  ", "箱"])
def test_exact_result_is_not_normalized(
    factory: Callable[[Mapping[str, str]], Catalog], value: str
) -> None:
    assert factory({"code": value}).lookup("code") == value


@pytest.mark.parametrize("factory", [DictCatalog, TupleCatalog])
@pytest.mark.parametrize("code", ["", "x", "X", " box "])
def test_absence_has_a_documented_error_and_no_effect_on_other_entries(
    factory: Callable[[Mapping[str, str]], Catalog], code: str
) -> None:
    catalog = factory({"box": "crate"})
    with pytest.raises(UnknownCode):
        catalog.lookup(code)
    assert catalog.lookup("box") == "crate"
    assert label_or_unlisted(catalog, code) == "unlisted"


@pytest.mark.parametrize("factory", [DictCatalog, TupleCatalog])
def test_constructor_detaches_from_the_source_mapping(
    factory: Callable[[Mapping[str, str]], Catalog],
) -> None:
    source = {"x": "original"}
    catalog = factory(source)
    source["x"] = "changed"
    source["new"] = "added later"
    assert lookup_twice(catalog, "x") == ("original", "original")
    with pytest.raises(UnknownCode):
        catalog.lookup("new")


@given(entries=st.dictionaries(st.text(), st.text(), max_size=12), code=st.text())
def test_representations_agree_for_generated_inputs(entries: dict[str, str], code: str) -> None:
    for catalog in (DictCatalog(entries), TupleCatalog(entries)):
        if code in entries:
            assert lookup_twice(catalog, code) == (entries[code], entries[code])
        else:
            with pytest.raises(UnknownCode):
                catalog.lookup(code)


def test_restricted_subclass_rejects_a_base_valid_call() -> None:
    catalog: Catalog = RestrictedCatalog({"x": "parcel"})
    with pytest.raises(ValueError):
        catalog.lookup("x")


def test_blank_fallback_is_not_equivalent_to_documented_absence() -> None:
    catalog: Catalog = BlankOnMissingCatalog({"empty": ""})
    assert label_or_unlisted(catalog, "absent") == ""
    assert label_or_unlisted(DictCatalog({"empty": ""}), "absent") == "unlisted"


def test_consuming_subclass_breaks_the_second_valid_read() -> None:
    catalog: Catalog = ConsumingCatalog({"x": "parcel"})
    assert catalog.lookup("x") == "parcel"
    with pytest.raises(UnknownCode):
        catalog.lookup("x")


def test_storage_exception_is_not_the_public_absence_exception() -> None:
    catalog: Catalog = LeakyErrorCatalog({})
    with pytest.raises(KeyError):
        label_or_unlisted(catalog, "absent")


def test_demonstration_reports_counterexamples_without_claiming_conformance() -> None:
    assert run_demo() == (
        "DictCatalog: repeated=('parcel', 'parcel'); missing='unlisted'",
        "TupleCatalog: repeated=('parcel', 'parcel'); missing='unlisted'",
        "RestrictedCatalog: repeated=ValueError; missing='unlisted'",
        "BlankOnMissingCatalog: repeated=('parcel', 'parcel'); missing=''",
        "ConsumingCatalog: repeated=UnknownCode; missing='unlisted'",
        "LeakyErrorCatalog: repeated=('parcel', 'parcel'); missing=KeyError",
    )
