# Hardware verification plan — Lighting ECU

**Phase 6 · ASPICE HWE.3 (verification of hardware design) / HWE.4 (hardware verification) ·
ISO 26262-5 (hardware integration and verification)**
**Status:** draft · **Owner:** hardware-engineer, with `verification-engineer` for the test cases

> Teaching/reference project. **All numeric values, sample sizes and severities are plausible
> example values, not validated data.**

---

## 1 Scope and the rule this plan enforces

A safety mechanism without a verification entry is not evidence. Every `SM-xx` in `05_hardware/`
therefore has at least one entry below, and every `HW-REQ` is referenced by at least one entry.

`HV-xx` identifiers are **verification-plan line items, not records of the project ID scheme**. Each
one becomes one or more `TC-xxx` records in `07_verification/testcases/`, which is owned by
`verification-engineer` — that is the hand-off, and it is what closes `OP-19` for the new records.

## 2 Verification levels

| Level | Object | Purpose |
|---|---|---|
| Component | Sample circuits, driver stage, sense chain on a test board | Tolerance chains, timing, thresholds — where a fault can still be injected precisely |
| ECU bench (DV) | Design-verification samples, series-intent design | Functional and safety-mechanism verification incl. fault injection, environmental and EMC |
| ECU (PV) | Production-validation samples from series tooling and process | Confirmation on the series process, reduced scope, statistically relevant sample |
| Vehicle | ECU with headlamp modules in the vehicle | Interaction with the real supply and bus, photometry |

DV runs on the design, PV on the process. A PV finding is a process finding; a DV finding is a design
finding. Mixing them is how a design defect gets shipped as a process deviation.

## 3 🔍 DEEP DIVE — verification entries per safety mechanism

| ID | Object | Method | Covers | Acceptance (plausible example) |
|---|---|---|---|---|
| **HV-01** | `SM-01` open-load detection 🔍 | Component + DV bench, fault injection: string disconnect at the connector, single-string disconnect, shunt open/short, amplifier input shorted, ADC reference shifted; over −40 °C … +85 °C and duty 20 … 100 % | `HW-REQ-001` … `005`, `009`, `SM-01` | Measurement uncertainty ≤ ±20 mA at 150 mA; trip guaranteed below 130 mA, no trip above 170 mA; detection ≤ 80 ms in every injected case; no false trip in 8 h of normal operation |
| **HV-02** | `SM-02` watchdog and disable path | DV bench: withhold the answer, wrong answer, answer with correct value but wrong time slot, MCU clock stopped, MCU held in reset | `HW-REQ-017`, `018`, `019`, `SM-02` | `SAFE_OFF` within 50 ms, channel de-energised within a further 10 ms; `SAFE_OFF` dominant with the MCU enable signal forced active |
| **HV-03** | `SM-03` short-to-battery | DV bench, fault injection: channel output shorted to `KL30` in the on-phase and in the off-phase, and through 10 Ω | `HW-REQ-006`, `020`, `SM-03` | Classification "short to battery", not "open load", within 45 ms; correct DTC |
| **HV-04** | `SM-04` overcurrent | DV bench: output shorted to ground, string partially shorted, output capacitance increased | `HW-REQ-007`, `021`, `SM-04` | Current limited to ≤ 1.8 A, latch-off ≤ 5 ms, status readable ≤ 10 ms, no damage in 100 repetitions |
| **HV-05** | `SM-05` derating and thermal design | Climatic chamber per **ISO 16750-4 (climatic loads)** with the LED module; cavity temperature stepped to 105 °C; heat path artificially degraded to twice its thermal resistance; junction temperature by the forward-voltage method | `HW-REQ-008`, `022`, `023`, `024`, `SM-05` | Set point follows the curve within ±5 %; set point never below 400 mA; junction ≤ 135 °C in the case-C condition; NTC open and short both detected |
| **HV-06** | `SM-06` voltage monitoring | DV bench with a programmable supply: ramp 0 → 60 V and back; rails individually forced out of tolerance | `HW-REQ-011`, `012`, `016`, `017`, `SM-06` | Reporting ≤ 10 ms; hardware shutdown ≤ 1 ms above 60 V; recovery ≤ 200 ms; no unintended actuation on any ramp |
| **HV-07** | Load dump and transients | DV per **ISO 16750-2 (electrical loads)** and **ISO 7637-2**, pulse table of `analysis_supply_and_transients.md` | `HW-REQ-013`, `014` | Function class per pulse as tabulated; **no open-load classification triggered by any pulse** |
| **HV-08** | Reverse polarity | DV per **ISO 16750-2**, −32 V for 60 s | `HW-REQ-015` | No damage, no channel energised, function restored afterwards |
| **HV-09** | EMC | DV per **ECE Regulation R10**, with the emission and immunity test methods of **CISPR 25** and **ISO 11452** as referenced by the OEM test plan; low beam on, dimmed to 20 % duty and at the derating floor | `CR-012`, indirectly `HW-REQ-001` | Emission limits met; under immunity exposure no false open-load classification and no set-point deviation > 5 % |
| **HV-10** | Environmental / mechanical | DV per **ISO 16750-3 (mechanical loads)**, **-4 (climatic loads)**, **-5 (chemical loads)**: vibration profile of the front module, thermal shock, damp heat cyclic, salt spray, IP protection | `CR-013`, `CR-014`, `A-11` | No functional deviation, no intermittent contact during vibration monitored on the channel current |
| **HV-11** | HALT / HASS | HALT on DV samples: stepped thermal and vibration stress beyond specification to the operational and destruct limits; HASS as a screening profile derived from the HALT result, applied in production | Design margin, not a requirement | Operational limits ≥ 20 K beyond the specified range; HASS profile ≤ 20 % of the destruct limit; no infant-mortality failure escaping the screen |
| **HV-12** | Bus transceivers | DV bench: bus lines shorted to supply and ground, TXD held dominant | `HW-REQ-025` | Bus released within 5 ms, no damage, recovery after fault removal |
| **HV-13** | Low-beam activation timing 🔍 | Component + DV bench: enable edge to channel current recorded on both channels simultaneously; over 18 … 32 V and −40 °C … +85 °C; set point at nominal and at the derating floor | `HW-REQ-026`, `027`, `028`, `030` | Enable-gate propagation ≤ 1 ms; ≥ 95 % of set point within 20 ms; ramp ≥ 5 ms and monotonic; channel-to-channel skew ≤ 10 ms; hardware share of the activation chain ≤ 25 ms |
| **HV-14** | Switch-on transient: inrush and false-trip freedom 🔍 | DV bench with current probe at the supply input and at both channels; **1000 switch-on cycles** at the corners of supply and temperature, including switch-on into a healthy load and switch-on into a pre-existing open load | `HW-REQ-029`, `030`, interaction with `SM-01` and `SM-06` | Input current ≤ 8 A instantaneous, `VBAT_PROT` dip ≤ 1 V, no `SM-06` undervoltage trip; **no open-load classification in 1000 switch-ons** of a healthy load; with a pre-existing open load, classification at ≤ 110 ms after enable (see `OP-42`) |

**HALT is not a verification of a requirement** — it is a search for the design margin, and it
belongs in this plan precisely because it produces findings no requirement-based test can. HASS,
derived from it, is a production screen and hence PV/series scope.

## 4 DV / PV scope

| Entry | DV | PV | Sample size (plausible example) |
|---|---|---|---|
| HV-01 … HV-06 | full | reduced (HV-01, HV-05, HV-06) | DV 6 units, PV 3 units per lot |
| HV-07, HV-08 | full | — | 3 units |
| HV-09 EMC | full | repeat only after a design change | 3 units |
| HV-10 environmental | full | reduced (vibration, damp heat) | 6 units DV, 3 PV |
| HV-11 HALT / HASS | HALT once per design | HASS 100 % in series | 4 units HALT |
| HV-12 | full | — | 3 units |
| HV-13, HV-14 | full | reduced (HV-14, switch-on cycles at nominal supply only) | DV 6 units, PV 3 units per lot |

## 5 Fault injection — hand-off to `verification-engineer`

The fault list of `HV-01` is not a test-designer's invention; it comes from the six failure-mode
groups of [`analysis_sm01_coverage.md`](analysis_sm01_coverage.md) section 2. The coverage claim of
`SM-01` is only demonstrated if **each group** has at least one injected fault and each of the four
conditional measures is shown to detect what it is credited with. In particular:

- Group 5 (sense chain stuck at a plausible value) must be injected **together with** an open load,
  because the danger is masking, not failure — a sequential test would pass while the masking case
  fails.
- Group 2 (single string lost) must be run at several duty values, since the channel voltage
  signature is what carries the detection.
- Every injection must also be run with the transients of `HV-07` active, otherwise the interaction
  between debounce and disturbance stays untested.

`HV-14` adds a case the `HV-01` fault list does not contain: the open load that is **already present
when the channel is switched on**, rather than appearing during operation. It is the commonest real
case (a lamp unplugged while the vehicle stood) and it exercises the blanking interval of
`HW-REQ-030` instead of the steady-state detection path. The two directions must both be measured —
switch-on into a healthy load, where the acceptance is *no* classification, and switch-on into an
open load, where the acceptance is a classification at ≤ 110 ms.

## 6 Open points

| # | Point | Owner |
|---|---|---|
| 1 | Turn `HV-01` … `HV-12` into `TC-xxx` records (`OP-19` extended to `HW-REQ-011` … `HW-REQ-025`) | verification-engineer |
| 2 | EMC test levels and the applicable OEM test plan to be fixed | systems-engineer, verification-engineer |
| 3 | Junction-temperature measurement method for `HV-05` to be agreed with the LED supplier | hardware-engineer |
| 4 | HALT/HASS profiles depend on the mechanical design, which does not exist yet | hardware-engineer |
| 5 | `HV-14` acceptance for the pre-existing open load (110 ms) is stated against a cap that `SYS-REQ-018` sets at 100 ms — `OP-42` has to be decided before this entry can be turned into a `TC-xxx`, otherwise the test would be written against a requirement it knowingly fails | systems-engineer, then verification-engineer |
| 6 | `HV-13`, `HV-14` → `TC-xxx` records for `HW-REQ-026` … `HW-REQ-030` (`OP-45`, extension of `OP-19`) | verification-engineer |

---

**Work products:** `05_hardware/hw_verification_plan.md`
**Open points:** section 6
**Process reference:** ASPICE **HWE.3** (verification against the hardware design) and **HWE.4**
(hardware verification) · ISO 26262 **Part 5** (hardware integration and verification, including
fault injection as a verification measure) · robustness and environmental testing per **ISO 16750**
series, transients per **ISO 7637-2**, EMC per **ECE R10** (parts and topics named, no clause
numbers cited).
