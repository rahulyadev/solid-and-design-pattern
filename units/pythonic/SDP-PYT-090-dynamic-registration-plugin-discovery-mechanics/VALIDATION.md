# Validation — SDP-PYT-090

## Scope and evidence boundary

| Field | Observed value |
|---|---|
| Date | 2026-09-06 |
| Exact branch | `topic/SDP-PYT-090` |
| Initialization baseline (`INIT_START`) | `dc27d203f7b89ac662e7f46f74e4e2df4339bc1b` |
| Initialization commit | `58c668a0bd637955ca2ff876a10b6ce71326a2b8` |
| Evidence profile | `E+I+D+X+T` |
| Canonical runtime | CPython 3.14.7 |
| Compatibility runtime | CPython 3.11.16 |
| Artifact state during this record | Approved |
| Learning state during this record | Not started |

This record validates maintainer-authored curriculum material. It contains no learner prediction,
attempt, explanation, delayed recall, transfer, refactoring submission, or interview answer.
Therefore only artifact state advances from Absent through Draft to Approved. Rahul's learning state
remains Not started, and every learner-evidence field in `PROGRESS.md` remains `—`.

## Sources actually read

- Python 3.14 `importlib.metadata` documentation for installed-distribution scope, distribution and
  import-package distinctions, selectable entry points, `EntryPoint` metadata and `load()`,
  `.dist`, distribution discovery, custom providers, and the 3.12/3.13 API changes.
- Python 3.11 `importlib.metadata` documentation for the compatibility-floor selectable API and
  no-argument `SelectableGroups` compatibility behavior.
- Python 3.14 import-system reference for `sys.modules` lookup, insertion before module execution,
  loader execution, cache identity, reload distinction, exception propagation, and failed-load
  cache behavior.
- PyPA entry-points specification for group, name, object reference, distribution conflict,
  `entry_points.txt`, extras, interoperability purpose, and history.
- PyPA `pyproject.toml` specification for modern entry-point publication tables.
- PyPA plugin-discovery guide for naming-convention, namespace-package, and package-metadata
  approaches plus namespace cautions.
- PyPA distribution-package versus import-package guide for naming, cardinality, normalization,
  and unsafe install-name inference.
- PyPA installed-project recording specification for `.dist-info`, `METADATA`, and
  `entry_points.txt` roles.
- PyPA name-normalization specification for distribution-name validation and comparison.

Subtle claims cite these sources near the relevant mechanics and judgments. No copied book prose,
external diagram, real third-party plugin, network provider, private data, production log,
credential, or proprietary package was used.

## Executed checks

| Check | Observed result |
|---|---|
| Focused unit tests, CPython 3.14.7 | 40 passed: 29 example/experiment/visual tests and 11 unsolved-practice behavior tests. |
| Focused unit tests, CPython 3.11.16 | The same 40 tests passed. |
| Repository regression, CPython 3.14.7 | 778 tests passed across all 53 discovered test directories, using a separate pytest process per directory. |
| Ruff lint | Passed for the complete SDP-PYT-090 unit tree with cache disabled. |
| Ruff formatting | All 17 format-eligible unit files are formatted. |
| Strict mypy, Python 3.14 target | No issues in 12 source files. |
| Strict mypy, Python 3.11 target | No issues in the same 12 source files. |
| Controlled negative mypy case | Both targets rejected `Callable[[str], str]` where `Callable[[ReportRequest], RenderedReport]` was required. |
| README Python snippets | All 12 fenced Python snippets compiled on CPython 3.14.7 and CPython 3.11.16. |
| Worked demo | Published `invoice-json,status-text`, mapped both semantic claims, rendered the synthetic invoice, and emitted registration/load/construction/validation/activation/invocation events. |
| Temporary distribution fixture | Found `Acme-Report-Plugin==2.4.0` advertising `sdp_pyt090_fixture_runtime:provide` without importing during discovery. |
| Entry-point load experiment | Two loads executed fixture module top-level code once in the process, returned the same function object, and produced the expected provider result. |
| Import/process experiment | Same-process imports reused module and token; two child interpreters each executed the module; the deliberate cycle raised `ImportError`. |
| Practice starter | Emitted the expected text and JSON exports; the target plugin refactoring remains absent. |
| Embedded visual model | Tests compared every field in all six embedded lifecycle scenarios with maintained Python observations and covered every lifecycle stage plus both failure policies. |
| HTML script syntax | The executable JavaScript block compiled with Node.js 24.19.0. |
| Static visual structure | All ten required DOM IDs were present, CSS braces balanced, and both narrow-layout media queries existed. |
| Interactive browser rendering | Not performed: the app browser blocked the local `file:` URL under its security policy. No bypass, indirect navigation, alternate browser automation, or policy workaround was attempted. |
| Repository validator | All structure, metadata, Markdown, links, evidence, version, lock-file, source-policy, and hygiene checks passed after generated caches were removed. |

The dual-runtime environments and caches lived under `/tmp`; no virtual environment, wheel,
temporary distribution, `.dist-info`, bytecode, pytest, Ruff, mypy, or uv cache was committed. The
temporary fixture creates and removes its module and distribution metadata during the process.

The browser-policy limitation narrows visual evidence honestly: the artifact has model parity,
JavaScript syntax, DOM-target, and responsive-source checks, but no claimed rendered desktop/mobile
observation. The self-contained visual has no network dependency. This limitation does not turn the
visual into runtime or accessibility proof.

## Manual content and boundary review

- Began with independent-provider change pressure, a simple lifecycle model, and direct-import
  alternatives before formal packaging mechanics.
- Kept provider publication, runtime registration/filtering, discovery, load, construction,
  individual validation, batch validation, activation, resolution, and invocation distinct.
- Covered explicit imports, configured allow-lists, static registries, decorator registration,
  entry points, namespace packages, naming conventions, framework registries, remote services, and
  rejection of unjustified plugin systems.
- Used `entry_points(group=...)` across Python 3.11/3.14 and documented no-argument return-shape and
  tuple-indexing differences without relying on legacy behavior.
- Distinguished entry-point name, semantic claim, distribution package, import package/module,
  object reference, distribution version, plugin API version, and capability.
- Applied PyPA-normalized distribution allow-list comparisons while keeping the entry-point name in
  its separate host-owned namespace.
- Used a client-owned frozen manifest/offer plus one factory and callable, with no speculative
  hierarchy, metaclass, container, hook DSL, installer, or hot-reload framework.
- Rejected invalid names and distribution policy before load, rejected every duplicate-name or
  semantic-claim claimant, and made ordering deterministic without declaring a winner.
- Separated fail-fast and optional quarantine, while missing required providers still block
  activation and readiness.
- Copied active bindings into an immutable process-local snapshot and made repeat startup build
  fresh state without accumulating global registrations.
- Distinguished immutable bindings from handler state safety, process-local imports from worker
  coordination, and ordinary module caching from unload or idempotent factory behavior.
- Preserved stage-specific and invocation exception identity while recording only provider,
  distribution, version, stage, and outcome in the teaching implementation.
- Made the security boundary explicit: entry points advertise; loading executes in-process code with
  application authority; metadata/version/shape are inputs, not trust or behavioral proof.
- Kept `SDP-PYT-080` honest: `singledispatch` registers and selects by first-argument runtime type;
  it does not discover installed distributions or govern plugins.
- Kept the report-renderer worked domain, temporary metadata/import probes, and alert-export practice
  domain separate.
- Kept practice runnable but unsolved: no target pipeline, learner attempt, released hint, solution,
  or false learning evidence was added.
- Used only synthetic provider/distribution names, report IDs, alerts, outputs, failures, and
  temporary filesystem state; examples use no network, database, real plugin, credential, or
  production data.

## Approval boundary

The artifact is Approved because repository validation, dual-runtime focused tests, complete
repository regression, focused lint/formatting, strict dual-target typing, controlled negative
typing, dual-runtime snippet compilation, demo and practice execution, real synthetic metadata and
import/process experiments, visual-model parity, JavaScript syntax, static visual checks, source
review, and manual pedagogical/security review passed. Approval applies only to the artifact. It
does not claim that Rahul has practiced, recalled, demonstrated, or retained the material.
