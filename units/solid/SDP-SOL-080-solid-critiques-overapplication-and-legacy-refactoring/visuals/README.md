# Visuals — SDP-SOL-080

Open [Compare observable behaviour](behaviour-comparison.html) in a browser. It is a
self-contained teaching page with no network dependencies, tracking, or external service.
GitHub's file view shows its source; download/open it or use a local preview to interact.

## How to read this visual

Choose one of five scenarios and compare the legacy function with either the helper
extraction or the eager rewrite. Read the final observations first, then each event column
top to bottom. Row numbers align event positions, not real time. The first changed event
has both a highlight and an explicit text label.

Try the successful case too: matching counts and saved lines still hide changed event order.
Then select the helper extraction and check the same failing case.

## Key insight

A refactoring comparison needs the behaviour relevant to the caller, including failure
effects and input consumption. A green return-value check can be too weak.

## Simplification or limitation

The page embeds actual JSON from [trace_probe.py](../examples/trace_probe.py), verified on
the runtimes recorded in [EXP-01](../experiments/EXP-01-observable-trace/README.md). It does
not run Python. Its “saved” lines belong to an in-memory fake, not durable storage. The
program is synchronous, has finite input, and makes read order observable by design.

Use the text experiment when JavaScript is unavailable. A matched selected trace does not
certify every possible input, a new writer, or a production rollout.

## Refactoring decision map

```text
real change known?
  no  -> preserve stable code; investigate a demonstrated problem first
  yes -> relevant behaviour observed?
           no  -> characterize the boundary or create one narrow test seam
           yes -> make one small structural edit -> compare -> review its benefit
```

### How to read this visual

Start at the first question and follow the applicable branch. Arrows mean decisions in
an engineering workflow, not Python calls or source imports.

### Key insight

Understanding behaviour precedes a broad structural cleanup.

### Simplification or limitation

This is a conceptual aid. It does not forbid focused emergency fixes or require perfect
coverage before every local improvement. The scope of observation should match the risk.
