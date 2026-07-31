---
id: SYS-REQ-010
text: >
  When the lighting ECU has classified a low-beam channel as failed, it shall request the driver warning via the vehicle gateway within 2 s of the classification.
type: functional
asil: B
source: CR-007
derived_from: [CR-007, FSR-004]
allocated_to: [ECU_LightingCtrl, Vehicle_Gateway]
verified_by: []
status: draft
rationale: >
  The 2 s are the customer requirement and lie outside the fault reaction budget of SG-01.
---

## Context

System requirement from phase 3 (ASPICE SYS.2). Allocation to HW / SW / system measures see
[`../../04_architecture/ee_architecture.md`](../../04_architecture/ee_architecture.md).
