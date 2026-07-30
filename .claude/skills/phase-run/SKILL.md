---
name: phase-run
description: Run one phase (0-11) of the lighting-system ASPICE/ISO 26262 reference project — loads the phase spec, selects the responsible agent, enforces the Golden Thread depth rule and the mandatory phase closing block. Use when the user says "Phase N", "weiter", "tiefer <Thema>", "kürzer", or asks to start/continue the project.
---

# Running a project phase

Authoritative phase specification:
`09_process/prompts/prompt_beleuchtungssystem_aspice_iso26262.md`
Binding project rules: `CLAUDE.md`.

## Procedure

1. **Read** `CLAUDE.md`, then the phase section in the prompt file, then any already-produced work
   products of previous phases (do not re-derive what exists — reuse the exact IDs and values).
2. **Route** to the responsible agent (see table). Multi-owner phases are split by section, not
   merged into one voice.
3. **Produce** the phase content in German, with the format rules from `CLAUDE.md`.
4. **Persist** work products to their repo paths. Requirements/test cases as Requirements-as-Code.
5. **Check** consistency: `python3 tools/trace_check.py` — report real output.
6. **Close** the phase with the mandatory block, then **stop and wait for `weiter`**.

## Phase → owner

| Phase | Content | Owner agent |
|---|---|---|
| 0 | Projektrahmen, Stakeholder, Rollen, Tailoring, Glossar, Annahmen | `safety-manager` + `config-manager` |
| 1 | Kundenanforderungen `CR-xxx` (SYS.1) | `systems-engineer` |
| 2 | Item Definition, HARA, Safety Goals, FSC (ISO 26262-3) | `safety-manager` |
| 3 | `SYS-REQ`, `TSR`, E/E-Architektur (SYS.2, SYS.3, Part 4) | `systems-engineer` |
| 4 | MagicGrid-Modell, 8 SysML-Sichten | `mbse-modeler` |
| 5 | FMEA, DFMEA, FTA, FMEDA, DFA, STPA, Verifikationsmatrix | `safety-analyst` |
| 6 | Hardware (HWE.1–4, Part 5) | `hardware-engineer` |
| 7 | Software (SWE.1–6, Part 6) | `software-engineer` |
| 8 | Verifikation & Validierung (SYS.4, SYS.5) | `verification-engineer` |
| 9 | Safety Case, Confirmation Measures | `safety-manager` + `quality-assessor` |
| 10 | GitHub CM & Nachweis | `config-manager` |
| 11 | Traceability & Metriken | `config-manager` + `quality-assessor` |

## Depth control

- Default: breadth `📋 ÜBERSICHT` (3–8 representative entries), depth `🔍 DEEP DIVE` only on the
  SG-01 Golden Thread; SG-02 stays deliberately shallower.
- `tiefer: <Thema>` → expand that topic to full detail level, keeping every existing ID and value.
- `kürzer` → next phase at overview level only; still emit the closing block.
- `weiter` → next phase in sequence.

## Mandatory phase closing block

```markdown
---
**Work Products:** `<Dateiname>` → `<Repo-Pfad>` (one line each)
**Offene Punkte:** numbered, each with an owner
**Prozessbezug:** ASPICE <Prozess-IDs> · ISO 26262 <Part, Thema/Clause wenn sicher>
```

## Before starting Phase 0

Ask **at most 3** clarifying questions, and only if the answer would materially change the project
cut. Otherwise start directly and record the open points as `A-xx` assumptions instead. After the
questions, output the table of contents with an estimated size per phase.

## Consistency guard

Before publishing, grep for every ID you reuse (`grep -rn "SYS-REQ-014" .`) and confirm the text,
ASIL and allocation match what was published earlier. A changed value requires an explicit change
note and a Requirement Change issue — never a silent edit.
