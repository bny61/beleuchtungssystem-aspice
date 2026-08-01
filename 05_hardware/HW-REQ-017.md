---
id: HW-REQ-017
text: >
  When an internal supply rail leaves its specified tolerance band, the ASIC_Watchdog shall hold
  the microcontroller in reset and assert SAFE_OFF within 5 ms of the deviation.
type: safety
asil: B
source: TSR-001
derived_from: [TSR-001, FSR-002]
allocated_to: [ASIC_Watchdog, Power_Supply_Unit, SM-06]
verified_by: []
status: draft
rationale: >
  A microcontroller running on an out-of-tolerance rail produces arbitrary outputs, including
  arbitrary PWM. Rail monitoring must therefore sit outside the microcontroller. Second owning
  requirement of SM-06 and a precondition for the freedom-from-interference argument of phase 7.
  Plausible example value.
---

## Context

Hardware requirement from the phase 6 refinement of the E/E architecture (HWE.1 / HWE.2).
Owning requirement of `SM-06`. Derivation: [`analysis_supply_and_transients.md`](analysis_supply_and_transients.md).
Verification entry: [`hw_verification_plan.md`](hw_verification_plan.md). Test cases are a
hand-off to `verification-engineer`.
