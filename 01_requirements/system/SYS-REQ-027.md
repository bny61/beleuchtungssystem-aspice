---
id: SYS-REQ-027
text: >
  The lighting ECU shall include a signal-group-specific data identifier in the checksum
  computation of every safety-relevant signal group, and shall use a different data identifier for
  each signal group.
type: communication
asil: B
source: SYS-REQ-022
derived_from: [SYS-REQ-022]
allocated_to: [ECU_LightingCtrl, SWC_LightManager]
verified_by: []
status: draft
rationale: >
  Without a data identifier in the checksum, a correctly formed frame delivered to the wrong
  identifier - a masquerade or a mis-routed frame in the gateway - passes the counter and checksum
  check. The identifier is what makes the check sensitive to the source of the data, not only to
  its content.
---

## Context

Data identifier values are listed in the message catalogue of
[`../../04_architecture/ee_architecture.md`](../../04_architecture/ee_architecture.md); they are
plausible example values and must be agreed with the gateway supplier (`OP-28`).
