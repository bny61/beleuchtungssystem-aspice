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
G-01  SG-01 is satisfied: no undetected failure of the low beam while driving
 ├ C-01 item boundary, operational situations
 ├ A-03 assumption on driver behaviour on warning
 └ S-01 argument over fault classes (systematic / random) and verification levels
    ├ G-02 random HW failures are sufficiently detected and controlled
    │   ├ Sn-01 FMEDA extract SPFM/LFM/PMHF vs. ASIL B targets
    │   ├ Sn-02 FTA with minimal cut sets, no order-1 cut sets
    │   └ Sn-03 fault injection tests TC-03x (detection time < FTTI)
    ├ G-03 systematic faults are avoided by the development process
    │   ├ Sn-04 review evidence (PRs, CODEOWNERS, SUP.4)
    │   ├ Sn-05 MISRA C conformance + deviations with rationale
    │   └ Sn-06 unit test structural coverage ASIL B
    └ G-04 requirements are fully traced and verified
        └ Sn-07 traceability matrix from CI (trace_check.py, 0 findings)
```

Emit the same structure as a PlantUML diagram with a reading-guidance sentence.

## Rules

1. **Every Solution node points to a real artefact** with a repo path and a baseline (tag). A GSN
   leaf without a locatable artefact is an unsupported claim — mark it `open` rather than drawing it
   as discharged.
2. Assumptions in the argument reuse the project `A-xx` IDs and must appear in
   `09_process/assumptions.md`; safety-relevant ones are validation targets.
3. Distinguish **verification** evidence from **validation** evidence at vehicle level — the safety
   goal argument needs both.
4. State the argument's weaknesses honestly in a "limits of the argument" section. A safety case
   that claims no residual uncertainty is not credible.

## Work product status list

| WP-ID | Work product | Repo path | ASPICE | ISO part | Status | Baseline (tag) | Owner |

`Status` ∈ planned, in progress, in review, released, under change.

## Confirmation measures (ISO 26262-2)

| Measure | Subject | Required independence (ASIL B) | Performed by | Evidence |
|---|---|---|---|---|
| Confirmation review | HARA, FSC, TSC, safety case, safety plan | I1/I2 depending on work product and ASIL | | Review record |
| Functional safety audit | Process implementation in the project | I2/I3 | | Audit report |
| Functional safety assessment | Overall argument | I3 for high ASIL | | Assessment report |

State the independence level per measure and **name who may not perform it** (nobody confirms their
own work product; the safety manager does not assess the safety case they authored). Where you are
not certain of the exact required independence level for ASIL B, say "depends on the work product,
per the table in ISO 26262-2" rather than inventing a level.

## Release for production

Criteria list, each with a hard pass condition: all safety WPs `freigegeben` and baselined; all
`AP = H` FMEA actions closed; HW metrics meeting ASIL B targets; safety goal validation at vehicle
level passed; open `RISK-xx` items accepted and signed; confirmation measures complete;
tool qualification for evidence-producing CI scripts addressed.
