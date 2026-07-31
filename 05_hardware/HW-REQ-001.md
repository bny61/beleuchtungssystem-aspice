---
id: HW-REQ-001
text: >
  The current sensing of a low-beam channel shall measure the channel load current with a total
  uncertainty of not more than +/-20 mA at a channel current of 150 mA, over an ambient temperature
  range of -40 C to +85 C and including the residual error under the conducted-disturbance test
  levels of the HW verification plan.
type: electrical
asil: B
source: SYS-REQ-016
derived_from: [SYS-REQ-016, FSR-001]
allocated_to: [LED_Driver_Stage_1, Current_Sense_Chain, SM-01]
verified_by: []
status: draft
rationale: >
  Tolerance chain: shunt (1.0 % initial, 50 ppm/K TCR, 0.5 % drift), amplifier (150 uV offset,
  1.0 % gain), ADC (3.3 V reference +/-0.5 %, 12 bit, 3 LSB offset, 2 LSB INL) gives +/-9.8 mA worst
  case, plus a +/-10 mA allowance for residual conducted disturbance. All plausible example values,
  not validated data. Assumptions A-08, A-11.
---

## Context

Hardware requirement from the phase 3 refinement of SYS-REQ-014. Analysis and derivation:
[`analysis_current_sensing.md`](analysis_current_sensing.md). New test cases are a handoff to
`verification-engineer`.
