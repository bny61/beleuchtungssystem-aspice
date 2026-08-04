---
id: SW-REQ-013
text: >
  The lighting ECU software shall execute every safety-relevant runnable on the task schedule
  specified in sw_architecture.md and shall complete the chain from an available open-load
  classification to the commanded safe state within 6 ms.
type: timing
asil: B
source: TSR-004
derived_from: [TSR-003, TSR-004]
allocated_to: [SWC_LightManager, MCU_Lockstep]
verified_by: []
status: draft
rationale: >
  Makes the software share of the SG-01 fault reaction explicit and testable. 6 ms = one 5 ms
  monitoring cycle (state transition and arbitration) + 1 ms actuation write. The remaining channel is
  already energised, so no driver-stage settling time enters the chain. Against the published budget:
  80 ms detection (HW-REQ-009) + 6 ms software + the rest of the 150 ms reaction allocation of TSR-004
  = 230 ms against the 300 ms FTTI of SG-01, unchanged. Plausible example values.
---

## Context

🔍 **DEEP DIVE — Golden Thread.** Full task table, priorities and deadlines:
[`sw_architecture.md`](sw_architecture.md), section on dynamic behaviour. Deadline violations are
detected by OS timing protection and by the deadline supervision of the Watchdog Manager
(`SW-REQ-010`).
