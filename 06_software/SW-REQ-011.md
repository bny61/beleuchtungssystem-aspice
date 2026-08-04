---
id: SW-REQ-011
text: >
  While the measured LED module temperature is above 105 C, SWC_LightManager shall compute the
  low-beam channel set point from the derating curve of HW-REQ-023 in every 100 ms thermal cycle, and
  shall never command a set point below the 400 mA derating floor.
type: functional
asil: B
source: HW-REQ-023
derived_from: [HW-REQ-023]
allocated_to: [SWC_LightManager, Temp_Sense_Chain, SM-05]
verified_by: []
status: draft
rationale: >
  Software side of SM-05. Curve, breakpoints and floor are taken unchanged from HW-REQ-023 and
  HW-REQ-008; this requirement adds only the cycle time and the floor clamp in software. The 100 ms
  cycle matches the temperature sampling interval of HW-REQ-022. The floor matters to the Golden
  Thread: a set point below 400 mA would make the 150 mA open-load threshold of SM-01 ambiguous.
  A commanded derating is also the third cause in the discrimination of SW-REQ-002, which is why the
  derating set point is an input to the monitoring path and not only to the actuation path.
---

## Context

📋 **OVERVIEW.** `OP-36` is open on the upstream side: `HW-REQ-023` carries ASIL B but hangs off the
QM requirement `CR-014`; the missing system-level requirement is `systems-engineer`'s. The ASIL here
is inherited from `HW-REQ-023`, not assigned.
