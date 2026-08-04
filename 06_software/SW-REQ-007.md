---
id: SW-REQ-007
text: >
  When a valid object list is received, SWC_HighBeamControl shall determine the high-beam segments to
  be masked from the object positions and shall command the corresponding LED driver segments within
  one 50 ms control cycle.
type: functional
asil: QM(A)
source: TSR-006
derived_from: [TSR-006]
allocated_to: [SWC_HighBeamControl, LED_Driver_Stage_1]
verified_by: []
status: draft
rationale: >
  QM(A) path of the decomposition of FSR-005; the ASIL is inherited from TSR-006 and is not raised by
  the software. The 50 ms cycle matches the ObjectList transmit cycle of the interface table — running
  faster would only re-evaluate identical data. Admissible only together with SW-REQ-008 and the
  freedom-from-interference argument in freedom_from_interference.md; RISK-02 stays open until the
  phase 5 DFA. Plausible example value.
---

## Context

📋 **OVERVIEW — SG-02 thread**, deliberately shallower than the SG-01 thread. This component sits in
the QM partition; the partitioning argument is in
[`../06_software/freedom_from_interference.md`](freedom_from_interference.md).
