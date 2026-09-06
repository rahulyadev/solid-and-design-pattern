# Practice — SDP-PYT-050 modules, import caching, and dependency lifetimes

| Field | Value |
|---|---|
| Unit note | [SDP-PYT-050](../README.md) |
| Curriculum | [CURRICULUM.md](../../../../CURRICULUM.md#sdp-pyt-050) |
| Evidence target | `E+I+D+X+T` |
| Attempt required before solution | Yes |
| Test command | `uv run --locked pytest -q -p no:cacheprovider units/pythonic/SDP-PYT-050-modules-import-caching-dependency-lifetimes/practice` |
| Status | Not attempted |

## Learning question

Can you replace a hidden import-time service with application- and request-owned lifetimes while
preserving behavior, deterministic cleanup, failure identity, and two-app isolation?

## Lab cycle

```text
predict → run → observe → explain → refactor → vary
```

Complete the stages in order. Green starter tests characterize the legacy behavior only; they do
not prove the target design.

## Starter files

- [fulfillment_lab.py](fulfillment_lab.py): runnable legacy allocation flow with an import-time
  gateway and a per-call session.
- [test_fulfillment_lab.py](test_fulfillment_lab.py): characterization tests that patch the name
  where the legacy function looks it up.

The worked usage-service example uses another synthetic domain. This folder contains no target
implementation, released hint, comparison solution, learner attempt, or fabricated evidence.

## Problem and change pressure

`allocate_order(...)` currently discovers `warehouse_gateway` through its module namespace. The
same cached module object usually means repeated importers in one interpreter reach the same
gateway. That happened to work for one application with one endpoint.

Now the process must host two independently configured application instances during tests and
local tools. Each application must own one gateway from startup through shutdown. Each allocation
must own a fresh session that closes after success or failure. Importing the module must declare
code, not acquire the gateway.

All endpoints, orders, failures, and resources are synthetic. Nothing contacts a warehouse,
database, network, filesystem, or framework.

## Legacy observable contract

| Dimension | Required observation |
|---|---|
| Formatting | Return `order_id:sku:quantity@endpoint#session-N`. |
| Text | Preserve blank order IDs, Unicode, spaces, colons, and literal pipes. |
| Validation | Reject non-positive quantity before opening a session. |
| Application reuse | Legacy calls through one module reuse its gateway. |
| Request isolation | Each valid call opens a distinct sequentially numbered session. |
| Success cleanup | Close the request session exactly once; keep the gateway open. |
| Failure cleanup | Propagate the same gateway failure and close the opened session once. |
| Input | Do not mutate the frozen request value. |

These observations are compatibility constraints, not approval of the hidden dependency.

## Prediction before running

Without running the code, record:

1. when `warehouse_gateway` is constructed;
2. which namespace `allocate_order(...)` consults at call time;
3. whether `from fulfillment_lab import warehouse_gateway` would track a later rebinding;
4. which object is shared across calls and which object is new per call;
5. what closes after a session failure;
6. whether the legacy gateway has any automatic application-shutdown contract; and
7. what happens if two app configurations need different endpoints in one interpreter.

No learner prediction has been recorded by the maintainer.

## Phase A — make the application owner explicit

Preserve `AllocationRequest`, `AllocationSession`, `WarehouseGateway`, and the observable
allocation contract. Remove live gateway acquisition from module import. Introduce the smallest
composition boundary that can create two application instances with different endpoints in the
same interpreter.

Your tests must demonstrate:

- importing or reloading the lab module does not construct a live gateway;
- two applications do not share gateways, sessions, counters, or closure state;
- repeated calls within one application reuse only that application's gateway;
- gateway acquisition failure does not pretend that shutdown ran; and
- a successfully started gateway closes exactly once on normal and exceptional shutdown.

Do not replace the global object with a global service locator, class-level instance cache, or
unbounded `functools.cache` merely to move the hidden state.

## Phase B — make request ownership explicit

Give each allocation a distinct session owned by a lexical or framework-equivalent request
boundary. Pass the needed capability to application policy explicitly. Preserve exception
identity when cleanup succeeds.

Add focused tests for:

- valid, invalid, blank, Unicode, duplicate, and punctuation-heavy values;
- two overlapping request scopes;
- handler failure before and after one session operation;
- session acquisition failure;
- session cleanup failure, including when the body also fails;
- use after request exit; and
- refusal to begin a request after application shutdown.

Document whether cleanup failure replaces, chains from, or is grouped with an active body
failure. Do not silently swallow either path.

## Phase C — transfer the design

Sketch how the same ownership maps to a FastAPI application without making business policy import
FastAPI:

- application resource acquisition and release;
- request session acquisition and release;
- route-level dependency receipt;
- background work that must not retain a closed request session; and
- worker-process multiplicity.

Then reject one unnecessary Singleton or dependency-injection-container design and explain why
the smaller composition is sufficient.

## Required edge cases

- Quantity `1`, a large positive value, `0`, and a negative value.
- Empty, Unicode, spaced, colon-containing, and pipe-containing identifiers.
- Two applications with equal configuration and two with different configuration.
- Multiple sequential and overlapping request scopes.
- Gateway creation failure, request body failure, operation failure, and both cleanup layers.
- Double shutdown and request-after-shutdown policy.
- Tests executed in a fresh interpreter and after the module is already cached.

## Commands

From the repository root:

```bash
uv run --locked python units/pythonic/SDP-PYT-050-modules-import-caching-dependency-lifetimes/practice/fulfillment_lab.py
uv run --locked pytest -q -p no:cacheprovider units/pythonic/SDP-PYT-050-modules-import-caching-dependency-lifetimes/practice
```

Record actual commands and output. Never treat starter green tests as learner evidence.

## Rahul's attempt

- Attempt file: —
- Prediction: —
- Design explanation: —
- Rejected alternative: —
- Test result: —

## Progressive hints

No hints are released. Ask for one at a time after recording an attempt.

## Observe and explain

After running and refactoring, explain:

1. Which cache behavior made the old global appear Singleton-like?
2. Which boundary now owns gateway construction and shutdown?
3. Which boundary now owns a session and why can it not escape?
4. Which tests prove two-app isolation instead of merely resetting globals?
5. Which failure has priority if cleanup also raises?
6. Which abstraction could still be removed?

## Refactor checkpoint

The target is not “use more classes.” It is visible construction, explicit ownership, deterministic
release, and the smallest dependency surface that lets policy run without importing infrastructure.

## Vary

Choose one change without implementing all of them:

- one application needs two named warehouse gateways;
- a tenant chooses a gateway per request;
- a request schedules work after the response boundary;
- startup is asynchronous and partially acquires two resources; or
- four worker processes serve the same deployment.

State which lifetime changes, which stays stable, and which old assumption is now false.

## Troubleshooting

- Run from the repository root so pytest discovers the sibling starter module consistently.
- Patch `fulfillment_lab.warehouse_gateway`, where the function resolves the name; patching an
  unrelated imported alias does not change that lookup.
- If test order matters, global state still leaks. Prove independent applications instead of
  adding broader reset fixtures.
- If import probing becomes confusing, use a subprocess for a fresh interpreter rather than
  deleting arbitrary essential entries from `sys.modules`.

## Closure

Add only after Rahul closes the exercise.

- Final learner solution: —
- Optional comparison solution: —
- Trade-offs: —
- Remaining weakness: —
- Evidence link for `PROGRESS.md`: —
