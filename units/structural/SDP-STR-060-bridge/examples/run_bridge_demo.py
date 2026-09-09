"""Deterministic report content; nothing is written outside stdout."""

from bridge import StockItem, make_report


def main() -> None:
    items = (StockItem("clip", 3, 5), StockItem("tray", 8, 8))
    for policy in ("inventory", "shortage"):
        for output in ("csv", "json"):
            artifact = make_report(policy, output).render(items)
            print(f"{policy}/{output} [{artifact.media_type}]")
            print(artifact.body.rstrip("\n"))


if __name__ == "__main__":
    main()
