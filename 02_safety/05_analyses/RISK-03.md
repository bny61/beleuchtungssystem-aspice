---
id: RISK-03
text: >
  The ASIL B single-point fault metric of the SG-01 path is met only if OP-34 is decided by
  differentiating the SAFE_OFF disable path by channel class. The phase 5 FMEDA and the SG-01
  fault tree assume that decision; it has not been taken.
type: risk
status: draft
owner: safety-manager
source: Phase 5 FMEDA, section 7 (sensitivity to OP-34)
mitigation: >
  Decide OP-34 in the technical safety concept. If SAFE_OFF differentiates by channel class, the
  published FMEDA result stands. If it does not, the FMEDA and fta_sg01 must be redone rather than
  adjusted, and the architecture needs a further measure on the low-beam disable path.
impact: >
  With undifferentiated SAFE_OFF the single-point fault metric falls from 91.8 % to 84.2 %, against
  an ASIL B target of 90 % - a 7.6 point swing across the target, not a rounding sensitivity. LFM
  and PMHF stay inside their targets in both cases, so SPFM alone decides.
---

## Context

`SM-02` de-energises the driver stages on `SAFE_OFF`. Applied to the low beam that action *is*
`H-01`, the hazard `SG-01` exists to prevent — which is why `OP-34` was raised when the safety
mechanism was written. Phase 5 was run on the human's instruction to analyse the **intended**
design, in which the disable path differentiates the low beam from the other channels.

Two failure modes carry the swing: `W4` (`SAFE_OFF` stuck asserted, 2.20 FIT) and `M2` (MCU stall
leading to the same assertion, 10.80 FIT). Under the assumption both are residual faults detected
by `SM-01`; without it both become single-point faults, and together with the two uncovered supply
modes they take the metric below target.

**This risk is not closed by any analysis.** It closes when `safety-manager` decides `OP-34`. Until
then the published SG-01 metrics are conditional, and the safety case must not cite them as
unconditional evidence.

Plausible example values throughout, as everywhere in this project.
