---
id: SYS-REQ-006
text: >
  When the steering angle signal exceeds 15 degrees, the lighting ECU shall activate the cornering light of the corresponding side within 200 ms.
type: functional
asil: A
source: CR-005
derived_from: [CR-005]
allocated_to: [ECU_LightingCtrl, LED_Driver_Stage_1]
verified_by: []
status: draft
rationale: >
  Split out of the deliberately weak CR-005, without the solution prescription. ASIL from SG-02, hazard H-07.
---

## Context

System requirement from phase 3 (ASPICE SYS.2). Allocation to HW / SW / system measures see
[`../../04_architecture/ee_architecture.md`](../../04_architecture/ee_architecture.md).
