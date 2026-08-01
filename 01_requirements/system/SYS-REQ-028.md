---
id: SYS-REQ-028
text: >
  The lighting ECU shall occupy not more than 1.0 % of the nominal capacity of the CAN FD segment
  to which it is connected with its own transmitted frames, measured over any 100 ms window and
  under any operating condition including the fault reaction.
type: communication
asil: B
source: SYS-REQ-020
derived_from: [SYS-REQ-020]
allocated_to: [ECU_LightingCtrl, CAN_FD_Transceiver]
verified_by: []
status: draft
rationale: >
  Turns the transmit budget of the bus load analysis into a verifiable bound. The bound covers only
  what the ECU controls - its own frames - because the receive traffic is produced by the vehicle
  gateway. The 100 ms window matters: an event-triggered warning frame (SYS-REQ-026) on top of the
  cyclic frames must not create a burst in exactly the fault case in which the bus is needed.
  Calculated worst 100 ms window 0.66 %, long-term average 0.20 % (plausible example values).
---

## Context

Derivation and the assumed background load of other ECUs (`A-14`):
[`../../04_architecture/ee_architecture.md`](../../04_architecture/ee_architecture.md), section
"Bus load and timing analysis".
