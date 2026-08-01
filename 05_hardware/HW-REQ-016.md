---
id: HW-REQ-016
text: >
  When the protected supply voltage leaves the range 9 V to 36 V, the supply monitor of the
  Power_Supply_Unit shall signal the condition to the microcontroller within 10 ms, and when it
  exceeds 60 V the supply monitor shall de-energise the LED driver stages via the enable gate
  within 1 ms.
type: safety
asil: B
source: FSR-002
derived_from: [FSR-002, SYS-REQ-012, TSR-001]
allocated_to: [Power_Supply_Unit, LED_Driver_Stage_1, SM-06]
verified_by: []
status: draft
rationale: >
  Owning requirement of SM-06 on the supply side. Two-stage response: a reported condition inside
  the operating envelope (software derates or sets a DTC) and a hardware shutdown above the
  component rating of the driver output stage, which cannot wait for software. The 60 V threshold
  lies above the 58 V clamped load-dump level that HW-REQ-013 requires the ECU to ride through and
  below the 65 V rating assumed for the output stage, so a load dump does not switch the low beam
  off. Detection 10 ms plus
  reaction 1 ms is far inside the 300 ms FTTI of SG-01. Plausible example values.
---

## Context

Hardware requirement from the phase 6 refinement of the E/E architecture (HWE.1 / HWE.2).
Owning requirement of `SM-06`. Derivation: [`analysis_supply_and_transients.md`](analysis_supply_and_transients.md).
Verification entry: [`hw_verification_plan.md`](hw_verification_plan.md). Test cases are a
hand-off to `verification-engineer`.
