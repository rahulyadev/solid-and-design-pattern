# Maintainer validation — SDP-SOL-070

Validation date: **2026-08-30**. This records artifact review and maintainer execution,
not Rahul's learning, practice, recall, interview, or mastery evidence.

## Scope and provenance

- Exact branch: `topic/SDP-SOL-070`, created in a dedicated clean Worktree.
- Synchronized main baseline and `INIT_START`: `172450a75daaafa55e0be7e63b231cc2635b5c3e`.
- Initialization commit: `ec0a5fa7811ed0f9d1ae2ba023693719909e31d3`.
- Initialization set the artifact to Draft. Finalization approves the reviewed material.
- Changes are limited to this unit folder and its one `PROGRESS.md` artifact-state cell.
- Learning stays **Not started**; evidence dates, weaknesses, and evidence links stay unchanged.
- `SDP-SOL-080` is untouched and uninitialized. No curriculum, project, template, workflow,
  dependency, validator, or license policy changed.

The user's explicit publication request authorizes the final push, pull request, checked
merge, and main synchronization. Publication identifiers and results belong in the final
task report; this record does not anticipate a successful remote action.

## Executed checks

| Check | Observed result |
|---|---|
| Repository validator | Passed, including lock consistency, Markdown, links, IDs, progress parity, and hygiene |
| Unit tests on CPython 3.14.7 | 39 passed |
| Unit tests on CPython 3.11.16 | 39 passed |
| Type checking | Passed for 13 Python source files on both target versions |
| Ruff lint and format | Passed on the unit's applicable files |
| Worked example and practice starter | Both ran on both interpreters |
| Runtime experiments | Both ran on both interpreters; recorded outputs agree |
| Runnable note excerpts | All 4 Python excerpts executed successfully on both interpreters |
| Full regression on CPython 3.14.7 | 492 tests passed across 18 units, using one pytest process per unit |
| Responsive visual states | 40 checks passed: 5 scenarios × 4 widths × 2 appearances |
| Browser console during visual checks | No warnings or errors observed |
| HTML and JavaScript | 17 unique IDs, 4 distinct local links exist, JavaScript syntax check passed |
| Staged initialization whitespace | Passed after removing four extra final blank lines |

Initial lint found two overlong Python lines; formatting corrected them. The staged diff
found extra blank lines at the end of four Markdown files; those were removed before commit.
No source, test, static-check error, or repository check was suppressed or bypassed.

## Environment and reproduction

The [practice guide](practice/README.md#commands) contains external-environment setup and
commands for examples, experiments, tests, lint, formatting, typing, and the validator.
The canonical and compatibility environments were installed separately from the repository
lock with `uv sync --locked --group dev`; the compatibility setup explicitly selected 3.11.
Subsequent `--no-sync` runs reused those already synchronized environments.

Both used Linux 7.0.0-30-generic, x86_64, glibc 2.43; pytest 8.4.2, mypy 1.20.2,
Ruff 0.16.1, and Hypothesis 6.165.2. Runtime versions were CPython 3.14.7 and 3.11.16.
Each experiment records its exact version strings. Compatibility typing explicitly used
`mypy --python-version 3.11`.

Environments, uv/mypy/Hypothesis caches, and temporary inspection files remained outside
committed content. Bytecode writing and pytest's cache provider were disabled; Ruff used
`--no-cache`. The exact temporary light-appearance HTML copy was removed before staging.
Pre-existing ignored files in the original Local checkout were preserved.

For full regression, after the guide's environment exports:

```bash
uv run --locked --no-sync python - <<'PY'
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

Separate processes avoid existing units' repeated test-module names. Full regression used
the canonical interpreter; the Python 3.11 regression was scoped to this unit.

## Visual review and limitations

All five scenarios were selected at 1024, 736, 360, and 320 pixels in dark and light appearance.
Checks verified selection, the displayed mechanism title, absence of horizontal document
overflow, and relevant element bounds. Code disclosure was opened with a click for these
checks. Desktop dark and phone light viewport screenshots were visually inspected.

Dark appearance used the browser's current preference. Light appearance used a temporary
copy with only its colour-scheme declarations changed. Synthetic keyboard presses did not
change the native selector or disclosure state in this browser session; keyboard operation
is therefore unconfirmed. No complete accessibility or cross-browser certification is claimed.

The visual contains predetermined examples, not an embedded Python runtime. The probes
exercise standard-library behaviour, not CPython memory internals. No real kiosk, catalogue,
external provider, connection, thread, or performance benchmark was used.

## Manual content review

- Matched the canonical title, outcome, prerequisites, classifications, estimates, and E+I+D+T profile.
- Supplied a minimal prerequisite bridge without inventing evidence of prior learning.
- Compared a direct function, passed callable, closure, configured instance, named Protocol,
  compatible module, explicit data, and a justified optional ABC family.
- Separated source imports from runtime calls and structural conformance from behavioural promises.
- Kept the policy independent of concrete layout imports; providers need not inherit or import its Protocol.
- Covered blank input before rendering, exact spelling, Unicode, JSON escaping, matching metadata,
  blank results, visible failures, order, duplicates, and independent callable configuration.
- Kept the separate catalogue exercise unsolved, including its new source, hints, and comparison solution.
- Preserved a concrete starter and characterization tests, including empty-title behaviour.
- Recorded actual experiment environments, outputs, interpretations, and limits.
- Read the listed primary sources; Python Mastery links are navigation references only.
- Included reading directions, key insights, and limitations for non-trivial visuals.
- Used original prose, code, and visuals with synthetic data; added no license or private material.

## Learning and NotebookLM boundary

Approval means the material is coherent, source-checked, and runnable. It does not close
the exercise or advance a learning state. Rahul's actual attempt and reasoning remain required.
The approved unit note is an eligible NotebookLM input; this maintainer record, progress
tracker, raw attempts, solutions, and test output are not an upload bundle.
