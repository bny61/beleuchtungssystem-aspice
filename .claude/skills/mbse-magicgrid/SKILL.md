---
name: mbse-magicgrid
description: MagicGrid (SysML v1.6) method guide plus PlantUML conventions for the eight required model views — MagicGrid matrix, use case, requirements, activity, sequence, state machine, BDD/IBD, parametric and the allocation table. Use whenever a diagram or model view is produced for this project.
---

# MagicGrid modelling & PlantUML conventions

## MagicGrid matrix

Fill with **this project's real artefact IDs**:

| | Requirements | Behavior | Structure | Parameters |
|---|---|---|---|---|
| **Problem Domain (Black Box)** | CR-xxx, SG-xx, FSR-xxx | Use Cases, Activity "Abblendlicht aktivieren" | Kontext/Item-Grenze | Nutzungs-/Umgebungsgrößen (Bordnetz 24 V, T_amb) |
| **Solution Domain (White Box)** | SYS-REQ-xxx, TSR-xxx | State Machine, Sequence "Open Load → DTC" | BDD/IBD Lighting-ECU | Constraints (Lichtstrom, I_LED, T_j) |
| **Implementation** | HW-REQ-xxx, SW-REQ-xxx | Task-/Zykluszeitmodell | HW-Blöcke, SW-Komponenten | Timing-Budgets, Deratingkurve |

Read MagicGrid columns as *what is required / how it behaves / what it is made of / by which values
it is constrained*, rows as increasing solution commitment.

## The eight required views

| # | View | File |
|---|---|---|
| 1 | Use Case (Fahrer, Werkstatt, Fahrzeug-Gateway, Umgebung) | `03_model/plantuml/uc_lighting.puml` |
| 2 | Requirements diagram (`«deriveReqt»`, `«satisfy»`, `«verify»`) | `req_golden_thread.puml` |
| 3 | Activity "Abblendlicht aktivieren inkl. Fehlerfall" | `act_low_beam.puml` |
| 4 | Sequence "Open Load → Fehlerreaktion → DTC" | `seq_open_load.puml` |
| 5 | State Machine "Lichtsystem-Betriebszustände" incl. Safe State | `stm_lighting.puml` |
| 6 | BDD + IBD (Ports, Flows, Signalpfade) | `bdd_system.puml`, `ibd_ecu.puml` |
| 7 | Parametric (Lichtstrom vs. T_j vs. I_LED) | `par_luminous_flux.puml` |
| 8 | Allocation table Funktion → logisch → physisch | `04_architecture/allocation.md` |

## PlantUML conventions

- Every element label carries its project ID: `[Lighting-ECU\n(ECU_LightingCtrl)]`,
  `SYS-REQ-014`, `SM-01`.
- SysML stereotypes as guillemets: `«block»`, `«requirement»`, `«deriveReqt»`, `«satisfy»`,
  `«verify»`, `«allocate»`.
- Safe state is visually distinct in state machines (e.g. `state "Safe State: Notlauf" as SAFE #LightBlue`).
- ASIL shown where meaningful: `note right: ASIL B`.
- Keep each diagram to one message — split rather than cram.

Skeletons:

```plantuml
@startuml req_golden_thread
skinparam rectangle {BackgroundColor White}
rectangle "«requirement»\nSG-01\nKein unerkannter Ausfall\ndes Abblendlichts" as SG01
rectangle "«requirement»\nFSR-001" as FSR001
rectangle "«requirement»\nTSR-003" as TSR003
rectangle "«block»\nSWC_LightManager" as SWC
rectangle "«testCase»\nTC-021" as TC021
SG01 <.. FSR001 : «deriveReqt»
FSR001 <.. TSR003 : «deriveReqt»
TSR003 <.. SWC : «satisfy»
TSR003 <.. TC021 : «verify»
@enduml
```

```plantuml
@startuml stm_lighting
[*] --> Init
Init --> Betrieb_Normal : Selbsttest ok
state "Safe State: Notlauf" as SAFE #LightBlue
Betrieb_Normal --> Degraded : SM-01 Open Load erkannt
Degraded --> SAFE : Reaktionszeit < FTTI
SAFE --> Betrieb_Normal : Fehler behoben && Zündung AUS/EIN
@enduml
```

## Rules

1. One PlantUML block per view, **always followed by 1–2 sentences of Leseanleitung**.
2. No element that does not exist in the requirements/architecture — raise it as an open point instead.
3. Sources are the single source of truth in `03_model/plantuml/`; rendered images are generated
   artefacts (produced by CI into the gitignored `03_model/exports/`, never hand-edited).
   Binary Cameo models (`.mdzip`) are the exception — those go through Git LFS.
4. Syntax check when available: `plantuml -checkonly 03_model/plantuml/*.puml`. If PlantUML is not
   installed, say so rather than claiming the diagram was validated.
