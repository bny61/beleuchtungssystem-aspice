# Tool qualification — note on the CI scripts (ISO 26262-8, Clause 11)

**Status:** Preliminary consideration, not a qualification record. Teaching/reference project.

## Tools considered

| Tool | Purpose in the project | Produces evidence? | Consideration |
|---|---|---|---|
| `tools/trace_check.py` | Checks traceability consistency, produces the traceability matrix and coverage KPIs | **yes** | Qualification candidate — see below |
| `tools/gen_index.py` | Produces the folder overviews of the requirements | indirectly | Derived artefact: the record remains the source. An error would be visible in review since overview and record sit side by side. Lower confidence need than `trace_check.py`. |
| `tools/gen_req_browser.py` | Produces the requirements browser (`07_verification/reports/requirements_browser.html`) — records, attributes, links and the rendered model views in one page | indirectly | Derived artefact, and the strongest case of "presentation between the reader and the record": it re-renders record text, resolves links and embeds diagrams. Two consequences are deliberate — it takes its KPIs from `trace_check.kpis()` verbatim rather than recomputing them, so the page cannot report a different coverage than the gate; and every record view names the record file as the source of truth. A reviewer reads it to navigate, and cites the record. |
| `tools/gen_trace_graph.py` | Produces the Mermaid traceability views and the HTML explorer | indirectly | Derived artefacts: the records remain the source, and every view carries a link table that a reviewer can check against the record. The **HTML explorer additionally places JavaScript between the record and its presentation** - a rendering fault there is not visible in the file itself. For that reason the Mermaid views, not the explorer, are the artefact to cite in a review; the explorer is a convenience. |
| GitHub Actions runner | Executes the checks, archives artefacts | indirectly | Infrastructure; the evidence lies in the archived artefacts |
| PlantUML | Renders model views from text sources, and gates their syntax in CI | no (presentation) | The source is the text, not the image — a rendering error is detectable in review. **Version pinned** (see below), because the check is only meaningful if it is reproducible |
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

## Note on the PlantUML version

PlantUML needs no qualification argument — it produces presentation, and the text source stays the
authoritative artefact. Its **version**, however, is a configuration item, because the CI syntax
check is a gate: an unpinned tool means the gate answers a different question on every run.

That was not theoretical. The job installed whatever `apt-get install plantuml` shipped on the
runner, which lagged the current release by years. `ibd_ecu.puml` used `portin` / `portout`, the
runner's version did not know them, and the gate went red on a diagram that was correct and rendered
locally without complaint. The failure survived several commits because the red run looked like the
traceability check failing, which it never was.

The version is therefore pinned in `.github/workflows/traceability.yml` to a release asset with a
recorded SHA-256, and Graphviz availability is asserted with `-testdot` before any diagram is
checked. Raising the version is a reviewable change with an impact on every model view, not a
silent drift.

**Residual point:** the locally installed PlantUML is not pinned by anything, so a diagram authored
with a newer local version can still fail the gate. The gate is the authority; local rendering is
convenience. Worth revisiting if the model views ever become cited evidence rather than illustration.

## Honest limitation

As long as tool qualification is open, a green CI run may be argued in the safety case only as
*supporting* evidence (Sn-07), not as sole evidence of requirements completeness.

The same applies, more strongly, to the visual views: a diagram that omits links for readability -
as the large safety goal views deliberately do - must never be cited as evidence of completeness.
Completeness is argued from `traceability_matrix.md` and from `trace_check.py`, not from a picture.
