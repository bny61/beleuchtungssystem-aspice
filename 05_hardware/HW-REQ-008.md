---
id: HW-REQ-008
text: >
  The thermal derating function of a low-beam channel shall not command a channel set point below
  400 mA while the channel is commanded on.
type: electrical
asil: B
source: SYS-REQ-014
derived_from: [SYS-REQ-014, HW-REQ-002]
allocated_to: [LED_Driver_Stage_1, SM-01]
verified_by: []
status: draft
rationale: >
  A fixed 150 mA threshold stays free of false trips only while the commanded set point exceeds
  191 mA (worst case from HW-REQ-002). 400 mA keeps a factor of 2.3 against the upper indeterminate
  band edge of 170 mA. Without this floor, normal derating produces a spurious safe-state
  transition. Plausible example values. Assumption A-12.
---

## Context

Hardware requirement from the phase 3 refinement of SYS-REQ-014. Analysis and derivation:
[`analysis_current_sensing.md`](analysis_current_sensing.md). New test cases are a handoff to
`verification-engineer`.

## Confirmation note (phase 6, hardware-engineer) — closes `OP-16`

**The 400 mA floor is confirmed against the LED module thermal design; the value is unchanged and
no change note on the requirement is needed.** Load-line evaluation in
[`analysis_thermal_derating.md`](analysis_thermal_derating.md): in the two realistic thermal cases
the derating loop settles at 733 mA and 476 mA and never reaches the floor. The floor is reached
only with a heat path degraded to twice its nominal thermal resistance at a headlamp cavity
temperature of 105 °C, and there the junction settles at about 130 °C — 5 K below the 135 °C design
limit and 20 K below the 150 °C component rating (plausible example values).

The condition under which this holds is now an explicit requirement, `HW-REQ-024`. Assumption `A-12`
therefore stays open but is no longer unsupported; its validation target is the DV thermal test
`HV-05`. The photometric consequence of the floor (about 232 lm per channel) is a system-level
question and is handed to `systems-engineer`.
