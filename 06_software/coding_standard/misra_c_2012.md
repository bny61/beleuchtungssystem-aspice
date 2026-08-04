# Coding standard — MISRA C:2012

**Phase 7 · ASPICE SWE.3 (software detailed design and unit construction), SUP.1 (quality
assurance) · ISO 26262-6 (design principles for software unit implementation, use of coding
guidelines)**
**Status:** draft · **Owner:** software-engineer

> Teaching/reference project. Tool names, thresholds and deviation examples are **plausible
> examples**, not a qualified tool chain.

---

## 1 The standard and how this project tailors it

The coding standard for all C source of the lighting ECU is **MISRA C:2012**, including its
published amendments. The project tailoring is deliberately strict and consists of one sentence:

> **Mandatory, required *and* advisory guidelines are all binding. Any violation, of any category,
> needs an approved deviation record.**

Advisory guidelines are normally left to the project's judgement. Treating them as binding-unless-
deviated is the cheaper option here, because it converts every "we thought about it" into a written
record instead of a habit. The cost is two deviation records instead of none, which is exactly what
section 3 shows.

**Rule text is paraphrased, never quoted**, in line with the project rule on standard citations.
Rule identifiers are given where they are certain; the identity and category of every rule named in
a deviation record is re-confirmed against the published MISRA document at the review that approves
the deviation.

## 2 Static analysis setup

| Item | Setting |
|---|---|
| Analyser | MISRA-checking static analyser with an ISO 26262 tool-confidence classification (plausible example: a commercial checker used by the OEM tool chain) |
| Rule set | Full MISRA C:2012 set, all categories enabled; project-specific suppressions only through the deviation mechanism of section 4 |
| Configuration in the repo | `06_software/coding_standard/ruleset/` — the analyser configuration is version-controlled like source, so a rule silently turned off is a reviewable diff |
| Additional checks | Compiler at the highest warning level, warnings as errors; cyclomatic complexity ≤ 10 per function; no recursion (call-graph check); stack usage report |
| Where it runs | GitHub Actions job on every pull request (no Jenkins, per the project tool chain); results uploaded as SARIF and shown inline in the PR |
| Gate | **Any new violation without an approved deviation fails the pull request.** The baseline of existing findings is zero; there is no "legacy" allowance because there is no legacy code |
| Evidence | Analyser report per pull request, retained as a build artefact and referenced from the safety case (phase 9) |

The analyser is a **tool-qualification candidate**, like `tools/trace_check.py`: it produces
evidence that a safety argument leans on. Tool confidence for it and for the coverage tool of
[`../sw_verification_plan.md`](../sw_verification_plan.md) is raised as `OP-50` and belongs in
`09_process/plans/tool_qualification.md`.

## 3 🔍 DEEP DIVE — the two deviations

`MD-xx` identifiers are **document-local line items, not records of the project ID scheme** — the
same convention as the `HV-xx` entries in the hardware verification plan.

### MD-01 — defensive default branches that the analyser proves unreachable

| Field | Content |
|---|---|
| Rule | MISRA C:2012 **Rule 2.2** — dead code (required). Paraphrased: code whose removal cannot change program behaviour must not be present. |
| Scope | The `default` arm of every `switch` over an enumerated state or cause, and the final `else` of every `if`/`else if` chain over a closed set of conditions, in `SWC_LightManager` and `SWC_HighBeamMonitor`. |
| Why it is needed | ISO 26262-6 asks for defensive implementation of software units. The state machine of `SWC_LightManager` has seven states in a `uint8_t`; a bit flip in RAM produces a value no path assigns. The `default` arm that catches it is, by construction, unreachable in fault-free execution — which is precisely what the analyser reports as dead code. Removing it would remove the detection of a corrupted state variable in an ASIL B component. |
| **Rationale** | The two requirements genuinely conflict: the coding guideline forbids code with no effect on fault-free behaviour, the safety standard asks for exactly that code. The deviation resolves it in favour of the safety standard, for the narrow case of a state or cause variable, and nowhere else. |
| **Compensating measure** | (a) The defensive arm must not be silent: it calls `LM_HandleImplausibleState()`, which sets a DEM event and forces the safe state, so the branch has an observable effect and is testable. (b) Each such branch is exercised by a fault-injection unit test that writes an out-of-range value into the state variable through the test seam — so the branch is covered by test even though it is unreachable in normal operation, and it is **not** counted as justified-unreached coverage. (c) The deviation is limited to `switch`/`else` over enumerated state and cause variables; it may not be used for range checks on data, which have to be reachable by design. |
| Review | Approved by software-engineer and safety-manager; re-reviewed whenever the state machine changes. |

**Why this is not a free pass:** the deviation buys back the very thing the rule protects — code that
does nothing. The compensating measure makes the branch do something and makes it testable. If a
defensive arm cannot be given an observable effect and a fault-injection test, it is dead code and
the rule wins.

### MD-02 — conversion between an integer address and a pointer in the register access layer

| Field | Content |
|---|---|
| Rule | MISRA C:2012 **Rule 11.4** — conversion between a pointer to object and an integer type (advisory; binding here through the tailoring of section 1). |
| Scope | Exactly one translation unit: the register access header of the MCAL wrapper (`Mcal_Reg.h`) that maps peripheral addresses onto `volatile` typed pointers for the ADC, PWM, DIO and SPI drivers. No application component, no SWC. |
| Why it is needed | Memory-mapped peripheral registers exist at fixed addresses. Reaching them in C requires converting an integer address into a pointer somewhere; the only choice is *where*, not *whether*. Concentrating the conversion in one header is the smallest possible scope. |
| **Rationale** | Not avoidable on this architecture, and moving the conversion into the drivers would multiply the deviation across five modules instead of one, which is worse both for review and for analysis. |
| **Compensating measure** | (a) All conversions live in one header; the analyser suppression is scoped to that file and would flag any conversion elsewhere. (b) Addresses come from the silicon vendor's device header, never as literals in project code. (c) A compile-time assertion checks the size and alignment of every register type. (d) The header is reviewed by two engineers, one of whom did not write it, and every change to it is a CODEOWNERS-protected review. (e) Register access is verified against a register model in unit test and re-verified on target in the hardware integration test, so a wrong address fails a test rather than a field vehicle. |
| Review | Approved by software-engineer; confirmed at the software integration review. |

**Why this is not a free pass:** the deviation is bounded by file, by address source and by test.
An engineer who wants a pointer/integer conversion in application code does not inherit this
deviation — they need a new one, and they will not get it.

## 4 How deviations are recorded and reviewed

| Step | Rule |
|---|---|
| Form | One Markdown record per deviation under `06_software/coding_standard/deviations/`, with the fields of section 3: rule, scope, need, rationale, compensating measure, approver, review trigger |
| Granularity | Per rule **and** per scope. A deviation is never "for the project"; it names files or a construct class |
| Approval | Software-engineer plus, for any rule touching an ASIL B unit, safety-manager. Approval is a PR review by CODEOWNERS, which is how this project makes approval technically enforced (SUP.4) |
| In-code marking | The suppression comment carries the `MD-xx` identifier, so the analyser report, the code and the deviation record can be joined mechanically |
| Expiry | A deviation is re-reviewed when the affected design changes, and at every safety-case baseline. There is no permanent deviation |
| Visibility | The count of open deviations is a metric reported with the phase status; a growing count is a design smell, not a process detail |

## 5 Deliberately not covered

- **No naming or formatting conventions.** Those belong in a style guide; they are not safety
  relevant and mixing them into a MISRA document dilutes both.
- **No third deviation.** The project brief asks for two examples; inventing more would suggest a
  code base that does not exist.
- **No qualified tool chain.** Compiler qualification and analyser tool confidence are named as open
  (`OP-50`), not claimed.

---

**Work products:** `06_software/coding_standard/misra_c_2012.md`
**Open points:** `OP-50` (tool confidence for the static analyser and the coverage tool)
**Process reference:** ASPICE **SWE.3** (software detailed design and unit construction) and
**SUP.1** (quality assurance) · ISO 26262 **Part 6** (design principles for software unit
implementation, including the use of coding guidelines and language subsets) · **Part 8** (software
tool confidence). Parts and topics named, no clause numbers cited.
