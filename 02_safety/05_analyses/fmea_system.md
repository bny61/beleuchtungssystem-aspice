# System-FMEA — Adaptive front lighting system (AIAG-VDA, 7 steps)

**Phase 5 · ASPICE SYS.2 / SYS.3 with SUP.9 carrying the findings back · ISO 26262-9 (safety
analyses, inductive analysis) · AIAG-VDA FMEA handbook, seven-step method — named by topic**
**Status:** draft · **Owner:** safety-analyst

> Teaching/reference project. **All ratings are plausible example values, not validated data.**
> **No RPN is computed anywhere in this document** — the method uses severity, occurrence and
> detection together with an action priority, and reducing them to a product is exactly what the
> AIAG-VDA revision removed.

---

## Step 1 — Planning and preparation

| Item | Content |
|---|---|
| Analysis object | `Item_LightingSystem` at system level: the lighting ECU, its sensing and actuation paths and its vehicle interfaces |
| Purpose | Identify system-level failure effects against `SG-01` and `SG-02`, and produce concrete actions where the risk is not adequately controlled |
| Boundary | Item boundary per `02_safety/01_item_definition/item_definition.md`. LED modules, vehicle gateway, object detection and instrument cluster are **outside** (`A-05`, `A-13`, `A-04`) |
| Baseline | `04_architecture/ee_architecture.md`, `05_hardware/hw_architecture.md`, `06_software/sw_architecture.md`, `SM-01` … `SM-06` |
| Team (role model, not persons) | safety-analyst (lead), systems-engineer, hardware-engineer, software-engineer, verification-engineer |
| Not analysed | Manufacturing and assembly process (a process FMEA is out of scope for this project) |

## Step 2 — Structure analysis

The system elements are the **published element names**; no new name is introduced.

```
Item_LightingSystem
 +- ECU_LightingCtrl
 |   +- Power_Supply_Unit
 |   +- MCU_Lockstep
 |   +- ASIC_Watchdog
 |   +- LED_Driver_Stage_1..n      (low beam, high beam, work lamps, cornering)
 |   +- Current_Sense_Chain
 |   +- Temp_Sense_Chain
 |   +- CAN_FD_Transceiver
 |   +- LIN_Transceiver
 |   +- SWC_LightManager / SWC_HighBeamControl / SWC_HighBeamMonitor
 |      SWC_WorkLampControl / SWC_DiagnosticManager
 +- (outside) Vehicle_Gateway, headlamp modules, work-lamp fixtures, LIN actuator
```

The component-level structure and boundary statements are already written down in
`05_hardware/hw_components.md` section 2, and are used here rather than repeated.

## Step 3 — Function analysis

| Element | Function (what it must do) | Traced to |
|---|---|---|
| `LED_Driver_Stage_1..n` | Drive the commanded constant channel current and report its own status | `SYS-REQ-001`, `TSR-004` |
| `Current_Sense_Chain` | Report the true channel current within ±20 mA at the 150 mA threshold | `HW-REQ-001`, `SM-01` |
| `MCU_Lockstep` | Execute the lighting application and its monitoring deterministically | `TSR-002`, `TSR-003` |
| `ASIC_Watchdog` | Detect a stalled microcontroller on an independent time base and assert `SAFE_OFF` | `TSR-001`, `SM-02` |
| `Power_Supply_Unit` | Provide `VBAT_PROT`, the rails and `VREF`, and flag excursions | `HW-REQ-011` … `016`, `SM-06` |
| `Temp_Sense_Chain` | Report the module temperature to ±3 K for the derating function | `HW-REQ-022`, `SM-05` |
| `CAN_FD_Transceiver` | Carry the light request in and the status and driver warning out | `TSR-005`, `SYS-REQ-022` |
| `SWC_HighBeamMonitor` | Check the commanded high-beam state against speed and ambient light | `TSR-007` |
| `SWC_WorkLampControl` | Inhibit the work lamps above 10 km/h and on an invalid speed signal | `TSR-008` |

## Step 4 — Failure analysis

Failure effects are stated **at the vehicle and driver level**, causes at component level. The
failure modes are drawn from the P-diagram error states in `05_hardware/hw_components.md` section 5,
so the FMEA rates candidates rather than inventing them.

## Step 5 — Risk analysis: `B` / `A` / `E` and action priority

Column convention: **B** = Bedeutung (severity, 1–10) · **A** = Auftreten (occurrence, 1–10) ·
**E** = Entdeckung (detection, 1–10). **AP** = action priority **H / M / L**.

**How AP is assigned here.** The assignment follows the AIAG-VDA action-priority logic; the
handbook's table is not reproduced. The working rule applied, stated so a reviewer can recompute
every row:

- `B` 9–10 → **H** if `A` ≥ 4, or if `A` ≥ 2 and `E` ≥ 5; **M** if `A` 2–3 and `E` ≤ 4; **L** only
  at `A` = 1 with `E` ≤ 4.
- `B` 7–8 → **H** if `A` ≥ 4 or `E` ≥ 6; otherwise **M**.
- `B` ≤ 6 → **M**, or **L** where both `A` and `E` are ≤ 4.

Every **`AP = H`** row carries a named action and an owner, per the rule that an H row must produce
an `SM-xx`, a requirement or a `RISK-xx`. This phase may create neither `SM-` nor requirements, so
each H row terminates in a `RISK-` record or an open point addressed to the owning agent.

### 🔍 DEEP DIVE — Golden Thread rows (SG-01)

| ID | System element | Function | Failure effect (FE) | **B** | Failure mode (FM) | Failure cause (FC) | Prevention control | **A** | Detection control | **E** | **AP** | Action / owner |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `FM-01` | `LED_Driver_Stage_1` | Drive the commanded low-beam channel current | One low-beam channel dark at night; the road on that side is unlit (`H-01`) | 9 | No output current (E1) | Output stage open, solder-joint fatigue, connector fretting | Derated design, AEC-Q qualified parts, connector with secondary lock | 3 | `SM-01` open-load detection ≤ 80 ms; `HV-01` fault injection | 3 | **M** | No new action. FMEDA rows `D1`/`H1`, coverage confirmed at 92.2 % (`OP-15` closed) — safety-analyst |
| `FM-02` | `Current_Sense_Chain` | Report the true channel current | A **real** open load is never classified: no warning, no limp-home — `SG-01` violated | 10 | Sense chain stuck at a plausible value (E1/E3) | Amplifier output stuck, shunt solder joint, ADC input stuck | Kelvin-sensed shunt, clamp, second reference leg | 2 | `HW-REQ-005` off-phase zero-current self-test, fault after 20 ms | 4 | **M** | The row is `M` **only because of `HW-REQ-005`** — without it `E` ≈ 9 and `AP` = H. Action: fault injection into the off-phase branch, not only into the load — verification-engineer (extends `OP-19`) |
| `FM-03` | `ASIC_Watchdog` | Detect a stalled MCU and assert `SAFE_OFF` | Both low-beam channels de-energised at night with no prior warning — the mechanism **creates** `H-01` | 10 | Spurious trip (E2) | Time-base drift, EMC on the question/answer line, threshold drift | Independent oscillator, question/answer instead of a simple trigger | 3 | The ECU cannot distinguish its own commanded off-state from a fault | 8 | **H** | **`OP-34` / `RISK-03`** — differentiate the disable path by channel class. Until decided, the `SG-01` metrics are conditional — safety-manager, systems-engineer |
| `FM-04` | `Power_Supply_Unit` | Provide `VBAT_PROT` and the internal rails | Total loss of the low beam; no warning can even be transmitted | 10 | Loss of `VBAT_PROT` (E2/E5) | Reverse-polarity FET open, TVS degraded to a short, output capacitor open | Derating, TVS coordination, ISO 7637-2 qualification | 2 | None effective — an unpowered item cannot diagnose itself | 9 | **H** | **`OP-54`** — order-1 cut sets `MCS-1`/`MCS-2`, 9.90 FIT, 54 % of the SPF+RF residue. Accept with an argued residual risk or split the supply path — systems-engineer, safety-manager |

### 📋 OVERVIEW — breadth rows

| ID | System element | Function | Failure effect (FE) | **B** | Failure mode (FM) | Failure cause (FC) | Prevention control | **A** | Detection control | **E** | **AP** | Action / owner |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `FM-05` | `Power_Supply_Unit` | Provide a 3.3 V ±0.5 % ADC reference | Every ADC reading is biased at once; the 150 mA threshold shifts and `SM-01` mis-classifies | 8 | `VREF` drift inside the rail tolerance (E3) | Reference ageing, temperature coefficient, layout coupling | 0.5 % reference, separate reference leg, layout rules | 3 | `HW-REQ-010` reference plausibility, 100 ms | 4 | **M** | Confirmed by the FMEDA (`P3`, 1.35 FIT latent). Treated as coupling factor `CF-1` in the DFA — safety-analyst |
| `FM-06` | `MCU_Lockstep` | Execute the mixed-ASIL application without interference | A QM partition disturbs the ASIL B Golden Thread: wrong command, or the fault reaction is not executed in time | 8 | Memory or timing interference between partitions (E5) | MPU not configured, timing protection absent, shared MCAL driver | AUTOSAR OS-Applications, priority assignment, execution budgets | 4 | Protection-violation trap and `WdgM` — but **no test exercises it** | 6 | **H** | **`OP-48`** (no `HW-REQ` requires the MPU), **`OP-56`** (shared MCAL drivers asserted ASIL B, not shown), **`OP-58`** (no fault-injection test of the partition boundary) — hardware-engineer, software-engineer, verification-engineer |
| `FM-07` | `LED_Driver_Stage_n` (high beam) | De-energise the glaring segment | An oncoming driver is glared beyond the 500 ms FTTI (`SG-02`) | 7 | Stage will not switch off (E4) | Output FET failed short, enable gate defeated downstream | Separate monitor enable path (`TSR-007`), dominant `SAFE_OFF` | 3 | Monitor path plus `DriverStatus` readback | 4 | **M** | A short **downstream** of the enable gate is covered by neither path — `OP-57`, and `fta_sg02.md` section 4 — systems-engineer |
| `FM-08` | `SWC_WorkLampControl` | Inhibit the work lamps above 10 km/h | Work lamps energised at road speed; glare to oncoming traffic (`H-03`) | 7 | Inhibit defeated | Speed signal stale or invalid, E2E counter not evaluated | `TSR-008` incl. the signal-invalid case | 3 | E2E invalidation (`SYS-REQ-023`) and per-group timeout | 4 | **M** | No new action; verification owed by `OP-33` — verification-engineer |
| `FM-09` | `CAN_FD_Transceiver` | Carry the driver warning to the instrument cluster | The driver is not warned of a failed channel; the controllability rating of `H-01` loses its basis (`A-03`) | 6 | Warning frames lost | Bus-off not recovered, transceiver stuck dominant | Event-triggered frame plus 500 ms cyclic repetition, E2E | 3 | Bus-off status readback — **unspecified** | 6 | **M** | Confirms **`OP-31`** (bus-off recovery and status readback) — hardware-engineer |
| `FM-10` | `Temp_Sense_Chain` | Report the module temperature to ±3 K | Derating engages too late; LED junction above its limit, accelerated lumen depreciation | 5 | NTC reads low (E1) | NTC drift, divider tolerance, connector corrosion at the module | Plausibility band against the board sensor | 3 | `HW-REQ-022` open/short detection and plausibility band | 4 | **L** | No action. Runs against the thermal FTTI (`A-21`), not against `SG-01` |

**Ten rows, four of them on the Golden Thread** — the depth rule asks for at least three.

## Step 6 — Optimisation

Three rows carry `AP = H`. Each produces a concrete, owned action, and none of them is answered by
tightening a rating:

| Row | Why it is H | Action taken here | Where it goes next |
|---|---|---|---|
| `FM-03` | `B` 10 with an undetectable failure mode: the item cannot tell a commanded off-state from a spurious one | `RISK-03` created; the FMEDA and the `SG-01` FTA are marked conditional throughout | `safety-manager` decides `OP-34`. **Not** closed here |
| `FM-04` | `B` 10, `E` 9 — no detection is possible once the item is unpowered | Quantified as two order-1 cut sets (9.90 FIT) in `fta_sg01.md`; `OP-54` raised | `systems-engineer` / `safety-manager`: accept with argument, or change the supply architecture |
| `FM-06` | `A` 4 and `E` 6: the measures are configuration, and nothing verifies them | Examined as coupling factors `CF-6`/`CF-7` in `dfa_decomposition.md`; `OP-56`, `OP-58` raised, `OP-48` confirmed as still open | `hardware-engineer`, `software-engineer`, `verification-engineer` |

Two `M` rows are worth an explicit note, because "M" hides *why* they are not H:

- **`FM-02` is M because a requirement exists.** `HW-REQ-005` moves detection from ≈ 9 to 4. That is
  the single highest-leverage requirement in the Golden Thread, and it is the reason four fault-tree
  cut sets sit at order 3 rather than order 2. It must not be traded away in a cost review.
- **`FM-01` is M because `SM-01` works.** The FMEDA has now confirmed the coverage independently
  (92.2 %), so the detection rating of 3 has evidence behind it rather than optimism.

## Step 7 — Results documentation

| Question | Answer |
|---|---|
| Are all safety-goal-relevant system failure effects covered? | For `SG-01` yes, and cross-checked against the fault tree cut sets. For `SG-02` at `📋 OVERVIEW` depth only — deliberate |
| Was any candidate failure mode from `hw_components.md` rejected? | Yes: `LIN_Transceiver` `E1`–`E3` and `CAN_FD_Transceiver` `E2`–`E3` are not rated. `LIN` is QM and carries no safety goal; the CAN modes are answered at system level by the E2E protection and the hold-last-valid rule (`SYS-REQ-022` … `025`), which the FMEA would only restate |
| Does any row change a published value? | **No.** No FTTI, threshold, detection time or cap was touched |
| What does this FMEA *not* do? | It rates no manufacturing cause, and it does not quantify. Quantification is the FMEDA's job, and the two are cross-checked rather than merged |

---

**Work products:** `02_safety/05_analyses/fmea_system.md`
**Open points:** new `OP-54`, `OP-56`, `OP-57`, `OP-58`; `RISK-03` created; `OP-31` and `OP-48`
confirmed as still open and left with their owners; `OP-34` deliberately **not** closed.
**Process reference:** ASPICE **SYS.2** (system requirements analysis) and **SYS.3** (system
architectural design) as the consumers of the findings, with **SUP.9** (problem resolution) as the
route back · ISO 26262 **Part 9** (safety analyses — inductive analysis of failure modes and their
effects) · **Part 3** (HARA, as the origin of the severity ratings). AIAG-VDA FMEA handbook named by
topic. Parts and topics named, no clause numbers cited.
