# Pull Request — Review-Nachweis (ASPICE SUP.4)

Dieser PR ist der auditierbare Review-Nachweis. Er wird nicht geloescht und nicht squash-verdichtet,
wenn er sicherheitsrelevante Artefakte betrifft.

## Inhalt der Aenderung

<!-- Was wurde geaendert und warum -->

**Betroffene IDs:**
**Bezug (Issue / CR / Problem Report):**

## Klassifikation

- [ ] sicherheitsrelevant (ASIL B) — CODEOWNERS-Freigabe durch Safety Manager erforderlich
- [ ] QM-relevant
- [ ] nur Prozess-/Infrastrukturaenderung

## Review-Checkliste

### Anforderungen
- [ ] EARS-konform formuliert, eindeutig, testbar, atomar
- [ ] `derived_from` gesetzt und korrekt
- [ ] `allocated_to` gesetzt (Pflicht bei ASIL != QM)
- [ ] `verified_by` gesetzt (Pflicht ab Status `reviewed`)
- [ ] ID-Schema eingehalten, keine ID stillschweigend geaendert

### Konsistenz
- [ ] Werte konsistent zu bereits veroeffentlichten Phasen (ASIL, FTTI, Schwellwerte, DC)
- [ ] Modellsichten (`03_model/plantuml/`) zur Aenderung nachgezogen
- [ ] Sicherheitsanalysen (FMEA / FTA / FMEDA / DFA) auf Auswirkung geprueft
- [ ] Annahmen als `A-xx` in `09_process/assumptions.md` erfasst

### Nachweis
- [ ] Traceability-Check gruen (`tools/trace_check.py`)
- [ ] Betroffene Testfaelle identifiziert bzw. ergaenzt
- [ ] Keine erfundenen Normzitate, keine woertlichen Normtexte
- [ ] Zahlenwerte als plausible Beispielwerte gekennzeichnet

## Impact-Analyse (bei Aenderung freigegebener Artefakte)

<!-- Betroffene Baseline (Tag), betroffene Downstream-Artefakte, Regressionsumfang -->

## Reviewer

- Fachreview: @
- Sicherheitsreview (bei ASIL-Relevanz, unabhaengig vom Autor): @

> Der Autor darf sein eigenes Work Product nicht freigeben (ISO 26262-2, Confirmation Measures).
