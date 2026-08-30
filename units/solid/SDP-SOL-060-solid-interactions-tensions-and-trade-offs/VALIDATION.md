# Maintainer validation — SDP-SOL-060

Validation date: **2026-08-30**. This is artifact evidence, not Rahul's practice, recall,
interview, or mastery evidence. Practice remains unsolved and learning remains **Not started**.

## Scope and branch provenance

- Exact branch: `topic/SDP-SOL-060`, created in a dedicated clean Worktree.
- Synchronized baseline and `INIT_START`: `14ec3516d6a00d0df048231f209699ba26492bc7`.
- Initialization commit: `78cea0af22b1924d240188bf2848005102db3f8c`.
- Initial artifact state was Draft. Finalization approves reviewed material only.
- Changes are limited to this unit folder and its one `PROGRESS.md` artifact-state cell.
- `SDP-SOL-070` is untouched and uninitialized. No curriculum, project, workflow, template,
  dependency, license, or validation policy changed.

The user's explicit publication instruction authorizes the final push, pull request, checked
merge, and main synchronization. The final task report records the publication commit,
pull request, merge commit, and resulting branch state; this file does not anticipate them.

## Executed checks

| Check | Observed result |
|---|---|
| Repository validator | Passed, including `uv lock --check`, Markdown, links, IDs, progress parity, and hygiene |
| Unit tests on CPython 3.14.7 | 45 passed |
| Unit tests on CPython 3.11.16 | 45 passed |
| Type checking | Passed for 11 Python source files on both target versions |
| Ruff lint and format | Passed on the unit's applicable files |
| Worked report and practice starter | Both ran successfully on both runtimes |
| Runtime experiments | Both ran on both runtimes; outputs agree with their experiment notes |
| Full regression on CPython 3.14.7 | 453 tests passed across 17 initialized units, one pytest process per unit |
| Visual state and layout | 40 checks passed: 5 states × 4 widths × 2 appearances |
| Browser console during visual checks | No warnings or errors observed |
| HTML and JavaScript | 4 local links exist, 16 unique element IDs, JavaScript syntax check passed |
| Diff whitespace | Working and staged diff checks passed before initialization commit |

Initial lint found a regex that needed an explicit raw-string marker. Formatting adjusted
two assertions/signatures in a test file. The mobile visual initially rotated full-width
arrow containers; giving them a bounded square fixed their layout. Checks were rerun.
No test, static error, repository check, or branch protection was suppressed or bypassed.

## Environment and reproduction

Use the exports and commands in the [practice guide](practice/README.md#commands).
Both development environments were synchronized with `uv sync --locked --group dev`.
The compatibility environment additionally selected the installed Python 3.11 interpreter.
Later `--no-sync` invocations reused those already synchronized environments.

Canonical environment: Linux 7.0.0-30-generic x86_64, glibc 2.43; CPython 3.14.7;
pytest 8.4.2; mypy 1.20.2; Ruff 0.16.1; Hypothesis 6.165.2.
Compatibility environment: CPython 3.11.16, the same locked tools, with
`mypy --python-version 3.11`. Script smoke runs were first made with the system's CPython
3.14.4, then repeated with the two explicit environments listed in the table.

Virtual environments, uv/mypy/Hypothesis caches, temporary reports, and visual QA files were
outside committed content. Bytecode writing and pytest's cache provider were disabled;
Ruff used `--no-cache`. A temporary light-theme HTML copy was removed before staging.

The initial Local-checkout validator encountered pre-existing ignored environments/caches
and an unwritable default uv cache. Those Local files were preserved. The clean topic
Worktree passed using an external tool environment; no hygiene rule was weakened.

For full regression, after applying the practice exports:

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

Existing units reuse test-module names, so separate pytest processes avoid import collisions.
Full regression was run on the canonical interpreter; the Python 3.11 run was scoped to this unit.

## Visual review and limitations

Each scenario was selected at 1024, 736, 360, and 320 pixels in both dark and light appearance.
Checks confirmed selected scenario, title, before/after responsibility labels, horizontal
overflow, and inspected element bounds. Desktop dark and phone light viewport screenshots
were visually inspected. The final viewport override was reset and the temporary tab closed.

Dark appearance used the browser's current system preference. Light appearance used a
temporary copy with only the colour-scheme setting changed. Native selector state changes
were exercised through the browser's selection API. Synthetic keyboard attempts did not
change the native selector in this browser session, so keyboard operation was not confirmed.
No full accessibility, screen-reader, or cross-browser certification is claimed.

The diagrams are conceptual. The quota schedule does not test threads or demonstrate
atomic Python methods. No real provider, external service, production data, or performance
benchmark was used.

## Manual content review

- Matched the canonical title, outcome, prerequisites, classification, estimates, and E+D+T profile.
- Included a short prerequisite bridge without assuming generated prerequisite notes prove learning.
- Distinguished change responsibility, client capability, source dependencies, runtime calls,
  structural type compatibility, and behavioural promises.
- Compared a direct function, returned data, a callable boundary, a justified richer contract,
  and speculative framework machinery. Kept the actual implementation small.
- Preserved legacy output during refactoring; tested cutoff inclusion, negative temperatures,
  order, duplicates, empty input, Unicode/escaping, visible failures, and input preservation.
- Kept the queued-provider exercise unsolved, with baseline tests only, no released hints,
  no invented learner prediction, and no replacement of Rahul's work.
- Recorded actual experiment output, environment, controls, interpretation, and limits.
- Supplied reading directions, key insights, and limitations for non-trivial visuals.
- Read the listed primary sources; Python Mastery links are navigation references only.
- Used original prose, code, and code-native visuals with synthetic data. No new license,
  copied book material, credentials, environments, or raw conversation transcript is included.
- Preserved NotebookLM boundaries: the approved unit note is eligible; progress, attempts,
  solutions, test output, and this maintainer record are not an upload bundle.

## Learning boundary

Artifact approval means the teaching material has been reviewed and checked. It does not
close the practice exercise or advance any learning state, review date, weakness, evidence
link, or mastery badge. Future learning evidence must come from Rahul's actual work.
