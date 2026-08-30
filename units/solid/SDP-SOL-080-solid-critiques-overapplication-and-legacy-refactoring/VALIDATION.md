# Maintainer validation — SDP-SOL-080

Date: **2026-08-30**. Artifact state: **Draft**. Learning state: **Not started**.
The [practice](practice/README.md) is **Not attempted**. This record concerns the material,
not Rahul's knowledge, prediction, implementation, interview performance, or retention.

## Scope and provenance

- Exact branch: `topic/SDP-SOL-080`.
- Clean synchronized initialization base: `fbff9a9ad9aced5946076adba9e78a80fc100a4e`.
- No pre-existing topic branch, competing Worktree, or uncommitted work was included.
- Changes are limited to this unit and its matching artifact-state cell in `PROGRESS.md`.
- Canonical IDs, classifications, prerequisites, learning paths, templates, tooling, and
  the next unit remain unchanged.

## Executed checks

| Check | Observed result |
|---|---|
| Baseline repository validator | Passed before initialization. |
| Final repository validator | Passed, including links, metadata, lock consistency, and zero hygiene violations. |
| Unit tests, CPython 3.14.7 | 51 passed. |
| Unit tests, CPython 3.11.16 | 51 passed. |
| Full repository regression, CPython 3.14.7 | 543 passed across 19 units, one pytest process per unit. |
| Strict mypy, Python 3.14 target | No issues in 7 source files. |
| Strict mypy, Python 3.11 target | No issues in 7 source files. |
| Ruff lint and formatting | Passed for the unit. |
| Python 3.11 syntax | All unit Python files parsed with the 3.11 grammar target. |
| Worked demo, lab baseline, and trace probe | Executed successfully on both runtimes. |
| Experiment record | Recorded output matched actual output on both runtimes. |
| Visual data | All 15 embedded observations matched the probe's JSON on both runtimes. |
| Interactive visual | All 10 scenario/candidate combinations passed at 1024, 736, 360, and 320 pixels in both light and dark appearance. |
| HTML navigation links | Both relative targets exist in the unit. |

The first lint pass requested explicit raw regex patterns and sorted imports; both were
corrected. An early test command ran before environment installation finished and could
not import pytest; the completed locked environments produced the results above. No
behaviour check was weakened, skipped, marked expected-failure, or suppressed to get a pass.

## Environment and reproduction

Both environments were synchronized from the unchanged repository lock using
`uv sync --locked --group dev`; the compatibility environment explicitly selected
`--python 3.11`. The actual checks used the resulting environments' Python, pytest, Ruff,
and mypy executables. The [practice guide](practice/README.md#commands) provides equivalent
`uv run --locked` commands and external-cache setup.

Platform: Linux 7.0.0-30-generic, x86_64, glibc 2.43. Tools: pytest 8.4.2,
Hypothesis 6.165.2, mypy 1.20.2, Ruff 0.16.1. Exact interpreter strings are recorded in
[EXP-01](experiments/EXP-01-observable-trace/README.md#environment).

Final environments and caches are outside the repository. The first full regression's
embedded mypy invocation created a cache inside the clean Worktree; that current-operation
cache was moved outside, and the rerun explicitly sets `MYPY_CACHE_DIR`. Bytecode writing and
pytest's cache provider were disabled; Ruff used `--no-cache`. Temporary browser previews and
inspection output were not added to the unit. Pre-existing ignored files in the original
Local checkout were left alone.

For full regression after the guide's environment exports:

```bash
uv run --locked python - <<'PY'
from pathlib import Path
import subprocess
import sys

for unit in sorted(Path("units").glob("*/*")):
    if unit.is_dir():
        subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", str(unit)],
            check=True,
        )
PY
```

Separate processes avoid repeated test-module names in existing units. Python 3.11 testing
was scoped to SDP-SOL-080; repository-wide compatibility was not re-certified.

## Visual verification and limits

The final visual's controls, comparison status, and table/element bounds were checked for
every state at all four widths. No horizontal document overflow or cell/control overflow
was observed. The limitations disclosure was opened successfully. The browser reported no
captured warning or error logs during the checks.

Dark appearance used the browser preference. Light appearance used a temporary copy whose
only source change forced the CSS colour scheme to light. Desktop and phone screenshots
were inspected; the event column and a cramped heading were adjusted. No screen-reader,
complete keyboard, or cross-browser certification is claimed.

The visual contains observations from our Python probe, not an embedded interpreter. The
probe has synthetic names and an in-memory sink. No production device, network writer,
database, concurrent workload, rollout, or performance benchmark was tested.

## Manual content review

- Matched the canonical title, outcome, prerequisite IDs, classifications, time estimates,
  and E+I+D+T evidence profile.
- Included a minimal prerequisite bridge without claiming prior learning.
- Critiqued each SOLID principle without assuming interfaces or inheritance are inherently bad.
- Compared a direct function, a justified extraction, an optional extension boundary, an
  overbuilt implementation, and an incompatible eager rewrite.
- Distinguished result/error agreement from effect order, partial state, and input consumption.
- Retained fixed oracles alongside differential and property-based tests.
- Tested first/later validation failures, source failure, and sink failures before and after
  an effect, including preserved exception identity and the unconsumed iterator tail.
- Kept the independent report lab unsolved, with a separate requested behaviour change,
  no final replacement, and no released hints or fabricated learner review.
- Covered independent reasons to change, compatibility quirks, public extension APIs,
  safe comparison, migration, rollback limits, and a stopping condition.
- Read the listed primary sources and placed important citations near claims. Python
  Mastery links are navigation references, not external lessons claimed as reviewed.
- Included reading directions, insights, and limitations for non-trivial visuals.
- Used original prose, code, and synthetic data; added no license or private material.

## Learning and NotebookLM boundary

Material approval requires coherent, source-checked, runnable artifacts. It does not close
the exercise or advance learning state. The approved unit note may be used in NotebookLM
after approval; this maintainer record, raw test output, progress tracker, learner attempts,
and any future solutions are not an upload bundle.
