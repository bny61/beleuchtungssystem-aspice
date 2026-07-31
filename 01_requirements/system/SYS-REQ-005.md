---
id: SYS-REQ-005
text: >
  While the vehicle speed signal exceeds 10 km/h, the lighting ECU shall inhibit energising of the work-lamp output stages.
type: functional
asil: A
source: CR-004
derived_from: [CR-004, FSR-008]
allocated_to: [ECU_LightingCtrl, SWC_WorkLampControl]
verified_by: []
status: draft
rationale: >
  ASIL from SG-02, hazard H-03. Threshold from CR-004.
---

## Context

System requirement from phase 3 (ASPICE SYS.2). Allocation to HW / SW / system measures see
[`../../04_architecture/ee_architecture.md`](../../04_architecture/ee_architecture.md).
