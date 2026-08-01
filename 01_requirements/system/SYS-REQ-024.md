---
id: SYS-REQ-024
text: >
  If a safety-relevant signal group is not received within the timeout defined for that signal
  group in the interface table, the lighting ECU shall mark that signal group as invalid.
type: communication
asil: B
source: SYS-REQ-022
derived_from: [SYS-REQ-022]
allocated_to: [ECU_LightingCtrl, SWC_LightManager]
verified_by: []
status: draft
rationale: >
  Makes the timeout column of the interface table a requirement instead of a table entry. Covers
  the loss failure mode, which the counter and checksum of SYS-REQ-023 cannot cover on their own
  once transmission stops entirely.
---

## Context

The timeout values themselves stay in the interface table of
[`../../04_architecture/ee_architecture.md`](../../04_architecture/ee_architecture.md) so that they
are maintained in one place. `TSR-008` is the oldest instance of this rule and is now a special
case of it.
