---
id: SYS-REQ-023
text: >
  If the alive counter of a received safety-relevant signal group does not increase by one modulo
  its range, or if the received checksum does not match the checksum recomputed over the payload,
  the lighting ECU shall mark that signal group as invalid within one reception cycle.
type: communication
asil: B
source: SYS-REQ-022
derived_from: [SYS-REQ-022]
allocated_to: [ECU_LightingCtrl, SWC_LightManager]
verified_by: []
status: draft
rationale: >
  Detection rule belonging to the protection of SYS-REQ-022. "Within one reception cycle" makes the
  detection latency bounded and testable; a tolerance of repeated counters is deliberately not
  granted, because the receiving functions all run slower than the transmit cycle.
---

## Context

The reaction to an invalid signal group is function-specific and is not part of this requirement:
low beam see `SYS-REQ-025`, work-lamp inhibit see `TSR-008`, high-beam monitor see `TSR-007`.
