---
id: HW-REQ-002
text: >
  The current sensing of a low-beam channel shall guarantee that a true channel current below
  130 mA is always evaluated as below the classification threshold and that a true channel current
  above 170 mA is never evaluated as below the classification threshold.
type: electrical
asil: B
source: SYS-REQ-016
derived_from: [SYS-REQ-016, HW-REQ-001]
allocated_to: [LED_Driver_Stage_1, Current_Sense_Chain, SM-01]
verified_by: []
status: draft
rationale: >
  Guaranteed-trip and guaranteed-no-trip bands around the 150 mA threshold following from
  HW-REQ-001. The 130 mA to 170 mA indeterminate band is accepted; it is 1.7 % of the nominal
  channel current of 1.2 A (plausible example value).
---

## Context

Hardware requirement from the phase 3 refinement of SYS-REQ-014. Analysis and derivation:
[`analysis_current_sensing.md`](analysis_current_sensing.md). New test cases are a handoff to
`verification-engineer`.
