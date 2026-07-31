---
id: HW-REQ-005
text: >
  The current sensing of a low-beam channel shall evaluate the measured current during the PWM
  off-phase and shall signal a current-sensing fault if the measured value exceeds 30 mA in the
  off-phase for more than 20 ms.
type: diagnostics
asil: B
source: FSR-001
derived_from: [FSR-001, SYS-REQ-014]
allocated_to: [ECU_LightingCtrl, Current_Sense_Chain, SM-01]
verified_by: []
status: draft
rationale: >
  The off-phase is a known-zero reference and therefore a stuck-at-high and offset-drift test of
  shunt, amplifier and ADC at no extra cost. Precondition for the diagnostic coverage claimed by
  SM-01; without it a sensing fault is latent and masks the open load. 30 mA is the offset band of
  HW-REQ-001 with margin (plausible example value).
---

## Context

Hardware requirement from the phase 3 refinement of SYS-REQ-014. Analysis and derivation:
[`analysis_current_sensing.md`](analysis_current_sensing.md). New test cases are a handoff to
`verification-engineer`.
