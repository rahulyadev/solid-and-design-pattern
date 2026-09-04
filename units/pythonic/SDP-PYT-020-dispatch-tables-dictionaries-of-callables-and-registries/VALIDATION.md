# Maintainer validation — SDP-PYT-020

Date: **2026-09-05**. Artifact state: **Approved**. Learning state: **Not started**.
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
- Draft initialization commit: `8ec5ba81f00c4df9fd064bb51fec9775754e8f3b`; it was pushed
  normally only after its local-only list matched `INIT_START..HEAD` exactly.
- Rahul's combined initialization and publication request authorizes the final approval commit,
  normal push, pull request, checked squash merge, and synchronized `main`.

The final approval commit is the commit that updates this record. Its exact SHA, pull request,
merge commit, and synchronized `main` result are reported after publication; a commit cannot
truthfully contain its own hash.

## Executed checks

| Check | Observed result |
|---|---|
| Clean baseline repository validator | Passed after placing uv cache outside the Worktree. |
| Final repository validator | Passed, including lock consistency, links, metadata, and zero hygiene violations. |
| Unit tests, CPython 3.14.7 and 3.11.16 | 40 passed on each runtime. |
| Full repository regression, CPython 3.14.7 | 619 passed across 21 units, one pytest process per unit. |
| Strict mypy, Python 3.14 and 3.11 targets | No issues in 9 source files on either target. |
| Ruff lint and formatting | Passed for all 15 Python and Markdown files considered by Ruff. |
| Python 3.11 grammar | All 9 Python files parsed. |
| README Python snippets | All 8 blocks parsed separately on Python 3.14 and 3.11. |
| Worked demo, both runtimes | Completed with identical stdout: three exact-handler results, then one explicit fallback result. |
| Exception-boundary probe, both runtimes | Identical stdout; broad catch misreported the failure and narrow catch preserved the original `KeyError`. |
| Registry-lifecycle probe, both runtimes | Identical stdout; binding writes and late registration failed while mutable callable state changed output. |
| Embedded visual observations | Unit test compared the complete HTML JSON block with actual Python observations. |
| HTML JavaScript | The executable script passed Node's syntax parser. |
| Interactive visual states | All 7 dispatch/lifecycle states produced their expected visible value. |

The first baseline validator invocation used uv's default cache and failed only because the sandbox
made that cache location read-only. The unchanged validator then passed with `UV_CACHE_DIR` under
the task's external temporary tool directory. No validator, dependency, or lockfile was changed.

## Environment and reproduction

The locked environment and every cache are outside the repository. Bytecode writing and pytest's
cache provider are disabled; Ruff uses `--no-cache`. Commands are documented in the
[practice guide](practice/README.md#commands).

| Item | Actual environment |
|---|---|
| OS | Linux-7.0.0-30-generic-x86_64-with-glibc2.43 |
| Architecture | x86_64 |
| Canonical runtime | CPython 3.14.7, Clang 22.1.3 |
| Compatibility runtime | CPython 3.11.16, Clang 22.1.3 |
| Development tools | pytest 8.4.2; mypy 1.20.2; Ruff 0.16.1; repository lock unchanged. |
| Cache policy | Bytecode disabled; environments, uv, mypy, and Hypothesis data outside the Worktree. |

## Visual verification and limits

All 7 states were exercised at 1024, 736, 360, and 320 pixel viewport widths under the host's dark
appearance: 28 state-width combinations. A temporary forced-light copy exercised all 7 states at
1024 and 320 pixels: 14 more combinations. Every selected button and displayed observation matched
the requested state. Automated element and document-bound checks found no horizontal overflow in
all 42 combinations.

Desktop dark, desktop light, and narrow mobile screenshots were inspected. Text, flow nodes,
controls, binding rows, state colors, and wrapping remained readable. The browser captured no
warning or error logs. The temporary loopback servers, theme-forcing copy, tabs, and viewport
override were removed or reset after inspection; no QA artifact entered the Worktree.

The visual displays fixed observations; it does not execute Python. Neither visual nor probes use
real events, addresses, networks, databases, brokers, plugins, concurrency, or production data.
Full screen-reader behavior, exhaustive keyboard-only use, cross-browser rendering, and WCAG
certification are not claimed.

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

Artifact approval does not advance learning state. The Approved unit README may be used as a
NotebookLM input. This validation record, `PROGRESS.md`, tests, experiment output, practice starter,
future attempts, reviews, and solutions are excluded from that upload bundle.
