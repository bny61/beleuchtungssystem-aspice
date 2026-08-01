---
id: HW-REQ-014
text: >
  While transient pulses per ISO 7637-2 are applied at the supply input, the lighting ECU shall
  meet the functional status class assigned to each pulse in the pulse table of
  analysis_supply_and_transients.md.
type: electrical
asil: B
source: CR-017
derived_from: [CR-017]
allocated_to: [Power_Supply_Unit, ECU_LightingCtrl]
verified_by: []
status: draft
rationale: >
  Closes the hardware side of OP-4. CR-017 demands "without loss of function" for all pulses, which
  is not achievable for the severe supply-interruption pulses at reasonable cost; the pulse table
  assigns class A to the pulses that occur during normal driving and class C only to pulses that
  represent a supply interruption. The resulting change to CR-017 is a hand-off to
  systems-engineer. Test severity levels per ISO 7637-2 for 24 V systems, plausible example values.
---

## Context

Hardware requirement from the phase 6 refinement of the E/E architecture (HWE.1 / HWE.2).
Derivation: [`analysis_supply_and_transients.md`](analysis_supply_and_transients.md).
Verification entry: [`hw_verification_plan.md`](hw_verification_plan.md). Test cases are a hand-off
to `verification-engineer`.
