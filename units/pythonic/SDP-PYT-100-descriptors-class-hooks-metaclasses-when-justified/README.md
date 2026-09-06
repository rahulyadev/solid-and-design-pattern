# SDP-PYT-100 — Descriptors, class hooks, and metaclasses only when justified

## Physical Notebook Core

### Problem or change pressure

Python lets an object intercept attribute access, a base class react to new subclasses, a decorator
transform a finished class, and a metaclass control class creation. These powers are useful when a
framework owns the corresponding boundary. In ordinary application code they can hide control flow,
couple inheritance, create import-time state, and surprise typing or tools.

### One-sentence mental model

> Choose the least powerful event boundary: explicit call first, attribute protocol for repeated
> attribute behavior, subclass hook for an owned hierarchy, class decorator for one explicit
> completed class, and metaclass only for class-creation power no smaller mechanism can supply.

### One essential visual

~~~text
change pressure
     |
     v
explicit function / dataclass / composition
     | one owner needs managed access
     v
property
     | repeated get-set-delete policy across fields or owners
     v
descriptor

one completed class needs an explicit transformation -> class decorator
every future subclass in an owned hierarchy needs a rule -> __init_subclass__
class-body namespace or class-family creation must change -> metaclass

no concrete force ---------------------------------------> use none of them
~~~

### How to read this visual

Start at the top-left and stop as soon as a mechanism satisfies the observed change. The two
sideways branches intercept class-definition events rather than attribute access. A metaclass is
not the “final upgrade”; it is a different boundary with a much larger ownership cost.

### Key insight

Name the event that must be intercepted before naming the mechanism.

### Simplification or limitation

This is a conceptual decision ladder, not literal interpreter control flow or a claim that every
design passes through each rung. It omits custom importers, dynamic bases, framework-specific
typing plugins, and implementation optimizations.

### Governing rules or invariants

1. For ordinary instance lookup: data descriptor, instance dictionary, non-data descriptor, class
   value, then `__getattr__` fallback.
2. A cooperative `__init_subclass__` consumes only its keywords and forwards the rest with
   `super()`.
3. A class decorator receives an already-created class; a replacing decorator may change identity.
4. A `type`-derived metaclass should delegate and pass the complete namespace to `type.__new__`.
5. Definition-time registration, validation, and mutation happen during import when the class
   statement is imported.

### Minimal Python example

~~~python
from __future__ import annotations

from typing import Generic, TypeVar, overload

T = TypeVar("T")


class Managed(Generic[T]):
    def __init__(self) -> None:
        self.storage_name = ""

    def __set_name__(self, owner: type[object], name: str) -> None:
        self.storage_name = f"_managed_{name}"

    @overload
    def __get__(self, instance: None, owner: type[object] | None = None) -> Managed[T]: ...

    @overload
    def __get__(self, instance: object, owner: type[object] | None = None) -> T: ...

    def __get__(self, instance: object | None, owner: type[object] | None = None) -> Managed[T] | T:
        if instance is None:
            return self
        return getattr(instance, self.storage_name)

    def __set__(self, instance: object, value: T) -> None:
        setattr(instance, self.storage_name, value)
~~~

This is a data descriptor because its type defines `__set__`. It is justified only after a property
or explicit assignment helper would be duplicated across real owners.

### One common misconception

**Mistake:** A metaclass is a cleaner way to run code whenever a class is declared.

**Correction:** Post-creation work usually belongs in `__init_subclass__` or a class decorator.
Use a metaclass only when the requirement reaches namespace preparation, coordinated class-object
creation, metaclass-level operations, or construction policy for every instance of its classes.

### Important trade-offs

- Hooks centralize a cross-cutting rule, but move work away from an explicit call site.
- Earlier interception is more powerful and more expensive to compose, type, test, and debug.
- Definition-time failure catches invalid declarations early, but can stop a whole module import.

### Interview-revision cues

- Descriptor question: state data versus non-data precedence before presenting code.
- Class-hook question: separate `__set_name__`, `__init_subclass__`, decorators, metaclass creation,
  and metaclass `__call__` by phase.
- Design question: identify the simpler rejected option and the exact force that earns more power.

## Unit metadata

| Field | Value |
|---|---|
| Domain | Pythonic language and library mechanisms |
| Curriculum | [SDP-PYT-100](../../../CURRICULUM.md#sdp-pyt-100) |
| Progress | [PROGRESS.md](../../../PROGRESS.md) |
| Python references | [PYTHON_REFERENCES.md](../../../PYTHON_REFERENCES.md) |
| Learning outcome | Evaluate descriptors, `__init_subclass__`, class decorators, and metaclasses as advanced pattern mechanisms while preferring simpler Python designs. |
| Hard prerequisites | `SDP-FND-040`, `SDP-FND-060`, `SDP-PYT-070` |
| Python Mastery bridge | `PY-OBJ-050`, `PY-OBJ-060`, `PY-OBJ-070`, `PY-OBJ-080` |
| Priority | Advanced |
| Interview frequency | Low |
| Production frequency | Medium |
| Python/backend relevance | Medium |
| Depth | D4 |
| Scope | Python, Runtime |
| Size | XL |
| Learning estimate | 6–9 hours |
| Mastery estimate | 8–14 hours |
| Evidence profile | `E+I+D+X+T` |
| Canonical Python | Python 3.14 |
| Interview compatibility | Python 3.11 |
| Artifact state | Draft |

The frequency labels are curriculum judgments, not measured usage statistics.

## 1. Simple explanation and prerequisite bridge

Most Python programs should make behavior visible:

~~~python
def normalized_port(raw: int) -> int:
    if isinstance(raw, bool) or not 1 <= raw <= 65_535:
        raise ValueError("invalid port")
    return raw
~~~

The caller can see when validation happens. A dataclass can hold the result. A property can manage
one attribute. A dictionary can register a small known set. A factory can construct an object.
These are easy to trace and test.

Advanced class machinery moves work into events Python already performs:

- dotted attribute lookup can call a descriptor;
- `type.__new__` can call `__set_name__`;
- defining a subclass can call an inherited `__init_subclass__`;
- a class statement can pass the created class through decorators;
- a metaclass can prepare the namespace and create the class object; and
- calling that class can run `__call__` on its metaclass.

That implicit collaboration is valuable when the event itself is the stable extension point. It is
harmful when used only to remove three explicit lines.

### Required bridge: lookup before recipes

Do not memorize descriptors from examples. First know:

- an instance normally has a namespace such as `__dict__`;
- a class has a namespace and a method resolution order (MRO);
- dotted access is behavior implemented by `__getattribute__`, not a raw dictionary read;
- special methods are normally looked up on a type; and
- `super()` continues lookup from a specific place in an MRO.

The official descriptor guide warns that most people do not need its deepest technical level; this
unit uses that depth to make rejection decisions, not to require metaprogramming everywhere.
[Python 3.14 Descriptor Guide](https://docs.python.org/3.14/howto/descriptor.html#technical-tutorial)

## 2. Real problem and forces

Consider a service configuration. At first it needs one validated port. A property is local and
clear:

~~~python
class Endpoint:
    def __init__(self, port: int) -> None:
        self.port = port

    @property
    def port(self) -> int:
        return self._port

    @port.setter
    def port(self, value: int) -> None:
        if isinstance(value, bool) or not 1 <= value <= 65_535:
            raise ValueError("invalid port")
        self._port = value
~~~

Now imagine multiple independently maintained model classes each require the same conversion,
validation, class-level introspection, assignment, and deletion behavior. Copying properties creates
drift. The repeated unit is no longer a class; it is an attribute policy. A descriptor may now be
earned.

A different requirement says every handler subclass in an existing hierarchy must declare a
validated code. That is not attribute access. `__init_subclass__` matches the subclass-creation
event.

A one-off completed class needs a marker. A class decorator makes the opt-in visible.

A framework must supply a special mapping before a class body executes and reject duplicate
declarations at assignment time. Post-creation hooks are too late. This can justify
`metaclass.__prepare__`—if the framework accepts the composition and tooling responsibility.

### Stable concerns

- client-facing values and operations;
- deterministic error semantics;
- explicit application assembly where possible;
- Python 3.11-compatible behavior; and
- debuggable, testable boundaries.

### Changing concerns

- number of fields sharing managed access;
- number of participating subclasses;
- definition-time metadata rules;
- whether transformation applies to one class or all descendants; and
- whether a framework truly owns class creation.

## 3. Decision ladder: least power first

Use this in a code review:

1. **Plain value or function.** Can an explicit call perform the work?
2. **Dataclass or ordinary class.** Is the need only data representation and construction
   invariants?
3. **Property.** Does one owner need managed access to one attribute?
4. **Ordinary function decorator.** Does one callable need wrapping?
5. **Explicit composition, map, or factory.** Can startup list dependencies and implementations?
6. **Descriptor.** Is get/set/delete behavior repeated as an attribute-level protocol?
7. **Class decorator.** Must one completed class be transformed through visible, local opt-in?
8. **`__init_subclass__`.** Must every future subclass in an already-justified hierarchy obey a
   cooperative post-creation rule?
9. **Metaclass.** Must code run before the class body, govern class-object creation, implement
   class-level special behavior, or wrap instance creation across a class family?
10. **None.** Is the proposed benefit only “less boilerplate” or “framework-like elegance” without
    measured change pressure?

The interactive [mechanism decision explorer](visuals/mechanism-decision-explorer.html) applies
this ladder to eight concrete scenarios.

## 4. Evidence labels used here

| Label | Meaning | Example |
|---|---|---|
| Python language guarantee | Defined by the language/data-model documentation | descriptor precedence and class-decorator application |
| Standard-library contract | Behavior of a documented library object | `dataclasses.dataclass` or `inspect.get_annotations` |
| CPython implementation detail | Documented as implementation-specific | namespace `__classcell__` propagation |
| Design mechanics | Collaboration chosen by this code | private descriptor storage naming |
| Framework behavior | A framework's own convention | automatic model registration |
| Professional inference | Production judgment, not interpreter law | prefer explicit startup over import-time registration |

Do not turn the lookup pseudocode in the Descriptor Guide into a claim that every Python
implementation uses those exact internal functions.

## 5. Descriptor protocol mechanics

### 5.1 What makes an object a descriptor

An object participates when its type provides one or more of:

~~~python
descriptor.__get__(instance, owner=None)
descriptor.__set__(instance, value)
descriptor.__delete__(instance)
~~~

`__get__` controls retrieval. `__set__` controls assignment. `__delete__` controls deletion.
`__set_name__` is a separate class-creation notification; an object can define it even if it is not
a descriptor. The protocol and data/non-data distinction are language-facing behavior documented
by Python.
[Descriptor protocol](https://docs.python.org/3.14/howto/descriptor.html#descriptor-protocol)

A descriptor must be found as a class attribute to participate in normal instance lookup. Putting a
descriptor object into an instance dictionary does not make it intercept its own access.
[Descriptor Guide primer](https://docs.python.org/3.14/howto/descriptor.html#closing-thoughts)

### 5.2 Data versus non-data descriptors

A descriptor whose type defines `__set__` or `__delete__` is a **data descriptor**. A descriptor
with only `__get__` is a **non-data descriptor**.

For ordinary `instance.name` lookup, the practical precedence is:

~~~text
1. data descriptor found in type(instance)'s MRO
2. instance dictionary entry
3. non-data descriptor found in the class MRO
4. ordinary class attribute found in the class MRO
5. __getattr__ fallback after __getattribute__ raises AttributeError
~~~

This is why a property remains authoritative even without a setter: the property type still
provides `__set__` and raises `AttributeError` when no setter exists. It is also why cached
computed values commonly use a non-data descriptor: the computed result can be written into the
instance dictionary and win next time.
[Invocation from an instance](https://docs.python.org/3.14/howto/descriptor.html#invocation-from-an-instance)

The unit's [lookup experiment](experiments/EXP-01-descriptor-lookup-precedence/README.md) proves both
branches with a same-named instance entry.

### 5.3 Owner versus instance access

For a descriptor `field` stored on class `Model`:

~~~text
model.field  -> field.__get__(model, Model)
Model.field  -> field.__get__(None, Model)
~~~

A well-behaved managed-field descriptor often returns itself for class access:

~~~python
def __get__(self, instance: object | None, owner: type[object] | None = None) -> object:
    if instance is None:
        return self
    return getattr(instance, self.storage_name)
~~~

This permits introspection without reaching directly into `vars(Model)`. It is a design choice, not
a universal return-value rule. A classmethod descriptor, for example, binds the class.
[Invocation from a class](https://docs.python.org/3.14/howto/descriptor.html#invocation-from-a-class)

`vars(Model)["field"]` bypasses dotted lookup and returns the stored descriptor object directly.
That distinction is useful in tests and debugging.

### 5.4 Why methods bind

A user-defined function stored in a class is a non-data descriptor. On instance access its
`__get__` behavior produces a bound method carrying:

~~~text
bound_method.__self__ -> the instance
bound_method.__func__ -> the original class-body function
~~~

Calling the bound method inserts `__self__` before the explicit arguments. This is the mechanism
behind ordinary `self` binding; it is not compiler rewriting at each call site.
[Functions and methods as descriptors](https://docs.python.org/3.14/howto/descriptor.html#functions-and-methods)

Because a function is non-data, an instance dictionary entry can shadow it. That flexibility is
also a reason not to describe every class attribute as though instance lookup always behaved the
same way.

### 5.5 `__set_name__` timing

When `type.__new__` creates a class, it scans class namespace values with `__set_name__` and calls
each with the new owner and assigned name. Assignment after class creation does not trigger the
notification automatically; code must call it explicitly if needed.
[`object.__set_name__`](https://docs.python.org/3.14/reference/datamodel.html#object.__set_name__)

~~~python
class Field:
    def __set_name__(self, owner: type[object], name: str) -> None:
        self.storage_name = f"_managed_{name}"


class Record:
    value = Field()  # automatic notification


late = Field()
Record.late = late
late.__set_name__(Record, "late")  # explicit because attachment was late
~~~

Avoid silently reusing one stateful descriptor instance under two different public names. Either
reject it, store owner/name mappings deliberately, or create separate descriptor objects.

### 5.6 Where state belongs

The descriptor object normally lives once on the class and is shared. Per-instance values must not
be stored as one `self.value` on that shared descriptor. Store them in the owner instance, a slot,
or another deliberately keyed structure.

~~~text
ServiceEndpoint.__dict__["port"] -> one ManagedField object

endpoint_a.__dict__["_managed_port"] -> 8080
endpoint_b.__dict__["_managed_port"] -> 9090
~~~

External keyed storage introduces object-lifetime, weak-reference, hashability, and concurrency
questions. Prefer ordinary instance storage unless the requirement rules it out.

### 5.7 Assignment and deletion

`instance.name = value` can call a data descriptor's `__set__`. `del instance.name` can call
`__delete__`. A read-only data descriptor should raise `AttributeError` in `__set__` rather than
silently accept an instance shadow.

Keep validation deterministic. A property or descriptor getter should not unexpectedly:

- query a database;
- call a network service;
- perform async work;
- mutate global registration;
- log secrets or complete values; or
- hide a retry policy.

Those behaviors deserve explicit service methods.

### 5.8 Custom `__getattribute__` can change the model

Descriptor invocation is implemented through attribute-access machinery such as
`object.__getattribute__`, `type.__getattribute__`, and `super` lookup. An override that does not
delegate can bypass normal descriptor behavior. This is a language-mechanics warning, not advice to
write a custom dispatcher.
[Descriptor invocation summary](https://docs.python.org/3.14/howto/descriptor.html#summary-of-invocation-logic)

Test a descriptor through dotted access. Calling `descriptor.__get__` directly tests the descriptor
method but not its place in lookup precedence.

## 6. Simplest alternatives before a descriptor

| Need | Smallest usual choice | Why |
|---|---|---|
| Transform one incoming value | function | explicit call and error boundary |
| Validate immutable construction | frozen dataclass plus factory or `__post_init__` | no later assignment policy |
| Manage one attribute on one class | property | policy stays beside its owner |
| Reuse only a validation predicate | shared function | no lookup interception |
| Attach a computed operation | method | explicit behavior and dependencies |
| Cache an expensive pure computation | documented cache/property tool | established cache semantics |
| Share get/set/delete behavior across owners | descriptor, if repetition is real | attribute protocol is the repeated unit |

Do not use a descriptor merely to avoid writing `self._name = name`.

## 7. Worked descriptor: justified, typed, and bounded

[`managed_fields.py`](examples/managed_fields.py) supplies one generic data descriptor used by two
synthetic configuration owners.

~~~python
class ServiceEndpoint:
    name = ManagedField(trimmed_text)
    port = ManagedField(port_number)

    def __init__(self, name: str, port: int) -> None:
        self.name = name
        self.port = port
~~~

Each abstraction has evidence:

- `ManagedField` owns repeated conversion, validation, naming, get/set/delete, and error chaining;
- `trimmed_text` and `port_number` remain ordinary explicit functions;
- each instance owns its values under a private name such as `_managed_port`;
- class access returns the descriptor for introspection;
- no registry, metaclass, database call, async hook, or framework is added.

The implementation uses `TypeVar`/`Generic` syntax compatible with Python 3.11 instead of Python
3.12's type-parameter syntax. Strict typing verifies that consumers see `endpoint.name` as `str`
and `endpoint.port` as `int`.

### Error boundary

Conversion `TypeError`/`ValueError` is wrapped in `FieldValidationError` with the public field name,
while the original error remains chained. Values are not included in the public message. Deleting
or reading an unassigned field raises `AttributeError`, preserving normal missing-attribute
semantics.

### Deliberate limitations

- owner instances need writable storage;
- one descriptor object cannot be rebound under another public name;
- conversion is synchronous and side-effect bounded;
- no attempt is made to synthesize constructor signatures; and
- runtime validation does not replace static typing or domain validation at a request boundary.

## 8. `__init_subclass__` mechanics

### 8.1 The event

Whenever a class inherits from a base, Python calls the relevant inherited `__init_subclass__` with
the new subclass as `cls`. Defined in an ordinary form, the hook is implicitly treated as a class
method. It runs during class creation, before the class statement finishes binding its final name.
[`object.__init_subclass__`](https://docs.python.org/3.14/reference/datamodel.html#object.__init_subclass__)

Use it when an existing base class owns a rule for every future subclass:

~~~python
class Handler:
    code: str

    def __init_subclass__(cls, /, *, code: str, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        if code != code.strip().lower() or not code:
            raise TypeError("code must be lowercase and trimmed")
        cls.code = code


class InvoiceHandler(Handler, code="invoice"):
    pass
~~~

### 8.2 Cooperative multiple inheritance

Class-definition keywords are shared across the cooperative hook chain. Each hook should:

1. accept the new subclass positionally;
2. name its own keyword, preferably keyword-only;
3. accept remaining keywords;
4. consume only what it owns;
5. delegate the rest through `super().__init_subclass__(**kwargs)`; and
6. avoid assuming it is the only base with a hook.

The terminal `object.__init_subclass__` accepts no arguments, so an unconsumed keyword produces an
error rather than silently disappearing. The official data model explicitly recommends forwarding
for compatibility.
[Keyword forwarding example](https://docs.python.org/3.14/reference/datamodel.html#object.__init_subclass__)

In [`class_hooks.py`](examples/class_hooks.py), `CodedRule` calls `super()` before recording. The
sibling `VersionedDefinition` therefore records first. The observed order follows MRO and each
method body's placement of `super()`, not a simplistic “left base always completes first” rule.

### 8.3 Ordering with descriptors and decorators

For a usual `type`-derived metaclass that delegates to `type.__new__`:

~~~text
type.__new__ creates class object
  -> call __set_name__ on values in the new class namespace
  -> call __init_subclass__ on the immediate parent in the new class MRO
metaclass __init__ completes its part of class creation
apply class decorators
bind the decorator result to the class name
~~~

The data-model documentation states the `__set_name__` then `__init_subclass__` callbacks inside
the `type.__new__` path and applies decorators after the class object is created.
[Creating the class object](https://docs.python.org/3.14/reference/datamodel.html#creating-the-class-object)

Do not use this compact ordering as a license to make hooks depend on unrelated side effects.

### 8.4 Validation versus registration

Definition-time validation can be appropriate because an invalid class should not exist.
Definition-time registration is more dangerous:

~~~python
HANDLERS: dict[str, type[object]] = {}


class AutoRegistered:
    def __init_subclass__(cls, /, *, code: str, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        HANDLERS[code] = cls
~~~

This map changes only when the defining modules execute. Results can depend on imports, reloads,
test order, optional modules, and worker processes. The hook also couples “is a subclass” to “is
globally active.” Prefer an explicit startup list or registry unless definition-time registration
is the demonstrated requirement. See
[SDP-PYT-090](../SDP-PYT-090-dynamic-registration-plugin-discovery-mechanics/README.md) for the full
registration/discovery boundary.

### 8.5 Failure boundary

A hook exception occurs while the class statement executes. During module import, that can prevent
the module from completing and remove access to later definitions. Failures should name the class
and violated declaration without exposing secrets. Frameworks should distinguish:

- class-definition validation failure;
- duplicate registration;
- module import failure;
- application startup activation failure; and
- request-time handler failure.

## 9. Class decorators

### 9.1 What Python does

Class decorators are applied to the created class and the resulting object is bound to the class
name. For:

~~~python
@outer
@inner
class Report:
    pass
~~~

the transformation is approximately:

~~~python
class Report:
    pass


Report = outer(inner(Report))
~~~

Application is bottom-up; the top decorator sees the inner decorator's result.
[Class definitions and decorators](https://docs.python.org/3.14/reference/compound_stmts.html#class-definitions)

Unlike `__init_subclass__`, a class decorator applies to the specific definition carrying the
syntax. It is not automatically re-run for descendants.

### 9.2 In-place mutation

~~~python
from collections.abc import Callable
from typing import TypeVar

ClassT = TypeVar("ClassT", bound=type[object])


def labeled(label: str) -> Callable[[ClassT], ClassT]:
    def decorate(cls: ClassT) -> ClassT:
        cls.definition_label = label
        return cls

    return decorate
~~~

Returning the same class preserves `decorated is original`, the original MRO, and normal
`isinstance` relationships. Static typing can express the identity-preserving shape, although an
arbitrary injected attribute is not automatically known to every type checker.

Mutation can still surprise tools that captured the class before decoration or expect immutable
metadata. Make the new contract documented and testable.

### 9.3 Replacement or wrapping

A decorator may return a subclass, proxy, unrelated class, or even a non-class. Python binds that
result. Replacement can affect:

- `is` identity and caches keyed by the original class;
- MRO and inherited behavior;
- `isinstance`/`issubclass` relationships;
- `__module__`, `__qualname__`, docs, and signatures;
- pickling and import-by-qualified-name behavior;
- static typing and IDE inference;
- dependency-injection, ORM, serialization, and test-discovery tools; and
- which class an earlier `__init_subclass__` or `__set_name__` callback observed.

Copying metadata does not restore identity or eliminate the extra behavioral layer. If wrapping is
needed only for one operation, decorate that method or inject a collaborator instead.

### 9.4 Class decorator versus subclass hook

| Question | Class decorator | `__init_subclass__` |
|---|---|---|
| Opt-in location | on each decorated definition | inheritance from the governing base |
| Receives | a completed class or prior decorator result | every newly created subclass |
| Descendant behavior | not reapplied automatically | inherited cooperatively |
| Keyword protocol | decorator arguments | class-definition keywords |
| Composition risk | stacking and replacement order | MRO, `super()`, keyword forwarding |
| Best fit | explicit one-class transformation | family-wide post-creation invariant |

## 10. Class objects, instances, and the two-level model

Keep these three objects distinct:

~~~text
job = AuditedJob("nightly")

job -------------------- instance
AuditedJob ------------- class of job
DefinitionMeta --------- class of AuditedJob (its metaclass)

type(job) is AuditedJob
type(AuditedJob) is DefinitionMeta
issubclass(DefinitionMeta, type)
~~~

Python classes are callable and normally create instances; call arguments usually flow to
`__new__` and `__init__`.
[Classes are callable](https://docs.python.org/3.14/reference/datamodel.html#classes)

Special call syntax roughly consults `type(x).__call__`. Therefore calling `AuditedJob(...)` can
run `DefinitionMeta.__call__` because `DefinitionMeta` is the type of `AuditedJob`.
[Emulating callable objects](https://docs.python.org/3.14/reference/datamodel.html#object.__call__)

## 11. Metaclass class-creation roles

### 11.1 Default: `type`

Without special bases or an explicit metaclass, Python uses `type`. Most user-defined classes are
instances of `type`:

~~~python
class Ordinary:
    pass


assert type(Ordinary) is type
~~~

### 11.2 High-level class statement phases

The documented class-creation process includes:

1. resolve non-type base MRO entries when relevant;
2. determine the appropriate metaclass;
3. prepare the class namespace;
4. execute the class body in that namespace; and
5. create the class object.

[Customizing class creation](https://docs.python.org/3.14/reference/datamodel.html#customizing-class-creation)

Decorator application happens after class-object creation.

### 11.3 `__prepare__`: before the body

If the chosen metaclass defines `__prepare__`, Python calls it with the class name, bases, and
class keywords before executing the body. It returns the mapping used as the body's local
namespace.

~~~python
class DefinitionMeta(type):
    @classmethod
    def __prepare__(
        mcls,
        name: str,
        bases: tuple[type[object], ...],
        **kwargs: object,
    ) -> dict[str, object]:
        return {}
~~~

This hook is justified only for behavior that must affect class-body execution or capture
declarations through the namespace. Examples include a framework-owned namespace that rejects
duplicate public declarations immediately or supplies deliberate declaration helpers. Ordinary
`dict` already preserves insertion order; order alone is not automatically a metaclass
requirement.

The namespace passed into `type.__new__` is copied into a new ordered mapping and exposed through a
read-only proxy as the class `__dict__`. Do not rely on the original prepared mapping remaining the
class dictionary.
[Preparing the class namespace](https://docs.python.org/3.14/reference/datamodel.html#preparing-the-class-namespace)

PEP 3115 introduced `__prepare__` so a metaclass could participate before the class body rather than
only after a complete namespace existed.
[PEP 3115](https://peps.python.org/pep-3115/)

### 11.4 Metaclass `__new__`: create the class object

`Meta.__new__(mcls, name, bases, namespace, **keywords)` receives the populated namespace and should
return the class object. For a `type` subclass, the safe default is to validate or transform only
what is required and delegate:

~~~python
class DefinitionMeta(type):
    def __new__(
        mcls,
        name: str,
        bases: tuple[type[object], ...],
        namespace: dict[str, object],
        **kwargs: object,
    ) -> type[object]:
        return super().__new__(mcls, name, bases, namespace, **kwargs)
~~~

Do not filter dunder entries by a broad naming rule. Some entries have language or
implementation-level roles.

### 11.5 Metaclass `__init__`: initialize the created class

After `__new__` returns the class object, metaclass `__init__` can initialize that object. If only
post-creation validation or attribute attachment is needed, this phase is usually evidence that a
smaller hook can work:

- family-wide rule: `__init_subclass__`;
- one explicit class: class decorator; or
- external assembly: ordinary function.

### 11.6 Metaclass `__call__`: calling the finished class

Defining `__call__` on a metaclass can intercept later calls to its class objects:

~~~python
class ConstructionMeta(type):
    def __call__(cls, *args: object, **kwargs: object) -> object:
        return super().__call__(*args, **kwargs)
~~~

The usual delegated path calls the target class's `__new__` and, under the documented normal
conditions, its `__init__`. This power can enforce a framework-wide construction contract, but an
explicit factory or dependency provider is often easier to type and replace.
[`object.__new__` and `object.__init__`](https://docs.python.org/3.14/reference/datamodel.html#basic-customization)

The [class-creation experiment](experiments/EXP-02-class-creation-order/README.md) separates these
events with actual observations.

## 12. Metaclass selection and conflicts

Python chooses a metaclass from the explicit metaclass, if any, and the metaclasses of all bases.
For a normal type-based choice, the selected metaclass must be a subtype of every candidate. If no
candidate satisfies that condition, class creation raises `TypeError`.
[Determining the appropriate metaclass](https://docs.python.org/3.14/reference/datamodel.html#determining-the-appropriate-metaclass)

~~~python
class FirstMeta(type):
    pass


class SecondMeta(type):
    pass


class First(metaclass=FirstMeta):
    pass


class Second(metaclass=SecondMeta):
    pass


# class Conflict(First, Second):
#     pass  # TypeError: metaclass conflict
~~~

A combined metaclass can sometimes reconcile the candidates, but it transfers composition
responsibility to application code and may depend on both libraries' undocumented assumptions.
PEP 487 specifically added simpler hooks in part to reduce unnecessary metaclass conflicts.
[PEP 487 background](https://peps.python.org/pep-0487/#background)

Do not add a compatibility metaclass mechanically. First ask whether either library could expose a
smaller hook or explicit integration point.

### Non-type metaclass callables

The language permits an explicit metaclass that is not an instance of `type`; it is used directly
as the metaclass callable. That callable need not return an ordinary class. This is advanced
language flexibility, not a production recipe. Most application and typing expectations assume an
actual class, so this unit's implementation stays with `type`-derived metaclasses.

## 13. `__classcell__` and zero-argument `super()`

Methods referring to `__class__` or zero-argument `super()` need an implicit closure cell. The
Python 3.14 data-model documentation labels the namespace `__classcell__` handoff a **CPython
implementation detail**: when present, a custom metaclass must propagate it to `type.__new__`, or
class initialization can raise `RuntimeError`.
[Creating the class object: `__classcell__`](https://docs.python.org/3.14/reference/datamodel.html#creating-the-class-object)

The safest policy is simple:

~~~python
created = super().__new__(mcls, name, bases, namespace, **kwargs)
~~~

Pass the complete namespace unless there is a precise, tested transformation. Do not pop unfamiliar
dunder names. PEP 3135 explains the implicit `__class__` cell used by zero-argument `super()`.
[PEP 3135](https://peps.python.org/pep-3135/)

The unit contains a CPython-gated negative test that deliberately drops `__classcell__` and observes
the documented failure. The test is skipped on other Python implementations; the implementation
detail is not generalized into a language guarantee.

## 14. Python 3.11 and 3.14 compatibility overlay

### Stable mechanics used by this unit

The following are available in Python 3.11 and remain the core model in Python 3.14:

- descriptor `__get__`, `__set__`, `__delete__`;
- `__set_name__` and `__init_subclass__`, added in Python 3.6;
- class decorators;
- `type`-derived metaclasses and `__prepare__`; and
- documented data/non-data lookup precedence.

All runnable teaching code uses Python 3.11-compatible syntax.

### Annotation introspection changed materially in Python 3.14

Python 3.14 lazily evaluates annotations and adds `annotationlib`. Class decorators, subclass hooks,
and metaclasses that inspect annotations are therefore version-sensitive. The 3.14 data model marks
class annotations as lazily evaluated, while `annotationlib.get_annotations` is the current
best-practice API after an object exists.
[Python 3.14 class annotations](https://docs.python.org/3.14/reference/datamodel.html#type.__annotations__)
[`annotationlib.get_annotations`](https://docs.python.org/3.14/library/annotationlib.html#annotationlib.get_annotations)

During metaclass processing before the class is fully created, Python 3.14 provides
`annotationlib.get_annotate_from_class_namespace`. That function does not exist in Python 3.11.
[Pre-creation annotation helper](https://docs.python.org/3.14/library/annotationlib.html#annotationlib.get_annotate_from_class_namespace)

Production guidance:

1. Do not inspect annotations in a class hook unless they are part of the real runtime contract.
2. After class creation, use the version-appropriate documented introspection API rather than
   assuming `cls.__annotations__` has eager values.
3. If Python 3.11 compatibility is required, design an explicit adapter and test both runtimes.
4. Prefer declarative runtime values or explicit registration when annotation evaluation timing
   would become part of application startup.

This unit deliberately does not build an annotation-driven framework.

### Type parameter syntax

Python 3.12 added class type-parameter lists. The worked generic descriptor uses
`TypeVar`/`Generic` so it compiles on Python 3.11. This is a syntax compatibility decision, not a
difference in descriptor precedence.

## 15. Direct comparison of mechanisms

| Mechanism | Intercepts | Natural scope | Identity effect | Main composition cost | Prefer when |
|---|---|---|---|---|---|
| Function | explicit call | one operation | none | caller wiring | behavior can stay visible |
| Dataclass | instance construction and generated value behavior | one data type | ordinary class | inheritance/generated-method details | representing a value |
| Property | one named attribute on one class | one owner | none | local getter/setter coupling | one owner needs managed access |
| Ordinary decorator | one callable definition/call | one callable | wrapper may replace callable | metadata/signature/typing | callable behavior is the unit |
| Explicit dictionary/factory | startup assembly or explicit construction | application boundary | none | manual wiring | known implementations can be listed |
| Descriptor | dotted get/set/delete | attribute reused across owners | owner class unchanged | lookup precedence and shared descriptor state | attribute protocol is genuinely repeated |
| `__init_subclass__` | creation of future subclasses | inheritance family | subclass unchanged | MRO, `super()`, keywords | a base owns a family-wide post-creation rule |
| Class decorator | completed class definition | explicit class | preserve or replace | stacking, metadata, typing, tooling | one class opts into a post-creation transform |
| Metaclass | namespace/class creation and class-level special behavior | class family/framework | creates the class; `__call__` may govern instances | selection conflicts and ecosystem ownership | smaller hooks cannot reach the needed phase |

### Similar names, different mechanisms

- Python decorator syntax is application of a callable; it is not the GoF Decorator pattern.
- A descriptor is an attribute protocol object; it is not a general event listener.
- `__init_subclass__` initializes a newly defined subclass; it does not initialize instances.
- metaclass `__new__` creates a class object; class `__new__` creates an instance.
- metaclass `__call__` can wrap calling a class; class instance `__call__` makes an instance callable.

## 16. Participants and responsibilities

| Participant | Responsibility | What it must not own |
|---|---|---|
| Client code | make explicit calls and use public attributes/classes | hidden class-creation policy |
| Owner class | declare fields and ordinary behavior | descriptor's per-owner shared mutable value |
| Descriptor object | manage a repeated attribute protocol | network/database workflow or application registry |
| Base class hook | enforce a family-wide subclass invariant cooperatively | unrelated sibling keywords or global activation |
| Class decorator | transform one completed class and return the intended binding | silent identity changes |
| Metaclass | own the justified class-creation phase | ordinary business logic |
| Startup composition root | assemble registries, factories, and dependencies | implicit import-order guesses |
| Tests and diagnostics | prove phase, identity, lookup, and failures | overspecified private call counts |

## 17. Collaboration and execution flow

~~~mermaid
sequenceDiagram
    participant Body as class body
    participant Meta as chosen metaclass
    participant TypeNew as type.__new__
    participant Descriptor
    participant Parent as parent hook
    participant Decorator
    participant Name as class name
    Meta->>Meta: __prepare__(name, bases, keywords)
    Meta-->>Body: namespace
    Body->>Body: execute declarations
    Body->>Meta: create class from namespace
    Meta->>TypeNew: __new__(...)
    TypeNew->>Descriptor: __set_name__(new_class, field)
    TypeNew->>Parent: __init_subclass__(new_class, keywords)
    TypeNew-->>Meta: class object
    Meta->>Meta: __init__(class object)
    Meta-->>Decorator: completed class
    Decorator-->>Name: original or replacement object
~~~

### How to read this visual

Read downward once for a class statement. The metaclass prepares a namespace before the body. A
usual delegated `type.__new__` path performs descriptor naming and parent subclass hooks while
creating the class. Decorators then transform the completed class, and the final result receives the
source-level name.

### Key insight

Each extension point sees a different amount of information at a different time. Pick the latest
phase that still satisfies the requirement.

### Simplification or limitation

This is a conceptual sequence for a cooperative `type`-derived metaclass. It omits decorator
expression evaluation, dynamic MRO entries, non-type metaclass callables, exceptions, and the later
instance-construction path. It is not CPython source code.

## 18. Realistic backend use case

A configuration library supports `ServiceEndpoint` and `HealthCheck` objects. Several public fields
need the same assignment-time conversion, class-level schema introspection, deletion semantics, and
per-instance storage. The descriptor in [`managed_fields.py`](examples/managed_fields.py) is earned.

The application also owns an existing shipping-rule hierarchy. Every subclass must declare a
stable code and schema version. Two cooperative `__init_subclass__` implementations validate those
declarations.

At startup, the application still constructs an explicit tuple or mapping of active rules. It does
not equate subclass definition with activation. This separates:

~~~text
definition validity -> class hook
application activation -> explicit startup composition
request invocation -> ordinary method call
~~~

The diagnostic `DefinitionMeta` exists only to teach `__prepare__`/`__new__`/`__init__`/`__call__`
phases. The backend design rejects it because the accepted requirements are satisfied by the
descriptor, bounded subclass hook, and explicit composition.

## 19. Failure scenarios and containment

### Descriptor failure

**Failure:** conversion rejects an assignment.

**Detect:** a public `FieldValidationError` names the field and chains the cause.

**Contain:** the backing value is written only after conversion and validation succeed.

**Recover:** correct the input; do not retry hidden I/O because none exists.

### Subclass-hook failure

**Failure:** a class declares invalid metadata or a hook leaves a keyword unconsumed.

**Detect:** `TypeError` occurs at the class statement.

**Contain:** do not register before all validation succeeds.

**Recover:** fix the definition; a production module may need a restart because import failed.

### Class-decorator failure

**Failure:** a replacing decorator returns a proxy that a serializer cannot locate by qualified
name.

**Detect:** identity/MRO/metadata contract tests and a real serialization integration test.

**Contain:** prefer identity-preserving mutation or method-level wrapping.

**Recover:** remove replacement or provide an explicitly supported wrapper type.

### Metaclass failure

**Failure:** incompatible bases select no common metaclass, or a custom `__new__` corrupts the
namespace.

**Detect:** definition-time `TypeError`/`RuntimeError` with a phase-specific test.

**Contain:** keep metaclass ownership inside one framework and expose smaller extension points.

**Recover:** reconcile only with an understood combined contract; never catch and ignore class-
creation failure.

## 20. Testing strategy

| Test type | What it proves | What not to overspecify |
|---|---|---|
| Unit | conversion, validation, per-instance storage, deletion | exact private helper call count |
| Lookup contract | data/non-data precedence and class/instance access | CPython C function names |
| Hook collaboration | keyword consumption, forwarding, MRO-dependent order | unrelated import ordering |
| Identity contract | in-place versus replacement decorator behavior | object addresses or repr |
| Metaclass phase | prepare/new/init/call and conflict failures | undocumented interpreter internals |
| Compatibility | same public behavior on Python 3.11 and 3.14 | bytecode identity |
| Integration | framework/serializer/typing tool behavior if actually used | a fictional framework |
| Visual contract | embedded scenarios equal maintained Python data | browser or accessibility behavior it did not test |

### Essential descriptor tests

- independent values on two owner instances;
- class access and raw `vars(owner)` access;
- same-named instance entry versus data descriptor;
- same-named instance entry versus non-data descriptor;
- assignment conversion and failed-write atomicity;
- deletion before and after assignment;
- inherited descriptor behavior;
- late descriptor attachment; and
- custom `__getattribute__` only if production code overrides it.

### Essential hook tests

- valid and invalid class keywords;
- multiple cooperative bases;
- unconsumed keyword failure at `object.__init_subclass__`;
- duplicate metadata policy;
- hook side effects after a failed definition;
- reload/import isolation if a registry exists; and
- metaclass coexistence if the base may mix with framework types.

### Do not fake portability

The `__classcell__` negative test is explicitly CPython-gated. Public behavior is tested on both
required CPython versions, but that does not prove PyPy or another implementation.

## 21. Observability and debugging

Hidden definition-time behavior needs phase vocabulary. A bounded diagnostic event can contain:

~~~text
phase: set_name | init_subclass | class_decorator | meta_prepare | meta_new | meta_init | meta_call
class_module: synthetic.module
class_qualname: Report
rule: unique-code
outcome: accepted | rejected
~~~

Do not record descriptor values, request bodies, credentials, complete annotations, or arbitrary
`repr` output.

### Debugging order

1. Confirm whether the failure happened during import, startup, or request handling.
2. Find the raw class attribute with `vars(cls).get(name)`.
3. Classify it as data descriptor, non-data descriptor, or ordinary value.
4. Inspect the instance dictionary only when one exists.
5. Check whether `__getattribute__` is overridden and delegates.
6. For class creation, list chosen bases and `type(base)` candidates.
7. Record which hook consumed each class keyword.
8. Compare the object before and after every class decorator with `is` and MRO.
9. Check that a metaclass passes the complete namespace through `type.__new__`.
10. Reproduce in a fresh process when import-time registries or reloads are involved.

### Error messages

Prefer:

~~~text
Invalid ReportHandler declaration: code must be lowercase and trimmed
~~~

Avoid dumping:

~~~text
namespace={...every class value, annotation, secret default, descriptor state...}
~~~

## 22. Import-time, global-state, and lifecycle hazards

Class bodies, descriptor naming, subclass hooks, metaclass creation, and class decorators normally
run while their defining module executes. Therefore:

- importing a module can mutate registries;
- skipped imports mean skipped definitions and registrations;
- a circular import can expose partially initialized modules;
- reload can create new class identities and repeat side effects;
- test order can leak a process-global registry;
- pre-fork and spawned workers can obtain different state; and
- “all subclasses” means live class objects known to that process, not an application catalog.

Contain these hazards by:

- making class hooks validate rather than activate;
- building a fresh explicit registry at startup;
- rejecting duplicates rather than choosing by import order;
- publishing an immutable snapshot;
- providing a test-local registry or resettable composition object;
- recording provenance without private payloads; and
- restarting workers for definition changes instead of promising magical hot reload.

These are production inferences from normal import and class-statement timing, not a Python promise
that every framework initializes the same way.

## 23. Concurrency and state safety

A descriptor class object is shared, but Python's lookup protocol does not make mutable descriptor
state thread-safe. Per-instance storage reduces accidental sharing; it does not make the stored
object immutable or synchronized.

An `__init_subclass__` registry backed by a process-global dictionary needs a concurrency and
lifecycle policy if classes can be created dynamically after startup. Prefer finishing definition
and validation before serving traffic, then expose an immutable registry snapshot.

Metaclass `__call__` is not a dependency-injection scope. If it caches instances, it must define
keys, lifetime, failure behavior, contention, async context, process boundaries, and test reset.
An explicit provider/factory usually states those rules more clearly.

No lock or async mechanism is added to this teaching code because its actual operations are
synchronous, definition-time, and completed before concurrent request handling.

## 24. Performance and memory

Descriptors add a call or policy step to dotted access. Class hooks and decorators usually spend
their work at definition time. Metaclass `__call__` can affect every construction call. Those are
mechanical observations, not benchmark results.

Before optimizing:

1. identify whether the cost is import/startup, construction, or hot-path lookup;
2. benchmark the real workload across supported runtimes;
3. include validation, allocation, cache, and contention behavior;
4. avoid comparing a descriptor that validates with a plain attribute that does not; and
5. record warm-up, trials, distributions, and uncertainty.

Memory questions include descriptor-owned caches retaining instances, extra wrapper subclasses,
registries retaining class objects after reload, and slot-backed storage. This unit claims no
speedup or memory reduction.

## 25. Framework-owned magic and security boundary

Credible framework uses exist:

- ORM fields and validation descriptors;
- declarative schemas that need class-body capture;
- ABC behavior implemented through `ABCMeta`;
- enum class construction;
- framework model registration; and
- proxy or instrumentation classes with a documented construction contract.

Using such a framework is not equivalent to authoring a metaclass. The framework should own:

- supported inheritance combinations;
- static typing integration;
- class identity and serialization behavior;
- import/startup lifecycle;
- diagnostics;
- upgrade compatibility; and
- escape hatches.

Descriptors and metaclasses run ordinary in-process Python with application authority. They are not
sandboxes, authentication, data validation for untrusted code, or permission boundaries.

## 26. Refactoring path

### From repeated properties to a descriptor

1. Preserve property behavior with tests.
2. Identify the exact repeated get/set/delete policy.
3. Extract conversion and validation functions first.
4. Introduce one descriptor for one field.
5. Prove class access, instance storage, precedence, error, and deletion behavior.
6. Migrate a second evidenced owner.
7. Remove duplicate properties.
8. Stop; do not add a metaclass to discover descriptors because `__set_name__` already supplies
   naming.

### From metaclass post-processing to `__init_subclass__`

1. Record which phase the current code actually needs.
2. Preserve valid/invalid class-definition tests.
3. Move post-creation family validation to the base hook.
4. Consume and forward class keywords cooperatively.
5. Keep registration or activation explicit.
6. test multiple inheritance with real framework bases.
7. Remove the metaclass if no pre-body or metaclass-level behavior remains.

### From replacing class decorator to explicit composition

1. Capture identity, MRO, metadata, typing, and integration behavior.
2. Identify which operation actually needs wrapping.
3. Decorate that callable or inject a collaborator.
4. Preserve the original class object.
5. Remove copied metadata and wrapper-class compatibility shims.

## 27. When to use each advanced mechanism

### Descriptor

- multiple real owners share attribute-level get/set/delete semantics;
- class-level field introspection is part of a stable contract;
- normal dotted syntax materially improves the model; and
- behavior remains local, synchronous, deterministic, and tested.

### `__init_subclass__`

- a base hierarchy already exists for behavioral reasons;
- every future subclass must satisfy one post-creation rule;
- multiple inheritance is supported cooperatively; and
- definition-time failure is the intended boundary.

### Class decorator

- transformation applies to one explicit completed class;
- local syntax is clearer than inheritance;
- identity policy is deliberate and tested; and
- stacking order is documented.

### Metaclass

- a framework must prepare or observe the namespace while the body executes;
- class-object creation needs coordinated semantics across the family;
- a special operation belongs to the class object's type; or
- construction of all instances truly requires framework-level interception and an explicit
  factory is insufficient.

## 28. When not to use them

Do **not** use these mechanisms when:

- a function, dataclass, property, explicit map, factory, or dependency parameter works;
- there is only speculative future reuse;
- a descriptor would perform I/O or hide expensive computation;
- inheritance exists only to trigger registration;
- class definition is being used as an application startup script;
- a decorator silently replaces a public class;
- a metaclass only adds a method or validates completed class attributes;
- multiple framework metaclasses would need fragile reconciliation;
- typing, serialization, inspection, or IDE behavior has no support plan;
- import order would decide business behavior;
- a global registry has no lifecycle or worker model; or
- the author cannot state the required interception phase.

### Justified “do not use this” conclusion

For the worked backend, **do not use a metaclass**. Repeated field semantics justify a descriptor.
An owned hierarchy justifies bounded cooperative `__init_subclass__` validation. Explicit startup
composition activates implementations. No accepted requirement needs pre-body namespace control,
class-level special operations, or universal instance-construction interception.

This rejection is part of the design, not a missing advanced feature.

## 29. Common misuse and overengineering

| Misuse | Why it happens | Better move |
|---|---|---|
| Descriptor for one trivial field | abstraction is mistaken for reuse | property or function |
| Per-instance value stored on descriptor | descriptor sharing is missed | owner instance storage |
| Descriptor getter performs I/O | dotted syntax looks convenient | explicit service method |
| Treat every descriptor as data | protocol category is skipped | inspect `__set__`/`__delete__` on its type |
| Manually attach descriptor and expect naming | class-creation timing is missed | define in class body or call `__set_name__` |
| Auto-register every subclass | definition is confused with activation | explicit startup registry |
| Omit `super()` in subclass hook | single inheritance test passed | cooperative forwarding contract |
| Swallow unknown class keywords | convenient permissiveness | let terminal hook expose mistakes |
| Replacing class decorator hides identity change | name and class are conflated | in-place transform or explicit wrapper |
| Copy `__name__` and assume identity restored | metadata is confused with object identity | preserve the class or document a new type |
| Metaclass validates completed attributes | power chosen before phase | class decorator or `__init_subclass__` |
| Combined metaclass by trial and error | conflict is treated as syntax | negotiate both framework contracts |
| Filter all dunder namespace entries | internals are guessed | pass complete namespace to `type.__new__` |
| Annotation-driven framework assumes eager values | version change is ignored | documented introspection adapter and dual tests |

## 30. Interview preparation

### Prompt 1 — descriptor precedence

> An instance dictionary contains `x = "instance"`. Its class contains an object named `x` with
> `__get__`. What does `obj.x` return?

Do not answer until you know whether the descriptor's **type** also defines `__set__` or
`__delete__`.

**Exact reasoning gap if missed:** the answer says “instance wins” or “descriptor wins” without
classifying data versus non-data.

**Likely follow-up:** Why can an instance shadow a normal method?

**Checkpoint:** user-defined functions are non-data descriptors.

### Prompt 2 — `__set_name__`

> A library assigns a descriptor to a class after the class was created. Why is its storage name
> empty?

**Exact reasoning gap if missed:** automatic name notification is tied to `type.__new__` scanning
the class namespace; later assignment does not replay it.

**Likely follow-up:** Is `__set_name__` itself enough to make the object a descriptor?

**Checkpoint:** no; descriptor participation comes from get/set/delete methods.

### Prompt 3 — cooperative subclass hooks

> Two mixins consume different class-definition keywords. How should their hooks compose?

**Exact reasoning gap if missed:** each hook must consume only its own keyword and forward the rest
through `super()`; final leftovers should fail.

**Likely follow-up:** Can you promise the visible left base records first?

**Checkpoint:** execution depends on MRO and where each hook calls `super()`.

### Prompt 4 — class decorator identity

> A class decorator returns a subclass with the same `__name__` and `__module__`. Is it the same
> class?

**Exact reasoning gap if missed:** copied metadata does not preserve `is` identity or MRO, and tools
may have captured the original.

**Likely follow-up:** What would you test?

**Checkpoint:** identity, MRO, `isinstance`, signature, typing, pickling, and real framework
integration.

### Prompt 5 — metaclass phases

> Distinguish metaclass `__prepare__`, `__new__`, `__init__`, and `__call__`.

**Exact reasoning gap if missed:** `__prepare__` precedes class-body execution; metaclass
`__new__` creates the class; metaclass `__init__` initializes that class; metaclass `__call__`
intercepts later calls to the finished class and usually delegates to instance `__new__`/`__init__`.

### Prompt 6 — conflict

> Why can inheriting from two framework classes raise a metaclass conflict?

**Exact reasoning gap if missed:** the selected metaclass must be a subtype of every type-based
candidate. “Python cannot do multiple inheritance” is not the reason.

**Senior follow-up:** When would you refuse to write a combined metaclass?

**Checkpoint:** refuse when the frameworks do not publish compatible composition contracts or a
smaller integration boundary exists.

### Prompt 7 — current-runtime difference

> What must a class-processing framework review when moving from Python 3.11 to 3.14?

**Exact reasoning gap if missed:** annotation evaluation became lazy in 3.14, and `annotationlib`
provides the documented inspection path; direct eager `__annotations__` assumptions need audit.

### Strong short answer

Use explicit Python first. A descriptor is justified when repeated attribute get/set/delete
behavior is the stable extension point; classify it as data or non-data to reason about lookup.
Use `__init_subclass__` for cooperative rules on every future subclass and a class decorator for an
explicit transformation of one completed class. A metaclass owns namespace and class-object
creation, while its `__call__` can own later instance construction. That power brings selection
conflicts, import-time failure, identity, typing, and tooling costs, so I require a phase no smaller
mechanism can reach.

### Code-review exercise

Review this proposal:

~~~python
MODELS: dict[str, type[object]] = {}


class ModelMeta(type):
    def __new__(
        mcls: type,
        name: str,
        bases: tuple[type[object], ...],
        namespace: dict[str, object],
    ) -> type[object]:
        cleaned = {key: value for key, value in namespace.items() if not key.startswith("__")}
        model = super().__new__(mcls, name, bases, cleaned)
        MODELS[name.lower()] = model
        return model
~~~

A strong critique should find:

1. no evidenced need for a metaclass;
2. definition-time process-global registration;
3. import/reload/order and duplicate ambiguity;
4. destructive removal of meaningful dunder namespace entries;
5. likely `__classcell__` breakage for zero-argument `super()` on CPython;
6. registration before a complete application activation policy;
7. missing cooperative keyword handling;
8. poor error provenance;
9. framework composition and metaclass-conflict risk; and
10. simpler alternatives: explicit map, class decorator, or `__init_subclass__` validation
    depending on the actual requirement.

### Small design exercise

For each scenario, choose exactly one smallest starting mechanism and explain the rejected next
power:

1. one immutable request value needs normalization;
2. one mutable class validates one field;
3. twenty owners share one field protocol;
4. one class needs a visible marker;
5. every descendant of an existing base needs a code;
6. a DSL must reject duplicate declarations while the class body runs; and
7. five known handlers must be assembled at startup.

## 31. Closed-book revision cues

1. Draw the lookup precedence ladder.
2. Explain owner versus instance arguments to `__get__`.
3. Explain why functions become bound methods.
4. State when `__set_name__` runs and when it does not.
5. Write a cooperative `__init_subclass__` keyword-forwarding skeleton.
6. Compare an in-place and replacing class decorator.
7. Draw class creation separately from instance creation.
8. State metaclass selection's “subtype of all candidates” rule.
9. Label `__classcell__` as CPython-specific.
10. Explain the Python 3.14 lazy-annotation impact.
11. Reject a metaclass for the worked backend.
12. Name one import-time and one tooling failure.

## 32. Vocabulary and professional English

### Intercept

| Item | Content |
|---|---|
| Pronunciation | in-ter-SEPT |
| Simple English meaning | catch an action before it finishes |
| Hindi cue | बीच में पकड़ना |
| Meaning here | run policy at attribute, subclass, class, or construction boundaries |

Natural examples:

1. The proxy intercepts outbound calls.
2. The validator intercepts an invalid assignment.
3. The hook intercepts subclass creation.
4. **Interview:** “Which event must this mechanism intercept?”
5. **Engineering:** “Do not intercept dotted lookup for a network operation.”

### Propagate

| Item | Content |
|---|---|
| Pronunciation | PROP-uh-gate |
| Simple English meaning | pass something onward without losing it |
| Hindi cue | आगे पहुँचाना |
| Meaning here | forward class keywords or `__classcell__` to the responsible next layer |

Natural examples:

1. The service propagates cancellation.
2. The wrapper propagates the original error.
3. The hook propagates unconsumed keywords.
4. **Interview:** “A cooperative hook must propagate keywords with `super()`.”
5. **Engineering:** “Pass the full namespace so required entries propagate.”

### Precedence

| Item | Content |
|---|---|
| Pronunciation | PRESS-uh-dens |
| Simple English meaning | the rule deciding what wins first |
| Hindi cue | प्राथमिकता |
| Meaning here | data descriptor versus instance and non-data lookup order |

Natural examples:

1. Safety has precedence over convenience.
2. The latest explicit configuration has precedence.
3. A data descriptor has precedence over the instance dictionary.
4. **Interview:** “State lookup precedence before predicting the result.”
5. **Engineering:** “The cache relies on non-data descriptor precedence.”

### Coupling

| Item | Content |
|---|---|
| Pronunciation | KUP-ling |
| Simple English meaning | how strongly parts depend on each other's details |
| Hindi cue | परस्पर निर्भरता |
| Meaning here | inheritance, metaclass, import, and tooling assumptions forced on clients |

Natural examples:

1. The adapter lowers vendor coupling.
2. Global state creates test coupling.
3. A metaclass adds inheritance-family coupling.
4. **Interview:** “Metaclass conflicts expose hidden coupling.”
5. **Engineering:** “Prefer a hook if it reduces metaclass coupling.”

## 33. Python Mastery references

The hard mapping in [PYTHON_REFERENCES.md](../../../PYTHON_REFERENCES.md) is:

| Python Mastery unit | Required bridge |
|---|---|
| [PY-OBJ-050 — Attribute lookup, customization, and slots](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-obj-050) | know instance/class namespaces, MRO, `__getattribute__`, and slots |
| [PY-OBJ-060 — Descriptors](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-obj-060) | know the protocol and data/non-data distinction |
| [PY-OBJ-070 — Class-creation hooks and class decorators](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-obj-070) | know `__set_name__`, cooperative `__init_subclass__`, and decorator application |
| [PY-OBJ-080 — Metaclasses and dynamic class creation](https://github.com/rahulyadev/python-mastery/blob/main/CURRICULUM.md#py-obj-080) | know class objects, `type`, selection, namespace, and creation phases |

Smallest bridge if these are not yet studied:

1. learn ordinary attribute lookup and MRO;
2. run [EXP-01](experiments/EXP-01-descriptor-lookup-precedence/README.md);
3. explain method binding;
4. run [EXP-02](experiments/EXP-02-class-creation-order/README.md); and
5. return to the decision ladder before implementing anything.

## 34. Practice, experiments, examples, and visual

| Artifact | Purpose | Evidence boundary |
|---|---|---|
| [Worked descriptor](examples/managed_fields.py) | justified typed managed fields | maintainer-authored example |
| [Class hook mechanics](examples/class_hooks.py) | cooperative hooks, decorators, metaclass phases | mechanism comparison, not framework recommendation |
| [Worked demo](examples/run_mechanism_demo.py) | smallest chosen combination and metaclass rejection | deterministic synthetic output |
| [Lookup probe](examples/lookup_probe.py) | precedence and binding observations | CPython executions recorded separately |
| [Class-creation probe](examples/class_creation_probe.py) | definition versus construction phases | explicit event instrumentation |
| [EXP-01](experiments/EXP-01-descriptor-lookup-precedence/README.md) | data/non-data lookup | actual output, bounded inference |
| [EXP-02](experiments/EXP-02-class-creation-order/README.md) | class and instance phase order | actual output, CPython detail labeled |
| [Practice lab](practice/README.md) | predict, run, observe, explain, refactor, vary | unsolved; no learner evidence yet |
| [Decision visual](visuals/mechanism-decision-explorer.html) | compare least-powerful mechanisms | embedded data tested; not browser proof |

## 35. Authoritative sources

Only the following sources were opened and read for this unit:

1. [Python 3.14 Descriptor Guide](https://docs.python.org/3.14/howto/descriptor.html) — protocol,
   lookup precedence, instance/class/`super` invocation, name notification, properties, methods,
   static methods, class methods, and slots.
2. [Python 3.14 data model: customizing class creation](https://docs.python.org/3.14/reference/datamodel.html#customizing-class-creation)
   — `__init_subclass__`, `__set_name__`, metaclass selection, namespace preparation, body
   execution, class-object creation, `__classcell__`, and decorator timing.
3. [Python 3.14 data model: classes and basic customization](https://docs.python.org/3.14/reference/datamodel.html#classes)
   — classes as callables and the `__new__`/`__init__` construction roles.
4. [Python 3.14 class definitions](https://docs.python.org/3.14/reference/compound_stmts.html#class-definitions)
   — class suite execution, decorator equivalence/application order, name binding, and type-
   parameter version note.
5. [Python 3.14 `annotationlib`](https://docs.python.org/3.14/library/annotationlib.html) — lazy
   annotation inspection after and during class creation.
6. [Python 3.11 data model](https://docs.python.org/3.11/reference/datamodel.html#customizing-class-creation)
   — compatibility-floor descriptor/class-creation mechanics and `__classcell__` note.
7. [PEP 487 — Simpler customisation of class creation](https://peps.python.org/pep-0487/) — rationale,
   `__init_subclass__`, `__set_name__`, easier inheritance, and reduced conflict pressure.
8. [PEP 3115 — Metaclasses in Python 3000](https://peps.python.org/pep-3115/) — metaclass syntax and
   the pre-body `__prepare__` hook.
9. [PEP 3135 — New Super](https://peps.python.org/pep-3135/) — implicit `__class__` cell and zero-
   argument `super()`.

The examples, exercises, diagrams, scenario data, and explanations are original and synthetic. No
framework source, private code, production log, credential, proprietary schema, or copied book
diagram is used.

## 36. Durable clarification log

| Date | Clarification | Why it belongs in canonical notes | Source or evidence |
|---|---|---|---|
| 2026-09-06 | A descriptor's data/non-data category changes whether an instance entry can shadow it. | Prevents the recurring “instance dictionary always wins” error. | Python Descriptor Guide and EXP-01 |
| 2026-09-06 | `__init_subclass__` and class decorators are post-creation mechanisms with different inheritance reach. | Prevents selecting a metaclass for ordinary post-creation work. | Python data model and PEP 487 |
| 2026-09-06 | Metaclass `__call__` governs calls to completed class objects; it is distinct from metaclass `__new__` creating those class objects. | Separates class creation from instance creation in interviews and debugging. | Python data model and EXP-02 |
| 2026-09-06 | `__classcell__` is labeled CPython-specific and should be propagated via the complete namespace. | Avoids inventing a cross-implementation internal guarantee. | Python data model and CPython-gated negative test |
| 2026-09-06 | Python 3.14 lazy annotations make annotation-driven class processing version-sensitive. | Prevents direct eager `__annotations__` assumptions across the 3.11/3.14 support range. | Python 3.14 data model and `annotationlib` |
