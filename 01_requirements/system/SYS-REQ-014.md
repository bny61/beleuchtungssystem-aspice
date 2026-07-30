---
id: SYS-REQ-014
text: >
  When the load current of a low-beam channel falls below 150 mA for more than 50 ms, the
  lighting ECU shall classify the channel as "open load" and increment the fault counter.
type: functional
asil: B
source: CR-007
derived_from: [CR-007, FSR-001]
allocated_to: [ECU_LightingCtrl, SWC_LightManager, SM-01]
verified_by: [TC-021]
status: reviewed
rationale: >
  Threshold and debounce time derived from the FTTI budget of SG-01
  (150 mA / 50 ms: plausible example values, not validated data).
---

## Context

Reference record for the Requirements-as-Code format. The threshold must be secured against the
spread of the current sensing chain (tolerance analysis).

## Open points

1. Tolerance analysis of the current sensing is open - owner: `hardware-engineer`.
