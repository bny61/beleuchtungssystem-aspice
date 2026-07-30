# Pull Request — review evidence (ASPICE SUP.4)

This PR is the auditable review record. It is neither deleted nor squashed away when it touches
safety-relevant artefacts.

## Content of the change

<!-- What changed and why -->

**Affected IDs:**
**Reference (issue / CR / problem report):**

## Classification

- [ ] safety-relevant (ASIL B) — CODEOWNERS approval by the safety manager required
- [ ] QM-relevant
- [ ] process/infrastructure change only

## Review checklist

### Requirements
- [ ] EARS-compliant, unambiguous, verifiable, atomic
- [ ] `derived_from` set and correct
- [ ] `allocated_to` set (mandatory for ASIL other than QM)
- [ ] `verified_by` set (mandatory from status `reviewed` onward)
- [ ] ID scheme observed, no ID silently changed

### Consistency
- [ ] Values consistent with already published phases (ASIL, FTTI, thresholds, DC)
- [ ] Model views (`03_model/plantuml/`) updated to match the change
- [ ] Safety analyses (FMEA / FTA / FMEDA / DFA) checked for impact
- [ ] Assumptions recorded as `A-xx` in `09_process/assumptions.md`

### Evidence
- [ ] Traceability check green (`tools/trace_check.py`)
- [ ] Requirement overviews up to date (`tools/gen_index.py --check`)
- [ ] Affected test cases identified or added
- [ ] No invented standard citations, no verbatim normative text
- [ ] Numeric values marked as plausible example values

## Impact analysis (when changing released artefacts)

<!-- Affected baseline (tag), affected downstream artefacts, regression scope -->

## Reviewers

- Technical review: @
- Safety review (where ASIL-relevant, independent of the author): @

> The author must not approve their own work product (ISO 26262-2, confirmation measures).
