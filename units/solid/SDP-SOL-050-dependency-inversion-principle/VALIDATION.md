# Artifact validation — SDP-SOL-050

Maintainer verification only. No learner prediction, practice attempt, teach-back, delayed
recall, or transfer answer was supplied. Practice remains **Not attempted** and learning
remains **Not started**. No learner evidence date, review date, or personal weakness is invented.

## Scope and initialization baseline

Only this unit directory and the `SDP-SOL-050` artifact-state cell in `PROGRESS.md` change.
The exact topic branch is `topic/SDP-SOL-050`, created in a dedicated clean Git Worktree.
Local `main`, refreshed `origin/main`, and the Worktree's initial commit all identified
`2e33d9c8a21615baf3ca3ea7246e59f92025b574`.
The exact local and remote topic refs were absent before branch creation.

Porcelain status produced no output before that commit was recorded as `INIT_START`.
No pre-existing tracked, staged, untracked, or local-only learning work was included or
rewritten. The original main checkout's ignored environments and caches were preserved.
Its initial validation failed filesystem hygiene and could not write to the default uv
cache. The clean topic Worktree passed using an external writable cache, without changing
the validator or removing the existing files.

Initialization commit `a6e22155d9c201454cd1ceb906c2fcc52c9fb570` records Draft material.
The user's explicit publication request also authorizes final checks, latest-change push,
pull-request creation, checked merge, and main synchronization. Approval of this material
does not establish completion of the learning unit.

## Checks observed on 2026-08-30

| Check | Observed result |
|---|---|
| Clean baseline repository validator | Passed, including uv lock consistency |
| Initialized-unit repository validator | Passed, including IDs, links, Markdown, tracker parity, hygiene, and lock consistency |
| Locked environments | Synchronized separately for CPython 3.14.7 and 3.11.16 |
| Canonical unit tests | 34 passed, without skips or expected failures |
| Python 3.11 compatibility | The same 34 tests passed with the same lockfile |
| Strict mypy | No issues in 12 source files with both 3.14 and 3.11 targets |
| Ruff lint | All checks passed |
| Ruff format | All applicable Python and Markdown files passed the format check |
| Note snippets | All 3 Python blocks executed successfully on both interpreters |
| Entry points | Replenishment demo, workshop starter, and import probe ran on both interpreters |
| Import experiment | Concrete import reached the blocked driver; inverted policy ran with the supplied fake |
| Full regression | 408 passed across all 16 initialized units, one pytest process per unit |
| Visual states and responsive layout | 32 checks passed: 4 states × 4 widths × 2 appearances |
| Browser console | No warnings or errors observed during visual checks |
| HTML links | All 3 local link targets exist in the repository |
| Diff whitespace | Unstaged and staged checks passed |

The initial lint pass found one nested-context-manager simplification in a test; it was
corrected. The initial format pass changed the probe's multiline string quoting. No test,
type-check, lint, or validation failure was suppressed. The compatibility invocation was
made explicit with `--python` so the repository's canonical interpreter pin did not produce
a misleading environment-selection warning.

## Environment and reproduction

Use the exports and commands in the [practice guide](practice/README.md#commands).
The canonical environment was Linux 7.0.0-30-generic x86_64, glibc 2.43, CPython 3.14.7,
pytest 8.4.2, mypy 1.20.2, Ruff 0.16.1, and Hypothesis 6.165.2.
The separate compatibility environment used CPython 3.11.16.

Both environments used `uv sync --locked --group dev`; compatibility synchronization also
selected the installed Python 3.11 interpreter. Compatibility runs used that interpreter
and `mypy --python-version 3.11`. Repeated runs used `--no-sync` only after synchronization.
Bytecode writing and pytest's cache provider were disabled. uv, mypy, Hypothesis, and tool
environments were outside the Worktree; Ruff used `--no-cache`.

The runnable experiment records its exact output and controls in its
[experiment note](experiments/EXP-01-import-isolation/README.md). No performance benchmark,
external database, real partner service, or framework lifecycle was tested.

Existing units reuse some test-module names. Run full regression in separate pytest
processes after applying the practice exports:

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

## Visual review and limits

Every combination of concrete/contract design and source/runtime view was checked at
1024, 736, 360, and 320 pixels. Checks covered selected state, node labels, arrow direction,
horizontal overflow, and checked elements extending outside the viewport.

Dark appearance used the browser's existing system appearance. Light appearance used a
temporary copy that changed only `color-scheme: light dark` to `color-scheme: light`.
The copy was removed before staging. Desktop dark and phone light screenshots were inspected.
The viewport override was restored and the temporary tab closed after testing.

Native labeled selects worked in all tested states. This is not a full keyboard,
screen-reader, browser-compatibility, or accessibility audit. The visual is a conceptual
model; Python behaviour is established by the separate executable example and experiment.

## Manual artifact review

- Matched the canonical title, outcome, prerequisites, dimensions, estimates, and evidence
  profile. No curriculum, learning-path, project, template, workflow, or validator policy changed.
- Kept a concise notebook core and a prerequisite bridge without assuming earlier notes prove learning.
- Distinguished source dependencies, runtime calls, structural conformance, injection, IoC,
  service location, and framework-managed wiring.
- Explained policy-owned vocabulary, transitive imports, vendor data/error leakage, and the
  composition root without requiring an inheritance hierarchy or dependency container.
- Compared direct data, a callable, a Protocol, a concrete injected counterexample, and
  overengineering. Documented snapshot, lifecycle, error, and per-item-query limits.
- Tested nonnegative and unknown stock, invalid targets before I/O, empty input, Unicode,
  quoted keys, non-mutation, partial failure, malformed storage data, and closed-resource misuse.
- Kept the independent workshop exercise unsolved, with no hints released or learner answer
  invented. Baseline tests do not claim to implement the new partner requirement.
- Included reading directions, key insights, and limitations for the diagrams and visual.
- Read primary sources for the formal and subtle claims; Python Mastery links remain
  navigation references, not sources claimed to have been studied by Rahul or read here.
- Used original prose, code, synthetic records, and code-native visuals. No new license,
  copied book diagrams, private data, credentials, caches, or raw transcripts are included.
- Preserved NotebookLM boundaries: approved notes may be used; this record, progress,
  raw attempts, and whole source trees are not an upload bundle.

## Publication and learning boundary

Finalization marks the reviewed material Approved while preserving every learning/evidence
field. `SDP-SOL-060` remains absent and uninitialized. The final task report records the
publication commits, pull request, merge result, synchronized main, and any remaining local work.
