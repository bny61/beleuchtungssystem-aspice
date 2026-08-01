---
id: SYS-REQ-022
text: >
  The lighting ECU shall protect every safety-relevant signal group exchanged with the vehicle
  gateway with an alive counter and a checksum computed over the payload of that signal group.
type: communication
asil: B
source: CR-020
derived_from: [CR-020, SYS-REQ-020]
allocated_to: [ECU_LightingCtrl, CAN_FD_Transceiver, SWC_LightManager, Vehicle_Gateway]
verified_by: []
status: draft
rationale: >
  SYS-REQ-020 fixed the transport (CAN FD / SAE J1939) but not the data integrity. A bus signal
  that carries an ASIL B function needs protection against loss, repetition, insertion, incorrect
  sequence and corruption; a timeout alone covers only loss. Counter plus checksum is the minimum
  set. The concrete profile (4-bit alive counter, CRC-8, data identifier) is fixed in the message
  catalogue of the E/E architecture and is a plausible example value.
---

## Context

Created with the phase 3 refinement of the E/E architecture (open point `OP-21` / `OP-22`).
Signal groups, data identifiers and the byte position of counter and checksum:
[`../../04_architecture/ee_architecture.md`](../../04_architecture/ee_architecture.md), section
"Message catalogue".

The receiver-side counterpart in the vehicle gateway is outside the item boundary and is covered by
assumption `A-15`; it is part of the interface agreement tracked as `OP-10`.
