# Tool qualification — note on the CI scripts (ISO 26262-8, Clause 11)

**Status:** Preliminary consideration, not a qualification record. Teaching/reference project.

## Tools considered

| Tool | Purpose in the project | Produces evidence? | Consideration |
|---|---|---|---|
| `tools/trace_check.py` | Checks traceability consistency, produces the traceability matrix and coverage KPIs | **yes** | Qualification candidate — see below |
| `tools/gen_index.py` | Produces the folder overviews of the requirements | indirectly | Derived artefact: the record remains the source. An error would be visible in review since overview and record sit side by side. Lower confidence need than `trace_check.py`. |
| GitHub Actions runner | Executes the checks, archives artefacts | indirectly | Infrastructure; the evidence lies in the archived artefacts |
| PlantUML | Renders model views from text sources | no (presentation) | The source is the text, not the image — a rendering error is detectable in review |
| Compiler / static analysis / coverage tool | Software verification | yes | Separate consideration required in the SW plan (phase 7) |

## Line of argument for `trace_check.py`

**Use case:** the script can *introduce* an error (wrong matrix) or *fail to detect* an existing one
(a missing trace stays unnoticed). The second case is the more relevant one: the script acts as a
verification measure.

**Failure modes:**
1. Front matter is parsed incorrectly → a record is silently ignored.
2. The check logic contains an error → a finding is not reported.
3. A folder lies outside `SEARCH_DIRS` → records are not captured.

**Measures reducing the confidence need:**
- Standard library only — no unqualified third-party dependency.
- The script reports the number of records found; an unexpectedly low value is detectable in review
  (failure modes 1 and 3 thereby become observable).
- Additional mandatory human review (CODEOWNERS, PR checklist) — the CI check does not replace the
  review, it complements it.
- Negative tests: deliberately faulty records must trigger the expected findings.

**Open point:** an actual qualification record (tool classification with TI/TD, the resulting TCL and
the qualification method following from it) has **not** been produced. For a production baseline it
would have to be. This file names the gap; it does not close it.

## Honest limitation

As long as tool qualification is open, a green CI run may be argued in the safety case only as
*supporting* evidence (Sn-07), not as sole evidence of requirements completeness.
