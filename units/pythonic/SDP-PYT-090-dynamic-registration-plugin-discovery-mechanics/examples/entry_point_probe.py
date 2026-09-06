"""Build a temporary installed-distribution fixture and probe entry-point loading."""

from __future__ import annotations

import importlib
import sys
from dataclasses import asdict, dataclass
from importlib import metadata
from pathlib import Path
from tempfile import TemporaryDirectory

PROBE_GROUP = "sdp.pyt090.fixture"
MODULE_NAME = "sdp_pyt090_fixture_runtime"


@dataclass(frozen=True, slots=True)
class EntryPointObservation:
    name: str
    group: str
    value: str
    module: str
    attribute: str
    distribution: str
    version: str
    imported_during_discovery: bool
    import_executions_after_two_loads: int
    same_loaded_object: bool
    provider_result: str


def _write_fixture(root: Path, marker: Path) -> None:
    module_source = f'''"""Synthetic module created only inside a temporary directory."""
from pathlib import Path

_MARKER = Path({str(marker)!r})
with _MARKER.open("a", encoding="utf-8") as stream:
    stream.write("imported\\n")

def provide() -> str:
    return "synthetic-provider-ready"
'''
    (root / f"{MODULE_NAME}.py").write_text(module_source, encoding="utf-8")

    dist_info = root / "acme_report_plugin-2.4.0.dist-info"
    dist_info.mkdir()
    (dist_info / "METADATA").write_text(
        "Metadata-Version: 2.1\nName: Acme-Report-Plugin\nVersion: 2.4.0\n",
        encoding="utf-8",
    )
    (dist_info / "entry_points.txt").write_text(
        f"[{PROBE_GROUP}]\nfixture = {MODULE_NAME}:provide\n",
        encoding="utf-8",
    )


def observe_entry_point_boundary() -> EntryPointObservation:
    with TemporaryDirectory(prefix="sdp-pyt090-entry-point-") as temporary:
        root = Path(temporary)
        marker = root / "import-marker.txt"
        _write_fixture(root, marker)
        sys.path.insert(0, str(root))
        importlib.invalidate_caches()
        try:
            matches = tuple(metadata.entry_points(group=PROBE_GROUP))
            if len(matches) != 1:
                raise RuntimeError(f"expected one synthetic entry point, found {len(matches)}")
            entry_point = matches[0]
            imported_during_discovery = marker.exists()

            first = entry_point.load()
            second = entry_point.load()
            executions = marker.read_text(encoding="utf-8").count("imported\n")
            distribution = getattr(entry_point, "dist", None)
            distribution_name = (
                str(distribution.metadata.get("Name", "<unknown>"))
                if distribution is not None
                else "<unknown>"
            )
            version = str(distribution.version) if distribution is not None else "<unknown>"
            provider_result = first()
            return EntryPointObservation(
                name=entry_point.name,
                group=entry_point.group,
                value=entry_point.value,
                module=entry_point.module,
                attribute=entry_point.attr,
                distribution=distribution_name,
                version=version,
                imported_during_discovery=imported_during_discovery,
                import_executions_after_two_loads=executions,
                same_loaded_object=first is second,
                provider_result=str(provider_result),
            )
        finally:
            sys.path.remove(str(root))
            sys.modules.pop(MODULE_NAME, None)
            importlib.invalidate_caches()


def main() -> None:
    for key, value in asdict(observe_entry_point_boundary()).items():
        print(f"{key}={value}")


if __name__ == "__main__":
    main()
