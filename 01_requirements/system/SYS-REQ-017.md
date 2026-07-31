---
id: SYS-REQ-017
text: >
  While the PWM on-time of a low-beam channel is shorter than 150 us, the lighting ECU shall report
  the open-load diagnosis of that channel as "not available".
type: diagnostics
asil: B
source: SYS-REQ-014
derived_from: [SYS-REQ-014]
allocated_to: [ECU_LightingCtrl, SWC_LightManager]
verified_by: []
status: draft
rationale: >
  Below the minimum usable on-time no valid sample exists. Reusing the last valid sample would make
  the detection time unbounded, which cannot be argued against the FTTI. Plausible example value.
---

## Context

Alternative to HW-REQ-004 (forced diagnostic window). Which of the two applies is a system-level
decision - see open point in the analysis document.
