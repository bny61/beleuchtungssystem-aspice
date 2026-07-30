# S/E/C classification — interpretation applied in this project

Supplement to [`hara.md`](hara.md). Documents **how** the classes were interpreted in this project
so that the ratings are traceable in the confirmation review.

> **Not a standard extract.** The classes S0–S3, E0–E4 and C0–C3 and the determination table are
> defined in ISO 26262-3. What follows is exclusively the project-specific interpretation in our own
> words — no normative text, no reproduced determination table.

## 1 Severity — severity of harm

| Class | Interpretation in this project | Example from this HARA |
|---|---|---|
| S0 | No injuries expected | Damage to the lamp unit without a driving situation |
| S1 | Light injuries, normally healing without consequences | H-06: reduced conspicuity in daylight |
| S2 | Severe injuries, survival probable | H-05, H-07: glare with remaining reaction time |
| S3 | Life-threatening or fatal injuries | H-01, H-02, H-03: unlit carriageway or abrupt glare at 80 km/h |

**Project rule:** where an 18 t combination is involved, harm to third parties is considered, not
only to the vehicle occupants. For collision scenarios this systematically leads to S3.

## 2 Exposure — probability of the operational situation

| Class | Interpretation in this project | Example |
|---|---|---|
| E0 | Practically impossible | — |
| E1 | Very low probability | — |
| E2 | Low probability; several conditions must coincide | H-02, H-03, H-07 |
| E3 | Medium probability; occurs regularly but not predominantly | H-01, H-04, H-05, H-06 |
| E4 | High probability; predominant part of operating time | — |

**Project rule:** what is rated is the **operational situation**, not the fault. The governing
measure is the share of operating time per usage profile `A-07`
(see [`operational_situations.md`](operational_situations.md)).

**Deliberate delimitation:** "night driving" in general would be E4 in long-haul operation. What is
hazard-relevant, however, is the narrower situation *night + unlit + rural-road speed*, and that is
E3. This delimitation decides between ASIL B and ASIL C and is tracked as `RISK-01`.

## 3 Controllability

| Class | Interpretation in this project | Example |
|---|---|---|
| C0 | Controllable in general | — |
| C1 | Simply controllable; practically all drivers control the situation | H-06 |
| C2 | Normally controllable; the majority of drivers control the situation | H-01, H-02, H-03, H-04, H-05 |
| C3 | Difficult to control or uncontrollable | H-07 |

**Project rule:** what is rated is controllability by the person who actually has to act. In glare
scenarios that is the **dazzled** driver, not the driver of the causing vehicle.

**What the C rating depends on:** for H-01, C2 presumes that the driver notices the failure and
responds. That presumption is assumption `A-03` and is technically supported by `FSR-004` (driver
warning within 2 s). Without the warning, C3 would have to be examined — with a corresponding
increase in ASIL. **The warning is therefore not optional; it carries the rating.**

## 4 Combinations used and result

Only the combinations that actually occurred in this HARA, with the result of the determination
table per ISO 26262-3:

| S | E | C | ASIL | Hazard |
|---|---|---|---|---|
| S3 | E3 | C2 | **B** | H-01, H-04 |
| S3 | E2 | C2 | **A** | H-02, H-03 |
| S2 | E3 | C2 | **A** | H-05 |
| S2 | E2 | C3 | **A** | H-07 |
| S1 | E3 | C1 | **QM** | H-06 |

For context on the borderline discussion: the combination S3/E4/C2 leads to **ASIL C**. That is
exactly why the E rating of H-01 is the critical decision of this project.
