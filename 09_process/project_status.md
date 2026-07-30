# Projektstatus — Arbeitsstand und offene Punkte

> Diese Datei ist der Wiedereinstiegspunkt. Sie wird am Ende jeder Phase fortgeschrieben.
> Letzter Stand: nach Phase 2.

## Phasenstatus

| Phase | Inhalt | Status | Federfuehrend |
|---|---|---|---|
| 0 | Projektrahmen, Stakeholder, Rollen, Tailoring, Glossar | **uebersprungen** | safety-manager, config-manager |
| 1 | Kundenanforderungen `CR-001 … CR-023` (SYS.1) | **abgeschlossen** (Entwurf) | systems-engineer |
| 2 | Item Definition, HARA, Safety Goals, FSC (ISO 26262-3) | **abgeschlossen** (Entwurf) | safety-manager |
| 3 | `SYS-REQ`, `TSR`, E/E-Architektur (SYS.2, SYS.3) | **naechste Phase** | systems-engineer |
| 4 | MBSE-Modell, MagicGrid, 8 SysML-Sichten | offen | mbse-modeler |
| 5 | FMEA, DFMEA, FTA, FMEDA, DFA, STPA | offen | safety-analyst |
| 6 | Hardware (HWE.1–4, Part 5) | offen | hardware-engineer |
| 7 | Software (SWE.1–6, Part 6) | offen | software-engineer |
| 8 | Verifikation & Validierung (SYS.4, SYS.5) | offen | verification-engineer |
| 9 | Safety Case, Confirmation Measures | offen | safety-manager, quality-assessor |
| 10 | GitHub-Konfigurationsmanagement und Nachweis | teilweise vorbereitet | config-manager |
| 11 | Traceability & Metriken | offen | config-manager, quality-assessor |

**Phase 0 wurde uebersprungen** und ist nachzuholen — Rollenmodell, Unabhaengigkeitsgrade und
Tailoring-Entscheidungen fehlen, werden aber spaetestens fuer Phase 9 gebraucht.

## Ergebnisse bisher

- **23 Kundenanforderungen** `CR-001 … CR-023`, alle Kategorien des Lastenhefts abgedeckt.
  Drei davon (`CR-002`, `CR-005`, `CR-016`) sind **bewusst schwach** formuliert und im
  `rationale`-Feld als solche markiert (Lehrzweck).
- **7 Gefaehrdungen** `H-01 … H-07`, davon 6 mit Safety Goal, eine mit Ergebnis QM.
- **2 Safety Goals**: `SG-01` (ASIL B, Golden Thread) und `SG-02` (ASIL A, zweiter Faden).
- **8 FSR** `FSR-001 … FSR-008`, inkl. ASIL-Dekomposition `FSR-005 → FSR-006 QM(A) + FSR-007 A(A)`.
- **Zeitbudget SG-01** geschlossen: 70 ms Erkennung + 150 ms Reaktion = 220 ms < FTTI 300 ms.
- Traceability-Check gruen, 38 Datensaetze.

## Offene Punkte

| ID | Punkt | Owner | Faellig |
|---|---|---|---|
| OP-1 | ASIL-Einstufung der `tbd`-Kundenanforderungen aus der HARA nachziehen | systems-engineer | Phase 3 |
| OP-2 | Verhalten ausserhalb des Bordnetz-Normalbereichs (Unter-/Ueberspannung, Load Dump) fehlt | systems-engineer | Phase 3 |
| OP-3 | `CR-007` ist nicht atomar (Erkennung + Anzeige); Aenderung nur ueber Requirement-Change-Issue | systems-engineer | vor Baseline |
| OP-4 | Geforderte Funktionsklasse je ISO-7637-2-Puls in `CR-017` festlegen | hardware-engineer | Phase 6 |
| OP-5 | Schwache Anforderungen `CR-002`, `CR-005`, `CR-016` vor einer echten Baseline ersetzen | quality-manager | vor Baseline |
| OP-6 | ASCII-Transliteration in den Datensaetzen auf echte Umlaute normalisieren | config-manager | vor Baseline |
| OP-7 | `RISK-01`: E-Einstufung H-01 (E3 vs. E4) im Confirmation Review bestaetigen | safety-manager | Phase 9 |
| OP-8 | `RISK-02`: DFA fuer die Dekomposition von `FSR-005` durchfuehren | safety-analyst | Phase 5 |
| OP-9 | `A-03` (Fahrerreaktion auf Warnung) als Validierungsziel auf Fahrzeugebene planen | verification-engineer | Phase 8 |
| OP-10 | Schnittstellenvereinbarung (DIA) zur Objekterkennung ausserhalb der Item-Grenze (`A-05`) | safety-manager | Phase 3 |
| OP-11 | ~~`RISK-01`/`RISK-02` als Datensaetze anlegen~~ | config-manager | **erledigt** |
| OP-12 | Kontextdiagramm `ctx_item.puml` syntaktisch pruefen (PlantUML lokal nicht installiert) | mbse-modeler | Phase 4 |
| OP-13 | Phase 0 nachholen: Rollenmodell, Unabhaengigkeitsgrade, Tailoring, Glossar | safety-manager | vor Phase 9 |

## Naechster Schritt

**Phase 3** — `SYS-REQ-xxx` aus `CR-xxx` und `FSR-xxx` ableiten, `TSR-xxx` bilden, E/E-Architektur
mit Schnittstellentabelle und Allokationsmatrix. Dabei zu beachten:

- `SYS-REQ-014` existiert bereits (Golden Thread) und darf nicht neu vergeben oder umformuliert werden.
- Die ASIL der Kundenanforderungen aus OP-1 werden hier gesetzt.
- Elementnamen aus Phase 2 sind bindend: `ECU_LightingCtrl`, `LED_Driver_Stage_1`,
  `SWC_LightManager`, `SWC_HighBeamControl`, `SWC_HighBeamMonitor`, `SWC_WorkLampControl`,
  `Fahrzeug_Gateway`, `Item_Beleuchtungssystem`.
