---
id: SYS-REQ-016
text: >
  The lighting ECU shall measure the load current of a low-beam channel with a total uncertainty of
  not more than +/-20 mA at the 150 mA classification threshold, over an ambient temperature range
  of -40 C to +85 C.
type: electrical
asil: B
source: SYS-REQ-014, FSR-001
derived_from: [SYS-REQ-014, FSR-001]
allocated_to: [ECU_LightingCtrl, LED_Driver_Stage_1]
verified_by: []
status: draft
rationale: >
  Makes the 150 mA threshold verifiable. Without a stated uncertainty the threshold cannot be
  tested and the classification is not falsifiable. Value from the tolerance chain, plausible
  example value.
---

## Context

Realised in hardware by HW-REQ-001 and HW-REQ-002.
