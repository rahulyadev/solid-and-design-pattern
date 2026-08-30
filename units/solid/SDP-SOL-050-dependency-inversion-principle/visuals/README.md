# Visuals — SDP-SOL-050 Dependency Inversion Principle

[Unit note](../README.md) · [Interactive dependency map](dependency-map.html)

Open the HTML file in a browser. It is self-contained, makes no network requests, and uses
the actual names from the [replenishment example](../examples/run_replenishment_demo.py).
It models relationships; it does not run Python or connect to a database.

## How to read this visual

Choose a design, then choose which kind of arrow to inspect:

1. **Injected concrete type + Source imports:** policy still reaches the adapter and driver.
2. **Policy-owned contract + Source imports:** policy and adapter refer inward to contract definitions.
3. **Policy-owned contract + Runtime calls:** policy calls the supplied SQLite object directly.
4. Change only the design while staying in Runtime calls. The concrete call path remains the same.

Read left to right on a wide display and top to bottom on a narrow display. The inward
adapter-to-contract arrow points left on a wide display and up on a narrow display.

## Key insight

Injection answers who supplies an object. DIP answers what source definitions the policy
depends on. Neither requires a Protocol object in the runtime call path.

## Simplification or limitation

These are conceptual source and call maps, not a complete module graph or a CPython memory
diagram. The source view omits standard-library helpers. The contract arrow from the SQLite
adapter represents its import of consumer-owned errors; Protocol conformance is structural.
The composition root knows both concrete setup and policy, and owns the database lifetime.

The runtime view represents a successful read. Unknown data, driver failure, concurrent
writes, and cleanup failures are omitted. Changing the drawing cannot make an unavailable
database work. The [import experiment](../experiments/EXP-01-import-isolation/README.md)
checks the narrower claim that policy can be reused without loading that driver.

## Static companion

| View | Before | After |
|---|---|---|
| Source imports | Policy → SQLite adapter → sqlite3 | Policy → stock contract ← SQLite adapter → sqlite3 |
| Runtime calls | Policy → SQLite adapter → SQLite connection | Policy → SQLite adapter → SQLite connection |
| Construction | Caller supplies concrete adapter | Caller supplies adapter fitting the contract |

Read a row as one comparison dimension. The important difference is in the first row.
The limitation is that this summary omits exception and data-contract dependencies; inspect
those in the code as well as looking at the picture.
