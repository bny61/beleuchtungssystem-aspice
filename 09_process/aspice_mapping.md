# ASPICE and ISO 26262 mapping — process area to work product

**Owner:** config-manager · **Status:** draft · **Process reference:** ASPICE SUP.8, MAN.3 ·
ISO 26262-2 (safety management)

> Teaching/reference project. The allocation below says where a work product *belongs*; it does
> not claim the work product exists. Whether an area is populated is computed from the repo by
> `tools/gen_req_browser.py`, never asserted here — an area with nothing allocated to it shows up
> as empty, and that is the point.

## Why this file exists

Process references used to live as prose inside individual records ("ASPICE SYS.2", "ISO 26262-4"),
which meant no one could answer "what is missing" without reading everything. This table is the
single place where the allocation is stated, so it can be reviewed, and so the requirements browser
can present the project along the V-model instead of along the folder tree.

**A record can appear under both frameworks.** `HW-REQ-011` is an ASPICE HWE.1 work product *and*
part of ISO 26262-5. That is not double counting — the two frameworks ask different questions of the
same artefact, and forcing a single home would lose one of them.

## How to read the table

| Column | Meaning |
|---|---|
| `Area` | Process area (ASPICE) or part (ISO 26262) |
| `Framework` | `ASPICE` or `ISO` — selects which grouping the row appears in |
| `Level` | `system`, `software`, `hardware`, `concept` or `supporting` — groups the V-model tiers |
| `Side` | `left` (specification), `right` (verification) or `supporting` |
| `Records` | Which Requirements-as-Code records belong here: `path:<folder>` or `id:<ID prefix>` |
| `Documents` | Narrative work products, as repo-relative paths |

`-` means nothing is allocated yet. For most `SWE.*` rows that is the honest state of this project:
phase 7 has not been run.

## Mapping

| Area | Framework | Name | Level | Side | Records | Documents |
|---|---|---|---|---|---|---|
| SYS.1 | ASPICE | Requirements elicitation | system | left | path:01_requirements/customer | - |
| SYS.2 | ASPICE | System requirements analysis | system | left | path:01_requirements/system | - |
| SYS.3 | ASPICE | System architectural design | system | left | - | 04_architecture/ee_architecture.md, 04_architecture/allocation.md, 03_model/magicgrid.md |
| SYS.4 | ASPICE | System integration and integration test | system | right | - | - |
| SYS.5 | ASPICE | System qualification test | system | right | id:TC- | 07_verification/reports/traceability_matrix.md, 07_verification/reports/traceability_views.md |
| SWE.1 | ASPICE | Software requirements analysis | software | left | id:SW-REQ- | - |
| SWE.2 | ASPICE | Software architectural design | software | left | - | - |
| SWE.3 | ASPICE | Software detailed design and unit construction | software | left | - | - |
| SWE.4 | ASPICE | Software unit verification | software | right | - | - |
| SWE.5 | ASPICE | Software integration and integration test | software | right | - | - |
| SWE.6 | ASPICE | Software qualification test | software | right | - | - |
| HWE.1 | ASPICE | Hardware requirements analysis | hardware | left | id:HW-REQ- | 05_hardware/analysis_current_sensing.md, 05_hardware/analysis_low_beam_activation.md |
| HWE.2 | ASPICE | Hardware design | hardware | left | id:SM- | 05_hardware/hw_architecture.md, 05_hardware/hw_components.md, 05_hardware/analysis_supply_and_transients.md, 05_hardware/analysis_thermal_derating.md |
| HWE.3 | ASPICE | Verification against the hardware design | hardware | right | - | 05_hardware/analysis_sm01_coverage.md |
| HWE.4 | ASPICE | Hardware verification | hardware | right | - | 05_hardware/hw_verification_plan.md |
| MAN.3 | ASPICE | Project management | supporting | supporting | - | 09_process/project_status.md |
| SUP.1 | ASPICE | Quality assurance | supporting | supporting | - | - |
| SUP.4 | ASPICE | Joint review | supporting | supporting | - | .github/pull_request_template.md |
| SUP.8 | ASPICE | Configuration management | supporting | supporting | - | 09_process/plans/tool_qualification.md, 09_process/aspice_mapping.md |
| SUP.9 | ASPICE | Problem resolution management | supporting | supporting | - | .github/ISSUE_TEMPLATE/problem_report.yml |
| SUP.10 | ASPICE | Change request management | supporting | supporting | - | .github/ISSUE_TEMPLATE/change_request.yml |
| Part 2 | ISO | Safety management, safety case | supporting | supporting | - | - |
| Part 3 | ISO | Concept phase: item definition, HARA, FSC | concept | left | path:02_safety/02_hara, path:02_safety/03_fsc | 02_safety/01_item_definition/item_definition.md, 02_safety/02_hara/hara.md, 02_safety/02_hara/operational_situations.md, 02_safety/02_hara/sec_classification.md |
| Part 4 | ISO | Product development at system level (TSC) | system | left | path:02_safety/04_tsc | 04_architecture/ee_architecture.md |
| Part 5 | ISO | Product development at hardware level | hardware | left | id:HW-REQ-, id:SM- | 05_hardware/hw_architecture.md, 05_hardware/hw_components.md, 05_hardware/hw_verification_plan.md, 05_hardware/analysis_low_beam_activation.md |
| Part 6 | ISO | Product development at software level | software | left | id:SW-REQ- | - |
| Part 8 | ISO | Supporting processes | supporting | supporting | - | 09_process/assumptions.md, 09_process/plans/tool_qualification.md |
| Part 9 | ISO | ASIL-oriented and safety-oriented analyses | supporting | supporting | path:02_safety/05_analyses | - |

## Known gaps this table makes visible

- **`SWE.1` … `SWE.6` and ISO 26262-6 are empty.** Phase 7 has not been run; `06_software/` holds
  skeleton folders only.
- **`SYS.4` is empty and `SYS.5` holds a single test case** for 94 requirements. The test strategy
  is owed by phase 8.
- **`HWE.3` and `HWE.4` carry plans, not results.** The verification plan exists (`HV-01` … `HV-12`);
  no verification has been performed, which is expected for a reference project.
- **ISO 26262-2 has nothing.** `08_safety_case/` is a skeleton; the GSN argument and the confirmation
  measures are owed by phase 9, and phase 0 (roles, independence, tailoring) was skipped — tracked
  as `OP-13`.
- **`SUP.1` has no work product.** Reviews happen through the PR template and CODEOWNERS; a quality
  assurance plan does not exist.

Naming a process area and its topic is deliberate; no clause numbers are cited here, in line with
the project rule on standard citations.
