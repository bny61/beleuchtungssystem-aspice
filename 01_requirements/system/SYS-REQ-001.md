---
id: SYS-REQ-001
text: >
  When the driver requests low beam via the light switch signal, the lighting ECU shall energise both low-beam channels within 300 ms.
type: functional
asil: B
source: CR-001
derived_from: [CR-001, FSR-002]
allocated_to: [ECU_LightingCtrl, SWC_LightManager, LED_Driver_Stage_1]
verified_by: []
status: draft
rationale: >
  Response time taken from CR-001. ASIL from SG-01: the low beam is the safety-relevant function.
---

## Context

System requirement from phase 3 (ASPICE SYS.2). Allocation to HW / SW / system measures see
[`../../04_architecture/ee_architecture.md`](../../04_architecture/ee_architecture.md).
