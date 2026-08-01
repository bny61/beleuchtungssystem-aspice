---
id: HW-REQ-013
text: >
  While a clamped load dump with a peak of 58 V and a decay time constant of 400 ms is applied at
  the supply input, the lighting ECU shall keep the low beam energised at the commanded set point
  and shall sustain no permanent damage.
type: electrical
asil: B
source: CR-017
derived_from: [CR-017, SYS-REQ-012, FSR-002]
allocated_to: [Power_Supply_Unit, LED_Driver_Stage_1]
verified_by: []
status: draft
rationale: >
  Load dump is tested per ISO 16750-2 (electrical loads, load-dump test) using the pulse shape of
  ISO 7637-2 (pulse 5a / 5b). The 58 V clamped level presumes central suppression in the vehicle
  (A-19); the unsuppressed case is explicitly excluded and is an assumption to be validated with
  the vehicle manufacturer. Functional status class A is demanded because the low beam is the
  ASIL B function of SG-01 and a load dump is a plausible night-driving event. Plausible example
  values.
---

## Context

Hardware requirement from the phase 6 refinement of the E/E architecture (HWE.1 / HWE.2).
Derivation: [`analysis_supply_and_transients.md`](analysis_supply_and_transients.md).
Verification entry: [`hw_verification_plan.md`](hw_verification_plan.md). Test cases are a hand-off
to `verification-engineer`.
