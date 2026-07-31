---
id: HW-REQ-007
text: >
  The LED driver stage shall provide its over-voltage, over-current and over-temperature status to
  the microcontroller as a readable signal with an update interval of not more than 10 ms.
type: interface
asil: B
source: SYS-REQ-019
derived_from: [SYS-REQ-019]
allocated_to: [LED_Driver_Stage_1, ECU_LightingCtrl, SM-01]
verified_by: []
status: draft
rationale: >
  Driver-internal fault classes are not observable at the shunt. Contributes to the diagnostic
  coverage claimed by SM-01. Assumption A-10.
---

## Context

Hardware requirement from the phase 3 refinement of SYS-REQ-014. Analysis and derivation:
[`analysis_current_sensing.md`](analysis_current_sensing.md). New test cases are a handoff to
`verification-engineer`.
