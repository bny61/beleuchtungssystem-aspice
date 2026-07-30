---
name: safety-case-gsn
description: Builds the safety case argumentation in GSN (Goal - Strategy - Solution - Evidence) incl. context and assumption nodes, the work product status list, confirmation measures with required independence, and release-for-production criteria. Use for ISO 26262 Part 2 safety management and any "how do we argue this is safe" question.
---

# Safety case & confirmation measures

## GSN element set

| Node | Prefix | Meaning |
|---|---|---|
| Goal | `G-` | a claim to be argued |
| Strategy | `S-` | how the goal is decomposed |
| Solution | `Sn-` | the evidence artefact that discharges a goal |
| Context | `C-` | scope/definition the claim depends on |
| Assumption | `A-` | reuse the project `A-xx` IDs |
| Justification | `J-` | why the strategy is adequate |

Structure for `SG-01`:

```
G-01  SG-01 ist erfüllt: kein unerkannter Ausfall des Abblendlichts während der Fahrt
 ├ C-01 Item-Grenze, Betriebssituationen
 ├ A-03 Annahme zum Fahrerverhalten bei Warnung
 └ S-01 Argumentation über Fehlerklassen (systematisch / zufällig) und Verifikationsebenen
    ├ G-02 Zufällige HW-Ausfälle sind hinreichend erkannt und beherrscht
    │   ├ Sn-01 FMEDA-Auszug SPFM/LFM/PMHF vs. ASIL-B-Ziele
    │   ├ Sn-02 FTA mit Minimal Cut Sets, keine Order-1-Cut-Sets
    │   └ Sn-03 Fehlerinjektionstests TC-03x (Erkennungszeit < FTTI)
    ├ G-03 Systematische Fehler sind durch den Entwicklungsprozess vermieden
    │   ├ Sn-04 Reviewnachweise (PRs, CODEOWNERS, SUP.4)
    │   ├ Sn-05 MISRA-C-Konformität + Deviations mit Begründung
    │   └ Sn-06 Unit-Test-Strukturabdeckung ASIL B
    └ G-04 Anforderungen sind vollständig verfolgt und verifiziert
        └ Sn-07 Traceability-Matrix aus CI (trace_check.py, 0 Findings)
```

Emit the same structure as a PlantUML diagram with a reading-guidance sentence.

## Rules

1. **Every Solution node points to a real artefact** with a repo path and a baseline (tag). A GSN
   leaf without a locatable artefact is an unsupported claim — mark it `offen` rather than drawing it
   as discharged.
2. Assumptions in the argument reuse the project `A-xx` IDs and must appear in
   `09_process/assumptions.md`; safety-relevant ones are validation targets.
3. Distinguish **verification** evidence from **validation** evidence at vehicle level — the safety
   goal argument needs both.
4. State the argument's weaknesses honestly in a "Grenzen der Argumentation" section. A safety case
   that claims no residual uncertainty is not credible.

## Work product status list

| WP-ID | Work Product | Repo-Pfad | ASPICE | ISO-Part | Status | Baseline (Tag) | Verantwortlich |

`Status` ∈ geplant, in Arbeit, im Review, freigegeben, unter Änderung.

## Confirmation measures (ISO 26262-2)

| Maßnahme | Gegenstand | Geforderte Unabhängigkeit (ASIL B) | Durchführender | Nachweis |
|---|---|---|---|---|
| Confirmation Review | HARA, FSC, TSC, Safety Case, Safety Plan | I1/I2 depending on work product and ASIL | | Review-Protokoll |
| Functional Safety Audit | Prozessumsetzung im Projekt | I2/I3 | | Audit-Bericht |
| Functional Safety Assessment | Gesamtargumentation | I3 for high ASIL | | Assessment-Bericht |

State the independence level per measure and **name who may not perform it** (nobody confirms their
own work product; the safety manager does not assess the safety case they authored). Where you are
not certain of the exact required independence level for ASIL B, say "abhängig vom Work Product,
gemäß ISO 26262-2 Tabelle" rather than inventing a level.

## Release for production

Criteria list, each with a hard pass condition: all safety WPs `freigegeben` and baselined; all
`AP = H` FMEA actions closed; HW metrics meeting ASIL B targets; safety goal validation at vehicle
level passed; open `RISK-xx` items accepted and signed; confirmation measures complete;
tool qualification for evidence-producing CI scripts addressed.
