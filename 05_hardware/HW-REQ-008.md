---
id: HW-REQ-008
text: >
  The thermal derating function of a low-beam channel shall not command a channel set point below
  400 mA while the channel is commanded on.
type: electrical
asil: B
source: SYS-REQ-014
derived_from: [SYS-REQ-014, HW-REQ-002]
allocated_to: [LED_Driver_Stage_1, SM-01]
verified_by: []
status: draft
rationale: >
  A fixed 150 mA threshold stays free of false trips only while the commanded set point exceeds
  191 mA (worst case from HW-REQ-002). 400 mA keeps a factor of 2.3 against the upper indeterminate
  band edge of 170 mA. Without this floor, normal derating produces a spurious safe-state
  transition. Plausible example values. Assumption A-12.
---

## Context

Hardware requirement from the phase 3 refinement of SYS-REQ-014. Analysis and derivation:
[`analysis_current_sensing.md`](analysis_current_sensing.md). New test cases are a handoff to
`verification-engineer`.
