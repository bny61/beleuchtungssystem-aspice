---
id: HW-REQ-023
text: >
  While the measured LED module temperature is above 105 C, the lighting ECU shall reduce the
  channel set point linearly by 40 mA per kelvin from 1.20 A down to the derating floor of
  HW-REQ-008, and shall hold the set point at that floor above 125 C.
type: electrical
asil: B
source: CR-014
derived_from: [CR-014, HW-REQ-008, HW-REQ-022]
allocated_to: [LED_Driver_Stage_1, Temp_Sense_Chain, SM-05]
verified_by: []
status: draft
rationale: >
  Owning requirement of SM-05 and the derating curve behind A-12. Breakpoints derived in
  analysis_thermal_derating.md: with the assumed thermal path the junction reaches its 135 C design
  limit at a solder-point temperature of about 130 C at full current, so derating has to start
  clearly below that. The floor is held rather than reducing further, because reducing below 400 mA
  would make the open-load threshold of SM-01 ambiguous (HW-REQ-002). Plausible example values.
  Assumptions A-12, A-20.
---

## Context

Hardware requirement from the phase 6 refinement of the E/E architecture (HWE.1 / HWE.2).
Owning requirement of `SM-05` (derating curve). Derivation: [`analysis_thermal_derating.md`](analysis_thermal_derating.md).
Verification entry: [`hw_verification_plan.md`](hw_verification_plan.md). Test cases are a
hand-off to `verification-engineer`.
