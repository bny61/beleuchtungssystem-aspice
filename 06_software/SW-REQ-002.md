---
id: SW-REQ-002
text: >
  When the measured load current of an energised and un-blanked low-beam channel remains below
  150 mA for more than 50 ms, SWC_LightManager shall classify the channel after a debounce of 20 ms
  and shall assign exactly one cause out of "open load", "short-to-battery" and "commanded current
  reduction" before it requests a fault reaction.
type: safety
asil: B
source: TSR-003
derived_from: [TSR-003, SYS-REQ-014, SYS-REQ-019]
allocated_to: [SWC_LightManager, SM-01, Current_Sense_Chain]
verified_by: []
status: draft
rationale: >
  Software side of SM-01. Threshold, window and debounce are taken unchanged from SYS-REQ-014 and
  SM-01, not re-derived. The cause discrimination uses U_Channel (HW-REQ-006, SM-03) and the driver
  status readback (HW-REQ-007) together with the internally known derating set point, because a
  single current threshold cannot separate the three causes (SYS-REQ-019). "Un-blanked" refers to the
  30 ms switch-on blanking of HW-REQ-030; the consequence for the start-up case is OP-42 and is not
  reinterpreted here. Plausible example values.
---

## Context

🔍 **DEEP DIVE — Golden Thread.** Evaluation path, state machine and pseudocode:
[`detailed_design/swc_lightmanager.md`](detailed_design/swc_lightmanager.md). This requirement
consumes no additional time in the SG-01 budget: the 50 ms window, the 20 ms debounce and the 5 ms
task latency are the terms of `HW-REQ-009`.
