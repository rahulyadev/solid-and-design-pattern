# Practice — SDP-PYT-020 Dispatch tables, dictionaries of callables, and registries

| Field | Value |
|---|---|
| Unit note | [SDP-PYT-020](../README.md) |
| Curriculum | [CURRICULUM.md](../../../../CURRICULUM.md#sdp-pyt-020) |
| Evidence target | E+I+D+T |
| Attempt required before solution | Yes |
| Test command | `uv run --locked pytest -q -p no:cacheprovider units/pythonic/SDP-PYT-020-dispatch-tables-dictionaries-of-callables-and-registries/practice` |
| Status | Not attempted |

## Learning question

Can you separate channel selection from notification execution, then create a registration
boundary whose duplicate, fallback, ordering, and lifetime policies are explicit?

## Lab cycle

```text
predict → run → observe → explain → refactor → vary
```

This is an activity sequence, not the program's runtime flow. Complete it in order. Green
starter tests prove only the legacy observations; they do not prove the new design.

## Starter files

- [notification_router_lab.py](notification_router_lab.py): runnable `if/elif` legacy code.
- [test_notification_router_lab.py](test_notification_router_lab.py): phase-A characterization
  tests.

The worked event-dispatch example uses another domain. This practice directory contains no
target implementation, hidden solution, released hint, or fabricated learner review.

## Problem and change pressure

A synthetic notification workflow supports `email` and `sms`. The current function both chooses
the channel behavior and traverses the notifications. A new deployment needs `push`, while a
different deployment must omit it. Startup configuration, not the traversal, should decide which
trusted handlers are enabled.

This lab returns strings. It performs no network call, sends no message, and contains no real
address or phone data.

### Phase A — preserve and separate

Refactor the stable traversal so it can execute a compatible notification handler without knowing
the channel names. Preserve `Notification`, `route_notifications(notifications, channel)`, and all
existing observations. The compatibility boundary may still translate the two old names.

Add a test that supplies a new compatible handler without editing the traversal. Explain:

1. where a name is selected;
2. where the selected callable is invoked;
3. which boundary owns unsupported-name policy; and
4. why a function annotation alone does not validate untrusted runtime configuration.

Do not add a registry in phase A if direct dependency passing and one small mapping are enough.

### Phase B — controlled registration

The composition root now receives an ordered iterable of enabled `(name, handler)` entries.
Design the smallest registration boundary that satisfies all of these promises:

- names are nonblank, contain no surrounding whitespace, and remain case-sensitive;
- a duplicate name is rejected instead of silently overwriting an earlier handler;
- the published name-to-handler bindings cannot be changed through the consumer's reference;
- registration after publication is rejected;
- separate application assemblies do not share registration state;
- insertion order is available for diagnostics only, never treated as priority;
- unknown-name behavior is either rejection or one explicitly supplied fallback;
- handler exceptions propagate as handler failures, including `KeyError`;
- no module-global registry, import-time decorator registration, discovery mechanism, or framework
  container is introduced.

Add `push` by configuration. The stable traversal should not gain another channel branch.

## Legacy observable contract

| Dimension | Required observation |
|---|---|
| Known channels | Exact lowercase `email` and `sms`. |
| Receipt shape | `{channel}:{recipient}:{body}`. |
| Unknown channel | `ValueError("unsupported channel: {name}")`. |
| Failure timing | Unknown channel is rejected before the input iterable is consumed. |
| Order and duplicates | Preserved. |
| Empty known channel | Empty tuple. |
| Input ownership | Input records are not mutated; a one-pass iterable works. |
| Text | Blank bodies, whitespace, separators, and Unicode are passed through unchanged. |

These are compatibility facts for synthetic data, not validation advice for a real messaging
system. Do not add normalization, deduplication, sorting, escaping, retries, or delivery claims
during the preservation step.

## Required new edge cases

- Empty registry and one-entry registry.
- Blank, padded, differently cased, and Unicode names.
- Same handler under two distinct names.
- Same name registered twice with the same handler and with a different handler.
- An ordered one-pass registration iterable.
- Mutation attempts through the published consumer reference.
- Repeated publication and registration after publication.
- Two independent registry owners used in interleaved order.
- Unknown key with no fallback and with one explicit fallback.
- A selected handler that raises `KeyError`, `ValueError`, or a caller-created exception instance.
- A handler with mutable internal state after registry publication.
- A source iterator and a handler that fail after earlier successful items.

Add one meaningful case of your own and explain why a caller cares about it.

## Prediction before running

Without running the code, write down:

1. both tuples printed by the starter;
2. whether an unknown channel touches a lazy input iterable;
3. whether registering the same key twice in an ordinary dictionary preserves the first value;
4. whether making a mapping read-only also freezes a mutable callable stored inside it; and
5. whether catching `KeyError` around lookup *and invocation* can distinguish the two origins.

No learner prediction has been recorded by the maintainer.

## Commands

Run from a clean repository Worktree. Keep environments and caches outside the repository because
the validator inspects ignored paths too:

```bash
SDP_PYT_020_TOOLS=$(mktemp -d /tmp/sdp-pyt-020-tools.XXXXXX)
export UV_PROJECT_ENVIRONMENT="$SDP_PYT_020_TOOLS/venv"
export UV_PYTHON_INSTALL_DIR="$SDP_PYT_020_TOOLS/python"
export UV_CACHE_DIR="$SDP_PYT_020_TOOLS/uv-cache"
export MYPY_CACHE_DIR="$SDP_PYT_020_TOOLS/mypy-cache"
export HYPOTHESIS_STORAGE_DIRECTORY="$SDP_PYT_020_TOOLS/hypothesis"
export PYTHONDONTWRITEBYTECODE=1

uv sync --locked --group dev
uv run --locked python units/pythonic/SDP-PYT-020-dispatch-tables-dictionaries-of-callables-and-registries/practice/notification_router_lab.py
uv run --locked pytest -q -p no:cacheprovider units/pythonic/SDP-PYT-020-dispatch-tables-dictionaries-of-callables-and-registries
uv run --locked ruff check --no-cache units/pythonic/SDP-PYT-020-dispatch-tables-dictionaries-of-callables-and-registries
uv run --locked ruff format --check --no-cache units/pythonic/SDP-PYT-020-dispatch-tables-dictionaries-of-callables-and-registries
uv run --locked mypy units/pythonic/SDP-PYT-020-dispatch-tables-dictionaries-of-callables-and-registries
UV_CACHE_DIR="$SDP_PYT_020_TOOLS/uv-cache" python scripts/validate_repo.py
```

Run the independent worked example and maintainer experiments with the same environment:

```bash
uv run --locked python units/pythonic/SDP-PYT-020-dispatch-tables-dictionaries-of-callables-and-registries/examples/run_dispatch_demo.py
uv run --locked python units/pythonic/SDP-PYT-020-dispatch-tables-dictionaries-of-callables-and-registries/examples/exception_boundary_probe.py
uv run --locked python units/pythonic/SDP-PYT-020-dispatch-tables-dictionaries-of-callables-and-registries/examples/registry_lifecycle_probe.py
```

For Python 3.11, create a separate external environment with
`uv sync --locked --group dev --python 3.11`, use `uv run --locked --python 3.11`, and pass
`--python-version 3.11` to mypy. Record the runtime actually used.

## Rahul's attempt

Not attempted. Before editing, preserve your prediction, first implementation, design reasoning,
rejected alternative, and command output. Preserve phase A before phase B in Git or in a clearly
named attempt artifact. Maintainer checks are not your attempt.

## Observe and explain

After running, explain the full path from channel input to selected handler to receipt. Identify
the exact exception boundary for missing names. Explain why mapping immutability, callable state,
thread safety, safe retries, and plugin trust are five separate questions.

## Refactor

Record a short design decision containing: change pressure, stable promises, selection owner,
execution owner, duplicate policy, unknown policy, lifecycle boundary, rejected alternative, and
the condition that would justify a richer mechanism. Preserve the old tests without weakening
their assertions.

## Progressive hints and review

No hints have been released and no learner review has occurred. After preserving an attempt, ask
for one hint at a time. Review should expose the first missing reasoning step with one focused case
before offering replacement code.

## Vary — production transfer

Handlers may now come from independently deployed packages, and some perform externally visible
writes. Propose where discovery, allowlisting, compatibility checks, timeouts, retries,
idempotency, and per-request resources belong. Explain why a global decorator registry plus
`try/except Exception` does not solve those concerns. Do not build a plugin loader or real message
transport here; those belong to later units.

## Interview checkpoint

Ask one question at a time, beginning: **“What policy does a registry add beyond a dictionary of
callables?”** Wait before probing exception scope, ordering, lifecycle, or plugin discovery.

## Troubleshooting

- The starter is expected to pass. The exercise remains unsolved.
- Hyphenated unit directories are not importable package names; run the documented file paths.
- A dictionary literal silently keeps the last repeated key; construct registration from ordered
  entries if duplicate detection is part of the contract.
- A read-only mapping does not make stateful handlers immutable or thread-safe.
- Do not catch handler `KeyError` inside the missing-dispatch-key translation boundary.
- Repository publication does not supply learner implementation or retrieval evidence.

## Closure requirements

Only after Rahul closes the exercise: link the preserved attempt; record prediction versus
observation; pass old and learner-added tests; explain edge cases, rejected designs, and transfer;
and complete review. Only then may a comparison solution be added. Until then, status stays
**Not attempted** and the learning tracker stays **Not started**.
