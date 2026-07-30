---
name: safety-analyses
description: Templates and calculation schemes for System-FMEA/DFMEA per AIAG-VDA 7 steps with B/A/E and AP (not RPZ), FTA with minimal cut sets, FMEDA with SPFM/LFM/PMHF computation against ASIL targets, DFA coupling-factor analysis and STPA. Use for any failure analysis, cut set, diagnostic coverage or hardware metric task.
---

# Safety analyses

All numbers produced here are **plausible example values**, never validated data. Label them.

## System-FMEA / DFMEA (AIAG-VDA, 7 steps)

Steps: 1 planning & preparation · 2 structure analysis · 3 function analysis · 4 failure analysis ·
5 risk analysis · 6 optimisation · 7 results documentation.

Row format (system FMEA ≥ 8 rows, ≥3 in the Golden Thread; DFMEA extract 5 rows):

| ID | System element | Function | Failure effect (FE) | S | Failure mode (FM) | Failure cause (FC) | Prevention control | O | Detection control | D | AP | Action / owner |

- **S** severity 1–10 · **O** occurrence 1–10 · **D** detection 1–10.
- **AP** = action priority **H / M / L**, derived from the S/O/D combination per the AIAG-VDA AP
  logic (high severity with high occurrence drives H). **Never compute or report an RPN.**
- Every `AP = H` row must have a concrete follow-up action with an owner, and should produce an
  `SM-xx`, a new requirement, or a `RISK-xx`.

## FTA

- Top event = **violation of the safety goal** (not "lamp defect").
- Develop with AND/OR gates down to basic events that are either component failure modes with a λ,
  or systematic causes.
- Emit as PlantUML; add a reading guidance sentence.
- **Minimal cut sets**: derive and list them. Order 1 = **single point fault** → name it explicitly
  and require a safety mechanism or an architecture change.
- Close with: "Single point faults present: yes/no — rationale".

## FMEDA

Row format:

| Component | λ [FIT] | Failure mode | Share [%] | safety-related? | DC [%] | SPF | RF | MPF | SF |

Computation, always shown step by step:

```
λ_total   = Σ λ_i (safety-related components only)
λ_SPF/RF  = λ_i · share · (1 − DC)
λ_MPF, λ_SF per classification

SPFM = 1 − ( Σ λ_SPF+RF / Σ λ_safety-related )
LFM  = 1 − ( Σ λ_MPF,latent / ( Σ λ_safety-related − Σ λ_SPF+RF ) )
PMHF = Σ λ_SPF+RF   [1/h]   (compare against the target in FIT resp. 1/h)
```

Target values for **ASIL B** per ISO 26262-5: SPFM ≥ 90 %, LFM ≥ 60 %, PMHF < 10⁻⁷ 1/h (100 FIT).
Report each computed value against its target with a pass/fail statement. If a target is missed,
propose the concrete measure (raise DC, add a mechanism, change the architecture) — do not tune the
input numbers to make it pass.

## DFA (Dependent Failure Analysis)

For the decomposed path, one row per coupling factor:

| Coupling factor | Description | Affected elements | Effect | Countermeasure | Residual risk |

Cover at minimum: common supply, common clock, common ground, thermal coupling, spatial proximity,
shared software resources, shared development tool, systematic cause (same design fault).

## STPA (short form, "high beam on")

1. Losses and hazards · 2. Control structure (controller, actuator, controlled process, sensor,
feedback) · 3. **Unsafe Control Actions** in the four classes:

| UCA-ID | Control Action | not provided | provided when unsafe | wrong timing/order | too long / stopped too soon |

4. Loss scenarios for the relevant UCAs, and what requirement each scenario generates.

## Verification matrix

| Requirement ID | Analysis | Review | Simulation | Test | Field data | Evidence objective |

One primary method per requirement, secondary methods marked — and every safety requirement needs at
least one method that produces a retained record.
