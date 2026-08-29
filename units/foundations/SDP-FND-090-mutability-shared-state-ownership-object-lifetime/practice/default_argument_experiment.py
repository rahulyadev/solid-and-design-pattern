"""Observe definition-time mutable default binding without cross-run contamination."""

from __future__ import annotations


def observe_default_argument() -> dict[str, object]:
    """Return identity and value observations from one freshly defined collector."""

    def collect(label: str, bucket: list[str] = []) -> list[str]:  # noqa: B006
        bucket.append(label)
        return bucket

    first = collect("first")
    first_value_before_second_call = tuple(first)
    second = collect("second")
    default_bucket = collect.__defaults__[0] if collect.__defaults__ is not None else None

    return {
        "first_value_before_second_call": first_value_before_second_call,
        "same_result_object": first is second,
        "default_is_result_object": default_bucket is second,
        "value_after_second_call": tuple(first),
    }


def main() -> None:
    """Print stable observations for the experiment record."""

    for key, value in observe_default_argument().items():
        print(f"{key}={value}")


if __name__ == "__main__":
    main()
