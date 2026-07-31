---
id: HW-REQ-006
text: >
  The LED driver stage shall provide the channel output voltage to the microcontroller as a
  measured value in both the PWM on-phase and the PWM off-phase, with a resolution of at least
  100 mV over a range of 0 V to 40 V.
type: electrical
asil: B
source: SYS-REQ-019
derived_from: [SYS-REQ-019]
allocated_to: [LED_Driver_Stage_1, SM-01]
verified_by: []
status: draft
rationale: >
  The off-phase channel voltage separates short-to-battery from open load; the on-phase channel
  voltage is the only signature of a parallel-string loss, which a constant-current driver renders
  invisible in the current domain. 100 mV resolves a single LED forward voltage step of about 3.2 V
  with large margin. Plausible example values.
---

## Context

Hardware requirement from the phase 3 refinement of SYS-REQ-014. Analysis and derivation:
[`analysis_current_sensing.md`](analysis_current_sensing.md). New test cases are a handoff to
`verification-engineer`.
