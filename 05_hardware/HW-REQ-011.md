---
id: HW-REQ-011
text: >
  While the protected supply voltage is between 9 V and 36 V, the Power_Supply_Unit shall keep the
  internal supply rails within +/-2 % (5 V and 3.3 V rails) and within +/-0.5 % (3.3 V ADC
  reference) of their nominal values.
type: electrical
asil: B
source: SYS-REQ-012
derived_from: [SYS-REQ-012, SYS-REQ-013]
allocated_to: [Power_Supply_Unit, SM-06]
verified_by: []
status: draft
rationale: >
  The rail band is what the tolerance chain of HW-REQ-001 assumes; a reference outside +/-0.5 %
  invalidates the 150 mA open-load threshold. The 9 V lower edge follows from SYS-REQ-013
  (undervoltage operation), the 36 V upper edge from the jump-start / overvoltage operating case of
  ISO 16750-2 (electrical loads) for a 24 V system. Plausible example values.
---

## Context

Hardware requirement from the phase 6 refinement of the E/E architecture (HWE.1 / HWE.2).
Derivation: [`analysis_supply_and_transients.md`](analysis_supply_and_transients.md).
Verification entry: [`hw_verification_plan.md`](hw_verification_plan.md). Test cases are a hand-off
to `verification-engineer`.
