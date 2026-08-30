# Practice — SDP-SOL-070 Pythonic SOLID with functions, modules, Protocols, and ABCs

| Field | Value |
|---|---|
| Unit note | [SDP-SOL-070](../README.md) |
| Curriculum | [CURRICULUM.md](../../../../CURRICULUM.md#sdp-sol-070) |
| Evidence target | E+I+D+T |
| Attempt required before solution | Yes |
| Test command | See Commands below |
| Status | Not attempted |

## Learning question

Can you integrate an independent catalogue without making its client depend on unused
capabilities or confusing “missing” with “unavailable”?

## Lab cycle

```text
predict → run → observe → explain → refactor → vary
```

## Starter files

- [reading_room_lab.py](reading_room_lab.py): a runnable concrete baseline.
- [test_reading_room_lab.py](test_reading_room_lab.py): existing observable behaviour only.

There is no replacement integration, proposed final signature, comparison solution, or
released hint. A passing baseline is not a completed exercise.

## Problem and change pressure

`build_reading_cards` currently depends on `ShelfCatalog`. It looks up titles, preserves code
order and duplicates, and represents an unknown code with an unavailable card. The catalogue
also has editing methods that this client never uses.

A second source is supplied as a Python module. Its public operation is
`fetch_title(code: str) -> str | None`. It returns `None` for an unknown code and raises
`ConnectionError` for an outage. An empty string is a valid stored draft title. The module
has no editing methods, and its owner will not add an inheritance relationship for your app.
Implement a synthetic version locally; do not call an external service.

A teammate proposes an ABC with lookup, replace, remove, connect, and close methods, plus a
factory for each implementation. Review that proposal before changing code. Choose and
defend a smaller boundary if the client's needs support one. Do not choose a class count
as your target. The badge example is a mechanism demonstration, not the catalogue solution.

## Expected observable behaviour

- Preserve order, duplicate codes, exact spelling, and the tuple result.
- Unknown codes produce `ReadingCard(code, "Not on this shelf", False)`.
- Known codes produce an available card, including the existing empty-title case.
- Outages remain visible exceptions. Do not turn them into missing cards or successful data.
- Reject every blank code before performing any lookup; an empty input makes no lookup.
- Preserve caller inputs. Do not silently strip, sort, deduplicate, or rewrite codes.
- The existing catalogue's administrative operations still work for its other clients.
- The reading client must not require unsupported administrative or lifecycle operations.

The current function accepts a `Sequence[str]`. Supporting single-pass generators would be
a separate requirement. Keep the contract explicit instead of broadening its type casually.

## Prediction before running

In your own attempt note, predict the three printed cards, the result for a blank second
code, and the difference between an unknown code, an empty title, and an outage. Draw the
current source dependency separately from the runtime lookup. Name the actual pressure.

No learner prediction has been recorded. Maintainer smoke runs do not replace this step.

## Commands

Run from a clean repository Worktree. Keep environments and caches outside it: the repository
validator checks ignored directories as well as tracked files.

```bash
SDP_SOL_070_TOOLS=$(mktemp -d /tmp/sdp-sol-070-tools.XXXXXX)
export UV_PROJECT_ENVIRONMENT="$SDP_SOL_070_TOOLS/venv"
export UV_CACHE_DIR="$SDP_SOL_070_TOOLS/uv-cache"
export MYPY_CACHE_DIR="$SDP_SOL_070_TOOLS/mypy-cache"
export HYPOTHESIS_STORAGE_DIRECTORY="$SDP_SOL_070_TOOLS/hypothesis"
export PYTHONDONTWRITEBYTECODE=1

uv sync --locked --group dev
uv run --locked python units/solid/SDP-SOL-070-pythonic-solid-with-functions-modules-protocols-and-abcs/practice/reading_room_lab.py
uv run --locked pytest -q -p no:cacheprovider units/solid/SDP-SOL-070-pythonic-solid-with-functions-modules-protocols-and-abcs
uv run --locked ruff check --no-cache units/solid/SDP-SOL-070-pythonic-solid-with-functions-modules-protocols-and-abcs
uv run --locked ruff format --check --no-cache units/solid/SDP-SOL-070-pythonic-solid-with-functions-modules-protocols-and-abcs
uv run --locked mypy units/solid/SDP-SOL-070-pythonic-solid-with-functions-modules-protocols-and-abcs
uv run --locked python scripts/validate_repo.py
```

The independent examples and runtime probes use the same environment:

```bash
uv run --locked python units/solid/SDP-SOL-070-pythonic-solid-with-functions-modules-protocols-and-abcs/examples/run_badge_demo.py
uv run --locked python units/solid/SDP-SOL-070-pythonic-solid-with-functions-modules-protocols-and-abcs/experiments/EXP-01-protocol-boundary/protocol_probe.py
uv run --locked python units/solid/SDP-SOL-070-pythonic-solid-with-functions-modules-protocols-and-abcs/experiments/EXP-02-abc-boundary/abc_probe.py
```

For a separate Python 3.11 environment, change `UV_PROJECT_ENVIRONMENT` to another external
path, run `uv sync --locked --group dev --python 3.11`, and use `uv run --locked --python 3.11`
for its commands. Pass `--python-version 3.11` to mypy. Do not replace an environment another
task is using. Record actual interpreter versions, commands, and results.

## Rahul's attempt

Not attempted. Preserve the original baseline, first prediction, first implementation,
design explanation, and one rejected alternative. Add a review only after an actual attempt.

## Observe and explain

After the baseline run, explain what makes a card “available,” which exceptions become
data, and which operations the reading client uses. Identify which parts of that promise
a type checker can check. Say whether a module, callable, Protocol, or ABC earns its place.

## Refactor

Write a short decision record before changing the boundary: force, stable promises, selected
mechanism, rejected alternative, costs, and trigger to reconsider. Then integrate the new
synthetic source and add behaviour tests. If construction changes, keep the meaningful
assertions and explain changed test setup. Avoid `Any`, ignored type errors, no-op methods,
global service lookup, or concrete-provider switches that hide the unresolved boundary.

No hints have been released. Request one progressive hint only after preserving your attempt.

## Required edge cases

Test a found title, unknown code, empty title, Unicode, whitespace-preserving codes, empty
input, duplicates, and invalid later input. Add an outage both on the first lookup and after
one successful lookup. Decide what side effects a lookup may leave if a later one fails;
returning a tuple does not make external operations transactional.

Check that a source with only the required reading operation works and that one source's
configuration does not unexpectedly affect another reader. These are behavioural prompts,
not a prescribed class or function layout.

## Vary: production transfer

After the first attempt, add two concurrently configured catalogues for different reading
rooms. The source must accept a room identifier. Explain where configuration belongs and
whether mutable module globals preserve caller isolation. Then consider a genuinely
stateful provider with an owned connection: define who opens, shares, and closes it before
adding lifecycle methods to any contract. No threads or real connections are required.

## Interview checkpoint

Ask one question at a time. Begin: **“What promise would the reading client lose if every
falsy title or every exception were treated as a missing item?”**

Review the precise missing reasoning step before suggesting code.

## Troubleshooting

- Run by the documented paths; hyphenated unit directories are not importable package names.
- Run full repository regression one unit per pytest process; older units reuse module names.
- Do not delete pre-existing environments or caches to satisfy hygiene; use a clean Worktree.
- `frozen=True` on the result is not a substitute for a clear provider contract.

## Review and closure

Closure requires the preserved attempt, tested integration, edge cases, explanation,
rejected alternative, and transfer reasoning. Add a comparison solution only after Rahul
closes the exercise. Baseline tests and generated material do not advance learning state.
