# Artifact validation — SDP-SOL-030

Maintainer verification only. Rahul has not supplied a prediction, lab attempt, teach-back,
closed-book recall, or transfer answer. Practice remains **Not attempted**; learning remains
**Not started**, with no invented evidence dates or weaknesses.

## Scope and initialization baseline

Only this unit directory and the `SDP-SOL-030` artifact-state cell in `PROGRESS.md` are changed.
The topic work used a dedicated clean Git Worktree on exactly `topic/SDP-SOL-030`.
Local `main`, `origin/main`, and the starting checkout were synchronized at
`5bafe232678adb3801c6a707c121ff1aa6887ca0`. The exact local and remote topic refs were absent.
Clean porcelain status was checked before recording that commit as `INIT_START`.
No pre-existing tracked, staged, untracked, or local-only learning work was included or rewritten.

Initialization commit `160854774a74ccf54131b264ebf1d1edcb96d587` recorded the required Draft state.
The same user request explicitly authorized finalization, latest-change publication, a checked
merge, and returning the main checkout to synchronized `main`. Artifact approval is the separate
finalization change after the checks below; it is not a claim of completed learning.

## Checks observed on 2026-08-30

| Check | Observed result |
|---|---|
| Clean baseline repository validator | Passed, including lock consistency |
| Validator with complete initialized unit | Passed, including Markdown, links, IDs, metadata, and filesystem hygiene |
| Locked development environment | `uv sync --locked --group dev` succeeded in an external environment |
| Canonical Python unit tests | 75 passed on CPython 3.14.7; no skips or expected failures |
| Python 3.11 compatibility | 75 passed on CPython 3.11.16 using the same lockfile |
| Strict mypy | No issues in 9 Python source files, with both 3.14 and 3.11 targets |
| Ruff lint | All checks passed |
| Ruff formatting | Check passed for applicable unit files |
| Note snippets | All four Python blocks executed successfully on both interpreters |
| Entry points | Catalog demo, reservation starter, and both experiments completed with identical output on both interpreters |
| Static negative-control experiment | Wrong arity rejected with an assignment diagnostic; wrong numeric meaning accepted, then exposed by a value test |
| Full existing-unit regression | 331 passed across all 14 initialized units, in separate pytest processes |
| Initial visual/Python comparison | All 30 provider/call outcomes matched actual Python outputs |
| Responsive visual states | 240 checked: 6 providers × 5 calls × 4 widths × 2 appearances; no horizontal overflow, clipped checked text, or out-of-viewport content |
| Pointer interaction | Provider reset, next/previous navigation, and disabled end controls verified |
| Browser console | No warnings or errors observed in the completed visual checks |
| Diff whitespace | `git diff --check` and staged diff check passed |

## Reproduction and environment

Use the external-cache exports and commands in the [practice guide](practice/README.md#commands).
The canonical run used Linux x86_64, CPython 3.14.7, pytest 8.4.2, Ruff 0.16.1, mypy 1.20.2,
and Hypothesis 6.165.2. The Python 3.11 run used its own external virtual environment and mypy
cache, selecting the already-installed CPython 3.11.16 explicitly through uv's `--python` option.
`--no-sync` was used for repeated uv runs after successful locked synchronization.

Bytecode writing and pytest's cache provider were disabled. Ruff used `--no-cache`; uv, mypy,
and Hypothesis caches stayed outside the Worktree. The initial dependency download was blocked
by sandbox networking; a permitted retry completed. The validator was not weakened, and no
pre-existing user environment or cache was removed.

Existing units reuse some test-module names. Full regression ran each unit in its own process,
without excluding any unit or test. With the external environment exports applied, reproduce it
from the repository root with:

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

The responsive widths were 1024, 736, 360, and 320 pixels. Dark checks used the system appearance;
light checks used a temporary copy forcing only the light CSS branch and native colour scheme.
That copy was removed before the initialization commit. Selected dark/mobile and light/tablet
screenshots were inspected. Browser viewport overrides were restored after testing.

Native keyboard focus reached the next button, but arrow-key selection and Enter activation
were not confirmed through the automation surface. A subsequent previous-button test found it
disabled because the call had not advanced. Pointer next/previous behaviour was then checked
successfully. No full keyboard, screen-reader, or accessibility audit is claimed.

## Manual artifact review

- Matched the exact canonical title, outcome, prerequisites, scope, depth, estimates, and evidence
  profile; no curriculum classification, prerequisite, order, or project scope was changed.
- Kept a reconstruction-oriented notebook core before formal mechanics and verified history.
- Compared direct lookup, a callable seam, a structural protocol, honest adapters, separate
  capabilities, and an overengineered universal hierarchy.
- Covered preconditions, postconditions, result values, documented errors, failure effects,
  invariants, history, aliases, constructor boundaries, and input/output variance.
- Distinguished behavioural compatibility, static member matching, runtime presence checks,
  and ordinary Python object identity. Made no invented CPython-internals claims.
- Demonstrated two conforming catalog representations and four explicit counterexamples.
  Shared contract tests certify the admitted examples in their tested scope; witness tests
  deliberately reproduce the other candidates' violations.
- Preserved an unsolved reservation lab. Its baseline tests are green, but its partner candidate
  remains intentionally defective for learner diagnosis; no repair or acceptance answer key is
  supplied. This intentional exercise defect is not a failed production-code test being bypassed.
- Included a real-capability limitation in the transfer exercise: a wrapper cannot simply promise
  rollback for an external provider that cannot support it.
- Supplied reading guides, insights, and limitations for the teaching visuals and evidence maps.
- Opened the cited primary sources. Cross-repository Python links are labeled as prerequisite
  references, not material read as sources for this unit.
- Used original prose, synthetic examples, and code-native visuals. No copied book diagram,
  private data, credentials, solution transcript, new license, or unrelated artifacts are included.
- Kept NotebookLM boundaries unchanged: the approved note is suitable input; this maintainer
  record, raw attempts, progress tracker, and source tree are not an upload bundle.

## Publication and learning boundary

Finalization marks only the artifact Approved. Learning state, evidence dates, review dates,
weaknesses, and other unit rows remain unchanged. `SDP-SOL-040` remains uninitialized.
No claim is made that Rahul completed practice or demonstrated LSP merely because this topic
can be published and merged. The final task report carries the exact publication commits,
pull request, merge result, and synchronization state.
