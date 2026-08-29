# SDP-FND-080 — Dependency management, test seams, and test doubles

## Physical Notebook Core

Keep this section short enough to reconstruct by hand. It is not a duplicate of the full note.

### Problem or change pressure

Business code needs time, storage, network clients, randomness, configuration, or outgoing
messages. If it also chooses and constructs those collaborators at the moment it uses them, tests
must fight hidden wiring, real side effects, nondeterminism, and lifetime decisions. The answer is
not “mock everything”; it is to expose the smallest honest control point, then choose the least
powerful double that supplies the evidence the test needs.

### One-sentence mental model

> A seam is a controlled place where behavior can vary; explicit dependencies put that place in
> the design, and a test double is one possible test-time collaborator—not proof of the real
> integration.

### One essential visual

```text
                         ASSEMBLY / CONFIGURATION
                chooses concrete objects and their lifetimes
                           │                 │
              production  │                 │  test
                           ▼                 ▼
                    real adapter         test double
                           │                 │
                           └────────┬────────┘
                                    ▼
                         EXPLICIT DEPENDENCY SEAM
                       parameter • constructor • callable
                                    │
                                    ▼
                              POLICY / USE CASE
                         uses capability; does not locate it
                                    │
                                    ▼
                         OBSERVABLE RESULT OR EFFECT
                    state assertion • contract • interaction

              unit evidence ──────────────┐
              contract evidence ──────────┼──> confidence
              integration evidence ───────┘    (different claims)
```

### How to read this visual

Start at assembly. Production and test code may choose different collaborators, but both enter the
same explicit seam. Follow the arrow into the use case: policy uses the capability without looking
it up globally or constructing it. Then read the bottom lanes as complementary evidence. A fast
test with a double proves the policy under the supplied behavior; contract and integration tests
must prove different boundary claims.

### Key insight

The valuable design move is making a dependency and its ownership visible. A mock library is only
a tool for supplying or observing one collaborator after that decision.

### Simplification or limitation

The visual is conceptual. Frameworks may perform assembly, one callable can satisfy several roles,
and a test may use a real cheap collaborator. It omits processes, transactions, retries,
concurrency, security, and distributed failure. “Explicit” does not require every value to become
a constructor argument or every collaborator to have an interface class.

### Governing rules or invariants

1. Separate **configuration from use**: the code deciding which collaborator and lifetime to use
   should normally sit outside the policy that needs the capability.
2. Add a seam for a real change, control, or boundary need; prefer a value, function, callable, or
   small object before a framework or speculative interface hierarchy.
3. Choose doubles by their role in one test, assert observable behavior by default, and add
   contract or integration evidence for semantics and wiring that the double cannot prove.

### Minimal Python example

```python
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Digest:
    account_id: str
    created_at: datetime


def build_digest(
    account_id: str,
    *,
    now: Callable[[], datetime],
) -> Digest:
    return Digest(account_id=account_id, created_at=now())


fixed = datetime.fromisoformat("2026-08-29T12:30:00+00:00")
result = build_digest("acct-7", now=lambda: fixed)
assert result == Digest("acct-7", fixed)
```

Time is a zero-argument capability, so a callable is enough. The function does not need a clock
class, a mock framework, or knowledge of how production obtains wall-clock time.

### One common misconception

**Mistake:** “Dependency injection means using a container and replacing every dependency with a
mock in unit tests.”

**Correction:** Passing a value or callable explicitly is already injection. Use real, cheap,
deterministic collaborators where they make the test clearer. Use a stub, fake, spy, or mock only
for the control or observation required by that test. A container is an optional assembly tool,
not the definition of dependency injection.

### Important trade-offs

- Explicit parameters reveal collaborators and simplify local reasoning, but too many independent
  parameters can expose a responsibility that should be split or assembled into a cohesive
  service.
- Handwritten fakes can make state-based tests readable and fast, but they can drift semantically
  from the real adapter and therefore need bounded contract tests.
- Mocks make otherwise invisible interactions observable and can model failures precisely, but
  broad or choreography-heavy assertions couple tests to implementation choices.
- Patching is valuable for legacy code and narrow platform seams, but its target depends on Python
  lookup names; repeated patching of ordinary collaborators often signals hidden assembly.
- More isolation improves fault localization, while too much isolation can leave real wiring,
  serialization, transactions, and provider behavior untested.

### Interview-revision cues

- Start with the hidden dependency or nondeterministic boundary, not with a preferred mocking tool.
- Distinguish dependency injection, dependency inversion, inversion of control, service location,
  fixtures, monkeypatching, and test doubles.
- Classify dummy, stub, fake, spy, and mock by their role in a test, not by the Python class used.
- Say “patch where the system under test looks up the name.”
- Prefer state or output verification; use interaction verification when the interaction itself is
  a requirement, such as “do not charge twice” or “publish this audit record.”
- Explain what the unit test cannot prove and name the smallest contract or integration test that
  closes that gap.
- Reject a new interface when a value, callable, small real object, or direct function is enough.

## Unit metadata

| Field | Value |
|---|---|
| Domain | Design foundations |
| Curriculum | [SDP-FND-080](../../../CURRICULUM.md#sdp-fnd-080) |
| Progress | [PROGRESS.md](../../../PROGRESS.md) |
| Python references | [PYTHON_REFERENCES.md](../../../PYTHON_REFERENCES.md) — hard `PY-TST-020`, `PY-TST-040`, `PY-TST-070` bridge |
| Learning outcome | Expose controllable seams, pass dependencies explicitly, and choose fakes, stubs, spies, or mocks without coupling tests to implementation details. |
| Hard prerequisites | `SDP-FND-030`, `SDP-FND-070` |
| Soft prerequisites | None |
| Priority | Core |
| Interview frequency | High |
| Production frequency | High |
| Python/backend relevance | High |
| Depth | D2 |
| Scope | Design, Testing |
| Size | L |
| Evidence profile | E+I+D+T |
| Canonical Python | Python 3.14 |
| Interview compatibility | Python 3.11 |
| Artifact state | Approved |

The frequency fields above are curriculum judgments, not measurements from a population survey.

## 1. Simple explanation

Imagine a cook who must make soup.

The cook needs vegetables, water, and heat. There are two ways to organize the kitchen:

1. Every time the cook starts, the cook buys a farm, drills a well, and builds a stove.
2. The kitchen supplies ingredients and a working heat source; the cook makes soup.

The first cook owns both **configuration** and **use**. That makes changing the supplier,
controlling temperature, or testing one recipe unnecessarily difficult.

Software has the same problem:

```python
def create_report(account_id: str) -> Report:
    database = ProductionDatabase.from_environment()
    clock = SystemClock()
    exporter = CloudExporter()
    ...
```

The function may look self-contained, but it hides important facts:

- it needs a database;
- it reads environment configuration;
- it chooses a cloud exporter;
- it chooses when those resources are created and destroyed;
- it obtains real time;
- it may perform side effects during a simple call.

If those choices move to an assembly boundary, the policy becomes easier to understand and test:

```python
def create_report(
    account_id: str,
    database: ReportDatabase,
    export: ExportReport,
    now: Clock,
) -> Report: ...
```

This does not mean every dependency must be fake. A test might use:

- a real immutable value;
- a real pure formatter;
- a temporary directory;
- a small in-memory repository fake;
- a stub clock;
- a spy exporter;
- one mock for an interaction whose exact occurrence matters.

The senior question is:

> Which collaborators must this policy control or observe, what is their smallest honest
> contract, who should select and own them, and which mix of real objects and doubles gives the
> required evidence without describing private choreography?

## 2. Prerequisite bridge

### From SDP-FND-030 — cohesion, coupling, and dependency direction

`SDP-FND-030` supplies three essential ideas:

1. A dependency is any fact one part of the system must know or rely upon.
2. Coupling is not automatically bad; hidden, broad, unstable, or wrongly directed coupling makes
   change expensive.
3. A boundary should protect stable policy from volatile details rather than add indirection with
   no change pressure.

Quick reconstruction:

```text
policy ──uses capability──> boundary contract <──implemented by── volatile detail
```

For this unit, add a construction question:

```text
composition root ──chooses detail──> policy receives capability
```

The first arrow is collaboration. The second is assembly. Mixing both responsibilities in the
policy is the testing pain explored here.

### From SDP-FND-070 — Python interface choices

`SDP-FND-070` distinguishes runtime duck typing, static structural typing with `Protocol`, nominal
inheritance, and ABC enforcement.

For test seams:

- a runtime call needs an object with the operation;
- a `Protocol` can describe that client-shaped operation to a type checker;
- neither production nor test implementations need to inherit the `Protocol`;
- an ABC is not justified just because two implementations exist;
- shape compatibility still does not prove behavioral meaning.

```text
test double has the right method shape?       ← typing/mechanism claim
test double preserves the required meaning?  ← contract/evidence claim
```

Keep those claims separate.

### Python testing bridge

The hard Python references are:

- `PY-TST-020`: pytest tests, assertions, parametrization, and fixtures;
- `PY-TST-040`: doubles, mocking, and patch target boundaries;
- `PY-TST-070`: formatting, linting, static analysis, and maintainability.

Minimum bridge:

1. A pytest fixture supplies arrange-state to a test through an explicit test-function parameter.
2. `monkeypatch` temporarily changes attributes, mappings, environment variables, paths, or the
   working directory and restores them after the requesting test or fixture.
3. `unittest.mock.patch` must replace the name where the system under test looks it up.
4. `Mock` can both supply values and record calls; those mechanics do not decide whether its role
   is stub, spy, or mock.
5. A passing isolated test does not prove the production graph is wired correctly.

The prerequisite artifacts are approved, but `PROGRESS.md` does not record Rahul's learning
evidence for them. This bridge supports study; it does not manufacture prerequisite mastery.

## 3. Start with the change pressure

A direct implementation may be exactly right:

```python
def delivery_fee(weight_kg: int) -> int:
    if weight_kg <= 0:
        raise ValueError("weight_kg must be positive")
    return 500 + weight_kg * 40
```

It is deterministic, pure, cheap, and locally complete. Creating a `FeeCalculator` interface and
mocking it would reduce clarity.

Pressure appears when the policy crosses boundaries or relies on inputs it cannot control:

- current time changes between runs;
- random or unique identifiers make exact results unpredictable;
- network and database operations are slow or unavailable;
- a payment provider can decline, time out, or return malformed data;
- sending email or publishing events is an irreversible side effect;
- environment and module state leak between tests;
- a collaborator's lifetime carries business meaning, such as idempotency or transaction scope;
- tests require failure paths that production dependencies rarely produce on demand;
- construction requires secrets, sockets, threads, or framework state;
- changing an import or helper sequence breaks many tests even though behavior remains stable.

The force is not “we want 100% unit-test isolation.” The force is that a policy needs controlled,
observable collaboration while production still needs honest integration.

## 4. Precise working vocabulary

### Dependency

A dependency is a value, service, operation, module, state, environment fact, or timing guarantee
that code relies on.

Not all dependencies are objects:

- `tax_rate: Decimal` is a value dependency;
- `now: Callable[[], datetime]` is an operation dependency;
- a repository is a stateful collaborator;
- an environment variable is a process-state dependency;
- “this function runs after startup” is a temporal dependency.

### Collaborator

A collaborator is another object or callable with which the system under test communicates during
the behavior being examined. A dependency may be static data that is not meaningfully a
collaborator.

### Dependency injection

Dependency injection means that a needed dependency is supplied from outside the code that uses
it, rather than selected through hidden construction or lookup inside that code.

Python forms include:

- function-parameter injection;
- constructor injection;
- a closure or factory capturing dependencies;
- explicit property/setter injection for genuinely optional or reconfigurable collaboration;
- framework-provided parameters, when the framework is the assembly boundary.

Injection is a wiring mechanism. It is not the Dependency Inversion Principle; `SDP-SOL-050`
owns the policy-level source dependency rule.

### Composition root

A composition root is the visible place where concrete objects, configuration, and lifetimes are
assembled into an application graph. In a small Python program it may be `main()`, an application
factory, a CLI entry point, or startup code. A framework can host this work, but business policy
should not depend on the container API merely to locate ordinary collaborators.

### Test seam

A test seam is a controlled place where a test can supply, replace, or observe behavior without
performing the unwanted real action.

A seam is broader than an interface class. It can be:

- a function argument;
- a constructor parameter;
- a callable;
- an adapter boundary;
- a temporary filesystem path;
- an environment mapping;
- a transaction boundary;
- a module name patched where it is looked up;
- a subprocess or HTTP boundary controlled by a test server.

### Test double

“Test double” is the umbrella term for an object or callable standing in for a collaborator in a
test. Dummy, stub, fake, spy, and mock describe different roles.

### Fixture

A fixture is the defined test context used during arrange, and sometimes teardown. It may create
real objects, values, doubles, files, or services. A fixture is not itself a synonym for a test
double or for production dependency injection.

### System under test

The system under test (SUT) is the behavior or component on which a test is focused. Its boundary
must be named clearly enough to distinguish observable behavior from the private work it performs.

## 5. Historical and library context

Martin Fowler's 2004 article on dependency injection compares injection with service location and
argues that the more fundamental concern is separating service configuration from service use. It
describes constructor, setter, and interface injection in the Java container context
([Fowler, “Inversion of Control Containers and the Dependency Injection pattern”](https://martinfowler.com/articles/injection.html)).

Modern Python does not require those Java container mechanics. Plain arguments, callables,
factories, and application startup code often express the same separation with less machinery.

Fowler's 2007 revision of “Mocks Aren't Stubs” follows Gerard Meszaros's test-double vocabulary and
distinguishes state verification from behavior/interaction verification. Its five roles—dummy,
fake, stub, spy, and mock—remain useful even though Python's `unittest.mock.Mock` class can be used
to perform several of them
([Fowler, “The Difference Between Mocks and Stubs”](https://martinfowler.com/articles/mocksArentStubs.html#TheDifferenceBetweenMocksAndStubs)).

The Python standard library has included `unittest.mock` since Python 3.3. Its documentation
describes `Mock` as a configurable object that creates attributes on access, records usage, and
supports action-then-assertion verification. That library contract is distinct from the design
decision about which collaborator should be doubled
([Python 3.14 `unittest.mock`](https://docs.python.org/3.14/library/unittest.mock.html)).

Do not tell a history in which dependency injection was invented for unit testing or in which
every configurable collaborator became a “mock.” The design problem is assembly and dependency
visibility; testing is one powerful feedback mechanism.

## 6. Design mechanics versus Python and library mechanics

| Claim | Classification | Evidence source |
|---|---|---|
| Configuration and use should be separated when collaborator choice varies | Design principle | Change analysis and architecture |
| A function parameter is an explicit seam | Pythonic design mechanism | Function signature and call site |
| `from module import name` creates a binding in the importing namespace | Python name-binding mechanism | Language behavior |
| `patch()` must target the name the SUT looks up | Standard-library contract | `unittest.mock` documentation and experiment |
| `autospec` checks visible members and call signatures | Standard-library contract | `unittest.mock` documentation and experiment |
| pytest `monkeypatch` restores requested changes after the test/fixture | pytest framework behavior | pytest documentation |
| A fake preserves the real adapter's semantics | Not guaranteed | Shared contract and integration evidence |
| A mock assertion proves the real provider received a request | Not guaranteed | Requires integration/observability evidence |

No CPython internals are required for this unit. The patch experiment demonstrates documented name
lookup and library behavior; it does not inspect interpreter implementation details.

## 7. Participants and responsibilities

| Participant | Responsibility | What it must not own |
|---|---|---|
| Policy / use case | Make business decisions and coordinate required capabilities | Hidden selection of volatile adapters and unrelated lifetimes |
| Boundary contract | Express the smallest behavior and meaning the policy needs | A provider's entire SDK or test-framework API |
| Production adapter | Translate the boundary contract to a database, clock, provider, queue, or platform | Business policy unrelated to translation |
| Composition root | Select implementations, configuration, ownership, and cleanup | Domain decisions merely because it constructs objects |
| Test | State one behavior, arrange controlled collaborators, and verify relevant evidence | Production wiring assumptions it never exercises |
| Test double | Supply or observe a collaborator role for one test | Pretending to prove real integration semantics |
| Contract test | Apply shared boundary examples to implementations | Every provider or infrastructure behavior |
| Integration test | Prove selected real components are wired and collaborate | Exhaustive policy combinations already covered cheaply |

## 8. Collaboration and execution flow

```mermaid
sequenceDiagram
    participant Root as Composition root
    participant UseCase as Renewal policy
    participant Ledger as Repository boundary
    participant Gateway as Payment boundary
    participant Audit as Audit boundary
    Root->>UseCase: construct(ledger, gateway, clock, audit)
    Note over Root,UseCase: configuration ends; use begins
    UseCase->>Ledger: find(request_id)
    alt prior receipt exists
        Ledger-->>UseCase: saved receipt
        UseCase-->>Root: saved receipt
    else first request
        Ledger-->>UseCase: none
        UseCase->>Gateway: charge(command)
        Gateway-->>UseCase: approved / declined
        UseCase->>Ledger: save(receipt)
        UseCase->>Audit: publish(receipt)
        UseCase-->>Root: receipt
    end
```

### How to read this visual

Read the first arrow separately from the rest: it is assembly. Then follow one runtime request. The
policy speaks only in boundary operations. In a unit test, the root supplies controlled doubles;
in production, it supplies adapters. The interaction shape is stable while implementations vary.

### Key insight

The repeated-request rule depends on repository state surviving more than one use-case call.
Making the repository explicit reveals that lifetime requirement; mocking a private constructor
can hide it.

### Simplification or limitation

This flow assumes a synchronous local transaction and one process. It omits race conditions,
exactly-once delivery, rollback after audit failure, outbox messaging, and provider idempotency.
Those require additional architecture; a unit-test seam alone does not solve them.

## 9. The simplest design before adding a seam

Use direct code when the dependency is stable, cheap, deterministic, and local:

```python
from decimal import Decimal


def apply_discount(subtotal: Decimal, percent: int) -> Decimal:
    if not 0 <= percent <= 100:
        raise ValueError("percent must be between 0 and 100")
    return subtotal * (Decimal(100 - percent) / Decimal(100))
```

A test can pass ordinary values and assert the result. There is no volatile collaborator and no
test double is needed.

Even when a helper exists, prefer the real helper if it is pure and trustworthy:

```python
def normalize_email(value: str) -> str:
    return value.strip().casefold()
```

Mocking `normalize_email()` would replace the behavior that the test most likely needs to verify.

## 10. Before-seam code and concrete pain

```python
from datetime import UTC, datetime
from uuid import uuid4


def register_account(email: str) -> str:
    repository = PostgresAccountRepository.from_environment()
    mailer = SmtpWelcomeMailer.from_environment()
    account_id = str(uuid4())
    account = Account(account_id, email, datetime.now(UTC))
    repository.add(account)
    mailer.send(account)
    return account_id
```

One function owns at least six concerns:

1. validating or normalizing the request;
2. selecting a database adapter;
3. reading environment configuration;
4. choosing an ID source;
5. choosing a clock;
6. choosing and invoking email infrastructure.

Testing a duplicate email, deterministic timestamp, ID collision, database failure, or mail
failure now requires real infrastructure or patches tied to this module's imports. The problem is
not that `datetime` or `uuid4` are “untestable.” The policy has fused its stable decisions with
volatile construction.

### A patch-only characterization

```python
from unittest.mock import patch


@patch("accounts.registration.SmtpWelcomeMailer")
@patch("accounts.registration.PostgresAccountRepository")
@patch("accounts.registration.uuid4")
@patch("accounts.registration.datetime")
def test_registers(...):
    ...
```

This can be an appropriate first step in legacy code. It preserves behavior before refactoring.
It becomes a design smell when many tests must reproduce the private construction graph and fail
after harmless import or helper changes.

## 11. Explicit dependency passing in Python

### Parameter injection

Best for a small operation whose dependencies are few and local:

```python
from collections.abc import Callable
from datetime import datetime


def issue_reference(
    prefix: str,
    *,
    now: Callable[[], datetime],
    next_sequence: Callable[[], int],
) -> str:
    return f"{prefix}-{now():%Y%m%d}-{next_sequence():06d}"
```

Advantages:

- dependencies appear at the call site;
- no instance lifetime is introduced;
- callables work naturally with functions, bound methods, closures, and callable objects.

Cost:

- many parameters can make every call noisy;
- repeatedly forwarding dependencies through unrelated layers may reveal a missing application
  service or composition boundary.

### Constructor injection

Best when an object is invalid without its collaborators or reuses them across operations:

```python
from dataclasses import dataclass


@dataclass
class AccountService:
    repository: AccountRepository
    send_welcome: SendWelcome

    def register(self, command: RegisterAccount) -> Account: ...
```

Advantages:

- one valid object holds required capabilities;
- dependency visibility and lifetime are clear;
- repeated method calls share intended collaborator state.

Cost:

- a large constructor can expose too many responsibilities;
- storing one-shot values as object fields may lengthen their lifetime unnecessarily.

### Closure or factory injection

Useful for a small configured function:

```python
from collections.abc import Callable


def make_sender(transport: Callable[[bytes], None]) -> Callable[[str], None]:
    def send(message: str) -> None:
        transport(message.encode("utf-8"))

    return send
```

The returned callable is already assembled. Do not wrap it in a class only to make the injection
look more formal.

### Setter or property injection

Use only when a collaborator is genuinely optional or must change during a valid object's life.
It permits temporarily invalid or partially configured objects if required collaborators are set
later.

```python
service.audit = audit_publisher
```

In ordinary Python application code, explicit constructor or function parameters usually make
invariants clearer.

### Default-argument trap

This looks injectable but captures the object at function definition time:

```python
from datetime import UTC, datetime


def created_at(now=datetime.now) -> datetime:
    return now(UTC)
```

Patching `datetime.now` later does not replace the already-bound default. Prefer an explicit
required parameter at policy level, or use a thin outer wrapper that supplies the production
default deliberately:

```python
def created_at(*, now: Clock) -> datetime:
    return now()


def created_at_now() -> datetime:
    return created_at(now=lambda: datetime.now(UTC))
```

## 12. A typed production-oriented example

This shipping quote example is separate from the practice lab so it teaches the mechanics without
revealing the learner's final renewal design.

```python
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Protocol


@dataclass(frozen=True)
class Rate:
    service_code: str
    amount_cents: int


@dataclass(frozen=True)
class Quote:
    order_id: str
    rate: Rate
    quoted_at: datetime


class RateProvider(Protocol):
    def cheapest(self, *, postal_code: str, weight_grams: int) -> Rate: ...


AuditQuote = Callable[[Quote], None]
Clock = Callable[[], datetime]


@dataclass
class QuoteShipping:
    rates: RateProvider
    now: Clock
    audit: AuditQuote

    def execute(
        self,
        *,
        order_id: str,
        postal_code: str,
        weight_grams: int,
    ) -> Quote:
        if weight_grams <= 0:
            raise ValueError("weight_grams must be positive")
        rate = self.rates.cheapest(
            postal_code=postal_code,
            weight_grams=weight_grams,
        )
        quote = Quote(order_id=order_id, rate=rate, quoted_at=self.now())
        self.audit(quote)
        return quote


class CarrierRateAdapter:
    def cheapest(self, *, postal_code: str, weight_grams: int) -> Rate:
        # Translate a real provider response and failures here.
        ...


def build_quote_shipping() -> QuoteShipping:
    return QuoteShipping(
        rates=CarrierRateAdapter(),
        now=lambda: datetime.now(UTC),
        audit=ProductionAuditPublisher().publish,
    )
```

Why each abstraction exists:

- `RateProvider` names a client-shaped, multi-field query used across a volatile adapter boundary.
- `Clock` is only one operation, so a callable alias is enough.
- `AuditQuote` is a one-operation side-effect boundary, so a bound method can satisfy it.
- `QuoteShipping` stores collaborators because multiple requests can reuse the configured service.
- `build_quote_shipping()` owns production selection; tests can construct `QuoteShipping` directly.

What is deliberately absent:

- no ABC;
- no base class for doubles;
- no container;
- no service locator;
- no repository because the scenario does not require persistence;
- no retry abstraction before a retry requirement exists.

## 13. Test seam catalog

| Seam | Python form | Good fit | Main risk |
|---|---|---|---|
| Value seam | parameter or immutable data | configuration, dates, thresholds, IDs already known | turning every constant into indirection |
| Callable seam | `Callable`, function, bound method, closure | time, ID generation, one-operation policy or effect | losing a useful named semantic contract when behavior grows |
| Object seam | duck-typed object or `Protocol` | stateful or multi-operation collaborator | broad “god port” copied from provider SDK |
| Constructor seam | required field/argument | reusable service and lifetime visibility | oversized constructor exposing mixed responsibilities |
| Composition seam | app factory, `main`, startup hook | choosing implementations and cleanup | business code depending on container APIs |
| Adapter seam | client-owned translation wrapper | third-party APIs, exception and data translation | leaking provider models through the boundary |
| Module patch seam | `patch`, `monkeypatch.setattr` | legacy code, narrow globals, platform facilities | coupling to import and lookup details |
| Environment seam | explicit mapping or `monkeypatch.setenv` | configuration reader tests | environment access scattered through policy |
| Filesystem seam | `tmp_path`, file-like object, path parameter | file behavior and serialization | mocking `open()` so deeply that file semantics disappear |
| Process/service seam | subprocess, local server, containerized dependency | real serialization, protocol, wiring | speed, flakiness, setup and cleanup cost |

### Seam selection questions

1. What must the test control: data, time, outcome, failure, state, or an outgoing effect?
2. Is the real collaborator cheap, deterministic, and safe? If yes, use it.
3. Is the boundary one operation? Consider a callable.
4. Does state or a family of operations matter? Consider a small object contract.
5. Is the API shape incompatible? Add an adapter, not a wishful fake.
6. Is the code legacy and unsafe to refactor without characterization? Patch tactically first.
7. What claim still requires a real integration test?

## 14. Test-double taxonomy

The role belongs to a test arrangement, not permanently to a class.

| Role | What it does | How the test normally uses it | Pythonic example |
|---|---|---|---|
| Dummy | Fills a required parameter but is not used on that path | Pass and ignore | `object()` or a sentinel |
| Stub | Supplies a controlled answer or failure | Assert SUT output/state | `lambda: fixed_time`; configured `return_value` |
| Fake | Implements working behavior through a production-unsuitable shortcut | Exercise and inspect state | in-memory repository |
| Spy | Records what happened for later assertions, often while also stubbing | Assert selected calls or captured values after exercise | list-appending function; handwritten recorder |
| Mock | Is configured with expected interactions and verified against them | Behavior/interaction verification | autospecced mock with call expectations |

### Dummy

```python
UNUSED_AUDIT = object()

# Validation fails before audit can be used.
with pytest.raises(ValueError):
    service.execute(invalid_request, audit=UNUSED_AUDIT)
```

If the object is unexpectedly used, a purpose-built exploding dummy can make the failure clearer.

### Stub

```python
fixed_now = datetime.fromisoformat("2026-08-29T12:30:00+00:00")
clock = lambda: fixed_now
```

The test controls an indirect input and asserts the returned business result. It does not need to
assert that `clock()` was called exactly once unless the call count has business meaning.

### Fake

```python
class InMemoryReceiptRepository:
    def __init__(self) -> None:
        self.by_request_id: dict[str, Receipt] = {}

    def find(self, request_id: str) -> Receipt | None:
        return self.by_request_id.get(request_id)

    def save(self, receipt: Receipt) -> None:
        self.by_request_id[receipt.request_id] = receipt
```

This fake has real state and behavior. It does not reproduce transactions, durability,
concurrency, collation, query semantics, or database errors unless those are deliberately modeled
and contract-tested.

### Spy

```python
published: list[Quote] = []
service = QuoteShipping(rates=stub_rates, now=stub_clock, audit=published.append)

quote = service.execute(...)

assert published == [quote]
```

`list.append` is a tiny spy. No custom spy class or mock framework is required.

### Mock

```python
from unittest.mock import create_autospec


audit = create_autospec(AuditPublisher, instance=True, spec_set=True)
service = Service(..., audit=audit)

result = service.execute(command)

audit.publish.assert_called_once_with(result)
```

This is justified when publishing exactly that record is itself part of the required behavior. It
is weak if the test asserts every internal query and helper call merely because they are visible.

### One object, several possible roles

```python
gateway = create_autospec(PaymentGateway, instance=True, spec_set=True)
gateway.charge.return_value = Approved("pay-42")  # stub behavior

result = service.execute(command)

gateway.charge.assert_called_once_with(command)  # spy-like post-hoc assertion
```

The Python object is a `Mock` instance. In test-double vocabulary it supplies a stubbed result and
records a spy observation. If the test defines required interaction expectations as its primary
verification, it is serving a mock role. Library type and test role answer different questions.

## 15. State, output, and interaction verification

### Output verification

```python
assert quote.rate.amount_cents == 799
```

Use when the public result expresses the behavior.

### State verification

```python
assert fake_repository.find("req-42") == receipt
```

Use when collaborator state is a meaningful observable result.

### Interaction verification

```python
gateway.charge.assert_not_called()
```

Use when the collaboration itself is a requirement. Examples:

- an invalid command must produce no side effect;
- an idempotent retry must not charge again;
- a successful operation must write a required audit record;
- a security boundary must call an authorization decision before protected work;
- a transaction must not commit after an error.

Avoid interaction assertions for replaceable choreography:

- which private helper ran;
- exact call order when order has no semantic effect;
- whether one query replaced two queries after optimization;
- which concrete class the composition root constructed in a policy unit test;
- every property accessed on a collaborator.

### The refactoring-resistance test

Ask:

> If I preserve every externally meaningful result and effect but reorganize private work, should
> this test still pass?

If yes, an interaction assertion tied to that private work is overspecified.

## 16. `unittest.mock` mechanics and limits

### Plain `Mock`

A plain `Mock` creates child mocks on attribute access and records calls. This is convenient but
can accept misspellings or APIs that do not exist:

```python
gateway = Mock()
gateway.chagre(500)  # typo creates and calls a child Mock
```

The practice experiment reproduces this behavior.

### `spec`

`spec=SomeType` restricts readable attributes to names visible on the spec. It does not recursively
enforce every child call signature.

### `spec_set`

`spec_set=SomeType` is stricter: getting or setting absent attributes raises `AttributeError`.

### `create_autospec`

`create_autospec()` recursively derives visible member specs and checks function or method call
signatures. With `spec_set=True` it can catch both misspelled attributes and invalid call shapes
([Python 3.14 `create_autospec`](https://docs.python.org/3.14/library/unittest.mock.html#unittest.mock.create_autospec)).

Autospec does **not** prove:

- return-value meaning;
- business invariants;
- exception semantics;
- network serialization;
- provider behavior;
- production wiring.

The documentation also records limits: autospec discovers attributes through introspection,
properties or descriptors may execute during that traversal, and attributes created only in
`__init__` may not be visible from a class spec
([Python 3.14, autospeccing caveats](https://docs.python.org/3.14/library/unittest.mock.html#autospeccing)).

### `return_value`, `side_effect`, and `wraps`

- `return_value` supplies a canned result: commonly a stub role.
- `side_effect` can raise, calculate a result, or yield successive results: useful for controlled
  failure and sequence tests.
- `wraps` delegates to a real object while recording calls: often a spy or partial-double role.

When combined, the documented precedence is `side_effect`, then `return_value`, then `wraps`
([Python 3.14, order of precedence](https://docs.python.org/3.14/library/unittest.mock.html#order-of-precedence-of-side-effect-return-value-and-wraps)).

Prefer one clear mechanism per test. Clever stacks of all three are hard to diagnose.

### `AsyncMock`

`AsyncMock` produces an awaitable and records awaits separately from calls. A coroutine can be
called without being awaited, so use `assert_awaited*` when awaiting is the meaningful interaction
([Python 3.14 `AsyncMock`](https://docs.python.org/3.14/library/unittest.mock.html#unittest.mock.AsyncMock)).

Do not convert synchronous domain policy to async merely because an adapter is async. Keep async at
the boundary unless concurrency is part of the policy.

### Sealing

`unittest.mock.seal()` prevents automatic creation of new child mocks after configuration. It can
make a deliberately configured graph stricter, but it does not repair an over-broad boundary.

## 17. Patching and Python name lookup

`patch()` temporarily rebinds a name. It does not mutate every alias to the original object.

Suppose:

```python
# source.py
class Gateway: ...


# service.py
from source import Gateway


def execute():
    return Gateway().call()
```

`execute()` looks up `Gateway` in `service`, so the effective target is:

```python
@patch("service.Gateway")
```

Patching `source.Gateway` after `service` imported the name leaves `service.Gateway` unchanged.
Python's documentation states the rule directly: patch where the object is looked up, which may
differ from where it is defined
([Python 3.14, “Where to patch”](https://docs.python.org/3.14/library/unittest.mock.html#where-to-patch)).

### Patching is appropriate when

- characterizing legacy behavior before a safe refactor;
- controlling a narrow standard-library or process boundary;
- testing configuration readers against environment or module state;
- a framework owns construction and exposes a documented override mechanism;
- explicit injection would leak a platform detail through many policy layers.

### Patching is a warning sign when

- every policy test patches several ordinary application collaborators;
- test targets mirror private module layout;
- harmless import changes break many tests;
- child-mock chains reproduce a provider SDK;
- test setup is longer than the behavior being verified;
- patching hides a lifetime or ownership defect.

### pytest `monkeypatch`

pytest's `monkeypatch` fixture can set or delete attributes, mapping items, and environment
variables, change directories, and alter `sys.path`. Requested modifications are undone after the
test or fixture completes
([pytest monkeypatch guide](https://docs.pytest.org/en/stable/how-to/monkeypatch.html)).

It does not change the design rule: target the binding the SUT reads, and prefer an explicit seam
when collaborator choice belongs in assembly.

## 18. Fixtures are test assembly, not production service location

pytest fixtures are explicit arrange functions requested through test or fixture parameters. The
pytest documentation emphasizes explicit, modular, scalable setup and gives each test fresh
function-scoped fixture state by default
([pytest fixture explanation](https://docs.pytest.org/en/stable/explanation/fixtures.html)).

```python
@pytest.fixture
def fake_repository() -> InMemoryRepository:
    return InMemoryRepository()


def test_registers(fake_repository: InMemoryRepository) -> None:
    service = RegistrationService(repository=fake_repository, ...)
    ...
```

The fixture assembles the test. Production code does not ask pytest for a repository.

### Fixture scope is a lifetime decision

- function scope: fresh per test; safest mutable default;
- class/module scope: shared within a broader group;
- package/session scope: shared widely, often for expensive resources.

A shared mutable fake can leak state and make tests order-dependent. Expand scope only for a named
cost and reset or isolate state deliberately.

### Avoid invisible autouse overreach

Autouse fixtures are useful for universal safety guards, such as blocking network access. They can
also hide setup and make a test's dependencies difficult to see. Prefer requested fixtures for
behavior-specific collaborators.

## 19. Fakes and contract tests

A fake is real code. It can contain bugs and semantic differences.

Common drift:

- dictionary lookup versus database collation;
- immediate visibility versus transaction isolation;
- no uniqueness constraints;
- no serialization round trip;
- no timeouts, partial failures, or connection loss;
- object identity preserved when a real adapter reconstructs data;
- query ordering accidentally deterministic;
- no optimistic locking or version checks.

### Shared contract pattern

```python
def repository_contract(make_repository: Callable[[], AccountRepository]) -> None:
    repository = make_repository()
    account = Account(...)
    repository.add(account)
    assert repository.get(account.account_id) == account
    with pytest.raises(DuplicateAccount):
        repository.add(account)
```

Run the same behavioral examples against:

- the fast fake;
- the real adapter with an isolated test resource;
- optionally multiple provider adapters.

Contract tests prove only the examples encoded. Keep integration tests for configuration,
migrations, credentials, network protocol, cleanup, and production-specific semantics.

The practice fake-contract experiment demonstrates one bounded drift case rather than claiming a
fake can become a complete database emulator.

## 20. Failure modeling

Dependency seams make failures controllable, but a double must use application-relevant failure
meaning.

```python
gateway.charge.side_effect = PaymentUnavailable("timeout")
```

Before configuring the failure, decide:

1. Is it an expected business result or an infrastructure failure?
2. Which layer translates a provider exception?
3. May the operation be retried safely?
4. What state changed before failure?
5. What must be logged or measured?
6. What does the caller observe?

### Failure matrix

| Failure | Unit evidence | Contract/integration evidence |
|---|---|---|
| Normal decline | translated result and no inappropriate retry | provider adapter maps real decline payload |
| Timeout | policy surfaces or retries as specified | client timeout and exception mapping are configured |
| Duplicate save | idempotency decision | database constraint and transaction behavior |
| Audit failure | state/return policy | broker/client failure and delivery semantics |
| Invalid input | no outgoing collaborators used | request boundary maps validation correctly |

Do not assert only that “an exception was raised.” Assert the application meaning and side-effect
boundary.

## 21. Observability and debugging

Explicit dependencies improve diagnostics because a composition root can name and configure each
adapter visibly.

Useful production context:

- operation and request ID;
- adapter/provider name;
- outcome category, not secret payload;
- duration at the boundary;
- retry count and final result;
- translated error code;
- idempotency decision;
- correlation or trace identifier.

Keep secrets, payment tokens, credentials, and personal data out of logs and test fixtures.

### Debugging sequence

```text
wrong business result?
    │
    ├─ unit policy test fails ─────────> inspect decision and controlled inputs
    ├─ contract test fails ─────────────> compare fake/adapter semantics
    ├─ integration test fails ──────────> inspect wiring, config, serialization
    └─ production only ─────────────────> inspect boundary telemetry and environment
```

### How to read this visual

Start with the observed failure and choose the narrowest evidence layer that also fails. Each lane
points to a different likely cause; do not add more mocks to an integration wiring defect.

### Key insight

Different tests localize different claims. A green unit test and failing integration test are not
contradictory; they indicate the policy works under the double but the real graph or semantics do
not match.

### Simplification or limitation

The decision tree omits flaky infrastructure, races, observability gaps, data-dependent provider
behavior, and failures shared across layers.

## 22. Concurrency, state, and lifetime

This unit introduces lifetime only where it affects dependency management. `SDP-FND-090` owns the
deeper treatment of shared state, ownership, mutation, and object lifetime.

Important seam questions:

- Is a fake fresh per test or shared?
- Is the production client safe to share across threads or tasks?
- Does a repository represent one transaction, one request, or the whole process?
- Can a clock advance during a test?
- Does a sequence stub remain safe under concurrent calls?
- Does a mock record concurrent interactions deterministically?

### A false sense of safety

```python
repository = InMemoryRepository()
```

This fake may make a check-then-save operation look atomic because one test runs one thread. A real
database under concurrency may require a unique constraint, transaction, optimistic lock, or
provider idempotency key. Unit seams make a race reproducible only if the test models the competing
operations; they do not create atomicity.

## 23. Performance and memory

No benchmark is required for this unit.

General trade-offs:

- small unit tests with in-process doubles usually execute quickly and localize failures;
- integration tests incur process, I/O, setup, and cleanup costs but prove necessary semantics;
- session-scoped resources can reduce setup cost while increasing state-leak risk;
- large auto-generated mock graphs add setup and cognitive cost even if runtime is fast;
- a faithful fake can become an expensive second implementation to maintain.

Do not optimize test duration by removing the only evidence for wiring or provider semantics. Split
suites, parallelize safely, or narrow integration scope after measuring the real bottleneck.

## 24. Testing strategy

| Test type | What it proves | Useful collaborators | What it must not claim |
|---|---|---|---|
| Pure unit | deterministic policy for values | real values and pure functions | database/network semantics |
| Collaborator unit | policy under controlled outcomes and failures | stubs, small fakes, selective spies/mocks | production wiring |
| Contract | implementations share selected boundary behavior | fake plus real adapter | total behavioral equivalence |
| Adapter unit | translation of provider-shaped samples | fixtures and narrow stubs | live provider availability |
| Integration | real components configure and communicate | real selected adapters | every policy combination |
| End-to-end | critical user path across deployed boundaries | mostly real system | precise fault localization |

### Behavior-first test shape

```text
Given meaningful state and controlled indirect inputs
When one public behavior runs
Then assert its result and required effects
And assert only semantically important non-effects
```

### What not to overspecify

- number of private helper calls;
- incidental ordering;
- exact SQL or SDK chain in a policy test;
- concrete class identity behind a boundary;
- log message punctuation unless logs are a public protocol;
- every collaborator call when the final state already proves behavior.

## 25. Refactoring path from hidden dependencies

1. **Preserve behavior.** Add characterization tests using the safest available seam, including
   tactical patching if necessary.
2. **List hidden dependencies.** Include values, time, environment, globals, construction, and
   lifetime—not only obvious service objects.
3. **Separate stable policy from volatile detail.** Name what the policy actually needs.
4. **Introduce one smallest seam.** Extract a parameter, callable, object field, or adapter at a
   time.
5. **Move construction outward.** Create or extend one visible composition root.
6. **Replace patch-heavy tests.** Construct the policy directly with simple real objects or
   role-specific doubles.
7. **Assert behavior.** Remove private choreography assertions that no longer protect a
   requirement.
8. **Add contract evidence.** Run shared cases against fakes and real adapters.
9. **Add one integration path.** Prove the production graph, configuration, and translation.
10. **Add the new requirement.** Confirm the seam handles actual change pressure.
11. **Remove speculative abstraction.** Keep only boundaries that carry meaning or volatility.

### Refactoring visual

```text
BEFORE                               TRANSITION                         AFTER

policy                               policy                            root
 ├─ constructs DB                    ├─ receives DB <── patched/name    ├─ real DB
 ├─ reads clock          ──────>     ├─ receives clock                 ├─ system clock
 └─ sends audit                      └─ sends audit <── explicit        └─ audit adapter
    hidden choices                       one seam at a time                 │
                                                                             ▼
                                                               policy receives capabilities
```

### How to read this visual

Move from left to right. The transition does not require a big-bang rewrite: a legacy patch can
protect behavior while each selection moves outward. The final root owns choices; the policy owns
use.

### Key insight

The goal is not a higher mock count. A successful refactor usually deletes patch targets and makes
tests construct the policy more directly.

### Simplification or limitation

The sketch omits circular imports, framework startup, resource cleanup, transaction ownership, and
multi-process deployment.

## 26. Common misuse and overengineering

| Misuse | Why it happens | Better move |
|---|---|---|
| Mock every collaborator | “Unit” is mistaken for “one class in total isolation” | Use real cheap deterministic objects; double only awkward boundaries |
| One interface per class | Multiple implementations are assumed to require nominal abstraction | Start from the client's smallest operation; use duck typing, callable, or `Protocol` when needed |
| Patch a definition module | Object identity is confused with lookup binding | Patch the name evaluated by the SUT; reproduce with EXP-01 |
| Deep return-value chains | A provider SDK leaks through the policy | Add a client-owned adapter that returns application data |
| Assert all calls and order | Call recording makes every detail tempting to verify | Assert outputs/state; retain only contract-significant interactions |
| Global service locator | Passing parameters feels repetitive | Use a composition root or cohesive service; keep dependencies visible |
| Production `if testing:` branch | Tests need a shortcut | Supply a different collaborator from test assembly |
| Fake as proof of database behavior | In-memory speed is confused with semantic fidelity | Shared contract tests plus real integration |
| Autospec as full safety | Signature strictness feels like realism | Add semantic contract and wiring evidence |
| Session-scoped mutable fake | Setup cost is reduced prematurely | Fresh function scope or explicit isolation/reset |
| Mock a pure function | Isolation becomes a reflex | Call the real pure function and verify its behavior |
| Sleep in a retry test | Real time seems easiest | Inject clock/sleeper or drive an explicit retry policy |
| Dependency framework for a small module | “DI” is equated with containers | Plain constructors, parameters, and application factory |
| Expose private state for tests | Observability is added only to satisfy assertions | Test public results/effects or add a real diagnostic boundary |

## 27. Dependency injection, service location, IoC, and DIP

| Concept | Core question | Python example | Main confusion |
|---|---|---|---|
| Dependency injection | How is a collaborator supplied? | constructor/function parameter | assumed to require a container |
| Service locator | Where does code ask for a collaborator? | global registry lookup | hidden dependencies mistaken for convenience |
| Inversion of control | Who controls the overall call or assembly flow? | framework calls handler; root supplies dependency | used as a synonym for every callback |
| Dependency Inversion Principle | Which source-code direction protects policy? | policy-owned `Protocol`, adapter depends inward | confused with passing any object as an argument |
| Fixture injection | How does pytest supply test arrange-state? | test parameter requests fixture | confused with production DI |
| Monkeypatching | Which binding/state is temporarily replaced? | `monkeypatch.setattr` | treated as a general architecture |

Fowler notes that dependency injection makes dependencies visible in constructors or setters,
whereas a locator requires searching for lookup calls. Both can technically be substituted in
tests; visibility and component reuse are separate design concerns
([Fowler, service locator versus injection](https://martinfowler.com/articles/injection.html#ServiceLocatorVsDependencyInjection)).

This unit teaches explicit seams and testing judgment. `SDP-SOL-050` later owns full dependency
inversion, and `SDP-RAR-050` owns Service Locator's limited uses and hidden-dependency costs.

## 28. Decision framework

```text
Need a test seam?
    │
    ├─ real collaborator is cheap, deterministic, safe, and clear? ── yes ─> use it
    │
    └─ no
        │
        ├─ control a plain value? ───────────────────────────────> pass value
        ├─ one stateless operation? ─────────────────────────────> pass callable
        ├─ state or several cohesive operations? ────────────────> small object/Protocol
        ├─ third-party shape or failures differ? ────────────────> adapter boundary
        ├─ legacy/global/platform lookup blocks first test? ─────> patch tactically
        └─ real semantics/wiring are the claim? ─────────────────> integration/contract test

After choosing a seam, need a double?
    │
    ├─ only fills unused input ─────────> dummy
    ├─ supplies answer/failure ─────────> stub
    ├─ supplies working state ──────────> fake + contract tests
    ├─ records selected calls ──────────> spy
    └─ interaction is specification ────> mock, preferably strict
```

### How to read this visual

Read the first tree before the second. The first chooses the boundary and evidence level; only then
does the second choose a double role. This prevents the mocking tool from designing the production
API accidentally.

### Key insight

“Which mock should I use?” is usually the second question. First ask whether the real collaborator
is usable and which seam honestly represents the production boundary.

### Simplification or limitation

Several answers may apply in one test. A fake can also spy, a stub can raise, and an integration
test can still use a stub for an out-of-scope external provider.

## 29. When to use explicit seams and doubles

- volatile I/O or provider boundaries;
- time, randomness, identifiers, scheduling, and retries;
- side effects that must not occur in unit tests;
- costly setup or unavailable infrastructure;
- precise normal and failure outcomes needed on demand;
- lifetime and state ownership that must be visible;
- legacy code needing characterization before refactoring;
- client-shaped contracts shared by multiple adapters;
- semantically important interaction or non-interaction requirements.

## 30. When not to add them

- pure deterministic calculation;
- stable value transformation;
- a cheap real collaborator clearer than a double;
- an interface whose only justification is “tests need to mock it”;
- provider behavior that only a real contract/integration test can establish;
- private helper calls that are not part of observable behavior;
- speculative future implementations;
- tiny scripts where direct construction is obvious, safe, and not under change pressure.

## 31. Realistic backend use case

Consider an API endpoint renewing a subscription.

### Boundary layers

```text
HTTP/framework boundary
    │ parses/authenticates/maps
    ▼
RenewSubscription application policy
    │ explicit ports/callables
    ├─ receipt repository
    ├─ billing adapter
    ├─ clock
    └─ audit publisher
         ▲
application factory / startup chooses concrete objects and lifetimes
```

Unit tests can cover:

- approval and decline decisions;
- validation before effects;
- idempotent replay;
- translated timeout policy;
- required audit content.

Contract tests can cover:

- fake and database repository semantics;
- billing response translation from recorded synthetic samples;
- audit serialization shape.

Integration tests can cover:

- environment/configuration wiring;
- database constraints and transactions;
- HTTP client timeout/authentication setup;
- broker or outbox integration;
- framework request/response mapping.

Do not place provider credentials or private production payloads in fixtures. Use synthetic values.

## 32. Interview preparation

### Common formulation 1

**“What is dependency injection, and how would you do it in Python?”**

A strong answer:

1. Defines injection as supplying a dependency from outside its user.
2. Starts with function parameters, constructors, callables, and application factories.
3. Explains configuration versus use and visible lifetimes.
4. Says a container is optional.
5. Distinguishes injection from DIP and service location.
6. Names over-injection and oversized constructors as design feedback.

### Common formulation 2

**“Explain mock, stub, fake, spy, and dummy.”**

A strong answer classifies roles:

- dummy fills an unused slot;
- stub supplies controlled indirect input;
- fake implements a working shortcut;
- spy records calls for later verification;
- mock centers expected interaction verification.

Then add: one `Mock` instance may serve stub and spy roles; the library class does not determine the
test-design role.

### Common formulation 3

**“Why did my Python patch not work?”**

Trace the name lookup. `from a import X` binds `X` in the importing module; patch that module's `X`
if the SUT reads it there. `import a; a.X` reads through `a`, so patch `a.X`. Mention cleanup and
prefer explicit seams for ordinary application collaborators.

### Common formulation 4

**“Should unit tests mock all external dependencies?”**

No. Use the real collaborator if it is cheap, deterministic, safe, and clear. Double boundaries
that are slow, nondeterministic, destructive, unavailable, or need controlled outcomes. Use
contract and integration tests for semantics and wiring. Avoid mocking the code whose behavior is
the claim.

### Common formulation 5

**“When is interaction verification appropriate?”**

When the interaction or its absence is itself a requirement: no duplicate charge, required audit,
no send after validation failure, correct commit/rollback decision. Avoid private choreography and
incidental order.

### Weak-answer traps

- “A fake returns fake data; a mock returns mocked data.”
- “Always mock databases in unit tests.”
- “Dependency injection is a framework that creates classes.”
- “Patch the class where it was defined.”
- “Autospec guarantees the mock behaves like production.”
- “If unit tests pass, wiring is correct.”
- “More interfaces always improve testability.”

### Likely follow-ups

1. How do you test an async collaborator?
2. How do contract tests keep a fake honest?
3. When would you prefer a callable to a `Protocol`?
4. How do you introduce seams safely in legacy code?
5. What does a session-scoped fixture risk?
6. How do you test retries without sleeping?
7. What should remain an integration test?
8. How can mock-heavy tests signal a design problem?

### Reasoning checkpoints

A strong senior answer identifies the change pressure, the assembly owner, the smallest seam, the
double role, the verification style, the contract gap, the real integration evidence, and the
simpler design that avoids unnecessary indirection.

## 33. Closed-book revision cues

1. Reconstruct the assembly → seam → policy → evidence visual.
2. Define dependency, injection, composition root, seam, double, and fixture.
3. Explain dummy, stub, fake, spy, and mock using one backend scenario.
4. Give one output assertion, one state assertion, and one justified interaction assertion.
5. Explain patch lookup for both `from a import X` and `import a`.
6. State what `spec`, `spec_set`, and autospec add—and do not add.
7. Explain why a fake needs contract tests.
8. Refactor one hidden clock or gateway to a callable or explicit collaborator.
9. Reject a DI container and a nominal interface in a scenario where plain arguments suffice.
10. Name the integration test that an isolated unit test cannot replace.

## 34. Practice and experiments

The [practice lab](practice/README.md) contains:

- an unsolved subscription-renewal refactoring;
- characterization tests for stable behavior and a hidden-lifetime defect;
- required edge cases and test-quality constraints;
- a patch lookup experiment;
- a `Mock` strictness experiment;
- a fake-versus-adapter contract experiment;
- exact reproduction commands and observed outputs.

The lab remains unsolved. Artifact verification does not advance `PROGRESS.md` learning state.

## 35. Source notes

Sources opened and used for this unit:

1. Martin Fowler, [“Inversion of Control Containers and the Dependency Injection pattern”](https://martinfowler.com/articles/injection.html) — configuration versus use, injection forms, and service-locator comparison.
2. Martin Fowler, [“Mocks Aren't Stubs”](https://martinfowler.com/articles/mocksArentStubs.html) — Meszaros test-double vocabulary and state versus behavior verification.
3. Python 3.14 documentation, [`unittest.mock`](https://docs.python.org/3.14/library/unittest.mock.html) — `Mock`, specs, autospec, `AsyncMock`, patch lookup, and precedence contracts.
4. pytest documentation, [fixtures](https://docs.pytest.org/en/stable/explanation/fixtures.html) and [monkeypatch](https://docs.pytest.org/en/stable/how-to/monkeypatch.html) — fixture assembly/lifetimes and temporary state replacement.

All explanations, diagrams, examples, exercises, and experiments here are original and use
synthetic data. No third-party source code or proprietary system is reproduced.
