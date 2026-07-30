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
