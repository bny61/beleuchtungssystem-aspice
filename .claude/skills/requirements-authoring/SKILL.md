---
name: requirements-authoring
description: EARS requirement patterns, the mandatory requirement table format, the Requirements-as-Code front-matter schema and the quality criteria (eindeutig, testbar, atomar) for CR/SYS-REQ/FSR/TSR/HW-REQ/SW-REQ. Use whenever writing, reviewing or reformatting a requirement in this project.
---

# Authoring requirements

## EARS patterns

| Pattern | Template |
|---|---|
| Ubiquitous | The `<system>` **shall** `<response>`. |
| Event-driven | **When** `<trigger>`, the `<system>` **shall** `<response>`. |
| State-driven | **While** `<state>`, the `<system>` **shall** `<response>`. |
| Unwanted behaviour | **If** `<unwanted condition>`, the `<system>` **shall** `<response>`. |
| Optional feature | **Where** `<feature>` **is present**, the `<system>` **shall** `<response>`. |
| Complex | Combination of the above — use sparingly, split instead. |

One requirement = one testable statement. "and/or" in the response part usually means split it.
Quantify: values, units, tolerances, timing bounds. Never "fast", "reliable", "suitable".

## Mandatory table format

| ID | Text | Type | ASIL | Source/trace | Verification method | Status |
|---|---|---|---|---|---|---|

- `Type` ∈ functional, legal, environmental-mechanical, electrical, diagnostics, communication,
  durability, safety, interface, process
- `ASIL` ∈ QM, A, B, C, D, decomposition notation `B(D)`
- `Verification method` ∈ Analysis, Review, Simulation, Test, Field data
- `Status` ∈ draft, reviewed, approved, implemented, verified, rejected

## Requirements-as-Code schema

`01_requirements/system/SYS-REQ-014.md`:

```markdown
---
id: SYS-REQ-014
text: >
  When the load current of a low-beam channel falls below 150 mA for more than 50 ms,
  the lighting ECU shall classify the channel as "open load".
type: functional
asil: B
source: CR-007
derived_from: [CR-007, FSR-001]
allocated_to: [ECU_LightingCtrl, SWC_LightManager, SM-01]
verified_by: [TC-021, TC-022]
status: reviewed
rationale: >
  Threshold and debounce time derived from the FTTI budget of SG-01
  (plausible example value, not validated).
---

## Context
Free text, derivation, open points.
```

Rules:
- `derived_from` is mandatory for everything except `CR-` (which carries `source` = stakeholder).
- `verified_by` may be empty in `draft`, must be non-empty from `reviewed` onward.
- Safety requirements (`asil != QM`) must be allocated (`allocated_to` non-empty).
- File name = ID. One file per requirement; keep IDs stable forever.

`tools/trace_check.py` enforces these — run it after every edit.

## Quality review

Assess each requirement against: **unambiguous** (one reading only), **verifiable** (a pass/fail
criterion exists), **atomic** (one statement), **complete** (no dangling condition), **traceable**
(trace present), **implementation-free** (says what, not how).

In Phase 1, three requirements are deliberately weak. For each, deliver:
`Review comment: <what is wrong and why>` + `Improvement: <reworded version>`.
Typical planted defects: unquantified performance ("sufficiently bright"), two requirements in one
sentence, and a solution-prescribing requirement that belongs in the architecture.
