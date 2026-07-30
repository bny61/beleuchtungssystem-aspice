---
name: safety-analyses
description: Templates and calculation schemes for System-FMEA/DFMEA per AIAG-VDA 7 steps with B/A/E and AP (not RPZ), FTA with minimal cut sets, FMEDA with SPFM/LFM/PMHF computation against ASIL targets, DFA coupling-factor analysis and STPA. Use for any failure analysis, cut set, diagnostic coverage or hardware metric task.
---

# Safety analyses

All numbers produced here are **plausible example values**, never validated data. Label them.

## System-FMEA / DFMEA (AIAG-VDA, 7 steps)

Steps: 1 Planung & Vorbereitung · 2 Strukturanalyse · 3 Funktionsanalyse · 4 Fehleranalyse ·
5 Risikoanalyse · 6 Optimierung · 7 Ergebnisdokumentation.

Row format (System-FMEA ≥ 8 rows, ≥3 in the Golden Thread; DFMEA extract 5 rows):

| ID | Systemelement | Funktion | Fehlerfolge (FE) | B | Fehlerart (FM) | Fehlerursache (FU) | Vermeidungsmaßnahme | A | Entdeckungsmaßnahme | E | AP | Maßnahme / Verantwortlich |

- **B** Bedeutung 1–10 · **A** Auftreten 1–10 · **E** Entdeckung 1–10.
- **AP** = Aufgabenpriorität **H / M / N**, derived from the B/A/E combination per the AIAG-VDA AP
  logic (high B with high A drives H). **Never compute or report an RPZ.**
- Every `AP = H` row must have a concrete follow-up action with an owner, and should produce an
  `SM-xx`, a new requirement, or a `RISK-xx`.

## FTA

- Top event = **violation of the safety goal** (not "lamp defect").
- Develop with AND/OR gates down to basic events that are either component failure modes with a λ,
  or systematic causes.
- Emit as PlantUML; add a reading guidance sentence.
- **Minimal cut sets**: derive and list them. Order 1 = **single point fault** → name it explicitly
  and require a safety mechanism or an architecture change.
- Close with: "Single Point Faults vorhanden: ja/nein — Begründung".

## FMEDA

Row format:

| Bauteil | λ [FIT] | Fehlermodus | Anteil [%] | sicherheitsbezogen? | DC [%] | SPF | RF | MPF | SF |

Computation, always shown step by step:

```
λ_total   = Σ λ_i (nur sicherheitsbezogene Bauteile)
λ_SPF/RF  = λ_i · Anteil · (1 − DC)
λ_MPF, λ_SF nach Klassifikation

SPFM = 1 − ( Σ λ_SPF+RF / Σ λ_sicherheitsbezogen )
LFM  = 1 − ( Σ λ_MPF,latent / ( Σ λ_sicherheitsbezogen − Σ λ_SPF+RF ) )
PMHF = Σ λ_SPF+RF   [1/h]   (Vergleich gegen Zielwert in FIT bzw. 1/h)
```

Target values for **ASIL B** per ISO 26262-5: SPFM ≥ 90 %, LFM ≥ 60 %, PMHF < 10⁻⁷ 1/h (100 FIT).
Report each computed value against its target with a pass/fail statement. If a target is missed,
propose the concrete measure (raise DC, add a mechanism, change the architecture) — do not tune the
input numbers to make it pass.

## DFA (Dependent Failure Analysis)

For the decomposed path, one row per coupling factor:

| Kopplungsfaktor | Beschreibung | Betroffene Elemente | Auswirkung | Gegenmaßnahme | Restrisiko |

Cover at minimum: gemeinsame Versorgung, gemeinsamer Takt, gemeinsame Masse, thermische Kopplung,
räumliche Nähe, gemeinsame Software-Ressourcen, gemeinsames Entwicklungswerkzeug, systematische
Ursache (gleicher Designfehler).

## STPA (short form, "Fernlicht ein")

1. Losses and hazards · 2. Control structure (controller, actuator, controlled process, sensor,
feedback) · 3. **Unsafe Control Actions** in the four classes:

| UCA-ID | Control Action | not provided | provided when unsafe | wrong timing/order | too long / stopped too soon |

4. Loss scenarios for the relevant UCAs, and what requirement each scenario generates.

## Verification matrix

| Anforderungs-ID | Analyse | Review | Simulation | Test | Feldnachweis | Nachweisziel |

One primary method per requirement, secondary methods marked — and every safety requirement needs at
least one method that produces a retained record.
