# FMEDA — Golden Thread extract (SG-01, ASIL B)

**Phase 5 · ASPICE HWE.1 / HWE.3 with SUP.9 feeding back · ISO 26262-5 (evaluation of the hardware
architectural metrics) · ISO 26262-9 (safety analyses, FMEDA)**
**Status:** draft · **Owner:** safety-analyst

> Teaching/reference project. **Every failure rate, share and diagnostic coverage below is a
> plausible example value, not validated data.** Nothing here may be presented as a qualified
> hardware metric.

---

## 1 Scope, and what is deliberately outside it

**Element under consideration:** the SG-01 realisation path — one low-beam channel from the driver
output stage through the ECU output connector, back through the shunt and sense chain into the ADC,
plus the ECU elements the detection and reaction depend on.

| In scope | Why |
|---|---|
| `LED_Driver_Stage_1` (one low-beam channel incl. its enable gate) | actuation of the safety goal |
| Channel connector and in-ECU harness up to the item boundary | `A-13`: the LED module itself is outside |
| `Current_Sense_Chain` | the diagnostic path of `SM-01` |
| `MCU_Lockstep` (safety-related share) | evaluation, PWM/ADC timing, fault reaction |
| `Power_Supply_Unit` | rails and `VREF` — a precondition of everything above |
| `ASIC_Watchdog` | `SM-02` and the `SAFE_OFF` path |

| Out of scope | Why |
|---|---|
| `CAN_FD_Transceiver`, `LIN_Transceiver` | chain A of the timing analysis is bus-independent; the bus carries the *warning* (`FSR-004`), which supports the controllability rating but is not inside the 300 ms FTTI |
| `Temp_Sense_Chain` | runs against the thermal FTTI (`A-21`), not against `SG-01` |
| LED module, headlamp optics | outside the item boundary (`A-13`) |
| `SG-02` elements | no FMEDA on the second thread by design (`📋 OVERVIEW` depth rule) |

Excluding the transceiver is a decision, not an oversight: including it would import ~15 FIT that
cannot violate `SG-01` within the FTTI and would flatter the metric.

## 2 Failure-rate basis

The failure rates follow the **parts-count method of a recognised electronic-component reliability
handbook** (the Siemens SN 29500 family of component failure-rate data — named as the *method*
source; no clause is cited and no value is quoted from it). What is taken from that source is the
**method**: a base failure rate per component class, scaled by an electrical stress factor and an
Arrhenius temperature factor, summed per assembly.

**The numbers themselves in this document are invented plausible examples.** They are of the right
order for automotive electronics and are internally consistent, and that is all that is claimed.

Mission profile assumed for the scaling:

| Parameter | Value |
|---|---|
| Service life | 15 years |
| Operating time | 6 000 h/year, ≈ 90 000 h total |
| Mean ECU internal temperature | 55 °C, worst case 105 °C in the headlamp cavity (`A-20`) |
| Duty | continuous low beam over the night share of `A-07`; PWM duty ≥ 20 % (`A-09`) |
| Electrical environment | 9–36 V, clamped load dump 58 V (`A-19`) |

The mission profile and the handbook reference are **not yet recorded as an `A-xx`** — this phase
creates no assumption records. Hand-off in `OP-59`.

## 3 Classification rules used

| Class | Rule applied here |
|---|---|
| **SPF** | Safety-related failure mode with **no** safety mechanism: the whole λ counts |
| **RF** | Residual of a covered safety-related mode: `λ · (1 − DC)` |
| **MPF** | Failure mode of a *safety mechanism or of the diagnostic path*: on its own it cannot violate `SG-01`, it needs a second fault. Split into MPF-detected (`λ · DC_latent`) and **MPF-latent** (`λ · (1 − DC_latent)`) |
| **SF** | No effect on `SG-01`. Includes modes that lead **into** the `SG-01` safe state (limp-home with a warning) — a spurious but announced degradation is not a safety-goal violation |

Two judgements are worth stating because a reviewer will want to challenge them:

1. **A false trip of `SM-01` is a safe fault for `SG-01`.** It de-energises a healthy channel, warns
   the driver and leaves the remaining channel lit — which *is* the published safe state. It is an
   availability problem, and it is a real one, but it is not a violation of "no **undetected**
   failure of the low beam".
2. **A total loss of supply is a single point fault and no diagnosis can change that.** Detecting it
   does not restore light, and once the rails are gone the ECU cannot even transmit the warning.
   Crediting `SM-06` with coverage there would be crediting a mechanism with an effect it does not
   have. See section 6 and `OP-54`.

## 4 🔍 DEEP DIVE — the FMEDA rows

All λ in FIT (1 FIT = 1 failure per 10⁹ h). Plausible example values throughout.

### 4.1 `Power_Supply_Unit` — λ = 45 FIT

| # | Failure mode | Share | λ | Safety-related? | Mechanism | DC | SPF | RF | MPF-latent | SF |
|---|---|---|---|---|---|---|---|---|---|---|
| P1 | Hard loss of `VBAT_PROT` (input protection or reverse-polarity FET open, output capacitor short) | 12 % | 5.40 | yes | — | 0 % | **5.40** | — | — | — |
| P2 | Rail drift out of tolerance (slow) | 28 % | 12.60 | yes | `SM-06` window comparators | 90 % | — | **1.26** | — | 11.34 |
| P3 | `VREF` drift inside the rail tolerance (E3) | 15 % | 6.75 | diagnostic path | `HW-REQ-010` reference plausibility, 100 ms | 80 % (latent) | — | — | **1.35** | 5.40 |
| P4 | UV/OV comparator stuck — no undervoltage flag (E4) | 15 % | 6.75 | mechanism fault | none required | 0 % (latent) | — | — | **6.75** | — |
| P5 | Damage by transient or reverse polarity (E5) | 10 % | 4.50 | yes | — | 0 % | **4.50** | — | — | — |
| P6 | Auxiliary rails, transceiver supply, no `SG-01` effect | 20 % | 9.00 | no | — | — | — | — | — | 9.00 |

`P4` is a finding, not a modelling artefact: `SM-06` itself says the comparator thresholds must be
testable at power-up, and **no `HW-REQ` requires that test**. 6.75 FIT therefore sit in the latent
column at zero coverage → `OP-53`.

### 4.2 `LED_Driver_Stage_1` (one low-beam channel) — λ = 55 FIT

| # | Failure mode | Share | λ | Safety-related? | Mechanism | DC | SPF | RF | MPF-latent | SF |
|---|---|---|---|---|---|---|---|---|---|---|
| D1 | No output current (E1) | 28 % | 15.40 | yes | `SM-01` core | 99 % | — | **0.154** | — | 15.25 |
| D2 | Output below set point, regulation drift (E2) | 14 % | 7.70 | yes | `HW-REQ-006` channel voltage + `HW-REQ-007` status | 80 % | — | **1.540** | — | 6.16 |
| D3 | Driver-internal latch-off, OCP/OVP/OT (E3) | 22 % | 12.10 | yes | `SM-04` + status readback | 80 % | — | **2.420** | — | 9.68 |
| D4 | Enable gate stuck de-asserted | 8 % | 4.40 | yes | `SM-01` (indistinguishable from an open load, correct reaction) | 99 % | — | **0.044** | — | 4.36 |
| D5 | Enable gate stuck asserted / `SAFE_OFF` leg open | 8 % | 4.40 | mechanism fault (`SM-02` actuation leg) | none required | 0 % (latent) | — | — | **4.40** | — |
| D6 | Output stuck conducting, will not switch off (E4) | 10 % | 5.50 | no for `SG-01` (it is an `SG-02` / `TSR-002` mode) | — | — | — | — | — | 5.50 |
| D7 | Status readback wrong (E7) | 5 % | 2.75 | diagnostic path | plausibility of status against measured current | 60 % (latent) | — | — | **1.10** | 1.65 |
| D8 | Soft-start / inrush faults (E5, E6) | 5 % | 2.75 | no for `SG-01` (activation timing, `SYS-REQ-001`) | — | — | — | — | — | 2.75 |

`D5` is the second half of the same finding as `P4`: the `SAFE_OFF` path is a safety mechanism whose
own failure is never tested. 4.40 FIT latent at zero coverage → `OP-52`.

### 4.3 Channel connector and in-ECU harness — λ = 25 FIT

| # | Failure mode | Share | λ | Mechanism | DC | RF |
|---|---|---|---|---|---|---|
| H1 | Open connection at the ECU output connector | 65 % | 16.25 | `SM-01` core | 99 % | **0.1625** |
| H2 | Short to battery | 20 % | 5.00 | `SM-03` channel voltage | 90 % | **0.5000** |
| H3 | Short to ground | 15 % | 3.75 | `SM-04` overcurrent + status | 95 % | **0.1875** |

### 4.4 `Current_Sense_Chain` — λ = 18 FIT (this element **is** the diagnostic path)

| # | Failure mode | Share | λ | Class | Mechanism | DC_latent | MPF-latent | SF |
|---|---|---|---|---|---|---|---|---|
| C1 | Reads high / stuck at a plausible value — `SM-01` blind (E1, E3) | 45 % | 8.10 | MPF | `HW-REQ-005` off-phase zero-current self-test | 85 % | **1.215** | 6.885 |
| C2 | Reads low — healthy channel classified open (E2) | 25 % | 4.50 | SF | leads into the `SG-01` safe state with a warning | — | — | 4.50 |
| C3 | Gain / offset drift inside the band | 15 % | 2.70 | MPF | `HW-REQ-010` + off-phase test | 80 % | **0.540** | 2.16 |
| C4 | Noise above the band, sample outside the on-phase (E4, E5) | 10 % | 1.80 | MPF | `HW-REQ-003` PWM-triggered conversion, debounce | 80 % | **0.360** | 1.44 |
| C5 | No conversion, open input (E6) | 5 % | 0.90 | MPF | absence of a conversion is self-evident to the evaluation | 99 % | **0.009** | 0.891 |

**Not one row of this component is an SPF.** That is the structural point of the Golden Thread: a
blind sensor cannot on its own turn the lamp off. It needs an open load to become dangerous, which
is why `C1` appears in the fault tree under an AND gate and here in the latent column.

### 4.5 `MCU_Lockstep` (safety-related share) — λ = 60 FIT

| # | Failure mode | Share | λ | Class | Mechanism | DC | RF | MPF-latent |
|---|---|---|---|---|---|---|---|---|
| M1 | Computation fault in the core (E1) | 35 % | 21.00 | RF | dual-core lockstep | 99 % | **0.21** | — |
| M2 | Execution stall, clock stall, hung task (E2) | 18 % | 10.80 | RF | `SM-02` watchdog | 90 % | **1.08** ⚠ | — |
| M3 | ADC conversion fault — gain, offset, stuck (E3) | 17 % | 10.20 | MPF | `HW-REQ-010` reference plausibility | 80 % | — | **2.04** |
| M4 | PWM trigger / sampling-phase fault | 8 % | 4.80 | MPF | `HW-REQ-003` hardware trigger, off-phase test | 80 % | — | **0.96** |
| M5 | Flash / RAM corruption of the application | 12 % | 7.20 | RF | ECC, lockstep, `WdgM` supervision | 90 % | **0.72** | — |
| M6 | Peripheral faults with no `SG-01` effect | 10 % | 6.00 | SF | — | — | — | — |

⚠ `M2` is scored as `RF` **only under the `OP-34` working assumption** (section 7). Without
channel-class differentiation, the reaction to a stalled MCU is `SAFE_OFF` on all stages, which
de-energises the low beam and *is* `H-01` — the whole 10.80 FIT would then be `SPF`.

### 4.6 `ASIC_Watchdog` — λ = 22 FIT

| # | Failure mode | Share | λ | Class | Mechanism | DC | RF | MPF-latent | SF |
|---|---|---|---|---|---|---|---|---|---|
| W1 | Does not trip — passive watchdog (E1) | 40 % | 8.80 | MPF | power-up question/answer negative test (`SM-02`) | 90 % (latent) | — | **0.88** | 7.92 |
| W2 | Trips spuriously (E2) | 25 % | 5.50 | SF ⚠ | low beam held in the hardware default state | — | — | — | 5.50 |
| W3 | Time base drifts with the MCU clock (E3) | 15 % | 3.30 | MPF, common cause | independent oscillator, DFA coupling factor CF-2 | 60 % (latent) | — | **1.32** | 1.98 |
| W4 | `SAFE_OFF` stuck asserted (E4) | 10 % | 2.20 | RF ⚠ | `SM-01` sees the resulting current deviation and warns | 90 % | **0.22** | — | 1.98 |
| W5 | Rail-monitor leg faulty | 10 % | 2.20 | MPF | none required | 0 % (latent) | — | **2.20** | — |

⚠ `W2` and `W4` are scored under the same `OP-34` working assumption as `M2`.

## 5 🔍 DEEP DIVE — the metrics, with the arithmetic shown

### 5.1 Column sums

```
lambda_total (safety-related elements in scope)
  = 45 (PSU) + 55 (Driver) + 25 (Harness) + 18 (Sense) + 60 (MCU) + 22 (Watchdog)
  = 225.000 FIT

lambda_SPF
  = P1 5.40 + P5 4.50
  = 9.900 FIT

lambda_RF
  = P2 1.260
  + D1 0.154 + D2 1.540 + D3 2.420 + D4 0.044      (= 4.158)
  + H1 0.1625 + H2 0.5000 + H3 0.1875              (= 0.850)
  + M1 0.21 + M2 1.08 + M5 0.72                    (= 2.010)
  + W4 0.22
  = 8.498 FIT

lambda_SPF+RF = 9.900 + 8.498 = 18.398 FIT

lambda_MPF,latent
  = PSU  P3 1.35 + P4 6.75                          (= 8.100)
  + Driver D5 4.40 + D7 1.10                        (= 5.500)
  + Sense  C1 1.215 + C3 0.540 + C4 0.360 + C5 0.009 (= 2.124)
  + MCU    M3 2.04 + M4 0.96                        (= 3.000)
  + WD     W1 0.88 + W3 1.32 + W5 2.20              (= 4.400)
  = 23.124 FIT
```

### 5.2 SPFM — single-point fault metric

```
SPFM = 1 - ( lambda_SPF+RF / lambda_total )
     = 1 - ( 18.398 / 225.000 )
     = 1 - 0.081769
     = 0.91823  ->  91.8 %
```

**Target for ASIL B (published target for that ASIL): ≥ 90 %. Result 91.8 % → PASS**, with a margin
of **1.8 percentage points**. That margin is thin, and 9.90 of the 18.398 FIT — **54 %** of the
entire residue — come from two supply failure modes that no mechanism covers (`P1`, `P5`).

### 5.3 LFM — latent fault metric

```
LFM = 1 - ( lambda_MPF,latent / ( lambda_total - lambda_SPF+RF ) )
    = 1 - ( 23.124 / ( 225.000 - 18.398 ) )
    = 1 - ( 23.124 / 206.602 )
    = 1 - 0.111925
    = 0.88808  ->  88.8 %
```

**Target for ASIL B: ≥ 60 %. Result 88.8 % → PASS**, comfortably. Note *why* it is comfortable: the
diagnostic test intervals of `SM-01` (2.5 ms … 100 ms, per `analysis_sm01_coverage.md` section 3)
are all far shorter than one driving cycle, so latent-fault detection does not depend on a power-up
test. The two places where it *does* depend on a power-up test that nobody has specified — `P4` and
`D5` — are exactly the two zero-coverage rows, 11.15 FIT, **48 % of the whole latent residue**.

### 5.4 PMHF — probabilistic metric for random hardware failures

```
PMHF = lambda_SPF+RF
     = 18.398 FIT
     = 18.398 x 10^-9  1/h
     = 1.84 x 10^-8  1/h
```

**Target for ASIL B: < 10⁻⁷ 1/h (100 FIT). Result 1.84 × 10⁻⁸ 1/h → PASS**, using **18 %** of the
budget. PMHF is the least strained of the three metrics, which is the usual pattern at ASIL B and
is the reason SPFM, not PMHF, is the number to watch here.

### 5.5 Summary against the targets

| Metric | Computed | ASIL B target | Verdict | Margin |
|---|---|---|---|---|
| SPFM | **91.8 %** | ≥ 90 % | PASS | 1.8 points |
| LFM | **88.8 %** | ≥ 60 % | PASS | 28.8 points |
| PMHF | **1.84 × 10⁻⁸ 1/h** | < 10⁻⁷ 1/h | PASS | 82 % of the budget unused |

All three verdicts are **conditional on the `OP-34` working assumption** — see section 7.

## 6 🔍 DEEP DIVE — `OP-15`: does the 90 % coverage claim of `SM-01` survive?

`analysis_sm01_coverage.md` proposes a six-group partition and arrives at 59.4 % bare and 93.0 %
with all four conditional measures. The FMEDA's job is to confirm or reject that, from its own rows.

**The scope `SM-01` claims to cover** is the low-beam output path: `LED_Driver_Stage_1` and the
channel harness. Taking only the safety-related modes of those two elements:

```
safety-related lambda in the SM-01 scope
  = D1 15.40 + D2 7.70 + D3 12.10 + D4 4.40        (= 39.60)
  + H1 16.25 + H2 5.00 + H3 3.75                   (= 25.00)
  = 64.600 FIT

undetected residue in that scope (the RF column)
  = D1 0.154 + D2 1.540 + D3 2.420 + D4 0.044
  + H1 0.1625 + H2 0.5000 + H3 0.1875
  = 5.008 FIT

DC(SM-01) = 1 - ( 5.008 / 64.600 ) = 1 - 0.077523 = 0.92248  ->  92.2 %
```

**Verdict on `OP-15`: the claim is CONFIRMED.** The FMEDA reaches **92.2 %** against the hardware
proposal of 93.0 %, and both clear the conditional 90 % of the `SM-01` record. The 0.8-point gap has
one cause and it is worth naming: the FMEDA credits the channel-voltage leg for partial string loss
at **80 %**, where `analysis_sm01_coverage.md` group 2 assumed 85 %. Substituting 85 % reproduces
the hardware figure almost exactly:

```
with DC(D2) = 85 %:  RF(D2) = 7.70 x 0.15 = 1.155
residue = 0.154 + 1.155 + 2.420 + 0.044 + 0.1625 + 0.5000 + 0.1875 = 4.623
DC(SM-01) = 1 - 4.623 / 64.600 = 92.8 %
```

So the two analyses agree to within half a point, and the disagreement is a single deliberate
judgement rather than a different model. The six-group partition of `analysis_sm01_coverage.md` is
**accepted as the basis**, with three qualifications:

1. **The conditionality is confirmed, not softened.** The FMEDA credits `HW-REQ-005`, `006`, `007`
   and `010` explicitly. Remove any one and the residue in section 4.2/4.3 rises above 6.5 FIT and
   the claim falls under 90 % — the same sensitivity the hardware analysis found.
2. **`HW-REQ-004` is credited with nothing**, per decision `OP-17`.
3. **92.2 % is a coverage of the SM-01 scope, not the SPFM.** SPFM is 91.8 % over a much wider
   scope that includes the supply. The two numbers being close is a coincidence of this example and
   must not be read as the same statement.

### 6.1 `OP-23` — does the FMEDA reopen per-string sensing?

`OP-18` decided against per-string current sensing, explicitly conditional on the FMEDA. The FMEDA's
answer: **the decision stands.**

| Question | Answer |
|---|---|
| Can group 2 (partial string loss) support the claimed coverage? | The FMEDA scores it at **80 %**, below the 85 % the hardware partition assumed, and the aggregate still reaches 92.2 % > 90 % |
| Would per-string sensing change the metric materially? | `D2` residue would fall from 1.540 to ≈ 0.385 FIT. SPFM would rise from 91.8 % to **92.3 %** — half a point |
| Is that worth a second shunt and sense channel per stage? | No. Half a point of SPFM against added parts, added λ and a second sense chain that is itself a latent-fault source |

**`OP-23` is closed: per-string sensing is not required by the FMEDA.** The closure carries one
condition, and it is the same one as everywhere else — it holds only while all four conditional
measures are implemented. If `HW-REQ-006` were dropped, group 2 loses its only coverage and
per-string sensing becomes the alternative, not an enhancement.

### 6.2 `OP-43` — does the 30 ms blanking window move the claim?

**No. `OP-43` is closed with no change to any coverage figure.** The reasoning:

- `HW-REQ-030` blanks the *classification*, it does not remove a detection capability. The fault is
  still detected — 30 ms later.
- The FMEDA's diagnostic coverage asks whether a fault is detected **within the FTTI**, not how
  quickly. Start-up case: 30 ms blanking + 80 ms detection + 150 ms reaction = **260 ms < 300 ms**.
  The fault stays in the detected column.
- What the blanking *does* consume is FTTI margin: 70 ms → 40 ms, i.e. 23 % → 13 %.
- And it breaches the 100 ms cap of `SYS-REQ-018` by 10 ms. That is `OP-42`, it belongs to
  `systems-engineer`, and the FMEDA does not resolve it or paper over it.

Stated the other way round: a blanking window would only reduce coverage if it could make a fault
permanently invisible. This one cannot — it expires.

## 7 The `OP-34` conditionality, and what happens if it is decided the other way

**Working assumption (a binding project decision for this analysis, not an analysis result):**
`OP-34` is assumed to be resolved by **differentiating `SAFE_OFF` by channel class** — work lamps
and high beam are de-energised, the low beam goes into a hardware default state and stays lit. Three
rows are scored under that assumption: `M2`, `W2`, `W4`. Each is marked ⚠ in section 4.

If `safety-manager` instead keeps a single undifferentiated `SAFE_OFF`, every reaction to a watchdog
event de-energises the low beam, which is `H-01`:

```
W2 spurious trip          5.50 FIT   SF   ->  SPF   (low beam goes dark on a watchdog fault)
W4 SAFE_OFF stuck         2.20 FIT   RF 0.22 -> SPF 2.20   (delta +1.98)
M2 MCU stall              10.80 FIT  RF 1.08 -> SPF 10.80  (delta +9.72)

lambda_SPF+RF = 18.398 + 5.50 + 1.98 + 9.72 = 35.598 FIT

SPFM = 1 - 35.598 / 225.000 = 1 - 0.158213 = 0.84179  ->  84.2 %   TARGET 90 %  -> FAIL
LFM  = 1 - 23.124 / (225.000 - 35.598) = 1 - 0.122089 = 0.87791  ->  87.8 %      -> pass
PMHF = 35.598 FIT = 3.56 x 10^-8 1/h                                             -> pass
```

**The ASIL B single-point fault metric is met only if `OP-34` is decided by channel-class
differentiation.** That is not a rounding sensitivity, it is a 7.6-point swing across the target.
Recorded as **`RISK-03`**. If the decision goes the other way, this FMEDA and the `SG-01` fault tree
must be redone — they are not adjustable at the margin.

## 8 What the FMEDA hands back

| Finding | Consequence | Routed to |
|---|---|---|
| `P4` + `D5`: 11.15 FIT of latent faults at **zero** coverage, because no `HW-REQ` requires a power-up test of the `SM-06` comparators or of the `SAFE_OFF` path | Two requirements are missing. This phase creates none — raised as `OP-52`, `OP-53` | hardware-engineer |
| `P1` + `P5`: 9.90 FIT of uncovered single point faults in the supply, 54 % of the SPF+RF residue | Architecture or an accepted-risk argument, not a diagnosis. `OP-54` | systems-engineer, safety-manager |
| The 99 % lockstep and 90 % `SM-02` claims have no named evidence source | `OP-55` | hardware-engineer |
| Mission profile and λ basis are not recorded as an assumption | `OP-59` | safety-manager |
| `SM-01` may return to `reviewed` on the coverage question | `OP-15` closed | safety-manager (`OP-20`) |

---

**Work products:** `02_safety/05_analyses/fmeda_golden_thread.md`
**Open points:** `OP-15` **closed** (coverage confirmed at 92.2 %), `OP-23` **closed** (per-string
sensing not required), `OP-43` **closed** (blanking does not move the claim); new `OP-52`, `OP-53`,
`OP-54`, `OP-55`, `OP-59`; `RISK-03` created; `OP-34` deliberately **not** closed — it is assumed,
not decided.
**Process reference:** ASPICE **HWE.1** (hardware requirements analysis) and **HWE.3**
(verification against the hardware design), with **SUP.9** carrying the findings back · ISO 26262
**Part 5** (evaluation of the hardware architectural metrics; hardware architectural design) ·
**Part 9** (safety analyses — FMEDA, and analysis of dependent failures). Parts and topics named, no
clause numbers cited.
