---
id: SYS-REQ-007
text: >
  When the steering angle signal falls below 5 degrees, the lighting ECU shall deactivate the cornering light within 200 ms.
type: functional
asil: A
source: CR-005
derived_from: [CR-005]
allocated_to: [ECU_LightingCtrl, LED_Driver_Stage_1]
verified_by: []
status: draft
rationale: >
  Second statement split out of CR-005.
---

## Context

System requirement from phase 3 (ASPICE SYS.2). Allocation to HW / SW / system measures see
[`../../04_architecture/ee_architecture.md`](../../04_architecture/ee_architecture.md).
