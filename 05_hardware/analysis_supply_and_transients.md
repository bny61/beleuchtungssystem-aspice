# Analysis — supply range, overvoltage, load dump and transients (OP-24, OP-4)

**Status:** applied to the records `HW-REQ-011 … HW-REQ-016`, `SM-06`.
**Owner:** hardware-engineer · **Process:** ASPICE HWE.1 / HWE.2 · ISO 26262-5

> Teaching/reference project. **All numeric values are plausible example values, not validated
> data.** In a real project the test levels and the applicability of individual pulses come from the
> vehicle manufacturer's test plan; here they are assumed (`A-19`).

---

## 1 📋 OVERVIEW — what was undefined

`SYS-REQ-012` covers 16–32 V, `SYS-REQ-013` covers 9–16 V. Everything above 32 V, everything below
9 V and every transient was undefined — the remainder of `OP-2`, tracked as `OP-24`, plus `OP-4`
(function class per `ISO 7637-2` pulse, originating from `CR-017`).

Two things had to be separated that the previous records conflated:

- the **electrical survival** question — does the hardware take damage, and
- the **functional** question — what does the *lighting function* do while the disturbance lasts.

The second is the safety-relevant one: a low beam that switches off during a load dump at night is
exactly hazard `H-01`, whatever the hardware survives.

## 2 Operating-range table

Functional status classes follow the classification scheme of **ISO 16750-1 (functional status
classification)** as used by **ISO 16750-2 (electrical loads)**: **A** full function, **B** reduced
function with automatic recovery, **C** loss of function with automatic recovery, **D** loss of
function requiring a reset or repair. No clause numbers are cited.

| Range (protected input) | Class | Behaviour of the lighting function | Record |
|---|---|---|---|
| U < 6 V | C | ECU unpowered, all channels de-energised, no unintended actuation on the way down or up; recovery ≤ 200 ms | HW-REQ-012 |
| 6 V ≤ U < 9 V | C | Rails collapse in a controlled sequence; driver stages disabled through the enable gate before the rails leave tolerance | HW-REQ-012, HW-REQ-017 |
| 9 V ≤ U < 16 V | B | Low beam energised at the 400 mA derating floor, DTC set; high beam and work lamps inhibited | SYS-REQ-013, HW-REQ-011 |
| 16 V ≤ U ≤ 32 V | A | Full function, unrestricted | SYS-REQ-012 |
| 32 V < U ≤ 36 V | A | Full function; jump-start / overvoltage operating case of ISO 16750-2 | HW-REQ-011, HW-REQ-012 |
| 36 V < U ≤ 60 V, steady | B | Low beam maintained, work lamps and high beam inhibited, DTC set; condition reported within 10 ms | HW-REQ-012, HW-REQ-016 |
| ≤ 58 V, transient ≤ 400 ms (clamped load dump) | A | Low beam maintained at the commanded set point, no damage | HW-REQ-013 |
| U > 60 V | C | Hardware overvoltage shutdown of the driver stages within 1 ms; recovery ≤ 200 ms after the supply returns | HW-REQ-016 |

**Why the shutdown threshold is 60 V and not 40 V.** The clamped load dump of a 24 V system reaches
58 V (`A-19`). A shutdown threshold below that would switch the low beam off during a disturbance
`CR-017` explicitly requires it to survive. The threshold therefore sits **above** the load-dump
level and **below** the assumed 65 V rating of the output stage — a 5 V window that is a real
constraint on component selection, not a free parameter.

## 3 Load dump

Tested per **ISO 16750-2 (electrical loads, load-dump test)** using the pulse shape of
**ISO 7637-2 (pulses 5a / 5b)**.

| Parameter | Plausible example value |
|---|---|
| Clamped test level U_s* | 58 V |
| Decay time constant | 400 ms |
| Generator internal resistance | 2 Ohm |
| Required function class | A for the low beam (`HW-REQ-013`) |

**Unsuppressed load dump (pulse 5a) is explicitly excluded**, recorded as assumption `A-19`: the
vehicle is assumed to suppress load dump centrally. This has to be agreed with the vehicle
manufacturer — if it is wrong, the input stage has to absorb roughly an order of magnitude more
energy and the whole protection topology changes.

**Thermal side effect:** during 400 ms at 58 V input the buck stage of a channel dissipates about
2.4 times its nominal loss (plausible example value). That is inside the pulse rating of the output
stage but it is a DV measurement item, not a calculation item — verification entry `HV-07`.

## 4 🔍 Transient pulse table (closes the hardware side of `OP-4`)

Levels per **ISO 7637-2** for 24 V systems; applicability per the vehicle test plan (`A-19`).

| Pulse | Physical origin | Plausible example level | Required class | Rationale |
|---|---|---|---|---|
| 1 | Supply disconnection from an inductive source | −600 V, 2 ms | **A** | The input series element blocks the negative excursion. A 2 ms interruption of channel current is photometrically irrelevant; what matters is that it causes neither a reset nor a false open-load classification. |
| 2a | Sudden interruption of current in a parallel load | +37 V | **A** | Inside the 60 V envelope of section 2, no functional effect. |
| 2b | DC motor acting as a generator after switch-off | per test plan, 0.2–2 s | **A** | Slow pulse, handled as a temporary overvoltage by the range table. |
| 3a | Switching transients, negative burst | −300 V | **A** | Coupled through the filter; required is immunity of the measurement path, not merely survival. |
| 3b | Switching transients, positive burst | +300 V | **A** | The pulse most likely to disturb the current measurement — the source of the ±10 mA disturbance allowance in `HW-REQ-001`. |
| 4 | Supply reduction during cranking | down to 10 V | **B** | Coincides with the 9–16 V range: low beam at the 400 mA floor per `SYS-REQ-013`. |
| 5a | Unsuppressed load dump | — | **not applicable** | Excluded by `A-19`, central suppression assumed. |
| 5b | Clamped load dump | 58 V, 400 ms | **A** | `HW-REQ-013`. |

### Interaction with `SM-01` — why this is a safety analysis and not an EMC checklist

Pulses 1, 3a and 3b last microseconds to milliseconds. `SM-01` qualifies an open load over a **50 ms
window plus an 8-sample debounce** (`HW-REQ-002`, `HW-REQ-009`). A transient can corrupt individual
samples but **cannot** produce a fault classification on its own — the debounce is not only a noise
filter, it is the argument why `CR-017` and `SG-01` do not conflict. The residual effect of a burst
is a measurement error, which is why `HW-REQ-001` carries an explicit ±10 mA disturbance allowance
instead of pretending the tolerance chain is a bench-top calculation.

## 5 Hand-off to `systems-engineer`

1. **`CR-017` must change.** Its current text ("shall maintain the low-beam function without loss of
   function" for *all* pulses) is neither achievable nor what the design does: pulse 4 gives reduced
   function (class B) by design and pulse 5a is excluded by assumption. Proposal: `CR-017` refers to
   the pulse table above and states a class per pulse. Hardware does not edit `CR-017`.
2. **System requirements are missing** for the ranges the `SYS-REQ` set does not cover (< 9 V and
   > 32 V). The hardware side is specified in `HW-REQ-011` … `HW-REQ-016`, but the functional
   statement ("what does the lighting do above 36 V") belongs at system level.
3. **Interface table** in `04_architecture/ee_architecture.md`: two signals from the supply monitor
   to the microcontroller, `U_Batt` and `RailStatus`, 10 ms, ASIL B.
4. **`A-19`** (central load-dump suppression) needs an interface agreement with the vehicle
   manufacturer, in the same way as `A-05`.

## 6 Open points

| # | Point | Owner |
|---|---|---|
| 1 | `CR-017` text change per section 5.1 | systems-engineer |
| 2 | Confirm `A-19` (clamped load dump, 58 V) with the vehicle manufacturer | systems-engineer, safety-manager |
| 3 | No `SYS-REQ` exists for the behaviour above 36 V; today it is a hardware statement only | systems-engineer |
| 4 | Fix pulse levels and applicability in the DV test plan | verification-engineer |

---

**Work products:** `05_hardware/analysis_supply_and_transients.md`, `HW-REQ-011` … `HW-REQ-016`,
`SM-06`
**Open points:** section 6
**Process reference:** ASPICE **HWE.1** (hardware requirements analysis), **HWE.2** (hardware
design) · ISO 26262 **Part 5** (hardware development — hardware safety requirements and hardware
design) · robustness testing per **ISO 16750-1/-2** and **ISO 7637-2** (parts and topics named, no
clause numbers cited).
