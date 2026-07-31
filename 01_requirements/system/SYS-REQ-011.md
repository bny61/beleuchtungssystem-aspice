---
id: SYS-REQ-011
text: >
  While exactly one low-beam channel is classified as failed, the lighting ECU shall continue to operate the remaining channel at its commanded set point.
type: functional
asil: B
source: CR-008
derived_from: [CR-008, FSR-003]
allocated_to: [ECU_LightingCtrl, LED_Driver_Stage_1]
verified_by: []
status: draft
rationale: >
  Realises the safe state of SG-01. Presumes freedom from interference between the channels, to be demonstrated by the DFA in phase 5.
---

## Context

System requirement from phase 3 (ASPICE SYS.2). Allocation to HW / SW / system measures see
[`../../04_architecture/ee_architecture.md`](../../04_architecture/ee_architecture.md).
