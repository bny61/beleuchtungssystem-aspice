---
id: SW-REQ-010
text: >
  When the external watchdog presents a new question, the watchdog service of the lighting ECU
  software shall compute and return the corresponding answer within 10 ms and in every case inside the
  50 ms question/answer window.
type: safety
asil: B
source: TSR-001
derived_from: [TSR-001]
allocated_to: [ECU_LightingCtrl, MCU_Lockstep, ASIC_Watchdog, SM-02]
verified_by: []
status: draft
rationale: >
  Software side of SM-02. The 50 ms window is published in HW-REQ-018 and TSR-001 and is not changed;
  the 10 ms is the service task period, which keeps a factor of five between the answer and the window
  so that a single missed activation does not trigger a reset. The answer is released only after the
  BSW Watchdog Manager reports that every supervised entity has met its alive and deadline
  supervision, so a hung safety runnable withholds the answer rather than being masked by a healthy
  service task. Plausible example values.
---

## Context

📋 **OVERVIEW.** Note `OP-34`: `SM-02` de-energises all driver stages on `SAFE_OFF`, which applied to
the low beam is exactly hazard `H-01`. That conflict is owned by `safety-manager` and
`systems-engineer` and is **not** resolved in the software; this requirement specifies only the
service of the watchdog protocol.
