# EXP-01 — Descriptor lookup precedence and method binding

| Field | Value |
|---|---|
| Owning unit | [SDP-PYT-100](../../README.md) |
| Curriculum | [CURRICULUM.md](../../../../../CURRICULUM.md#sdp-pyt-100) |
| Precise question | Does an instance entry beat a data descriptor, a non-data descriptor, or a class function during dotted lookup? |
| Classification | Python language behavior; the probe output was observed on CPython |
| Status | Reproduced |

## Why observation is necessary

“The instance dictionary is searched first” is an attractive but wrong shortcut. The descriptor
category changes precedence, and class functions demonstrate why method binding is part of the
same lookup model.

## Hypothesis

> A data descriptor will beat the same-named instance entry; the instance entry will beat a
> non-data descriptor and a function; class access will pass no instance; an unshadowed function
> will bind `self`.

## Environment

~~~text
Date: 2026-09-06
Operating system: Linux 7.0.0-31-generic
Architecture: x86_64
Python runs: CPython 3.14.7 and CPython 3.11.16
Canonical build: Clang 22.1.3
Dependencies: standard library only
Relevant flags: none
~~~

## Controls and variables

- Controlled: one `Sample` class, one instance, and fixed descriptor results.
- Changed: data versus non-data descriptor category and class versus instance access.
- Measured: returned value, descriptor identity, and bound-method `__self__`/`__func__`.

## Reproduction command

~~~bash
uv run --locked python units/pythonic/SDP-PYT-100-descriptors-class-hooks-metaclasses-when-justified/examples/lookup_probe.py
~~~

## Predicted result

~~~text
data descriptor wins over the attempted instance shadow
instance value wins over the non-data descriptor
class access returns each descriptor
method access binds the instance and retains the original function
data assignment and deletion call the descriptor
~~~

## Observed result

Both CPython 3.14.7 and CPython 3.11.16 produced the same output:

~~~text
sample.data -> data-default
sample.__dict__['data'] -> instance-data-shadow-attempt
sample.cached -> instance-cached
Sample.data is raw_data -> True
Sample.cached is raw_non_data -> True
bound.__self__ is sample -> True
bound.__func__ is raw_method -> True
bound() -> bound-result
sample.data after assignment -> assigned-through-data-descriptor
sample.data after deletion -> data-default
~~~

## Interpretation

1. The same-named instance `data` entry exists but does not control `sample.data` because
   `DataValue` implements `__set__`/`__delete__` and is a data descriptor.
2. `NonDataValue` implements only `__get__`, so `sample.__dict__["cached"]` wins.
3. Class access invokes `__get__(None, Sample)`; this implementation returns the descriptor itself.
4. The class-body function is a non-data descriptor. With no shadowing entry, instance access
   produces a method carrying the instance in `__self__` and original function in `__func__`.
5. The output does not reveal CPython's C functions, cache strategy, or performance.

## Visual interpretation

~~~text
sample.name
    |
    +-- data descriptor in class MRO? ------ yes --> __get__(sample, Sample)
    |
    +-- instance __dict__ entry? ----------- yes --> return instance value
    |
    +-- non-data descriptor in class MRO? -- yes --> __get__(sample, Sample)
    |
    +-- ordinary class value? -------------- yes --> return class value
    |
    +-- otherwise --------------------------------> __getattr__ fallback
~~~

### How to read this visual

Start at the top for every ordinary instance dotted lookup and stop at the first matching branch.
The two descriptor branches surround the instance dictionary because data and non-data descriptors
have different precedence.

### Key insight

“Descriptor” alone is not enough information. Ask whether it is data or non-data and whether access
starts from an instance, a class, or `super()`.

### Simplification or limitation

This is the ordinary `object.__getattribute__` decision shape. It omits custom
`__getattribute__`, slots, metaclass attribute lookup, `super()`'s different starting point, and
implementation caches.

## Design conclusion

Use a data descriptor only when it must remain authoritative over same-named instance data. A
non-data descriptor is appropriate for computed defaults or caches that instances may override.
For one attribute on one class, a property communicates the policy more directly.

## Sources

1. [Python 3.14 Descriptor Guide — descriptor protocol and invocation](https://docs.python.org/3.14/howto/descriptor.html#technical-tutorial).
2. [Python 3.14 data model — implementing descriptors](https://docs.python.org/3.14/reference/datamodel.html#implementing-descriptors).
