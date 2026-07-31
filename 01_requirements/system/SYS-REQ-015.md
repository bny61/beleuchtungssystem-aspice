---
id: SYS-REQ-015
text: >
  When a low-beam channel is classified as "open load", the lighting ECU shall increment the fault
  counter of that channel.
type: diagnostics
asil: B
source: SYS-REQ-014
derived_from: [SYS-REQ-014]
allocated_to: [ECU_LightingCtrl, SWC_LightManager]
verified_by: []
status: draft
rationale: >
  Split out of SYS-REQ-014 for atomicity - counting is a separate testable statement from
  classifying.
---

## Context

Created with the phase 3 refinement of SYS-REQ-014.
