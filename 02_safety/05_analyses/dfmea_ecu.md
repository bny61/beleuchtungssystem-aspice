# DFMEA — `ECU_LightingCtrl` assembly (5-row extract)

**Phase 5 · ASPICE HWE.2 (hardware design) · ISO 26262-9 (safety analyses, inductive analysis) ·
ISO 26262-5 (hardware development) · AIAG-VDA FMEA handbook, seven-step method — named by topic**
**Status:** draft · **Owner:** safety-analyst

> Teaching/reference project. **All ratings are plausible example values, not validated data.**
> **No RPN is computed.**

---

## 1 Why this is a five-row extract, and how the five were chosen

`05_hardware/hw_components.md` section 5 offers **38 candidate failure modes** from the eight
P-diagrams, ten of them on the Golden Thread. The candidates are exactly that: the DFMEA rates them
and may reject them. This extract takes five and says why, because "we picked five" is not a
selection method.

| # | Candidate taken | Why this one |
|---|---|---|
| `D-01` | `Current_Sense_Chain` **E1** — reads high, `SM-01` blind | Golden Thread. The only candidate whose effect is *nothing visibly happening* — the mechanism reports "healthy" while the channel is dead. The `hw_components.md` reading guidance warns explicitly that `E1` and `E2` must not be rated alike; this row is the test of whether the DFMEA obeyed that |
| `D-02` | `LED_Driver_Stage_1..n` **E1** — no output | Golden Thread. The failure the whole thread exists to detect; without it the FMEDA row `D1` and the fault-tree events `B5`/`B7` have no design-level counterpart |
| `D-03` | `ASIC_Watchdog` **E2** — spurious trip | Golden Thread. The only candidate where the **safety mechanism itself** produces the hazard, and the design-level face of `OP-34` / `RISK-03` |
| `D-04` | `Power_Supply_Unit` **E3** — `VREF` drift | One of the three candidates `hw_components.md` names as *more than a local fault*. Rated here because the design controls are local (reference choice, layout); the *coupling* is handled in the DFA |
| `D-05` | `MCU_Lockstep` **E5** — interference between ASIL B and QM partitions | The second of the three coupling candidates, and the one with the weakest design control: the measures are software configuration and no `HW-REQ` demands the platform feature (`OP-48`) |

**The third coupling candidate — `ASIC_Watchdog` `E3`, a time base that drifts with the part it
monitors — is deliberately *not* a DFMEA row.** A common-cause failure between a monitor and its
monitored element is not a component design fault; rating it with occurrence and detection would
produce a number that says nothing about the dependency. It is analysed as coupling factor `CF-2`
in [`dfa_decomposition.md`](dfa_decomposition.md).

**Candidates deliberately rejected in this extract**, so the omission is visible: `LIN_Transceiver`
`E1`–`E3` (QM, no safety goal depends on it), `Temp_Sense_Chain` `E1`–`E4` (runs against the thermal
FTTI of `A-21`, covered by `SM-05` and `HV-05`), and `CAN_FD_Transceiver` `E1`–`E2` (answered at
system level by `SYS-REQ-022` … `025`; the DFMEA would only restate the requirement).

## 2 Ratings and AP

`B` severity · `A` occurrence · `E` detection, each 1–10. **AP** = action priority H / M / L,
assigned by the same working rule stated in [`fmea_system.md`](fmea_system.md) step 5; the AIAG-VDA
table itself is not reproduced.

**A DFMEA rates *design* controls.** Prevention is what the design does to stop the cause arising;
detection is what the **design verification** would find before release — the `HV-xx` entries of
`05_hardware/hw_verification_plan.md`, simulation, and design review. It is not the in-vehicle
diagnosis; that is what the System-FMEA rated, and the two detection columns are deliberately
different.

## 3 🔍 DEEP DIVE / 📋 OVERVIEW — the five rows

| ID | Component (focus element) | Function | Failure effect (FE) | **B** | Failure mode (FM) | Failure cause (FC) | Prevention control (design) | **A** | Detection control (design verification) | **E** | **AP** | Action / owner |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `D-01` 🔍 | `Current_Sense_Chain` | Report the true channel current within ±20 mA at 150 mA | `SM-01` reports "healthy" while the channel is dead: the open load is never classified, no warning, no limp-home — `SG-01` violated | 10 | **E1** reads high / stuck at a plausible value | Amplifier output stage stuck, shunt Kelvin joint cracked, ADC input latched, offset drift beyond the budget | Kelvin-sensed shunt, gain 50 V/V with `Vos` ≤ 150 µV RTI, clamp to the ADC range, **off-phase zero-current branch by design** (`HW-REQ-005`), second reference leg (`HW-REQ-010`) | 2 | `HV-01` fault injection: shunt open/short, amplifier input shorted, reference shifted, over −40 … +85 °C and 20 … 100 % duty; tolerance-chain simulation of `analysis_current_sensing.md` | 4 | **M** | Extend `HV-01` so the **off-phase branch itself** is injected (self-test disabled, wrong window) — today the plan injects the load, not the self-test. verification-engineer, extends `OP-19` |
| `D-02` 🔍 | `LED_Driver_Stage_1..n` | Drive the commanded constant channel current | One low-beam channel dark at night (`H-01`) | 9 | **E1** no output | Output FET open, inductor solder joint, current-set resistor open, enable gate stuck de-asserted | Derated output stage, AEC-Q qualified parts, per-channel independence, soft start ≥ 5 ms (`HW-REQ-027`) | 3 | `HV-01` (string disconnect at the connector), `HV-13` (activation timing on both channels), `HV-10` vibration with the channel current monitored for intermittent contact | 3 | **M** | No new action. Covered by `SM-01` at a coverage the FMEDA has now confirmed (92.2 %) |
| `D-03` 🔍 | `ASIC_Watchdog` | Detect a stalled MCU on an independent time base and assert `SAFE_OFF` | Both low-beam channels de-energised at night, no prior warning — the mechanism produces `H-01` | 10 | **E2** trips spuriously | Time-base drift, EMC coupling on the question/answer lines, threshold drift, marginal answer timing | Independent oscillator, question/answer rather than a simple trigger, guard band on the answer window, `HW-REQ-018` | 3 | `HV-02` (withheld/wrong/mistimed answer, clock stopped), `HV-09` EMC immunity with the low beam on | 7 | **H** | **`RISK-03`, `OP-34`.** The design cannot make this row `M` — a correct trip and a spurious trip are the same electrical event. The answer is the *reaction*: differentiate `SAFE_OFF` by channel class so the low beam goes to a hardware default state instead of dark — safety-manager, systems-engineer |
| `D-04` 📋 | `Power_Supply_Unit` | Provide a 3.3 V ±0.5 % ADC reference | Every ADC reading in the ECU is biased at once; the `SM-01` threshold shifts with no other symptom | 8 | **E3** `VREF` drift | Reference ageing, temperature coefficient, load regulation from a shared reference pin, layout coupling | 0.5 % reference, buffered and separately filtered, **second reference leg for the plausibility check** (`HW-REQ-010`), layout rules | 3 | `HV-06` (rails forced out of tolerance), `HV-01` (reference shifted deliberately), thermal-drift simulation of the tolerance chain | 4 | **M** | Local design control accepted. The **coupling** — one reference feeding current sensing, temperature sensing and the plausibility leg — is `CF-1` in the DFA and is where the residual sits — safety-analyst |
| `D-05` 📋 | `MCU_Lockstep` | Execute the mixed-ASIL application without interference | A QM partition corrupts data or starves a task of the ASIL B Golden Thread: wrong command, or the fault reaction misses the 150 ms budget | 8 | **E5** interference between ASIL B and QM partitions | MPU region wrongly generated, timing protection not enabled, shared MCAL driver reentrancy, one core and one clock for all partitions | AUTOSAR OS-Applications with MPU-backed regions, priority assignment, execution budgets, no shared writable data (`06_software/freedom_from_interference.md`) | 4 | **None at hardware DV level.** No `HV-xx` exercises a partition boundary, and no `HW-REQ` even requires the MPU | 7 | **H** | **`OP-48`** (platform capability required by no `HW-REQ`), **`OP-56`** (shared MCAL drivers asserted ASIL B, not shown), **`OP-58`** (no fault-injection test from the QM(A) partition). The prevention control is *configuration*, and configuration verified by nothing is not a control — hardware-engineer, software-engineer, verification-engineer |

## 4 Optimisation — the two `AP = H` rows

| Row | The honest statement | What is **not** done |
|---|---|---|
| `D-03` | Detection cannot be improved by design: the watchdog trip is electrically identical whether it is right or wrong. The severity is the reaction, not the detection | No new `SM-`. No rating tuned down "because `SM-02` is qualified" |
| `D-05` | The occurrence rating of 4 reflects that the causes are generated configuration, and the detection rating of 7 reflects that nothing in the hardware verification plan tests them | No credit taken for the partitioning argument. `freedom_from_interference.md` says of itself that it is an argument and not a proof, and the DFMEA takes it at its word |

Both terminate in an existing or new open point rather than in a requirement, because this phase
creates neither `SM-` nor `HW-REQ`/`SW-REQ`. That is a deliberate constraint, and it means these two
rows stay open until their owners act.

---

**Work products:** `02_safety/05_analyses/dfmea_ecu.md`
**Open points:** confirms `OP-48`; new `OP-56`, `OP-58`; `RISK-03` referenced; extension of `OP-19`
requested for the `HV-01` off-phase branch. `OP-34` deliberately **not** closed.
**Process reference:** ASPICE **HWE.2** (hardware design) with **HWE.3** as the consumer of the
detection column · ISO 26262 **Part 5** (hardware development, hardware architectural design) ·
**Part 9** (safety analyses — inductive analysis at design level). AIAG-VDA FMEA handbook named by
topic. Parts and topics named, no clause numbers cited.
