# EXP-02 — Small operations, shared invariant

| Field | Value |
|---|---|
| Owning unit | [SDP-SOL-060](../../README.md) |
| Curriculum | [CURRICULUM.md](../../../../../CURRICULUM.md#sdp-sol-060) |
| Precise question | What happens when two consumers separate checking a quota from consuming it? |
| Classification | Python execution of a deterministic schedule; design-level interpretation |
| Status | Interpreted by the maintainer; learner prediction not recorded |

## Why observation is necessary

A method-by-method review misses the collaboration. Each consumer sees one available token
before either consumer spends it. Executing that schedule makes the shared invariant visible.
There is no timing dependency, real thread, lock, database, or GIL argument.

## Hypothesis

Teaching prediction: check/check/consume/consume accepts two requests for one token. Two
serial `try_consume` calls accept one. This compares API collaboration under the stated
schedule; it does not establish the atomicity of Python method bodies in production.

## Environment

```text
Date: 2026-08-30
Operating system: Linux 7.0.0-30-generic, glibc 2.43
Architecture: x86_64
Python version: CPython 3.14.7
sys.version: 3.14.7 (main, Aug 25 2026, 14:02:56) [Clang 22.1.3 ]
sys.implementation: cpython; cache_tag=cpython-314; version=3.14.7 final
Dependencies: probe uses standard library only; pytest 8.4.2 for checks
Relevant flags: PYTHONDONTWRITEBYTECODE=1; pytest cache disabled; tool caches outside Worktree
```

## Controls and variables

- Controlled: one initial token, two consumers, no interleaving inside a method body.
- Changed: split calls versus a cohesive state transition.
- Measured: acceptance decisions and remaining tokens.
- Additional controls: zero tokens and enough tokens, where the split schedule does not fail.

## Reproduction command

From the repository root, apply the [practice environment exports](../../practice/README.md#commands):

```bash
uv run --locked python units/solid/SDP-SOL-060-solid-interactions-tensions-and-trade-offs/experiments/EXP-02-split-operation/split_probe.py
uv run --locked pytest -q -p no:cacheprovider units/solid/SDP-SOL-060-solid-interactions-tensions-and-trade-offs/experiments/EXP-02-split-operation
```

## Predicted result

The split schedule should reach negative one token. The cohesive serial schedule should
reject the second request and leave zero tokens.

## Observed result

Executed by the maintainer on the canonical runtime:

```text
split: accepted=(True, True); remaining=-1
cohesive: accepted=(True, False); remaining=0
schedule: calls interleave; method bodies do not
```

## Interpretation

1. Narrow operations do not guarantee a safe collaboration.
2. The split API allowed the callers to act on an outdated check.
3. A cohesive operation provides a place to enforce the invariant for serial callers.
4. Real concurrency would require an appropriate synchronization mechanism inside that
   boundary. Calling a method “cohesive” or “atomic” does not supply one.

## Visual interpretation

```text
Split schedule, one token:
A checks: yes → B checks: yes → A consumes: 0 → B consumes: -1

Cohesive serial schedule, one token:
A tries: accepted, 0 → B tries: rejected, 0
```

### How to read this visual

Read each row left to right. Arrows show the exact schedule in the script. The two rows are
separate runs with fresh state, not simultaneous threads.

### Key insight

Segregate what clients need without transferring responsibility for a shared invariant to them.

### Simplification or limitation

This is a deterministic execution trace. It permits interleaving between calls only, so the
second row is not evidence of thread safety, database isolation, or distributed correctness.

## Design conclusion

ISP is about dependencies on capabilities, not maximizing the number of tiny operations.
SRP does not require separating checking from changing the state it governs. Keep the
invariant's owner clear; choose actual synchronization only when the runtime model requires it.

## Limitations

- The toy quota has no time window, refill, persistence, user identity, or retry model.
- Public mutable fields make the state easy to inspect, not suitable for a production limiter.
- Real threads could interleave inside `try_consume`; this code must not be advertised as a thread-safe limiter.
- No performance benchmark or empirical claim about production failure frequency was made.
- Tests that confirm negative capacity validate the intentional counterexample, not its safety.

## Sources

1. [Martin, ISP: class versus object interfaces](https://d3s.mff.cuni.cz/f/teaching/nprg043/extras/martin96-interface_segregation_principle.pdf): different client views can share one implementation.
2. [Martin, SRP](https://blog.cleancoder.com/uncle-bob/2014/05/08/SingleReponsibilityPrinciple.html): coherent change responsibility.

The quota schedule and its interpretation are original. No source is claimed to prove
thread-level atomicity for this Python example.
