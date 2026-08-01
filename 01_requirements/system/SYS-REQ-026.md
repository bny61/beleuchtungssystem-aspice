---
id: SYS-REQ-026
text: >
  When the lighting ECU has classified a low-beam channel as failed, it shall transmit the driver
  warning signal group as an event-triggered frame within 20 ms of the classification and
  subsequently with a cyclic repetition of 500 ms.
type: communication
asil: B
source: SYS-REQ-010
derived_from: [SYS-REQ-010, TSR-005]
allocated_to: [ECU_LightingCtrl, CAN_FD_Transceiver, SWC_LightManager]
verified_by: []
status: draft
rationale: >
  TSR-005 fixes only the cyclic repetition. Purely cyclic transmission would put up to one full
  cycle of 500 ms of dead time in front of the warning; the event-triggered first frame removes it
  and gives the 2 s budget of SYS-REQ-010 a margin of more than an order of magnitude. 20 ms is one
  transmit task period plus worst-case queuing delay (plausible example values).
---

## Context

Timing derivation: `04_architecture/ee_architecture.md`, section "Bus load and timing analysis",
chain B.
