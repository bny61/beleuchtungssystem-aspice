---
id: HW-REQ-020
text: >
  When the channel output voltage of a low-beam channel measured during the PWM off-phase exceeds
  3 V for more than 30 ms, the lighting ECU shall classify the channel as "short to battery".
type: diagnostics
asil: B
source: SYS-REQ-019
derived_from: [SYS-REQ-019, TSR-003, HW-REQ-006]
allocated_to: [LED_Driver_Stage_1, ECU_LightingCtrl, SM-03]
verified_by: []
status: draft
rationale: >
  Owning requirement of SM-03. In the off-phase the channel output is pulled low by the driver, so
  any voltage above the divider error band comes from an external source. 3 V is one LED forward
  voltage below the first string node and well above the 100 mV resolution of HW-REQ-006. Detection
  30 ms plus the 150 ms fault reaction of TSR-004 is 180 ms against the 300 ms FTTI of SG-01.
  Plausible example values.
---

## Context

Hardware requirement from the phase 6 refinement of the E/E architecture (HWE.1 / HWE.2).
Owning requirement of `SM-03`. Derivation: [`analysis_current_sensing.md`](analysis_current_sensing.md) section 5.
Verification entry: [`hw_verification_plan.md`](hw_verification_plan.md). Test cases are a
hand-off to `verification-engineer`.
