---
id: SW-REQ-005
text: >
  When a safety-relevant signal group is received, SWC_LightManager shall verify its alive counter,
  its checksum computed over the signal-group data identifier and the payload, and its reception
  timeout, and shall mark the signal group invalid within one reception cycle if any of the three
  checks fails.
type: communication
asil: B
source: SYS-REQ-022
derived_from: [SYS-REQ-022, SYS-REQ-023, SYS-REQ-024, SYS-REQ-027]
allocated_to: [SWC_LightManager, CAN_FD_Transceiver, MCU_Lockstep]
verified_by: []
status: draft
rationale: >
  Collects the four end-to-end system requirements into one software requirement, because in the
  implementation they are one check performed at one place: the E2E library call in the reception
  runnable. Profile (4-bit alive counter, CRC-8, 16-bit data identifier) and the timeout per group are
  taken from the message catalogue of the E/E architecture and are not restated here, so that they
  stay maintained in one place. The counterpart in the vehicle gateway is outside the item boundary
  (A-15, OP-28).
---

## Context

📋 **OVERVIEW.** Applies to `SG_LightRequest`, `SG_VehicleDynamics`, `SG_Environment`,
`SG_LightingStatus` and `SG_DriverWarning`. `ObjectList` is deliberately **not** covered: it is QM(A)
and carries a timeout and per-object valid flag only, per the interface table of
`04_architecture/ee_architecture.md`. The reaction to an invalid group is function-specific:
`SW-REQ-004` for the low beam, `SW-REQ-009` for the work lamps, `SW-REQ-008` for the high-beam
monitor.
