---
id: SW-REQ-014
text: >
  When a valid light request for low beam is received, the lighting ECU software shall command the
  low-beam channels within 10 ms of the reception indication of the light request signal group.
type: timing
asil: B
source: SYS-REQ-001
derived_from: [SYS-REQ-001]
allocated_to: [SWC_LightManager, MCU_Lockstep]
verified_by: []
status: draft
rationale: >
  The 10 ms software share of the 300 ms activation budget of SYS-REQ-001, taken from
  05_hardware/analysis_low_beam_activation.md section 3 where it is already an entry in the budget
  table. Decomposed: 1 ms reception indication in the communication stack + 5 ms worst-case wait for
  the next activation of the 5 ms request runnable + 2 ms request evaluation including the E2E check +
  0.5 ms actuation write = 8.5 ms against the 10 ms cap. Plausible example values. This 300 ms is an
  activation latency and is unrelated to the 300 ms FTTI of SG-01.
---

## Context

🔍 **DEEP DIVE — Golden Thread.** The budget for the whole chain, and the finding that about two
thirds of it is consumed outside the item boundary (`OP-44`), stay with
`05_hardware/analysis_low_beam_activation.md`; this record only fixes the software share as a
requirement so that it can be measured.
