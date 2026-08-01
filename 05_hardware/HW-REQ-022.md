---
id: HW-REQ-022
text: >
  The Temp_Sense_Chain shall measure the LED module temperature over the range -40 C to +150 C with
  an accuracy of +/-3 K between +80 C and +140 C, shall update the value at least every 100 ms, and
  shall classify a measured value outside the band -50 C to +160 C as a sensor fault.
type: electrical
asil: B
source: CR-014
derived_from: [CR-014, FSR-002]
allocated_to: [Temp_Sense_Chain, SM-05]
verified_by: []
status: draft
rationale: >
  An NTC divider with a pull-up rail reads towards one supply end on an open circuit and towards
  the other on a short, so both sensor failure modes leave the plausibility band and are detected
  without an extra component. +/-3 K in the derating region is what makes the 105 C / 125 C
  breakpoints of HW-REQ-023 meaningful; outside that region the accuracy is irrelevant to the
  function. Plausible example values.
---

## Context

Hardware requirement from the phase 6 refinement of the E/E architecture (HWE.1 / HWE.2).
Owning requirement of `SM-05` (sensing path). Derivation: [`analysis_thermal_derating.md`](analysis_thermal_derating.md).
Verification entry: [`hw_verification_plan.md`](hw_verification_plan.md). Test cases are a
hand-off to `verification-engineer`.
