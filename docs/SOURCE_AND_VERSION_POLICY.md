# Source, History, and Version Policy

[Back to README](../README.md)

## Python baseline

- Canonical teaching baseline: Python 3.14.
- Initially verified runtime: CPython 3.14.7, released August 5, 2026.
- Interview compatibility baseline: Python 3.11.
- Preview releases are non-canonical until stable.
- `.python-version` records the initially tested patch version.

For syntax or behaviour introduced after Python 3.11, state the first supported Python version and give a useful Python 3.11 alternative when practical.

## Source order for Python mechanics

Prefer:

1. [Python Language Reference](https://docs.python.org/3/reference/);
2. [Python Standard Library documentation](https://docs.python.org/3/library/);
3. [Python typing specification](https://typing.python.org/en/latest/spec/);
4. relevant accepted or final [PEPs](https://peps.python.org/);
5. Python Developer’s Guide;
6. CPython source and official implementation notes only when needed;
7. authoritative documentation for pytest, mypy, Ruff, Hypothesis, or a framework used in a bounded example.

## Source order for design and history

Prefer original or authoritative sources:

1. Gamma, Helm, Johnson, and Vlissides, *Design Patterns: Elements of Reusable Object-Oriented Software*, for the original GoF catalog and terminology;
2. Liskov and Wing, [“A Behavioral Notion of Subtyping”](https://dl.acm.org/doi/10.1145/197320.197383), for behavioural subtyping;
3. original writings or publications by the named principle or pattern authors when available;
4. Martin Fowler’s [enterprise application pattern catalog](https://martinfowler.com/eaaCatalog/) for application-pattern context;
5. credible books, papers, talks, and articles by established practitioners;
6. strong secondary explanations only when primary material is unavailable or too terse.

The GoF book, Fowler’s books, and other copyrighted works may be cited and summarized, but their prose, diagrams, and substantial examples must not be reproduced.

## History claims

For dates, origin, authorship, or original intent:

- verify the claim;
- cite near the claim;
- distinguish established history from later interpretation;
- avoid invented origin stories;
- state uncertainty when primary sources disagree or are unavailable.

## Pattern-frequency classifications

Interview and production frequencies in `CURRICULUM.md` are reasoned professional judgments, not measured statistics. Unit notes should say so when the frequency classification is discussed. Do not fabricate surveys, percentages, benchmark evidence, or claims of universal popularity.

## Claim classification

Classify subtle claims as one of:

- design-level mechanics;
- Python language guarantee;
- standard-library contract;
- typing-specification behaviour;
- CPython implementation detail;
- framework behaviour;
- platform-specific behaviour;
- version-dependent behaviour;
- professional inference.

Do not convert a CPython observation or framework convention into a language guarantee.

## Citation policy

Cite only sources actually opened and read. Place citations close to important claims involving:

- formal definitions;
- historical attribution;
- Python semantics;
- version changes;
- surprising edge cases;
- concurrency, memory, or object-lifetime behaviour;
- performance or security;
- CPython internals.

Ordinary original teaching prose does not need a citation after every sentence. Keep each unit’s source list compact and exact.

## No fake internals

Do not force an “internals” section into every pattern. Separate:

- participants and collaboration;
- Python dispatch, descriptors, decorators, imports, or protocols;
- standard-library implementation behaviour;
- CPython source-level details.

Use CPython details only when they materially explain the design and can be reproduced or sourced.

## Experiments and benchmarks

Every experiment records its question, hypothesis, exact environment, command, actual output, interpretation, and limitations. Every benchmark records workload, input distribution, warm-up, trials, timing method, observations, uncertainty, and limitations.

Never claim that a test, experiment, benchmark, profiler session, or comparison ran when it did not. Never invent a speedup or memory reduction.

## Framework examples

FastAPI or Django may appear only when a framework example materially improves backend understanding. Label framework-managed dependency injection, MVT, ORM Active Record/Data Mapper behaviour, transaction management, and event hooks accurately. Do not turn a unit into a framework curriculum.

## Release upgrade process

When a new stable Python feature release is considered:

1. Verify it through official Python sources.
2. Update the baseline and verification date.
3. Update `.python-version`, `pyproject.toml`, and `uv.lock` when appropriate.
4. Run repository validation and all existing tests.
5. Audit typing, decorators, protocols, imports, dataclasses, enums, concurrency, and framework examples.
6. Add version overlays rather than rewriting historical behaviour.
7. Preserve Python 3.11 interview alternatives where useful.
