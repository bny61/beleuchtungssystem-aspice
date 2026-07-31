# HOWTO — Working with this project

Reference/teaching project: **Adaptive front lighting system for a heavy commercial vehicle (N3)**,
developed along **Automotive SPICE (PAM 4.0)** and **ISO 26262:2018**, model-based (MagicGrid /
SysML v1.6), with GitHub as the configuration management and evidence layer.

**Language:** the project is English throughout. The only German document is the original
commissioning prompt in `09_process/prompts/`, deliberately left unchanged.

---

## 1. What was set up

```
CLAUDE.md                     Binding project context: variables, ID scheme, Golden Thread, hard rules
HOWTO.md                      This file
tools/trace_check.py          Traceability consistency checker (stdlib only, CI gate)
tools/gen_index.py            Generates a clickable README.md index per requirement folder
tools/gen_trace_graph.py      Generates the Mermaid traceability views and the HTML explorer
tools/hooks/pre-commit        Keeps those indexes up to date on every commit
.claude/agents/               9 role agents
.claude/skills/               7 method skills
.github/                      Workflow, issue templates, PR template, CODEOWNERS
01_… 09_…                     Work product folders (see CLAUDE.md for the mapping)
09_process/prompts/           The original meta-prompt that defines phases 0–11
```

Seed records already in place (they double as the Requirements-as-Code examples):
`CR-007` → `SYS-REQ-014` → `FSR-001` / `SG-01` → `SM-01` → `TC-021`.

---

## 2. Quick start

```bash
cd /Users/ano/Documents/beleuchtungssystem
python3 tools/trace_check.py     # sanity check: should report 6 records, no findings
```

Then start the project in Claude Code:

```
/phase-run
```

The skill asks at most 3 clarifying questions, prints the table of contents with an estimated size
per phase, and then delivers **Phase 0**. After each phase it stops.

### Control words

| You type | What happens |
|---|---|
| `next` | next phase |
| `deeper: FMEDA` | expands that topic to full detail level, keeping all existing IDs and values |
| `shorter` | next phase condensed to overview level |
| `/phase-run 5` | jumps straight to a specific phase |

---

## 3. The agents

Invoke by name (`use the safety-analyst agent to …`) or let Claude route automatically.

| Agent | Owns | Process reference |
|---|---|---|
| `systems-engineer` | `CR-xxx`, `SYS-REQ-xxx`, E/E architecture, interface table, TSR allocation | SYS.1, SYS.2, SYS.3 |
| `safety-manager` | Item definition, HARA, `SG-xx`, FSC/`FSR`, TSC/`TSR`, ASIL decomposition, tailoring, safety case, confirmation measures | ISO 26262-2/3/4/8/9 |
| `safety-analyst` | System-FMEA & DFMEA (B/A/E + AP), FTA + minimal cut sets, FMEDA + SPFM/LFM/PMHF, DFA, STPA, verification matrix | ISO 26262-5/9 |
| `mbse-modeler` | MagicGrid matrix + the 8 SysML views as PlantUML | MBSE |
| `hardware-engineer` | `HW-REQ-xxx`, HW blocks, safety mechanisms `SM-xx`, HW verification plan | HWE.1–4, ISO 26262-5 |
| `software-engineer` | `SW-REQ-xxx`, layered SW architecture, `SWC_LightManager` detailed design, MISRA C, unit test strategy | SWE.1–6, ISO 26262-6 |
| `verification-engineer` | Test strategy, `TC-xxx`, fault injection, validation, regression | SYS.4, SYS.5 |
| `config-manager` | Repo structure, Requirements-as-Code, branching, baselines/tags, issue & PR templates, CODEOWNERS, Actions, Git LFS, ASPICE↔GitHub mapping incl. honest limits | SUP.4, SUP.8, SUP.9, SUP.10, MAN.3 |
| `quality-assessor` | Independent review — consistency, traceability, invented citations, silent assumptions, independence. **Read-only: reports findings, never patches.** | SUP.1, SUP.4, ISO 26262-2 |

Agents hand off to each other explicitly (each definition has a *Handoffs* section), so an analysis
finding lands as a requirement change rather than dying in a report.

---

## 4. The skills

| Skill | Use it for |
|---|---|
| `phase-run` | Running a phase; owns phase→agent routing, depth control and the closing block |
| `requirements-authoring` | EARS patterns, requirement table format, Requirements-as-Code schema, quality criteria |
| `hara` | Item definition, operational situations, S/E/C with rationale, safety goals with safe state/FTTI, FSC, ASIL decomposition |
| `safety-analyses` | AIAG-VDA FMEA (AP, not RPZ), FTA + cut sets, FMEDA calculation scheme with ASIL B targets, DFA, STPA |
| `mbse-magicgrid` | MagicGrid matrix, the 8 required views, PlantUML conventions |
| `safety-case-gsn` | GSN argumentation, work product status list, confirmation measures, release-for-production criteria |
| `trace-audit` | Running the trace check, coverage KPIs, the Golden Thread matrix |

Invoke with `/hara`, `/safety-analyses`, … or just describe the task — descriptions are written so
Claude picks them up automatically.

---

## 5. Daily workflow

1. **Work a phase** — `/phase-run`, then `weiter` after each stop.
2. **Persist requirements** as Requirements-as-Code files (one file per ID, filename = ID).
3. **Check before closing a phase:**
   ```bash
   python3 tools/trace_check.py
   python3 tools/trace_check.py --matrix 07_verification/reports/traceability_matrix.md
   python3 tools/gen_index.py     # folder overviews (runs automatically via the pre-commit hook)
   ```
4. **Review independently:** `use the quality-assessor agent to review Phase 3` — it returns a
   finding table with severities and a pass/conditional/fail verdict.
5. **Baseline a gate:** `git tag -a BL-PH3-v1.0 -m "Baseline Gate SYS.3"`.

### Traceability checks enforced

`orphan` · `dangling` · `untested` · `unallocated` (ASIL ≠ QM without allocation) · `asil-drop`
(derived requirement below its parent's ASIL without decomposition) · `duplicate-id` ·
`sg-uncovered` (safety goal with no FSR) · `hazard-uncovered` (hazard with ASIL ≠ QM and no safety
goal) · `id-scheme`.

Exit code 1 on findings — that is what makes it usable as a required check.

### Following traceability visually

Three complementary views, all generated from the same records:

| View | Where | Good for |
|---|---|---|
| **Mermaid graphs** | `07_verification/reports/traceability_views.md` | Following a thread end to end. Rendered by GitHub. One view per safety goal plus the Golden Thread. |
| **Upstream / downstream columns** | every folder `README.md` | "What hangs off this record?" — scales to any repo size, no diagram needed. |
| **Interactive explorer** | `07_verification/reports/trace_explorer.html` | Searching and filtering all records, hopping along links. Open it **locally** in a browser — GitHub does not render HTML stored in a repo. |

```bash
python3 tools/gen_trace_graph.py           # regenerate views and explorer
python3 tools/gen_trace_graph.py --check   # verify only
open 07_verification/reports/trace_explorer.html   # macOS
```

Large safety goal views deliberately show the derivation skeleton only — allocation and
verification links converge on a few nodes and would obscure the structure. They stay complete in
the link table under each view. **A diagram is never the completeness evidence**; that is
`traceability_matrix.md` plus `trace_check.py`.

### Folder overviews — kept up to date automatically

**Every folder** gets a generated `README.md`, so opening one tells you what it is for:

- folders holding requirement records get the record table (ID → file, text, type, ASIL, status,
  upstream, downstream) plus a list of the other documents in that folder;
- all other folders get a purpose line and a file listing, with each file's purpose extracted from
  its own content — the `title` of a PlantUML view, the first heading of a Markdown file, the
  docstring of a script;
- container folders additionally list their subfolders.

Record folders with enough variety additionally get a **grouping by allocated element**. A record
appears under *every* element it is allocated to — allocation is many-to-many, which is exactly why
this is a grouping and not a folder split. The grouping is suppressed where it would not
discriminate (e.g. customer requirements, which nearly all allocate to the item as a whole).

**When to introduce subfolders.** The generator prints a note once a folder passes 40 records, and
it prints the evidence with it: split only by a field that is **single-valued for every record** in
that folder. For hardware requirements `allocated_to` is not — every single one is allocated to
several elements, so a split by component would force an arbitrary filing decision per record and
send readers to the wrong folder. For software requirements it may well be single-valued per
`SWC_*`; the note tells you which case you are in instead of leaving it to taste.

`03_model/plantuml/` also documents the file name prefixes (`uc_`, `req_`, `act_`, `seq_`, `stm_`,
`bdd_`, `ibd_`, `par_`, `ctx_`), which is what the view type is encoded in.

GitHub renders these as soon as you open the folder. Three layers keep them current:

| Layer | What it does | Setup |
|---|---|---|
| Pre-commit hook | Regenerates the overviews and adds them to the commit | `ln -sf ../../tools/hooks/pre-commit .git/hooks/pre-commit` (once per clone) |
| CI on pull requests | Fails the check if an overview is stale | automatic |
| CI on push to `main` | Regenerates and commits the result back | automatic |

Manual run: `python3 tools/gen_index.py` · verify only: `python3 tools/gen_index.py --check`

The generator refuses to touch a `README.md` that lacks its generated-by marker, so hand-written
folder READMEs — including the repo root one — are safe. Edit the record, never the overview.

---

## 6. Adding a requirement

Create `01_requirements/system/SYS-REQ-021.md`:

```markdown
---
id: SYS-REQ-021
text: >
  When <trigger>, the lighting ECU shall <response>.
type: functional
asil: B
source: CR-012
derived_from: [CR-012]
allocated_to: [ECU_LightingCtrl]
verified_by: [TC-031]
status: draft
rationale: >
  Derivation; mark plausible example values as such.
---

## Context
```

Then run the trace check. `status: draft` tolerates an empty `verified_by`; from `reviewed` onward
it is a finding. See `01_requirements/system/SYS-REQ-014.md` for the filled reference.

---

## 7. GitHub side (optional, for phase 10)

Already prepared: workflow `.github/workflows/traceability.yml`, four issue templates
(Change Request, Problem Report, Safety Anomaly, Requirement Change), PR template with review
checklist, `CODEOWNERS`, `.gitattributes` with Git LFS rules.

To activate on a real remote:

```bash
git add -A && git commit -m "chore: initial project skeleton"
gh repo create <name> --private --source=. --push
```

Then, in the repository settings:
- Branch protection on `main`: require PR, require the `Traceability consistency check` check,
  require Code Owner review, no force pushes.
- Replace the placeholder handles in `.github/CODEOWNERS` with real users/teams.
- Labels: `asil-b`, `safety-relevant`, `sys-req`, `swe`, `hwe`, `impact-analysis-required`.
- Commits: Conventional Commits with the requirement ID in the footer — `Refs: SYS-REQ-014`.
- Baselines: annotated tags + GitHub Releases per gate.

**Nothing is committed or pushed automatically** — the agents only write files locally.

---

## 8. Rules that are enforced, not suggested

- **No invented standard citations.** Clause numbers only when certain, otherwise part + topic. No
  verbatim normative text.
- **Assumptions are explicit** as `A-xx` in `09_process/assumptions.md`.
- **IDs and values never change silently** — a change needs a change note and a Requirement Change
  issue.
- **Every numeric value is a plausible example value**, labelled as such. Nothing here is validated
  data, and nothing here is a production baseline.
- **Depth rule:** breadth 3–8 entries per work product (`📋 OVERVIEW`), full depth only along the
  SG-01 Golden Thread (`🔍 DEEP DIVE`).

## 9. Known limits

- `tools/trace_check.py` produces safety-case evidence and is therefore a **tool qualification
  candidate**. The classification is sketched in `09_process/plans/tool_qualification.md`; a real
  qualification is **not** performed. Treat a green CI run as supporting evidence only.
- The front-matter parser covers a YAML subset (scalars, folded blocks, inline and dash lists) —
  enough for this schema, not a general YAML implementation. Anchors, nested maps and multi-document
  files are not supported.
- GitHub alone does not provide independence of assessment, qualified tool confidence, or a records
  system with regulatory retention guarantees. Phase 10 must state these limits rather than paper
  over them.
