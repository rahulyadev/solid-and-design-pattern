"""Deterministic observations of permission, stale data, expiry and ownership."""

from dataclasses import dataclass

from catalog_contract import Document, Key
from catalog_proxy import CatalogProxy, MemoryCatalog, Observation


@dataclass
class Clock:
    now: float = 0.0

    def __call__(self) -> float:
        return self.now


def probe() -> list[tuple[str, str, int, int, str]]:
    key = Key("orchard", "guide")
    base = MemoryCatalog({key: Document(key, 1, ("old",))})
    clock = Clock()
    permissions = {("reader", key)}
    events: list[Observation] = []
    builds = 0

    def factory() -> MemoryCatalog:
        nonlocal builds
        builds += 1
        return base

    def authorize(principal: str, requested: Key) -> None:
        if (principal, requested) not in permissions:
            raise PermissionError("access denied")

    proxy = CatalogProxy("reader", factory, authorize, ttl=10, clock=clock, observe=events.append)
    rows: list[tuple[str, str, int, int, str]] = [("wired", "-", builds, base.reads, "-")]

    def read(label: str) -> None:
        try:
            value = str(proxy.read(key).revision)
        except PermissionError:
            value = "PermissionError"
        rows.append((label, value, builds, base.reads, events[-1].outcome))

    read("first")
    base.put(Document(key, 2, ("new",)))
    read("cached")
    permissions.clear()
    read("revoked")
    permissions.add(("reader", key))
    clock.now = 10
    read("expiry")
    base.put(Document(key, 3, ("newest",)))
    proxy.invalidate()
    read("invalidated")
    proxy.close()
    rows.append(("closed", str(base.closes), builds, base.reads, "-"))
    return rows


if __name__ == "__main__":
    for row in probe():
        print(" | ".join(map(str, row)))
