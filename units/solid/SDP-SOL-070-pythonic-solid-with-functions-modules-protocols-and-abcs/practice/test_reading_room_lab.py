import pytest
from reading_room_lab import ReadingCard, ShelfCatalog, build_reading_cards


def test_found_missing_order_and_duplicates() -> None:
    catalog = ShelfCatalog({"night": "Night Skies", "garden": "Small Gardens"})
    assert build_reading_cards(("night", "absent", "garden", "night"), catalog) == (
        ReadingCard("night", "Night Skies", True),
        ReadingCard("absent", "Not on this shelf", False),
        ReadingCard("garden", "Small Gardens", True),
        ReadingCard("night", "Night Skies", True),
    )


class UnavailableShelf(ShelfCatalog):
    def lookup(self, code: str) -> str:
        raise OSError("catalog unavailable")


def test_empty_input_does_not_access_catalog() -> None:
    assert build_reading_cards((), UnavailableShelf({})) == ()


@pytest.mark.parametrize("blank", ["", " ", "\t\n"])
def test_all_codes_are_validated_before_lookup(blank: str) -> None:
    with pytest.raises(ValueError, match="nonblank"):
        build_reading_cards(("night", blank), UnavailableShelf({}))


def test_outage_is_not_reported_as_missing() -> None:
    with pytest.raises(OSError, match="catalog unavailable"):
        build_reading_cards(("night",), UnavailableShelf({}))


def test_whitespace_and_unicode_are_preserved() -> None:
    catalog = ShelfCatalog({"  sky  ": "星の本"})
    assert build_reading_cards(("  sky  ", "sky"), catalog) == (
        ReadingCard("  sky  ", "星の本", True),
        ReadingCard("sky", "Not on this shelf", False),
    )


def test_inputs_are_preserved_and_catalog_owns_a_copy() -> None:
    titles = {"night": "Night Skies"}
    catalog = ShelfCatalog(titles)
    titles["night"] = "Changed outside"
    codes = ["night", "absent"]
    assert build_reading_cards(codes, catalog)[0].title == "Night Skies"
    assert codes == ["night", "absent"]


def test_catalog_administration_still_works() -> None:
    catalog = ShelfCatalog({})
    catalog.replace("night", "Night Skies")
    assert catalog.lookup("night") == "Night Skies"
    catalog.remove("night")
    with pytest.raises(KeyError):
        catalog.lookup("night")


def test_empty_title_is_characterized_without_silently_tightening_the_contract() -> None:
    assert build_reading_cards(("draft",), ShelfCatalog({"draft": ""})) == (
        ReadingCard("draft", "", True),
    )
