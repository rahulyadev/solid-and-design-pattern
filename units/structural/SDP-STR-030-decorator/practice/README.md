# Unsolved quote-combination lab — SDP-STR-030

A synthetic parcel preview quotes integer cents. One client has flags for a discount and a minimum;
now different channels require different orders and an optional surcharge. No payment or shipment
occurs. The worked text example does not contain the quote policy or a lab solution.

`build_quote` deliberately raises NotImplementedError. Its `object` annotation is a temporary seam
for you to replace after deciding the useful operation and result contract. Baseline tests remain
runnable; they do not define your final structure or prove exercise completion.

## Predict

Write the current output for Parcel(150), with neither option and with both options. Explain which
operation acts first. Predict whether swapping the two operations changes the result. Draw the
current dependency from the client to the base pricing function before reading test output.

## Run

Use the existing locked interpreter and `/tmp` cache exports from the parent note:

```bash
python units/structural/SDP-STR-030-decorator/practice/quote_lab.py
mkdir -p /tmp/sdp-str-030/pytest
python -m pytest -q -p no:cacheprovider --basetemp=/tmp/sdp-str-030/pytest/lab units/structural/SDP-STR-030-decorator/practice
```

## Observe

The script prints the baseline amounts and `target_complete=False`. Compare the actual output with
your prediction; keep both. Passing characterization tests only protects current behavior.

## Explain

Which decisions vary by channel, which stay in base pricing, and what result promise permits a
wrapper to change the amount? Explain why a function/closure might be enough, then identify a real
reason for choosing an object capability. Do not choose from pattern names alone.

## Refactor — public requirements, no solution

Preserve your original code and reasoning before editing the attempt. Design one typed quote
capability that both the base and your selected wrappers can satisfy. Keep client calls stable while
configuration chooses and orders policies:

- Base pricing remains `100 + 2 * mass_grams`, in synthetic integer cents; mass must be positive.
- A discount returns 90% of the amount it receives, rounded down to integer cents.
- A minimum raises any received amount below its configured nonnegative floor to that floor.
- A surcharge adds a configured nonnegative number of cents to the received amount.
- Any subset can be configured. The explicit nesting order determines how policies combine.
- A quote must delegate once per layer, pass the same parcel through, and never mutate it.
- Invalid configuration is rejected at construction; errors from the base remain visible with no
  automatic retry, cache, success placeholder, or external charge.
- Unknown extra source capabilities must not silently become part of the client's quote contract.
- Plain base callers must still be supported. Give the composition root responsibility for wiring.

Keep the final operation narrow. Define rounding, nonnegative amounts, equality at the minimum,
and what makes a discount/minimum combination legal for the client. Add your own tests for each
boundary and for at least two noncommuting compositions. Use a fake that can count calls and fail;
verify effects and error preservation rather than concrete private wrapper layout. Update the
unsolved-target characterization only after preserving the starting attempt.

## Vary

A new channel requires the minimum to apply after all adjustments and says discounts may never
reduce a mandatory handling fee. Decide whether arbitrary decorators still communicate valid choices
well or whether a named fixed feature is safer. Then imagine returning a mutable itemized quote:
explain ownership of its lines and how sharing could change results without a new request.
Do not implement extra infrastructure until you have stated the changed contract.

## Evidence and review

Provide your attempt, actual edge-case results, one composition diagram, one failure diagnosis, and
an argument for your simplest design under the variation. A coach should ask one question at a time
and identify the first missing reasoning step. Request hints progressively after an attempt; no
reference solution, final expected composition outputs, or hints are included here.
