---
id: HW-REQ-025
text: >
  The CAN_FD_Transceiver shall withstand a permanent short of either bus line to the supply voltage
  or to ground without damage and shall release the bus within 5 ms if its transmit input remains
  dominant.
type: interface
asil: B
source: SYS-REQ-020
derived_from: [SYS-REQ-020, FSR-004]
allocated_to: [CAN_FD_Transceiver]
verified_by: []
status: draft
rationale: >
  The driver warning of FSR-004 and the lighting status travel over this bus, so a transceiver that
  babbles takes down the communication of the whole segment including its own warning path. The
  dominant timeout is the standard transceiver-level containment for that failure mode. Plausible
  example value.
---

## Context

Hardware requirement from the phase 6 refinement of the E/E architecture (HWE.1 / HWE.2).
Architecture: [`hw_architecture.md`](hw_architecture.md).
Verification entry: [`hw_verification_plan.md`](hw_verification_plan.md). Test cases are a
hand-off to `verification-engineer`.
