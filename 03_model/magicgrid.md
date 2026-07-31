# MBSE model — MagicGrid (SysML v1.6)

**Phase 4 · Owner:** mbse-modeler · **Status:** draft

> Teaching/reference project. All numeric values are plausible example values, not validated data.

The model does not restate the requirements — it makes their structure and behaviour inspectable.
Every element carries the project ID it comes from; nothing in the model exists that is not in the
requirements or the architecture.

---

## 1 MagicGrid matrix

Filled with the concrete artefacts of this project.

| | **Requirements** | **Behavior** | **Structure** | **Parameters** |
|---|---|---|---|---|
| **Problem Domain**<br/>(black box) | `CR-001` … `CR-023`<br/>`H-01` … `H-07`<br/>`SG-01`, `SG-02`<br/>`FSR-001` … `FSR-008` | Use cases `UC-1` … `UC-7`<br/>Activity "activate low beam"<br/>Operational situations `BS-01` … `BS-07` | Item boundary<br/>(`ctx_item.puml`)<br/>`Item_LightingSystem` | 24 V supply, `T_amb` −40…+85 °C<br/>FTTI 300 ms, FRT 150 ms<br/>Usage profile `A-07` |
| **Solution Domain**<br/>(white box) | `SYS-REQ-001` … `SYS-REQ-021`<br/>`TSR-001` … `TSR-008` | State machine "operating states"<br/>Sequence "open load → DTC" | BDD system decomposition<br/>IBD `ECU_LightingCtrl`<br/>(`bdd_system.puml`, `ibd_ecu.puml`) | Detection ≤ 80 ms<br/>Threshold 150 mA / 50 ms<br/>PWM 400 Hz, duty ≥ 20 % |
| **Implementation** | `HW-REQ-001` … `HW-REQ-010`<br/>`SM-01`<br/>(SW-REQ: phase 7) | Task and cycle time model<br/>(phase 7) | HW blocks `MCU_Lockstep`,<br/>`ASIC_Watchdog`, `LED_Driver_Stage_1`,<br/>`Current_Sense_Chain`<br/>SW blocks `SWC_*` | Measurement uncertainty ±20 mA<br/>Derating floor 400 mA<br/>Luminous flux model `A-13` |

Read the columns as *what is required · how it behaves · what it is made of · by which values it is
constrained*; the rows as increasing commitment to a solution.

---

## 2 The eight views

All sources in [`plantuml/`](plantuml/). Rendered exports are CI artefacts and deliberately not
committed — the text is the source of truth.

### 2.1 Use cases — [`uc_lighting.puml`](plantuml/uc_lighting.puml)

Actors driver, workshop, vehicle gateway and environment against the seven use cases of the item.

**Reading it:** `UC-1` includes `UC-5` — failure detection is not an optional add-on to operating
the low beam but part of it. `UC-5` and `UC-2` extend into `UC-7` (safe state), which is where both
safety goals attach.

### 2.2 Requirements — [`req_golden_thread.puml`](plantuml/req_golden_thread.puml)

The Golden Thread with the SysML relations `«deriveReqt»`, `«satisfy»` and `«verify»`.

**Reading it:** the chain runs hazard → safety goal → FSR → TSR → SYS-REQ → HW-REQ; `SM-01` and
`SWC_LightManager` satisfy it, `TC-021` verifies three levels of it at once. That `TC-021` alone
carries the verification of `SG-01`, `TSR-003` and `SYS-REQ-014` is visible here — and is a thin
spot, see the open points.

### 2.3 Activity — [`act_low_beam.puml`](plantuml/act_low_beam.puml)

Activating the low beam including the fault path.

**Reading it:** the red path is the fault case. The decision "PWM on-time ≥ 150 µs" is the gating
question from `SYS-REQ-017`: below it the diagnosis reports "not available" rather than a wrong
result.

### 2.4 Sequence — [`seq_open_load.puml`](plantuml/seq_open_load.puml)

Open load → fault reaction → diagnostic DTC, with the timing budget as notes.

**Reading it:** the two notes carry the safety argument — classification at ≤ 80 ms, safe state at
≤ 230 ms against an FTTI of 300 ms. The off-phase zero check (`HW-REQ-005`) runs *before* the
reaction, because a stuck sense chain would otherwise trigger a false safe-state transition.

### 2.5 State machine — [`stm_lighting.puml`](plantuml/stm_lighting.puml)

Operating states Init, Normal, Degraded, Safe state, Sleep.

**Reading it:** the safe state is highlighted and is reached from two directions — via `Degraded`
after a detected channel loss, and directly from `Normal_Operation` when the watchdog is not served
(`TSR-001`). Leaving it requires an ignition cycle, so a sporadic fault cannot silently self-clear.

### 2.6 Structure — [`bdd_system.puml`](plantuml/bdd_system.puml) and [`ibd_ecu.puml`](plantuml/ibd_ecu.puml)

System decomposition and the internal signal flows of the ECU.

**Reading it:** the BDD shows the software components as named blocks without internals — their
design is phase 7, and inventing it here would be a model that outruns its requirements. In the IBD
the safety-relevant loop `LED_Driver → Current_Sense_Chain → MCU → LED_Driver` is closed, and the
watchdog has its own path to the driver stages, bypassing the microcontroller.

### 2.7 Parametric — [`par_luminous_flux.puml`](plantuml/par_luminous_flux.puml)

Constraint luminous flux ↔ junction temperature ↔ channel current.

**Reading it:** the constraint binds the derating floor of `HW-REQ-008` to the legal minimum
luminous flux. At 400 mA and 110 °C junction temperature the model yields roughly 264 lm — below
the legal minimum. That is the intended reading: **limp-home is a fault state, not a permitted
operating mode**, and it must end the journey rather than continue it.

### 2.8 Allocation

Function → logical element → physical element:
[`../04_architecture/allocation.md`](../04_architecture/allocation.md)

---

## 3 What the model exposed

Modelling is a review technique, not decoration. Three things became visible:

1. **`TC-021` is a single point of verification.** In the requirements diagram three `«verify»`
   edges converge on one test case. Verification depth does not match specification depth — new
   test cases are owed for `HW-REQ-001` … `HW-REQ-010` (`OP-19`) and for the `SG-02` thread.
2. **`SG-02` has no behavioural view.** The state machine and the sequence cover the low beam only.
   The decomposed high-beam path (`TSR-006` / `TSR-007`) is structurally present but behaviourally
   unmodelled — which is consistent with it being the deliberately shallower thread, but it should
   be a conscious decision, not an oversight. Recorded as `OP-25`.
3. **The software components are empty shells.** Legitimate for phase 4, but it means the IBD
   cannot yet show where freedom from interference between `SWC_HighBeamControl` (QM) and
   `SWC_HighBeamMonitor` (ASIL A) is enforced. Phase 7 owes that.

---

**Work products:** `magicgrid.md`, `plantuml/uc_lighting.puml`, `req_golden_thread.puml`,
`act_low_beam.puml`, `seq_open_load.puml`, `stm_lighting.puml`, `bdd_system.puml`, `ibd_ecu.puml`,
`par_luminous_flux.puml` → `03_model/` · `allocation.md` → `04_architecture/`

**Open points:** `OP-25` behavioural views for the `SG-02` thread · `OP-19` test cases for the
hardware requirements · `OP-26` freedom-from-interference view once the SW architecture exists

**Process reference:** MBSE / MagicGrid · ASPICE **SYS.3** (the structural views document the
system architectural design) · ISO 26262 **Part 4** — the model supports the technical safety
concept but is not itself the safety argument.
