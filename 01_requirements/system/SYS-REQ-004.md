---
id: SYS-REQ-004
text: >
  When the vehicle gateway reports an oncoming or preceding vehicle, the lighting ECU shall mask the affected high-beam segment within 500 ms.
type: functional
asil: A
source: CR-003
derived_from: [CR-003, FSR-005]
allocated_to: [ECU_LightingCtrl, SWC_HighBeamControl]
verified_by: []
status: draft
rationale: >
  ASIL from SG-02. The object data originate outside the item boundary (A-05).
---

## Context

System requirement from phase 3 (ASPICE SYS.2). Allocation to HW / SW / system measures see
[`../../04_architecture/ee_architecture.md`](../../04_architecture/ee_architecture.md).
