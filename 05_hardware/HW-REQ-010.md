---
id: HW-REQ-010
text: >
  The microcontroller shall verify the plausibility of the analogue-to-digital converter reference
  used for the low-beam current measurement against an independent reference at intervals of not
  more than 100 ms.
type: diagnostics
asil: B
source: FSR-001
derived_from: [FSR-001, HW-REQ-001]
allocated_to: [ECU_LightingCtrl, SM-01]
verified_by: []
status: draft
rationale: >
  Reference drift is a gain-type error that shifts the effective threshold without any other
  symptom. Together with HW-REQ-005 this covers the latent failure modes of the diagnostic path
  itself and is a precondition for the diagnostic coverage claimed by SM-01. Plausible example
  value.
---

## Context

Hardware requirement from the phase 3 refinement of SYS-REQ-014. Analysis and derivation:
[`analysis_current_sensing.md`](analysis_current_sensing.md). New test cases are a handoff to
`verification-engineer`.
