---
id: SYS-REQ-018
text: >
  When an open load occurs in a low-beam channel, the lighting ECU shall report the fault to the
  fault reaction within 100 ms of fault occurrence.
type: safety
asil: B
source: SYS-REQ-014, FSR-001
derived_from: [SYS-REQ-014, FSR-001]
allocated_to: [ECU_LightingCtrl, SM-01]
verified_by: []
status: draft
rationale: >
  Makes the detection budget explicit and testable. 100 ms is the allocated cap; the worst-case
  design value is 80 ms (HW-REQ-009). With the 150 ms fault reaction time of SG-01 the total stays
  below the 300 ms FTTI under any implementation variant.
---

## Context

The cap, not the design value, is the requirement - it leaves the implementation room while keeping
the FTTI argument valid.
