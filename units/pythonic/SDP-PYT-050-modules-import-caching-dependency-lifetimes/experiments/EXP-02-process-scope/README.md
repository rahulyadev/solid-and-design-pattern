# EXP-02 — Import-cache scope across worker processes

| Field | Value |
|---|---|
| Owning unit | [SDP-PYT-050](../../README.md) |
| Curriculum | [CURRICULUM.md](../../../../../CURRICULUM.md#sdp-pyt-050) |
| Precise question | Do two overlapping fresh Python processes share one import execution or reuse only inside each interpreter? |
| Classification | Python process and import-system behavior |
| Status | Reproduced |

## Why observation is necessary

Backend discussions often shorten “same cached module in an interpreter” to “one global on the
server.” A server may run several worker processes. The distinction is architectural: an in-memory
client, lock, registry, or Singleton does not automatically cross that boundary.

## Hypothesis

> Each fresh child will execute the synthetic target once and reuse it for its own second import.
> The two overlapping children will have distinct process IDs, demonstrating separate runtime
> boundaries rather than one shared module object.

## Environment

```text
Date: 2026-09-06
Operating system: Linux 7.0.0-31-generic
Architecture: x86_64
Primary Python: CPython 3.14.7, Clang 22.1.3, glibc 2.43
Compatibility reproduction: CPython 3.11.16, Clang 22.1.3, glibc 2.43
Dependencies: Python standard library only
Relevant flags: two direct subprocesses; no multiprocessing start-method selection
```

## Controls and variables

- Controlled: same interpreter executable per run, same child script, same target name, two child
  processes started before collection, and normalized output.
- Changed: process boundary only.
- Measured: distinct child PIDs, target execution count inside each child, and identity reuse for
  two imports inside each child.

## Reproduction command

From the repository root:

```bash
uv run --locked python units/pythonic/SDP-PYT-050-modules-import-caching-dependency-lifetimes/examples/process_scope_probe.py
/tmp/sdp-pyt-040-tools.b57yty/venv311/bin/python units/pythonic/SDP-PYT-050-modules-import-caching-dependency-lifetimes/examples/process_scope_probe.py
```

## Predicted result

```text
two distinct children
target execution count 1 in each child
second import reuses target inside each child
```

## Observed result

Both CPython 3.14.7 and CPython 3.11.16 produced this normalized result:

```json
{
  "child_processes": 2,
  "distinct_processes": true,
  "each_process_executes_target_once": true,
  "each_process_reuses_its_own_module": true
}
```

Raw PIDs were used only for the distinctness comparison and intentionally were not recorded as
stable output.

## Interpretation

1. The result directly shows two process identities, one first execution in each, and cache reuse
   for the second import inside each child.
2. It supports the inference that an ordinary in-memory module object is worker-local in this
   direct-subprocess setup.
3. It does not prove a particular web server's worker model, multiprocessing start method,
   subinterpreter behavior, host topology, or distributed coordination guarantee.

## Visual interpretation

```text
parent probe
├─ child process P1 ──> interpreter/cache P1 ──> target executes once; second import reuses
└─ child process P2 ──> interpreter/cache P2 ──> target executes once; second import reuses

no observed cache edge between P1 and P2
```

### How to read this visual

Follow each branch independently. “Once” is inside that child observation, not once for the host.

### Key insight

Process-local sameness cannot enforce a deployment-wide invariant.

### Simplification or limitation

This is a direct subprocess experiment, not a memory-layout diagram. It does not use `fork`,
`spawn`, `forkserver`, shared memory, a process manager, containers, or multiple hosts.

## Design conclusion

Own app resources once per actual worker/app instance when that is correct. For a job, lease, or
business key that must be unique across workers, use an external coordinator with an explicit
failure and expiry contract.

## Limitations

- Process overlap makes distinct live PIDs deterministic for the observation, not their values.
- The probe normalizes away scheduling and timing.
- Import behavior inside forked children may inherit prior memory differently; the architectural
  conclusion still requires the deployment's documented worker/start model.
- No cluster or container boundary was executed.

## Sources

1. Python Software Foundation, [Python 3.14 module cache](https://docs.python.org/3.14/reference/import.html#the-module-cache).
2. Python Software Foundation, [Python 3.14 multiprocessing contexts and start methods](https://docs.python.org/3.14/library/multiprocessing.html#contexts-and-start-methods).
