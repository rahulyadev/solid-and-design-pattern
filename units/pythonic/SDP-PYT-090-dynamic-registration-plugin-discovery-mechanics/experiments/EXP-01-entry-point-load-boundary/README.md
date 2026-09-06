# EXP-01 — Entry-point discovery versus load

## Question

Can the host inspect an installed entry point's name, group, object reference, distribution, and
version without importing the advertised module, and what changes when `EntryPoint.load()` runs?

## Why this experiment exists

“Discover” and “load” are often collapsed into one vague word. That hides the most important trust
boundary. The PyPA entry-point data model describes an object reference; resolving that reference
imports its module and traverses the named attribute. Python exposes the metadata through
`importlib.metadata.EntryPoint` and supplies `load()` for resolution
([entry-point specification](https://packaging.python.org/en/latest/specifications/entry-points/),
[Python 3.14 entry points](https://docs.python.org/3.14/library/importlib.metadata.html#entry-points)).

## Predict before running

Write `yes`, `no`, or a precise value before execution:

| Prediction | Your answer |
|---|---|
| Will `entry_points(group=...)` create the module's marker file? | — |
| Will the entry-point name equal the distribution name? | — |
| What import module and attribute will `.value` encode? | — |
| How many times will module top-level code execute after two `load()` calls in one process? | — |
| Will both loads return the same function object in this ordinary import case? | — |

## Synthetic fixture

[entry_point_probe.py](../../examples/entry_point_probe.py) creates this structure only under a
`TemporaryDirectory`:

```text
temporary-directory/
├── sdp_pyt090_fixture_runtime.py
└── acme_report_plugin-2.4.0.dist-info/
    ├── METADATA
    └── entry_points.txt
```

The distribution name is `Acme-Report-Plugin`; the import module is
`sdp_pyt090_fixture_runtime`; the entry-point group is unique to this experiment. The module appends
one line to a marker during import and exposes a harmless local `provide()` function. No package is
installed, no network is used, and no real third-party code executes. The temporary tree is deleted
when the probe exits.

## Run

From the repository root:

```bash
uv run --locked python units/pythonic/SDP-PYT-090-dynamic-registration-plugin-discovery-mechanics/examples/entry_point_probe.py
uv run --locked pytest -q -p no:cacheprovider units/pythonic/SDP-PYT-090-dynamic-registration-plugin-discovery-mechanics/examples/test_runtime_probes.py
```

## Maintainer observation

On the supported CPython 3.14 and 3.11 validation runtimes, the checked fixture reports:

```text
name=fixture
group=sdp.pyt090.fixture
value=sdp_pyt090_fixture_runtime:provide
module=sdp_pyt090_fixture_runtime
attribute=provide
distribution=Acme-Report-Plugin
version=2.4.0
imported_during_discovery=False
import_executions_after_two_loads=1
same_loaded_object=True
provider_result=synthetic-provider-ready
```

This output is a maintained local observation, not a promise that arbitrary custom metadata
providers, import hooks, or plugin code have no side effects during enumeration. The documented
API separates selected entry-point metadata from `.load()` resolution. The one-execution and object-
identity results arise from the ordinary import path and `sys.modules` cache used by this fixture.

## Explain

1. **Discovery:** the host found `entry_points.txt`, created an `EntryPoint`, and read metadata. The
   fixture module marker did not exist.
2. **Load:** `entry_point.load()` resolved `module:attribute`; importing the module executed its
   top-level code with the current process's authority.
3. **Cache reuse:** the second ordinary load found the module in `sys.modules`, so this module's
   top-level marker did not run again.
4. **Construction remains separate:** the resolved object happened to be a provider function. The
   host had not yet called it merely by loading it.
5. **Trust remains unresolved:** metadata, a successful import, and a plausible version are inputs
   to policy. None proves origin, safety, compatibility, or behavior.

The distribution/import naming difference is intentional. Packaging tools install a distribution;
Python imports modules and import packages, and the names need not correspond one-to-one
([PyPA distribution versus import package](https://packaging.python.org/en/latest/discussions/distribution-package-vs-import-package/)).

## Failure boundaries to vary

Change one thing at a time and predict the stage:

- malformed or unreadable metadata → discovery;
- missing module in the object reference → load;
- missing attribute after a successful import → load;
- resolved integer instead of a factory → construction when called, or earlier owned shape check;
- factory raises → construction;
- factory returns the wrong contract value → validation; and
- valid renderer later raises → invocation.

Do not wrap all of these in one “plugin unavailable” exception. Stage identity is essential for
containment, rollback, alerts, and diagnosis.

## Cleanup and limitation

The probe removes its temporary path from `sys.path`, removes its synthetic module from
`sys.modules`, invalidates import caches, and lets `TemporaryDirectory` delete the fixture. That
cleanup exists only to isolate a repeatable test. Production code should not pretend arbitrary
plugin code can be safely unloaded by deleting a cache key.

This experiment does not verify package signatures, installer provenance, wheel integrity,
subinterpreters, native extensions, custom importers, isolation, or hostile code. It demonstrates
one precise standard-library boundary.
