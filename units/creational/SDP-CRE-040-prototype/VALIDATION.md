# Validation — SDP-CRE-040

## Scope and learning boundary

This record covers only `topic/SDP-CRE-040`, its unit tree, and the matching progress row.
`INIT_START` is `33eb230e921b2abcc5e1fab1dbadd061bd2841d7`, recorded after a clean tracked/untracked
status. Artifact state is Draft during initialization; learning remains Not started. No learner
prediction, attempt, explanation, recall, or transfer evidence is invented.

GitHub identity preflight passed as `rahulyadev` using elevated network permission after the
restricted check reported a token/network failure. Exact no-tag main fetch succeeded, and the exact
topic branch probe returned absent (exit 2). Main, origin/main, and detached Worktree HEAD matched;
no other Worktree owned this branch. The exact branch was then created from that baseline.

The source policy, unit template, canonical entry, relevant Python mappings, progress row,
publication workflow, and predecessor quality standard were read. Source references near claims
identify authoritative pages actually read. All explanations, diagrams, code, and data are original
synthetic examples. No license change or learner solution is included.

## Browser limitation

The in-app browser rejected the direct local `file:` URL under its URL security policy. Rendering
was not performed and no bypass was attempted. Static data/accessibility/responsive contracts and
JavaScript syntax are distinct from browser rendering.

## Check record

Initialization checks executed on 2026-09-09:

| Check | Observed result |
|---|---|
| CPython 3.14.7 focused tests | 42 passed |
| CPython 3.11.16 focused tests | 42 passed |
| Strict mypy 1.20.2 | Passed all 6 non-test Python source files for both 3.11 and 3.14 targets |
| Ruff 0.16.1 | Lint passed; 16 format-eligible files compliant |
| README snippets | 11 Python blocks compiled and executed independently on both runtimes |
| Demo | Both printed `(True, True, True, True, 0)` |
| Copy probe | All five observations matched on both runtimes |
| Practice | Both printed the internal destination count and `target_complete=False` |
| Visual contract | Embedded observations, order, controls and static structure passed |
| JavaScript syntax | Node.js 24.19.0 `--check` passed |
| Repository validator | Passed including lock consistency; zero forbidden-path violations |
| Git diff | `git diff --check` passed; only this unit and its progress row changed |

The first 3.14 test run exposed a documented-versus-implemented dataclass exception difference.
After inspecting the official version-pinned source, tests assert the actual exception classes on
each tested runtime and the notes explain the discrepancy. No failed check was bypassed.

The existing Local 3.14 environment supplies exact locked tool versions. A separate locked 3.11
support environment was created under `/tmp`. All pytest, Hypothesis, mypy, Ruff, uv, coverage, and
bytecode output is redirected to `/tmp`; pytest's repository cache provider is disabled. The full
regression will inherit the same mypy setting, including tests that invoke mypy internally.
No environment, cache, ZIP, transcript, credential, or raw log is included in this unit.
