# Artifact validation — SDP-SOL-010

This is a maintainer's artifact record, not a learner review. The practice is **Not attempted**;
no prediction, implementation, teach-back, or mastery evidence is attributed to Rahul.

## Scope

Only this unit directory and the `SDP-SOL-010` artifact-state cell in `PROGRESS.md` are changed.
The unit was initialized from synchronized `main` at
`a7e78e232ac9bc0979999bb140a5b0577d3600b6`, with clean status before `INIT_START`.

## Checks recorded on 2026-08-30

| Check | Observed result |
|---|---|
| Clean baseline repository validation | Passed, including `uv lock --check` |
| Locked development environment | CPython 3.14.7; `uv sync --locked --group dev` succeeded outside the repository |
| Focused unit tests | 43 passed; no skips or expected failures |
| Teaching and starter runners | Both completed successfully with synthetic data |
| Failure experiment | Mixed and split observations agree; partial effects and duplicate retry recorded in the experiment note |
| Focused Ruff lint | All checks passed |
| Focused strict mypy | Success; no issues in 6 Python source files |
| Repository validation with the unit present | Passed, including Markdown links, metadata, hygiene, and lock consistency |
| Regression coverage | All 12 initialized unit suites ran separately: 190 passed, no failing groups |
| Python 3.11 compatibility | 43 passed on CPython 3.11.16; strict mypy with `--python-version 3.11` also passed |
| Entry points across versions | All three runners produced identical successful output on CPython 3.14.7 and 3.11.16 |
| Note examples | All four Python blocks executed; notebook examples and before/after publication outcomes checked |
| Formatting | Ruff format check passed for all applicable unit files |
| Interactive visual | All 12 requirement/structure selections checked; no browser warnings or errors observed |
| Responsive visual | 1060, 736, 360, and 320 px viewport checks; no horizontal overflow in the inspected layouts |
| Appearance | Dark appearance and a temporary forced-light copy inspected; QA copy removed |

The local artifact review is complete. The validated initialization commit `01d2cd8` recorded
Draft as required by the workflow. The separately requested finalization marks the material
Approved for publication on 2026-08-30. Learning state remains Not started; approval does not
represent completion of the learner exercises.

## Environment and reproducibility

The locked tools are pytest 8.4.2, Ruff 0.16.1, mypy 1.20.2, and Hypothesis 6.165.2. The initial
test command used `uv run --locked --no-sync pytest -q -p no:cacheprovider` followed by this unit's
path. Ruff used `check --no-cache`; mypy used its repository strict configuration. Final checks
used external caches or disabled caching. Ruff and mypy caches created during earlier checks in
this task's clean Worktree were removed; no pre-existing local-checkout caches were deleted.

Use the [practice commands](practice/README.md#commands) to reproduce validation. The original
local checkout contains pre-existing ignored environments and caches; its direct hygiene run
reported those artifacts. They were left untouched. Validation is performed in a clean isolated
Worktree with external development tooling, not by weakening the validator or ignoring failures.

A single repository-wide pytest invocation encountered pre-existing duplicate module names:
`test_runtime_experiments.py` in `SDP-FND-050` and `SDP-FND-090`. Regression verification therefore
ran every initialized unit in a separate pytest process, with no tests excluded. This collection
limitation in older units is unchanged. After the environment exports from the practice guide,
the equivalent regression command is:

```bash
uv run --locked python - <<'PY'
from pathlib import Path
import subprocess
import sys

for unit_dir in sorted(Path("units").glob("*/*")):
    if unit_dir.is_dir():
        subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", str(unit_dir)],
            check=True,
        )
PY
```

The browser check covered selection-driven changes, visible labels, layout, and both appearances.
Keyboard-only selection was not confirmed through the automation surface; the page retains native
labeled selects, and no complete accessibility audit is claimed.

## Manual artifact review

- Checked the exact curriculum outcome, prerequisites, metadata, and evidence profile.
- Checked change-pressure-first teaching, a compact notebook core, participants, call flow,
  formal meaning, Python mechanics, counterexamples, and limits of the proposed boundaries.
- Reviewed the distinction between a direct implementation edit and a changed result consumed
  by otherwise stable code; the visual also shows a legitimate shared-contract change.
- Opened the cited primary sources. The prose, diagrams, domains, and code are original; no
  book example, proprietary content, credentials, new license, or unrelated files are included.
- Checked that the working parcel example does not complete the separate workshop exercise.
- Checked that the supplementary experiment preserves the canonical E+I+D+T evidence profile
  and does not imply database, delivery, concurrency, or performance guarantees.
- Checked that each non-trivial visual includes a reading guide, insight, and limitation.

## Exercise and publication boundaries

- The parcel example is solved teaching material in a different domain.
- The workshop preview and policy-change exercise remains unsolved. Its original characterization
  suite passes, but its new acceptance tests and refactoring remain learner work.
- The experiment records actual maintainer output and states its limits.
- No learner `REVIEW.md`, evidence date, learning transition, or mastery badge is fabricated.
- Publication is explicitly authorized for this task. The exact topic branch is
  `topic/SDP-SOL-010`; `SDP-SOL-020` is not initialized by this operation.
