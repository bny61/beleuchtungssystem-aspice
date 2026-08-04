---
id: SW-REQ-008
text: >
  While the high beam is commanded on, SWC_HighBeamMonitor shall evaluate every 20 ms whether the
  commanded high-beam state is plausible against vehicle speed and ambient brightness, and shall
  de-energise the high beam through its own enable path within 250 ms of detecting an implausible
  state.
type: safety
asil: A(A)
source: TSR-007
derived_from: [TSR-007]
allocated_to: [SWC_HighBeamMonitor, LED_Driver_Stage_1, MCU_Lockstep]
verified_by: []
status: draft
rationale: >
  Safety path of the decomposition; ASIL inherited from TSR-007. 20 ms monitor period is the value
  already used in chain C of the E/E architecture timing analysis (120 ms detection + 250 ms reaction
  = 370 ms against the 500 ms FTTI of SG-02). The monitor uses different inputs from SWC_HighBeamControl
  and acts on a separate enable path, which is the substance of the independence claim. A staleness
  reaction on AmbientLight is **not** specified here because the choice between a shorter timeout and
  a staleness reaction is OP-29 and belongs to safety-manager. Plausible example values.
---

## Context

📋 **OVERVIEW — SG-02 thread.** Depends on `OP-29`: the published `AmbientLight` timeout of 500 ms
equals the SG-02 FTTI, so a signal that simply stops is not declared invalid before the FTTI has
elapsed. The software architecture provides the hook (a signal-age input to the plausibility
decision) but does not fix the threshold; that is a decision, not an implementation detail.
