# Visual — SDP-PYT-050 dependency lifetime map

Open [lifetime-map.html](lifetime-map.html) in a browser and choose among module cache,
application, request, transient operation, and traditional Singleton lifetimes.

## How to read this visual

1. Start with the two questions at the top: cache reuse and ownership are different decisions.
2. Choose a lifetime on the left.
3. Read the selected owner, then follow begin → sharing boundary → end.
4. Finish with cleanup and the red boundary warning.
5. Compare application scope with module cache and traditional Singleton before choosing a design.

## Key insight

The import system may return one cached module object for one name in one interpreter. That fact
does not identify which application instance owns a resource, when it becomes ready, when it must
close, or how many worker processes exist. Explicit lifetime boundaries answer those questions.

## Simplification or limitation

This is a conceptual ownership explorer, not literal CPython memory layout or a complete ASGI
timeline. Real frameworks may distinguish response, function, connection, task, and process
scopes; cleanup failure and cancellation add paths not drawn here.

The JSON embedded in the HTML is compared with [visual_data.py](../examples/visual_data.py) by an
automated test so the selectable states cannot silently drift from the maintained Python model.
