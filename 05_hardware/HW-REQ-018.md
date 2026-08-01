---
id: HW-REQ-018
text: >
  The ASIC_Watchdog shall run a question/answer protocol on a time base independent of the
  microcontroller clock and shall assert SAFE_OFF within 50 ms of the first missing or incorrect
  answer.
type: safety
asil: B
source: TSR-001
derived_from: [TSR-001]
allocated_to: [ASIC_Watchdog, MCU_Lockstep, SM-02]
verified_by: []
status: draft
rationale: >
  Owning requirement of SM-02. Window/question-answer watchdog rather than a simple timeout,
  because a stuck task that still toggles a pin satisfies a timeout watchdog. The independent time
  base is what makes the mechanism valid against a clock fault, which the lockstep core cannot
  cover. Detection 50 ms plus reaction 10 ms (HW-REQ-019) is inside the 300 ms FTTI of SG-01.
  Plausible example value.
---

## Context

Hardware requirement from the phase 6 refinement of the E/E architecture (HWE.1 / HWE.2).
Owning requirement of `SM-02`. Architecture: [`hw_architecture.md`](hw_architecture.md).
Verification entry: [`hw_verification_plan.md`](hw_verification_plan.md). Test cases are a
hand-off to `verification-engineer`.
