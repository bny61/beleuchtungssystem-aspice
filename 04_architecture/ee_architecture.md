# E/E architecture — Lighting ECU

**Phase 3 · ASPICE SYS.3 · ISO 26262-4 (technical safety concept)**
**Status:** draft · **Owner:** systems-engineer, with safety-manager for the TSR allocation

> Teaching/reference project. All numeric values are plausible example values, not validated data.

---

## 1 📋 OVERVIEW — Architecture blocks

| Block | Element name | Function | ASIL |
|---|---|---|---|
| Microcontroller | `MCU_Lockstep` | Application, monitoring, diagnostics; dual-core lockstep | B |
| External watchdog | `ASIC_Watchdog` | Independent time base, question/answer watchdog, disable path to the driver stages | B |
| LED driver stages | `LED_Driver_Stage_1..n` | Constant-current control per channel, PWM dimming, OVP/OCP/thermal status | B |
| Current sensing | `Current_Sense_Chain` | Shunt, amplifier, ADC input per channel; PWM-synchronous sampling | B |
| Temperature sensing | `Temp_Sense_Chain` | LED module NTC and ECU board sensor; input to the derating function | B |
| Supply | `Power_Supply_Unit` | 16–32 V input, buck plus linear stage, undervoltage and overvoltage monitoring | B |
| Bus interface | `CAN_FD_Transceiver`, `LIN_Transceiver` | CAN FD / SAE J1939 to the vehicle gateway, LIN to the actuator | B / QM |
| Diagnostic path | `SWC_DiagnosticManager` | DTC memory, UDS server per ISO 14229 | QM |

**Decision on the microcontroller concept:** lockstep MCU **and** external watchdog, not one or the
other. The lockstep core covers random faults of the computing core; it cannot cover a stalled
clock or a hung application, which is what the watchdog with its independent time base addresses
(`TSR-001`). For ASIL B this pairing is deliberate over-provisioning, and it is what makes the
freedom-from-interference argument for the mixed ASIL B / QM software feasible in phase 7.

```plantuml
@startuml bdd_ee_architecture
title E/E architecture - Lighting ECU (SYS.3)
skinparam componentStyle rectangle
skinparam rectangle {BackgroundColor White}

rectangle "Vehicle" as VEH #LightGray {
  rectangle "Vehicle_Gateway\nCAN FD / J1939" as GW
  rectangle "Vehicle supply 24 V" as PWR
}

rectangle "ECU_LightingCtrl" as ECU #LightYellow {
  rectangle "MCU_Lockstep\n«block» ASIL B" as MCU
  rectangle "ASIC_Watchdog\n«block» ASIL B\nTSR-001" as WD
  rectangle "Power_Supply_Unit\n16-32 V" as PSU
  rectangle "CAN_FD_Transceiver" as CAN
  rectangle "LIN_Transceiver" as LIN
  rectangle "LED_Driver_Stage_1..n\n«block» ASIL B" as DRV
  rectangle "Current_Sense_Chain\nSM-01 / HW-REQ-001" as CS
  rectangle "Temp_Sense_Chain" as TS
}

rectangle "Headlamp modules\nlow / high / cornering" as LAMP
rectangle "Work-lamp output stages" as WORK

PWR --> PSU : KL30 / KL15
GW <--> CAN : light request, v_veh,\nsteering angle, object data, status
CAN <--> MCU
MCU --> DRV : PWM, enable
MCU <--> WD : question / answer
WD --> DRV : disable (TSR-001)
DRV --> LAMP : channel current
DRV --> WORK
DRV --> CS : shunt voltage
CS --> MCU : I_load (PWM-synchronous)
TS --> MCU : T_LED, T_board
DRV --> MCU : OVP / OCP / thermal status
MCU --> LIN : actuator command
@enduml
```

**How to read it:** the yellow block is the item boundary of the ECU. The safety-relevant loop of
the Golden Thread runs `DRV → CS → MCU → DRV`: the driver stage feeds the shunt, the current sense
chain reports back to the microcontroller, and the microcontroller commands the fault reaction. The
watchdog has its **own** path to the driver stages so that a hung microcontroller cannot prevent the
de-energisation.

---

## 2 🔍 DEEP DIVE — Interface table

Only interfaces of the Golden Thread and of `SG-02` are listed at signal level; the remaining
interfaces are summarised.

| Signal | Direction | Type | Range | Timing | ASIL |
|---|---|---|---|---|---|
| `LightRequest` | Gateway → ECU | enum {off, DRL, low, high, work} | 5 states | cyclic 100 ms, timeout 300 ms | B |
| `VehicleSpeed` | Gateway → ECU | uint16, 0.01 km/h | 0 … 150 km/h | cyclic 20 ms, timeout 100 ms | A |
| `SteeringAngle` | Gateway → ECU | int16, 0.1 ° | −540 … +540 ° | cyclic 20 ms, timeout 100 ms | A |
| `AmbientLight` | Gateway → ECU | uint16, 1 lx | 0 … 60000 lx | cyclic 100 ms, timeout 500 ms | B |
| `ObjectList` | Gateway → ECU | struct, ≤ 8 objects | — | cyclic 50 ms, timeout 200 ms | QM(A) |
| `DriverWarningReq` | ECU → Gateway | enum {none, lowBeamFault} | 2 states | cyclic 500 ms | B |
| `LightingStatus` | ECU → Gateway | bitfield per channel | 16 bit | cyclic 100 ms | B |
| `I_Load_Ch1..n` | Sense chain → MCU | uint12 ADC | 0 … 1.5 A | PWM-synchronous, 2.5 ms raster | B |
| `U_Channel_Ch1..n` | Driver → MCU | uint12 ADC | 0 … 40 V | 10 ms | B |
| `DriverStatus_Ch1..n` | Driver → MCU | bitfield OVP/OCP/OT | 3 bit | ≤ 10 ms | B |
| `T_LED`, `T_Board` | Sense chain → MCU | uint12 ADC | −40 … +150 °C | 100 ms | B |
| `PWM_Ch1..n` | MCU → Driver | PWM | 400 Hz, duty 0 … 100 % | continuous | B |
| `Enable_Ch1..n` | MCU → Driver | digital | 0 / 1 | continuous | B |
| `WD_Disable` | Watchdog → Driver | digital | 0 / 1 | ≤ 50 ms | B |

**Timeout handling is part of the interface, not of the application.** Every safety-relevant input
carries a timeout; on timeout the receiving function must assume the signal invalid. `TSR-008`
makes this explicit for the speed signal, because an inhibit that can be defeated by a lost frame
is not an inhibit.

**On `ObjectList` at QM(A):** the signal originates outside the item boundary (`A-05`) and feeds
the QM path of the decomposition (`TSR-006`). The safety argument rests on the independent monitor
`TSR-007`, which does **not** use this signal. The interface agreement with the vehicle manufacturer
is still open (`OP-10`).

---

## 3 🔍 DEEP DIVE — TSR allocation matrix

| TSR | ASIL | Hardware measure | Software measure | System measure |
|---|---|---|---|---|
| TSR-001 | B | `ASIC_Watchdog`, independent time base, disable path to the driver stages | Watchdog service task, question/answer protocol | — |
| TSR-002 | B | `Current_Sense_Chain` feedback | `SWC_LightManager`: command/feedback comparison per cycle | — |
| **TSR-003** | **B** | **`SM-01`** — shunt sensing, PWM-synchronous sampling, off-phase self-test (`HW-REQ-001` … `HW-REQ-010`) | Threshold evaluation, debouncing, cause discrimination (`SYS-REQ-019`) | Detection budget cap 100 ms (`SYS-REQ-018`) |
| TSR-004 | B | Channel-wise independent driver stages | `SWC_LightManager`: limp-home state machine | Safe state defined in `SG-01` |
| TSR-005 | B | `CAN_FD_Transceiver` | Cyclic warning message, 500 ms | Driver warning displayed by the instrument cluster (`A-04`) |
| TSR-006 | QM(A) | — | `SWC_HighBeamControl` | Object data from the vehicle (`A-05`) |
| TSR-007 | A(A) | Separate enable path to the high-beam driver stage | `SWC_HighBeamMonitor`, separate task and memory partition | Independence argument, DFA in phase 5 (`RISK-02`) |
| TSR-008 | A | — | `SWC_WorkLampControl`, inhibit incl. signal-invalid case | Speed signal timeout per the interface table |

**Reading the matrix:** a TSR with an entry in only one column is a warning sign. `TSR-006` is
QM-only by construction — that is exactly why it is admissible only in combination with `TSR-007`.

---

## 4 System-level decisions taken in this phase

**OP-17 — gating below the minimum PWM on-time: decided in favour of `SYS-REQ-017`,
"diagnosis not available".** The forced diagnostic window of `HW-REQ-004` injects a current pulse
into a channel that the driver deliberately dimmed, which is visible as flicker at low duty and
constitutes an unrequested actuation of a safety-relevant output — precisely what `TSR-002` is meant
to prevent. Declaring the diagnosis unavailable is honest and bounded: it is reported on the bus,
and it is time-limited because low beam runs at duty ≥ 20 % under `A-09`. `HW-REQ-004` is therefore
**not** implemented in the base variant and is retained as an option for work lamps, where deep
dimming is a normal operating case.

**OP-18 — per-string current sensing: decided against, with a compensating measure.** Per-string
sensing would require a second shunt and sense channel per driver stage; the benefit is confined to
one failure mode (loss of one parallel string). The same failure mode is covered by the channel
voltage measurement `HW-REQ-006`, which is needed anyway to discriminate short-to-battery. The
decision is therefore *channel voltage instead of per-string current*, and it must be revisited if
the FMEDA in phase 5 shows the diagnostic coverage target cannot be met without it.

Both decisions change what the diagnosis can do, not only how it is built, and are consequently
recorded here rather than in the hardware requirements.

---

## 5 Open points

| ID | Point | Owner |
|---|---|---|
| OP-10 | Interface agreement (DIA) for `ObjectList` with the vehicle manufacturer | safety-manager |
| OP-21 | Message catalogue and signal encoding for CAN FD / J1939 not yet specified at frame level | systems-engineer |
| OP-22 | Bus load and timing analysis for the cycle times of the interface table | systems-engineer |
| OP-23 | The decision against per-string sensing must be revisited after the FMEDA | safety-analyst |

---

**Work products:** `ee_architecture.md` → `04_architecture/` · `TSR-001` … `TSR-008` →
`02_safety/04_tsc/` · `SYS-REQ-001` … `SYS-REQ-021` → `01_requirements/system/`
**Process reference:** ASPICE **SYS.2** (system requirements analysis), **SYS.3** (system
architectural design) · ISO 26262 **Part 4** (technical safety concept, system design) ·
**Part 9** (ASIL decomposition for `TSR-006` / `TSR-007`).
