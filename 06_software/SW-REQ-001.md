---
id: SW-REQ-001
text: >
  While a low-beam channel is commanded energised, SWC_LightManager shall compare the commanded
  channel state with the measured channel state in every 5 ms monitoring cycle, and shall set the
  channel discrepancy status of that channel when commanded and measured state disagree in four
  consecutive cycles.
type: safety
asil: B
source: TSR-002
derived_from: [TSR-002]
allocated_to: [SWC_LightManager, MCU_Lockstep, Current_Sense_Chain]
verified_by: []
status: draft
rationale: >
  Software realisation of the command/feedback comparison demanded by TSR-002 (SM-01 reporting path).
  The 5 ms cycle is the monitoring task period of sw_architecture.md and is the 5 ms task-latency term
  already counted in HW-REQ-009; four consecutive cycles equal the 20 ms debounce of SM-01, so the
  software adds no time to the published 80 ms detection budget. Plausible example values.
---

## Context

🔍 **DEEP DIVE — Golden Thread.** Detailed behaviour in
[`detailed_design/swc_lightmanager.md`](detailed_design/swc_lightmanager.md). The comparison is the
software half of `SM-01`; the measurement chain itself is `HW-REQ-001` … `HW-REQ-005`. Test cases are
a hand-off to `verification-engineer`.
