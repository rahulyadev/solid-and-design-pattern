# Practice — SDP-PYT-080 single-dispatch incident digests

| Field | Value |
|---|---|
| Unit note | [SDP-PYT-080](../README.md) |
| Starter | [incident_digest_lab.py](incident_digest_lab.py) |
| Behavior tests | [test_incident_digest_lab.py](test_incident_digest_lab.py) |
| Test command | `uv run --locked pytest -q -p no:cacheprovider units/pythonic/SDP-PYT-080-singledispatch-open-function-extension/practice` |
| State | Unsolved |

## Scenario and change pressure

An operations service turns a few incident values into short digests. The small `isinstance`
conditional works and its behavior tests pass. A security team now owns a new frozen data type,
`SecurityFinding`, in another module. It must add digest behavior without repeatedly editing the
operations module. Startup wiring can explicitly import one approved support module; automatic
package discovery is not required.

Your goal is not merely to spell `@singledispatch`. Decide whether runtime type is the honest
selection key, preserve the existing contract, make the default deliberate, and give registration
one visible owner. Keep the exercise synchronous and in memory.

## Predict before running

Record answers before executing anything:

1. Which branch handles `bool` if an `int` implementation exists but `bool` does not?
2. Would changing only `context.audience` change the selected implementation?
3. Should an unknown incident produce a generic string or fail closed here?
4. If two imported support modules register the same exact type, what policy should this
   application use?
5. Does annotating a handler with `list[ServiceAlert]` make runtime dispatch inspect list items?
6. What must be tested directly: only the generic call, or each registered implementation too?

No learner prediction has been recorded by the maintainer.

## Run the starter

From the repository root:

```bash
uv run --locked python units/pythonic/SDP-PYT-080-singledispatch-open-function-extension/practice/incident_digest_lab.py
uv run --locked pytest -q -p no:cacheprovider units/pythonic/SDP-PYT-080-singledispatch-open-function-extension/practice
```

Write down the exact runtime, output, and test count. The maintainer's validation does not count as
your prediction, attempt, explanation, or learning evidence.

## Observe the existing design

Before refactoring, identify:

- the value that actually selects behavior;
- the behavior shared by every branch;
- validation and error behavior that must not drift;
- the one place currently reopened for each supported type; and
- whether the two context fields are dispatch keys or ordinary handler inputs.

The current conditional is not automatically wrong. It becomes costly only under the stated
cross-module extension pressure.

## Explain the mechanism in your own words

Without copying the unit note, explain:

1. what the base/default implementation should do;
2. why only the first argument controls selection;
3. how inheritance changes the selected implementation;
4. why a type annotation for container items is not a runtime dispatch rule;
5. when registration happens; and
6. who owns the resulting registry and startup order.

## Refactor

Preserve the existing public call and behavior while creating the smallest justified extension
seam. The target design should let an explicitly imported support module add `SecurityFinding`
behavior without editing the generic function's core module.

Required constraints:

- use the runtime type of the first argument as the only dispatch key;
- keep a deliberate base/default implementation;
- preserve every existing behavior test;
- add direct tests for each implementation as well as end-to-end generic calls;
- use both an annotation-inferred and an explicit registration form somewhere appropriate;
- make duplicate exact-type policy explicit at the application boundary;
- expose enough registry or dispatch information to diagnose startup configuration;
- do not scan installed packages or build entry-point discovery; and
- do not change `PROGRESS.md` from this practice directory.

Do not move shared validation into every handler by copy and paste. Do not use a metaclass,
framework container, Visitor hierarchy, or custom multimethod package.

## Required edge cases

- empty and surrounding-space text;
- Unicode, colon, and literal-pipe content;
- severities `1`, `5`, and values outside that range;
- an unregistered subclass and then an exact registration for that subclass;
- `str` and `bytes` sharing behavior;
- an unknown type reaching the deliberate default;
- a handler exception remaining distinguishable from a missing registration;
- two support modules attempting the same exact registration;
- registry inspection before request handling; and
- two contexts proving that later arguments affect output but not selection.

## Rahul's attempt

- Attempt file: —
- Prediction: —
- Chosen registry owner: —
- Duplicate policy: —
- Rejected alternative: —
- Runtime evidence: —
- Test result: —

## Progressive hints

No hints are released. Ask for one at a time after recording an attempt.

## Observe and explain after refactoring

1. Which function object owns the registry?
2. Which exact types are registered, including the base `object` entry?
3. What does `dispatch(SecurityFinding)` return before and after support is installed?
4. How is a missing registration distinguished from an exception raised inside a selected handler?
5. Why is explicit import wiring sufficient for this requirement?
6. What would force a move to discovery, Strategy, methods, or Visitor?
7. Which abstraction could still be removed?

## Vary

Choose one change and defend whether the mechanism should change:

- selection depends on incident type **and** output channel;
- third-party distributions must be discovered from installed package metadata;
- every incident type owns several evolving operations;
- the supported incident set is closed and exhaustive; or
- registration can change while multiple worker threads serve requests.

State what changes in the registry owner, public contract, tests, startup, and observability.

## Troubleshooting

- Run commands from the repository root so pytest can resolve the sibling starter module.
- Put the dispatching value first; `singledispatch` ignores later argument types.
- Register runtime classes such as `list`, not parameterized aliases such as `list[int]`.
- If a support import appears ineffective, inspect `dispatch(Type)` and `registry` before guessing.
- If tests influence each other, create a fresh generic function per isolation-sensitive test instead
  of mutating a shared production registry.
- If the requested key is a string or enum rather than a type, prefer a callable dictionary.

## Closure

Add only after Rahul closes the exercise.

- Final learner solution: —
- Optional comparison solution: —
- Trade-offs: —
- Remaining weakness: —
- Evidence link for `PROGRESS.md`: —
