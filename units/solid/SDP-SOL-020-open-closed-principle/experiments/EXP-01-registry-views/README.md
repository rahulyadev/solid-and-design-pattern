# EXP-01 — Registry views, copied bindings, and callable state

| Field | Value |
|---|---|
| Owning unit | [SDP-SOL-020](../../README.md) |
| Curriculum | [CURRICULUM.md](../../../../../CURRICULUM.md#sdp-sol-020) |
| Precise question | Does a read-only registry keep its selected behavior unchanged when other code still owns the mapping or a callable? |
| Classification | Python language and standard-library behavior |
| Status | Interpreted |

This is a supplementary maintainer experiment, not Rahul's practice attempt or a new curriculum
requirement. The canonical evidence profile remains E+I+D+T.

## Why observation is necessary

A type such as `Mapping` or a read-only view can make a registry appear stable. That says little
about aliases to its backing dictionary or the state inside registered objects. Those hidden
relationships matter when a supposedly stable workflow starts behaving differently.

## Hypothesis

> A live proxy will observe a replaced binding. A proxy over copied bindings will keep the original
> function. Copying bindings will still share the state of a registered callable object.

This was the maintainer's expectation before execution. For learner practice, predict the output
independently before opening the observed-result section.

## Environment

```text
Date: 2026-08-30
Operating system: Linux 7.0.0-30-generic
Architecture: x86_64
Python version: CPython 3.14.7
sys.version: 3.14.7 (main, Aug 25 2026, 14:02:56) [Clang 22.1.3 ]
sys.implementation.name: cpython
Runtime dependencies: standard library only
Tests: pytest 8.4.2 from the locked development environment
Relevant environment: PYTHONDONTWRITEBYTECODE=1; external uv environment/cache
```

This is not a CPython-specific claim. The interpretation relies on documented mapping behavior
and observable references, without inspecting implementation internals.

## Controls and variables

- Controlled: input value `7`, the initial function, the two proxy constructions, and operation order.
- Changed: the source mapping's `display` binding, the addition of `extra`, then a separate callable's
  `prefix` attribute.
- Observed: rendered strings and the visible names in each mapping.
- Excluded: threads, asynchronous tasks, plugin discovery, filesystem writes, and timing measurements.

## Reproduction command

Use the external environment exports in the [practice guide](../../practice/README.md#commands),
then run from the repository root:

```bash
uv run --locked --no-sync python units/solid/SDP-SOL-020-open-closed-principle/experiments/EXP-01-registry-views/registry_views.py
uv run --locked --no-sync pytest -q -p no:cacheprovider units/solid/SDP-SOL-020-open-closed-principle/experiments/EXP-01-registry-views
```

## Predicted result

Both views initially render with `plain`. Replacing the source binding changes the live view only.
Adding a name changes the live view's names only. Mutating a callable's own state changes its
output even through the mapping with copied bindings.

## Observed result

Actual maintainer output from `registry_views.py` on the environment above:

```text
before: live=plain:7; snapshot=plain:7
after replacement: live=LOUD:7; snapshot=plain:7
names: live=('display', 'extra'); snapshot=('display',)
callable state before: first:7
callable state after: second:7
```

## Interpretation

1. The first three lines show that the proxy is live, while the copied mapping keeps its own name
   bindings. `MappingProxyType` is documented as a dynamic read-only view, not a snapshot.
   [Standard-library contract](https://docs.python.org/3.14/library/types.html#types.MappingProxyType).
2. The final two lines show that copying the mapping did not copy or freeze the callable object.
   The same object's changed prefix affects its next call. This is a direct observation of this
   construction, not a claim that every callable is stateful.
3. Predictable registration needs an ownership and lifecycle policy. A read-only API alone does
   not prove that behavior will remain stable. This is the design inference from the experiment.

The visible name order follows dictionary insertion order. It is not a priority-selection policy.
[Dictionary behavior](https://docs.python.org/3.14/library/stdtypes.html#mapping-types-dict).

## Visual interpretation

```text
live proxy ───────► source dictionary ── display ──► loud

copied proxy ─────► separate dictionary ─ display ─► plain

separate state case:
source dictionary ───┐
                    ├── display ──► one PrefixRenderer object
copied dictionary ───┘               prefix changes: first → second
```

### How to read this visual

Arrows indicate conceptual references after the mapping replacement. The lower case is a separate
setup: two mappings reference one mutable callable. This is not a CPython memory-layout diagram.

### Key insight

There are two different things to protect: name-to-callable bindings and the behavior/state of the
callables themselves. Copying the first does not freeze the second.

### Simplification or limitation

The diagram omits local-variable references and allocation details. No thread scheduling,
simultaneous mutation, or automatic isolation is demonstrated.

## Design conclusion

The worked example's registry builder constructs a private dictionary and exposes only a proxy.
Its intended renderers are stateless functions or frozen objects with simple string configuration.
That is enough for this teaching scenario. Stateful resource-owning extensions would need a
separate ownership decision. OCP does not supply that policy automatically.

## Limitations

- Copying a mapping is shallow; it is not a deep-copy or sandbox mechanism.
- Read-only name access does not establish behavioral compatibility or thread safety.
- The example does not establish atomic reconfiguration, hot-reload safety, or deployment guarantees.
- No speed, memory-saving, or benchmark claim is made.
- Reproducing the output without explaining it does not establish learner evidence.

## Sources

1. [Python 3.14 — MappingProxyType](https://docs.python.org/3.14/library/types.html#types.MappingProxyType).
2. [Python 3.14 — dictionary operations](https://docs.python.org/3.14/library/stdtypes.html#mapping-types-dict).
