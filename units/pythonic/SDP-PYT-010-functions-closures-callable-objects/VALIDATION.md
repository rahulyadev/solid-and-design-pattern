# Maintainer validation — SDP-PYT-010

Date: **2026-08-31**. Artifact state: **Draft**. Learning state: **Not started**.
The [practice](practice/README.md) is **Not attempted**. These are checks of the generated
material, not Rahul's prediction, implementation, interview performance, or retention.

## Scope and provenance

- Exact branch: `topic/SDP-PYT-010`.
- Synchronized initialization base: `38fbb55b551df86bc1f55f4258b1fa14e89d400b`.
- The dedicated Worktree was clean before recording `INIT_START` at that commit.
- No existing exact topic branch, competing owner, or pre-existing changes were included.
- Changes are limited to this unit and its matching artifact-state cell in `PROGRESS.md`.
- Curriculum IDs, prerequisites, classifications, estimates, paths, tooling, dependencies,
  and **SDP-PYT-020** remain unchanged.

## Executed checks

| Check | Observed result |
|---|---|
| Clean baseline repository validator | Passed, including the lock check and zero hygiene violations. |
| Repository validator after writing this record | Passed, including links, lock consistency, metadata, and zero hygiene violations. |
| Unit tests, CPython 3.14.7 | 36 passed. |
| Unit tests, CPython 3.11.16 | 36 passed. |
| Full repository regression, CPython 3.14.7 | 579 passed across 20 units, one pytest process per unit. |
| Strict mypy, Python 3.14 target | No issues in 9 source files. |
| Strict mypy, Python 3.11 target | No issues in 9 source files. |
| Ruff lint and formatting | Passed for the unit. |
| Python 3.11 grammar | All 9 Python files parsed. |
| README Python snippets | All 3 blocks executed separately on both runtimes. |
| Worked demo, lab baseline, binding probe, effects probe | All 4 documented commands ran on both runtimes, with identical stdout. |
| Embedded visual observations | A test compared the complete data block with actual Python observations on both runtimes. |
| HTML source | All 3 relative links exist; its JavaScript passed Node's syntax check. |

The initial static check found an assertion on a function annotated to return only None;
the empty-input test now checks that invocation succeeds. Formatting was normalized.
One B023 suppression remains deliberately confined to the late-binding counterexample;
the test verifies its surprising result. No behavioural test was skipped, marked as
expected failure, or weakened to hide a failure. The repository validator rejects Markdown
disclosure tags, so the experiment uses ordinary Markdown instead. A child type-checker
in the first full regression created a local cache; only that task-created cache was removed,
and the successful full rerun explicitly placed its cache outside the Worktree.

## Environment and reproduction

Both external environments were synchronized from the unchanged repository lock with
`uv sync --locked --group dev`, explicitly selecting Python 3.11 for compatibility.
Reproduction commands and cache placement are in [practice](practice/README.md).

| Item | Actual environment |
|---|---|
| OS | Linux-7.0.0-30-generic-x86_64-with-glibc2.43 |
| Architecture | x86_64 |
| Canonical runtime | CPython 3.14.7, Clang 22.1.3 |
| Compatibility runtime | CPython 3.11.16, Clang 22.1.3 |
| Development tools | pytest 8.4.2; mypy 1.20.2; Ruff 0.16.1; repository lock unchanged. |
| Cache policy | Bytecode disabled; environments, uv, mypy, and Hypothesis data outside the repository. |

The original Local checkout contains pre-existing ignored environments and caches. Its
initial validator invocation rejected those paths and could not write the default uv cache.
They were preserved. Validation was then performed successfully in the clean dedicated
Worktree with an external cache; neither the validator nor its hygiene rules were changed.
Sandbox network restrictions required approved access for locked dependency downloads.

## Visual verification and limits

The two scenarios were checked at 1024, 736, 360, and 320 pixel viewport widths in light
and dark appearance. All 32 combinations of scenario/step, width, and appearance displayed
the expected values without horizontal document, cell, or control overflow. Screenshot
inspection found a narrow mobile caption; its display rule was corrected before publication.
The final rerun after that correction passed all 32 combinations, and another mobile
screenshot confirmed that the caption wraps across the available width.

Appearance checks used a temporary loopback-only QA server. Its only theme substitution
was the root `color-scheme` declaration; the repository file follows the browser preference.
The disclosure opened successfully. No browser warning or error logs were captured during
the checked interactions. Full keyboard-only navigation, screen-reader behavior, and
cross-browser certification are not claimed.

The visual displays the probe's fixed observations; it does not execute Python. The probes
do not exercise real connections, brokers, concurrency, process restarts, benchmarks, or
production data. They are maintainer demonstrations and not learner evidence.

## Manual content review

- Matched the canonical title, outcome, prerequisite IDs, metadata, and E+I+D+T profile.
- Included the smallest prerequisite bridge without claiming those units were learned.
- Compared the direct function, replaceable callable, closure, partial, bound method,
  callable instance, and the cost of an unnecessary hierarchy.
- Separated setup, invocation, and effects; explained Strategy-like versus Command-like roles.
- Distinguished enclosing lookup, mutation, rebinding, defaults, shallow snapshots, and aliases.
- Kept callback argument kinds and keywords explicit; did not claim runtime type enforcement.
- Covered errors before/after effects, exception identity, order, duplicates, source
  consumption, successful-call counts, independent owners, and replay.
- Kept the independent lab unsolved, with preserved baseline tests, a new quota requirement,
  no released hints, no replacement implementation, and no fabricated learner review.
- Included visual reading guides, key insights, and limitations.
- Read primary sources for subtle claims; Python Mastery lesson links are navigation
  references, not external lessons claimed as read.
- Used original explanations and synthetic examples; added no license, credentials,
  private material, test caches, or raw conversation transcripts.

## Learning and NotebookLM boundary

Artifact approval requires coherent, source-checked, runnable material. It does not close
the exercise or change learning state. After approval, the unit README may be used with
NotebookLM. This validation record, raw test output, progress tracker, learner attempts,
and any future solutions are not a NotebookLM upload bundle.
