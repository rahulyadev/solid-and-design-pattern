"""Unsolved import preflight lab; baseline commands make no storage writes."""

from dataclasses import dataclass


@dataclass(frozen=True)
class FileInfo:
    name: str
    size: int
    supported: bool


class Inspector:
    def __init__(self, files: tuple[FileInfo, ...]) -> None:
        self._files = files

    def inspect(self) -> tuple[FileInfo, ...]:
        return self._files


class Capacity:
    def __init__(self, remaining: int) -> None:
        self._remaining = remaining

    def remaining_bytes(self) -> int:
        return self._remaining


def cli_preview(inspector: Inspector, capacity: Capacity) -> str:
    files = inspector.inspect()
    total = sum(file.size for file in files)
    return f"files={len(files)}; bytes={total}; fits={total <= capacity.remaining_bytes()}"


def web_preview(inspector: Inspector, capacity: Capacity) -> dict[str, int | bool]:
    files = inspector.inspect()
    total = sum(file.size for file in files)
    return {"count": len(files), "bytes": total, "fits": total <= capacity.remaining_bytes()}


def build_preflight(inspector: Inspector, capacity: Capacity) -> object:
    """Define the new task result and implement the brief after your prediction."""
    raise NotImplementedError("SDP-STR-020: preserve your attempt before requesting a hint")


def main() -> None:
    inspector = Inspector((FileInfo("sample.txt", 4, True),))
    capacity = Capacity(8)
    print(cli_preview(inspector, capacity))
    print(web_preview(inspector, capacity))
    print("target_complete=False")


if __name__ == "__main__":
    main()
