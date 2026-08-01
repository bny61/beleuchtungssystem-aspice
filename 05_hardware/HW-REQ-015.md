---
id: HW-REQ-015
text: >
  The supply input of the lighting ECU shall withstand a continuous reverse voltage of -32 V for at
  least 60 s without damage and without energising any lighting channel.
type: electrical
asil: B
source: CR-017
derived_from: [CR-017, SYS-REQ-012]
allocated_to: [Power_Supply_Unit]
verified_by: []
status: draft
rationale: >
  Reverse-polarity condition of ISO 16750-2 (electrical loads) for a 24 V system, realised by a
  series reverse-polarity MOSFET ahead of the pre-regulator, a TVS clamp for the transient energy
  and a common-mode choke plus pi filter for the conducted emission limits of ECE R10 (CR-012).
  "Without energising any channel" is the safety-relevant part: a reverse-conducting body diode in
  the driver output path would be an uncommanded actuation. Plausible example values.
---

## Context

Hardware requirement from the phase 6 refinement of the E/E architecture (HWE.1 / HWE.2).
Derivation: [`analysis_supply_and_transients.md`](analysis_supply_and_transients.md).
Verification entry: [`hw_verification_plan.md`](hw_verification_plan.md). Test cases are a hand-off
to `verification-engineer`.
