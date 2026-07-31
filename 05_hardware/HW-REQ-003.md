---
id: HW-REQ-003
text: >
  The analogue-to-digital conversion of the low-beam channel current shall be triggered by the PWM
  timer unit of the LED driver stage, with a sampling instant inside the PWM on-phase not earlier
  than 50 us after the rising edge and not later than 20 us before the falling edge.
type: electrical
asil: B
source: SYS-REQ-014
derived_from: [SYS-REQ-014]
allocated_to: [ECU_LightingCtrl, LED_Driver_Stage_1, SM-01]
verified_by: []
status: draft
rationale: >
  Blanking covers driver current rise (20 us), sense amplifier settling (15 us), filter group delay
  (8 us) and switching-edge ringing (10 us). A software trigger cannot guarantee the phase
  relationship under interrupt load, and a phase error of one on-time is a 100 % measurement error.
  Plausible example values. Assumption A-09.
---

## Context

Hardware requirement from the phase 3 refinement of SYS-REQ-014. Analysis and derivation:
[`analysis_current_sensing.md`](analysis_current_sensing.md). New test cases are a handoff to
`verification-engineer`.
