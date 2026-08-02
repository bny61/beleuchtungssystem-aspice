---
id: HW-REQ-029
text: >
  When both low-beam channels are switched on simultaneously at a supply voltage within 18 V to 32 V,
  the current drawn at the supply input shall not exceed 8 A at any instant, and the protected supply
  voltage VBAT_PROT shall not drop by more than 1 V below its pre-switch-on value.
type: electrical
asil: B
source: SYS-REQ-001
derived_from: [SYS-REQ-001, HW-REQ-027]
allocated_to: [Power_Supply_Unit, LED_Driver_Stage_1]
verified_by: []
status: draft
rationale: >
  Steady-state draw of two low-beam channels is roughly 2 x 1.20 A x 12 x 3.2 V / (24 V x 0.9) ~ 4.3 A
  at the input. The 8 A cap allows a factor of about 1.9 for the charging of the driver output
  capacitance during the soft-start ramp of HW-REQ-027 and is the sizing input for the input filter
  and the buffered rail. The 1 V dip limit is the coupling to SM-06: an unbounded switch-on dip could
  cross the 9 V undervoltage threshold of HW-REQ-016 at a low supply and produce a self-inflicted
  safe-state transition at the very moment the driver asks for light. Plausible example values.
---

## Context

Hardware requirement from the refinement of `SYS-REQ-001` (low-beam activation). Analysis and
derivation: [`analysis_low_beam_activation.md`](analysis_low_beam_activation.md), section 5.

No value of `SM-06`, `HW-REQ-011` or `HW-REQ-016` is changed by this record — it constrains the
disturbance, not the monitor. The lower bound of the stated voltage range is 18 V rather than the
9 V of `HW-REQ-011` because the inrush limit is a design-load statement for the nominal 24 V
bordnetz; behaviour below 18 V is governed by the functional status classes of `HW-REQ-012`.
Verification entry: `HV-14` in [`hw_verification_plan.md`](hw_verification_plan.md).
