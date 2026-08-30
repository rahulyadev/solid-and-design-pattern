# EXP-01 — Import isolation is different from injection

| Field | Value |
|---|---|
| Owning unit | [SDP-SOL-050](../../README.md) |
| Curriculum | [CURRICULUM.md](../../../../../CURRICULUM.md#sdp-sol-050) |
| Precise question | Can policy import and run without the database driver when its collaborator is injected? |
| Classification | Python import behaviour, subprocess standard-library use, and design-level interpretation |
| Status | Run and interpreted by the maintainer; no learner prediction recorded |

## Why observation is necessary

A method can use only `units_available` while its module still imports an entire concrete
integration. A test in a long-lived interpreter can also hide import work behind the module
cache. This probe starts a separate interpreter for each case.

## Hypothesis

> Injecting a collaborator does not eliminate concrete module imports. A policy that imports
> only its own contract can still run with a small fake when the database driver is unavailable.

This is the experiment's proposed hypothesis, not Rahul's recorded prediction.

## Environment

```text
Date: 2026-08-30
Operating system: Linux 7.0.0-30-generic, glibc 2.43
Architecture: x86_64
Python version: CPython 3.14.7
sys.version: 3.14.7 (main, Aug 25 2026, 14:02:56) [Clang 22.1.3 ]
sys.implementation.name: cpython
Runtime dependencies: Python standard library and the unit's example modules
Dev environment: pytest 8.4.2, mypy 1.20.2, Ruff 0.16.1, Hypothesis 6.165.2
Child flags: -I -B; explicit example-directory path; 10-second timeout
```

The probe was also reproduced with CPython 3.11.16 in a separate environment using the same
lockfile. Its `sys.version` was `3.11.16 (main, Aug 25 2026, 14:00:53) [Clang 22.1.3 ]`.
The three output lines were identical. This establishes the supplied probe's compatibility,
not equivalence of every import or typing feature across those versions.

## Controls and variables

- **Controlled:** fresh process, same interpreter, same example directory, blocked driver.
- **Changed:** the concrete-dependent module versus the policy-contract module.
- **Observed:** import outcome and, where import succeeds, the actual call and returned plan.
- **Not measured:** timing, memory, real service failure rates, or production resilience.

The child assigns `None` to `sys.modules["sqlite3"]`. Python documents that this makes
an import of that name raise `ModuleNotFoundError`. The modification is restricted to the
disposable process; it does not uninstall a driver or change the parent's module cache.
[Python import reference, module cache](https://docs.python.org/3.14/reference/import.html#the-module-cache).

## Reproduction command

First apply the [external-environment setup](../../practice/README.md#commands), then run
from the repository root:

```bash
uv run --locked python units/solid/SDP-SOL-050-dependency-inversion-principle/experiments/EXP-01-import-isolation/import_isolation.py
```

The [probe](import_isolation.py) imports the actual example files. It does not substitute
an unrelated miniature implementation for either policy. The fake is local to the child.

## Predicted result

The concrete module should fail before its function can be called. The inverted module
should import successfully and calculate a shortage through the supplied fake.

## Observed result

The maintainer executed the command on the environment above and observed:

```text
concrete: import blocked (sqlite3)
runtime: policy -> fake.units_available(BOLT)
inverted: {'BOLT': 5}
```

The command exited successfully: the intended concrete import failure is caught only when
the missing module is exactly `sqlite3`. Unexpected import failures or subprocess failures
are not converted into successful observations.

## Interpretation

1. **Direct observation:** importing the concrete counterexample reaches the blocked driver.
2. **Direct observation:** the other policy runs through the fake while the driver remains blocked.
3. **Design inference:** separating the policy contract removed this infrastructure requirement
   from the policy's import path. Injection alone did not do that in the counterexample.
4. **Not established:** all possible dependencies, production uptime, transaction semantics,
   type-only independence, or arbitrary adapter correctness.

## Visual interpretation

```text
concrete module ──imports──> SQLite adapter ──imports──> blocked driver
policy module   ──imports──> stock contract
policy function ───calls───> supplied fake ──returns───> 3
```

### How to read this visual

The first two rows show import relationships. The last row shows a later runtime call.
These rows are different kinds of evidence, not one combined call stack.

### Key insight

Policy can call a concrete object without importing that object's implementation module.

### Simplification or limitation

The diagram omits interpreter startup and standard-library imports. The real SQLite adapter
cannot work when its driver is blocked; only the isolated policy plus a fake is being exercised.

## Design conclusion and limitations

Use import isolation as a focused architectural regression. Also inspect types, values,
exceptions, dynamic imports, and package initializers. Passing this probe cannot prove that
a type-only vendor reference or a vendor-shaped contract is independent of the vendor.

The subprocess mechanism is not a production technique for dependency injection or fault
tolerance. It is an experimental control. There are no benchmarks or CPython-specific
memory claims. The [shared contract tests](../../examples/test_replenishment.py) separately
exercise the actual memory and SQLite adapters.

## Sources

- [Python import reference: module cache](https://docs.python.org/3.14/reference/import.html#the-module-cache): documented import blocking used as the control.
- [Robert C. Martin, The Dependency Inversion Principle](https://www.cs.utexas.edu/~downing/papers/DIP-1996.pdf): source-dependency interpretation, not a claim about this experiment's output.
