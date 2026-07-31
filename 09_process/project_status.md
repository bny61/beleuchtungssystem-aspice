# Project status — current state and open points

> This file is the re-entry point. It is updated at the end of every phase.
> Last update: after phase 2.

## Phase status

| Phase | Content | Status | Lead |
|---|---|---|---|
| 0 | Project frame, stakeholders, roles, tailoring, glossary | **skipped** | safety-manager, config-manager |
| 1 | Customer requirements `CR-001 … CR-023` (SYS.1) | **complete** (draft) | systems-engineer |
| 2 | Item definition, HARA, safety goals, FSC (ISO 26262-3) | **complete** (draft) | safety-manager |
| 3 | `SYS-REQ`, `TSR`, E/E architecture (SYS.2, SYS.3) | **complete** (draft) | systems-engineer |
| 4 | MBSE model, MagicGrid, 8 SysML views | **complete** (draft) | mbse-modeler |
| 5 | FMEA, DFMEA, FTA, FMEDA, DFA, STPA | **next phase** | safety-analyst |
| 6 | Hardware (HWE.1–4, Part 5) | open | hardware-engineer |
| 7 | Software (SWE.1–6, Part 6) | open | software-engineer |
| 8 | Verification & validation (SYS.4, SYS.5) | open | verification-engineer |
| 9 | Safety case, confirmation measures | open | safety-manager, quality-assessor |
| 10 | GitHub configuration management and evidence | partly prepared | config-manager |
| 11 | Traceability & metrics | open | config-manager, quality-assessor |

**Phase 0 was skipped** and needs to be caught up — the role model, independence levels and
tailoring decisions are missing but will be required at the latest for phase 9.

## Results so far

- **23 customer requirements** `CR-001 … CR-023`, covering all categories of the customer
  specification. Three of them (`CR-002`, `CR-005`, `CR-016`) are **deliberately weak** and marked
  as such in the `rationale` field (teaching purpose).
- **7 hazards** `H-01 … H-07`, six of them with a safety goal, one resulting in QM.
- **2 safety goals**: `SG-01` (ASIL B, Golden Thread) and `SG-02` (ASIL A, second thread).
- **8 FSR** `FSR-001 … FSR-008`, incl. the ASIL decomposition
  `FSR-005 → FSR-006 QM(A) + FSR-007 A(A)`.
- **Timing budget SG-01** closes: 70 ms detection + 150 ms reaction = 220 ms < FTTI 300 ms.
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
- Traceability check green, 83 records.

## Open points

| ID | Point | Owner | Due |
|---|---|---|---|
| OP-1 | ~~Carry the ASIL of the `tbd` customer requirements over from the HARA~~ | systems-engineer | **done** (phase 3) |
| OP-2 | ~~Behaviour outside the normal supply range is missing~~ — undervoltage covered by `SYS-REQ-013`; overvoltage and load dump remain open for phase 6 | systems-engineer | **partly done** |
| OP-3 | `CR-007` is not atomic (detection + indication); change only via a requirement-change issue | systems-engineer | before baseline |
| OP-15 | Confirm the 90 % diagnostic coverage of `SM-01` against the FMEDA — blocks `SM-01` returning to `reviewed` | safety-analyst | Phase 5 |
| OP-16 | Feasibility of the 400 mA derating floor (`HW-REQ-008`, `A-12`) against the LED module thermal design | hardware-engineer | Phase 6 |
| OP-17 | ~~Decide the gating scheme below the minimum PWM on-time~~ — decided for `SYS-REQ-017` ("diagnosis not available"); `HW-REQ-004` not implemented in the base variant | systems-engineer | **done** (phase 3) |
| OP-18 | ~~Decide whether per-string current sensing is added~~ — decided against; channel voltage (`HW-REQ-006`) covers the failure mode. Revisit after the FMEDA (`OP-23`) | systems-engineer | **done** (phase 3) |
| OP-19 | New test cases for `HW-REQ-001` … `HW-REQ-010` | verification-engineer | Phase 8 |
| OP-20 | Re-review `SYS-REQ-014`, `SM-01` and `TC-021` — dropped to `draft` by the refinement | safety-manager | Phase 3 |
| OP-21 | CAN FD / J1939 message catalogue and signal encoding not specified at frame level | systems-engineer | Phase 4 |
| OP-22 | Bus load and timing analysis for the cycle times of the interface table | systems-engineer | Phase 4 |
| OP-23 | Revisit the decision against per-string sensing after the FMEDA | safety-analyst | Phase 5 |
| OP-24 | Overvoltage and load-dump behaviour still undefined (`OP-2` remainder) | hardware-engineer | Phase 6 |
| OP-4 | Define the required function class per ISO 7637-2 pulse in `CR-017` | hardware-engineer | Phase 6 |
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
- Element names are binding: `ECU_LightingCtrl`, `LED_Driver_Stage_1`,
  `SWC_LightManager`, `SWC_HighBeamControl`, `SWC_HighBeamMonitor`, `SWC_WorkLampControl`,
  `Vehicle_Gateway`, `Item_LightingSystem`, `Current_Sense_Chain`, `MCU_Lockstep`,
  `ASIC_Watchdog`, `Power_Supply_Unit`, `Temp_Sense_Chain`, `SWC_DiagnosticManager`.

> **Language:** the project is English throughout since the translation. German remains only in
> `09_process/prompts/` — that is the original commissioning document and is deliberately unchanged.
> Two element names were renamed with the translation: `Item_Beleuchtungssystem` →
> `Item_LightingSystem` and `Fahrzeug_Gateway` → `Vehicle_Gateway`.
