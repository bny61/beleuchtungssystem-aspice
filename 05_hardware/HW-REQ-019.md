---
id: HW-REQ-019
text: >
  The enable input of each LED driver stage shall be driven by the logical conjunction of the
  microcontroller enable signal and the negated SAFE_OFF and OV_SHUTDOWN signals, and shall bring
  the channel into its de-energised state within 10 ms of SAFE_OFF or OV_SHUTDOWN becoming active.
type: electrical
asil: B
source: TSR-001
derived_from: [TSR-001, TSR-004]
allocated_to: [LED_Driver_Stage_1, ASIC_Watchdog, SM-02]
verified_by: []
status: draft
rationale: >
  Defines the topology of the disable path: SAFE_OFF is dominant, so a hung microcontroller that
  holds its enable signal active cannot prevent de-energisation, and the path contains no software.
  Realised per channel so that the channel-wise independence assumed by SYS-REQ-011 is not defeated
  by a shared gate. Plausible example value.
---

## Context

Hardware requirement from the phase 6 refinement of the E/E architecture (HWE.1 / HWE.2).
Owning requirement of `SM-02` (disable path topology). Architecture: [`hw_architecture.md`](hw_architecture.md).
Verification entry: [`hw_verification_plan.md`](hw_verification_plan.md). Test cases are a
hand-off to `verification-engineer`.
