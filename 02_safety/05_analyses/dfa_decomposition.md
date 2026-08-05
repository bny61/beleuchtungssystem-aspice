# DFA — dependent failure analysis of the `FSR-005` decomposition

**Phase 5 · ASPICE SWE.2 / SYS.3 as the consumers · ISO 26262-9 (analysis of dependent failures,
and criteria for coexistence of elements) · ISO 26262-6 (freedom from interference between software
elements of different ASIL)**
**Status:** draft · **Owner:** safety-analyst

> Teaching/reference project. All statements are plausible example values, not validated data.

---

## 1 What is being analysed, and what a positive result would mean

`FSR-005` (ASIL A) is decomposed into `FSR-006` **QM(A)** and `FSR-007` **A(A)**, realised as
`TSR-006` (`SWC_HighBeamControl`) and `TSR-007` (`SWC_HighBeamMonitor`). The decomposition is only
admissible if the two paths are **sufficiently independent**. `RISK-02` has said since phase 2 that
this is not demonstrated, and `OP-8` asked for this analysis.

**What a DFA can and cannot deliver.** It cannot prove independence. It enumerates the ways two
elements can fail together, states the countermeasure for each and names what is left over. A
decomposition is defensible when every coupling factor has a countermeasure whose effectiveness is
itself evidenced. Where the evidence is an assertion, the DFA says so and the residual stays.

`06_software/freedom_from_interference.md` is the input, and it says of itself: *"It is an argument,
not a proof."* This analysis takes that literally — it does not convert the argument into evidence
by citing it.

## 2 🔍 DEEP DIVE — coupling factors

| ID | Coupling factor | Description | Affected elements | Effect if it acts | Countermeasure | Residual risk |
|---|---|---|---|---|---|---|
| `CF-1` | **Common supply and reference** | One `Power_Supply_Unit` feeds the MCU rails, the ADC reference `VREF` and the driver stages. A rail excursion or `VREF` drift acts on both partitions and on every measurement at once | `Power_Supply_Unit`, `MCU_Lockstep`, both SWCs, `LED_Driver_Stage_n` | Control and monitor produce consistent-looking but equally wrong results; the AND gate of the `SG-02` fault tree degenerates | `SM-06` window comparators (≤ 10 ms) with hardware shutdown; `HW-REQ-010` reference plausibility on a second reference (100 ms); rail monitoring by `ASIC_Watchdog` (≤ 5 ms) | **Medium.** The UV/OV comparators themselves have **no power-up test required by any `HW-REQ`** — 6.75 FIT latent at zero coverage in the FMEDA (`P4`). A stuck comparator is a latent common-cause enabler. `OP-53` |
| `CF-2` | **Common clock / time base** | The monitor task and the control task run on the same MCU clock. The watchdog has an independent oscillator, but a drift *common* to MCU and watchdog is the classic monitor-defeat | `MCU_Lockstep`, `ASIC_Watchdog`, both partitions | Both partitions run slow or fast together; the monitor's 20 ms period stretches with the control path it is supposed to check, and neither notices | Physically separate oscillator in `ASIC_Watchdog`; question/answer with a *time window* rather than a simple trigger, so an answer that is correct but early or late fails (`HW-REQ-018`, verified by `HV-02`) | **Low–medium.** The window is the real measure and it is verified. Residual: a common environmental cause (temperature, supply ripple) shifting both oscillators in the same direction. This is `ASIC_Watchdog` `E3`, one of the three candidates `hw_components.md` handed to this analysis |
| `CF-3` | **Common ground / return path** | Both driver stages and the sensing chains share the ECU ground plane and the return path through the connector | `Power_Supply_Unit`, `Current_Sense_Chain`, `LED_Driver_Stage_1..n` | A ground offset biases the sense chain and the channel-voltage divider in the same direction, so the cross-check `SM-03` performs against `SM-01` loses its independence | Kelvin sensing at the shunt; the plausibility leg referenced to the same node deliberately, so an offset shows as an implausible pair rather than a consistent one; layout rules | **Medium.** Layout rules are a design intent, not a verified property. No `HV-xx` measures ground offset under full channel load |
| `CF-4` | **Thermal coupling** | All partitions execute on one die; all driver stages sit on one board in a cavity that reaches 105 °C (`A-20`) | `MCU_Lockstep`, `LED_Driver_Stage_1..n` | An over-temperature condition degrades control and monitor simultaneously; derating acts on all channels at once | Junction design limit 135 °C against a 150 °C rating (`A-20`), verified by `HV-05`; derating floor 400 mA (`HW-REQ-008`) keeps the low beam above the `SM-01` threshold | **Low.** Quantified, with a 15 K margin, and it is the one coupling factor with a measurement plan behind it |
| `CF-5` | **Spatial proximity** | One PCB, one housing, one output connector for both low-beam channels and for the high-beam channels | whole ECU | Mechanical damage, moisture ingress or a connector fault takes out both paths of a supposedly redundant pair | Per-channel independence of the current-set and enable circuitry; `HV-10` environmental and vibration testing with the channel current monitored for intermittent contact; IP protection | **Medium.** Genuine and unavoidable at this architecture: a single-ECU, single-connector design cannot be spatially independent. It is the reason `FSR-003` (limp-home on the remaining channel) needs section 4 below |
| `CF-6` | **Shared computing resource** | One lockstep core pair, one MPU, one OS, one RTE for all four OS-Applications | `MCU_Lockstep`, all SWCs | A fault in the MPU configuration or in the OS scheduler defeats every partition boundary at once — partitioning cannot protect against a failure of the partitioning | MPU-backed OS-Applications, priority assignment (`Task_Monitor_20ms` above `Task_HighBeam_50ms`), execution budgets, 42 % periodic load against a ≈ 73.5 % bound | **High.** The measures are *generated configuration*. Nothing verifies them, and **no `HW-REQ` requires the MPU or OS timing protection at all** (`OP-48`). This is the weakest row in the table |
| `CF-7` | **Shared software platform** | ADC, PWM timers and the CAN controller are reached through common MCAL drivers used by more than one partition; RTE and OS code are common to all | MCAL, RTE, OS | A reentrancy or state fault in a shared driver is a common-cause failure that no partition boundary sees, because the driver runs on behalf of both | The driver code is stated to be part of the ASIL B qualified set | **High.** That statement is an assertion. No qualification evidence, tool-confidence record or supplier safety manual is identified — `OP-56` |
| `CF-8` | **Common actuation path** | `SAFE_OFF` reaches the enable gate of **every** driver stage, from every partition's point of view identically | `ASIC_Watchdog`, `LED_Driver_Stage_1..n` | One event de-energises the high beam *and* the low beam. For `SG-02` that is benign; for `SG-01` it is the hazard itself | Under the working assumption of this phase: `SAFE_OFF` differentiated by channel class (`OP-34`) | **High and unresolved.** The differentiation is assumed, not decided — `RISK-03`. Additionally, the `SAFE_OFF` path has **no power-up test required by any `HW-REQ`**: 4.40 FIT latent at zero coverage (`D5` in the FMEDA), `OP-52` |
| `CF-9` | **Shared development tool** | One compiler, one configuration generator, one static analyser for the QM(A) and the A(A) code | build tool chain | A code-generation or optimisation fault affects both partitions identically; a systematic fault is duplicated rather than diversified | Tool confidence work is planned but not performed (`OP-50`); MISRA C:2012 with two documented deviations and a static-analysis gate | **Medium.** Ordinary and accepted practice at ASIL A/B, but the tool-confidence record does not yet exist |
| `CF-10` | **Common systematic cause** | Control and monitor derive from the same requirement set, are written against the same interpretation of the object-list semantics, and are reviewed by the same people | `FSR-006`/`FSR-007`, `TSR-006`/`TSR-007` | A misunderstanding of "which segment is glaring" is implemented identically in both paths, so the monitor confirms the control path's error | Different input signals and a different algorithm: the monitor checks *plausibility against speed and ambient light*, not the segment computation. That is functional diversity, not redundancy | **Low–medium.** The diversity is real and is the strongest single element of the independence argument. Residual: both still depend on `SG-02` being correctly understood |
| `CF-11` | **Common input data — absent by design** | Control uses `ObjectList`; the monitor uses `VehicleSpeed` and `AmbientLight`. No signal is shared, and the data flow is one-way, control → monitor | interface table, `SWC_HighBeamControl`, `SWC_HighBeamMonitor` | — | Deliberate: `OBJ_List_1` is left un-E2E-protected precisely so that no protected channel runs into a QM function; the monitor's inputs are E2E-protected groups | **Low.** This is the row that works. Residual: a stale-but-not-timed-out monitor input (`OP-29`) and the total absence of `ObjectList`, for which no requirement exists (`OP-57`) |

## 3 The three coupling candidates handed over by `hw_components.md`

Section 5 of `05_hardware/hw_components.md` named three error states as *more than local faults* and
said the DFA owed an answer for each. Here they are:

| Candidate | Answer |
|---|---|
| `Power_Supply_Unit` `E3` — a common `VREF` biasing every reading | **Confirmed as a coupling factor** (`CF-1`), not as a local fault. The countermeasure exists (`HW-REQ-010`, second reference, 100 ms) and the FMEDA prices the residue at 1.35 FIT latent. What is *not* covered is the monitoring hardware of `SM-06` itself — `OP-53` |
| `ASIC_Watchdog` `E3` — a time base drifting with the part it monitors | **Confirmed as a coupling factor** (`CF-2`). The effective countermeasure is not the separate oscillator but the *time window* in the question/answer protocol, and that is verified by `HV-02`. Residual: a common environmental driver of both oscillators, unquantified |
| `MCU_Lockstep` `E5` — mixed-ASIL software on one part | **Confirmed, and it is the weakest point of the whole decomposition** (`CF-6`, `CF-7`). The measures are configuration; no requirement demands the platform capability; no test exercises a partition boundary |

## 4 🔍 The other independence claim nobody asked about: `FSR-003`

`FSR-003` — *"while only one low-beam channel has failed, continue to operate the remaining
channel"* — is the safe state of `SG-01`, and its own rationale says it *"presumes freedom from
interference between the channels"*. That presumption has never been analysed. It is analysed here
because the `SG-01` fault tree depends on it: cut set family `{Bi, B15}` is exactly the case where
the presumption fails.

| Coupling between the two low-beam channels | Effect | Countermeasure | Residual |
|---|---|---|---|
| Common `VBAT_PROT` and input protection | Both channels lost together | none | **This is `MCS-1`/`MCS-2`, the two order-1 cut sets, 9.90 FIT.** `OP-54` |
| Common enable-gate logic and `SAFE_OFF` | Both channels de-energised together | Channel-class differentiation (`CF-8`) | Assumed, not decided — `RISK-03` |
| Common output connector | One connector fault kills both | Per-channel pins, secondary lock, `HV-10` vibration | Medium; a connector-level common cause remains |
| Shared driver IC package (if both channels sit in one part) | One package fault kills both | Component selection has not been made | **Open**: the component choice has not yet been constrained to two separate packages. Folded into `OP-54` |
| Shared sense chain | Would make one blind sensor blind both channels | Per-channel shunt and amplifier — **separate by design** | Low. This one is genuinely independent |

**Finding:** the limp-home safe state of `SG-01` rests on channel independence that is real in the
sensing path and absent in the supply and enable paths. That is not a new discovery — it is the same
finding as `OP-54`, arrived at from the opposite direction, which is the sort of agreement between
two analyses that is worth writing down.

## 5 Verdict on `RISK-02` and `OP-8`

| Question | Answer |
|---|---|
| Does the DFA exist? | **Yes.** `OP-8` is closed on delivery |
| Is the `FSR-005` decomposition **supportable**? | **Yes, in structure.** `CF-10` and `CF-11` — functional diversity and disjoint inputs — carry a genuine independence argument, and the monitor's separate enable path means it can act without the control path's cooperation |
| Is it **demonstrated**? | **No.** Three coupling factors carry a *high* residual: `CF-6` (partitioning verified by nothing, and required by no `HW-REQ` — `OP-48`), `CF-7` (shared MCAL qualification asserted — `OP-56`), `CF-8` (common actuation path, and `OP-34` undecided) |
| Can the safety case cite this? | It may cite the analysis and its structure. It may **not** yet cite independence as established |

**`RISK-02` is answered but not discharged.** Its mitigation ("DFA in phase 5") is delivered; its
substance now has three named, owned conditions instead of one unnamed one. That is progress and it
is not closure, and the record is updated to say exactly that rather than being marked done.

**`OP-48` is inherited, explicitly.** The whole of section 4 of `freedom_from_interference.md` — and
therefore rows `CF-6` and `CF-7` of this table — rests on an MPU and OS timing protection that **no
hardware requirement demands**. This analysis cannot fix that, and it must not pretend the weakness
stops at the software document: **the conclusion of this DFA inherits it.** If the selected
microcontroller has no MPU, or if timing protection is not enabled in the delivered configuration,
`CF-6` has no countermeasure at all and the decomposition falls back — `FSR-006` would have to be
ASIL A rather than QM(A), with the corresponding requirements on the control path. `OP-48` stays
open and stays with `hardware-engineer`.

## 6 Findings

| Finding | Action | Owner |
|---|---|---|
| `CF-1` residual: no power-up test of the `SM-06` comparators; 6.75 FIT latent at DC 0 % | `OP-53` | hardware-engineer |
| `CF-8` residual: no power-up test of the `SAFE_OFF` path to the enable gate; 4.40 FIT latent at DC 0 % | `OP-52` | hardware-engineer |
| `CF-7`: ASIL B qualification of the shared MCAL drivers is asserted, not shown | `OP-56` | software-engineer |
| `CF-6`: nothing tests a partition boundary | `OP-58` | verification-engineer |
| `CF-6`/`CF-7`: no `HW-REQ` requires MPU or timing protection | `OP-48` confirmed, **not** closed | hardware-engineer |
| `CF-8`: `SAFE_OFF` common to every channel class | `RISK-03`; `OP-34` **not** closed | safety-manager, systems-engineer |
| `FSR-003` channel independence broken in the supply and enable paths | folded into `OP-54` | systems-engineer, safety-manager |
| `CF-9`: no tool-confidence record | `OP-50` confirmed, unchanged | config-manager, quality-assessor |

---

**Work products:** `02_safety/05_analyses/dfa_decomposition.md`; change note on `RISK-02.md`
**Open points:** `OP-8` **closed** (the DFA exists); `RISK-02` answered with three named residuals
and deliberately **not** discharged; new `OP-52`, `OP-53`, `OP-56`, `OP-58`; `OP-48` and `OP-34`
confirmed open and left with their owners.
**Process reference:** ASPICE **SWE.2** (software architectural design, resource and partitioning
considerations) and **SYS.3** (system architectural design) as consumers · ISO 26262 **Part 9**
(analysis of dependent failures; criteria for coexistence of elements) · **Part 6** (freedom from
interference between software elements of different ASIL) · **Part 3** (ASIL decomposition, as the
origin of `FSR-006`/`FSR-007`). Parts and topics named, no clause numbers cited.
