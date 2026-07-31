---
id: HW-REQ-004
text: >
  Where the commanded PWM on-time of a low-beam channel is shorter than 150 us, the LED driver
  stage shall insert a diagnostic measurement window of at least 200 us at the commanded set point
  at intervals of not more than 10 ms.
type: electrical
asil: B
source: SYS-REQ-017
derived_from: [SYS-REQ-017]
allocated_to: [LED_Driver_Stage_1, SM-01]
verified_by: []
status: draft
rationale: >
  Below the minimum usable on-time no valid sample exists. Either this window or the
  "diagnosis not available" path of SYS-REQ-017 must apply; reuse of a stale sample would make the
  detection time unbounded. Plausible example values.
---

## Context

Hardware requirement from the phase 3 refinement of SYS-REQ-014. Analysis and derivation:
[`analysis_current_sensing.md`](analysis_current_sensing.md). New test cases are a handoff to
`verification-engineer`.
