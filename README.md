# Beleuchtungssystem Nutzfahrzeug — MBSE-Referenzprojekt (ASPICE + ISO 26262)

Lehr-/Referenzprojekt fuer ein **adaptives Front-Beleuchtungssystem inkl. Arbeitsscheinwerfer-
Steuerung** in einem schweren Nutzfahrzeug (N3, 18 t Sattelzugmaschine).
Durchgaengig modellbasiert (MagicGrid / SysML v1.6), normkonform nach Automotive SPICE (PAM 4.0)
und ISO 26262:2018, mit GitHub als Konfigurationsmanagement- und Nachweisebene.

> **Kein Serienstand.** Alle Zahlenwerte sind plausible Beispielwerte, keine validierten Daten.

- **Ziel-ASIL:** ASIL B (Ausfall Abblendlicht bei Nachtfahrt)
- **Golden Thread:** `SG-01` → `FSR-001` → `TSR` → `SM-01` → `SWC_LightManager` → `TC-021` →
  FTA-Pfad → FMEDA-Zeile → Safety-Case-Argument
- **Zweiter, flacherer Faden:** `SG-02` (Blendung durch Fernlicht/Arbeitsscheinwerfer)

## Einstieg

Arbeitsanleitung: **[HOWTO.md](HOWTO.md)** · Verbindlicher Projektkontext: **[CLAUDE.md](CLAUDE.md)**

```bash
python3 tools/trace_check.py     # Traceability-Konsistenzpruefung
```

In Claude Code: `/phase-run` startet Phase 0 und arbeitet die Phasen 0–11 getaktet ab.

## Struktur

Die Ordner bilden den V-Zyklus ab: Spezifikation (linker Ast) → Realisierung → Nachweis (rechter
Ast). Querschnittsordner wirken auf alle Phasen.

```mermaid
flowchart LR
    subgraph CROSS["Querschnitt — wirkt auf alle Phasen"]
        P["<b>09_process</b><br/>Plaene · Annahmen A-xx<br/>Tailoring · Templates<br/><small>SUP · MAN.3</small>"]
        T["<b>tools</b><br/>trace_check.py<br/>Traceability-Gate<br/><small>SUP.1 · SUP.8</small>"]
        G["<b>.github</b><br/>Actions · PR-/Issue-Templates<br/>CODEOWNERS · Baselines<br/><small>SUP.4 · SUP.8–10</small>"]
    end

    subgraph SPEC["Spezifikation — linker Ast des V"]
        R["<b>01_requirements</b><br/>CR · SYS-REQ<br/><small>SYS.1 · SYS.2</small>"]
        S["<b>02_safety</b><br/>Item Definition · HARA · SG<br/>FSC · TSC · Analysen<br/><small>ISO 26262-3/4/9</small>"]
        A["<b>04_architecture</b><br/>E/E-Architektur · Schnittstellen<br/>Allokation TSR → HW/SW<br/><small>SYS.3</small>"]
        M["<b>03_model</b><br/>SysML-Sichten als PlantUML<br/>MagicGrid-Matrix<br/><small>MBSE</small>"]
    end

    subgraph REAL["Realisierung"]
        HW["<b>05_hardware</b><br/>HW-REQ · Sicherheits-<br/>mechanismen SM-xx<br/><small>HWE.1–4 · Part 5</small>"]
        SW["<b>06_software</b><br/>SW-REQ · Architektur<br/>SWC_LightManager<br/><small>SWE.1–6 · Part 6</small>"]
    end

    subgraph PROOF["Nachweis — rechter Ast des V"]
        V["<b>07_verification</b><br/>Teststrategie · TC-xxx<br/>Fehlerinjektion · Berichte<br/><small>SYS.4 · SYS.5</small>"]
        SC["<b>08_safety_case</b><br/>GSN-Argumentation<br/>Confirmation Measures<br/><small>ISO 26262-2</small>"]
    end

    R -->|"CR speist HARA-Kontext"| S
    R -->|"SYS-REQ"| A
    S -->|"FSR / TSR"| A
    A -->|"Allokation HW"| HW
    A -->|"Allokation SW"| SW
    HW -->|"HW-Verifikation"| V
    SW -->|"Unit- / Integrationstest"| V
    V -->|"Testergebnisse als Evidence"| SC
    S -.->|"Analysenachweise"| SC
    A <-.->|"Modellsichten ↔ Design"| M

    P -.->|"Vorgaben · Annahmen"| R
    T -.->|"prueft Traces ueber alle Ordner"| A
    T -.->|"Coverage-KPIs"| V
    G -.->|"erzwingt Review & Baseline"| T

    classDef spec fill:#e7f0fb,stroke:#3b6ea5,color:#10233a
    classDef real fill:#eaf4ea,stroke:#4a8a4a,color:#102a10
    classDef proof fill:#fdf0e3,stroke:#c07d29,color:#3a2408
    classDef cross fill:#f0edf7,stroke:#7a5ea8,color:#241a3a
    class R,S,A,M spec
    class HW,SW real
    class V,SC proof
    class P,T,G cross

    style SPEC fill:#fafbfd,stroke:#b9c6d6,color:#37475c
    style REAL fill:#fafcfa,stroke:#bcd4bc,color:#37503a
    style PROOF fill:#fdfbf8,stroke:#e0c9a8,color:#5c4726
    style CROSS fill:#fcfbfd,stroke:#cbc0dd,color:#4a3e63
```

**Leseanleitung:** Durchgezogene Pfeile sind der Ableitungsfluss der Work Products — jede Kante ist
im Traceability-Graph als `derived_from` bzw. `allocated_to` hinterlegt. Gestrichelte Pfeile sind
Nachweis- und Steuerbeziehungen: `tools/` prueft die Traces, `.github/` erzwingt Review und
Baseline, `09_process/` setzt die Vorgaben. Der Golden Thread `SG-01` laeuft einmal quer durch alle
vier Bloecke.

| Pfad | Inhalt | Prozessbezug |
|---|---|---|
| `01_requirements/` | Kundenanforderungen, Systemanforderungen | SYS.1, SYS.2 |
| `02_safety/` | Item Definition, HARA, FSC, TSC, Sicherheitsanalysen | ISO 26262-3/4/9 |
| `03_model/` | PlantUML-Modellsichten (Quellen), Exporte (CI-generiert) | MBSE |
| `04_architecture/` | E/E-Architektur, Schnittstellen, Allokation | SYS.3 |
| `05_hardware/` | HW-Anforderungen, Sicherheitsmechanismen, HW-Verifikation | HWE.1–4, Part 5 |
| `06_software/` | SW-Anforderungen, Architektur, Detaildesign | SWE.1–6, Part 6 |
| `07_verification/` | Teststrategie, Testfaelle, Berichte | SYS.4, SYS.5 |
| `08_safety_case/` | GSN, Work-Product-Status, Confirmation Measures | ISO 26262-2 |
| `09_process/` | Plaene, Templates, Annahmen, Tailoring, Meta-Prompt | SUP, MAN.3 |
| `tools/` | CI-Skripte (Traceability) | SUP.1, SUP.8 |
