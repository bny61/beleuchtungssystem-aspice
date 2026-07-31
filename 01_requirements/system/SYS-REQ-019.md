---
id: SYS-REQ-019
text: >
  When the measured load current of a low-beam channel falls below 150 mA, the lighting ECU shall
  classify the cause as exactly one of "open load", "short-to-battery" or "commanded current
  reduction" before triggering a fault reaction.
type: diagnostics
asil: B
source: SYS-REQ-014
derived_from: [SYS-REQ-014]
allocated_to: [ECU_LightingCtrl, SWC_LightManager]
verified_by: []
status: draft
rationale: >
  A single current threshold cannot separate these causes. Short-to-battery reads as open load, and
  a commanded reduction through thermal derating is not a fault at all. Implementation-free - the
  means are specified in HW-REQ-006 and HW-REQ-007.
---

## Context

Does not cover partial string failure: with a constant-current driver that fault is invisible in the
current domain, see the analysis document.
