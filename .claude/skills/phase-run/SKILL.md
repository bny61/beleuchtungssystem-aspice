---
name: phase-run
description: Run one phase (0-11) of the lighting-system ASPICE/ISO 26262 reference project — loads the phase spec, selects the responsible agent, enforces the Golden Thread depth rule and the mandatory phase closing block. Use when the user says "phase N", "next", "deeper <topic>", "shorter", or asks to start or continue the project.
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
3. **Plan and wait.** Present what the phase will produce — which work products, which IDs,
   which values, what is deliberately left out — and stop for approval. A phase creates a lot
   at once, so this is where a wrong reading is cheapest to correct. Binding rule in
   `CLAUDE.md`, "Plan first, then change".
4. **Produce** the phase content in English, with the format rules from `CLAUDE.md`.
5. **Persist** work products to their repo paths. Requirements/test cases as Requirements-as-Code.
6. **Check** consistency: `python3 tools/trace_check.py` — report real output.
7. **Close** the phase with the mandatory block, then **stop and wait for `next`**.

## Phase → owner

| Phase | Content | Owner agent |
|---|---|---|
| 0 | Project frame, stakeholders, roles, tailoring, glossary, assumptions | `safety-manager` + `config-manager` |
| 1 | Customer requirements `CR-xxx` (SYS.1) | `systems-engineer` |
| 2 | Item definition, HARA, safety goals, FSC (ISO 26262-3) | `safety-manager` |
| 3 | `SYS-REQ`, `TSR`, E/E architecture (SYS.2, SYS.3, Part 4) | `systems-engineer` |
| 4 | MagicGrid model, 8 SysML views | `mbse-modeler` |
| 5 | FMEA, DFMEA, FTA, FMEDA, DFA, STPA, verification matrix | `safety-analyst` |
| 6 | Hardware (HWE.1–4, Part 5) | `hardware-engineer` |
| 7 | Software (SWE.1–6, Part 6) | `software-engineer` |
| 8 | Verification & validation (SYS.4, SYS.5) | `verification-engineer` |
| 9 | Safety case, confirmation measures | `safety-manager` + `quality-assessor` |
| 10 | GitHub CM & evidence | `config-manager` |
| 11 | Traceability & metrics | `config-manager` + `quality-assessor` |

## Depth control

- Default: breadth `📋 OVERVIEW` (3–8 representative entries), depth `🔍 DEEP DIVE` only on the
  SG-01 Golden Thread; SG-02 stays deliberately shallower.
- `deeper: <topic>` → expand that topic to full detail level, keeping every existing ID and value.
- `shorter` → next phase at overview level only; still emit the closing block.
- `next` → next phase in sequence.

## Mandatory phase closing block

```markdown
---
**Work products:** `<filename>` → `<repo path>` (one line each)
**Open points:** numbered, each with an owner
**Process reference:** ASPICE <process IDs> · ISO 26262 <part, topic/clause when certain>
```

## Before starting Phase 0

Ask **at most 3** clarifying questions, and only if the answer would materially change the project
cut. Otherwise start directly and record the open points as `A-xx` assumptions instead. After the
questions, output the table of contents with an estimated size per phase.

## Consistency guard

Before publishing, grep for every ID you reuse (`grep -rn "SYS-REQ-014" .`) and confirm the text,
ASIL and allocation match what was published earlier. A changed value requires an explicit change
note and a Requirement Change issue — never a silent edit.
