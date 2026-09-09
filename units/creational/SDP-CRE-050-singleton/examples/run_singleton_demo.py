"""Run from any directory; no network, credentials, or files are used."""

from copy import copy, deepcopy
from pickle import dumps, loads

from lifetimes import MemoryReader, application
from singleton import ProcessMarker


def main() -> None:
    marker = ProcessMarker()
    print(
        "marker",
        marker is ProcessMarker(),
        copy(marker) is marker,
        deepcopy(marker) is marker,
        loads(dumps(marker)) is marker,
    )
    reader = MemoryReader({"cover": "indigo"}, revision="r1")
    with application(lambda: reader) as app:
        print("shared", app.preview.reader is app.export.reader)
        print(app.preview.render("cover"))
    print("closed", reader.closed)


if __name__ == "__main__":
    main()
