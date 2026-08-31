# EXP-02 — State ownership, deferred effects, and replay

| Field | Value |
|---|---|
| Owning unit | [SDP-PYT-010](../../README.md) |
| Curriculum | [CURRICULUM.md](../../../../../CURRICULUM.md#sdp-pyt-010) |
| Precise question | What do callable aliasing, action preparation, failure, and replay actually guarantee? |
| Classification | Python language state binding plus the explicit contract of our synthetic runner. |
| Status | Reproduced on both recorded runtimes by the maintainer. |

## Why observation is necessary

A closure can look stateless at its call site. A deferred action can look like a queue
message. Neither appearance tells us whether two calls share state or whether replay is
safe. The probe exposes actual counts and effects instead of inferring them from syntax.

## Hypothesis

An alias to one counter shares its count; a second factory call starts independently.
Preparing our actions has no effect. Sequential execution stops on the first exception,
but completed effects remain, including an effect performed by the failing action.
Replaying an action performs its effect again. These are maintainer predictions only.

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

- Controlled: one process, ordered calls, immutable byte payloads, in-memory recording.
- State control: first counter, an alias to it, and a separately constructed second counter.
- Failure injection: the sink appends `events:stop`, then raises the exact stored OSError.
- Replay: execute the already-successful `ready` action one additional time.
- Measured: counter results, effects before execution, effects after failure/replay,
  and whether the original exception object reached the caller.

## Reproduction command

After the external environment setup in [practice](../../practice/README.md):

```bash
uv run --locked python units/pythonic/SDP-PYT-010-functions-closures-callable-objects/examples/effects_probe.py
```

Repeat in the compatibility environment with `--python 3.11` after `--locked`.
Source: [effects_probe.py](../../examples/effects_probe.py); runner and actions:
[callable_tools.py](../../examples/callable_tools.py).

## Predicted result

The first/alias/second/first counter schedule should return `[1, 2, 1, 3]`. Preparation
should leave an empty record. Failure should leave `ready` and `stop`, with `later` absent.
Replay should append a second `ready` record, and the original exception should propagate.

## Observed result

Actual stdout was identical on CPython 3.14.7 and 3.11.16:

```json
{
  "counter_calls_first_alias_second_first": [
    1,
    2,
    1,
    3
  ],
  "before_execution": [],
  "after_failure": [
    "events:ready",
    "events:stop"
  ],
  "same_exception": true,
  "after_replay": [
    "events:ready",
    "events:stop",
    "events:ready"
  ]
}
```

## Interpretation

1. The alias and first counter are one callable, not two independent owners.
2. A separately created counter has separate state in this implementation.
3. Our factory performs no write. Deferral is a property of its code, not every callable factory.
4. An exception reports failure, not the absence of effects. The runner supplies no rollback.
5. A second invocation repeats the effect because this action has no deduplication policy.

## Visual interpretation

```text
prepare actions      run ready       run stop           run later       replay ready
records: []       -> [ready]       -> [ready, stop]   -> not reached  -> [ready, stop, ready]
                                        raises
```

### How to read this visual

Read in call order. Arrows mean later observations. The `stop` action records first and
then raises; normal execution never reaches `later`. Replay happens explicitly after the catch.

### Key insight

A callable can package an action, but failure recovery and replay safety require separate design.

### Simplification or limitation

This is one synthetic sequential trace, not a transaction log or distributed-delivery guarantee.
There is no broker, persistence, external writer, retry loop, lock, or compensating action.

## Design conclusion

Name the callable's owner and resource lifetime. For effects, document whether failures
can happen before or after a visible change, and decide retry/idempotency at the proper
boundary. Do not add a generic catch-and-retry wrapper merely because the action is callable.

## Limitations

The probe does not test races, cancellation, process restarts, network ambiguity, or
exactly-once delivery. A different sink could fail before recording; the worked-example
tests cover both before-effect and after-effect failures. No learner attempt is recorded.

## Sources

1. [Python execution model: name resolution](https://docs.python.org/3.14/reference/executionmodel.html#resolution-of-names) — enclosing bindings and `nonlocal`.
2. [Our executed runner and tests](../../examples/test_callable_tools.py) — ordering,
   error identity, replay, and retained effects are claims about this code, not Python transactions.
