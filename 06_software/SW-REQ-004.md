---
id: SW-REQ-004
text: >
  While the light request signal group is marked invalid and the low beam was energised at the moment
  of invalidation, SWC_LightManager shall hold the last valid low-beam set point until a valid light
  request signal group is received again or the ignition status changes to off.
type: safety
asil: B
source: SYS-REQ-025
derived_from: [SYS-REQ-025]
allocated_to: [SWC_LightManager, LED_Driver_Stage_1]
verified_by: []
status: draft
rationale: >
  Direct software refinement of SYS-REQ-025 with no added condition. The mirror case — request
  invalid while the low beam is not energised — deliberately does not switch the low beam on, in line
  with the context of SYS-REQ-025. The held set point is the arbitrated set point including any
  active thermal derating (SW-REQ-011), not the raw request, so that holding cannot undo a derating
  already commanded.
---

## Context

🔍 **DEEP DIVE — Golden Thread.** The hold behaviour is the `HOLD_LAST_VALID` branch of the state
machine in [`detailed_design/swc_lightmanager.md`](detailed_design/swc_lightmanager.md). Invalidation
itself is `SW-REQ-005`.
