---
id: SYS-REQ-014
text: >
  When the load current of a low-beam channel, measured during the PWM on-phase, remains below
  150 mA for more than 50 ms, the lighting ECU shall classify the channel as "open load".
type: functional
asil: B
source: CR-007
derived_from: [CR-007, FSR-001]
allocated_to: [ECU_LightingCtrl, SWC_LightManager, SM-01]
verified_by: [TC-021]
status: draft
rationale: >
  Threshold and debounce time derived from the FTTI budget of SG-01 (150 mA / 50 ms: plausible
  example values, not validated data). Measurement uncertainty at the threshold is +/-20 mA per
  HW-REQ-001; guaranteed trip below 130 mA, guaranteed no trip above 170 mA per HW-REQ-002.
---

## Context

Reference record for the Requirements-as-Code format and part of the Golden Thread.

## Change note (phase 3 refinement, hardware-engineer)

Previous wording: "When the load current of a low-beam channel falls below 150 mA for more than
50 ms, the lighting ECU shall classify the channel as 'open load' and increment the fault counter."

Two defects were resolved:

1. **Not atomic** — the fault counter was a second testable statement. Split out as `SYS-REQ-015`.
2. **Not unambiguous** — the text did not say when the current is measured. Under PWM dimming the
   current is genuinely zero in every off-phase, so an ungated comparison trips on every dim cycle.
   The measurement is now bound to the PWM on-phase.

The ID is retained because it carries the original meaning and is part of the Golden Thread.
Status dropped from `reviewed` to `draft`; re-review required. Analysis:
[`../../05_hardware/analysis_current_sensing.md`](../../05_hardware/analysis_current_sensing.md)

## Open points

1. Tolerance analysis of the current sensing — **closed**, see `HW-REQ-001` / `HW-REQ-002`.
