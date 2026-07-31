---
id: SYS-REQ-002
text: >
  When the ambient brightness signal remains below 1000 lx for more than 3 s, the lighting ECU shall switch from daytime running lights to low beam within 500 ms.
type: functional
asil: B
source: CR-002
derived_from: [CR-002, FSR-002]
allocated_to: [ECU_LightingCtrl, SWC_LightManager]
verified_by: []
status: draft
rationale: >
  Quantifies the deliberately weak CR-002. Threshold, debounce and switching time are plausible example values; the hysteresis for switching back is SYS-REQ-003.
---

## Context

System requirement from phase 3 (ASPICE SYS.2). Allocation to HW / SW / system measures see
[`../../04_architecture/ee_architecture.md`](../../04_architecture/ee_architecture.md).
