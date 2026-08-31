# EXP-01 — Binding, mutation, and retained references

| Field | Value |
|---|---|
| Owning unit | [SDP-PYT-010](../../README.md) |
| Curriculum | [CURRICULUM.md](../../../../../CURRICULUM.md#sdp-pyt-010) |
| Precise question | Which later readers observe mutation, rebinding, and a loop's final setting? |
| Classification | Python language mechanics and the standard-library partial contract; documented cell introspection. |
| Status | Reproduced on both recorded runtimes by the maintainer. |

## Why observation is necessary

The same result immediately after construction can hide different retained references.
A callback bug may appear only after setup finishes or configuration changes. This probe
separates those events instead of treating all capture as a value copy.

## Hypothesis

The live closure follows the enclosing binding. The default and partial retain the
original list object. An integer tuple snapshot does not observe an append. Loop readers
that share one enclosing binding see its final value when called after construction.
These are maintainer hypotheses, not Rahul's recorded predictions.

## Environment

```text
Date: 2026-08-31
OS: Linux-7.0.0-30-generic-x86_64-with-glibc2.43
Architecture: x86_64
Canonical: CPython 3.14.7
sys.version: 3.14.7 (main, Aug 25 2026, 14:02:56) [Clang 22.1.3 ]
Compatibility: CPython 3.11.16
sys.version: 3.11.16 (main, Aug 25 2026, 14:00:53) [Clang 22.1.3 ]
sys.implementation.name: cpython (both)
Dependencies: standard library only for the probe
Flags: PYTHONDONTWRITEBYTECODE=1; external locked environments and caches
```

## Controls and variables

- Controlled: deterministic settings 2, 5, and 8; synchronous calls; no external effects.
- Changed: append to the existing list, then rebind the outer name to a new list.
- Compared: enclosing lookup, a default argument, partial application, and a tuple snapshot.
- Loop control: separate default arguments and separate calls to a small factory.
- Measured: returned values and whether first/last reader cells are the same object.

Each observed tuple is converted to a new JSON list for output. Recorded observations
therefore do not themselves change when the original list changes later.

## Reproduction command

From the repository root, after the external environment setup in [practice](../../practice/README.md):

```bash
uv run --locked python units/pythonic/SDP-PYT-010-functions-closures-callable-objects/examples/binding_probe.py
```

For the separately installed compatibility environment, add `--python 3.11` after
`--locked`. The implementation is [binding_probe.py](../../examples/binding_probe.py).

## Predicted result

| Step | Live closure | Default argument | partial | Integer tuple snapshot |
|---|---|---|---|---|
| Create | `(2,)` | `(2,)` | `(2,)` | `(2,)` |
| Append 5 | `(2, 5)` | `(2, 5)` | `(2, 5)` | `(2,)` |
| Rebind to a new list containing 8 | `(8,)` | `(2, 5)` | `(2, 5)` | `(2,)` |

For the loop, predict late-reader results `[8, 8, 8]`, with default/factory controls
`[2, 5, 8]`. Predict a shared cell for the late readers and distinct factory cells.

## Observed result

The following stdout was captured, not manually invented. It was identical on CPython
3.14.7 and 3.11.16. It also matches the [interactive visual](../../visuals/callable-state.html).

Make your prediction before reading this captured output.

```json
{
  "capture": [
    {
      "stage": "Create readers",
      "current": [
        2
      ],
      "original": [
        2
      ],
      "closure": [
        2
      ],
      "default": [
        2
      ],
      "partial": [
        2
      ],
      "snapshot": [
        2
      ]
    },
    {
      "stage": "Mutate original list",
      "current": [
        2,
        5
      ],
      "original": [
        2,
        5
      ],
      "closure": [
        2,
        5
      ],
      "default": [
        2,
        5
      ],
      "partial": [
        2,
        5
      ],
      "snapshot": [
        2
      ]
    },
    {
      "stage": "Rebind outer name",
      "current": [
        8
      ],
      "original": [
        2,
        5
      ],
      "closure": [
        8
      ],
      "default": [
        2,
        5
      ],
      "partial": [
        2,
        5
      ],
      "snapshot": [
        2
      ]
    }
  ],
  "loop": {
    "configured": [
      2,
      5,
      8
    ],
    "late": [
      8,
      8,
      8
    ],
    "default": [
      2,
      5,
      8
    ],
    "factory": [
      2,
      5,
      8
    ],
    "shared_cell": true,
    "separate_cells": true
  }
}
```

## Interpretation

1. Appending changes the shared List A object, so three reference-based readers notice it.
2. Rebinding redirects only the live closure's route in this experiment. It does not move
   the references already stored as a default or partial argument.
3. Each factory call gives its returned reader a separate enclosing binding. Merely
   defining another reader in the same loop does not do that.
4. The observations support the predicted language/library behaviour. They do not measure
   how much memory a closure occupies or prove a specific interpreter memory layout.

## Visual interpretation

```text
before rebinding:  closure -> values binding -> List A [2, 5]
                   default ------------------> List A [2, 5]
                   partial ------------------> List A [2, 5]
                   snapshot -> tuple (2,)

after rebinding:   closure -> values binding -> List B [8]
                   default ------------------> List A [2, 5]
                   partial ------------------> List A [2, 5]
                   snapshot -> tuple (2,)
```

### How to read this visual

Compare the upper and lower blocks. Arrows indicate conceptual references. Only the
outer `values` binding is redirected by assignment; List A still exists through other references.

### Key insight

A binding change is not an object mutation, and argument binding is not deep copying.

### Simplification or limitation

This is a conceptual object graph. Default arguments can be explicitly replaced by
call-time arguments. The tuple snapshot contains only integers; nested mutable elements
would remain shared after a shallow conversion. Cells are inspected for this experiment,
not proposed as a production API for configuring callables.

## Design conclusion

Choose deliberately between live configuration, a retained object reference, and a
snapshot. Give each independently configured operation its intended ownership boundary.
Do not repair a lifetime problem merely by replacing `lambda` with `def`.

## Limitations

The loop readers are invoked after loop completion, not during it. The probe does not
measure resource finalization, garbage collection, async scheduling, parallel mutation,
serialization, or performance. It does not prove the independent practice lab is solved.

## Sources

1. [Python execution model: name resolution](https://docs.python.org/3.14/reference/executionmodel.html#resolution-of-names) — bindings and enclosing lookup.
2. [Python function definitions](https://docs.python.org/3.14/reference/compound_stmts.html#function-definitions) — default evaluation.
3. [Python functools.partial](https://docs.python.org/3.14/library/functools.html#functools.partial) — retained arguments and later calls.
4. [Python FAQ: loop-defined functions](https://docs.python.org/3.14/faq/programming.html#why-do-lambdas-defined-in-a-loop-with-different-values-all-return-the-same-result) — late lookup also applies to `def`.
5. [Python data model: function closure attributes](https://docs.python.org/3.14/reference/datamodel.html#user-defined-functions) — the documented introspection surface.
