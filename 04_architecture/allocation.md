# Allocation — function → logical element → physical element

**Phase 4 · MagicGrid view 8 · Owner:** systems-engineer with mbse-modeler

> Companion to the TSR allocation matrix in
> [`ee_architecture.md`](ee_architecture.md). That matrix allocates *requirements*;
> this table allocates *functions*.

| Function | Requirement | Logical element | Physical element | ASIL |
|---|---|---|---|---|
| Operate low beam | `SYS-REQ-001`, `SYS-REQ-012` | `SWC_LightManager` | `MCU_Lockstep`, `LED_Driver_Stage_1`, headlamp module | B |
| Automatic light control | `SYS-REQ-002`, `SYS-REQ-003` | `SWC_LightManager` | `MCU_Lockstep` (ambient light via `Vehicle_Gateway`) | B |
| Detect channel failure | `SYS-REQ-014` … `019`, `TSR-003` | `SWC_LightManager`, `SM-01` | `Current_Sense_Chain`, `LED_Driver_Stage_1` | B |
| Fault reaction, limp-home | `SYS-REQ-011`, `TSR-004` | `SWC_LightManager` | `MCU_Lockstep`, `LED_Driver_Stage_1` | B |
| Driver warning | `SYS-REQ-010`, `TSR-005` | `SWC_LightManager` | `CAN_FD_Transceiver` → instrument cluster (external) | B |
| Program flow monitoring | `TSR-001` | — (hardware function) | `ASIC_Watchdog` incl. disable path | B |
| Glare-free high beam | `SYS-REQ-004`, `TSR-006` | `SWC_HighBeamControl` | `MCU_Lockstep`, `LED_Driver_Stage_1` | QM(A) |
| High-beam plausibility monitor | `TSR-007` | `SWC_HighBeamMonitor` | `MCU_Lockstep` (separate partition), separate enable path | A(A) |
| Work-lamp inhibit | `SYS-REQ-005`, `TSR-008` | `SWC_WorkLampControl` | `MCU_Lockstep`, work-lamp output stages | A |
| Cornering light | `SYS-REQ-006` … `008` | `SWC_LightManager` | `LIN_Transceiver`, actuator (external) | A |
| Daytime running lights | `SYS-REQ-009` | `SWC_LightManager` | `LED_Driver_Stage_1` | QM |
| Thermal derating | `HW-REQ-008` | `SWC_LightManager` | `Temp_Sense_Chain`, `LED_Driver_Stage_1` | B |
| Diagnostics, DTC, UDS | `SYS-REQ-021` | `SWC_DiagnosticManager` | `MCU_Lockstep`, `CAN_FD_Transceiver` | QM |
| Supply and monitoring | `SYS-REQ-012`, `SYS-REQ-013` | — (hardware function) | `Power_Supply_Unit` | B |

## Two observations from the allocation

**`MCU_Lockstep` carries functions from QM to ASIL B side by side.** `SWC_HighBeamControl` (QM(A))
and `SWC_HighBeamMonitor` (A(A)) run on the same physical element. Freedom from interference —
memory partitioning and timing monitoring — is therefore not optional but a precondition for the
decomposition to hold. Owed by phase 7, tracked with `RISK-02`.

**Two functions have no logical element.** Program flow monitoring and supply monitoring are pure
hardware functions. That is correct, not a gap — but it means their verification cannot be a
software test, which the test strategy in phase 8 has to reflect.
