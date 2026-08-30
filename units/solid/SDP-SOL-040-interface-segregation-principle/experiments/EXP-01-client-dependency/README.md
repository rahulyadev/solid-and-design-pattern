# EXP-01 — Unused contract growth and the unchanged Python call

| Field | Value |
|---|---|
| Owning unit | [SDP-SOL-040](../../README.md) |
| Curriculum | [CURRICULUM.md](../../../../../CURRICULUM.md#sdp-sol-040) |
| Precise question | Can an unrelated contract change reject a reader statically while its preview call still works? |
| Classification | Python runtime behaviour, typing specification, and mypy observation |
| Status | Run and interpreted by maintainer; learner prediction not recorded |

## Why observation is necessary

The source body calls only `read`. It is easy to confuse a changed parameter contract with
an extra runtime operation. Comparing both outcomes makes the difference observable.
This optional mechanism probe supports the unit; it does not add a canonical evidence requirement.

## Hypothesis

Adding write/remove to a shared contract will make the reader fail static checking.
Keeping the preview attached to its own reader contract will preserve static compatibility.
All three actual preview calls will return the same value because their executed bodies
and provider remain unchanged. This is the maintainer's hypothesis, not Rahul's prediction.

## Environment

```text
Date: 2026-08-30
Operating system: Linux 7.0.0-30-generic, glibc 2.43
Architecture: x86_64
Python version: CPython 3.14.7
sys.version: 3.14.7 (main, Aug 25 2026, 14:02:56) [Clang 22.1.3 ]
sys.implementation.name: cpython
Dependencies: mypy 1.20.2; pytest 8.4.2 for the experiment tests
Flags: PYTHONDONTWRITEBYTECODE=1; external tool/cache directories
Mypy controls: isolated strict configuration, explicit interpreter version, no incremental cache reuse
```

## Controls and variables

- Controlled: provider, input key, return value, preview body, and tool versions.
- Changed: whether the shared contract grows and which contract annotates the preview.
- Measured: mypy exit status/diagnostic codes and the actual runtime result.

The runner writes three standalone candidates to temporary directories. It runs mypy and
executes only this fixed, original probe source. It does not execute user-supplied code.

## Reproduction command

Apply the external-environment setup in the [practice guide](../../practice/README.md#commands),
then run from the repository root:

```bash
uv run --locked python units/solid/SDP-SOL-040-interface-segregation-principle/experiments/EXP-01-client-dependency/dependency_probe.py
uv run --locked pytest -q -p no:cacheprovider units/solid/SDP-SOL-040-interface-segregation-principle/experiments/EXP-01-client-dependency
```

Record your prediction before running. Source: [dependency_probe.py](dependency_probe.py).

## Predicted result

| Scenario | Static prediction | Runtime prediction |
|---|---|---|
| Shared contract before growth | Accept | hello |
| Shared contract after growth | Reject missing write/remove | hello |
| Client contract after growth | Accept | hello |

## Observed result

The runner actually produced:

```text
shared contract before growth: static=accepted; errors=none; runtime='hello'
shared contract after growth: static=rejected; errors=arg-type; runtime='hello'
client contract after growth: static=accepted; errors=none; runtime='hello'
```

The same output was reproduced on CPython 3.11.16 using the locked mypy. The six experiment
tests passed as part of the 43-test unit suite on both interpreters. The rejected
candidate is an intentional negative control whose diagnostic is asserted; no failed test
is skipped or relabeled as passing.

## Interpretation

1. The added member requirements change static compatibility for the shared boundary.
2. The narrower client boundary remains compatible in this controlled change.
3. Runtime still executes the same read call; ordinary annotations do not enforce the type.
4. This does not prove a useful provider can satisfy every behavioural promise of a reader,
   or that the real application has no remaining module-level coupling.

[Python typing introduction](https://docs.python.org/3.14/library/typing.html) distinguishes
runtime execution from annotation checking.
[Protocol assignability](https://typing.python.org/en/latest/spec/protocol.html#assignability-relationships-with-other-types)
defines the static member requirement. The diagnostic wording/code above is a mypy observation.

## Visual interpretation

```text
same provider + same preview body
                 |
       parameter contract changes
                 |
    +------------+-------------+
    |                          |
static obligation changes   runtime still calls read
```

### How to read this visual

Follow the common starting point, then compare the two kinds of observation.

### Key insight

An unnecessary dependency can matter before execution, even when the particular call still works.

### Simplification or limitation

Conceptual explanation, not an execution scheduler or CPython memory layout. The two results
are produced separately; Python does not call mypy before the preview.

## Design conclusion

Keep the client's declared capability aligned with its real workflow. Do not fix the static
error by adding false write/remove promises to a reader. Also inspect imports and behaviour;
changing an annotation alone does not establish those boundaries.

## Limitations

This is a small synchronous, in-memory probe. It does not measure compilation time, deployment
cost, performance, security, or concurrency. Other checkers may format diagnostics differently.
Dynamic code, casts, and untyped call sites can evade static checks; this probe deliberately
uses fully checked call sites. See [maintainer validation](../../VALIDATION.md) for compatibility
and broader verification records, not learner evidence.

## Sources

1. [Python 3.14 typing documentation](https://docs.python.org/3.14/library/typing.html).
2. [Typing specification: protocols](https://typing.python.org/en/latest/spec/protocol.html).
