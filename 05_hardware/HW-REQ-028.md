---
id: HW-REQ-028
text: >
  When both low-beam channels are enabled by the same light request, the difference between the
  instants at which the two channels reach 95 % of their commanded set point shall not exceed 10 ms.
type: electrical
asil: B
source: SYS-REQ-001
derived_from: [SYS-REQ-001]
allocated_to: [LED_Driver_Stage_1]
verified_by: []
status: draft
rationale: >
  SYS-REQ-001 requires "both low-beam channels" to be energised, which makes the later of the two the
  requirement-relevant instant and leaves the asymmetry unbounded. A visible left/right switch-on
  offset is a perceived quality defect and, above roughly 50 ms, is reported as a lamp fault by
  drivers. 10 ms is a bound on the difference, not an additional budget term: both channels are
  commanded from the same microcontroller register write and both are bounded by HW-REQ-026 and
  HW-REQ-027, so the asymmetry is contained inside the 25 ms hardware share and does not add to it.
  Plausible example value.
---

## Context

Hardware requirement from the refinement of `SYS-REQ-001` (low-beam activation). Analysis and
derivation: [`analysis_low_beam_activation.md`](analysis_low_beam_activation.md), section 3.

Channel-wise independence of the driver stages (`TSR-004`, `HW-REQ-019`) is deliberately **not**
weakened by this requirement: it bounds an observable difference, it does not require a shared
enable path. A common gate would defeat the independence argument of `SG-01`.
Verification entry: `HV-13` in [`hw_verification_plan.md`](hw_verification_plan.md).
