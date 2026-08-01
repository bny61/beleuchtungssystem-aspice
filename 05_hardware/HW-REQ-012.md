---
id: HW-REQ-012
text: >
  The lighting ECU shall meet the functional status class assigned to each supply voltage range in
  the operating-range table of analysis_supply_and_transients.md, and shall resume unrestricted
  operation within 200 ms after the supply voltage has returned into the range 16 V to 32 V.
type: electrical
asil: B
source: SYS-REQ-012
derived_from: [SYS-REQ-012, SYS-REQ-013, FSR-002]
allocated_to: [Power_Supply_Unit, LED_Driver_Stage_1, ECU_LightingCtrl]
verified_by: []
status: draft
rationale: >
  Closes the overvoltage half of OP-2 / OP-24. Functional status classes follow the classification
  scheme of ISO 16750-1 (functional status classification) as used by ISO 16750-2 (electrical
  loads): class A full function, class B reduced function with automatic recovery, class C loss of
  function with automatic recovery, class D loss of function requiring a reset. The 200 ms recovery
  keeps a supply dip below the 300 ms FTTI of SG-01. Plausible example values.
---

## Context

Hardware requirement from the phase 6 refinement of the E/E architecture (HWE.1 / HWE.2).
Derivation: [`analysis_supply_and_transients.md`](analysis_supply_and_transients.md).
Verification entry: [`hw_verification_plan.md`](hw_verification_plan.md). Test cases are a hand-off
to `verification-engineer`.
