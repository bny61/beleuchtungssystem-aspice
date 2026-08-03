# Hardware components and their P-diagrams

**ASPICE HWE.2 (hardware design) · ISO 26262-5 · Owner:** hardware-engineer
**Status:** draft · **Purpose:** structure and function analysis feeding the phase 5 DFMEA

> Teaching/reference project. All numeric values are plausible example values, not validated data.

---

## 1 Why this document exists

Phase 5 opens with a System-FMEA and a DFMEA per the AIAG-VDA seven-step method, and step 1 of
that method is a **structure analysis**: what the components are and where each one's boundary
runs. The project had never written that down. `hw_architecture.md` names the blocks and lists
what is inside them, but nothing stated what a block is *responsible for*, what its ideal
function is, or how it fails.

A **P-diagram** supplies the missing piece. It states the ideal function, the noise factors that
push a component away from it, the control factors that hold it there, and the **error states** —
which are the failure modes the DFMEA then rates. Written first, the DFMEA rows are *derived*
rather than invented, and the same noise factors feed the FMEDA's failure-mode distribution.

**A P-diagram is a robustness tool, not a safety analysis.** It produces candidate failure modes.
Phase 5 rates them, and may reject some.

## 2 📋 OVERVIEW — the eight components

The element names are the identity; they are the same names used in every `allocated_to` field,
in `ee_architecture.md` and in `ibd_ecu.puml`. No new ID prefix is introduced.

| Component | Boundary — what is inside | Owning `HW-REQ` | Safety mechanisms | ASIL |
|---|---|---|---|---|
| `Power_Supply_Unit` | KL30 input protection through to the 5 V / 3.3 V rails and `VREF`; **not** the vehicle supply itself | `HW-REQ-011` … `016` | `SM-06` | B |
| `MCU_Lockstep` | The microcontroller including its ADC and PWM timer unit; **not** the software running on it | `HW-REQ-003` | contributes to `SM-01` | B |
| `ASIC_Watchdog` | Independent time base, question/answer logic, rail monitor, reset and `SAFE_OFF` driver | `HW-REQ-017`, `018` | `SM-02`, rail leg of `SM-06` | B |
| `LED_Driver_Stage_1..n` | Per-channel enable gate and constant-current stage up to the channel output; **not** the LED module | `HW-REQ-019` … `021`, `026` … `030` | `SM-03`, `SM-04` | B |
| `Current_Sense_Chain` | Shunt, amplifier, anti-alias filter, clamp, up to the ADC input pin; **not** the ADC itself | `HW-REQ-001` … `005`, `009`, `030` | `SM-01` | B |
| `Temp_Sense_Chain` | LED module NTC path and board sensor up to the ADC input; **not** the derating function | `HW-REQ-022`, `023`, `024` | `SM-05` | B |
| `CAN_FD_Transceiver` | Bus interface between the CAN controller and the vehicle bus | `HW-REQ-025` | — | B |
| `LIN_Transceiver` | Actuator link to the headlamp levelling and bending actuator | — | — | QM |

**Two boundaries are worth stating explicitly**, because both are where a DFMEA usually goes
wrong. `Current_Sense_Chain` ends at the ADC *input pin* — the conversion belongs to
`MCU_Lockstep`, which is why a wrong `VREF` shows up as a noise factor in one component and an
error state in another. And `LED_Driver_Stage` ends at the channel output: the LED module is
outside the item boundary, covered by assumption `A-13`.

## 3 🔍 DEEP DIVE — the Golden Thread components

### 3.1 `Current_Sense_Chain`

```plantuml
@startuml pdiag_current_sense_chain
title P-diagram - Current_Sense_Chain (DEEP DIVE, Golden Thread, SM-01)
skinparam defaultTextAlignment left
skinparam rectangle {
  BackgroundColor White
  RoundCorner 8
}

rectangle "**Noise factors**\n//piece-to-piece//  shunt 1.0 %, amplifier gain 1.0 %, Vos <= 150 uV RTI,\n   VREF 0.5 % (HW-REQ-001)\n//over time//  shunt 50 ppm/K drift, solder-joint ageing, VREF drift\n//customer usage//  duty 20..100 %, dimming, deep derating to 400 mA\n//environment//  -40..+85 C ambient, ISO 7637-2 transients, EMC injection\n//system interaction//  PWM edge coupling, ADC sampling raster,\n   supply ripple from the driver stage" as N #FFF8E1

rectangle "**Input signal**\nTrue channel current\n0 .. 1.5 A through the\n50 mOhm shunt" as I #E7F0FB

rectangle "**Ideal function**\nReport the true low-beam\nchannel current to the MCU\nwith a total uncertainty of\nnot more than +/-20 mA at\nthe 150 mA classification\nthreshold" as F #EAF4EA

rectangle "**Intended output**\nI_Load_Ch1..n, 12 bit,\nPWM-synchronous,\n2.5 ms raster,\nwithin the tolerance band" as O #E7F0FB

rectangle "**Error states**\nE1  reads high -> open load missed (SM-01 blind)\nE2  reads low -> healthy channel classified as open\nE3  stuck value -> fault frozen, no detection\nE4  noise above the band -> chattering classification\nE5  sample outside the PWM on-phase -> invalid reading\nE6  no conversion -> diagnosis unavailable" as E #FBEAEA

rectangle "**Control factors**\nKelvin-sensed shunt, gain 50 V/V, anti-alias RC f_c 40 kHz,\nclamp to the ADC range, PWM-timer-triggered conversion\n(HW-REQ-003), second reference leg for the plausibility check,\noff-phase self-test, 20 ms debounce (HW-REQ-005)" as C #F0EDF7

N -down-> F
I -right-> F
F -right-> O
F -right-> E
O -[hidden]down- E
C -up-> F

note bottom of C
  Tolerance chain and the +/-20 mA budget: 05_hardware/analysis_current_sensing.md
  Error states E1 .. E6 are candidate DFMEA failure modes for phase 5.
end note
@enduml
```

**How to read it:** the ideal function is a *measurement* accuracy statement, so the noise
factors are the terms of the tolerance chain in `analysis_current_sensing.md` and the control
factors are what buys each term back. Error states `E1` and `E2` are the two directions of the
same failure and are not symmetric in consequence: `E1` makes `SM-01` blind to a real open load
and threatens `SG-01`; `E2` de-energises a healthy channel and *is* `H-01`. A DFMEA that rates
them the same has misread the diagram.

### 3.2 `LED_Driver_Stage_1..n`

```plantuml
@startuml pdiag_led_driver_stage
title P-diagram - LED_Driver_Stage_1..n (DEEP DIVE, Golden Thread, SM-03 / SM-04)
skinparam defaultTextAlignment left
skinparam rectangle {
  BackgroundColor White
  RoundCorner 8
}

rectangle "**Noise factors**\n//piece-to-piece//  current-set resistor 1 %, switching-node timing spread\n//over time//  MOSFET R_DS(on) rise, output-capacitor ageing, connector fretting\n//customer usage//  duty 20..100 %, frequent switch-on cycles, deep derating\n//environment//  cavity up to 105 C, 9..36 V supply, load dump 58 V, EMC\n//system interaction//  SAFE_OFF from the watchdog, derating set point,\n   inrush of the parallel channel, harness impedance" as N #FFF8E1

rectangle "**Input signal**\nPWM_Ch1..n 400 Hz and\nEnable_Ch1..n from the MCU,\ncommanded set point\n0.40 .. 1.20 A" as I #E7F0FB

rectangle "**Ideal function**\nDrive the commanded\nconstant channel current\ninto the LED module and\nreport its own status,\nwhile the enable gate\nremains dominated by\nSAFE_OFF (HW-REQ-019)" as F #EAF4EA

rectangle "**Intended output**\nChannel current at set\npoint within 20 ms\n(HW-REQ-027), skew\n<= 10 ms (HW-REQ-028),\nDriverStatus OVP/OCP/OT" as O #E7F0FB

rectangle "**Error states**\nE1  no output -> low beam lost (H-01)\nE2  output below set point -> illuminance below CR-024\nE3  output above set point -> overcurrent, LED stress\nE4  will not switch off -> unintended actuation (TSR-002)\nE5  slow or absent soft start -> activation misses SYS-REQ-001\nE6  excessive inrush -> supply dip, spurious SM-06 trip\nE7  status readback wrong -> fault reaction on false data" as E #FBEAEA

rectangle "**Control factors**\nConstant-current buck with soft start (HW-REQ-027), enable gate\nEN_MCU AND not(SAFE_OFF) (HW-REQ-019), current limit 1.8 A with\nlatch-off <= 5 ms (HW-REQ-021), off-phase channel-voltage check\n(HW-REQ-020), inrush limited to 8 A (HW-REQ-029), thermal derating\n(HW-REQ-023), per-channel independence" as C #F0EDF7

N -down-> F
I -right-> F
F -right-> O
F -right-> E
O -[hidden]down- E
C -up-> F

note bottom of C
  Soft start, skew and inrush budget: 05_hardware/analysis_low_beam_activation.md
  E1 is the failure the whole Golden Thread exists to detect.
  Error states are candidate DFMEA failure modes for phase 5.
end note
@enduml
```

**How to read it:** `E1` is the failure the entire Golden Thread exists to detect, which is why
this component carries both `SM-03` and `SM-04` and is the target of `SM-01`'s detection. `E4`
is its mirror image — a stage that will not switch off — and is what `TSR-002` and the dominant
`SAFE_OFF` path address. The soft-start and inrush entries come from
`analysis_low_beam_activation.md`.

## 4 📋 OVERVIEW — the remaining six

### 4.1 `Power_Supply_Unit`

```plantuml
@startuml pdiag_power_supply_unit
title P-diagram - Power_Supply_Unit (OVERVIEW, SM-06)
skinparam defaultTextAlignment left
skinparam rectangle {
  BackgroundColor White
  RoundCorner 8
}

rectangle "**Noise factors**\n//piece-to-piece//  regulator tolerance, VREF 0.5 %, inductor spread\n//over time//  electrolytic capacitor drying, TVS degradation\n//customer usage//  cranking, jump start, frequent KL15 cycling\n//environment//  9..36 V, load dump 58 V / 400 ms, ISO 7637-2 pulses,\n   reverse polarity -32 V, -40..+85 C\n//system interaction//  inrush of both driver channels, bus wake" as N #FFF8E1

rectangle "**Input signal**\nKL30 / KL15 vehicle supply,\n16 .. 32 V nominal,\n9 .. 36 V operating" as I #E7F0FB

rectangle "**Ideal function**\nProvide clean 5 V and 3.3 V\nrails and the 3.3 V ADC\nreference, and flag any\nexcursion outside the\noperating range within\n10 ms (HW-REQ-016)" as F #EAF4EA

rectangle "**Intended output**\n5 V / 3.3 V rails within\ntolerance, VREF 3.3 V\n+/-0.5 %, VBAT_PROT,\nRailStatus to the MCU" as O #E7F0FB

rectangle "**Error states**\nE1  rail out of tolerance -> undefined ECU behaviour\nE2  rail collapses -> loss of low beam (H-01)\nE3  VREF drift -> every ADC reading biased, SM-01 affected\nE4  no undervoltage flag -> silent brown-out\nE5  damage from transient or reverse polarity -> total loss" as E #FBEAEA

rectangle "**Control factors**\nReverse-polarity FET, TVS clamp, CM choke and pi filter\n(HW-REQ-015, HW-REQ-014), buck plus LDO, buffered VBAT_PROT,\nUV/OV window comparators with hardware shutdown above 60 V\n(HW-REQ-016), separate reference for the plausibility leg" as C #F0EDF7

N -down-> F
I -right-> F
F -right-> O
F -right-> E
O -[hidden]down- E
C -up-> F

note bottom of C
  Ranges and status classes: 05_hardware/analysis_supply_and_transients.md
end note
@enduml
```

**How to read it:** `E3` is the interesting one — a drifting `VREF` biases every ADC reading in
the ECU at once, so it is a common-cause candidate for the DFA in phase 5 rather than a local
fault.

### 4.2 `MCU_Lockstep`

```plantuml
@startuml pdiag_mcu_lockstep
title P-diagram - MCU_Lockstep (OVERVIEW, contributes to SM-01)
skinparam defaultTextAlignment left
skinparam rectangle {
  BackgroundColor White
  RoundCorner 8
}

rectangle "**Noise factors**\n//piece-to-piece//  ADC gain and offset spread, oscillator tolerance\n//over time//  flash retention, oscillator ageing, solder-joint fatigue\n//customer usage//  continuous operation, frequent mode changes\n//environment//  -40..+85 C, EMC injection, supply ripple\n//system interaction//  watchdog question/answer, PWM/ADC timing,\n   mixed ASIL software on one part" as N #FFF8E1

rectangle "**Input signal**\nBus signals via the\ntransceivers, I_Load, U_Channel,\nT_LED, T_Board, driver status" as I #E7F0FB

rectangle "**Ideal function**\nExecute the lighting\napplication and its\nmonitoring deterministically,\nand sample the sense\nchains in the PWM\non-phase (HW-REQ-003)" as F #EAF4EA

rectangle "**Intended output**\nPWM and enable per channel,\nbus status and warning\nframes, watchdog answers,\nDTC memory" as O #E7F0FB

rectangle "**Error states**\nE1  computation wrong -> wrong command, undetected\nE2  execution stalls -> no fault reaction (covered by SM-02)\nE3  ADC conversion mistimed -> SM-01 samples the off-phase\nE4  task overrun -> timing budget of SG-01 missed\nE5  interference between ASIL B and QM partitions" as E #FBEAEA

rectangle "**Control factors**\nDual-core lockstep, PWM-timer-triggered conversion, second\nreference leg, external watchdog with an independent time base\n(SM-02), memory and timing partitioning owed by phase 7" as C #F0EDF7

N -down-> F
I -right-> F
F -right-> O
F -right-> E
O -[hidden]down- E
C -up-> F

note bottom of C
  Freedom from interference is owed by the software architecture (OP-26).
end note
@enduml
```

**How to read it:** the lockstep pair covers computation, not timing, which is why `E2` is
delegated to `SM-02` and why `E5` cannot be closed by hardware at all — freedom from
interference is owed by the software architecture (`OP-26`).

### 4.3 `ASIC_Watchdog`

```plantuml
@startuml pdiag_asic_watchdog
title P-diagram - ASIC_Watchdog (OVERVIEW, SM-02)
skinparam defaultTextAlignment left
skinparam rectangle {
  BackgroundColor White
  RoundCorner 8
}

rectangle "**Noise factors**\n//piece-to-piece//  time-base tolerance, threshold spread\n//over time//  oscillator drift, threshold drift\n//customer usage//  every drive cycle, cold start\n//environment//  -40..+85 C, EMC, supply transients\n//system interaction//  shares the supply with the part it monitors" as N #FFF8E1

rectangle "**Input signal**\nQuestion/answer traffic from\nthe MCU, internal supply rails" as I #E7F0FB

rectangle "**Ideal function**\nDetect a stalled or\nmisbehaving microcontroller\non an independent time base\nand assert SAFE_OFF within\n50 ms (HW-REQ-018)" as F #EAF4EA

rectangle "**Intended output**\nReset and SAFE_OFF to the\nenable gate of every driver\nstage, rail status" as O #E7F0FB

rectangle "**Error states**\nE1  does not trip -> hung MCU keeps commanding (TSR-001 defeated)\nE2  trips spuriously -> low beam de-energised in normal driving (H-01)\nE3  time base drifts with the MCU clock -> common-cause failure\nE4  SAFE_OFF stuck asserted -> channels cannot be energised" as E #FBEAEA

rectangle "**Control factors**\nIndependent oscillator, question/answer rather than a simple\ntrigger, dominant hardware path to the enable gate (HW-REQ-019),\nrail monitor with reset (HW-REQ-017)" as C #F0EDF7

N -down-> F
I -right-> F
F -right-> O
F -right-> E
O -[hidden]down- E
C -up-> F

note bottom of C
  E2 is the SM-02 versus SG-01 conflict recorded as OP-34: de-energising the
  low beam is itself the hazard. The disable path may need differentiating
  by channel class - a technical safety concept decision, not a hardware one.
end note
@enduml
```

**How to read it:** `E2` is not a hardware defect to be designed out. A watchdog that trips
spuriously de-energises the low beam, which is `H-01` — the hazard `SG-01` exists to prevent.
That conflict is recorded as `OP-34` and belongs to the technical safety concept.

### 4.4 `Temp_Sense_Chain`

```plantuml
@startuml pdiag_temp_sense_chain
title P-diagram - Temp_Sense_Chain (OVERVIEW, SM-05)
skinparam defaultTextAlignment left
skinparam rectangle {
  BackgroundColor White
  RoundCorner 8
}

rectangle "**Noise factors**\n//piece-to-piece//  NTC tolerance, divider resistor tolerance\n//over time//  NTC drift, connector corrosion at the module\n//customer usage//  long high-load operation, frequent switching\n//environment//  cavity to 105 C, thermal shock, humidity\n//system interaction//  self-heating from the channel it measures,\n   shares the ADC and reference with the current sensing" as N #FFF8E1

rectangle "**Input signal**\nLED module and board\ntemperature, -40 .. +150 C" as I #E7F0FB

rectangle "**Ideal function**\nReport the LED module\ntemperature to within\n+/-3 K so the derating\nfunction can hold the\njunction below its limit\n(HW-REQ-022)" as F #EAF4EA

rectangle "**Intended output**\nT_LED, T_Board, 100 ms,\nplausibility flag for open\nor shorted sensor" as O #E7F0FB

rectangle "**Error states**\nE1  reads low -> derating too late, junction over limit\nE2  reads high -> derating too early, illuminance lost needlessly\nE3  open or short undetected -> derating on meaningless data\nE4  slow response -> thermal excursion missed" as E #FBEAEA

rectangle "**Control factors**\nNTC divider with RC and clamp, plausibility band against the board\nsensor, open and short detection (HW-REQ-022), derating curve\nwith the 400 mA floor (HW-REQ-023, HW-REQ-008)" as C #F0EDF7

N -down-> F
I -right-> F
F -right-> O
F -right-> E
O -[hidden]down- E
C -up-> F

note bottom of C
  Thermal model and the derating floor: 05_hardware/analysis_thermal_derating.md
end note
@enduml
```

**How to read it:** `E1` and `E2` trade a thermal risk against a photometric one, and the
derating floor of `HW-REQ-008` is where that trade was settled.

### 4.5 `CAN_FD_Transceiver`

```plantuml
@startuml pdiag_can_fd_transceiver
title P-diagram - CAN_FD_Transceiver (OVERVIEW)
skinparam defaultTextAlignment left
skinparam rectangle {
  BackgroundColor White
  RoundCorner 8
}

rectangle "**Noise factors**\n//piece-to-piece//  propagation-delay spread, threshold tolerance\n//over time//  ESD-structure degradation, connector fretting\n//customer usage//  continuous bus traffic across the drive cycle\n//environment//  EMC injection, bus short to supply or ground,\n   ground offset between ECUs\n//system interaction//  bus load from other ECUs (A-14)" as N #FFF8E1

rectangle "**Input signal**\nCAN FD bus, 500 kbit/s\narbitration, 2 Mbit/s data" as I #E7F0FB

rectangle "**Ideal function**\nCarry the lighting signal\nset to and from the vehicle\ngateway without corrupting\nor delaying it beyond the\ncycle times of the\ninterface table" as F #EAF4EA

rectangle "**Intended output**\nRx frames to the CAN\ncontroller, Tx frames to\nthe bus, error flags" as O #E7F0FB

rectangle "**Error states**\nE1  frames lost -> signal group times out, hold-last-valid (SYS-REQ-025)\nE2  frames corrupted -> caught by the E2E counter and CRC (SYS-REQ-022)\nE3  stuck dominant -> bus blocked for every ECU\nE4  bus-off not recovered -> lighting status and warning lost" as E #FBEAEA

rectangle "**Control factors**\nBus-fault protection against a permanent short, dominant timeout\n<= 5 ms (HW-REQ-025), end-to-end protection in software\n(SYS-REQ-022 .. 024), timeout per signal group" as C #F0EDF7

N -down-> F
I -right-> F
F -right-> O
F -right-> E
O -[hidden]down- E
C -up-> F

note bottom of C
  Bus-off recovery, wake behaviour and status readback are still open (OP-31).
end note
@enduml
```

**How to read it:** `E1` and `E2` are already answered at system level by the end-to-end
protection and the hold-last-valid rule, which is why they are annotated with `SYS-REQ-` rather
than a hardware measure. `E4` has no answer yet (`OP-31`).

### 4.6 `LIN_Transceiver`

```plantuml
@startuml pdiag_lin_transceiver
title P-diagram - LIN_Transceiver (OVERVIEW, QM)
skinparam defaultTextAlignment left
skinparam rectangle {
  BackgroundColor White
  RoundCorner 8
}

rectangle "**Noise factors**\n//piece-to-piece//  slope-control tolerance\n//over time//  connector corrosion at the actuator\n//customer usage//  levelling and bending actuation across the drive cycle\n//environment//  EMC, short to supply or ground, -40..+85 C\n//system interaction//  shares the harness with the headlamp wiring" as N #FFF8E1

rectangle "**Input signal**\nActuator commands from\nthe MCU" as I #E7F0FB

rectangle "**Ideal function**\nCarry levelling and\ncornering commands to the\nheadlamp actuator over\nthe LIN bus" as F #EAF4EA

rectangle "**Intended output**\nLIN frames to the actuator,\nactuator response" as O #E7F0FB

rectangle "**Error states**\nE1  command lost -> cornering or levelling does not follow\nE2  bus shorted -> actuator link dead\nE3  wrong position commanded -> beam aimed incorrectly" as E #FBEAEA

rectangle "**Control factors**\nSlope-controlled driver, short-circuit protection, LIN per ISO 17987" as C #F0EDF7

N -down-> F
I -right-> F
F -right-> O
F -right-> E
O -[hidden]down- E
C -up-> F

note bottom of C
  QM path: no safety goal depends on it. Cornering light is ASIL A at system
  level (SYS-REQ-006 .. 008), realised through the actuator, not this part.
end note
@enduml
```

**How to read it:** the only QM component in the set. Cornering light is ASIL A at system level,
but that requirement is met through the actuator rather than through this part.

## 5 Error state → candidate DFMEA failure mode

**Phase 5 takes its DFMEA rows from this table rather than starting fresh.** Every entry is a
*candidate*: the DFMEA rates it with B/A/E and an action priority, and may reject it.

| Component | Error states | Of those, in the Golden Thread |
|---|---|---|
| `Current_Sense_Chain` | `E1` … `E6` | `E1`, `E2`, `E5` |
| `LED_Driver_Stage_1..n` | `E1` … `E7` | `E1`, `E4`, `E5` |
| `Power_Supply_Unit` | `E1` … `E5` | `E2`, `E3` |
| `MCU_Lockstep` | `E1` … `E5` | `E3` |
| `ASIC_Watchdog` | `E1` … `E4` | `E1`, `E2` |
| `Temp_Sense_Chain` | `E1` … `E4` | — |
| `CAN_FD_Transceiver` | `E1` … `E4` | — |
| `LIN_Transceiver` | `E1` … `E3` | — |

Thirty-eight candidates, ten of them on the Golden Thread. The phase 5 spec asks for at least
eight System-FMEA rows with three in the Golden Thread, and a five-row DFMEA extract — so the
selection is a judgement the analyst still has to make and defend, not a matter of transcribing
this table.

**Three candidates are already known to be more than local faults**, and the DFA in phase 5 owes
an answer for each: `Power_Supply_Unit` `E3` (a common `VREF` biasing every reading),
`ASIC_Watchdog` `E3` (a time base that drifts with the part it monitors), and `MCU_Lockstep`
`E5` (mixed-ASIL software sharing one part).

## 6 Open points

| ID | Point | Owner |
|---|---|---|
| `OP-34` | `ASIC_Watchdog` `E2`: de-energising on `SAFE_OFF` is itself `H-01` for the low beam | safety-manager |
| `OP-26` | `MCU_Lockstep` `E5`: freedom from interference needs the software architecture | software-engineer |
| `OP-31` | `CAN_FD_Transceiver` `E4`: bus-off recovery and status readback unspecified | hardware-engineer |
| `OP-8` | The DFA owes an answer on the three coupling candidates in section 5 | safety-analyst |

No new open point is raised here: every one of these already existed, and the P-diagrams have
placed them on a specific component and error state rather than leaving them as prose.

---

**Work products:** `hw_components.md` → `05_hardware/` · `pdiag_*.puml` → `03_model/plantuml/`
**Process reference:** ASPICE **HWE.2** (hardware design) · ISO 26262 **Part 5** (hardware
development) · AIAG-VDA FMEA handbook, step 1 structure analysis and step 2 function analysis —
named by topic, no clause cited.
