"""Run the worked example without contacting a real output device."""

from name_export import export_legacy, export_overbuilt, export_refactored, preview_names


def main() -> None:
    names = ("Mira", " Omar ", "Mira")
    for export in (export_legacy, export_refactored, export_overbuilt):
        lines: list[str] = []
        count = export(names, lines.append)
        print(f"{export.__name__}: count={count}; lines={lines!r}")
    print(f"separate preview feature: {preview_names(names)!r}")


if __name__ == "__main__":
    main()
