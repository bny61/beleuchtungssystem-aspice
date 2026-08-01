# Analysis — hardware side of the SM-01 diagnostic coverage claim (preparation for OP-15)

**Status:** preparation for the FMEDA. **This document does not assert a diagnostic coverage
figure.** It states what the hardware buys, so that `safety-analyst` can confirm or reject the
90 % claim of `SM-01` in phase 5.
**Owner:** hardware-engineer · **Process:** ASPICE HWE.1 · ISO 26262-5 (evaluation of hardware
architectural metrics), ISO 26262-9 (FMEDA as a safety analysis)

> Teaching/reference project. **All numeric values are plausible example values, not validated
> data.** The failure-rate distribution below is a *hardware proposal for the partition*, not an
> FMEDA result. The FMEDA owns both the partition and the coverage per group.

---

## 1 Why this document exists

`analysis_current_sensing.md` section 6 states that the bare threshold scheme is worth about **60 %**
and that **90 %** becomes arguable only with four additional measures. That is a defensible
position, but it is not yet in a form the FMEDA can check: it names measures without saying *which
part of the failure space* each measure covers. A coverage claim that cannot be decomposed cannot be
confirmed — it can only be believed.

## 2 🔍 DEEP DIVE — failure-mode partition of the low-beam output path

Element under consideration: one low-beam channel, from the driver output stage through the harness
and LED module back through the shunt, amplifier, filter and ADC input.

| # | Failure-mode group | Proposed share of λ | Bare scheme | With the additional measure | Measure |
|---|---|---|---|---|---|
| 1 | Complete open load — connector, harness open, driver output open, both strings lost | 60 % | ~99 % | ~99 % | `SM-01` core (threshold + debounce) |
| 2 | Partial load loss — one of two parallel strings | 8 % | **0 %** | ~85 % | `HW-REQ-006` channel voltage |
| 3 | Short to battery on the channel output | 7 % | **0 %** (worse: misclassified) | ~90 % | `HW-REQ-006` + `SM-03` / `HW-REQ-020` |
| 4 | Driver-internal faults — output stage, OVP/OCP/OT trip, regulation loop | 10 % | **0 %** | ~80 % | `HW-REQ-007` status readback (`SM-04`) |
| 5 | Sense-chain faults — shunt open/short, amplifier stuck, offset drift | 10 % | **0 %** (masks the fault) | ~85 % | `HW-REQ-005` off-phase zero-current test |
| 6 | Reference and gain drift of the ADC path | 5 % | **0 %** | ~80 % | `HW-REQ-010` reference plausibility |

Weighted result of this partition (plausible example arithmetic, **not** an FMEDA result):

```
bare scheme        0.60 x 0.99                                     = 59.4 %   ~ 60 %
+ HW-REQ-006       0.08 x 0.85 + 0.07 x 0.90                       = 13.1 pts
+ HW-REQ-007       0.10 x 0.80                                     =  8.0 pts
+ HW-REQ-005       0.10 x 0.85                                     =  8.5 pts
+ HW-REQ-010       0.05 x 0.80                                     =  4.0 pts
---------------------------------------------------------------------------------
all measures                                                       = 93.0 %
```

That is consistent with the 60 % / 90 % statement already published and leaves about **3 percentage
points of margin** on the 90 % claim — thin enough that removing any single measure breaks it:

| Measure removed | Resulting coverage | 90 % still met? |
|---|---|---|
| `HW-REQ-005` (off-phase self-test) | 84.5 % | no |
| `HW-REQ-006` (channel voltage) | 79.9 % | no |
| `HW-REQ-007` (driver status) | 85.0 % | no |
| `HW-REQ-010` (reference plausibility) | 89.0 % | no (marginally) |

**None of the four is optional.** That is the hardware-side statement, and it is the one the safety
case needs — not the 90 % itself.

## 3 What the FMEDA has to decide, and what hardware must not pre-empt

| Question | Owner |
|---|---|
| Is the λ partition of section 2 realistic against the component list? | `safety-analyst` |
| Are the per-group coverages defensible (a table lookup for the diagnostic technique, not an opinion)? | `safety-analyst` |
| Which of these are single-point-fault detections and which reduce latent faults (LFM)? | `safety-analyst` |
| Does SPFM/LFM/PMHF meet the ASIL B targets with these numbers? | `safety-analyst` |
| Does the diagnostic test interval fit the FTTI (SPF) and the multiple-point fault detection interval (LFM)? | hardware provides the intervals, `safety-analyst` evaluates |

Test intervals hardware guarantees, for the FMEDA to use directly:

| Measure | Test interval | Purpose in the metric |
|---|---|---|
| `SM-01` core | continuous, per PWM period (2.5 ms), qualified over 50 ms | single-point fault detection inside the 300 ms FTTI |
| `HW-REQ-005` off-phase test | every PWM period, fault after 20 ms | detects sense-chain faults that would otherwise be **latent and masking** |
| `HW-REQ-006` channel voltage | 10 ms | single-point fault detection and cause discrimination |
| `HW-REQ-007` driver status | 10 ms | single-point fault detection |
| `HW-REQ-010` reference plausibility | 100 ms | latent-fault detection of the measurement path |

All of these are far shorter than one driving cycle, so the latent-fault argument does not depend on
a power-up test only.

## 4 What `SM-01` must state so the claim is checkable

The record has been updated accordingly (see the change note in `SM-01.md`). It must carry:

1. the **failure-mode partition** it claims to cover, by reference to section 2 of this document —
   a coverage number without a denominator is not evidence;
2. the **conditionality**, naming the four requirements explicitly (already present);
3. the **test interval per measure** (section 3), because the FMEDA needs the interval, not only the
   coverage;
4. the **detected-fault statement and the not-covered statement** — `SM-01` previously had no
   explicit "not covered" field, and the uncovered residue is what the FMEDA prices;
5. the note that `HW-REQ-004` is **not implemented in the base variant** (decision `OP-17` in
   `04_architecture/ee_architecture.md` section 4), so no coverage may be claimed from it;
6. the statement that the number itself is **owned by `safety-analyst`** and that `SM-01` stays
   `draft` until the FMEDA confirms it.

## 5 Consequences hardware already sees for the FMEDA

- **Group 5 is the dangerous one.** A sense chain stuck at a plausible value does not fail the
  diagnosis, it *masks* the fault it should detect. In the FTA this is an AND gate (open load AND
  sense chain stuck), in the FMEDA it is a latent fault. `HW-REQ-005` is what breaks it, and it costs
  nothing because the PWM off-phase is a free known-zero reference.
- **Group 2 remains the weakest leg** at ~85 % via the channel voltage. If the FMEDA cannot support
  85 % there, `OP-23` (per-string sensing, decided against in phase 3) has to be reopened — the
  decision was explicitly made conditional on this.
- **Groups 3 and 4 depend on components**, not on design: `A-10` (driver status available) is a
  datasheet assumption. If a candidate driver does not provide the status, 8 percentage points
  disappear and the 90 % is gone.

## 6 Open points

| # | Point | Owner |
|---|---|---|
| 1 | `OP-15` — confirm or reject the 90 % against the FMEDA using the partition of section 2 | safety-analyst |
| 2 | If group 2 cannot support ~85 %, reopen `OP-23` (per-string sensing) | safety-analyst, systems-engineer |
| 3 | Confirm `A-10` against a real LED driver datasheet during component selection | hardware-engineer |
| 4 | Fault injection at the level of the six groups — test design | verification-engineer |

---

**Work products:** `05_hardware/analysis_sm01_coverage.md`, updated `SM-01.md`
**Open points:** section 6
**Process reference:** ASPICE **HWE.1** (hardware requirements analysis) with the safety analyses of
**SUP.9 / MAN.5** feeding back · ISO 26262 **Part 5** (evaluation of the hardware architectural
metrics; hardware architectural design) · **Part 9** (safety analyses, FMEDA).
