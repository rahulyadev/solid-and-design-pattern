import os
import subprocess
import sys
from pathlib import Path

import pytest


@pytest.mark.parametrize("target", ["3.11", "3.14"])
def test_positive_and_negative_contracts(tmp_path: Path, target: str) -> None:
    env = dict(os.environ, MYPYPATH=str(Path(__file__).resolve().parent))
    env["MYPY_CACHE_DIR"] = str(tmp_path / "mypy")
    fixture = tmp_path / "contract_case.py"
    args = [sys.executable, "-m", "mypy", "--strict", "--python-version", target, str(fixture)]
    fixture.write_text(
        "from catalog_contract import Catalog, OwnedCatalog, Key, headline\n"
        "from catalog_proxy import CatalogProxy, MemoryCatalog\n"
        "owned: OwnedCatalog = MemoryCatalog({})\n"
        "client: Catalog = CatalogProxy('reader', lambda: owned, lambda p, k: None, ttl=10)\n"
        "result: str = headline(client, Key('orchard', 'guide'))\n"
    )
    good = subprocess.run(args, env=env, capture_output=True, text=True, check=False)
    assert good.returncode == 0, good.stdout + good.stderr
    fixture.write_text(
        "from catalog_contract import Catalog, Key, Document, OwnedCatalog\n"
        "from catalog_proxy import CatalogProxy\n"
        "class WrongResult:\n"
        "    def read(self, key: Key, /) -> bytes:\n"
        "        return b'wrong'\n"
        "class ReadOnly:\n"
        "    def read(self, key: Key, /) -> Document:\n"
        "        return Document(key, 1, ())\n"
        "wrong: Catalog = WrongResult()\n"
        "owned: OwnedCatalog = ReadOnly()\n"
        "def boolean_policy(p: str, k: Key) -> bool:\n"
        "    return False\n"
        "proxy = CatalogProxy('reader', lambda: owned, boolean_policy, ttl=10)\n"
    )
    bad = subprocess.run(args, env=env, capture_output=True, text=True, check=False)
    assert bad.returncode == 1, bad.stdout + bad.stderr
    assert bad.stdout.count("[assignment]") == 2
    assert bad.stdout.count("[arg-type]") == 1
    assert "Found 3 errors" in bad.stdout
