# Project: Adaptive Front Lighting System — Commercial Vehicle (ASPICE + ISO 26262)

MBSE reference/teaching project. **Not a production baseline.** Every number is a plausible
example value, never validated data.

## Project variables (binding for all agents and skills)

| Variable | Value |
|---|---|
| `FAHRZEUG` | Heavy truck, class N3, 18 t tractor unit |
| `PRODUKT` | Adaptive front lighting system incl. work-lamp control |
| `ZIEL_ASIL` | ASIL B (loss of low beam during night driving) |
| `LANGUAGE` | **English throughout**; normative terms keep their established form |
| `MBSE_METHODE` | MagicGrid (SysML v1.6) |
| `NOTATION` | PlantUML (fallback: Mermaid) |
| `TOOLCHAIN` | Cameo/MagicDraw, Requirements-as-Code, Git/GitHub, GitHub Actions only (no Jenkins) |
| `UMFANG` | Teaching/reference project, no series status |

> The project is English throughout. The only exception is
> `09_process/prompts/prompt_beleuchtungssystem_aspice_iso26262.md` — the original German
> commissioning document, deliberately left unchanged as the record of what was requested.

## The Golden Thread (depth rule)

Breadth everywhere (3–8 representative entries per work product), full depth on exactly one thread:

**SG-01 "No undetected failure of the low beam while driving" (ASIL B)**
→ FSR → TSR → architecture element → HW safety mechanism → SW component incl. detailed design
→ test cases → FTA path → FMEDA row → safety case argument.

Second, deliberately shallower thread for contrast:
**SG-02 "No unintended glare caused by high beam or work lamps"**

Mark sections visibly: `🔍 DEEP DIVE` (detail) and `📋 OVERVIEW` (breadth).

## ID scheme (never reuse, never silently change)

`CR-` customer req · `SYS-REQ-` system req · `H-` hazard (HARA) · `SG-` safety goal ·
`FSR-` functional safety req · `TSR-` technical safety req · `HW-REQ-` · `SW-REQ-` ·
`SM-` safety mechanism · `TC-` test case · `A-` assumption · `RISK-` risk

Numbering is 3-digit zero-padded (`CR-001`), safety goals and hazards 2-digit (`SG-01`, `H-01`).

`H-` records are the machine-readable form of the HARA rows: they carry situation, malfunction,
S/E/C, resulting ASIL and the safety goal. Every hazard with an ASIL other than QM must have a
safety goal deriving from it (`derived_from: [H-xx]`) — the trace check enforces this.

## Hard rules

1. **No invented standard citations.** Cite a clause number only when certain; otherwise name the
   part and topic ("ISO 26262-6, SW architectural design"). Never quote normative text verbatim.
2. **Assumptions are explicit** as `A-xx` in `09_process/assumptions.md`. Never assume silently.
3. **Consistency is binding.** Once an ID, value, or architecture element is published it does not
   change without an explicit change note (and a CR/impact analysis entry).
4. **Requirements always as a table**: ID · Text · Type · ASIL · Source/trace · Verification method · Status.
   Requirement text follows the **EARS** patterns.
5. **Diagrams always as renderable PlantUML code blocks**, each followed by 1–2 sentences of reading guidance.
6. **Every phase ends with**: Work products (filename + repo path) · Open points · reference to the
   ASPICE process and ISO 26262 part/clause.
7. Realistic numeric values (currents, temperatures, cycle times, failure rates), always labelled as
   plausible example values.

## Repo layout

```
01_requirements/   customer/ (CR), system/ (SYS-REQ)   — SYS.1, SYS.2
02_safety/         item definition, HARA, FSC, TSC, analyses — ISO 26262-3/4/9
03_model/          plantuml/ sources, exports/ rendered  — MBSE
04_architecture/   E/E architecture, interfaces, allocation — SYS.3
05_hardware/       HW-REQ, HW architecture, HW verification — HWE.1–4, Part 5
06_software/       SW-REQ, SW architecture, detailed design — SWE.1–6, Part 6
07_verification/   test strategy, testcases/, reports/     — SYS.4/SYS.5
08_safety_case/    GSN, work product status, confirmation measures — Part 2
09_process/        plans, templates, glossary, assumptions, tailoring — SUP/MAN
tools/             CI scripts (traceability, req lint)
.github/           workflows, issue/PR templates, CODEOWNERS
```

## Requirements-as-Code format

One Markdown file per requirement set; each requirement is a YAML front-matter record or a row in
a `.yaml` file with fields:
`id, text, type, asil, derived_from[], allocated_to[], verified_by[], status, source, rationale`

`status ∈ {draft, reviewed, approved, implemented, verified, rejected}`
`asil ∈ {QM, A, B, C, D, "B(D)"}` (decomposition notation allowed)

`tools/trace_check.py` is the authority on whether the trace graph is consistent — run it before
claiming a phase is complete.

## Phase workflow

Phases 0–11 are defined in `09_process/prompts/prompt_beleuchtungssystem_aspice_iso26262.md`.
Deliver **one phase at a time**, stop, and wait for `next`. Honour `deeper: <topic>` (expand to
detail level) and `shorter` (condense the next phase to overview level).
