#!/usr/bin/env python3
"""Validate the SOLID and Design Patterns learning repository using only the standard library."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import tomllib
import zipfile
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from urllib.parse import unquote

UNIT_ID_RE = re.compile(r"SDP-[A-Z]{3}-\d{3}")
PROJECT_ID_RE = re.compile(r"SDP-PRJ-\d{3}")
EXPECTED_UNIT_COUNT = 100
EXPECTED_PROJECT_IDS = [f"SDP-PRJ-{number:03d}" for number in range(10, 70, 10)]
EXPECTED_PATHS = [
    ("emergency-interview-revision", "Emergency interview revision"),
    ("seven-day-interview-crash", "7-day interview crash path"),
    ("fourteen-day-interview-preparation", "14-day interview preparation"),
    ("thirty-day-strong-foundation", "30-day strong-foundation path"),
    ("complete-solid-pattern-mastery", "Complete SOLID and design-pattern mastery"),
    ("python-backend-application-architecture", "Python backend and application architecture"),
    ("refactoring-pythonic-design", "Refactoring and Pythonic design"),
    ("senior-comparison-design-practice", "Senior interview comparison and design practice"),
]
REQUIRED_FILES = [
    ".gitignore",
    ".python-version",
    "AGENTS.md",
    "BUNDLE_MANIFEST.md",
    "CURRICULUM.md",
    "LEARNING_PATHS.md",
    "PYTHON_REFERENCES.md",
    "NOTEBOOKLM.md",
    "PROGRESS.md",
    "PROJECTS.md",
    "README.md",
    "START_HERE.md",
    "pyproject.toml",
    "uv.lock",
    "docs/COPYRIGHT_AND_LICENSE.md",
    "docs/NOTEBOOKLM.md",
    "docs/SOURCE_AND_VERSION_POLICY.md",
    "docs/WORKFLOW.md",
    "scripts/validate_repo.py",
    "templates/experiment.md",
    "templates/practice.md",
    "templates/project.md",
    "templates/review.md",
    "templates/unit.md",
]
FORBIDDEN_COMPONENTS = {
    ".venv", "venv", "env", "ENV", "__pycache__", ".pytest_cache",
    ".mypy_cache", ".ruff_cache", ".hypothesis", "secrets", "credentials",
    "transcripts", "chat-exports", ".idea", ".vscode",
}
FORBIDDEN_ARCHIVE_PREFIXES = (".git/", "units/", "projects/")
FORBIDDEN_LICENSE_NAMES = {"LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING"}
SENSITIVE_SUFFIXES = {".pem", ".key", ".p12", ".pfx", ".kdbx"}
ALLOWED_ANGLE_PLACEHOLDERS = {
    "<DOMAIN>", "<THREE-DIGIT-SEQUENCE>", "<TOPIC-ID>", "<PROJECT-ID>",
    "<topic or question>", "<question or concept>", "<domain-slug>",
    "<topic-slug>", "<project-slug>",
}
ALLOWED_ARTIFACT_STATES = {"Absent", "Draft", "Approved"}
ALLOWED_LEARNING_STATES = {
    "Not started", "Learning", "Practiced", "Recalled", "Demonstrated", "Retained"
}
ALLOWED_PROJECT_STATES = {"Planned", "Active", "Complete"}
ALLOWED_PRIORITIES = {"Core", "Professional", "Advanced", "Reference"}
ALLOWED_FREQUENCIES = {"High", "Medium", "Low"}
ALLOWED_DEPTHS = {"D1", "D2", "D3", "D4"}
ALLOWED_SIZES = {"S", "M", "L", "XL"}
ALLOWED_EVIDENCE_TOKENS = {"E", "I", "D", "X", "(X)", "T"}
ALLOWED_SCOPES = {
    "Anti-pattern risk", "Anti-patterns", "Application", "Architecture", "Backend",
    "Behavioral", "Comparison", "Concurrency", "Contracts", "Creational", "Data model",
    "Design", "Distributed", "Domain", "Events", "GoF", "Idiom", "Interview", "Modules",
    "Persistence", "Plugins", "Protocols", "Python", "Refactoring", "Reference", "Runtime",
    "SOLID", "Standard library", "Structural", "Synthesis", "Testing", "Typing",
}
EXPECTED_SOLID_UNITS = {
    "SDP-SOL-010": "Single Responsibility Principle",
    "SDP-SOL-020": "Open/Closed Principle",
    "SDP-SOL-030": "Liskov Substitution Principle and behavioural subtyping",
    "SDP-SOL-040": "Interface Segregation Principle",
    "SDP-SOL-050": "Dependency Inversion Principle",
}
EXPECTED_GOF_UNITS = {
    "SDP-CRE-010": "Factory Method",
    "SDP-CRE-020": "Abstract Factory",
    "SDP-CRE-030": "Builder",
    "SDP-CRE-040": "Prototype",
    "SDP-CRE-050": "Singleton",
    "SDP-STR-010": "Adapter",
    "SDP-STR-020": "Facade",
    "SDP-STR-030": "Decorator",
    "SDP-STR-040": "Proxy",
    "SDP-STR-050": "Composite",
    "SDP-STR-060": "Bridge",
    "SDP-STR-070": "Flyweight",
    "SDP-BEH-010": "Strategy",
    "SDP-BEH-020": "State",
    "SDP-BEH-030": "Observer",
    "SDP-BEH-040": "Command",
    "SDP-BEH-050": "Chain of Responsibility",
    "SDP-BEH-060": "Template Method",
    "SDP-BEH-070": "Iterator",
    "SDP-BEH-080": "Mediator",
    "SDP-BEH-090": "Memento",
    "SDP-BEH-100": "Visitor",
    "SDP-BEH-110": "Interpreter",
}
EXPECTED_GRASP_TERMS = {
    "Information Expert", "Creator", "Controller", "Low Coupling", "High Cohesion",
    "Indirection", "Polymorphism", "Protected Variations", "Pure Fabrication",
}
RAPID_MINUTES_BY_SIZE = {
    "S": (10, 15),
    "M": (15, 25),
    "L": (20, 30),
    "XL": (30, 45),
}
RAPID_PATH_ANCHORS = {
    "emergency-interview-revision",
    "seven-day-interview-crash",
    "fourteen-day-interview-preparation",
    "thirty-day-strong-foundation",
}
EXPECTED_RAPID_ACTIVITY_BREAKDOWNS = {
    "emergency-interview-revision": {
        "Recall": (45, 45),
        "Comparison": (30, 45),
        "Mock interview": (45, 45),
        "Refactoring/project checkpoint": (30, 45),
    },
}
REQUIRED_DEV_TOOLS = {"hypothesis", "mypy", "pytest", "pytest-cov", "ruff"}
MANUAL_INSPECTION_ITEMS = [
    "Pedagogical depth and simple-first explanations in future generated units",
    "Idiomatic Python quality of future generated examples and labs",
    "Copyright originality and historical-source interpretation",
    "Interview realism and production judgment beyond structural metadata",
]
APPROVED_PYTHON_REFERENCES = {
    "PY-OBJ-010": "Classes, instances, methods, and construction",
    "PY-OBJ-020": "Properties, encapsulation, and composition",
    "PY-OBJ-030": "Inheritance, MRO, and super",
    "PY-OBJ-040": "Python data model and special methods",
    "PY-FIT-030": "Higher-order functions, callable objects, and side effects",
    "PY-FIT-040": "Closures, free variables, and late binding",
    "PY-FIT-050": "Decorators",
    "PY-FIT-070": "Iterable and iterator protocols",
    "PY-FIT-080": "Generators, yield, and delegation",
    "PY-FIT-090": "Lazy pipelines and streaming transformations",
    "PY-ERR-030": "Context managers and resource safety",
    "PY-MOD-010": "Modules, packages, and executable modules",
    "PY-MOD-020": "Import resolution, sys.path, and module caching",
    "PY-MOD-030": "Circular imports and package boundaries",
    "PY-MOD-070": "Package layouts, resources, entry points, and plugin boundaries",
    "PY-TYP-050": "Protocols, ABCs, and structural versus nominal typing",
    "PY-TYP-030": "Generics and type variables",
    "PY-TYP-040": "Variance and safe generic API design",
    "PY-TYP-060": "Callable typing, overloads, ParamSpec, and Self",
    "PY-LIB-060": "Dataclasses, enums, types, and generated data models",
    "PY-TST-020": "Pytest fundamentals and fixtures",
    "PY-TST-040": "Test doubles, mocking, and patching boundaries",
    "PY-TST-070": "Formatting, linting, static analysis, and maintainability",
    "PY-LIB-040": "Callable transformation with functools and operator",
    "PY-OBJ-050": "Attribute lookup, customization, and slots",
    "PY-OBJ-060": "Descriptors",
    "PY-OBJ-070": "Class-creation hooks and class decorators",
    "PY-OBJ-080": "Metaclasses and dynamic class creation",
    "PY-FND-020": "Objects, names, references, and mutability",
    "PY-IOP-060": "Pickle, shelve, copying, and object graphs",
    "PY-MPR-010": "Object lifetime, reference counting, finalization, and weak references",
    "PY-BLT-050": "Dictionaries and mapping behaviour",
    "PY-BLT-080": "Equality, ordering, hashing, and hashability",
}


@dataclass
class Report:
    root: Path
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    checks: dict[str, str] = field(default_factory=dict)
    statistics: dict[str, object] = field(default_factory=dict)
    archive: dict[str, object] | None = None

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warning(self, message: str) -> None:
        self.warnings.append(message)

    def mark(self, name: str, result: bool | str) -> None:
        if isinstance(result, str):
            if result not in {"passed", "failed", "skipped"}:
                raise ValueError(f"Invalid check result: {result}")
            self.checks[name] = result
        else:
            self.checks[name] = "passed" if result else "failed"

    def as_dict(self) -> dict[str, object]:
        return {
            "schema_version": 1,
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "status": "passed" if not self.errors else "failed",
            "repository_root": ".",
            "validation_scope": {
                "automated": "completed",
                "manual_inspection": {
                    "status": "not_performed",
                    "items": MANUAL_INSPECTION_ITEMS,
                },
            },
            "checks": self.checks,
            "statistics": self.statistics,
            "archive": self.archive,
            "errors": self.errors,
            "warnings": self.warnings,
        }


@dataclass(frozen=True)
class Unit:
    unit_id: str
    title: str
    outcome: str
    prerequisites: tuple[str, ...]
    anchor: str
    priority: str
    interview: str
    production: str
    python_backend: str
    depth: str
    scopes: tuple[str, ...]
    size: str
    first_hours: tuple[int, int]
    practice_hours: tuple[int, int]
    evidence: tuple[str, ...]


@dataclass(frozen=True)
class Project:
    project_id: str
    title: str
    anchor: str
    required: tuple[str, ...]
    recommended: tuple[str, ...]


def read_text(path: Path, report: Report) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        try:
            relative = path.relative_to(report.root)
        except ValueError:
            relative = path
        report.error(f"Cannot read UTF-8 text file {relative}: {exc}")
        return ""


def split_table_row(line: str) -> list[str]:
    text = line.strip()
    if not text.startswith("|"):
        return []
    text = text[1:]
    if text.endswith("|") and not text.endswith(r"\|"):
        text = text[:-1]
    cells: list[str] = []
    current: list[str] = []
    escaped = False
    code_delimiter = 0
    index = 0
    while index < len(text):
        char = text[index]
        if escaped:
            current.append(char)
            escaped = False
            index += 1
            continue
        if char == "\\":
            current.append(char)
            escaped = True
            index += 1
            continue
        if char == "`":
            run = 1
            while index + run < len(text) and text[index + run] == "`":
                run += 1
            current.extend("`" * run)
            if code_delimiter == 0:
                code_delimiter = run
            elif run == code_delimiter:
                code_delimiter = 0
            index += run
            continue
        if char == "|" and code_delimiter == 0:
            cells.append("".join(current).strip())
            current = []
        else:
            current.append(char)
        index += 1
    cells.append("".join(current).strip())
    return cells


def is_separator_row(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in cells)


def lines_outside_fences(text: str, relative_path: str, report: Report) -> tuple[list[tuple[int, str]], int]:
    visible: list[tuple[int, str]] = []
    open_fence: tuple[str, int, int] | None = None
    blocks = 0
    for line_number, line in enumerate(text.splitlines(), 1):
        match = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if match:
            marker = match.group(1)
            char = marker[0]
            length = len(marker)
            if open_fence is None:
                open_fence = (char, length, line_number)
                blocks += 1
            elif char == open_fence[0] and length >= open_fence[1]:
                open_fence = None
            continue
        if open_fence is None:
            visible.append((line_number, line))
    if open_fence is not None:
        report.error(f"Unclosed code fence in {relative_path}, opened at line {open_fence[2]}")
    return visible, blocks


def github_slug(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"[`*_~]", "", text).strip().lower()
    text = re.sub(r"[^\w\- ]", "", text, flags=re.UNICODE)
    text = re.sub(r"\s+", "-", text)
    return re.sub(r"-+", "-", text).strip("-")


def anchors_for_markdown(path: Path, report: Report) -> set[str]:
    text = read_text(path, report)
    anchors = set(re.findall(r'<a\s+id="([^"]+)"\s*></a>', text))
    visible, _ = lines_outside_fences(text, str(path.relative_to(report.root)), report)
    counts: defaultdict[str, int] = defaultdict(int)
    for _, line in visible:
        match = re.match(r"^ {0,3}#{1,6}\s+(.+?)\s*#*\s*$", line)
        if not match:
            continue
        base = github_slug(match.group(1))
        if not base:
            continue
        count = counts[base]
        anchors.add(base if count == 0 else f"{base}-{count}")
        counts[base] += 1
    return anchors


def markdown_links(text: str, relative_path: str, report: Report) -> list[tuple[int, str]]:
    visible, _ = lines_outside_fences(text, relative_path, report)
    pattern = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
    links: list[tuple[int, str]] = []
    for line_number, line in visible:
        for match in pattern.finditer(line):
            target = match.group(1).strip()
            if " " in target and not target.startswith("<"):
                target = target.split(" ", 1)[0]
            links.append((line_number, target.strip("<>")))
    return links


def validate_required_files(report: Report) -> None:
    missing = [path for path in REQUIRED_FILES if not (report.root / path).is_file()]
    for path in missing:
        report.error(f"Required file is missing: {path}")
    report.statistics["required_files"] = len(REQUIRED_FILES)
    report.statistics["required_files_present"] = len(REQUIRED_FILES) - len(missing)
    report.mark("required_files", not missing)


def parse_hour_range(value: str) -> tuple[int, int] | None:
    cleaned = value.strip().replace("**", "").replace(",", "")
    match = re.fullmatch(r"(\d+)\s*[–-]\s*(\d+)\s*h", cleaned)
    if not match:
        return None
    return int(match.group(1)), int(match.group(2))


def parse_duration_minutes(value: str) -> tuple[int, int] | None:
    cleaned = value.strip().replace("**", "").replace(",", "").rstrip(".")
    cleaned = re.sub(r"\s+before\b.*$", "", cleaned)
    parts = re.split(r"\s*[–-]\s*", cleaned, maxsplit=1)
    if len(parts) != 2:
        return None
    unit_hint = "h" if "h" in cleaned else "min"

    def parse_part(part: str) -> int | None:
        hours = re.search(r"(\d+)\s*h", part)
        minutes = re.search(r"(\d+)\s*min", part)
        if hours or minutes:
            return (int(hours.group(1)) * 60 if hours else 0) + (int(minutes.group(1)) if minutes else 0)
        bare = re.fullmatch(r"\s*(\d+)\s*", part)
        if bare:
            return int(bare.group(1)) * (60 if unit_hint == "h" else 1)
        return None

    low = parse_part(parts[0])
    high = parse_part(parts[1])
    if low is None or high is None:
        return None
    return low, high


def extract_labeled_duration(section: str, label: str) -> tuple[int, int] | None:
    match = re.search(rf"(?m)^\*\*{re.escape(label)}:\*\* (.+)$", section)
    return parse_duration_minutes(match.group(1)) if match else None


def parse_activity_duration_minutes(value: str) -> tuple[int, int] | None:
    ranged = parse_duration_minutes(value)
    if ranged is not None:
        return ranged
    cleaned = value.strip().replace("**", "").replace(",", "").rstrip(".")
    match = re.fullmatch(r"(?:(\d+)\s*h)?(?:\s*(\d+)\s*min)?", cleaned)
    if match is None or (match.group(1) is None and match.group(2) is None):
        return None
    total = (int(match.group(1)) * 60 if match.group(1) else 0) + (
        int(match.group(2)) if match.group(2) else 0
    )
    return total, total


def extract_activity_breakdown(
    section: str, report: Report, path_title: str
) -> dict[str, tuple[int, int]] | None:
    heading = re.search(r"(?m)^### Required timed activity breakdown\s*$", section)
    if heading is None:
        report.error(f"Learning path '{path_title}' is missing its explicit activity breakdown")
        return None
    next_heading = re.search(r"(?m)^### ", section[heading.end():])
    end = heading.end() + next_heading.start() if next_heading else len(section)
    block = section[heading.end():end]
    rows = [split_table_row(line) for line in block.splitlines() if line.lstrip().startswith("|")]
    rows = [row for row in rows if row]
    if len(rows) < 3 or rows[0] != ["Activity", "Required time"] or not is_separator_row(rows[1]):
        report.error(f"Learning path '{path_title}' has a malformed activity-breakdown table")
        return None
    result: dict[str, tuple[int, int]] = {}
    for row in rows[2:]:
        if len(row) != 2:
            report.error(f"Learning path '{path_title}' has a malformed activity-breakdown row: {row}")
            continue
        name, value = row
        if name in result:
            report.error(f"Learning path '{path_title}' repeats activity '{name}'")
            continue
        duration = parse_activity_duration_minutes(value)
        if duration is None:
            report.error(f"Learning path '{path_title}' has malformed duration for '{name}': {value}")
            continue
        result[name] = duration
    return result


def parse_curriculum(report: Report) -> tuple[list[Unit], dict[str, Unit]]:
    text = read_text(report.root / "CURRICULUM.md", report)
    units: list[Unit] = []
    row_pattern = re.compile(
        r'^<a id="(?P<anchor>sdp-[a-z]{3}-\d{3})"></a>\s+`(?P<id>SDP-[A-Z]{3}-\d{3})`\s+—\s+\*\*(?P<title>.+?)\*\*$'
    )
    for line_number, line in enumerate(text.splitlines(), 1):
        if not line.startswith('| <a id="sdp-'):
            continue
        cells = split_table_row(line)
        if len(cells) != 13:
            report.error(f"Curriculum row at line {line_number} does not have 13 columns")
            continue
        match = row_pattern.fullmatch(cells[0])
        if not match:
            report.error(f"Malformed curriculum ID/title cell at line {line_number}: {cells[0]}")
            continue
        unit_id = match.group("id")
        anchor = match.group("anchor")
        if anchor != unit_id.lower():
            report.error(f"Anchor {anchor} does not match {unit_id} at line {line_number}")
        prerequisites = tuple(UNIT_ID_RE.findall(cells[2]))
        priority, interview, production, python_backend, depth = cells[3:8]
        scopes = tuple(scope.strip() for scope in cells[8].split(",") if scope.strip())
        size = cells[9]
        first_hours = parse_hour_range(cells[10])
        practice_hours = parse_hour_range(cells[11])
        evidence_text = cells[12].strip("`")
        evidence = tuple(re.findall(r"\(X\)|[EIDXT]", evidence_text))
        if priority not in ALLOWED_PRIORITIES:
            report.error(f"{unit_id} has invalid priority {priority!r}")
        for field_name, value in (("interview", interview), ("production", production), ("Python/backend", python_backend)):
            if value not in ALLOWED_FREQUENCIES:
                report.error(f"{unit_id} has invalid {field_name} frequency {value!r}")
        if depth not in ALLOWED_DEPTHS:
            report.error(f"{unit_id} has invalid depth {depth!r}")
        if size not in ALLOWED_SIZES:
            report.error(f"{unit_id} has invalid size {size!r}")
        unknown_scopes = sorted(set(scopes) - ALLOWED_SCOPES)
        if unknown_scopes:
            report.error(f"{unit_id} has invalid scope values: {', '.join(unknown_scopes)}")
        unknown_evidence = sorted(set(evidence) - ALLOWED_EVIDENCE_TOKENS)
        reconstructed = "+".join(evidence)
        if unknown_evidence or reconstructed != evidence_text:
            report.error(f"{unit_id} has invalid evidence value {evidence_text!r}")
        if first_hours is None or practice_hours is None:
            report.error(f"{unit_id} has malformed time estimate")
            first_hours = first_hours or (0, 0)
            practice_hours = practice_hours or (0, 0)
        units.append(Unit(
            unit_id, match.group("title"), cells[1], prerequisites, anchor, priority,
            interview, production, python_backend, depth, scopes, size,
            first_hours, practice_hours, evidence,
        ))

    ids = [unit.unit_id for unit in units]
    duplicates = sorted(unit_id for unit_id, count in Counter(ids).items() if count > 1)
    if len(units) != EXPECTED_UNIT_COUNT:
        report.error(f"Expected {EXPECTED_UNIT_COUNT} curriculum units, found {len(units)}")
    if duplicates:
        report.error(f"Duplicate curriculum unit IDs: {', '.join(duplicates)}")
    unit_map = {unit.unit_id: unit for unit in units}
    positions = {unit.unit_id: index for index, unit in enumerate(units)}
    for unit in units:
        for prerequisite in unit.prerequisites:
            if prerequisite not in unit_map:
                report.error(f"{unit.unit_id} has unknown prerequisite {prerequisite}")
            elif positions[prerequisite] >= positions[unit.unit_id]:
                report.error(f"Curriculum puts {unit.unit_id} before prerequisite {prerequisite}")

    state = {unit_id: 0 for unit_id in unit_map}
    stack: list[str] = []

    def visit(unit_id: str) -> None:
        state[unit_id] = 1
        stack.append(unit_id)
        for prerequisite in unit_map[unit_id].prerequisites:
            if prerequisite not in unit_map:
                continue
            if state[prerequisite] == 0:
                visit(prerequisite)
            elif state[prerequisite] == 1:
                start_index = stack.index(prerequisite)
                report.error("Curriculum prerequisite cycle: " + " -> ".join(stack[start_index:] + [prerequisite]))
        stack.pop()
        state[unit_id] = 2

    for unit_id in unit_map:
        if state[unit_id] == 0:
            visit(unit_id)

    for expected_id, expected_title in EXPECTED_SOLID_UNITS.items():
        unit = unit_map.get(expected_id)
        if unit is None or unit.title != expected_title:
            report.error(f"Missing or renamed SOLID principle unit: {expected_id} — {expected_title}")
    for expected_id, expected_title in EXPECTED_GOF_UNITS.items():
        unit = unit_map.get(expected_id)
        if unit is None or unit.title != expected_title:
            report.error(f"Missing or renamed independent GoF unit: {expected_id} — {expected_title}")
    grasp_unit = unit_map.get("SDP-FND-020")
    if grasp_unit:
        missing_grasp = sorted(term for term in EXPECTED_GRASP_TERMS if term not in grasp_unit.outcome)
        if missing_grasp:
            report.error("SDP-FND-020 is missing GRASP coverage: " + ", ".join(missing_grasp))

    report.statistics["curriculum_units"] = len(units)
    report.statistics["unique_curriculum_ids"] = len(set(ids))
    report.statistics["prerequisite_edges"] = sum(len(unit.prerequisites) for unit in units)
    report.statistics["curriculum_domains"] = len({unit.unit_id.split("-")[1] for unit in units})
    report.statistics["solid_principles"] = sum(unit_id in unit_map for unit_id in EXPECTED_SOLID_UNITS)
    report.statistics["gof_patterns"] = sum(unit_id in unit_map for unit_id in EXPECTED_GOF_UNITS)
    report.statistics["grasp_responsibility_lenses"] = len(EXPECTED_GRASP_TERMS)
    report.mark("curriculum", len(units) == EXPECTED_UNIT_COUNT and len(set(ids)) == EXPECTED_UNIT_COUNT and not duplicates)
    report.mark("curriculum_prerequisite_order", not any("Curriculum puts" in e for e in report.errors))
    report.mark("curriculum_classifications", not any(" has invalid " in error or "malformed time estimate" in error for error in report.errors))
    report.mark("solid_coverage", all(unit_map.get(k) and unit_map[k].title == v for k, v in EXPECTED_SOLID_UNITS.items()))
    report.mark("gof_coverage", all(unit_map.get(k) and unit_map[k].title == v for k, v in EXPECTED_GOF_UNITS.items()))
    report.mark("grasp_coverage", bool(grasp_unit) and all(term in grasp_unit.outcome for term in EXPECTED_GRASP_TERMS))
    report.mark("prerequisite_cycles", not any("prerequisite cycle" in error for error in report.errors))
    return units, unit_map

def validate_progress(report: Report, units: list[Unit], unit_map: dict[str, Unit]) -> None:
    text = read_text(report.root / "PROGRESS.md", report)
    rows: list[tuple[str, str, str, str, str]] = []
    pattern = re.compile(
        r'^\| `(?P<id>SDP-[A-Z]{3}-\d{3})` \| \[(?P<title>[^\]]+)\]\(CURRICULUM\.md#(?P<anchor>sdp-[a-z]{3}-\d{3})\) \| (?P<priority>[^|]+?) \| (?P<artifact>Absent|Draft|Approved) \| (?P<learning>Not started|Learning|Practiced|Recalled|Demonstrated|Retained) \|'
    )
    for line in text.splitlines():
        match = pattern.match(line)
        if match:
            rows.append((match.group("id"), match.group("title"), match.group("anchor"), match.group("artifact"), match.group("learning")))
    row_ids = [row[0] for row in rows]
    canonical_ids = [unit.unit_id for unit in units]
    if len(rows) != EXPECTED_UNIT_COUNT:
        report.error(f"Expected {EXPECTED_UNIT_COUNT} curriculum progress rows, found {len(rows)}")
    if row_ids != canonical_ids:
        report.error("Curriculum progress rows do not match canonical curriculum order")
    for unit_id, title, anchor, artifact, learning in rows:
        unit = unit_map.get(unit_id)
        if unit and (title != unit.title or anchor != unit.anchor):
            report.error(f"Progress row metadata mismatch for {unit_id}")
        if artifact not in ALLOWED_ARTIFACT_STATES:
            report.error(f"Invalid artifact state for {unit_id}: {artifact}")
        if learning not in ALLOWED_LEARNING_STATES:
            report.error(f"Invalid learning state for {unit_id}: {learning}")
    report.statistics["progress_unit_rows"] = len(rows)
    report.mark("progress_units", len(rows) == EXPECTED_UNIT_COUNT and row_ids == canonical_ids)


def validate_learning_paths(report: Report, units: list[Unit], unit_map: dict[str, Unit]) -> None:
    text = read_text(report.root / "LEARNING_PATHS.md", report)
    section_pattern = re.compile(r'(?m)^<a id="([^"]+)"></a>\n## (.+)$')
    matches = list(section_pattern.finditer(text))
    actual = [(m.group(1), m.group(2)) for m in matches]
    if actual != EXPECTED_PATHS:
        report.error(f"Learning-path anchors or titles differ from expected paths: {actual}")
    selector_end = matches[0].start() if matches else len(text)
    selector = text[:selector_end]
    for anchor, title in EXPECTED_PATHS:
        if f"[{title}](#{anchor})" not in selector:
            report.error(f"Learning-path selector is missing {title} -> #{anchor}")

    rapid_contracts = {
        size: RAPID_MINUTES_BY_SIZE[size]
        for size in ("S", "M", "L", "XL")
    }
    for size, (low, high) in rapid_contracts.items():
        expected_cell = f"{low}–{high} min"
        if f"| {size} | {expected_cell} |" not in text:
            report.error(f"Rapid interview contract is missing {size} = {expected_cell}")

    total_links = 0
    total_project_callouts = 0
    timing_stats: dict[str, object] = {}
    canonical_ids = [unit.unit_id for unit in units]
    for index, match in enumerate(matches):
        section_end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        section = text[match.end():section_end]
        path_anchor, path_title = match.group(1), match.group(2)
        entry_pattern = re.compile(
            r'(?m)^(\d+)\. \[(SDP-[A-Z]{3}-\d{3}) — (.+?)\]\(CURRICULUM\.md#(sdp-[a-z]{3}-\d{3})\)$'
        )
        entries = [(int(m.group(1)), m.group(2), m.group(3), m.group(4)) for m in entry_pattern.finditer(section)]
        numbers = [item[0] for item in entries]
        if numbers != list(range(1, len(entries) + 1)):
            report.error(f"Learning path '{path_title}' has non-sequential numbering")
        ids = [item[1] for item in entries]
        duplicates = sorted(unit_id for unit_id, count in Counter(ids).items() if count > 1)
        if duplicates:
            report.error(f"Learning path '{path_title}' repeats: {', '.join(duplicates)}")
        declared_match = re.search(r'(?m)^\*\*Canonical units in this path:\*\* (\d+)\s*$', section)
        if not declared_match:
            report.error(f"Learning path '{path_title}' is missing its declared unit count")
        elif int(declared_match.group(1)) != len(entries):
            report.error(f"Learning path '{path_title}' declares {declared_match.group(1)} units but links {len(entries)}")
        positions = {unit_id: position for position, unit_id in enumerate(ids)}
        omitted = 0
        for _, unit_id, title, anchor in entries:
            unit = unit_map.get(unit_id)
            if unit is None:
                report.error(f"Learning path '{path_title}' uses unknown unit {unit_id}")
                continue
            if title != unit.title or anchor != unit.anchor:
                report.error(f"Learning path metadata mismatch for {unit_id} in '{path_title}'")
            for prerequisite in unit.prerequisites:
                if prerequisite in positions:
                    if positions[prerequisite] > positions[unit_id]:
                        report.error(f"Learning path '{path_title}' puts {unit_id} before included prerequisite {prerequisite}")
                else:
                    omitted += 1
        if omitted:
            lowered = section.lower()
            if "assumed prior knowledge" not in lowered and "prerequisite bridge" not in lowered:
                report.error(f"Learning path '{path_title}' omits prerequisites without an assumed-knowledge or prerequisite-bridge label")
        if "SOLID coverage:** Complete" in section:
            missing_solid = sorted(set(EXPECTED_SOLID_UNITS) - set(ids))
            if missing_solid:
                report.error(f"Learning path '{path_title}' claims complete SOLID coverage but omits: {', '.join(missing_solid)}")
        if path_anchor == "complete-solid-pattern-mastery" and ids != canonical_ids:
            report.error("Complete mastery path does not match all canonical units in canonical order")

        if path_anchor in RAPID_PATH_ANCHORS:
            rapid_unit = (
                sum(RAPID_MINUTES_BY_SIZE[unit_map[unit_id].size][0] for unit_id in ids),
                sum(RAPID_MINUTES_BY_SIZE[unit_map[unit_id].size][1] for unit_id in ids),
            )
            full_unit = (
                sum((unit_map[unit_id].first_hours[0] + unit_map[unit_id].practice_hours[0]) * 60 for unit_id in ids),
                sum((unit_map[unit_id].first_hours[1] + unit_map[unit_id].practice_hours[1]) * 60 for unit_id in ids),
            )
            declared_rapid_unit = extract_labeled_duration(section, "Rapid-pass unit total")
            declared_activities = extract_labeled_duration(section, "Required path activities")
            declared_rapid_total = extract_labeled_duration(section, "Rapid-path total")
            declared_full = extract_labeled_duration(section, "Full-mastery unit total")
            activity_breakdown: dict[str, tuple[int, int]] | None = None
            activities = declared_activities
            expected_breakdown = EXPECTED_RAPID_ACTIVITY_BREAKDOWNS.get(path_anchor)
            if expected_breakdown is not None:
                activity_breakdown = extract_activity_breakdown(section, report, path_title)
                if activity_breakdown is not None:
                    if activity_breakdown != expected_breakdown:
                        report.error(
                            f"Learning path '{path_title}' activity breakdown is "
                            f"{activity_breakdown}, expected {expected_breakdown}"
                        )
                    activities = (
                        sum(duration[0] for duration in activity_breakdown.values()),
                        sum(duration[1] for duration in activity_breakdown.values()),
                    )
                    if declared_activities != activities:
                        report.error(
                            f"Learning path '{path_title}' required path activities are "
                            f"{declared_activities}, but the explicit breakdown totals {activities} minutes"
                        )
                else:
                    activities = None
            if declared_rapid_unit != rapid_unit:
                report.error(f"Learning path '{path_title}' rapid unit total is {declared_rapid_unit}, expected {rapid_unit} minutes")
            if declared_full != full_unit:
                report.error(f"Learning path '{path_title}' full-mastery unit total is {declared_full}, expected {full_unit} minutes")
            if activities is None or declared_rapid_total is None:
                report.error(f"Learning path '{path_title}' has malformed rapid activity or total timing")
            else:
                expected_total = (rapid_unit[0] + activities[0], rapid_unit[1] + activities[1])
                if declared_rapid_total != expected_total:
                    report.error(f"Learning path '{path_title}' rapid total is {declared_rapid_total}, expected {expected_total} minutes")
            timing_stats[path_anchor] = {
                "units": len(ids),
                "rapid_unit_minutes": list(rapid_unit),
                "required_activity_minutes": list(activities) if activities else None,
                "activity_breakdown_minutes": (
                    {name: list(duration) for name, duration in activity_breakdown.items()}
                    if activity_breakdown is not None else None
                ),
                "rapid_total_minutes": list(declared_rapid_total) if declared_rapid_total else None,
                "full_mastery_minutes": list(full_unit),
            }

        callout_pattern = re.compile(r'\[(SDP-PRJ-\d{3}) — ([^\]]+)\]\(PROJECTS\.md#(sdp-prj-\d{3})\)')
        callouts = callout_pattern.findall(section)
        for project_id, _title, anchor in callouts:
            if project_id not in EXPECTED_PROJECT_IDS or anchor != project_id.lower():
                report.error(f"Invalid project callout {project_id} in '{path_title}'")
        total_links += len(entries)
        total_project_callouts += len(callouts)

    report.statistics["learning_paths"] = len(matches)
    report.statistics["learning_path_topic_links"] = total_links
    report.statistics["learning_path_project_callouts"] = total_project_callouts
    report.statistics["rapid_path_timings"] = timing_stats
    path_errors = [e for e in report.errors if "Learning path" in e or "Complete mastery" in e or "Rapid interview contract" in e]
    report.mark("learning_paths", actual == EXPECTED_PATHS and not path_errors)
    report.mark("learning_path_counts", not any("declares" in e or "declared unit count" in e for e in report.errors))
    report.mark("learning_path_prerequisite_order", not any("before included prerequisite" in e for e in report.errors))
    report.mark("learning_path_solid_claims", not any("claims complete SOLID" in e for e in report.errors))
    report.mark("rapid_path_timings", not any("rapid unit total" in e or "full-mastery unit total" in e or "rapid total is" in e or "malformed rapid" in e or "activity breakdown" in e or "activity-breakdown" in e or "required path activities" in e for e in report.errors))

def parse_projects(report: Report, unit_map: dict[str, Unit]) -> dict[str, Project]:
    text = read_text(report.root / "PROJECTS.md", report)
    details_pattern = re.compile(
        r'(?m)^<a id="(?P<anchor>sdp-prj-\d{3})"></a>\n## (?P<id>SDP-PRJ-\d{3}) — (?P<title>.+)$'
    )
    detail_matches = list(details_pattern.finditer(text))
    projects: dict[str, Project] = {}
    for index, match in enumerate(detail_matches):
        end = detail_matches[index + 1].start() if index + 1 < len(detail_matches) else len(text)
        section = text[match.end():end]
        required_match = re.search(r'(?m)^\*\*Required:\*\* (.+)$', section)
        recommended_match = re.search(r'(?m)^\*\*Recommended:\*\* (.+)$', section)
        required = tuple(UNIT_ID_RE.findall(required_match.group(1))) if required_match else ()
        recommended = tuple(UNIT_ID_RE.findall(recommended_match.group(1))) if recommended_match else ()
        project = Project(match.group("id"), match.group("title"), match.group("anchor"), required, recommended)
        if project.project_id in projects:
            report.error(f"Duplicate detailed project ID {project.project_id}")
        projects[project.project_id] = project
        if project.anchor != project.project_id.lower():
            report.error(f"Project anchor {project.anchor} does not match {project.project_id}")
        for unit_id in required + recommended:
            if unit_id not in unit_map:
                report.error(f"{project.project_id} references unknown prerequisite {unit_id}")

    overview_pattern = re.compile(
        r'(?m)^\| `(SDP-PRJ-\d{3})` \| \[([^\]]+)\]\(#(sdp-prj-\d{3})\) \|'
    )
    overview = list(overview_pattern.finditer(text))
    overview_ids = [m.group(1) for m in overview]
    if overview_ids != EXPECTED_PROJECT_IDS:
        report.error(f"Project overview IDs are invalid or out of order: {overview_ids}")
    for match in overview:
        project_id, title, anchor = match.groups()
        project = projects.get(project_id)
        if project is None:
            report.error(f"Project overview links to missing detail section {project_id}")
        elif title != project.title or anchor != project.anchor:
            report.error(f"Project overview metadata mismatch for {project_id}")
    if list(projects) != EXPECTED_PROJECT_IDS:
        report.error(f"Detailed project IDs are invalid or out of order: {list(projects)}")

    progress = read_text(report.root / "PROGRESS.md", report)
    tracker_pattern = re.compile(
        r'(?m)^\| `(SDP-PRJ-\d{3})` \| \[([^\]]+)\]\(PROJECTS\.md#(sdp-prj-\d{3})\) \| (Planned|Active|Complete) \| `project/(SDP-PRJ-\d{3})` \|'
    )
    tracker = list(tracker_pattern.finditer(progress))
    tracker_ids = [m.group(1) for m in tracker]
    if tracker_ids != EXPECTED_PROJECT_IDS:
        report.error(f"Project tracker IDs are invalid or out of order: {tracker_ids}")
    for match in tracker:
        project_id, title, anchor, state, branch_id = match.groups()
        project = projects.get(project_id)
        if project and (title != project.title or anchor != project.anchor or branch_id != project_id):
            report.error(f"Project tracker metadata mismatch for {project_id}")
        if state not in ALLOWED_PROJECT_STATES:
            report.error(f"Invalid project state for {project_id}: {state}")
    curriculum = read_text(report.root / "CURRICULUM.md", report)
    for project_id in EXPECTED_PROJECT_IDS:
        if re.search(rf'`{re.escape(project_id)}`\s+—', curriculum):
            report.error(f"Project ID {project_id} was incorrectly added as a curriculum unit")

    report.statistics["projects"] = len(projects)
    report.statistics["project_tracker_rows"] = len(tracker)
    report.mark(
        "projects",
        list(projects) == EXPECTED_PROJECT_IDS and overview_ids == EXPECTED_PROJECT_IDS and tracker_ids == EXPECTED_PROJECT_IDS,
    )
    return projects


def validate_python_references(report: Report) -> None:
    text = read_text(report.root / "PYTHON_REFERENCES.md", report)
    pattern = re.compile(
        r'\[(PY-[A-Z]{3}-\d{3}) — ([^\]]+)\]\(https://github\.com/rahulyadev/python-mastery/blob/main/CURRICULUM\.md#(py-[a-z]{3}-\d{3})\)'
    )
    links = pattern.findall(text)
    seen: dict[str, str] = {}
    for unit_id, title, anchor in links:
        if anchor != unit_id.lower():
            report.error(f"Python Mastery anchor mismatch for {unit_id}: {anchor}")
        expected_title = APPROVED_PYTHON_REFERENCES.get(unit_id)
        if expected_title is None:
            report.error(f"Unapproved or unknown Python Mastery reference {unit_id}")
        elif title != expected_title:
            report.error(f"Python Mastery title mismatch for {unit_id}")
        if unit_id in seen and seen[unit_id] != title:
            report.error(f"Conflicting Python Mastery titles for {unit_id}")
        seen[unit_id] = title
    missing = sorted(set(APPROVED_PYTHON_REFERENCES) - set(seen))
    if missing:
        report.error(f"Missing approved Python Mastery references: {', '.join(missing)}")
    report.statistics["python_mastery_reference_links"] = len(links)
    report.statistics["unique_python_mastery_references"] = len(seen)
    report.mark("python_references", not any("Python Mastery" in error for error in report.errors))


def validate_markdown(report: Report) -> None:
    markdown_files = sorted(
        path for path in report.root.rglob("*.md")
        if ".git" not in path.parts and not any(part in FORBIDDEN_COMPONENTS for part in path.parts)
    )
    table_count = 0
    fence_blocks = 0
    link_count = 0
    anchor_cache: dict[Path, set[str]] = {}
    for path in markdown_files:
        relative = str(path.relative_to(report.root))
        text = read_text(path, report)
        visible, blocks = lines_outside_fences(text, relative, report)
        fence_blocks += blocks
        visible_lines = [line for _, line in visible]
        visible_numbers = [number for number, _ in visible]
        index = 0
        while index + 1 < len(visible_lines):
            header = split_table_row(visible_lines[index])
            separator = split_table_row(visible_lines[index + 1])
            if header and is_separator_row(separator):
                table_count += 1
                expected = len(header)
                if len(separator) != expected:
                    report.error(f"Table separator column mismatch in {relative} at line {visible_numbers[index + 1]}")
                row_index = index + 2
                while row_index < len(visible_lines) and visible_lines[row_index].strip().startswith("|"):
                    cells = split_table_row(visible_lines[row_index])
                    if len(cells) != expected:
                        report.error(
                            f"Table row column mismatch in {relative} at line {visible_numbers[row_index]}: expected {expected}, found {len(cells)}"
                        )
                    row_index += 1
                index = row_index
            else:
                index += 1

        if "templates" not in path.parts:
            if re.search(r"\{\{[A-Z0-9_]+\}\}", text):
                report.error(f"Unexpected template placeholder outside templates/: {relative}")
            for placeholder in re.findall(r"<[^>\n]{1,100}>", text):
                if placeholder.startswith("<a ") or placeholder.startswith("</") or placeholder == "<br>":
                    continue
                if placeholder not in ALLOWED_ANGLE_PLACEHOLDERS:
                    report.error(f"Unexpected angle placeholder {placeholder} in {relative}")

        links = markdown_links(text, relative, report)
        link_count += len(links)
        if "templates" in path.parts:
            continue
        for line_number, target in links:
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", target) or target.startswith("mailto:"):
                continue
            target = unquote(target)
            file_part, separator, anchor = target.partition("#")
            resolved = path if file_part == "" else (path.parent / file_part).resolve()
            try:
                resolved.relative_to(report.root.resolve())
            except ValueError:
                report.error(f"Internal link escapes repository in {relative}:{line_number}: {target}")
                continue
            if not resolved.exists():
                report.error(f"Broken internal link in {relative}:{line_number}: {target}")
                continue
            if separator and anchor and resolved.is_file() and resolved.suffix.lower() == ".md":
                if resolved not in anchor_cache:
                    anchor_cache[resolved] = anchors_for_markdown(resolved, report)
                if anchor not in anchor_cache[resolved]:
                    report.error(f"Missing anchor #{anchor} for link in {relative}:{line_number}: {target}")

    report.statistics["markdown_files"] = len(markdown_files)
    report.statistics["markdown_tables"] = table_count
    report.statistics["code_fence_blocks"] = fence_blocks
    report.statistics["markdown_links"] = link_count
    bad_phrases = ("code fence", "Table ", "Broken internal link", "Missing anchor", "escapes repository", "placeholder")
    report.mark("markdown", not any(any(phrase in error for phrase in bad_phrases) for error in report.errors))


def validate_template_links(report: Report) -> None:
    substitutions = {
        "{{TOPIC_ID}}": "SDP-FND-010",
        "{{TOPIC_ANCHOR}}": "sdp-fnd-010",
        "{{PROJECT_ID}}": "SDP-PRJ-010",
        "{{PROJECT_ANCHOR}}": "sdp-prj-010",
        "{{DOMAIN_SLUG}}": "foundations",
        "{{TOPIC_SLUG}}": "design-vocabulary",
        "{{PROJECT_SLUG}}": "solid-legacy-refactoring-clinic",
    }
    intended = {
        "templates/unit.md": Path("units/foundations/SDP-FND-010-design-vocabulary/README.md"),
        "templates/practice.md": Path("units/foundations/SDP-FND-010-design-vocabulary/practice/README.md"),
        "templates/experiment.md": Path("units/foundations/SDP-FND-010-design-vocabulary/experiments/EXP-01-example/README.md"),
        "templates/review.md": Path("units/foundations/SDP-FND-010-design-vocabulary/review.md"),
        "templates/project.md": Path("projects/SDP-PRJ-010-solid-legacy-refactoring-clinic/README.md"),
    }
    virtual_files = set(intended.values()) | {
        Path("units/foundations/SDP-FND-010-design-vocabulary/README.md"),
        Path("projects/SDP-PRJ-010-solid-legacy-refactoring-clinic/README.md"),
    }
    checked = 0
    anchor_cache: dict[Path, set[str]] = {}
    for template_path, location in intended.items():
        text = read_text(report.root / template_path, report)
        for source, replacement in substitutions.items():
            text = text.replace(source, replacement)
        for line_number, target in markdown_links(text, template_path, report):
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", target):
                continue
            checked += 1
            file_part, separator, anchor = unquote(target).partition("#")
            resolved_relative = location if file_part == "" else Path(os.path.normpath(str(location.parent / file_part)))
            actual = report.root / resolved_relative
            if resolved_relative not in virtual_files and not actual.exists():
                report.error(
                    f"Template-relative link from {template_path}:{line_number} resolves to missing {resolved_relative}"
                )
                continue
            if separator and anchor and actual.exists() and actual.suffix == ".md":
                if actual not in anchor_cache:
                    anchor_cache[actual] = anchors_for_markdown(actual, report)
                if anchor not in anchor_cache[actual]:
                    report.error(
                        f"Template-relative link from {template_path}:{line_number} targets missing #{anchor}"
                    )
    report.statistics["template_relative_links"] = checked
    report.mark("template_links", not any("Template-relative link" in error for error in report.errors))


def validate_repository_paths(report: Report) -> None:
    scanned = 0
    violations = 0
    for path in report.root.rglob("*"):
        relative = path.relative_to(report.root)
        if relative.parts and relative.parts[0] == ".git":
            continue
        if path.is_file():
            scanned += 1
        if set(relative.parts) & FORBIDDEN_COMPONENTS:
            report.error(f"Forbidden generated or privacy-sensitive path: {relative}")
            violations += 1
        if path.name in FORBIDDEN_LICENSE_NAMES:
            report.error(f"License file exists before an explicit license decision: {relative}")
            violations += 1
        if path.is_file() and (path.suffix.lower() in SENSITIVE_SUFFIXES or path.name == ".env"):
            report.error(f"Potential credential or secret file: {relative}")
            violations += 1
    report.statistics["repository_files_scanned"] = scanned
    report.statistics["forbidden_path_violations"] = violations
    report.mark("repository_hygiene", violations == 0)


def validate_canonical_ids(report: Report) -> None:
    domains = "FND|SOL|PYT|CRE|STR|BEH|APP|ARC|RAR|REF|INT"
    short_pattern = re.compile(rf"(?<!SDP-)(?<![A-Z0-9-])(?:{domains})-\d{{3}}")
    malformed_pattern = re.compile(r"SDP-[A-Z]{1,4}-\d{1,4}")
    shortened: list[str] = []
    malformed: list[str] = []
    for path in report.root.rglob("*.md"):
        if "templates" in path.parts or ".git" in path.parts:
            continue
        text = read_text(path, report)
        for match in short_pattern.finditer(text):
            shortened.append(f"{path.relative_to(report.root)}:{match.group(0)}")
        for match in malformed_pattern.finditer(text):
            value = match.group(0)
            if not UNIT_ID_RE.fullmatch(value) and not PROJECT_ID_RE.fullmatch(value):
                malformed.append(f"{path.relative_to(report.root)}:{value}")
    if shortened:
        report.error(f"Shortened curriculum IDs found: {', '.join(shortened[:10])}")
    if malformed:
        report.error(f"Malformed SDP IDs found: {', '.join(malformed[:10])}")
    report.statistics["shortened_unit_id_references"] = len(shortened)
    report.statistics["malformed_sdp_id_references"] = len(malformed)
    report.mark("canonical_id_format", not shortened and not malformed)


def validate_toml_and_tooling(report: Report) -> None:
    pyproject_path = report.root / "pyproject.toml"
    lock_path = report.root / "uv.lock"
    parsed: dict[str, object] = {}
    try:
        parsed = tomllib.loads(read_text(pyproject_path, report))
        report.mark("pyproject_toml", True)
    except tomllib.TOMLDecodeError as exc:
        report.error(f"pyproject.toml is invalid TOML: {exc}")
        report.mark("pyproject_toml", False)
    try:
        lock_data = tomllib.loads(read_text(lock_path, report))
        report.mark("uv_lock_toml", True)
    except tomllib.TOMLDecodeError as exc:
        report.error(f"uv.lock is invalid TOML: {exc}")
        report.mark("uv_lock_toml", False)
        lock_data = {}

    groups = parsed.get("dependency-groups", {}) if isinstance(parsed, dict) else {}
    dev_entries = groups.get("dev", []) if isinstance(groups, dict) else []
    declared: set[str] = set()
    for entry in dev_entries if isinstance(dev_entries, list) else []:
        if isinstance(entry, str):
            name = re.split(r"[<>=!~ ;\[]", entry, maxsplit=1)[0].strip().lower().replace("_", "-")
            declared.add(name)
    missing_declared = sorted(REQUIRED_DEV_TOOLS - declared)
    if missing_declared:
        report.error("pyproject.toml dev group is missing: " + ", ".join(missing_declared))
    packages = lock_data.get("package", []) if isinstance(lock_data, dict) else []
    locked_names = {pkg.get("name") for pkg in packages if isinstance(pkg, dict)}
    missing_locked = sorted(REQUIRED_DEV_TOOLS - locked_names)
    if missing_locked:
        report.error("uv.lock is missing approved development tools: " + ", ".join(missing_locked))
    root_package = next((pkg for pkg in packages if isinstance(pkg, dict) and pkg.get("name") == "solid-design-pattern"), None)
    root_dev = set()
    if isinstance(root_package, dict):
        dev_dependencies = root_package.get("dev-dependencies", {})
        if isinstance(dev_dependencies, dict):
            for item in dev_dependencies.get("dev", []):
                if isinstance(item, dict) and isinstance(item.get("name"), str):
                    root_dev.add(item["name"])
    if root_dev != REQUIRED_DEV_TOOLS:
        report.error(f"uv.lock root dev dependencies are {sorted(root_dev)}, expected {sorted(REQUIRED_DEV_TOOLS)}")
    report.statistics["declared_dev_tools"] = sorted(declared)
    report.statistics["locked_packages"] = len(packages)
    report.mark("development_tooling", not missing_declared and not missing_locked and root_dev == REQUIRED_DEV_TOOLS)

    uv = shutil.which("uv")
    if uv is None:
        report.mark("uv_lock_consistency", "skipped")
        report.statistics["uv_lock_check"] = {"status": "skipped", "reason": "uv executable unavailable"}
    else:
        env = os.environ.copy()
        env["UV_PYTHON"] = sys.executable
        env["UV_NO_PROGRESS"] = "1"
        try:
            completed = subprocess.run(
                [uv, "lock", "--check"], cwd=report.root, env=env,
                text=True, capture_output=True, timeout=30, check=False,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            report.error(f"uv lock --check could not complete: {exc}")
            report.mark("uv_lock_consistency", False)
            report.statistics["uv_lock_check"] = {"status": "failed", "reason": str(exc)}
        else:
            status = "passed" if completed.returncode == 0 else "failed"
            report.mark("uv_lock_consistency", completed.returncode == 0)
            lock_check: dict[str, object] = {
                "status": status,
                "returncode": completed.returncode,
            }
            if completed.returncode != 0:
                lock_check["stdout"] = completed.stdout.strip()
                lock_check["stderr"] = completed.stderr.strip()
                report.error("uv lock --check failed: " + (completed.stderr.strip() or completed.stdout.strip()))
            report.statistics["uv_lock_check"] = lock_check


def validate_terminology(report: Report) -> None:
    occurrences: list[str] = []
    for path in report.root.rglob("*.md"):
        if ".git" in path.parts:
            continue
        text = read_text(path, report)
        for line_number, line in enumerate(text.splitlines(), 1):
            if re.search(r"\bMaterial state\b", line, re.IGNORECASE):
                occurrences.append(f"{path.relative_to(report.root)}:{line_number}")
    if occurrences:
        report.error("Use 'Artifact state' instead of 'Material state': " + ", ".join(occurrences[:10]))
    report.statistics["material_state_occurrences"] = len(occurrences)
    report.mark("artifact_state_terminology", not occurrences)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_archive(report: Report, archive_path: Path) -> None:
    errors_before = len(report.errors)
    info: dict[str, object] = {"path": archive_path.name, "exists": archive_path.is_file()}
    if not archive_path.is_file():
        report.error(f"Archive does not exist: {archive_path}")
        report.archive = info
        report.mark("archive", False)
        return
    info["sha256"] = sha256_file(archive_path)
    info["size_bytes"] = archive_path.stat().st_size
    try:
        with zipfile.ZipFile(archive_path) as archive:
            entries = archive.infolist()
            names = [entry.filename for entry in entries if not entry.is_dir()]
            info["entry_count"] = len(names)
            corrupt = archive.testzip()
            info["corrupt_entry"] = corrupt
            if len(names) != len(set(names)):
                report.error("Archive contains duplicate paths")
            if "README.md" not in names or "AGENTS.md" not in names:
                report.error("Archive has a wrapper directory or lacks root bootstrap files")
            for required in REQUIRED_FILES:
                if required not in names:
                    report.error(f"Archive is missing required file: {required}")
            for entry in entries:
                name = entry.filename
                pure = PurePosixPath(name)
                if pure.is_absolute() or ".." in pure.parts:
                    report.error(f"Unsafe archive path: {name}")
                if name.startswith(FORBIDDEN_ARCHIVE_PREFIXES):
                    report.error(f"Forbidden archive path: {name}")
                if any(part in FORBIDDEN_COMPONENTS for part in pure.parts):
                    report.error(f"Forbidden generated or privacy-sensitive archive path: {name}")
                if pure.name in FORBIDDEN_LICENSE_NAMES:
                    report.error(f"Archive contains a license before explicit selection: {name}")
                if pure.suffix.lower() in SENSITIVE_SUFFIXES or pure.name == ".env":
                    report.error(f"Archive may contain credentials or secrets: {name}")
                mode = (entry.external_attr >> 16) & 0o170000
                if mode == 0o120000:
                    report.error(f"Archive contains a symbolic link: {name}")
            if corrupt is not None:
                report.error(f"Archive contains a corrupt entry: {corrupt}")
            if corrupt is None and len(report.errors) == errors_before:
                with tempfile.TemporaryDirectory(prefix="sdp-bootstrap-validate-") as temporary:
                    extracted_root = Path(temporary)
                    archive.extractall(extracted_root)
                    extracted_report = build_report(extracted_root)
                    info["extracted_validation_status"] = (
                        "passed" if not extracted_report.errors else "failed"
                    )
                    info["extracted_errors"] = extracted_report.errors
                    info["extracted_warnings"] = extracted_report.warnings
                    if extracted_report.errors:
                        for error in extracted_report.errors:
                            report.error(f"Extracted archive validation: {error}")
                    if extracted_report.warnings:
                        for warning in extracted_report.warnings:
                            report.warning(f"Extracted archive validation: {warning}")
    except (OSError, zipfile.BadZipFile) as exc:
        report.error(f"Cannot validate archive {archive_path}: {exc}")
    report.archive = info
    report.mark("archive", len(report.errors) == errors_before)


def build_report(root: Path, archive: Path | None = None) -> Report:
    report = Report(root=root.resolve())
    validate_required_files(report)
    units, unit_map = parse_curriculum(report)
    validate_progress(report, units, unit_map)
    validate_learning_paths(report, units, unit_map)
    parse_projects(report, unit_map)
    validate_python_references(report)
    validate_markdown(report)
    validate_template_links(report)
    validate_repository_paths(report)
    validate_canonical_ids(report)
    validate_toml_and_tooling(report)
    validate_terminology(report)
    if archive is not None:
        validate_archive(report, archive.resolve())
    return report


def print_report(report: Report) -> None:
    print(f"SOLID and Design Patterns repository validation: {'PASSED' if not report.errors else 'FAILED'}")
    print()
    for name, result in sorted(report.checks.items()):
        print(f"- {name}: {result}")
    print()
    for name, value in sorted(report.statistics.items()):
        print(f"- {name}: {value}")
    if report.archive:
        print()
        for name, value in sorted(report.archive.items()):
            print(f"- archive.{name}: {value}")
    print("\nManual inspection: not performed by this automated validator")
    for item in MANUAL_INSPECTION_ITEMS:
        print(f"- {item}")
    if report.warnings:
        print("\nWarnings:")
        for warning in report.warnings:
            print(f"- {warning}")
    if report.errors:
        print("\nErrors:")
        for error in report.errors:
            print(f"- {error}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root", type=Path, default=Path(__file__).resolve().parents[1],
        help="Repository root; defaults to the parent of scripts/.",
    )
    parser.add_argument("--archive", type=Path, help="Optional ZIP archive to validate.")
    parser.add_argument("--json", type=Path, help="Write a machine-readable JSON report.")
    args = parser.parse_args()
    report = build_report(args.root, args.archive)
    print_report(report)
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report.as_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0 if not report.errors else 1


if __name__ == "__main__":
    sys.exit(main())
