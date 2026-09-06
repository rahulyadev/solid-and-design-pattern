# Practice — SDP-PYT-090 governed alert-export plugins

| Field | Value |
|---|---|
| Unit note | [SDP-PYT-090](../README.md) |
| Starter | [alert_export_lab.py](alert_export_lab.py) |
| Behavior tests | [test_alert_export_lab.py](test_alert_export_lab.py) |
| Test command | `uv run --locked pytest -q -p no:cacheprovider units/pythonic/SDP-PYT-090-dynamic-registration-plugin-discovery-mechanics/practice` |
| State | Unsolved |

## Scenario and change pressure

An operations service exports validated alerts as text or JSON. The application owns both formats,
the small conditional is readable, and all behavior tests pass. Keep it if that remains the whole
problem.

The requirement changes: independently released internal distributions may advertise alert
exporters. Operations selects an explicit allow-list of plugin names and distributions. Startup
must discover metadata, load only enabled candidates, reject incompatible or duplicate claims, and
publish a stable registry before traffic. One optional broken plugin may be quarantined, but a
configured required exporter must stop readiness. Plugin code runs in-process; no sandbox is being
built.

Your goal is to design the smallest host-owned boundary that makes those policies visible. Do not
copy the worked report example. Preserve this starter as your original attempt or make a separate
attempt file before refactoring.

## Predict before running

Record answers before executing anything:

1. Does asking `entry_points(group=...)` import each advertised plugin module?
2. Which exact operation crosses the boundary where plugin code first executes?
3. If two distributions advertise the same entry-point name, which one should win?
4. If different names both claim `format.yaml`, is that a second kind of duplicate?
5. Can a distribution version string prove behavioral compatibility or trust?
6. After one process builds a registry, will another worker automatically share it?
7. Which failure policy is appropriate for a required exporter and for an optional exporter?
8. What fields can telemetry record without exposing an alert body?

No learner prediction has been recorded by the maintainer.

## Run the starter

From the repository root:

```bash
uv run --locked python units/pythonic/SDP-PYT-090-dynamic-registration-plugin-discovery-mechanics/practice/alert_export_lab.py
uv run --locked pytest -q -p no:cacheprovider units/pythonic/SDP-PYT-090-dynamic-registration-plugin-discovery-mechanics/practice
```

Write down the runtime, exact output, and test count. Maintainer validation is artifact evidence,
not your prediction, attempt, or explanation.

## Observe the existing design

Before refactoring, identify:

- the stable client operation and result;
- validation and exception behavior that must not drift;
- why the current closed conditional is reasonable;
- the new boundary introduced by independently installed code; and
- which facts are application policy rather than `importlib.metadata` behavior.

## Explain the lifecycle in your own words

Explain these as seven separate stages: registration, discovery, load, construction, validation,
activation, and invocation. For each stage name its input, output, likely failures, and whether plugin
code can have executed yet.

Then explain why an entry point is advertisement metadata rather than authentication, compatibility
proof, a sandbox, an active plugin, or an invocation result.

## Refactor

Preserve the public export behavior while adding a host-owned plugin boundary. Keep built-in text
and JSON support explicit. Add dynamic discovery only for the new installed-provider requirement.

Required constraints:

- define the smallest client-owned request, result, manifest, and callable/factory contract;
- use `importlib.metadata.entry_points(group=...)` in a Python 3.11-compatible form;
- inspect and sort metadata before calling `EntryPoint.load()`;
- filter an explicit name and distribution allow-list before load;
- separate load, construction, contract validation, activation, and invocation errors;
- negotiate one host API version and a small capability set;
- reject every claimant for duplicate entry names or duplicate semantic format claims;
- make ordering deterministic but never use order to choose a duplicate winner;
- support fail-fast and quarantine policy without hiding required-plugin failure;
- publish a fresh immutable snapshot and make repeated startup safe;
- record provider, distribution, version, stage, and outcome without alert content or secrets;
- keep Python 3.11 compatibility and standard-library-only runtime code; and
- do not change `PROGRESS.md` from this practice directory.

Do not add a dependency-injection container, metaclass, framework registry, custom importer, remote
package-index query, signature-inspection framework, hot-reload system, or subprocess sandbox.

## Required edge cases

- discovery returns no candidates;
- a configured module is missing;
- `EntryPoint.load()` raises;
- a loaded target is not callable;
- a provider factory raises;
- a provider returns the wrong value;
- host and plugin API majors differ;
- a required capability is absent;
- manifest name and entry-point name differ;
- duplicate entry names arrive in reverse input order;
- distinct names claim the same format;
- an optional bad provider is quarantined;
- a required provider cannot activate;
- the published mapping rejects writes;
- two startup calls do not accumulate process-global registrations;
- an unknown provider is requested;
- a renderer returns the wrong result type;
- a renderer raises its own exception and keeps that identity; and
- two worker processes each execute their own startup.

## Rahul's attempt

- Attempt file: —
- Prediction: —
- Contract chosen: —
- Allow-list and duplicate policies: —
- Failure policy: —
- Rejected alternative: —
- Runtime evidence: —
- Test result: —

## Progressive hints

No hints are released. Ask for one at a time after recording an attempt.

## Observe and explain after refactoring

1. Prove discovery alone did not import the temporary fixture module.
2. Show the exact line or call where imported plugin code may execute.
3. Show how a construction exception differs from invalid manifest data.
4. Reverse candidate input and prove the result or failure remains deterministic.
5. Show that both semantic duplicate claimants are absent after quarantine.
6. Prove the active bindings cannot be mutated through the public snapshot.
7. Run startup twice and explain why no global registrations accumulated.
8. Run two processes and identify which state each owns.
9. Trigger a renderer failure and prove it was not relabeled as discovery or load failure.
10. Name one abstraction that can still be removed if dynamic discovery disappears.

## Vary

Choose one change and defend the new boundary:

- plugins come only from five application-owned modules;
- one plugin needs a database client constructed by the host;
- two compatible plugins may intentionally share a capability but not a semantic claim;
- a tenant chooses different active formats;
- plugins must be isolated from application credentials and memory; or
- activation must change while requests are already running.

State whether the correct response is explicit imports, dependency passing, a fresh snapshot,
process isolation, rolling restart, or rejection of the plugin design.

## Troubleshooting

- Run from the repository root so pytest resolves the sibling starter module.
- Do not install a real package for the exercise; create metadata under a temporary directory.
- Use a unique synthetic entry-point group so the environment cannot supply an accidental match.
- Do not assert discovery iteration order; sort by an owned key.
- Do not catch `BaseException`; cancellation and process-control signals are not plugin failures.
- Do not call `load()` while merely filtering metadata.
- Do not mutate `sys.modules` to simulate production unloading.
- If typing cannot trust an object returned from `load()`, narrow it at the owned runtime boundary.

## Closure

Add only after Rahul closes the exercise.

- Final learner solution: —
- Optional comparison solution: —
- Trade-offs: —
- Remaining weakness: —
- Evidence link for `PROGRESS.md`: —
