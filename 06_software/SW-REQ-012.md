---
id: SW-REQ-012
text: >
  When a diagnostic tester sends a UDS request, SWC_DiagnosticManager shall answer within 100 ms with
  the diagnostic trouble codes stored for the lighting functions.
type: diagnostics
asil: QM
source: SYS-REQ-021
derived_from: [SYS-REQ-021]
allocated_to: [SWC_DiagnosticManager, CAN_FD_Transceiver]
verified_by: []
status: draft
rationale: >
  Refinement of SYS-REQ-021; QM inherited, because reading the fault memory is not part of the safety
  chain. The DTC content is produced by the ASIL B components and only stored and served here — the QM
  component is deliberately not in the data path of any safety function, which is the same argument the
  allocation table already makes for the communication functions.
---

## Context

📋 **OVERVIEW.** Runs in the background task at the lowest priority, in its own OS-Application. The
DTC set for the Golden Thread (open load, short-to-battery, derating active) is listed in
[`sw_architecture.md`](sw_architecture.md).
