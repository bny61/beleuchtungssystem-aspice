---
id: HW-REQ-030
text: >
  While less than 30 ms have elapsed since the effective enable signal of a low-beam channel became
  active, the lighting ECU shall suppress the open-load classification of that channel, and shall
  resume it at the end of that interval without reusing any sample acquired within it.
type: diagnostics
asil: B
source: SYS-REQ-001
derived_from: [SYS-REQ-001, SYS-REQ-018, HW-REQ-027]
allocated_to: [Current_Sense_Chain, ECU_LightingCtrl, SM-01]
verified_by: []
status: draft
rationale: >
  During the soft-start ramp required by HW-REQ-027 the channel current is below the 150 mA threshold
  of HW-REQ-001 / HW-REQ-002 by design, so an unblanked SM-01 classifies every switch-on as an open
  load. 30 ms = 20 ms worst-case ramp (HW-REQ-027) + 1 ms enable propagation (HW-REQ-026) + 9 ms
  margin for supply and temperature spread. Consequence, stated plainly: an open load already present
  at switch-on is reported at 30 ms + 80 ms (HW-REQ-009) = 110 ms, which EXCEEDS the 100 ms cap of
  SYS-REQ-018. Against the FTTI the case still closes: 110 ms + 150 ms reaction = 260 ms against the
  300 ms FTTI of SG-01, margin 40 ms (13 %). The cap conflict is not resolved here - see OP-42.
  Plausible example values.
---

## Context

🔍 **DEEP DIVE — Golden Thread.** Hardware requirement from the refinement of `SYS-REQ-001`
(low-beam activation), and the point at which the activation path and the `SG-01` detection path
touch. Analysis and derivation:
[`analysis_low_beam_activation.md`](analysis_low_beam_activation.md), section 4.

**No new safety mechanism.** This record constrains the operating condition of the existing `SM-01`;
it adds no detection and claims no diagnostic coverage. `SM-01.md` is deliberately **not** modified —
its `detection_time` of ≤ 80 ms and its conditional 90 % coverage claim are unchanged, and the
start-up detection case introduced here is handed to `safety-analyst` as `OP-43` rather than written
into a record that `OP-15` already blocks.

**Why blanking and not a lower threshold.** Raising the diagnosis to a set-point-relative threshold,
or re-deriving the blanking against the 170 mA guaranteed-no-trip edge of `HW-REQ-002`, would change
the basis of an approved concept and would design around a cap that belongs to `SYS-REQ-018`. The
conflict is recorded instead of engineered away; its owner is `systems-engineer`.

**What must not be lost at the end of the interval.** Resuming the classification must not reuse
samples taken during the ramp — a stale below-threshold sample carried across the boundary would
produce exactly the false trip the blanking exists to prevent, one qualification window later.

Verification entries: `HV-13` and `HV-14` in
[`hw_verification_plan.md`](hw_verification_plan.md), including the acceptance criterion that
1000 switch-ons produce no open-load classification.
