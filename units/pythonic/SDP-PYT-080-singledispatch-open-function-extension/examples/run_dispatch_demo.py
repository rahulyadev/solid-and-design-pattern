"""Run the worked single-dispatch example from the repository root."""

from open_rendering import (
    DispatchObservation,
    PrivilegedUserRegistered,
    RenderContext,
    render_observed,
)


def main() -> None:
    observations: list[DispatchObservation] = []
    result = render_observed(
        PrivilegedUserRegistered("evt-41", "rahul", "example.test", "admin"),
        context=RenderContext("req-41", "operations"),
        observe=observations.append,
    )
    print(result.body)
    print(observations[0])


if __name__ == "__main__":
    main()
