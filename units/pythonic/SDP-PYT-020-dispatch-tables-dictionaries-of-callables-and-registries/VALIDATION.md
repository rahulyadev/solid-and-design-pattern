# Maintainer validation — SDP-PYT-020

Date: **2026-09-05**. Artifact state: **Draft**. Learning state: **Not started**.
The [practice](practice/README.md) is **Not attempted**. These checks validate generated material;
they are not Rahul's prediction, implementation, interview answer, review, or retention evidence.

## Scope and provenance

- Exact branch: `topic/SDP-PYT-020`.
- Synchronized initialization base and `INIT_START`:
  `32774539f7692ea9d4e79d415c5e07f5efd57f1f`.
- The exact local and remote topic refs did not exist before this operation.
- The dedicated Worktree was clean before `INIT_START` was recorded.
- The original Local checkout's unrelated untracked foundation ZIP files were left untouched.
- Changes are limited to this unit and the matching artifact-state cell in `PROGRESS.md`.
- Curriculum IDs, title, outcome, prerequisites, classifications, estimates, learning paths,
  Python mappings, project definitions, tooling, dependency lock, and **SDP-PYT-030** are unchanged.

The Draft initialization commit is pending at the time of this record. Its exact SHA and all final
publication evidence will be added after the initialization commit and final approval checks.

## Executed Draft checks

| Check | Observed result |
|---|---|
| Clean baseline repository validator | Passed after placing uv cache outside the Worktree. |
| Unit tests, CPython 3.14.7 | 40 passed. |
| Full repository regression, CPython 3.14.7 | 619 passed across 21 units, one pytest process per unit. |
| Strict mypy, Python 3.14 target | No issues in 9 source files. |
| Ruff lint and formatting | Passed for all 14 Python and Markdown files considered by Ruff. |
| Worked demo | Completed; three exact handler results followed by one explicit fallback result. |
| Exception-boundary probe | Completed; broad catch misreported the failure and narrow catch preserved the original `KeyError`. |
| Registry-lifecycle probe | Completed; binding writes and late registration failed while mutable callable state changed output. |
| Embedded visual observations | Unit test compared the complete HTML JSON block with actual Python observations. |
| HTML JavaScript | The executable script passed Node's syntax parser. |

The first baseline validator invocation used uv's default cache and failed only because the sandbox
made that cache location read-only. The unchanged validator then passed with `UV_CACHE_DIR` under
the task's external temporary tool directory. No validator, dependency, or lockfile was changed.

## Environment and reproduction

The locked environment and every cache are outside the repository. Bytecode writing and pytest's
cache provider are disabled; Ruff uses `--no-cache`. Commands are documented in the
[practice guide](practice/README.md#commands).

| Item | Actual Draft environment |
|---|---|
| OS | Linux-7.0.0-30-generic-x86_64-with-glibc2.43 |
| Architecture | x86_64 |
| Canonical runtime | CPython 3.14.7, Clang 22.1.3 |
| Development tools | pytest 8.4.2; mypy 1.20.2; Ruff 0.16.1; repository lock unchanged. |
| Cache policy | Bytecode disabled; environments, uv, mypy, and Hypothesis data outside the Worktree. |

## Draft visual review and limits

The visual is self-contained and its JavaScript syntax and Python-backed observation data are
checked. Final viewport, light/dark, interaction, overflow, and screenshot inspection remain part
of the approval pass and are not claimed in this Draft record.

The visual displays fixed observations; it does not execute Python. Neither visual nor probes use
real events, addresses, networks, databases, brokers, plugins, concurrency, or production data.

## Manual content review

- Matched the canonical title, outcome, prerequisites, metadata, and E+I+D+T profile.
- Included the smallest callable, dependency-direction, dictionary, hashing, and order bridge
  without claiming prerequisite learning.
- Began with change pressure and simple intuition before formal mechanics.
- Compared direct calls, `if`, `match`, passed callables, dictionaries, registry builders,
  predicate rules, receiver polymorphism, `singledispatch`, and plugin discovery.
- Separated lookup from invocation and duplicate, fallback, ordering, lifecycle, handler-state,
  observability, and concurrency policies.
- Kept the worked example independent from the unsolved practice domain.
- Kept the practice starter runnable but unsolved, with no released hint or target implementation.
- Labeled conceptual visuals and included reading guides, insights, and limitations.
- Read primary Python and typing sources for subtle claims and used original synthetic material.
- Added no license, secrets, private data, copied diagrams, framework dependency, cache, generated
  environment, or conversation transcript.

## Learning and NotebookLM boundary

Draft or Approved material does not advance learning state. Only the Approved unit README is a
NotebookLM input. This validation record, `PROGRESS.md`, tests, experiment output, practice starter,
future attempts, reviews, and solutions are excluded from that upload bundle.
