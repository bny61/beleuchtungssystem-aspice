---
id: HW-REQ-027
text: >
  When the effective enable signal of a low-beam channel becomes active, the LED driver stage shall
  raise the channel current from 0 mA to at least 95 % of the commanded set point within 20 ms, with
  a monotonic current ramp of not less than 5 ms duration.
type: electrical
asil: B
source: SYS-REQ-001
derived_from: [SYS-REQ-001, HW-REQ-026]
allocated_to: [LED_Driver_Stage_1]
verified_by: []
status: draft
rationale: >
  Two-sided requirement. The upper bound of 20 ms is the dominant hardware term of the activation
  budget of SYS-REQ-001 (analysis_low_beam_activation.md section 3). The lower bound of 5 ms is a
  soft-start floor: an unlimited ramp on a constant-current buck driving 1.20 A into 12 LEDs plus the
  output capacitance produces an inrush the supply has to absorb (HW-REQ-029) and an audible and
  optically abrupt switch-on. 95 % of set point is the photometric acceptance point; the remaining
  regulation settles inside the same window. Plausible example values.
---

## Context

Hardware requirement from the refinement of `SYS-REQ-001` (low-beam activation). Analysis and
derivation: [`analysis_low_beam_activation.md`](analysis_low_beam_activation.md).

The ramp mandated here is what makes `HW-REQ-030` necessary: during the ramp the channel current is
below the 150 mA open-load threshold of `HW-REQ-001` / `HW-REQ-002` by design, so `SM-01` has to be
blanked over the transient. Verification entries: `HV-13` and `HV-14` in
[`hw_verification_plan.md`](hw_verification_plan.md).
