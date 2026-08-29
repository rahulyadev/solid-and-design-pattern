# Practice — SDP-FND-100 Modules, package boundaries, and circular dependencies

| Field | Value |
|---|---|
| Unit note | [SDP-FND-100](../README.md) |
| Curriculum | [CURRICULUM.md](../../../../CURRICULUM.md#sdp-fnd-100) |
| Evidence target | E+I+D+(X)+T |
| Attempt required before solution | Yes |
| Focused test command | `uv run pytest -q units/foundations/SDP-FND-100-modules-package-boundaries-circular-dependencies/practice` |
| Status | Not attempted |

The starter, defect-characterization suite, dependency graph, and four controlled runtime
experiments have been run to verify the artifact. That proves only that the supplied files execute
as documented. It does **not** count as Rahul's prediction, package-boundary analysis, refactoring
attempt, alternative comparison, or learning evidence.

## Learning question

How can a Python backend assign stable meaning, application orchestration, adapter behavior, and
concrete wiring to modules that depend in one intentional direction—without hiding the cycle in a
local import, creating a generic `common.py`, or building an interface hierarchy for one function?

## Lab cycle

```text
predict → run → observe → trace import timeline → draw source graph
        → assign ownership → refactor → enforce boundary → vary
```

Do not begin by moving `from .email_adapter import send_receipt` inside `checkout()`. That may delay
the failure, but it neither decides who owns the result contract nor removes the application
service's concrete adapter choice.

## Starter files

```text
practice/
├── README.md
├── run_checkout_lab.py
├── test_checkout_lab.py
├── dependency_graph_experiment.py
├── module_cache_probe.py
├── module_cache_experiment.py
├── cycle_timing_experiment.py
├── execution_context_experiment.py
├── package_init_experiment.py
├── test_import_experiments.py
├── checkout_lab/
│   ├── __init__.py
│   ├── __main__.py
│   ├── model.py
│   ├── service.py
│   └── email_adapter.py
├── cycle_examples/
│   ├── __init__.py
│   ├── from_cycle/
│   │   ├── __init__.py
│   │   ├── alpha.py
│   │   └── beta.py
│   └── module_cycle/
│       ├── __init__.py
│       ├── alpha.py
│       └── beta.py
├── execution_probe/
│   ├── __init__.py
│   ├── helper.py
│   └── report.py
└── eager_package/
    ├── __init__.py
    ├── public_api.py
    └── leaf.py
```

- `checkout_lab/` is the unsolved package-boundary refactoring.
- `run_checkout_lab.py` and `checkout_lab/__main__.py` both expose its deterministic startup
  failure.
- `test_checkout_lab.py` preserves stable model behavior and characterizes the broken import in
  subprocesses so pytest collection remains healthy.
- `dependency_graph_experiment.py` parses local imports with `ast` and reports a directed cycle.
- The remaining scripts isolate Python import-cache, partial-initialization, execution-context, and
  package-initializer behavior.
- `test_import_experiments.py` makes every reported experiment outcome reproducible.

All orders, identifiers, SKUs, prices, provider references, and module names are synthetic. The
lab performs no network request, reads no credential, and contains no production code or data.

## Problem

The package intends to support one checkout use case:

1. construct validated immutable order values;
2. calculate an exact decimal total;
3. complete checkout;
4. send one receipt notification;
5. return the result and notification reference;
6. expose the use case through `python -m checkout_lab`.

The stable model already works. The service and adapter do not import:

```text
checkout_lab.service
    imports checkout_lab.email_adapter.send_receipt

checkout_lab.email_adapter
    imports checkout_lab.service.CheckoutResult

checkout_lab.service
    has not defined CheckoutResult yet
```

The cycle also reveals responsibility problems:

- application policy chooses its concrete email adapter;
- the adapter needs an application-owned result merely to format one identifier;
- construction/wiring has no outer owner;
- package startup cannot reach a usable state;
- tests cannot import the service directly without failing collection;
- swapping email for an audit/event adapter would require editing application policy.

The goal is not merely a successful import. The final graph must make the intended direction and
public contract explainable.

## Current source dependency graph

```text
checkout_lab.__main__ ─────> checkout_lab.model
          │
          └───────────────> checkout_lab.service
                                      │
                                      ├────> checkout_lab.model
                                      │
                                      ▼
                            checkout_lab.email_adapter
                                      │
                                      └────> checkout_lab.service

cycle: service → email_adapter → service
```

### How to read this visual

Every arrow is a source import found by the AST experiment. Begin at `__main__` and follow the
service edge. Service reaches the concrete adapter, which returns to service to obtain
`CheckoutResult`.

### Key insight

`model.py` is already dependency-light and stable. The cycle is between orchestration and a
concrete delivery detail; simply relocating syntax must not blur that ownership fact.

### Simplification or limitation

The graph contains only imports inside `checkout_lab`. It does not show standard-library imports,
call direction, dynamic imports, data/schema coupling, test dependencies, or runtime object
construction.

## Current import timeline

```text
run_checkout_lab imports checkout_lab.service
  1. create/cache empty-ish service module
  2. service asks for email_adapter.send_receipt
  3. create/cache email_adapter module
  4. email_adapter asks cached service for CheckoutResult
  5. service has not executed the dataclass definition
  6. ImportError; checkout never begins
```

### How to read this visual

Read downward as execution time. The cycle returns to the same cached service module object; it
does not create a second service. The requested attribute is missing at that moment.

### Key insight

The failure happens before any order or email behavior. Import-time ordering has accidentally
become a precondition of application collaboration.

### Simplification or limitation

This omits parent-package initialization and import-loader details. The exact error text is a
CPython observation; the missing definition and failed import are the portable design concern.

## Stable behavior to preserve

- SKU must contain non-whitespace text.
- Quantity must be positive.
- Unit price must be non-negative.
- Order ID must contain non-whitespace text.
- An order must contain at least one line.
- Totals use `Decimal` and sum every `quantity × unit_price` subtotal.
- Checkout returns the order ID, exact total, and a notification reference.
- No module performs network I/O or reads environment configuration during import.
- The package entrypoint remains invocable with `python -m checkout_lab`.

The current tests prove only the model items and current import failure. The checkout contract must
receive new behavior tests during refactoring.

## Change pressure

The next version must support both an email notifier and a recording test notifier while keeping
checkout policy independent of concrete delivery.

Required meaning:

1. importing the service in a fresh process succeeds;
2. running `python -m checkout_lab` succeeds and prints the deterministic sample result;
3. application policy does not import a concrete email/audit/provider adapter;
4. one explicit outer boundary chooses the concrete notifier and its lifetime;
5. the notification capability contains no operation unused by checkout;
6. adapter code receives only the data it actually needs through a stable contract;
7. model imports remain independent of application and infrastructure;
8. package initialization stays small and performs no I/O;
9. tests use a simple fake/spy without patching provider construction;
10. a static boundary test rejects the forbidden direction and all local cycles;
11. notification failure has a stated contract and no false “checkout succeeded” output;
12. the design remains Python 3.11 compatible.

Do not add a framework, database, message broker, service locator, global container, dynamic plugin
registry, or network client. Those would add unrelated forces.

## Boundary worksheet — complete before code changes

### Stable meaning

- Which module owns `Order` and `OrderLine`?
- Which module should own the checkout return value?
- Does the adapter need the entire return value, or only a smaller receipt/message value?
- Which definitions can change with business policy?
- Which definitions can change with a provider?

### Source direction

- List every current internal import edge.
- Which edge is policy → concrete detail?
- Which edge exists only because of a type annotation?
- Which edge represents real runtime collaboration?
- Which arrows should remain after refactoring?

### Runtime collaboration

- Who constructs the concrete notifier?
- How does checkout receive it?
- Is one callable enough, or does a named multi-operation contract have real value?
- What value crosses the application/adapter boundary?
- What happens if notification fails?

### Package surface

- Which imports should consumers use?
- Should `checkout_lab/__init__.py` re-export anything?
- Which modules remain private implementation details?
- What work is safe during package import?
- How will a clean subprocess exercise the public API?

### Testing and enforcement

- Which existing tests are stable behavior tests?
- Which tests encode the current defect and must be replaced after the contract is written?
- How will a spy prove notification data and call count?
- Which AST edge is forbidden?
- How will the test detect a three-or-more-node cycle?

Do not answer these with only “use dependency injection” or “create `ports.py`.” State ownership
and the required arrow before choosing a mechanism or filename.

## Required refactoring evidence

- Rahul's prediction before the first run.
- The exact first traceback classification and import timeline.
- The current AST source graph and identified cycle.
- A completed stable-meaning/source-direction worksheet.
- The first refactoring attempt preserved at a path or commit.
- A before/after dependency visual with explicit arrow meaning.
- Fresh-process service import succeeds.
- Package `-m` entrypoint succeeds.
- Stable model validation and total behavior still pass.
- Checkout behavior tests cover one recording notifier and exact transmitted value.
- Notification failure behavior is defined and tested.
- No application-policy import of a concrete adapter.
- One complete directed-cycle check and one forbidden-edge rule.
- A written reason for callable, `Protocol`, merged module, or another chosen boundary.
- One rejected local-import, module-style-import, `common.py`, service-locator, or over-interface
  response with a concrete reason.
- Focused tests, Ruff, strict mypy, and repository validation pass.
- One production transfer explains where configuration, adapter construction, and resource
  lifetime would live.

Passing the supplied characterization tests unchanged is insufficient. Two assertions explicitly
expect the broken import and must be replaced only after their old observation and new contract
are recorded.

## Required edge cases

- One order line and several order lines.
- Zero-priced line.
- Blank and whitespace-only SKU.
- Zero and negative quantity.
- Negative unit price.
- Blank and whitespace-only order ID.
- Empty order.
- Exact decimal total such as `2 × 12.50 + 3 × 1.25`.
- Recording notifier receives exactly one value.
- Notifier returns an empty or malformed provider reference, if the contract disallows it.
- Notifier raises its declared failure.
- Service imported before adapter and adapter imported before service in fresh processes.
- Package root and important leaf modules imported independently.
- Entry module invoked with `-m`.
- Boundary checker sees a two-node cycle and a synthetic three-node cycle.
- No test relies on a previous test having populated `sys.modules`.

Do not add discounts, tax, inventory, persistence, retries, async delivery, or provider SDKs until
the import and ownership contract passes these cases.

## Commands

Run from the repository root through the locked environment unless the command says otherwise.

Observe the deliberately failing runner:

```bash
uv run python \
  units/foundations/SDP-FND-100-modules-package-boundaries-circular-dependencies/practice/run_checkout_lab.py
```

Run the package entrypoint from the practice directory so `checkout_lab` is the import package:

```bash
cd units/foundations/SDP-FND-100-modules-package-boundaries-circular-dependencies/practice
uv run python -m checkout_lab
```

Return to the repository root, then run the graph and experiments:

```bash
uv run python \
  units/foundations/SDP-FND-100-modules-package-boundaries-circular-dependencies/practice/dependency_graph_experiment.py
uv run python \
  units/foundations/SDP-FND-100-modules-package-boundaries-circular-dependencies/practice/module_cache_experiment.py
uv run python \
  units/foundations/SDP-FND-100-modules-package-boundaries-circular-dependencies/practice/cycle_timing_experiment.py
uv run python \
  units/foundations/SDP-FND-100-modules-package-boundaries-circular-dependencies/practice/execution_context_experiment.py
uv run python \
  units/foundations/SDP-FND-100-modules-package-boundaries-circular-dependencies/practice/package_init_experiment.py
```

Run checks:

```bash
uv run pytest -q \
  units/foundations/SDP-FND-100-modules-package-boundaries-circular-dependencies/practice
uv run ruff check \
  units/foundations/SDP-FND-100-modules-package-boundaries-circular-dependencies/practice
uv run mypy \
  units/foundations/SDP-FND-100-modules-package-boundaries-circular-dependencies/practice
```

Record actual commands and output. Never describe an expected failure or passing check as observed
until the command has run.

## Prediction before the first run

Write answers before executing anything:

1. Which file begins loading first when `run_checkout_lab.py` imports the service?
2. At what exact statement does the import path return to `service.py`?
3. Is `checkout_lab.service` present in `sys.modules` at that moment?
4. Which service names have been defined, and which requested name has not?
5. Will changing `from .service import CheckoutResult` to `from . import service` make startup
   complete? If yes, what design cycle remains?
6. Would moving the email import inside `checkout()` fail at startup, first call, or not at all?
7. Which module should own the data that crosses the notifier boundary?
8. Is a function parameter, callable type alias, `Protocol`, ABC, or service locator smallest here?
9. What will the AST graph report?
10. Which transitive module loads when only `eager_package.leaf` is requested?
11. What changes between direct internal-file execution and `python -m`?
12. How many times will `module_cache_probe` execute after two imports and after reload?

Record:

- Expected runner result:
- Predicted traceback path:
- Predicted cache state at failure:
- Current source graph:
- Intended source graph:
- Shared-contract owner:
- Concrete-wiring owner:
- Simplest boundary mechanism:
- Rejected alternative:
- Reasoning:

## Artifact-verification observation

Do not copy these observations into the prediction. On 2026-08-29, the supplied artifact was run
with CPython 3.14.7 on Linux x86_64.

Both the direct runner and package entrypoint exited with status `1`. The relevant final error was:

```text
ImportError: cannot import name 'CheckoutResult' from partially initialized module
'checkout_lab.service' (most likely due to a circular import)
```

The runner traceback followed:

```text
run_checkout_lab.py
→ checkout_lab.service
→ checkout_lab.email_adapter
→ checkout_lab.service.CheckoutResult (not yet defined)
```

Focused tests:

```text
..............                                                           [100%]
14 passed in 0.24s
```

Ruff:

```text
All checks passed!
```

Strict mypy:

```text
Success: no issues found in 27 source files
```

Timing is informational and may differ. The exit status, error classification, behavior assertions,
and pass counts are the recorded observations. Passing characterization tests does not approve the
starter design.

## Rahul's attempt

- Prediction:
- First runner output:
- First import-timeline explanation:
- Current source graph:
- Stable-meaning owner:
- Intended source graph:
- Boundary mechanism selected:
- Package public surface:
- Entrypoint/composition owner:
- Failure contract:
- First attempt path or commit:
- Boundary-test design:
- Rejected alternative:
- Focused test result:
- Static/lint result:
- Remaining uncertainty:

## Refactoring checkpoints

### Checkpoint 1 — Classify every edge

Complete this table before moving imports:

| Importer | Imported module/name | Runtime | Type-only | Composition-only | Optional | Why needed? |
|---|---|:---:|:---:|:---:|:---:|---|
| `checkout_lab.__main__` | `model` |  |  |  |  |  |
| `checkout_lab.__main__` | `service` |  |  |  |  |  |
| `checkout_lab.service` | `model.Order` |  |  |  |  |  |
| `checkout_lab.service` | `email_adapter.send_receipt` |  |  |  |  |  |
| `checkout_lab.email_adapter` | `service.CheckoutResult` |  |  |  |  |  |

An edge can be runtime and composition-only, but explain the calling module's responsibility.

### Checkpoint 2 — Assign each definition

| Meaning or action | Current owner | Intended owner | Why stable there? |
|---|---|---|---|
| `OrderLine` invariant |  |  |  |
| `Order` total |  |  |  |
| Checkout result |  |  |  |
| Notification input |  |  |  |
| Notification capability |  |  |  |
| Concrete email delivery |  |  |  |
| Adapter construction |  |  |  |
| Sample CLI execution |  |  |  |

Avoid “shared” as an owner. Choose a named cohesive module/package.

### Checkpoint 3 — Choose the smallest collaboration boundary

Compare these without implementing all of them:

- one callable parameter;
- a callable type alias;
- a small `Protocol`;
- a nominal ABC;
- a module exposing one function;
- a registry/service locator;
- direct concrete import.

State the number of required operations, lifecycle needs, adapter count, typing value, and test
seam. Choose the smallest option that preserves the intended direction.

### Checkpoint 4 — Move concrete wiring outward

Identify one place allowed to import both application policy and concrete adapter. It may be
`__main__.py` or a dedicated bootstrap function. It must:

1. construct/select the adapter;
2. pass its capability to checkout;
3. invoke the sample command;
4. report failure without pretending completion;
5. remain thin enough that policy tests do not import it.

Do not make `checkout_lab/__init__.py` a hidden container.

### Checkpoint 5 — Replace defect characterizations carefully

Preserve tests that prove model validation and totals. Record, then replace tests that expect:

- service import to fail;
- package entrypoint to fail;
- `CheckoutResult` to be unavailable during import.

Add black-box tests for checkout output, notification input/call count, error behavior, fresh
imports, and entrypoint output before deleting the old failure expectations.

### Checkpoint 6 — Enforce the graph

Extend or reuse the AST graph tool to assert:

- no internal directed cycle;
- model imports no service or adapter;
- application policy imports no concrete adapter;
- the composition root is allowed to import both;
- a synthetic three-node graph is detected correctly.

Document dynamic-import and string-registration limitations. A boundary test supports judgment; it
does not replace it.

### Checkpoint 7 — Prove a change

Add a recording notifier or one alternate synthetic adapter without editing checkout policy. Do
not add provider configuration or I/O. Explain why the new requirement changes wiring/adapters but
not stable business meaning.

## Progressive hints

No hints are populated yet. Request one hint at a time after preserving the original attempt and
identifying the first incorrect assumption.

## Experiment environment

All five observations below were reproduced in this environment:

```text
Date: 2026-08-29
Operating system: Linux 7.0.0-30-generic
Architecture: x86_64
Python version: CPython 3.14.7
sys.version: 3.14.7 (main, Aug 25 2026, 14:02:56) [Clang 22.1.3 ]
sys.implementation: cpython
Dependencies: Python standard library only for experiment scripts
Relevant flags: normal repository interpreter; fresh subprocesses where stated
```

This is a reproducibility record, not a claim that traceback wording, loader internals, startup
timing, cache sharing, or file resolution are identical across Python implementations and hosts.

## Experiment 1 — Static source dependency graph

| Field | Value |
|---|---|
| Precise question | Which internal import edges exist in `checkout_lab`, and do they contain a directed cycle? |
| Classification | Static source/design observation using Python standard-library `ast` |
| Status | Run and interpreted |

### Why observation is necessary

The runtime traceback shows one execution path but does not list every package edge. Parsing import
statements makes the source graph explicit and produces a regression tool after refactoring.

### Hypothesis

> Five package modules will be found. Service and email adapter will form a directed two-node cycle;
> model will have no internal dependencies.

### Controls and variables

- Controlled: one fixed package tree, only `.py` files, internal imports, deterministic sorting.
- Changed: none in the baseline run; later refactoring changes import statements.
- Measured: module count, source edges, and first deterministic DFS cycle.

### Reproduction command

```bash
uv run python \
  units/foundations/SDP-FND-100-modules-package-boundaries-circular-dependencies/practice/dependency_graph_experiment.py
```

### Predicted result

```text
module_count=5
cycle includes checkout_lab.service and checkout_lab.email_adapter
```

### Observed result

```text
module_count=5
edge=checkout_lab.__main__ -> checkout_lab.model
edge=checkout_lab.__main__ -> checkout_lab.service
edge=checkout_lab.email_adapter -> checkout_lab.service
edge=checkout_lab.service -> checkout_lab.email_adapter
edge=checkout_lab.service -> checkout_lab.model
cycle=checkout_lab.service -> checkout_lab.email_adapter -> checkout_lab.service
```

### Interpretation

1. Directly shown: the five parsed modules contain the listed import statements and one detected
   service/adapter cycle.
2. Reasonable inference: the application service knows a concrete adapter while that adapter knows
   an application definition, so ownership/direction deserve refactoring.
3. Not shown: runtime call order, dynamic imports, framework registration, data/schema coupling,
   whether every import executes on every path, or the correct target architecture.

### Visual interpretation

```text
__main__ ──> service ──> email_adapter
                ▲              │
                └──────────────┘
     │          │
     └────────> model <────────┘ (no adapter edge in baseline)
```

#### How to read this visual

Follow arrows as source imports. The loop between service and adapter is the detected cycle. Model
has no outgoing application edges.

#### Key insight

A static graph reveals the forbidden direction even if import timing is later changed enough for
runtime startup to succeed.

#### Simplification or limitation

The tiny parser handles ordinary internal imports for this lab. Production tools must define
rules for conditional imports, aliases, namespace packages, dynamic loading, generated code, and
external dependencies.

### Design conclusion

Retain a dependency-boundary check after refactoring, but let responsibility/change reasoning
select the direction it enforces.

### Source

Python 3.14.7 Standard Library,
[`ast` — Abstract syntax trees](https://docs.python.org/3.14/library/ast.html).

## Experiment 2 — Module cache, reload, and cache deletion

| Field | Value |
|---|---|
| Precise question | Does a second import reuse the module, what does reload re-execute, and what identity appears after deleting the cache entry? |
| Classification | Python language/import system plus standard-library `importlib` |
| Status | Run and interpreted |

### Why observation is necessary

“Imports run once” is too broad. Identity checks and an execution counter distinguish ordinary
cached import, reload of the same module object, and re-import after cache invalidation while an old
reference remains.

### Hypothesis

> Two normal imports reuse one object and one execution. Reload reuses this probe's module object,
> re-executes code, and replaces its token. Removing the cache key then importing creates another
> module object while the old reference still exists.

### Controls and variables

- Controlled: one local probe module, one process, deterministic integer counter and token object.
- Changed: ordinary import, `importlib.reload`, and removal of only the probe's cache key.
- Measured: module identity, execution count, and token identity.

### Reproduction command

```bash
uv run python \
  units/foundations/SDP-FND-100-modules-package-boundaries-circular-dependencies/practice/module_cache_experiment.py
```

### Predicted result

```text
same_object_after_second_import=True
executions_after_second_import=1
same_object_after_reload=True
executions_after_reload=2
token_replaced_by_reload=True
new_object_after_cache_deletion=True
fresh_executions_after_cache_deletion=1
```

### Observed result

```text
same_object_after_second_import=True
executions_after_second_import=1
same_object_after_reload=True
executions_after_reload=2
token_replaced_by_reload=True
new_object_after_cache_deletion=True
fresh_executions_after_cache_deletion=1
```

### Interpretation

1. Directly shown: ordinary second import reused the cached probe; reload re-executed it and kept
   this module object; cache deletion plus re-import produced a distinct object.
2. Reasonable inference: module globals can retain process-local state, while reload/deletion can
   leave external references pointing at old objects.
3. Not shown: reload behavior for every extension/custom-loaded module, safe hot reload, general
   application reset, multi-interpreter sharing, or resource cleanup.

### Visual interpretation

```text
import 1 ─creates/caches─> module A (executions=1, token X)
import 2 ─cache hit──────> module A (executions=1, token X)
reload   ─re-executes────> module A (executions=2, token Y)
del cache; import ───────> module B (executions=1, token Z)
old external ref ────────> module A still exists
```

#### How to read this visual

The object letter represents module identity; token letters represent objects rebound in its
namespace. Deleting the cache edge does not delete an external reference to module A.

#### Key insight

Module-name caching is an identity and execution mechanism, not a complete state-lifecycle or hot-
reload design.

#### Simplification or limitation

The probe deliberately has no external resource, threads, class instances held elsewhere, custom
loader, or failed reload. Those cases add more caveats.

### Design conclusion

Give mutable application state an explicit owner and test isolation strategy. Do not delete
arbitrary `sys.modules` entries as a normal reset technique.

### Sources

1. Python 3.14.7 Language Reference,
   [“The module cache”](https://docs.python.org/3.14/reference/import.html#the-module-cache).
2. Python 3.14.7 Standard Library,
   [`importlib.reload`](https://docs.python.org/3.14/library/importlib.html#importlib.reload).

## Experiment 3 — Partial initialization and name-binding timing

| Field | Value |
|---|---|
| Precise question | What differs when a cycle immediately imports a not-yet-defined name versus binding a module and looking up its attribute later? |
| Classification | Python language import mechanism; traceback phrase observed on CPython |
| Status | Run and interpreted |

### Why observation is necessary

Both examples contain a source cycle. Only one fails during import. The contrast prevents the
incorrect conclusion that successful module-style syntax removes the design cycle.

### Hypothesis

> The `from` cycle will fail while alpha is partial. The module-style cycle will complete, but beta
> will record that alpha's later constant was absent during beta initialization. A later function
> lookup will then find beta's ready value.

### Controls and variables

- Controlled: two two-module packages, one constant on each side, fresh failing subprocess, cache
  cleanup around the completing package.
- Changed: immediate `from module import name` versus module binding with delayed attribute access.
- Measured: failure classification, partial-initialization phrase, visibility during load, and
  later lookup result.

### Reproduction command

```bash
uv run python \
  units/foundations/SDP-FND-100-modules-package-boundaries-circular-dependencies/practice/cycle_timing_experiment.py
```

### Predicted result

```text
from_cycle_failed=True
from_cycle_error_is_import_error=True
from_cycle_mentions_partial_initialization=True
module_cycle_loaded=True
alpha_ready_visible_during_beta_load=False
delayed_lookup_result=beta-ready
```

### Observed result

```text
from_cycle_failed=True
from_cycle_error_is_import_error=True
from_cycle_mentions_partial_initialization=True
module_cycle_loaded=True
alpha_ready_visible_during_beta_load=False
delayed_lookup_result=beta-ready
```

### Interpretation

1. Directly shown: immediate name binding failed; module-style binding completed; beta observed no
   `ALPHA_READY` during its load; later lookup returned `beta-ready`.
2. Reasonable inference: module-style import can delay an attribute request until after both module
   bodies finish.
3. Not shown: an improved dependency direction, safety of arbitrary cycles, portable traceback
   wording, or behavior when a top-level call performs the delayed lookup too early.

### Visual interpretation

```text
immediate from-binding              delayed module binding

alpha starts                        alpha starts
  → beta starts                       → beta starts
    → ask alpha.ALPHA_READY              → bind partial alpha module
      missing → ImportError              → define BETA_READY
                                      → define ALPHA_READY
later never reached                 later read_beta() → beta.BETA_READY
```

#### How to read this visual

Both sides return to alpha while alpha is partial. The left requests a missing name immediately;
the right retains the module object and waits to access beta's name until a later call.

#### Key insight

Import syntax can alter failure timing without altering the source dependency cycle.

#### Simplification or limitation

No package initializer, third module, thread, custom loader, or import-time function call appears.
The completing example is intentionally not presented as recommended architecture.

### Design conclusion

Use module-style imports for clarity or accurate delayed lookup, not as proof that bidirectional
ownership is healthy. Keep a graph rule if the design direction matters.

### Sources

1. Python 3.14.7 Language Reference,
   [“Loading”](https://docs.python.org/3.14/reference/import.html#loading).
2. Python 3.14.7 Language Reference,
   [“The import statement”](https://docs.python.org/3.14/reference/simple_stmts.html#the-import-statement).

## Experiment 4 — Direct file versus `-m` execution context

| Field | Value |
|---|---|
| Precise question | Does an internal module's explicit relative import behave differently when the file path is run directly versus located with `-m`? |
| Classification | Python command-line and import-system behavior |
| Status | Run and interpreted |

### Why observation is necessary

The same source file can be valid package code yet fail as a directly executed internal file. The
experiment records package metadata after the package-aware form succeeds.

### Hypothesis

> Direct file execution will lack a known parent package and fail its relative import. `-m` will
> locate the module through the import system, set package/spec metadata, and run it as `__main__`.

### Controls and variables

- Controlled: one `execution_probe.report` source file, one relative import, same interpreter and
  working directory, fresh subprocess per invocation.
- Changed: direct path argument versus `-m execution_probe.report`.
- Measured: exit status, error classification, `__name__`, `__package__`, `__spec__.name`, message.

### Reproduction command

```bash
uv run python \
  units/foundations/SDP-FND-100-modules-package-boundaries-circular-dependencies/practice/execution_context_experiment.py
```

### Predicted result

```text
direct_file_failed=True
direct_file_relative_import_error=True
module_execution_succeeded=True
module_name=__main__
package=execution_probe
spec_name=execution_probe.report
message=package-context-preserved
```

### Observed result

```text
direct_file_failed=True
direct_file_relative_import_error=True
module_execution_succeeded=True
module_name=__main__
package=execution_probe
spec_name=execution_probe.report
message=package-context-preserved
```

### Interpretation

1. Directly shown: direct internal-file execution failed the relative import; `-m` succeeded with
   the recorded package and spec names.
2. Reasonable inference: executable package/module surfaces should be invoked through documented
   module or console entrypoints rather than arbitrary internal file paths.
3. Not shown: installed console-script behavior, every `sys.path` entry, zip/directory execution,
   or that relative imports are universally preferable.

### Visual interpretation

```text
python execution_probe/report.py       python -m execution_probe.report
            │                                      │
            ▼                                      ▼
     __name__ = __main__                    __name__ = __main__
     no package parent                      __package__ = execution_probe
     relative import fails                  __spec__.name = execution_probe.report
                                             relative import succeeds
```

#### How to read this visual

Both forms use `__main__` for top-level execution. The difference is package/spec context supplied
by module-aware lookup.

#### Key insight

“The file exists” is not the same as “the module is being executed inside its package.”

#### Simplification or limitation

The experiment runs from the practice directory and uses a regular package. Installation,
namespace packages, isolated mode, environment variables, and console-script wrappers are omitted.

### Design conclusion

Provide a thin `__main__.py` or console entrypoint and keep reusable work in importable functions.
Do not modify `sys.path` inside internal modules to imitate package execution.

### Sources

1. Python 3.14.7 Standard Library,
   [`__main__` — top-level code environment](https://docs.python.org/3.14/library/__main__.html).
2. Python 3.14.7 command-line documentation,
   [`-m module-name`](https://docs.python.org/3.14/using/cmdline.html#cmdoption-m).

## Experiment 5 — Eager `__init__.py` import cascade

| Field | Value |
|---|---|
| Precise question | When one leaf submodule is requested, does the regular parent package initializer eagerly import an unrelated public module first? |
| Classification | Python regular-package import behavior plus deliberate package code |
| Status | Run and interpreted |

### Why observation is necessary

Package-root re-exports look like surface-only convenience. A trace makes the transitive execution
order visible when a consumer asks for a different leaf.

### Hypothesis

> Importing `eager_package.leaf` will execute the parent initializer first. Its re-export will load
> `public_api`, and only then will the requested leaf execute.

### Controls and variables

- Controlled: one regular package, three deterministic trace appends, cache cleared before/after.
- Changed: only the requested qualified name (`eager_package.leaf`).
- Measured: leaf value, public-module cache presence, execution-trace order.

### Reproduction command

```bash
uv run python \
  units/foundations/SDP-FND-100-modules-package-boundaries-circular-dependencies/practice/package_init_experiment.py
```

### Predicted result

```text
requested_leaf_value=leaf-value
public_module_loaded_transitively=True
execution_trace=('package-init', 'public-api', 'leaf')
```

### Observed result

```text
requested_leaf_value=leaf-value
public_module_loaded_transitively=True
execution_trace=('package-init', 'public-api', 'leaf')
```

### Interpretation

1. Directly shown: requesting the leaf executed the parent initializer, which imported public API
   before the leaf.
2. Reasonable inference: eager package-root re-exports expand startup work and potential cycle
   paths for every imported child.
3. Not shown: re-exports are always wrong, measurable performance harm, behavior of namespace
   packages, or a real application's ideal public surface.

### Visual interpretation

```text
request eager_package.leaf
            │
            ▼
eager_package/__init__.py
            │ eager re-export
            ▼
eager_package.public_api
            │ returns to requested load
            ▼
eager_package.leaf
```

#### How to read this visual

The leaf request first initializes its parent package. The initializer adds a transitive import
before control reaches the requested leaf.

#### Key insight

`__init__.py` is executable dependency-graph code, not only package metadata.

#### Simplification or limitation

The trace uses deliberate mutable state for observation and clears the package cache. Real package
initializers may involve multiple subpackages, conditional imports, custom loaders, or no re-
exports at all.

### Design conclusion

Use package-root re-exports deliberately, keep their graph small, and smoke-test important leaf
imports independently.

### Source

Python 3.14.7 Language Reference,
[“Regular packages”](https://docs.python.org/3.14/reference/import.html#regular-packages).

## Observe and explain

After running the starter and experiments, explain without reading the canonical note:

1. Why is the model importable while the service is not?
2. Which object is already cached when the adapter asks for `CheckoutResult`?
3. Why does the graph experiment add evidence beyond the traceback?
4. Which direction expresses stable policy versus concrete delivery?
5. What does the module-cache experiment prove and not prove?
6. Why can the module-style source cycle complete even though beta saw alpha as incomplete?
7. What exact metadata does `-m` preserve in the execution experiment?
8. Why did importing one leaf execute `public_api`?
9. Which response fixes only type/runtime timing, and which fixes construction ownership?
10. Why might merging modules be better than adding a port?
11. Which old tests must change after the refactor, and why is deleting them immediately unsafe?
12. What static/dynamic edges can the AST checker miss?

## Vary

After the core refactoring passes, choose exactly one variation.

### Variation A — second notifier

Add a synthetic audit notifier that records the same stable notification value. Select email or
audit only in the composition root. Prove application policy does not change.

### Variation B — type-only adapter annotation

Add a helper whose annotation mentions a concrete adapter but whose runtime never uses that type.
Choose an accurate forward-reference/`TYPE_CHECKING` approach, then use reflection to explain any
runtime annotation-resolution trade-off.

### Variation C — optional report extension

Add an optional report renderer loaded only when a command flag requests it. Define missing-
extension versus extension-initialization failure separately. Justify local import or metadata
discovery without introducing a general plugin framework.

Do not combine the variations. The purpose is transfer of dependency direction, not feature
volume.

## Review rubric

| Area | Strong evidence | Weak evidence |
|---|---|---|
| Import mechanics | Reconstructs cache/partial/execution/binding timeline | “Python reads files in order” |
| Source graph | Full qualified arrows plus detected cycle | Only repeats traceback filenames |
| Ownership | Stable value, policy, adapter, and wiring owners named | Moves all shared names to `common.py` |
| Boundary mechanism | Callable/port choice follows required operations | Interface chosen by habit |
| Package surface | Public imports and initializer work are explicit | Re-export everything for convenience |
| Entrypoint | Thin package-aware composition root | Reusable policy mixed with startup |
| Testing | Behavior, fresh import, `-m`, and graph rules | Tests pass only after another import |
| Failure | Startup and notification failures have contracts | Broad `ImportError` catch hides defects |
| Simplicity | Merge/move-definition considered first | New layers/packages for every name |
| Explanation | Design, language, library, CPython, and packaging claims separated | One experiment generalized universally |

## Troubleshooting

- Run root-level commands exactly as documented; the deliberate lab runner places its practice
  directory on `sys.path` by normal script execution.
- For `python -m checkout_lab`, change into the practice directory or install an equivalent package
  context; do not add a `sys.path` mutation to `checkout_lab`.
- If pytest fails during collection, inspect whether a test imported the broken service in-process
  instead of characterizing it in a subprocess.
- If the traceback no longer fails after only changing import syntax, rerun the static graph; the
  cycle may still exist.
- If graph output misses an edge, inspect relative-import level, aliasing, conditional/dynamic
  imports, and whether the parser recognizes that syntax.
- If experiment output changes between tests, clear only the controlled package keys or use a
  fresh subprocess; never delete arbitrary interpreter modules.
- If mypy reports a deliberate cycle fixture, keep any suppression exact and local, and state why
  the unresolved type is the experiment subject.
- If a package initializer loads unrelated modules, inspect re-exports before adding lazy magic.
- If direct file execution fails relative imports, use `-m`; do not replace explicit package
  imports with repository-relative path hacks.
- If an optional import catches `ImportError`, prove the exception means the target is missing and
  was not raised from inside a broken target module.
- If the proposed port has one method and no lifecycle, compare it with a callable parameter.
- If the new “shared” module collects unrelated values, stop and reassign ownership.

## Closure

Add only after Rahul closes the exercise.

- Final learner solution:
- Original attempt preserved at:
- Boundary worksheet:
- Before/after source graphs:
- Fresh import result:
- Entrypoint result:
- Focused test result:
- Static/lint result:
- Variation result:
- Rejected alternative:
- Production transfer:
- Trade-offs:
- Remaining weakness:
- Evidence link for `PROGRESS.md`:
