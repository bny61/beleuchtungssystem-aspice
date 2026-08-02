# Project status — current state and open points

> This file is the re-entry point. It is updated at the end of every phase.
> Last update: after the E/E architecture refinement (systems-engineer + hardware-engineer,
> between phase 4 and phase 5).

## Phase status

| Phase | Content | Status | Lead |
|---|---|---|---|
| 0 | Project frame, stakeholders, roles, tailoring, glossary | **skipped** | safety-manager, config-manager |
| 1 | Customer requirements `CR-001 … CR-028` (SYS.1) | **complete** (draft) | systems-engineer |
| 2 | Item definition, HARA, safety goals, FSC (ISO 26262-3) | **complete** (draft) | safety-manager |
| 3 | `SYS-REQ`, `TSR`, E/E architecture (SYS.2, SYS.3) | **complete** (draft) | systems-engineer |
| 4 | MBSE model, MagicGrid, 8 SysML views | **complete** (draft) | mbse-modeler |
| 4a | E/E architecture refinement — bus catalogue, timing, HW architecture detail | **complete** (draft) | systems-engineer, hardware-engineer |
| 5 | FMEA, DFMEA, FTA, FMEDA, DFA, STPA | **next phase** | safety-analyst |
| 6 | Hardware (HWE.1–4, Part 5) | **partly pulled forward** in 4a | hardware-engineer |
| 7 | Software (SWE.1–6, Part 6) | open | software-engineer |
| 8 | Verification & validation (SYS.4, SYS.5) | open | verification-engineer |
| 9 | Safety case, confirmation measures | open | safety-manager, quality-assessor |
| 10 | GitHub configuration management and evidence | partly prepared | config-manager |
| 11 | Traceability & metrics | open | config-manager, quality-assessor |

**Phase 0 was skipped** and needs to be caught up — the role model, independence levels and
tailoring decisions are missing but will be required at the latest for phase 9.

## Results so far

- **28 customer requirements** `CR-001 … CR-028`, covering all categories of the customer
  specification. Three of them (`CR-002`, `CR-005`, `CR-016`) are **deliberately weak** and marked
  as such in the `rationale` field (teaching purpose).
- **SYS.1 increment "illuminance" (after phase 4a):** `CR-024` … `CR-028` add the photometric side
  of the adaptive front lighting — base level at 75R, glare limit at B50L, the degraded-channel
  case, the AFS mode-change time and the stability band. All five are `asil: QM` **as a
  placeholder only**; the classification is the safety-manager's (`OP-41`). `CR-026` is
  deliberately left unquantified so that it cannot contradict the `SG-01` safe state, see `OP-38`.
  Measuring convention: `A-22`. No `SYS-REQ` is derived from them yet — the derivation follows in
  the next SYS.2 increment, after the ASIL of `OP-41` is settled.
- **7 hazards** `H-01 … H-07`, six of them with a safety goal, one resulting in QM.
- **2 safety goals**: `SG-01` (ASIL B, Golden Thread) and `SG-02` (ASIL A, second thread).
- **8 FSR** `FSR-001 … FSR-008`, incl. the ASIL decomposition
  `FSR-005 → FSR-006 QM(A) + FSR-007 A(A)`.
- **Timing budget SG-01** closes: 80 ms detection + 150 ms reaction = 230 ms < FTTI 300 ms.
  (Phase 2 stated 70 ms / 220 ms; the tolerance analysis of the current sensing raised the
  detection time to 80 ms — worst case 77.6 ms in the chain-A analysis of `ee_architecture.md`.)
- **Documented phase 2 work products:** `02_safety/01_item_definition/item_definition.md`,
  `02_safety/02_hara/hara.md`, `operational_situations.md`, `sec_classification.md`.
- **Phase 3 refinement of `SYS-REQ-014`** (hardware-engineer): tolerance analysis of the current
  sensing closed. `SYS-REQ-014` split, `SYS-REQ-015` … `SYS-REQ-019` and `HW-REQ-001` … `HW-REQ-010`
  created, `SM-01` detection time 70 → 80 ms, diagnostic coverage 90 % made conditional.
  Analysis: `05_hardware/analysis_current_sensing.md`.
- **Phase 3:** 15 further system requirements (`SYS-REQ-001` … `013`, `020`, `021`), 8 technical
  safety requirements `TSR-001` … `TSR-008` incl. the decomposed pair `TSR-006 QM(A)` /
  `TSR-007 A(A)`, E/E architecture with interface table and TSR allocation matrix
  (`04_architecture/ee_architecture.md`). ASIL of all customer requirements set from the HARA.
- **Phase 4:** MagicGrid matrix and the eight SysML views as PlantUML
  (`03_model/magicgrid.md`, `03_model/plantuml/`), function allocation
  (`04_architecture/allocation.md`). PlantUML installed locally, all ten diagrams
  syntax-checked and rendered.
- **Architecture refinement (4a), systems side:** CAN FD / SAE J1939 message catalogue at frame
  level and the bus load / timing analysis (`04_architecture/ee_architecture.md`, now 7 sections),
  closing `OP-21` and `OP-22`. Seven new system requirements `SYS-REQ-022` … `SYS-REQ-028` for
  end-to-end protection (alive counter, checksum, data identifier), invalidation on mismatch and on
  timeout, hold-last-valid for the low beam, the event-triggered warning frame and the ECU transmit
  budget. Interface table gained an `Integrity` column and the missing `IgnitionStatus` row.
  SG-01 chain A: **77.6 ms detection + 150 ms reaction = 230 ms** against FTTI 300 ms, and the chain
  is bus-independent. Lighting signal set ≈ 1.9 % bus load, segment ≈ 37 %.
- **Architecture refinement (4a), hardware side:** `05_hardware/hw_architecture.md` plus four
  analyses (supply and transients, thermal derating, SM-01 coverage, HW verification plan with
  `HV-01` … `HV-12`). New records `HW-REQ-011` … `HW-REQ-025` (supply ranges 9–36 V, clamped load
  dump 58 V / 400 ms, ISO 7637-2 pulse classes, reverse polarity, rail and watchdog monitoring,
  enable-gate topology, short-to-battery, overcurrent, thermal derating, CAN transceiver
  robustness) and safety mechanisms `SM-02` … `SM-06`, each with an explicit FTTI budget.
  `ibd_ecu.puml` rewritten as a hardware view; new `ibd_current_sense_chain.puml` as the
  🔍 DEEP DIVE of the Golden Thread element.
  **`OP-16` closed:** the 400 mA derating floor is confirmed — the degraded heat path at 105 °C
  cavity reaches T_j ≈ 130 °C, 5 K below the 135 °C design limit. **`OP-24` and the hardware side
  of `OP-4` closed.**
- **`SM-01` coverage made checkable rather than assertive:** bare scheme 59.4 %, all four measures
  93.0 %; dropping any single measure gives 84.5 / 79.9 / 85.0 / 89.0 %, so none is optional. The
  90 % claim stays conditional until the FMEDA confirms it (`OP-15`).
- Traceability check green, **110 records**, requirements coverage 81/94 = 86 %.

### Housekeeping from the parallel refinement

The two agents ran concurrently and both appended assumptions numbered `A-14` … `A-17`. The
collision was resolved **before any commit** by renumbering the hardware set to
**`A-18` … `A-21`** (supply interruption, central load-dump suppression, thermal model, thermal
FTTI); the systems set keeps `A-14` … `A-17` (bus segment, gateway E2E counterpart, placeholder
PGNs, gateway forwarding time). All references were updated; `A-01` … `A-21` are unique. Two further
reconciliations: `ibd_ecu.puml` annotated `CAN_FD_Transceiver` with `HW-REQ-024` (the thermal
requirement) instead of `HW-REQ-025`, and `HW-REQ-004` lacked the variant marking that the phase 3
`OP-17` decision implies. Both fixed.

## Open points

| ID | Point | Owner | Due |
|---|---|---|---|
| OP-1 | ~~Carry the ASIL of the `tbd` customer requirements over from the HARA~~ | systems-engineer | **done** (phase 3) |
| OP-2 | ~~Behaviour outside the normal supply range is missing~~ — undervoltage in `SYS-REQ-013`, overvoltage and load dump in `HW-REQ-011` … `HW-REQ-016`. Residual: the system-level requirement for < 9 V / > 32 V, see `OP-36` | systems-engineer, hardware-engineer | **done** (4a) |
| OP-3 | `CR-007` is not atomic (detection + indication); change only via a requirement-change issue | systems-engineer | before baseline |
| OP-15 | Confirm the 90 % diagnostic coverage of `SM-01` against the FMEDA — blocks `SM-01` returning to `reviewed` | safety-analyst | Phase 5 |
| OP-16 | ~~Feasibility of the 400 mA derating floor (`HW-REQ-008`, `A-12`)~~ — confirmed by the load-line analysis, condition captured as `HW-REQ-024` | hardware-engineer | **done** (4a) |
| OP-17 | ~~Decide the gating scheme below the minimum PWM on-time~~ — decided for `SYS-REQ-017` ("diagnosis not available"); `HW-REQ-004` not implemented in the base variant | systems-engineer | **done** (phase 3) |
| OP-18 | ~~Decide whether per-string current sensing is added~~ — decided against; channel voltage (`HW-REQ-006`) covers the failure mode. Revisit after the FMEDA (`OP-23`) | systems-engineer | **done** (phase 3) |
| OP-19 | New test cases for `HW-REQ-001` … `HW-REQ-025`, `SM-02` … `SM-06` and `HV-01` … `HV-12` | verification-engineer | Phase 8 |
| OP-20 | Re-review `SYS-REQ-014`, `SM-01` and `TC-021` — dropped to `draft` by the refinement | safety-manager | Phase 3 |
| OP-21 | ~~CAN FD / J1939 message catalogue and signal encoding at frame level~~ — `ee_architecture.md` section 3; residual items split to `OP-27` / `OP-28` | systems-engineer | **done** (4a) |
| OP-22 | ~~Bus load and timing analysis for the cycle times of the interface table~~ — `ee_architecture.md` section 4; residual assumption `A-14` | systems-engineer | **done** (4a) |
| OP-23 | Revisit the decision against per-string sensing after the FMEDA | safety-analyst | Phase 5 |
| OP-24 | ~~Overvoltage and load-dump behaviour undefined~~ — operating-range table, clamped load dump, `HW-REQ-011` … `HW-REQ-016` | hardware-engineer | **done** (4a) |
| OP-4 | Function class per ISO 7637-2 pulse — **hardware side done** (pulse/class table in `analysis_supply_and_transients.md`); the `CR-017` text still has to be corrected, see `OP-35` | hardware-engineer, systems-engineer | **partly done** (4a) |
| OP-5 | Replace the weak requirements `CR-002`, `CR-005`, `CR-016` before a real baseline | quality-manager | before baseline |
| OP-6 | ~~Normalise the ASCII transliteration in the records to proper umlauts~~ | config-manager | **obsolete** — resolved by the translation to English |
| OP-7 | `RISK-01`: confirm the E rating of H-01 (E3 vs. E4) in the confirmation review | safety-manager | Phase 9 |
| OP-8 | `RISK-02`: perform the DFA for the decomposition of `FSR-005` | safety-analyst | Phase 5 |
| OP-9 | Plan `A-03` (driver response to the warning) as a validation target at vehicle level | verification-engineer | Phase 8 |
| OP-10 | Interface agreement (DIA) for the object detection outside the item boundary (`A-05`) | safety-manager | Phase 3 |
| OP-11 | ~~Create `RISK-01`/`RISK-02` as records~~ | config-manager | **done** |
| OP-12 | ~~Syntax-check the context diagram~~ — PlantUML installed; both existing diagrams were in fact broken (`skinparam` single-line block) and are fixed | mbse-modeler | **done** (phase 4) |
| OP-25 | No behavioural views for the `SG-02` thread (state machine and sequence cover the low beam only) | mbse-modeler | Phase 5 |
| OP-26 | Freedom-from-interference view for `SWC_HighBeamControl` QM(A) vs. `SWC_HighBeamMonitor` A(A) — needs the SW architecture | software-engineer | Phase 7 |
| OP-27 | Confirm PGNs, source addresses and the background bus load against the OEM J1939 database (`A-14`, `A-16`) | systems-engineer | before baseline |
| OP-28 | Agree E2E data identifiers, CRC parameters and counter handling with the gateway supplier (`A-15`) | safety-manager | Phase 7 |
| OP-29 | `AmbientLight` timeout (500 ms) equals the SG-02 FTTI — decide between a shorter timeout and a staleness reaction in `SWC_HighBeamMonitor` | safety-manager | Phase 5 |
| OP-30 | ~~`HW-REQ-004` lacks the variant marking implied by the `OP-17` decision~~ | hardware-engineer | **done** (4a) |
| OP-31 | `CAN_FD_Transceiver`: bus-off recovery, wake behaviour and fault-status readback still unspecified (`HW-REQ-025` covers only bus short / dominant timeout) | hardware-engineer | Phase 6 |
| OP-32 | ~~`ibd_ecu.puml` missing `CAN_FD_Transceiver` and `LIN_Transceiver`~~ | mbse-modeler | **done** (4a) |
| OP-33 | Verification methods and test cases for `SYS-REQ-022` … `SYS-REQ-028` (E2E fault injection, bus load and latency measurement) | verification-engineer | Phase 8 |
| OP-34 | **`SM-02` conflicts with `SG-01`**: `TSR-001` de-energises the driver stages on SAFE_OFF — applied to the low beam that is exactly `H-01`. Differentiate the disable path by channel class | safety-manager, systems-engineer | Phase 5 |
| OP-35 | `CR-017` demands "no loss of function for all pulses", which is neither designed nor achievable; reword against the pulse/class table | systems-engineer | before baseline |
| OP-36 | Missing `SYS-REQ` for behaviour below 9 V / above 32 V and for thermal derating — `HW-REQ-023` carries ASIL B but hangs off the QM requirement `CR-014` | systems-engineer | Phase 5 |
| OP-37 | Interface table additions from the hardware view: `U_Batt`, `RailStatus`, and `SAFE_OFF` / `OV_SHUTDOWN` into the enable gate | systems-engineer | Phase 5 |
| OP-38 | Photometric compliance at the 400 mA floor (≈ 232 lm/channel) against the legal minimum — affects the `SG-01` safe state and `SYS-REQ-013`, not only the derating curve | safety-manager, systems-engineer | Phase 5 |
| OP-39 | `A-19` (central load-dump suppression) needs an interface agreement with the vehicle manufacturer, like `A-05` | safety-manager | Phase 6 |
| OP-40 | `A-12` ("the derating curve never commands below 400 mA") restates `HW-REQ-008`, which requires exactly that. Since the requirement exists, the assumption should be confirmed or marked superseded rather than left `open` — an assumption and a requirement asserting the same thing invite them to drift apart | hardware-engineer | Phase 6 |
| OP-41 | ASIL of the illuminance requirements `CR-024` … `CR-028` is unassigned — all five carry `asil: QM` as a placeholder. Classify them from the HARA, as was done for the `tbd` records in `OP-1`; `CR-024`/`CR-026` touch `SG-01`, `CR-025` touches `SG-02` | safety-manager | Phase 5 |
| OP-13 | Catch up phase 0: role model, independence levels, tailoring, glossary | safety-manager | before phase 9 |
| OP-14 | ~~HARA and item definition existed only in chat, not as work products~~ | safety-manager | **done** |

## Next step

**Phase 5** — safety analyses: System-FMEA and DFMEA per AIAG-VDA with B/A/E and AP, FTA with
minimal cut sets, FMEDA with SPFM/LFM/PMHF against the ASIL B targets, DFA for the decomposed path,
STPA, verification matrix. Points to observe:

- The DFA is blocking: `RISK-02` states the decomposition `TSR-006` / `TSR-007` is not demonstrated
  until it exists.
- The FMEDA must re-derive the diagnostic coverage of `SM-01`; the 90 % claim is conditional
  (`OP-15`) and the bare scheme is worth about 60 %.
- `OP-23`: the decision against per-string sensing has to be revisited against the FMEDA result.
- **New input from 4a:** `05_hardware/analysis_sm01_coverage.md` decomposes the SM-01 claim into six
  failure-mode groups with a per-measure contribution and a sensitivity table. The FMEDA should
  confirm or reject that decomposition rather than start from scratch.
- **New input from 4a:** `SM-02` … `SM-06` now exist with declared detection/reaction times and
  FTTI budgets, and the coverage figures in them are marked as **unconfirmed targets** owned by
  `safety-analyst`. They are FMEDA input, not FMEDA results.
- **`OP-34` is a concept-level conflict, not an analysis detail:** `SM-02` de-energises the driver
  stages on SAFE_OFF, which applied to the low beam produces `H-01` — the hazard `SG-01` exists to
  prevent. This wants resolving in the TSC before the FMEDA quantifies anything around it.
- `OP-29`, `OP-38`: two further findings that touch safety goals rather than hardware detail.
- Element names are binding: `ECU_LightingCtrl`, `LED_Driver_Stage_1`,
  `SWC_LightManager`, `SWC_HighBeamControl`, `SWC_HighBeamMonitor`, `SWC_WorkLampControl`,
  `Vehicle_Gateway`, `Item_LightingSystem`, `Current_Sense_Chain`, `MCU_Lockstep`,
  `ASIC_Watchdog`, `Power_Supply_Unit`, `Temp_Sense_Chain`, `SWC_DiagnosticManager`,
  `CAN_FD_Transceiver`, `LIN_Transceiver`.

> **Language:** the project is English throughout since the translation. German remains only in
> `09_process/prompts/` — that is the original commissioning document and is deliberately unchanged.
> Two element names were renamed with the translation: `Item_Beleuchtungssystem` →
> `Item_LightingSystem` and `Fahrzeug_Gateway` → `Vehicle_Gateway`.
