---
id: SYS-REQ-020
text: >
  The lighting ECU shall exchange light request, vehicle speed, steering angle, ambient brightness, object data and lighting status with the vehicle gateway via CAN FD according to SAE J1939.
type: communication
asil: B
source: CR-020
derived_from: [CR-020]
allocated_to: [ECU_LightingCtrl, Vehicle_Gateway]
verified_by: []
status: draft
rationale: >
  Carries signals used by safety functions; ASIL inherited from the highest function using them (SG-01, B). Signal detail in the interface table.
---

## Context

System requirement from phase 3 (ASPICE SYS.2). Allocation to HW / SW / system measures see
[`../../04_architecture/ee_architecture.md`](../../04_architecture/ee_architecture.md).
