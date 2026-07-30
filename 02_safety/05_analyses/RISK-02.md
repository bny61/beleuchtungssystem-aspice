---
id: RISK-02
text: >
  The ASIL decomposition of FSR-005 into FSR-006 (QM(A)) and FSR-007 (A(A)) is not demonstrated
  until the DFA is available.
type: risk
status: draft
owner: safety-analyst
source: FSC phase 2, ISO 26262-9
mitigation: >
  DFA in phase 5 covering common supply, clock, ground, thermal and spatial coupling, shared
  software resources and common design faults.
impact: >
  Without an independence argument the decomposition falls back: FSR-006 would then be ASIL A
  instead of QM(A), with corresponding requirements on the functional path.
---

## Context

Until demonstrated, the QM path must not be argued as discharged in the safety case.
