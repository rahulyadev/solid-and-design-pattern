# EXP-02 — ABC membership, construction, and behaviour

| Field | Value |
|---|---|
| Owning unit | [SDP-SOL-070](../../README.md) |
| Curriculum | [CURRICULUM.md](../../../../../CURRICULUM.md#sdp-sol-070) |
| Precise question | What does an ABC enforce, and what does virtual registration leave unchanged? |
| Classification | Standard library |
| Status | Interpreted by maintainer; no learner attempt recorded |

## Why observation is necessary

“It is an instance of the ABC” can mean regular inheritance or virtual registration.
Neither statement alone establishes that a write stored anything. This experiment separates
those facts with a tiny in-memory buffer; no filesystem or network is involved.

## Hypothesis

> A regular subclass missing the abstract hook cannot be constructed; a registered class
> gains membership without methods; a no-op override can be constructed but loses the payload.

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

- Controlled: `BufferBase`, the `append` promise, one `b"sample"` payload, and result inspection.
- Changed: missing override, unrelated registered class, no-op override, or storing override.
- Measured: construction outcome, runtime membership, member availability, and record count.
- Each virtual-observation call creates a fresh unrelated class before registering it.

## Reproduction command

Apply the external-environment setup in the [practice guide](../../practice/README.md#commands),
then run from the repository root:

```bash
uv run --locked python units/solid/SDP-SOL-070-pythonic-solid-with-functions-modules-protocols-and-abcs/experiments/EXP-02-abc-boundary/abc_probe.py
uv run --locked pytest -q -p no:cacheprovider units/solid/SDP-SOL-070-pythonic-solid-with-functions-modules-protocols-and-abcs/experiments/EXP-02-abc-boundary
```

Use the separate Python 3.11 environment described in that guide for the compatibility run.
[Probe source](abc_probe.py) · [Behaviour checks](test_abc_probe.py)

## Predicted result

The incomplete nominal subclass is blocked. The unrelated registered object passes runtime
membership yet lacks both the required hook and the base implementation. The no-op subclass
stores zero records, while the honest implementation stores one.

## Observed result

Both CPython 3.14.7 and 3.11.16 produced:

```text
incomplete nominal subclass: blocked by TypeError
virtual subclass: membership=True; append=False; inherited count=False
DroppingBuffer: stored=0
MemoryBuffer: stored=1
```

## Interpretation

1. The abstract-method gate blocks this incomplete regular subclass.
2. Registering the unrelated class changes membership without adding the required operation
   or the concrete `count` method.
3. The no-op class supplies the override and passes construction, but violates our explicit
   stored-record postcondition. An ABC is not an LSP proof.
4. The tests also cover an empty payload and duplicate payloads for the storing implementation.

## Visual interpretation

```text
Missing override   --> cannot construct
Virtual membership --> construct, but no inherited append/count
No-op override     --> construct, but no stored payload
Storing override   --> construct, and the observed payload is stored
```

### How to read this visual

Read each line independently. The arrow leads from a design choice to the observed result.

### Key insight

Membership, method availability, and behavioural correctness are different claims.

### Simplification or limitation

The visual is conceptual and scoped to these four implementations. It omits ABC caching,
metaclass internals, and custom subclass hooks. The experiment makes no claims about them.

## Design conclusion and limitations

Use an ABC when your owned family benefits from shared code or required extension hooks.
Do not register a class as a substitute for implementing its missing behaviour. Use explicit
contract tests for the promises that matter to a caller.

The constructor-reporting helper catches `TypeError` for this known incomplete class; it
does not identify why every arbitrary constructor might fail. Runtime registration also
does not establish that a static type checker will accept every use of the registered class.
The buffer is a synchronous, local example with no durability or thread-safety guarantee.

## Sources

1. [Python abc documentation](https://docs.python.org/3.14/library/abc.html): regular abstract methods, virtual registration, and inherited implementation boundaries.
