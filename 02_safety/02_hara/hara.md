# Hazard Analysis and Risk Assessment (HARA)

**Item:** Adaptive front-lighting system incl. work-lamp control
**Vehicle:** Heavy truck, class N3, 18 t tractor unit
**Standard:** ISO 26262-3 (Hazard Analysis and Risk Assessment)
**Status:** Phase 2, draft — not confirmed by a confirmation review
**Owner:** safety-manager

> **Not a production baseline.** All ratings and numeric values are plausible example values of a
> teaching/reference project, not validated data and no substitute for a real HARA.

---

## 1 Method

1. **Define the item boundary** — see [`../01_item_definition/item_definition.md`](../01_item_definition/item_definition.md).
2. **Build operational situations** as the cross product of driving situation x operating mode x
   environment, then reduce to the relevant combinations — see
   [`operational_situations.md`](operational_situations.md).
3. **Derive malfunctioning behaviour systematically** per function using the fault classes
   *loss of function · unintended activation · incorrect value · too early / too late · stuck*.
4. **State the hazard at vehicle level** (the effect in traffic, not the component fault).
5. **Rate S/E/C** with a written rationale per rating —
   see [`sec_classification.md`](sec_classification.md).
6. **Determine the ASIL** from the combination per the determination table of ISO 26262-3.
7. **Derive safety goals**, merging hazards with identical goal wording and carrying the highest
   ASIL.

---

## 2 Hazard table

| ID | OS | Malfunctioning behaviour | Hazard at vehicle level | S | E | C | **ASIL** | Safety goal |
|---|---|---|---|---|---|---|---|---|
| **H-01** | BS-01 | Failure of the low beam (both channels) | Carriageway unlit at 80 km/h, running off the road or colliding with an unlit obstacle | 3 | 3 | 2 | **B** | SG-01 |
| **H-02** | BS-02 | High beam stays active with oncoming traffic | Glare to the oncoming driver, head-on collision | 3 | 2 | 2 | **A** | SG-02 |
| **H-03** | BS-01 | Work lamps unintentionally active while driving | Glare to oncoming and following traffic | 3 | 2 | 2 | **A** | SG-02 |
| **H-04** | BS-03 | Unintended deactivation of the low beam | As H-01, additionally unexpected for the driver | 3 | 3 | 2 | **B** | SG-01 |
| **H-05** | BS-01 | Headlamp levelling permanently too high | Sustained glare to oncoming traffic | 2 | 3 | 2 | **A** | SG-02 |
| **H-06** | BS-06 | Failure of the daytime running lights | Reduced conspicuity of the vehicle in good visibility | 1 | 3 | 1 | **QM** | — |
| **H-07** | BS-05 | Cornering light swivels into the oncoming lane | Glare to oncoming traffic, unexpected and not correctable by the affected driver | 2 | 2 | 3 | **A** | SG-02 |

**Result:** 7 hazards, 6 of them leading to a safety goal and one (H-06) resulting in QM.
Highest resulting ASIL: **B** (H-01, H-04) — ASIL B is therefore the target ASIL of the project.

> **Machine-readable form:** every row of this table also exists as a record `H-01.md` … `H-07.md`
> in this folder (overview: [`README.md`](README.md)). The safety goals reference them via
> `derived_from: [H-xx]`; `tools/trace_check.py` reports any hazard with an ASIL other than QM that
> has no safety goal (`hazard-uncovered`).
>
> **Deliberate redundancy:** the values appear both in this table and in the front matter of the
> records. When changing either, update **both** — the check does not detect a divergence between
> table and record.

---

## 3 Rationale for the ratings

### H-01 — Failure of the low beam (design-driving case)

| | Rating | Rationale |
|---|---|---|
| **S** | **S3** | Complete loss of carriageway illumination at 80 km/h on an unlit rural road. Running off the road or colliding with an unlit obstacle at 18 t gross mass is highly likely to cause life-threatening or fatal injuries, including to uninvolved third parties. |
| **E** | **E3** | Night driving on unlit rural roads occurs regularly in N3 long-haul operation, but not predominantly. Under usage profile `A-07` the share is in the range of a few percent of operating time — medium probability. |
| **C** | **C2** | The driver notices the failure immediately (the carriageway goes dark) and can decelerate in a controlled manner; residual light from position lamps/daytime running lights and ambient light remains. A safe stop succeeds for the majority of drivers, but not practically all — hence C2 and not C1. |

**Borderline discussion (deliberately disclosed, tracked as `RISK-01`):**
With **E4** instead of E3 the determination table would yield **ASIL C** instead of B. E3 was chosen
because the hazard is bound to the combination *night + unlit + rural-road speed*, not to night
driving in general. This is the most sensitive single decision of the entire HARA — it determines
the target ASIL of the project and thereby the target values for SPFM, LFM and PMHF, the required
independence and the structural coverage in software. It must be explicitly confirmed in the
confirmation review of SG-01.

### H-02 and H-03 — Glare from high beam or work lamps

| | Rating | Rationale |
|---|---|---|
| **S** | S3 | Glare to oncoming traffic can cause a head-on collision; with an 18 t combination involved, fatal injuries are likely. |
| **E** | E2 | The hazard requires night, oncoming traffic and a fault to coincide — low exposure. |
| **C** | C2 | The dazzled driver can typically respond by decelerating and holding the lane; the glare is brief and recognised as such. |

### H-04 — Unintended deactivation

The effect is identical to H-01, hence the same rating **S3/E3/C2**. The difference is the fault
class: H-01 is a failure, H-04 an unintended deactivation. Both lead to **SG-01** but are addressed
by different safety requirements (`FSR-001` versus `FSR-002`).

### H-05 — Headlamp levelling too high

**S2** — the glare builds up less abruptly than in H-02, leaving oncoming traffic reaction time;
severe but survivable injuries are the more likely outcome.
**E3** — affects essentially every night drive with oncoming traffic.
**C2** — controllable by decelerating.

### H-06 — Failure of the daytime running lights (result QM)

**S1** — an 18 t vehicle remains clearly visible by its silhouette in daylight and good visibility;
at most light injuries are to be expected.
**E3** — daytime driving in good visibility is frequent, though the failure itself is the precondition.
**C1** — the situation is controllable by practically all road users.

> **Result QM — no safety goal arises.** The associated requirement remains legally relevant
> (ECE R48, daytime running light switching requirement) but is not safety-relevant in the sense of
> ISO 26262. This case is included deliberately to show that not every hazard leads to a safety goal.

### H-07 — Cornering light swivels into the oncoming lane

**S2** — glare with remaining reaction time, as H-05.
**E2** — requires cornering at night with oncoming traffic and a fault.
**C3** — the misalignment occurs unexpectedly and cannot be corrected by the affected driver
himself; he can only decelerate. Therefore difficult to control.

---

## 4 Derived safety goals

| ID | Wording | ASIL | Safe state | FTTI | Fault reaction time | Source |
|---|---|---|---|---|---|---|
| **SG-01** | No undetected failure of the low beam while driving | **B** | Limp-home operation: remaining channels active at reduced power, driver warning active, DTC stored | **300 ms** | **150 ms** | H-01, H-04 |
| **SG-02** | No unintended glare to other road users caused by high beam or work lamps | **A** | High beam and work lamps deactivated, low beam remains active | 500 ms | 250 ms | H-02, H-03, H-05, H-07 |

Records: [`../03_fsc/SG-01.md`](../03_fsc/SG-01.md) · [`../03_fsc/SG-02.md`](../03_fsc/SG-02.md)

### Rationale for the safe state of SG-01

"Lights off" would be the wrong safe state — it *is* the hazard. The safe state is therefore
*degraded but visible*: the intact channel keeps operating (`FSR-003`), the driver is warned
(`FSR-004`) and can end the journey in a controlled manner. It is precisely this warning that
underpins the C2 rating of H-01. Assumption **`A-03`** (driver response to the warning) is thereby
safety-relevant and a validation target at vehicle level, not a side note.

### Timing budget SG-01

```
Detection       SM-01, PWM-synchronous (HW-REQ-009):
                2.5 ms sync + 0.1 ms acquisition + 50 ms window
                + 20 ms debounce + 5 ms task latency           =  80 ms
Fault reaction  transition to limp-home                        = 150 ms   (fault reaction time)
                                                         Total = 230 ms
FTTI                                                           = 300 ms
Margin                                                         =  70 ms   (23 %)
```

> Updated with the phase 3 refinement of `SYS-REQ-014` (detection 70 ms -> 80 ms). The PWM-
> synchronous measurement adds synchronisation, acquisition and task latency. See
> [`../../05_hardware/analysis_current_sensing.md`](../../05_hardware/analysis_current_sensing.md).

The budget closes against the values held in `SG-01` and `SM-01`. The 2 s driver warning from
`CR-007` / `FSR-004` lies **outside** this budget: it is an information requirement, not a fault
reaction. This separation is binding — otherwise the design is dimensioned against the wrong
time limit.

---

## 5 Assumptions used

| ID | Assumption | Safety-relevant |
|---|---|---|
| `A-03` | The driver responds to the visual warning within the assumed reaction time | yes — underpins the C rating of H-01 |
| `A-05` | Object detection for the glare-free high beam lies outside the item boundary | yes — part of the SG-02 chain |
| `A-06` | Light switch position and ignition status arrive as bus signals | yes |
| `A-07` | Usage profile N3 long-haul with a predominant night share in the winter half-year | yes — basis of the E rating |

Full list: [`../../09_process/assumptions.md`](../../09_process/assumptions.md)

---

## 6 Open points

| ID | Point | Owner |
|---|---|---|
| OP-7 / `RISK-01` | Confirm the E rating of H-01 (E3 versus E4) in the confirmation review | safety-manager |
| OP-9 | Plan `A-03` as a validation target at vehicle level | verification-engineer |
| OP-10 | Interface agreement (DIA) for the object detection outside the item boundary | safety-manager |
| OP-13 | Role model and independence levels are missing (phase 0 skipped) — a precondition for the confirmation review of this HARA | safety-manager |

---

**Work products:** `hara.md`, `operational_situations.md`, `sec_classification.md` → `02_safety/02_hara/`
**Process reference:** ISO 26262 **Part 3** (Hazard Analysis and Risk Assessment, Safety Goals) ·
**Part 2** (confirmation review of the HARA) · ASPICE **SYS.1/SYS.2** as the requirements basis.
