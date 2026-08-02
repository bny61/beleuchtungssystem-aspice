---
id: HW-REQ-026
text: >
  When the microcontroller enable signal of a low-beam channel becomes active while neither SAFE_OFF
  nor OV_SHUTDOWN is active, the enable gate shall present the effective enable signal at the input
  of the LED driver stage within 1 ms.
type: electrical
asil: B
source: SYS-REQ-001
derived_from: [SYS-REQ-001]
allocated_to: [LED_Driver_Stage_1, MCU_Lockstep]
verified_by: []
status: draft
rationale: >
  HW-REQ-019 specifies the enable gate only in the de-energising direction (10 ms after SAFE_OFF or
  OV_SHUTDOWN). The energising direction carries the activation latency of SYS-REQ-001 and was
  unspecified. 1 ms covers gate propagation, level shifting and the driver enable input filter with
  margin; it is the first term of the 25 ms hardware share of the activation budget in
  analysis_low_beam_activation.md. Plausible example value.
---

## Context

Hardware requirement from the refinement of `SYS-REQ-001` (low-beam activation). Analysis and
derivation: [`analysis_low_beam_activation.md`](analysis_low_beam_activation.md). Complements
`HW-REQ-019`, whose published 10 ms de-energising value is **unchanged**. Verification entry:
`HV-13` in [`hw_verification_plan.md`](hw_verification_plan.md). Test cases are a hand-off to
`verification-engineer`.

**The 300 ms of `SYS-REQ-001` is an activation latency, not the 300 ms FTTI of `SG-01`.** The two
figures are numerically equal and unrelated.
