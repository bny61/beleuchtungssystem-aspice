---
id: SW-REQ-006
text: >
  When SWC_LightManager has classified a low-beam channel as failed, it shall request transmission of
  the driver warning signal group as an event-triggered frame within 20 ms of the classification and
  shall repeat the request cyclically every 500 ms while the classification persists.
type: communication
asil: B
source: SYS-REQ-026
derived_from: [SYS-REQ-026, TSR-005]
allocated_to: [SWC_LightManager, CAN_FD_Transceiver]
verified_by: []
status: draft
rationale: >
  Software refinement of SYS-REQ-026 and TSR-005 with no new value. The 20 ms is met by the 10 ms
  transmit runnable plus the worst-case queuing delay of chain B in the E/E architecture (13 ms
  worst case, specified 20 ms). The warning is outside the FTTI chain of SG-01 — it is a report, not
  the fault reaction — which is why it may sit in the slower task.
---

## Context

📋 **OVERVIEW.** Timing derivation: `04_architecture/ee_architecture.md`, chain B. Transmission is
performed by the COM stack; this requirement owns the request and its repetition, not the frame.
