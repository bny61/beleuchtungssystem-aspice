---
id: HW-REQ-009
text: >
  The hardware detection path of the low-beam open-load mechanism shall report a detected open load
  to the software fault reaction within 80 ms of the occurrence of the fault.
type: safety
asil: B
source: SYS-REQ-018
derived_from: [SYS-REQ-018, FSR-001]
allocated_to: [ECU_LightingCtrl, SM-01]
verified_by: []
status: draft
rationale: >
  2.5 ms PWM synchronisation + 0.1 ms acquisition + 50 ms threshold window + 20 ms debounce + 5 ms
  task latency = 77.6 ms. With the 150 ms fault reaction time of SG-01 the total is 230 ms against
  an FTTI of 300 ms, margin 70 ms (23 %). Plausible example values.
---

## Context

Hardware requirement from the phase 3 refinement of SYS-REQ-014. Analysis and derivation:
[`analysis_current_sensing.md`](analysis_current_sensing.md). New test cases are a handoff to
`verification-engineer`.
