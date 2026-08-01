---
id: HW-REQ-021
text: >
  The LED driver stage shall limit the channel output current to 1.8 A, shall latch the channel off
  within 5 ms if the limit is active continuously, and shall report the event in DriverStatus within
  10 ms.
type: electrical
asil: B
source: FSR-002
derived_from: [FSR-002, TSR-002, HW-REQ-007]
allocated_to: [LED_Driver_Stage_1, SM-04]
verified_by: []
status: draft
rationale: >
  Owning requirement of SM-04. 1.8 A is 1.5 times the 1.20 A nominal set point (A-08) and therefore
  above every regulated operating case including the inrush of the output capacitance, and below
  the pulse rating of the output stage. The latch-off protects the harness on a short to ground;
  the status report is what makes the event visible to the fault reaction rather than a silent
  channel loss. Plausible example values.
---

## Context

Hardware requirement from the phase 6 refinement of the E/E architecture (HWE.1 / HWE.2).
Owning requirement of `SM-04`. Architecture: [`hw_architecture.md`](hw_architecture.md).
Verification entry: [`hw_verification_plan.md`](hw_verification_plan.md). Test cases are a
hand-off to `verification-engineer`.
