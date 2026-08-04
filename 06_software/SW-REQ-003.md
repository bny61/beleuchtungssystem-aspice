---
id: SW-REQ-003
text: >
  When a low-beam channel has been classified as failed, SWC_LightManager shall enter the LIMP_HOME
  state within one 5 ms monitoring cycle, shall keep the remaining low-beam channel energised at its
  current set point, and shall not command the failed channel to be re-energised until the next
  ignition cycle.
type: safety
asil: B
source: TSR-004
derived_from: [TSR-004]
allocated_to: [SWC_LightManager, LED_Driver_Stage_1, MCU_Lockstep]
verified_by: []
status: draft
rationale: >
  Software realisation of the SG-01 safe state: degraded but visible, not off. The software share of
  the 150 ms fault reaction time of TSR-004 is one 5 ms cycle plus the actuation write (see
  SW-REQ-013), which leaves the published 150 ms allocation untouched and unspent. Re-energising is
  blocked for the rest of the ignition cycle so that an intermittent open load cannot produce a
  flickering headlamp, which is a driver distraction rather than a diagnosis. Plausible example
  values.
---

## Context

🔍 **DEEP DIVE — Golden Thread.** The state machine, including the transition guards and the safe
state, is in [`detailed_design/swc_lightmanager.md`](detailed_design/swc_lightmanager.md).
`TSR-004` allocates 150 ms; this requirement uses a small part of it — the timing argument is in
`SW-REQ-013`.
