"""Run the worked pricing snapshot flow."""

from __future__ import annotations

from value_models import QuoteRecord, quote_from_record, quote_to_record


def main() -> None:
    incoming: QuoteRecord = {
        "quote_id": "quote-101",
        "state": "draft",
        "revision": 1,
        "lines": [
            {
                "sku": "book-blue",
                "quantity": 2,
                "unit_minor_units": 750,
                "currency": "INR",
            },
            {
                "sku": "pen-black",
                "quantity": 3,
                "unit_minor_units": 125,
                "currency": "INR",
            },
        ],
    }

    draft = quote_from_record(incoming)
    confirmed = draft.confirm()

    print(f"draft={draft.state.value}@r{draft.revision}")
    print(f"confirmed={confirmed.state.value}@r{confirmed.revision}")
    print(f"total={confirmed.total.currency.value} {confirmed.total.minor_units}")
    print(quote_to_record(confirmed))


if __name__ == "__main__":
    main()
