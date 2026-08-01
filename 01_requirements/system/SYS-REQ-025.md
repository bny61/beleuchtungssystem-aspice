---
id: SYS-REQ-025
text: >
  While the light request signal group is marked as invalid and the low beam was energised at the
  moment of invalidation, the lighting ECU shall keep the low-beam channels energised at the last
  valid set point until a valid light request signal group is received again or the ignition signal
  changes to off.
type: safety
asil: B
source: SYS-REQ-024
derived_from: [SYS-REQ-024, FSR-002]
allocated_to: [ECU_LightingCtrl, SWC_LightManager, LED_Driver_Stage_1]
verified_by: []
status: draft
rationale: >
  Golden Thread. A communication fault must not switch off the low beam at night: that would be
  exactly hazard H-04 (unintended deactivation) triggered by the safety measure itself. Failing
  silent towards "keep the light on" is the correct direction for SG-01, and it is bounded because
  the loss is reported by SYS-REQ-024 and shown to the driver via the warning path.
---

## Context

The mirror case - light request invalid while the low beam is *not* energised - deliberately does
not switch the low beam on. Automatic activation is covered by the ambient-brightness path
(`SYS-REQ-002`), which carries its own validity information.
