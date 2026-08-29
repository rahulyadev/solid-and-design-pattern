"""Compare assignment, shallow copy, and deep copy on one nested object graph."""

from __future__ import annotations

from copy import copy, deepcopy


def observe_copy_depth() -> dict[str, object]:
    """Mutate one nested list and report which object graphs observe the change."""

    original = [["pick"], ["pack"]]
    assignment_alias = original
    shallow = copy(original)
    deep = deepcopy(original)

    original[0].append("scan")

    return {
        "assignment_is_original": assignment_alias is original,
        "shallow_is_original": shallow is original,
        "shallow_first_step_is_original": shallow[0] is original[0],
        "deep_first_step_is_original": deep[0] is original[0],
        "original_first_step": tuple(original[0]),
        "shallow_first_step": tuple(shallow[0]),
        "deep_first_step": tuple(deep[0]),
    }


def main() -> None:
    """Print stable observations for the experiment record."""

    for key, value in observe_copy_depth().items():
        print(f"{key}={value}")


if __name__ == "__main__":
    main()
