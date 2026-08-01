---
id: HW-REQ-024
text: >
  The thermal design of a low-beam channel shall keep the LED junction temperature at or below
  135 C for a headlamp cavity temperature up to 105 C, with the derating curve of HW-REQ-023
  active and the module heat path degraded to twice its nominal thermal resistance.
type: electrical
asil: B
source: CR-014
derived_from: [CR-014, HW-REQ-023]
allocated_to: [LED_Driver_Stage_1, Temp_Sense_Chain]
verified_by: []
status: draft
rationale: >
  This is the condition under which the 400 mA floor of HW-REQ-008 is thermally admissible: in the
  worst case analysed (cavity 105 C, thermal path degraded by a factor of two) the equilibrium
  junction temperature is about 130 C, leaving 5 K against the 135 C design limit and 15 K against
  the 150 C component rating. Derivation and load-line arithmetic in analysis_thermal_derating.md.
  Plausible example values. Assumptions A-20, A-21.
---

## Context

Hardware requirement from the phase 6 refinement of the E/E architecture (HWE.1 / HWE.2).
Thermal design constraint behind the derating floor. Derivation: [`analysis_thermal_derating.md`](analysis_thermal_derating.md).
Verification entry: [`hw_verification_plan.md`](hw_verification_plan.md). Test cases are a
hand-off to `verification-engineer`.
