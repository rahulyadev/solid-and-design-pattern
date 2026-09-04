# EXP-02 — Registry bindings, publication, and callable state

| Field | Value |
|---|---|
| Owning unit | [SDP-PYT-020](../../README.md) |
| Curriculum | [CURRICULUM.md](../../../../../CURRICULUM.md#sdp-pyt-020) |
| Precise question | What becomes stable when a startup builder copies bindings into a read-only mapping, and what remains mutable? |
| Classification | Python mapping behavior plus lifecycle design |
| Status | Interpreted |

This is a supplementary maintainer experiment. It does not count as Rahul's prediction,
implementation, debugging, or explanation.

## Why observation is necessary

“Frozen registry” is ambiguous. It can mean that consumers cannot add or replace names, but it may
be incorrectly heard as “the registered objects can never change.” The experiment separates those
claims.

## Hypothesis

> Publication will preserve registration order, reject mapping writes and later registration, but
> a mutable callable already stored under a name will still change its own later result.

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

- Controlled: two registration names, their insertion order, event, and trace identifier.
- Changed: a post-publication mapping write, a post-publication registration, and one handler's
  `prefix` field.
- Observed: name order, exception classes/messages, and handler output.
- Excluded: simultaneous mutation, discovery, process restart, deep copying, and benchmarks.

## Reproduction command

Use the external environment from the [practice guide](../../practice/README.md#commands), then:

```bash
uv run --locked python units/pythonic/SDP-PYT-020-dispatch-tables-dictionaries-of-callables-and-registries/examples/registry_lifecycle_probe.py
uv run --locked pytest -q -p no:cacheprovider units/pythonic/SDP-PYT-020-dispatch-tables-dictionaries-of-callables-and-registries/examples/test_probes.py
```

## Observed result

```text
names: ('record.created', 'record.custom')
mapping write: TypeError
post-seal registration: RegistrySealed: registry is sealed
callable state before: probe:first:R-5
callable state after: probe:second:R-5
```

## Interpretation

The builder publishes a proxy over a private copied dictionary. Consumers cannot mutate those
name bindings, and the builder refuses later registration. The stored `PrefixHandler` remains the
same mutable object, so changing its `prefix` changes its later output. Mapping publication and
handler-state policy are separate design decisions.

Python dictionaries preserve insertion order. That makes the displayed name order dependable on
Python 3.11 and 3.14, but it does not create priority semantics. `MappingProxyType` is documented as
a dynamic read-only view; copying first is what separates the published bindings from the
builder's original dictionary. See the [dictionary contract](https://docs.python.org/3.14/library/stdtypes.html#mapping-types-dict)
and [`MappingProxyType`](https://docs.python.org/3.14/library/types.html#types.MappingProxyType).

## Visual interpretation

```text
startup entries ──► RegistryBuilder ── seal/copy ──► read-only name bindings
                           │                              │
                     later register ✕                    └──► mutable PrefixHandler
                                                               first → second
```

### How to read this visual

The top path is the registration lifecycle. The lower arrows distinguish rejected binding changes
from an allowed state change inside a referenced handler.

### Key insight

Read-only bindings protect the dispatch table shape, not every object reachable through it.

### Simplification or limitation

This is a conceptual ownership view, not CPython memory layout. “Private” is a design boundary,
not an access-control mechanism enforced against hostile code.

## Limitations

- A shallow binding copy is not a deep copy or security sandbox.
- The experiment does not establish thread safety for the builder or handler.
- Insertion order is suitable for diagnostics, not a substitute for explicit precedence.
- No plugin loading, entry-point discovery, real I/O, or performance measurement occurs.
