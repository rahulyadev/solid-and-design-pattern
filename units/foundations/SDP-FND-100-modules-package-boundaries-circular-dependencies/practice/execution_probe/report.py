"""Report package metadata after a relative import succeeds."""

from .helper import MESSAGE


def main() -> None:
    """Print the execution context relevant to package imports."""

    spec_name = __spec__.name if __spec__ is not None else None
    print(f"module_name={__name__}")
    print(f"package={__package__}")
    print(f"spec_name={spec_name}")
    print(f"message={MESSAGE}")


if __name__ == "__main__":
    main()
