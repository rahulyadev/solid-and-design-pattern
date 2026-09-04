# EXP-01 — Lookup failure versus handler failure

| Field | Value |
|---|---|
| Owning unit | [SDP-PYT-020](../../README.md) |
| Curriculum | [CURRICULUM.md](../../../../../CURRICULUM.md#sdp-pyt-020) |
| Precise question | What information is lost when one `KeyError` handler surrounds both dictionary lookup and selected-handler invocation? |
| Classification | Python exception flow plus design boundary |
| Status | Interpreted |

This is a supplementary maintainer experiment, not Rahul's practice attempt and not a new
curriculum requirement. The canonical evidence profile remains E+I+D+T.

## Why observation is necessary

Both a missing dispatch key and ordinary handler code may raise `KeyError`. A short implementation
can accidentally translate both into “unknown event,” hiding a real payload or configuration bug.

## Hypothesis

> A broad catch will mislabel the handler's `KeyError`. Resolving inside a narrow catch and calling
> afterward will preserve the original handler exception object.

This was the maintainer's prediction before execution.

## Environment

```text
Date: 2026-09-05
Operating system: Linux
Architecture: x86_64
Canonical target: CPython 3.14
Interview compatibility target: CPython 3.11
Runtime dependencies: standard library only
Relevant environment: bytecode disabled; uv environment and caches outside the Worktree
```

Exact patch versions and successful commands are recorded in [VALIDATION.md](../../VALIDATION.md).

## Controls and variables

- Controlled: the event, registered handler, caller-created `KeyError`, and trace identifier.
- Changed: only the scope of the `try` statement.
- Observed: exception type, message, and identity.
- Excluded: logging frameworks, retries, async code, threads, real payloads, and timing.

## Reproduction command

Use the external environment from the [practice guide](../../practice/README.md#commands), then:

```bash
uv run --locked python units/pythonic/SDP-PYT-020-dispatch-tables-dictionaries-of-callables-and-registries/examples/exception_boundary_probe.py
uv run --locked pytest -q -p no:cacheprovider units/pythonic/SDP-PYT-020-dispatch-tables-dictionaries-of-callables-and-registries/examples/test_probes.py
```

## Observed result

```text
broad catch: UnknownEventType: unsupported event type: record.broken
lookup-only catch: KeyError: 'payload.customer_id'; same=True
```

## Interpretation

The broad form catches the selected handler's failure because invocation is inside the same
`try`. The controlled form catches only mapping lookup, translates a missing key, exits the catch
boundary, and then invokes the selected handler. The original exception therefore reaches the
caller unchanged.

Dictionary subscription raises `KeyError` for a missing key; that language-level observation does
not imply every `KeyError` inside a handler is a lookup miss. See the
[Python 3.14 dictionary contract](https://docs.python.org/3.14/library/stdtypes.html#mapping-types-dict).

## Visual interpretation

```text
broad:      try [ lookup ──► call ──► handler KeyError ] ──► UnknownEventType

controlled: try [ lookup ] ──► call ──► handler KeyError ──► caller unchanged
```

### How to read this visual

The brackets show the code covered by the missing-name translation. Follow left to right.

### Key insight

An exception boundary should cover only the operation whose failure it can interpret correctly.

### Simplification or limitation

This is conceptual exception flow, not stack-frame or CPython memory layout. The fixed probe does
not cover exception groups, asynchronous cancellation, retries, or logging.

## Limitations

- One synthetic failure cannot prove every handler contract is correct.
- The probe makes no recommendation to catch all handler failures at this layer.
- Preserving an exception is not the same as adding useful operational context.
- No performance or reliability claim is made.
