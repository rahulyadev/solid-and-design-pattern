"""Parse the checkout lab's local imports and report one directed cycle."""

from __future__ import annotations

import ast
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import cast

Graph = dict[str, set[str]]


def _module_name(path: Path, package_root: Path, package_name: str) -> tuple[str, bool]:
    relative = path.relative_to(package_root)
    parts = list(relative.with_suffix("").parts)
    is_package = parts[-1] == "__init__"
    if is_package:
        parts.pop()
    suffix = ".".join(parts)
    return (package_name if not suffix else f"{package_name}.{suffix}", is_package)


def _relative_base(current: str, is_package: bool, level: int) -> list[str]:
    package_parts = current.split(".") if is_package else current.split(".")[:-1]
    ascend = level - 1
    if ascend > len(package_parts):
        return []
    return package_parts[: len(package_parts) - ascend]


def _targets(
    node: ast.Import | ast.ImportFrom,
    current: str,
    is_package: bool,
) -> Iterable[str]:
    if isinstance(node, ast.Import):
        yield from (alias.name for alias in node.names)
        return

    if node.level == 0:
        if node.module is not None:
            yield node.module
        return

    base = _relative_base(current, is_package, node.level)
    if node.module is not None:
        yield ".".join([*base, node.module])
        return

    for alias in node.names:
        yield ".".join([*base, alias.name])


def build_import_graph(package_root: Path, package_name: str) -> Graph:
    """Return internal module dependencies discovered from import statements."""

    module_files = {
        path: _module_name(path, package_root, package_name)
        for path in sorted(package_root.rglob("*.py"))
    }
    known_modules = {module for module, _ in module_files.values()}
    graph: Graph = {module: set() for module in known_modules}

    for path, (module, is_package) in module_files.items():
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, (ast.Import, ast.ImportFrom)):
                continue
            for target in _targets(node, module, is_package):
                matching = [
                    candidate
                    for candidate in known_modules
                    if candidate == target or target.startswith(f"{candidate}.")
                ]
                if matching:
                    graph[module].add(max(matching, key=len))

    return graph


def find_cycle(graph: Mapping[str, set[str]]) -> tuple[str, ...] | None:
    """Return the first deterministic directed cycle, including its repeated start."""

    active: set[str] = set()
    complete: set[str] = set()
    stack: list[str] = []

    def visit(node: str) -> tuple[str, ...] | None:
        active.add(node)
        stack.append(node)
        for dependency in sorted(graph.get(node, set())):
            if dependency in active:
                start = stack.index(dependency)
                return (*stack[start:], dependency)
            if dependency not in complete:
                cycle = visit(dependency)
                if cycle is not None:
                    return cycle
        stack.pop()
        active.remove(node)
        complete.add(node)
        return None

    for node in sorted(graph):
        if node not in complete:
            cycle = visit(node)
            if cycle is not None:
                return cycle
    return None


def observe_dependency_graph() -> dict[str, object]:
    """Return stable graph facts for the unsolved checkout package."""

    package_root = Path(__file__).resolve().parent / "checkout_lab"
    graph = build_import_graph(package_root, "checkout_lab")
    edges = tuple(
        f"{source} -> {target}" for source in sorted(graph) for target in sorted(graph[source])
    )
    return {
        "module_count": len(graph),
        "edges": edges,
        "cycle": find_cycle(graph),
    }


def main() -> None:
    """Print one line per stable dependency-graph observation."""

    observation = observe_dependency_graph()
    print(f"module_count={observation['module_count']}")
    edges = cast(tuple[str, ...], observation["edges"])
    for edge in edges:
        print(f"edge={edge}")
    cycle = cast(tuple[str, ...] | None, observation["cycle"])
    print(f"cycle={' -> '.join(cycle) if cycle is not None else 'none'}")


if __name__ == "__main__":
    main()
