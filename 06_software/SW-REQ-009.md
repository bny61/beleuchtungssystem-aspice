---
id: SW-REQ-009
text: >
  While the vehicle speed exceeds 10 km/h or the vehicle dynamics signal group is marked invalid,
  SWC_WorkLampControl shall keep the work-lamp output stages de-energised.
type: safety
asil: A
source: TSR-008
derived_from: [TSR-008]
allocated_to: [SWC_WorkLampControl, MCU_Lockstep]
verified_by: []
status: draft
rationale: >
  Direct refinement of TSR-008 including the signal-invalid case, which is the point of the
  requirement: an inhibit that a lost frame can defeat is not an inhibit. Invalidity is supplied by
  SW-REQ-005; this requirement owns only the reaction to it.
---

## Context

📋 **OVERVIEW — SG-02 thread.** Runs in the 10 ms control task. The 10 km/h threshold is published in
`TSR-008` and `SYS-REQ-005` and is used unchanged.
