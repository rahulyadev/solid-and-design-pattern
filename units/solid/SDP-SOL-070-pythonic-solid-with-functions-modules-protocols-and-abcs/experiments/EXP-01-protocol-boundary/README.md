# EXP-01 — A Protocol check is not a contract check

| Field | Value |
|---|---|
| Owning unit | [SDP-SOL-070](../../README.md) |
| Curriculum | [CURRICULUM.md](../../../../../CURRICULUM.md#sdp-sol-070) |
| Precise question | Does runtime Protocol membership establish signature compatibility or the promised result? |
| Classification | Standard library and Python call semantics |
| Status | Interpreted by maintainer; no learner attempt recorded |

## Why observation is necessary

Three checks are easy to confuse: whether a member exists, whether a call can be made, and
whether the result keeps a promise. The probe makes each outcome visible using independent
implementations, including one with the right name but the wrong signature.

## Hypothesis

> A runtime member check will accept both a wrong signature and a wrong implementation;
> the subsequent call and explicit result check will distinguish those failures.

The known business promise for this small probe is to concatenate the supplied prefix and
title without dropping either. This promise is our example contract, not a Protocol feature.

## Environment

```text
Date: 2026-08-30
Operating system: Linux 7.0.0-30-generic, glibc 2.43
Architecture: x86_64
Canonical sys.version: 3.14.7 (main, Aug 25 2026, 14:02:56) [Clang 22.1.3 ]
Compatibility sys.version: 3.11.16 (main, Aug 25 2026, 14:00:53) [Clang 22.1.3 ]
sys.implementation.name: cpython on both
sys.implementation.cache_tag: cpython-314 / cpython-311
Runtime dependencies: standard library only
Test tool: pytest 8.4.2 from the repository lock
Relevant flags: PYTHONDONTWRITEBYTECODE=1; no optimization flag
```

## Controls and variables

- Controlled: the title `Luna`, prefix `Hi: `, protocol declaration, call, and result check.
- Changed: the provider's member presence, signature, or body; runtime decorator opt-in.
- Measured: membership outcome, call failure category, and the example postcondition.
- Both interpreters ran the same source. No dynamic attributes or monkey-patching were used.

## Reproduction command

Apply the external-environment setup in the [practice guide](../../practice/README.md#commands),
then run from the repository root:

```bash
uv run --locked python units/solid/SDP-SOL-070-pythonic-solid-with-functions-modules-protocols-and-abcs/experiments/EXP-01-protocol-boundary/protocol_probe.py
uv run --locked pytest -q -p no:cacheprovider units/solid/SDP-SOL-070-pythonic-solid-with-functions-modules-protocols-and-abcs/experiments/EXP-01-protocol-boundary
```

Use the guide's separate Python 3.11 environment to repeat the same commands on that runtime.
[Probe source](protocol_probe.py) · [Behaviour checks](test_protocol_probe.py)

## Predicted result

An ordinary Protocol rejects `isinstance` use. The runtime-checkable Protocol accepts the
three objects with `make`. The correct implementation keeps the result contract, the wrong
signature raises `TypeError`, and the wrong body returns an incorrect result.

## Observed result

Both CPython 3.14.7 and 3.11.16 produced:

```text
ordinary Protocol isinstance: TypeError
GoodMaker: member check=True; call=contract kept
WrongSignature: member check=True; call=TypeError
IgnoresTitle: member check=True; call=contract broken
object: member check=False; call=missing member
```

## Interpretation

1. Membership and callability with this signature are different observations.
2. Call success and business correctness are also different observations.
3. `observe` deliberately accepts `object`, then uses a runtime check. Passing its static
   checks does not establish that `WrongSignature` structurally matches a statically typed
   parameter. A runtime narrowing operation is not signature verification.
4. This one postcondition is evidence about one input, not proof of all future behaviour.

## Visual interpretation

```text
candidate --> member check --> actual call --> expected result check
                   yes           TypeError       not reached
                   yes           returns         contract broken
                   yes           returns         contract kept
```

### How to read this visual

Each row after the arrows is a different candidate. Follow the checks left to right;
failure at one stage prevents meaningful success at the next stage.

### Key insight

No earlier check replaces the later check.

### Simplification or limitation

This is a conceptual diagnostic sequence, not Python's internal execution algorithm.
It omits the missing-member and undecorated-Protocol branches shown in the actual output.

## Design conclusion and limitations

Do not use runtime Protocol membership as plugin validation. Test the required call and
behaviour at an appropriate boundary, and use static checking for statically known code.
The probe catches `TypeError` only to report the deliberate mismatch; it is not a general
exception-handling policy for production providers.

Python 3.12 changed runtime Protocol attribute lookup to use static lookup and froze the
checked member set at class creation. These results cover ordinary methods on the two
recorded versions; they do not generalize to every descriptor or dynamic attribute provider.

## Sources

1. [Python typing documentation: runtime_checkable](https://docs.python.org/3.14/library/typing.html#typing.runtime_checkable): the member-check contract and Python 3.12 changes.
2. [Typing specification: Protocols](https://typing.python.org/en/latest/spec/protocol.html): static structural assignability, distinct from this runtime observation.
