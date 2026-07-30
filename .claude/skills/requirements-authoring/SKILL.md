---
name: requirements-authoring
description: EARS requirement patterns, the mandatory requirement table format, the Requirements-as-Code front-matter schema and the quality criteria (eindeutig, testbar, atomar) for CR/SYS-REQ/FSR/TSR/HW-REQ/SW-REQ. Use whenever writing, reviewing or reformatting a requirement in this project.
---

# Authoring requirements

## EARS patterns (German wording, English keywords kept)

| Pattern | Schablone |
|---|---|
| Ubiquitous | Das `<System>` **soll** `<Antwort>`. |
| Event-driven | **Wenn** `<Trigger>`, **soll** das `<System>` `<Antwort>`. |
| State-driven | **Solange** `<Zustand>`, **soll** das `<System>` `<Antwort>`. |
| Unwanted behaviour | **Wenn** `<unerwünschte Bedingung>`, **soll** das `<System>` `<Antwort>`. |
| Optional feature | **Sofern** `<Merkmal>` **vorhanden ist**, **soll** das `<System>` `<Antwort>`. |
| Complex | Combination of the above — use sparingly, split instead. |

One requirement = one testable statement. "und/oder" in the response part usually means split it.
Quantify: values, units, tolerances, timing bounds. Never "schnell", "zuverlässig", "geeignet".

## Mandatory table format

| ID | Text | Typ | ASIL | Quelle/Trace | Verifikationsmethode | Status |
|---|---|---|---|---|---|---|

- `Typ` ∈ funktional, gesetzlich, Umwelt/Mechanik, Elektrik, Diagnose, Kommunikation, Lebensdauer,
  Sicherheit, Schnittstelle, Prozess
- `ASIL` ∈ QM, A, B, C, D, decomposition notation `B(D)`
- `Verifikationsmethode` ∈ Analyse, Review, Simulation, Test, Feldnachweis
- `Status` ∈ draft, reviewed, approved, implemented, verified, rejected

## Requirements-as-Code schema

`01_requirements/system/SYS-REQ-014.md`:

```markdown
---
id: SYS-REQ-014
text: >
  Wenn der Laststrom eines Abblendlicht-Kanals für mehr als 50 ms unter 150 mA fällt,
  soll das Lighting-ECU den Kanal als "Open Load" klassifizieren.
type: funktional
asil: B
source: CR-007
derived_from: [CR-007, FSR-001]
allocated_to: [ECU_LightingCtrl, SWC_LightManager, SM-01]
verified_by: [TC-021, TC-022]
status: reviewed
rationale: >
  Schwellwert und Entprellzeit aus dem FTTI-Budget von SG-01 abgeleitet
  (plausibler Beispielwert, nicht validiert).
---

## Kontext
Freitext, Herleitung, offene Punkte.
```

Rules:
- `derived_from` is mandatory for everything except `CR-` (which carries `source` = stakeholder).
- `verified_by` may be empty in `draft`, must be non-empty from `reviewed` onward.
- Safety requirements (`asil != QM`) must be allocated (`allocated_to` non-empty).
- File name = ID. One file per requirement; keep IDs stable forever.

`tools/trace_check.py` enforces these — run it after every edit.

## Quality review

Assess each requirement against: **eindeutig** (one reading only), **testbar** (a pass/fail criterion
exists), **atomar** (one statement), **vollständig** (no dangling condition), **verfolgbar** (trace
present), **implementierungsfrei** (says what, not how).

In Phase 1, three requirements are deliberately weak. For each, deliver:
`Review-Kommentar: <Was ist falsch und warum>` + `Verbesserungsvorschlag: <umformulierte Fassung>`.
Typical planted defects: unquantified performance ("ausreichend hell"), two requirements in one
sentence, and a solution-prescribing requirement that belongs in the architecture.
