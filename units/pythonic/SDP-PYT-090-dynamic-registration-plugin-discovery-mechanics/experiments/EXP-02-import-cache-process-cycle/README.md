# EXP-02 — Import cache, process scope, and circular failure

## Question

What state does repeated import reuse inside one process, what happens in two fresh worker
processes, and why can a circular import observe an incomplete module?

## Why this experiment exists

Plugin registration often happens during import, which tempts teams to describe it as “once.” The
missing qualifier is **per ordinary module name in one interpreter process**. Python checks
`sys.modules` first, inserts a new module there before executing its code, and removes the failing
module when loading raises. The early insertion prevents unbounded recursive loading, but a cycle
can still request an attribute before its definition executed
([Python 3.14 import cache and loading](https://docs.python.org/3.14/reference/import.html#the-module-cache)).

## Predict before running

| Prediction | Your answer |
|---|---|
| Are two same-process imports the identical module object? | — |
| Is an object created at module top level identical through both imports? | — |
| How many marker lines follow two same-process imports? | — |
| How many total lines follow two additional child-process imports? | — |
| What exception family will the deliberately early circular attribute access raise? | — |
| Does a registry built in the parent become shared mutable memory in the children? | — |

## Synthetic fixture

[import_process_probe.py](../../examples/import_process_probe.py) creates three modules under a
temporary directory:

```text
sdp_pyt090_cache_target.py    appends a marker and creates TOKEN
sdp_pyt090_cycle_alpha.py     imports VALUE_B, then defines VALUE_A
sdp_pyt090_cycle_beta.py      imports VALUE_A, then defines VALUE_B
```

The probe imports the cache target twice in its process, launches two fresh interpreter children,
then attempts the cycle. It never installs or imports a real plugin.

## Run

```bash
uv run --locked python units/pythonic/SDP-PYT-090-dynamic-registration-plugin-discovery-mechanics/examples/import_process_probe.py
uv run --locked pytest -q -p no:cacheprovider units/pythonic/SDP-PYT-090-dynamic-registration-plugin-discovery-mechanics/examples/test_runtime_probes.py
```

## Maintainer observation

The supported CPython validation runtimes report:

```text
same_module_in_process=True
same_token_in_process=True
executions_after_same_process_imports=1
executions_after_two_child_processes=3
cycle_error_type=ImportError
cycle_modules_cached_after_failure=False
```

The first four observations illustrate documented caching plus separate processes. The exact error
text and many private import-lock details are deliberately not asserted. The final cache result is
an observation of this fixture on the tested CPython runtimes; the language reference supplies the
relevant loading rules, while custom importers may add behavior.

## Explain

### Same process

The second import used the cached module object. Its `TOKEN` and any decorator-populated global
registry therefore remain the same process-local objects. This helps ordinary idempotent imports,
but does not make arbitrary registration functions idempotent: calling a factory or registration
function twice is separate from importing its module twice.

### Multiple processes

Each child interpreter owned a different `sys.modules` mapping and executed the target module. A
pre-fork server may copy initial memory and a spawned worker may import afresh, but neither model
turns a normal Python dictionary into coordinated cross-process state. Every worker must reach the
same validated readiness configuration, and rollout telemetry should compare their published
inventories.

### Circular import

Alpha entered `sys.modules` before its body completed. Beta then received that partial module and
requested `VALUE_A` before alpha's defining line ran. Cache insertion prevented recursive module
creation; it did not manufacture the future attribute. Plugin contracts should therefore live in a
small client-owned module that does not import providers, while the outer composition root imports
or discovers providers.

## Design consequence

Prefer this source dependency:

```text
host contract  <── plugin implementation
      ▲
      │
composition root imports/configures both
```

Avoid making the contract module import every implementation that imports the contract back. A
local import may postpone the symptom, but it does not necessarily repair ownership.

## Vary

1. Replace the provider with a decorator that mutates a module global. Is importing twice enough to
   duplicate registration? What about explicitly calling its installer twice?
2. Run startup in two processes with different allow-lists. Which observable inventory detects the
   drift?
3. Catch the cycle and continue. Which successfully imported side-effect modules remain cached?
4. Replace the cycle's `from module import name` with `import module`. Does the timing change, and
   is the dependency graph now well owned?

## Cleanup and limitation

The probe uses temporary files, removes its three synthetic `sys.modules` entries, and invalidates
import caches. It is not a production hot-unload recipe. It omits fork servers, subinterpreters,
custom loaders, native modules, thread races, distributed locks, and deployment orchestration.
