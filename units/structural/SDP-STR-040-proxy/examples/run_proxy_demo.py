from catalog_contract import Document, Key, headline
from catalog_proxy import CatalogProxy, MemoryCatalog, Observation


def main() -> None:
    key = Key("orchard", "guide")
    events: list[Observation] = []

    def authorize(principal: str, requested: Key) -> None:
        if principal != "reader" or requested.tenant != "orchard":
            raise PermissionError("access denied")

    proxy = CatalogProxy(
        "reader",
        lambda: MemoryCatalog({key: Document(key, 1, ("Check the gates",))}),
        authorize,
        ttl=10,
        clock=lambda: 0.0,
        observe=events.append,
    )
    try:
        print(headline(proxy, key))
        print(headline(proxy, key))
        print([event.outcome for event in events])
    finally:
        proxy.close()


if __name__ == "__main__":
    main()
