# Commercial vehicle lighting system — MBSE reference project (ASPICE + ISO 26262)

Teaching/reference project for an **adaptive front-lighting system incl. work-lamp control** in a
heavy commercial vehicle (N3, 18 t tractor unit). Model-based throughout (MagicGrid / SysML v1.6),
compliant with Automotive SPICE (PAM 4.0) and ISO 26262:2018, with GitHub as the configuration
management and evidence layer.

> **Not a production baseline.** All numeric values are plausible example values, not validated data.

- **Target ASIL:** ASIL B (loss of low beam during night driving)
- **Golden Thread:** `SG-01` → `FSR-001` → `TSR` → `SM-01` → `SWC_LightManager` → `TC-021` →
  FTA path → FMEDA row → safety case argument
- **Second, shallower thread:** `SG-02` (glare from high beam / work lamps)

## Getting started

Working guide: **[HOWTO.md](HOWTO.md)** · Binding project context: **[CLAUDE.md](CLAUDE.md)** ·
Current state: **[09_process/project_status.md](09_process/project_status.md)**

```bash
python3 tools/trace_check.py     # traceability consistency check
```

In Claude Code: `/phase-run` starts phase 0 and works through phases 0–11 one at a time.

## Structure

The folders mirror the V-cycle: specification (left branch) → realisation → evidence (right branch).
Cross-cutting folders act on every phase.

```mermaid
flowchart LR
    subgraph CROSS["Cross-cutting — acts on every phase"]
        P["<b>09_process</b><br/>Plans · assumptions A-xx<br/>Tailoring · templates<br/><small>SUP · MAN.3</small>"]
        T["<b>tools</b><br/>trace_check.py<br/>Traceability gate<br/><small>SUP.1 · SUP.8</small>"]
        G["<b>.github</b><br/>Actions · PR/issue templates<br/>CODEOWNERS · baselines<br/><small>SUP.4 · SUP.8–10</small>"]
    end

    subgraph SPEC["Specification — left branch of the V"]
        R["<b>01_requirements</b><br/>CR · SYS-REQ<br/><small>SYS.1 · SYS.2</small>"]
        S["<b>02_safety</b><br/>Item definition · HARA · SG<br/>FSC · TSC · analyses<br/><small>ISO 26262-3/4/9</small>"]
        A["<b>04_architecture</b><br/>E/E architecture · interfaces<br/>Allocation TSR → HW/SW<br/><small>SYS.3</small>"]
        M["<b>03_model</b><br/>SysML views as PlantUML<br/>MagicGrid matrix<br/><small>MBSE</small>"]
    end

    subgraph REAL["Realisation"]
        HW["<b>05_hardware</b><br/>HW-REQ · safety<br/>mechanisms SM-xx<br/><small>HWE.1–4 · Part 5</small>"]
        SW["<b>06_software</b><br/>SW-REQ · architecture<br/>SWC_LightManager<br/><small>SWE.1–6 · Part 6</small>"]
    end

    subgraph PROOF["Evidence — right branch of the V"]
        V["<b>07_verification</b><br/>Test strategy · TC-xxx<br/>Fault injection · reports<br/><small>SYS.4 · SYS.5</small>"]
        SC["<b>08_safety_case</b><br/>GSN argumentation<br/>Confirmation measures<br/><small>ISO 26262-2</small>"]
    end

    R -->|"CR feeds the HARA context"| S
    R -->|"SYS-REQ"| A
    S -->|"FSR / TSR"| A
    A -->|"allocation to HW"| HW
    A -->|"allocation to SW"| SW
    HW -->|"HW verification"| V
    SW -->|"unit / integration test"| V
    V -->|"test results as evidence"| SC
    S -.->|"analysis evidence"| SC
    A <-.->|"model views ↔ design"| M

    P -.->|"rules · assumptions"| R
    T -.->|"checks traces across all folders"| A
    T -.->|"coverage KPIs"| V
    G -.->|"enforces review & baseline"| T

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

**How to read it:** solid arrows are the derivation flow of the work products — every edge is held
in the traceability graph as `derived_from` or `allocated_to`. Dotted arrows are evidence and
control relations: `tools/` checks the traces, `.github/` enforces review and baseline,
`09_process/` sets the rules. The Golden Thread `SG-01` runs once through all four blocks.

| Path | Content | Process reference |
|---|---|---|
| `01_requirements/` | Customer requirements, system requirements | SYS.1, SYS.2 |
| `02_safety/` | Item definition, HARA, FSC, TSC, safety analyses | ISO 26262-3/4/9 |
| `03_model/` | PlantUML model views (sources), exports (CI-generated) | MBSE |
| `04_architecture/` | E/E architecture, interfaces, allocation | SYS.3 |
| `05_hardware/` | HW requirements, safety mechanisms, HW verification | HWE.1–4, Part 5 |
| `06_software/` | SW requirements, architecture, detailed design | SWE.1–6, Part 6 |
| `07_verification/` | Test strategy, test cases, reports | SYS.4, SYS.5 |
| `08_safety_case/` | GSN, work product status, confirmation measures | ISO 26262-2 |
| `09_process/` | Plans, templates, assumptions, tailoring, meta-prompt | SUP, MAN.3 |
| `tools/` | CI scripts (traceability, folder overviews) | SUP.1, SUP.8 |

## Working with the agents

Phases 0–11 are not worked by a generalist but by **nine specialist agents** with clear
responsibilities. The `phase-run` skill routes each phase to the lead agent, the **method skills**
supply the procedures, and two gates secure the result.

```mermaid
flowchart TB
    U["<b>You</b><br/>/phase-run · next<br/>deeper: topic · shorter"]
    SK["<b>Skill phase-run</b><br/>Routing phase → agent<br/>Golden Thread depth rule<br/><small>DEEP DIVE vs. OVERVIEW</small>"]

    subgraph AGENTS["Specialist agents — one leads per phase"]
        direction TB
        A1["<b>systems-engineer</b><br/>CR · SYS-REQ · E/E architecture<br/><small>phase 1 · 3</small>"]
        A2["<b>safety-manager</b><br/>HARA · SG · FSC · TSC · safety case<br/><small>phase 0 · 2 · 9</small>"]
        A3["<b>safety-analyst</b><br/>FMEA · FTA · FMEDA · DFA · STPA<br/><small>phase 5</small>"]
        A4["<b>mbse-modeler</b><br/>MagicGrid · SysML views<br/><small>phase 4</small>"]
        A5["<b>hardware-engineer</b><br/>HW-REQ · SM-xx · HW verification<br/><small>phase 6</small>"]
        A6["<b>software-engineer</b><br/>SW-REQ · SWC_LightManager<br/><small>phase 7</small>"]
        A7["<b>verification-engineer</b><br/>TC-xxx · fault injection<br/><small>phase 8</small>"]
        A8["<b>config-manager</b><br/>CM · baselines · GitHub evidence<br/><small>phase 10 · 11</small>"]
    end

    subgraph METH["Method skills — loaded by the agents"]
        direction TB
        S1["requirements-authoring<br/><small>EARS · req table · RaC schema</small>"]
        S2["hara<br/><small>S/E/C · safe state · FTTI</small>"]
        S3["safety-analyses<br/><small>AP not RPZ · SPFM/LFM/PMHF</small>"]
        S4["mbse-magicgrid<br/><small>PlantUML conventions</small>"]
        S5["safety-case-gsn<br/><small>Goal → Strategy → Evidence</small>"]
        S6["trace-audit<br/><small>coverage KPIs</small>"]
    end

    WP["<b>Work products</b><br/>Requirements-as-Code<br/>PlantUML · analyses · test cases<br/><small>01_… to 09_</small>"]
    TCK{"<b>tools/trace_check.py</b><br/>orphan · dangling · untested<br/>unallocated · asil-drop"}
    QA{"<b>quality-assessor</b><br/>independent review<br/><small>read-only · findings only</small>"}
    OUT["<b>PR + baseline</b><br/>Review evidence SUP.4 · Git tag SUP.8<br/><small>then: next → following phase</small>"]

    U --> SK
    SK --> AGENTS
    METH -.->|"method"| AGENTS
    AGENTS -->|"produce"| WP
    WP --> TCK
    TCK -->|"findings → rework"| AGENTS
    TCK -->|"green"| QA
    QA -->|"blocker / major"| AGENTS
    QA -->|"approval"| OUT

    classDef user fill:#e7f0fb,stroke:#3b6ea5,color:#10233a
    classDef agent fill:#eaf4ea,stroke:#4a8a4a,color:#102a10
    classDef skill fill:#f0edf7,stroke:#7a5ea8,color:#241a3a
    classDef gate fill:#fdf0e3,stroke:#c07d29,color:#3a2408
    classDef out fill:#fbeaea,stroke:#b05252,color:#3a1010
    class U,SK user
    class A1,A2,A3,A4,A5,A6,A7,A8 agent
    class S1,S2,S3,S4,S5,S6 skill
    class WP,TCK,QA gate
    class OUT out

    style AGENTS fill:#fafcfa,stroke:#bcd4bc,color:#37503a
    style METH fill:#fcfbfd,stroke:#cbc0dd,color:#4a3e63
```

**How to read it:** the flow runs top to bottom — you start with `/phase-run`, the skill selects the
responsible agent, that agent produces the work products. Two gates then apply: `tools/trace_check.py`
checks the traces mechanically, the `quality-assessor` reviews independently and read-only. Both
gates loop back to the agents on findings — only after approval do PR and baseline follow. The agents
hand off to each other, e.g. an FMEA finding from the `safety-analyst` becomes a new requirement for
the `systems-engineer`.

### Control words

| Input | Effect |
|---|---|
| `/phase-run` | starts or continues the phase sequence |
| `next` | next phase |
| `deeper: <topic>` | works the topic out at detail level; IDs and values stay unchanged |
| `shorter` | next phase at overview level only |

Who leads which phase and which skills exist: **[HOWTO.md](HOWTO.md)**, sections 3 and 4.

## Language

The project is **English throughout**. The only German document is
`09_process/prompts/prompt_beleuchtungssystem_aspice_iso26262.md` — the original commissioning
document, deliberately left unchanged as the record of what was requested.
