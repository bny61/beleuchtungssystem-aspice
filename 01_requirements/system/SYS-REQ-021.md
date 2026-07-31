---
id: SYS-REQ-021
text: >
  When a diagnostic tester sends a UDS request according to ISO 14229, the lighting ECU shall provide the stored diagnostic trouble codes within 100 ms.
type: diagnostics
asil: QM
source: CR-019
derived_from: [CR-019]
allocated_to: [ECU_LightingCtrl]
verified_by: []
status: draft
rationale: >
  Reading the fault memory is not part of the safety chain; the safety-relevant warning path is SYS-REQ-010. QM.
---

## Context

System requirement from phase 3 (ASPICE SYS.2). Allocation to HW / SW / system measures see
[`../../04_architecture/ee_architecture.md`](../../04_architecture/ee_architecture.md).
