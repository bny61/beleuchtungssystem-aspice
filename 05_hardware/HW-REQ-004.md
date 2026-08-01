---
id: HW-REQ-004
text: >
  Where the commanded PWM on-time of a low-beam channel is shorter than 150 us, the LED driver
  stage shall insert a diagnostic measurement window of at least 200 us at the commanded set point
  at intervals of not more than 10 ms.
type: electrical
asil: B
source: SYS-REQ-017
derived_from: [SYS-REQ-017]
allocated_to: [LED_Driver_Stage_1, SM-01]
verified_by: []
status: draft
rationale: >
  Below the minimum usable on-time no valid sample exists. Either this window or the
  "diagnosis not available" path of SYS-REQ-017 must apply; reuse of a stale sample would make the
  detection time unbounded. Plausible example values.
---

## Context

Hardware requirement from the phase 3 refinement of SYS-REQ-014. Analysis and derivation:
[`analysis_current_sensing.md`](analysis_current_sensing.md). New test cases are a handoff to
`verification-engineer`.

## Variant applicability (change note, phase 6 — closes OP-30)

**Not implemented in the base variant.** The `OP-17` decision recorded in
[`../04_architecture/ee_architecture.md`](../04_architecture/ee_architecture.md) section 4 resolved
the gating question in favour of the "diagnosis not available" path of `SYS-REQ-017`: the forced
measurement window injects a current pulse into a deliberately dimmed channel, which is visible as
flicker at low duty and is an unrequested actuation of a safety-relevant output — the very thing
`TSR-002` exists to prevent.

The requirement is **retained as an option for the work-lamp channels**, where deep dimming is a
normal operating case and no safety goal is attached to the output. It is therefore excluded from
the SM-01 coverage claim; see the `not_covered` field of [`SM-01.md`](SM-01.md) and
[`analysis_sm01_coverage.md`](analysis_sm01_coverage.md). The record text is unchanged — only its
applicability is stated here, because the decision was already published in phase 3.
