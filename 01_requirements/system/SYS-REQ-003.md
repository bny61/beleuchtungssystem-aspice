---
id: SYS-REQ-003
text: >
  When the ambient brightness signal remains above 2000 lx for more than 30 s, the lighting ECU shall switch from low beam to daytime running lights within 2 s.
type: functional
asil: B
source: CR-002
derived_from: [CR-002]
allocated_to: [ECU_LightingCtrl, SWC_LightManager]
verified_by: []
status: draft
rationale: >
  Hysteresis against oscillation at dusk. Switching off the low beam in bright conditions is not safety-relevant; QM.
---

## Context

System requirement from phase 3 (ASPICE SYS.2). Allocation to HW / SW / system measures see
[`../../04_architecture/ee_architecture.md`](../../04_architecture/ee_architecture.md).
