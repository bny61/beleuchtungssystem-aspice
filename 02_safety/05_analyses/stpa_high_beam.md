# STPA (short form) — control action "high beam on"

**Phase 5 · ASPICE SYS.2 as the consumer of the findings · ISO 26262-9 (safety analyses; STPA is
used here as a complementary technique, not as a substitute for the FMEA/FTA)**
**Status:** draft · **Owner:** safety-analyst

> Teaching/reference project. Plausible example values, not validated data.

---

## 📋 OVERVIEW — why this is short

STPA is included on the **second thread** for contrast: it asks a different question from the FMEA
and the FTA. Those two start from a component and ask how it fails; STPA starts from a *control
action* and asks when issuing it — or not issuing it — is unsafe, even with every component working.
The value of running it on `SG-02` is precisely that the hazard there is not a component failure but
a **correct command issued at the wrong moment**.

## 1 Losses and hazards

| ID | Loss |
|---|---|
| `L-1` | Collision or injury because an oncoming or preceding driver is glared |
| `L-2` | Collision or injury because the own sight distance is insufficient |

| ID | System-level hazard | Leads to | Safety goal |
|---|---|---|---|
| `HZ-A` | The high beam illuminates a segment occupied by another road user | `L-1` | `SG-02` |
| `HZ-B` | The high beam is unavailable while the road ahead is clear and dark | `L-2` | none — availability, no ASIL |

`HZ-B` is listed on purpose. It has no safety goal, and naming it prevents the analysis from
answering every UCA with "switch it off", which would trade a rated hazard for an unrated one.

## 2 Control structure

```
                 driver request (light switch, via Vehicle_Gateway)
                                   |
                                   v
  +-------------------------------------------------------------+
  |  SWC_HighBeamControl  (QM(A), TSR-006)   -- controller       |
  |     segment masking computed from ObjectList                 |
  +-------------------------------------------------------------+
        | CA-1 "high beam segment ON"        ^
        | CA-2 "high beam segment OFF"       | feedback: DriverStatus, I_Load
        v                                    |
  +-------------------------------------------------------------+
  |  LED_Driver_Stage_n  -- actuator (enable gate + PWM)         |
  +-------------------------------------------------------------+
        |                                    ^
        v                                    |
  +-------------------------------------------------------------+
  |  High-beam segments -- controlled process (the light itself) |
  +-------------------------------------------------------------+
        |
        v  observed by the vehicle's camera / object detection (A-05, outside the item)
  +-------------------------------------------------------------+
  |  ObjectList (no E2E), VehicleSpeed + AmbientLight (E2E)      |
  +-------------------------------------------------------------+
        |                                    |
        v                                    v
  +-------------------------------------------------------------+
  |  SWC_HighBeamMonitor  (A(A), TSR-007)  -- second controller  |
  |     separate enable path to the driver stage                 |
  +-------------------------------------------------------------+
```

Two controllers act on one process through two paths. That is the decomposition drawn as a control
structure, and the monitor's separate enable path is what makes it a control structure rather than a
picture of one.

## 3 Unsafe control actions — `CA-1` "high beam segment ON"

| UCA-ID | Not provided | Provided when unsafe | Wrong timing / order | Too long / stopped too soon |
|---|---|---|---|---|
| `UCA-01` | `CA-1` not provided while the road ahead is clear and dark → `HZ-B` | — | — | — |
| `UCA-02` | — | `CA-1` provided while an oncoming or preceding vehicle occupies the segment → `HZ-A` | — | — |
| `UCA-03` | — | — | `CA-1` provided **before** a valid `ObjectList` has been evaluated — at power-on, after a bus recovery, or after a mode change → `HZ-A` | — |
| `UCA-04` | — | — | — | `CA-1` maintained for longer than the 500 ms FTTI after the object has been reported → `HZ-A` |

## 4 Loss scenarios, and the requirement each one generates

| Scenario | UCA | What actually happens | Requirement it generates | Status in this project |
|---|---|---|---|---|
| `LS-1` | `UCA-02` | `ObjectList` is stale, corrupt or mis-routed. It is deliberately **not** E2E-protected, so nothing detects it; the control path masks the wrong segment and believes it has done the right thing | The monitor must de-energise on an implausible high-beam state using **different** inputs | **Exists** — `TSR-007`, and it is why `CF-11` in the DFA is the row that works |
| `LS-2` | `UCA-02` | The monitor's own inputs are **stale but not timed out**: `AmbientLight` has a 500 ms timeout, which equals the whole `SG-02` FTTI. The monitor evaluates old data and confirms an unsafe state | A staleness reaction shorter than the FTTI, not only a timeout | **Missing** — `OP-29`, and the FTA lists it as `C5` in nine of eleven cut sets. Deliberately **not** closed here: it is a concept decision |
| `LS-3` | `UCA-03` | The ECU is still booting, or the bus has just recovered, when the light request arrives. No object data has been evaluated yet, and the segment is energised on a default state | A defined power-on and recovery state for the high beam, with the high beam **inhibited** until a valid object evaluation exists | **Missing** — this is `OP-46` (power-on readiness) seen from the `SG-02` side. `SYS-REQ-025` specifies hold-last-valid for the **low beam**; nothing states the high-beam behaviour, and hold-last-valid would be the wrong rule there |
| `LS-4` | `UCA-03` | `ObjectList` is absent entirely rather than wrong. `TSR-006`/`TSR-007` address implausible states; neither addresses absence | An explicit reaction to a missing object list at speed | **Missing** — `OP-57` |
| `LS-5` | `UCA-04` | The monitor issues its off command, but the driver stage will not switch off — failed short downstream of the enable gate, where neither path reaches | Detection of a high-beam stage that stays conducting with its enable removed | **Missing** — folded into `OP-57`; also the second order-1 candidate in `fta_sg02.md` |
| `LS-6` | `UCA-01` | The monitor de-energises the high beam on a marginal plausibility check and does not release it again; the driver has no high beam on a clear road | A release condition and hysteresis, so the safety reaction is not a one-way latch | **Missing, and unrated.** `HZ-B` has no safety goal, so no ASIL requirement follows — but a monitor that latches off is a warranty and acceptance problem, and it is how safety mechanisms get disabled in the field. Recorded here, routed to `systems-engineer` as part of `OP-57` |

## 5 What STPA added that the FMEA and FTA did not

Three of the six scenarios (`LS-3`, `LS-4`, `LS-6`) involve **no component failure at all**. The
FMEA cannot find them, because it starts from a failure mode, and the FTA finds them only if
somebody thinks to draw the basic event. That is the argument for running a control-action analysis
alongside the failure-based ones, and it is the reason the phase asked for it.

The one it did **not** add: `LS-1` and `LS-2` were already known from the fault tree and from
`OP-29`. STPA confirmed them from a different direction, which is worth something but is not a new
finding.

---

**Work products:** `02_safety/05_analyses/stpa_high_beam.md`
**Open points:** new `OP-57` (missing `ObjectList`, high-beam stage stuck conducting, and the
release condition of `LS-6`); `OP-29` and `OP-46` confirmed from a second direction and deliberately
**not** closed — both are concept decisions for `safety-manager` and `systems-engineer`.
**Process reference:** ASPICE **SYS.2** (system requirements analysis) as the consumer of the
generated requirements · ISO 26262 **Part 9** (safety analyses — STPA used as a complementary
technique alongside the inductive and deductive analyses) · **Part 3** (functional safety concept,
as the origin of `SG-02`). Parts and topics named, no clause numbers cited.
