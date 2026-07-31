---
id: SYS-REQ-013
text: >
  While the vehicle supply voltage is between 9 V and 16 V, the lighting ECU shall keep the low beam energised at a reduced set point of at least 400 mA per channel and shall set a diagnostic trouble code.
type: electrical
asil: B
source: CR-016
derived_from: [CR-016, FSR-003]
allocated_to: [ECU_LightingCtrl, LED_Driver_Stage_1]
verified_by: []
status: draft
rationale: >
  Closes open point OP-2: undervoltage behaviour was undefined. The 400 mA floor is the derating floor of HW-REQ-008, so the open-load threshold stays valid. Plausible example values.
---

## Context

System requirement from phase 3 (ASPICE SYS.2). Allocation to HW / SW / system measures see
[`../../04_architecture/ee_architecture.md`](../../04_architecture/ee_architecture.md).
