# Analysis — low-beam current sensing and open-load detection (SM-01 / SYS-REQ-014)

**Status:** **Applied** to the records. Resolves the open point "tolerance analysis of the current
sensing" attached to `SYS-REQ-014`. The records created or changed from this analysis are listed in
section 11; all of them carry a change note.
**Owner:** hardware-engineer · **Process:** ASPICE HWE.1 · ISO 26262-5

> All numeric values are plausible example values of a teaching/reference project, not validated
> data. Design assumptions are marked as `A-xx` candidates.

---

## 1 Assumed sensing topology (`A-08`, `A-09`, `A-11`)

| Item | Plausible example value |
|---|---|
| Channel set point, nominal | 1.20 A (constant-current buck LED driver) |
| String topology | 2 parallel strings x 600 mA, 6 LEDs each, Vf ~ 3.2 V |
| Shunt | 50 mOhm, +/-1.0 % initial, TCR +/-50 ppm/K |
| Sense amplifier | gain 50 V/V, Vos +/-150 uV RTI, gain error +/-1.0 % |
| ADC | 12 bit, Vref 3.3 V +/-0.5 %, offset +/-3 LSB, INL +/-2 LSB |
| PWM | 400 Hz, duty >= 20 % in normal operation |
| Operating range | -40 ... +85 °C ambient |

1 LSB = 0.32 mA of channel current.

## 2 Tolerance chain at the 150 mA threshold

| Group | Worst case |
|---|---|
| Offset-type (amp Vos, ADC offset, INL, quantisation) | +/-4.8 mA |
| Gain-type (shunt tolerance + TCR + drift, amp gain, ADC reference) | +/-3.33 % = +/-5.0 mA |
| Residual conducted-disturbance error allowance | +/-10 mA |
| **Total at threshold** | **+/-20 mA** |

```
Guaranteed trip      I_true < 130 mA   always evaluated as below threshold
Guaranteed no trip   I_true > 170 mA   never evaluated as below threshold
Indeterminate band   130 ... 170 mA    13 % of threshold, 1.7 % of nominal
```

Worst-case reading at the minimum regulated current (1.14 A) is 1.097 A — a factor of 6.4 above the
upper band edge. **The fixed 150 mA threshold is defensible for complete loss of load current.**

**Derived constraint:** the threshold stays free of false trips only while the commanded set point
exceeds 191 mA. With a design margin, the **thermal derating curve must never command a channel
below 400 mA** — otherwise normal derating produces a spurious safe-state transition. This
constraint exists nowhere in the current record set.

## 3 PWM dimming — gating

The measured current is genuinely zero during every PWM off-phase, so an ungated comparison trips on
every dim cycle. Required:

1. **PWM-synchronous, hardware-triggered sampling** — a software trigger cannot guarantee the phase
   relationship under interrupt load, and a phase error of one on-time is a 100 % measurement error.
2. **Blanking** — 50 us after the rising edge (driver rise 20 us, amplifier settling 15 us, filter
   group delay 8 us, edge ringing 10 us), 20 us guard before the falling edge, ~20 us conversion
   → minimum usable on-time **150 us** (6 % duty at 400 Hz).
3. **A validity concept below that on-time** — either a forced diagnostic window of >= 200 us every
   10 ms, or the diagnosis is declared "not available". Reusing a stale sample would make the
   detection time unbounded.

Duty-averaged reconstruction is not acceptable as the sole ASIL B method: a duty error propagates
1:1 into the reconstructed current, and the duty command is itself part of the failure space.

## 4 Timing budget

```
t_sync    worst-case wait for the next valid PWM on-window (400 Hz)  =   2.5 ms
t_acq     blanking + aperture/conversion + filter delay              =   0.1 ms
t_qual    below-threshold qualification window (20 valid samples)    =  50.0 ms
t_deb     debounce (8 valid samples)                                 =  20.0 ms
t_task    worst-case latency of the 5 ms monitoring task             =   5.0 ms
---------------------------------------------------------------------------
t_detect  worst case                                                 =  77.6 ms  -> specify <= 80 ms
t_react   transition to limp-home (SG-01)                            = 150.0 ms
---------------------------------------------------------------------------
Total                                                                = 230.0 ms
FTTI (SG-01)                                                         = 300.0 ms
Margin                                                               =  70.0 ms  (23 %)
```

**The budget closes.** The refined scheme costs 10 ms against the currently published 70 ms.
The published timing in `SG-01`, `SM-01` and `02_safety/02_hara/hara.md` section 4 would change from
70 / 220 / 80 ms to **80 / 230 / 70 ms**.

## 5 Fault discrimination — what a single threshold cannot do

| Fault | Signature at the shunt | Detected? | Additional criterion needed |
|---|---|---|---|
| Complete open load | ~ 0 mA | **yes** | — |
| Short-to-battery | current may bypass the shunt | **false positive** | channel output voltage in the off-state |
| Partial string failure (1 of 2 parallel) | **unchanged at 1.20 A** | **no — structurally blind** | channel output voltage, driver status |
| Series LED short inside a string | current maintained, voltage drops ~3.2 V | no | output voltage plausibility |
| Normal thermal derating | reduced set point by design | no false trip against the *fixed* threshold | commanded set point as a diagnosis input |
| Sense chain stuck-at-high | reads nominal regardless of load | **no — masks a real open load** | zero-current check in the PWM off-phase |

Two conclusions:

- The **parallel-string case is the hard one**: a constant-current driver makes it invisible in the
  current domain by construction. Current sensing alone therefore satisfies `SG-01` (complete loss)
  but **not** `CR-007` ("detect the failure of a low-beam channel") for partial failures.
- The **PWM off-phase does double duty**: it causes the gating problem and is simultaneously a free
  periodic test of the sense chain, because the true current is known to be ~0 there.

## 6 Diagnostic coverage — the 90 % claim in SM-01

**Not defensible with current-threshold sensing alone** — estimate for the bare scheme is
**DC ~ 60 %** (plausible example value). Uncovered: partial load loss, short-to-battery
misclassification, and failures of the diagnostic path itself, which are latent and mask the fault
they should detect.

The 90 % claim becomes arguable if **all four** of these are added: off-phase zero-current check,
channel output voltage sense, LED driver status readback, and ADC reference plausibility check.
Even then the number belongs to `safety-analyst` to confirm against the FMEDA — hardware states only
that the claim is arguable *with* these measures and not arguable *without* them.

---

## 7 Requirement split (applied)

`SYS-REQ-014` keeps its original meaning and its ID — it is part of the Golden Thread. The current
text fails *atomic* ("classify ... **and** increment the fault counter") and *unambiguous* (it does
not say which current, measured when).

| ID | Proposed text (EARS) | Type | ASIL |
|---|---|---|---|
| **SYS-REQ-014** | **When** the load current of a low-beam channel, measured during the PWM on-phase, remains below 150 mA for more than 50 ms, the lighting ECU **shall** classify the channel as "open load". | functional | B |
| SYS-REQ-015 | **When** a low-beam channel is classified as "open load", the lighting ECU **shall** increment the fault counter of that channel. | diagnostics | B |
| SYS-REQ-016 | The lighting ECU **shall** measure the load current with a total uncertainty of not more than +/-20 mA at the 150 mA threshold, over -40 °C to +85 °C. | electrical | B |
| SYS-REQ-017 | **While** the PWM on-time is shorter than 150 us, the lighting ECU **shall** report the open-load diagnosis of that channel as "not available". | diagnostics | B |
| SYS-REQ-018 | **When** an open load occurs, the lighting ECU **shall** report the fault to the fault reaction within 100 ms of fault occurrence. | safety | B |
| SYS-REQ-019 | **When** the measured load current falls below 150 mA, the lighting ECU **shall** classify the cause as exactly one of "open load", "short-to-battery" or "commanded current reduction" before triggering a fault reaction. | diagnostics | B |

## 8 Hardware requirements (applied)

Ten records `HW-REQ-001 … HW-REQ-010`, all ASIL B, `status: draft`:

| ID | Subject |
|---|---|
| HW-REQ-001 | Measurement uncertainty <= +/-20 mA at 150 mA over temperature incl. disturbance allowance |
| HW-REQ-002 | Guaranteed trip below 130 mA, guaranteed no trip above 170 mA |
| HW-REQ-003 | PWM-timer-triggered conversion, 50 us blanking, 20 us guard |
| HW-REQ-004 | Forced diagnostic window >= 200 us every 10 ms below the minimum on-time |
| HW-REQ-005 | Off-phase zero-current self-test, fault above 30 mA for more than 20 ms |
| HW-REQ-006 | Channel output voltage sense in both phases, 100 mV over 0–40 V |
| HW-REQ-007 | LED driver OVP/OCP/thermal status readable, update <= 10 ms |
| HW-REQ-008 | Derating floor: never command below 400 mA while the channel is on |
| HW-REQ-009 | Detection reported to the software fault reaction within 80 ms |
| HW-REQ-010 | ADC reference plausibility check against an independent reference, <= 100 ms |

## 9 Change to SM-01 (applied)

- `text` — extend to PWM-synchronous measurement, off-phase self-test and discrimination against
  short-to-battery and commanded current reduction
- `detection_time` — `50 ms + 20 ms debounce` → `<= 80 ms worst case`, allocated cap 100 ms
- `diagnostic_coverage` — 90 % becomes **conditional** on HW-REQ-005/006/007/010; without them
  ~60 %; confirmation owned by `safety-analyst` via the FMEDA
- `rationale` — updated arithmetic 80 + 150 = 230 ms < 300 ms FTTI

## 10 New assumption candidates

`A-08` driver topology and set point · `A-09` PWM 400 Hz, duty >= 20 % · `A-10` driver status signal
available · `A-11` sensing chain qualified over -40 … +85 °C · `A-12` derating never below 400 mA.

## 11 Impact

**Procedural:** `SYS-REQ-014`, `SM-01`, `SG-01`, `FSR-001`, `CR-007`, `TC-021` are `reviewed`.
A change request with impact analysis is required; `SYS-REQ-014` and `SM-01` drop back to `draft`
and need re-review.

| Artefact | Impact |
|---|---|
| `02_safety/02_hara/hara.md` §4 | timing budget 70 / 220 / 80 → 80 / 230 / 70 ms |
| `07_verification/testcases/TC-021.md` | expected result "within 50 ms plus debounce" → `<= 80 ms`; preconditions must fix the PWM duty; steps must capture off-phase sampling |
| FMEDA (`02_safety/05_analyses/`) | new rows for sense-chain failure modes; the DC row must be re-derived, not carried over; LFM directly affected |
| FTA | new basic-event paths: sense chain stuck-at-high masks the fault; PWM duty below minimum, diagnosis unavailable |
| `06_software/` | 5 ms monitoring task, sample-count debounce, "diagnosis not available" state, DTC differentiation |
| `04_architecture/` | the sense chain becomes a named element with an explicit diagnostic interface |
| `08_safety_case/` G-01 | detection leg now rests on 80 ms; new leg for sense-chain self-test coverage |

**Not affected:** `SG-01` (FTTI and fault reaction time unchanged — the 10 ms is absorbed by margin),
`CR-007`, `FSR-001`.

## 12 Open points

1. Confirmation of the 90 % DC against the FMEDA — `safety-analyst` (blocks SM-01 returning to
   `reviewed`). The hardware side is now decomposed into six failure-mode groups with a per-measure
   sensitivity in `analysis_sm01_coverage.md`, so the claim is checkable rather than assertive.
2. ~~Feasibility of the 400 mA derating floor against the LED module thermal design~~ — **closed in
   phase 6**: floor confirmed, unchanged, see `analysis_thermal_derating.md` and the confirmation
   note in `HW-REQ-008`. The condition is now `HW-REQ-024`.
3. Gating scheme below the minimum on-time: forced window vs. "diagnosis not available" — a system-level
   decision, `systems-engineer`, because it changes the availability of the diagnosis
4. Whether per-string current sensing is added — the only way to see parallel-string loss in the
   current domain; cost/benefit, `systems-engineer` with `hardware-engineer`
5. New test cases for HW-REQ-001 … 010 — `verification-engineer`
6. SYS-REQ ID range 015–019 to be confirmed as free against the later-phase requirement plan

---

## 13 Phase 6 addendum (hardware-engineer)

Section 6 of this analysis is extended by [`analysis_sm01_coverage.md`](analysis_sm01_coverage.md),
which turns the 60 % / 90 % statement into a failure-mode partition the FMEDA can confirm or reject.
Section 12 point 2 is closed by [`analysis_thermal_derating.md`](analysis_thermal_derating.md).
Nothing in sections 1–11 changed.
