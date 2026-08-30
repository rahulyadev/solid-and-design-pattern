# Artifact validation — SDP-SOL-040

Maintainer verification only. No learner prediction, practice attempt, teach-back, recall,
or transfer answer was supplied. Practice remains **Not attempted** and learning remains
**Not started**, with no invented evidence date, review date, or personal weakness.

## Scope and initialization baseline

Only this unit directory and the `SDP-SOL-040` artifact-state cell in `PROGRESS.md` change.
The exact topic branch is `topic/SDP-SOL-040`, in a dedicated clean Git Worktree.
Local `main`, refreshed `origin/main`, and the starting Worktree all identified
`2f9ea995bb83468bb423542406bdae34e4419773`.
The exact local and remote topic refs were absent before creation.

Porcelain status produced no output before that commit was recorded as `INIT_START`.
No pre-existing tracked, staged, untracked, or local-only learning work was included or
rewritten. The Local checkout's existing ignored environments and caches were preserved.
They caused its initial filesystem-hygiene validation to fail; the clean topic baseline
passed without changing the validator.

The initialization records Draft. The user separately authorized finalization, latest-change
publication, a checked merge, and synchronizing the main checkout. Approval of the material
after review is distinct from completion of learning.

## Checks observed on 2026-08-30

| Check | Observed result |
|---|---|
| Clean baseline repository validator | Passed, including uv lock consistency |
| Locked tool environments | Synchronized successfully for CPython 3.14.7 and 3.11.16 |
| Canonical unit tests | 43 passed; no skips or expected failures |
| Python 3.11 compatibility | The same 43 tests passed with the same lockfile |
| Strict mypy | No issues in 8 source files with both 3.14 and 3.11 targets |
| Ruff lint | All checks passed |
| Note snippets | All 4 Python blocks executed on both interpreters |
| Entry points | Archive demo, station starter, and dependency experiment ran on both interpreters with identical output |
| Contract-growth experiment | Accepted / rejected for unused members / accepted, while all actual calls returned hello |
| Type matrix | All 24 client/contract/provider combinations checked by mypy: 10 accepted, 14 rejected |
| Full regression | 374 passed across all 15 initialized units, one pytest process per unit |
| Visual scenarios and layout | 192 checks passed: 24 combinations × 4 widths × 2 appearances |

The initial strict check flagged a direct identity comparison between two protocol-typed
references as non-overlapping. The demo now compares both references with the actual provider
object; the runtime observation is unchanged and no diagnostic is suppressed. The initial
format check found one formatting change; Ruff applied it.

## Environment and reproduction

Use the external-environment exports and commands in the [practice guide](practice/README.md#commands).
The canonical environment was Linux 7.0.0-30-generic x86_64, glibc 2.43, CPython 3.14.7,
pytest 8.4.2, mypy 1.20.2, Ruff 0.16.1, and Hypothesis 6.165.2.
The compatibility run used a separate environment with CPython 3.11.16 and
`mypy --python-version 3.11`. Both environments used `uv sync --locked --group dev`;
the second selected the installed Python 3.11 interpreter explicitly.

Repeated runs used `--no-sync` only after synchronization completed. Bytecode writing
and pytest's cache provider were disabled. Ruff used `--no-cache`; uv, mypy, Hypothesis,
temporary source probes, and tool environments lived outside the Worktree.
Network access was approved for locked dependency installation and GitHub access.

Existing units reuse some test-module names. No units were excluded: run regression in
separate pytest processes from the repository root after applying the practice exports:

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

For the type matrix, each provider was assigned to the actual shared or client-specific
protocol for every visual selection. Diagnostics matched precisely the expected rejected
assignments; no unrelated diagnostic was accepted as evidence of the intended failure.

## Visual review and limits

The interactive map was checked at widths 1024, 736, 360, and 320 pixels. Every selection
was checked for its verdict, operation table, horizontal overflow, clipped checked elements,
and elements outside the viewport. Dark mode used the system appearance. Light mode used
a temporary copy changing only the dark CSS condition and native color scheme; the copy
was removed before committing.

Desktop dark and phone light screenshots were inspected. Full-page phone capture failed;
a bounded screenshot succeeded. The automated native arrow/Tab actions did not confirm
selection change or focus advance. Semantic selection controls worked for all combinations.
No complete keyboard, screen-reader, or accessibility audit is claimed. The browser viewport
override was reset after testing.

## Manual artifact review

- Matched the exact canonical title, outcome, prerequisites, dimensions, estimates, and evidence
  profile. No curriculum, learning-path, project, workflow, template, or validation policy changed.
- Kept a short notebook core, a simple prerequisite bridge, change pressure, participants,
  collaboration, mechanics, alternatives, and production limitations.
- Compared direct data access, a callable, client protocols, a combined capability, and
  unjustified nominal fragmentation without forcing an interface onto every function.
- Distinguished client contracts from provider decomposition, static assignability, runtime
  method availability, module imports, access control, lifecycle, and state guarantees.
- Verified original source material near formal and subtle claims. Python Mastery links are
  navigation references, not sources claimed to have been read.
- Kept practice unsolved, hints unreleased, and the teaching example separate. Baseline tests
  do not claim to implement or certify the new partner requirement.
- Included empty data, missing keys, Unicode, replacement, repeated deletion, copy failure,
  snapshot ownership, invalid intervals, and an uncertain remote-outcome transfer scenario.
- Supplied reading directions, key insights, and limitations for the non-trivial visuals.
- Used original prose, synthetic data, and code-native visuals; no copied book diagrams,
  credentials, private transcripts, new license, or unrelated generated output is included.
- Preserved NotebookLM boundaries: approved notes may be used; progress, raw attempts,
  maintainer logs, and source trees are not a prepared upload bundle.

## Publication and learning boundary

Artifact approval changes no learning-state or evidence field. `SDP-SOL-050` remains absent
and uninitialized. The final task report records the exact initialization/finalization commits,
pull request, checked merge, and synchronized main result.
