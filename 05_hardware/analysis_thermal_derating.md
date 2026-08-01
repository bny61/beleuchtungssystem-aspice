# Analysis — thermal derating and feasibility of the 400 mA floor (OP-16)

**Status:** applied. `OP-16` is **closed with the result "floor confirmed, unchanged at 400 mA"**,
under the condition stated in section 6.
**Owner:** hardware-engineer · **Process:** ASPICE HWE.1 / HWE.2 · ISO 26262-5

> Teaching/reference project. **All numeric values are plausible example values, not validated
> data.** The thermal model is a lumped two-resistance model, which is adequate for a feasibility
> statement and not adequate for a release.

---

## 1 The question

`HW-REQ-008` and `A-12` forbid the derating function to command a channel below **400 mA**. The
floor exists for a diagnostic reason: below roughly 191 mA the fixed 150 mA open-load threshold of
`SM-01` can no longer distinguish commanded derating from a real open load (`HW-REQ-002`).

A floor is a **refusal to reduce power**. The obvious objection is thermal: if the LED module runs
too hot and the ECU is not allowed to reduce further, does the junction temperature run away?
`OP-16` is exactly that question.

## 2 Thermal model and input values

| Parameter | Plausible example value | Source |
|---|---|---|
| LEDs per channel | 12 (2 parallel strings × 6) | `A-08` |
| Forward voltage at 600 mA / at 200 mA per string | 3.2 V / 2.9 V | `A-08`, `A-20` |
| Radiant (optical) fraction of the electrical power | 30 % | `A-20` |
| Thermal resistance junction → solder point, per LED | 3.5 K/W | `A-20` |
| Thermal resistance module → headlamp cavity | 2.2 K/W (channel) | `A-20` |
| Degraded heat path (soiling, dried thermal interface, blocked convection) | factor 2 → 4.4 K/W | `A-20` |
| Headlamp cavity temperature, hot case / extreme case | 95 °C / 105 °C | `A-20` |
| Junction design limit / component rating | 135 °C / 150 °C | `A-20` |
| Measured quantity of the derating function | solder-point temperature `T_LED` (module NTC) | `HW-REQ-022` |

Derived electrical/thermal figures:

```
I_ch = 1.20 A  ->  P_el = 12 x 3.2 V x 0.6 A = 23.0 W ->  P_th = 16.1 W  (1.34 W per LED)
I_ch = 0.40 A  ->  P_el = 12 x 2.9 V x 0.2 A =  6.96 W ->  P_th =  4.87 W (0.41 W per LED)
Linearised:      P_th  ~ 13.4 W per ampere of channel current
```

## 3 Derating curve (`HW-REQ-023`)

```
I_set [A]
 1.20 |-----------\
      |            \        slope -40 mA/K
 0.40 |             \------------------------  floor (HW-REQ-008, A-12)
      +------------------------------------->  T_LED [°C]
                  105        125
```

- `T_LED` ≤ 105 °C: 1.20 A
- 105 … 125 °C: linear, −40 mA/K
- `T_LED` ≥ 125 °C: hold 400 mA, DTC, status on the bus

The curve is closed-loop through the hardware: reducing the current reduces `P_th`, which reduces
`T_LED`. The operating point is therefore the intersection of the curve with the thermal load line
`T_LED = T_cavity + R_th,module × P_th(I)`, not the end of the curve.

## 4 🔍 Load-line evaluation

Load line: `T_LED = T_cav + R × 13.4 × I`, curve: `I = 1.20 − 0.04 × (T_LED − 105)`.

| Case | T_cav | R_th,module | Equilibrium T_LED | Equilibrium I | T_j | Margin to 135 °C |
|---|---|---|---|---|---|---|
| A — nominal path, hot cavity | 95 °C | 2.2 K/W | 116.7 °C | 733 mA | 119.6 °C | 15 K |
| B — degraded path, hot cavity | 95 °C | 4.4 K/W | 123.1 °C | 476 mA | 125.0 °C | 10 K |
| C — degraded path, extreme cavity | 105 °C | 4.4 K/W | curve clamps → **128.6 °C at the floor** | **400 mA** | **130.0 °C** | **5 K** |
| D — reference: no derating at all | 95 °C | 2.2 K/W | 130.4 °C | 1200 mA | 135.1 °C | −0.1 K |

Case D is the reason derating exists at all: at full current the assumed thermal path reaches the
junction design limit exactly at the hot-cavity condition, with no margin.

Cases A and B **never reach the floor** — the loop settles at 733 mA and 476 mA. The floor is
reached only in case C, and there the equilibrium junction temperature is **130 °C, 5 K below the
135 °C design limit and 20 K below the 150 °C component rating**.

**Feasibility limit.** At the floor the self-heating is `4.4 × 4.87 = 21.4 K` plus 1.4 K junction
rise, so the floor stays admissible as long as

```
T_cavity <= 135 - 1.4 - 21.4 = 112 °C   (degraded heat path)
T_cavity <= 135 - 1.4 - 10.7 = 123 °C   (nominal heat path)
```

## 5 Result for `OP-16`

**The 400 mA floor is confirmed. `HW-REQ-008` and `A-12` keep their value — no change note on the
number is required.** What is added is the *condition* under which the confirmation holds, and that
condition is now an explicit requirement: `HW-REQ-024` (junction ≤ 135 °C at cavity 105 °C with a
doubled thermal resistance and derating active).

Two secondary results:

1. **The floor is not the binding constraint in normal operation.** In both realistic thermal cases
   the loop settles well above 400 mA. The floor is a boundary condition of the diagnosis, not a
   thermal operating point — which is the right way round.
2. **Above 140 °C solder-point temperature the design has no thermal answer.** At 400 mA that
   temperature can only be reached by an external heat source or a secondary failure. Reducing
   current further would break `SM-01`; switching the channel off would produce hazard `H-01`. The
   design therefore keeps the channel at the floor and relies on the driver's own junction
   protection (`SM-04`) as the last resort, reporting the event. **This trade — component
   protection against `SG-01` — is a system-level decision and is handed to `systems-engineer`.**

## 6 Photometric consequence — a genuine open question

With `A-13` (`Phi = 1200 lm × (I/1.20 A) × (1 − 0.004 × (T_j − 25 °C))`) the flux at the floor in
case C is

```
Phi = 1200 x (0.40/1.20) x (1 - 0.004 x (130 - 25)) = 400 lm x 0.58 = 232 lm per channel
```

roughly **19 % of the nominal flux** per channel. Whether two channels at 232 lm still meet the
legal photometric minimum for the passing beam is **not a hardware question** and is not answered
here. The same number applies to the undervoltage case of `SYS-REQ-013`, which uses the same 400 mA.
If the legal minimum is not met, the *limp-home state itself* is non-compliant, and that would
affect `SG-01`'s safe state, not just the derating curve. Hand-off to `systems-engineer`, see
section 7.

## 7 Hand-off to `systems-engineer`

1. Photometric compliance of the 400 mA operating point (derating floor and `SYS-REQ-013`
   undervoltage floor) against the legal minimum for the passing beam — potentially affects the
   definition of the safe state of `SG-01`.
2. The behaviour above 140 °C solder-point temperature (component protection versus `SG-01`) needs a
   system-level decision; hardware's position is "hold the floor and report".
3. `SYS-REQ` level has no requirement for thermal derating at all — `HW-REQ-023` currently derives
   from `CR-014`, which is a QM environmental requirement. A `SYS-REQ` for derating with ASIL B is
   missing.

## 8 New assumptions

`A-20` (thermal model values) and `A-21` (thermal FTTI ≥ 10 s from the module time constant) are
appended in `09_process/assumptions.md`.

---

**Work products:** `05_hardware/analysis_thermal_derating.md`, `HW-REQ-022`, `HW-REQ-023`,
`HW-REQ-024`, `SM-05`; confirmation note in `HW-REQ-008`
**Open points:** section 7; `HW-REQ-024` is a validation target for the DV thermal test (`HV-05`)
**Process reference:** ASPICE **HWE.1/HWE.2** · ISO 26262 **Part 5** (hardware design and hardware
architectural constraints; derating and operating conditions) · environmental testing per
**ISO 16750-4 (climatic loads)**.
