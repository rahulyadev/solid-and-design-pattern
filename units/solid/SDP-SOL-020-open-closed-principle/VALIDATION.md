# Artifact validation — SDP-SOL-020

This is a maintainer record, not a learner review. The separate practice remains **Not attempted**;
no prediction, implementation attempt, recall, teach-back, or mastery evidence is attributed to Rahul.

## Scope and baseline

Only this unit directory and the `SDP-SOL-020` artifact-state cell in `PROGRESS.md` are changed.
Initialization began in a dedicated clean Worktree on exactly `topic/SDP-SOL-020`, from synchronized
`main` and `origin/main` at `ecfba99a5da9ba1c0223081d6c8ff07b0cba3e70`.
The exact local and remote topic refs were absent, and clean status was confirmed before recording
that commit as `INIT_START`. No pre-existing work was included or rewritten.

## Checks recorded on 2026-08-30

| Check | Observed result |
|---|---|
| Clean baseline repository validation | Passed, including `uv lock --check` |
| Repository validation with the complete unit | Passed, including Markdown, links, metadata, hygiene, and lock consistency |
| Locked development environment | `uv sync --locked --group dev` succeeded in an external environment using CPython 3.14.7 |
| Focused unit tests | 66 passed on CPython 3.14.7; no skips or expected failures |
| Focused Ruff lint | All checks passed |
| Strict mypy | Success; no issues in 9 Python source files |
| Python 3.11 compatibility | 66 passed on CPython 3.11.16; strict mypy with `--python-version 3.11` also passed |
| Note examples | All four Python blocks executed successfully on both interpreters |
| Entry points | Teaching demo, practice starter, and registry experiment completed; output was identical across both Python versions |
| Regression tests | All 13 initialized units ran in separate processes: 256 passed, no failing groups |
| Formatting | Ruff format check passed for applicable unit files |
| Interactive behavior | All four requirement choices updated the three design rows; no browser warnings or errors were observed |
| Responsive appearance | 32 combinations checked: four requirements, 1060/736/360/320 px widths, and light/dark appearances; no remaining overflow |
| Visual correction | A 4 px narrow-screen role-label overflow was found and fixed; the affected layout was rechecked |

## Reproduction and environment

Use the external environment exports and commands in the [practice guide](practice/README.md#commands).
The locked tools used here are pytest 8.4.2, Ruff 0.16.1, mypy 1.20.2, and Hypothesis 6.165.2.
Python 3.11 testing used a separate external environment installed from the same lockfile,
selecting the already-installed Python 3.11 interpreter explicitly with uv's `--python` option.

Bytecode writing and pytest's cache provider were disabled. Ruff used `--no-cache`; final checks
use external mypy, Hypothesis, and uv caches. One early regression subprocess created a mypy cache
inside this task's initially clean Worktree; that task-created cache was removed and regression
was repeated with an external mypy cache. The strict repository validator scans
ignored paths too: the initial direct check in the original local checkout reported its pre-existing
environments/caches and a uv cache permission failure. Those files were not deleted, and the
validator was not weakened. The clean Worktree baseline passed with a writable external uv cache.

Existing units contain duplicate test module names, so regression runs each unit in its own pytest
process. No unit or test is excluded. With the practice environment exports applied, the equivalent
regression command is:

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

Browser inspection covered the visible labels, all requirement choices, responsive boundaries,
and both appearances. Dark narrow-screen and light tablet layouts were also inspected as images.
A temporary forced-light copy was removed after QA. Native keyboard focus reached the select,
but changing its option by arrow key was not confirmed through the automation surface; no full
keyboard or accessibility audit is claimed.

## Manual artifact review

- Matched the canonical title, outcome, prerequisites, priority, depth, scope, estimates, and evidence profile.
- Kept the notebook core concise, with change pressure before terminology and reconstruction cues.
- Compared a direct conditional, data variation, callables, callable objects, registration, and speculative overengineering.
- Distinguished runtime calls from source imports, a stable implementation from stable output,
  and a compatible extension from a revised shared contract.
- Reviewed duplicate and missing names, callback exception boundaries, partial writer effects,
  mapping ownership, and the limit of static type checking.
- Explicitly noted that the two demo APIs have different selection/error interfaces; migration
  must preserve an old facade's promises where callers depend on them.
- Checked each non-trivial visual's reading guide, insight, and limitation.
- Opened the cited primary sources; identified historical attribution through Martin's account.
- Used original explanations, diagrams, code, and synthetic data. No external code, private data,
  credentials, new license, copied book diagram, or unrelated artifact is included.
- Kept the queue exercise and its future acceptance tests unsolved. Its green tests characterize
  only existing behavior. No hints, answer keys, learner review, or evidence dates were invented.

## Artifact and learning state

The initialization artifact is Draft. The explicit publication request permits a separate final
artifact approval after validation; it does not establish learner completion. Learning state remains
Not started, with no change to evidence dates or other unit rows. `SDP-SOL-030` is referenced as the
next unit but is not initialized by this operation.
