# FTA — SG-02 "No unintended glare caused by high beam or work lamps" (ASIL A)

**Phase 5 · ASPICE SUP.9 feeding SYS.3 · ISO 26262-9 (safety analyses, deductive analysis)**
**Status:** draft · **Owner:** safety-analyst

> Teaching/reference project. All statements are plausible example values, not validated data.

---

## 📋 OVERVIEW — depth, on purpose

This is the **second, deliberately shallower thread**. The tree is developed to named basic events
and to minimal cut sets, but it is **not quantified**: `SG-02` carries no FMEDA, so attaching FIT
values here would fabricate a precision that no other document supports. What it *does* deliver in
full is the structural question the decomposition depends on — whether the AND between control path
and monitor path actually holds — and that question is handed to
[`dfa_decomposition.md`](dfa_decomposition.md).

## 1 Top event

> **SG-02 violated — another road user is glared by the high beam or by a work lamp, and the state
> persists beyond the 500 ms FTTI.**

Note what the wording excludes: a segment that is briefly bright while the masking is computed is
not the top event. Persistence beyond the FTTI is.

## 2 The fault tree

```plantuml
@startuml fta_sg02
title Fault tree - top event: SG-02 violated (OVERVIEW, second thread, ASIL A)
skinparam defaultTextAlignment center
skinparam shadowing false
skinparam nodesep 12
skinparam ranksep 26
skinparam rectangle {
  BackgroundColor White
  RoundCorner 6
}

rectangle "**TOP**\nSG-02 violated:\nother road users are glared by high beam or work lamps\nand the state persists beyond the 500 ms FTTI" as TOP #FBEAEA

rectangle "OR" as GT #F0EDF7

rectangle "**G1**\nGlaring high-beam segment\nnot switched off" as G1 #FFF8E1
rectangle "**G2**\nWork lamps energised\nwhile driving" as G2 #FFF8E1

rectangle "AND" as G1G #F0EDF7
rectangle "AND" as G2G #F0EDF7

rectangle "**G1a**\nControl path leaves the\nsegment energised" as G1A #FFF8E1
rectangle "OR" as G1AG #F0EDF7

rectangle "**G1b**\nMonitor path does not\nde-energise the high beam" as G1B #FFF8E1
rectangle "OR" as G1BG #F0EDF7

rectangle "C1\nObject data wrong, late or\nabsent (A-05, no E2E on\nOBJ_List_1)" as C1 #E7F0FB
rectangle "C2\nSWC_HighBeamControl\ncomputes the wrong segment\n(QM(A), TSR-006)" as C2 #E7F0FB
rectangle "C3\nHigh-beam driver stage\nwill not switch off (E4)" as C3 #E7F0FB

rectangle "C4\nSWC_HighBeamMonitor\nfails or is starved\n(A(A), TSR-007)" as C4 #E7F0FB
rectangle "C5\nAmbientLight or VehicleSpeed\nstale but not timed out\n(OP-29)" as C5 #E7F0FB
rectangle "C6\nSeparate enable path to the\nhigh-beam stage inoperative" as C6 #E7F0FB
rectangle "C7\n<<common cause>>\nDependent failure of control\nand monitor (DFA)" as C7 #FBEAEA

rectangle "C8\nWork-lamp stage energised\nwithout request or stuck on" as C8 #E7F0FB
rectangle "C9\nSpeed inhibit defeated:\nsignal invalid or stale\n(TSR-008)" as C9 #E7F0FB

TOP -down- GT
GT -down-> G1
GT -down-> G2

G1 -down- G1G
G1G -down-> G1A
G1G -down-> G1B

G1A -down- G1AG
G1AG -down-> C1
G1AG -down-> C2
G1AG -down-> C3

G1B -down- G1BG
G1BG -down-> C4
G1BG -down-> C5
G1BG -down-> C6

G2 -down- G2G
G2G -down-> C8
G2G -down-> C9

GT -down-> C7

note right of C7
  C7 defeats the AND of G1 in one event and is
  therefore an order-1 cut set unless the DFA
  holds: 02_safety/05_analyses/dfa_decomposition.md.
end note

note bottom of GT
  OVERVIEW depth on purpose: basic events are named
  but not quantified, because SG-02 carries no FMEDA.
end note
@enduml
```

Source: [`../../03_model/plantuml/fta_sg02.puml`](../../03_model/plantuml/fta_sg02.puml).

**How to read it:** the left branch is the ASIL decomposition drawn as a fault tree — the QM(A)
control path (`G1a`) and the A(A) monitor path (`G1b`) meet at an AND gate, and that gate is the
entire reason `TSR-006` may be QM at all. `C7` hangs off the top OR rather than under either path,
because a dependent failure is by definition the event that makes the AND meaningless.

## 3 Minimal cut sets

```
TOP = G1 + G2 + C7
G1  = (C1 + C2 + C3) . (C4 + C5 + C6)
G2  = C8 . C9
```

**11 minimal cut sets:**

| Order | Cut sets | Count |
|---|---|---|
| 1 | `{C7}` | 1 |
| 2 | `{C1,C4}` `{C1,C5}` `{C1,C6}` `{C2,C4}` `{C2,C5}` `{C2,C6}` `{C3,C4}` `{C3,C5}` `{C3,C6}` | 9 |
| 2 | `{C8,C9}` | 1 |

## 4 Single point faults present: **yes — one, and it is not a component**

**`{C7}`, the dependent failure of control path and monitor path.** Every order-2 cut set on the
high-beam branch depends on the two paths failing independently; `C7` is the single event that makes
that assumption false, and it is order 1 by construction.

That is not a defect to be designed out with a mechanism. It is the reason `RISK-02` exists and the
reason `ISO 26262-9` asks for a dependent failure analysis at all. **The `SG-02` fault tree is
therefore only as strong as [`dfa_decomposition.md`](dfa_decomposition.md)**, and the DFA's verdict —
supportable but conditional — transfers directly to this tree.

**A second candidate, stated because the tree as drawn hides it.** `C3` (high-beam stage will not
switch off) is drawn under `G1a`, which presumes the stuck state is *upstream* of the enable gate,
where the monitor's separate enable path can still break it. A stage failed short **downstream** of
the gate cannot be de-energised by either path and would be a genuine order-1 cut set. No safety
mechanism in the current set addresses it; `SM-04`'s overcurrent latch-off happens to help, but a
short that keeps the current in band does not trip it. Raised as part of `OP-57` rather than answered
here — this thread is `📋 OVERVIEW` and a new mechanism is out of this phase's remit.

## 5 Findings

| Finding | Action | Owner |
|---|---|---|
| `{C7}` is order 1; the whole SG-02 argument rests on the DFA | `dfa_decomposition.md`; `RISK-02` answered but conditional | safety-analyst, software-engineer |
| `C5` — a stale-but-not-timed-out `AmbientLight` sits inside a cut set with every control-path event | Confirms `OP-29`; **not closed**, the resolution is a concept decision | safety-manager |
| `C1` — no requirement covers a *missing* `OBJ_List_1` (deliberately un-E2E-protected). `TSR-006`/`TSR-007` cover implausible states, not absence | `OP-57` | systems-engineer, safety-manager |
| High-beam stage failed short downstream of the enable gate | folded into `OP-57` | systems-engineer |

---

**Work products:** `02_safety/05_analyses/fta_sg02.md`, `03_model/plantuml/fta_sg02.puml`
**Open points:** new `OP-57`; `OP-29` confirmed and deliberately **not** closed (it is a concept
decision for `safety-manager`, not an analysis result).
**Process reference:** ASPICE **SUP.9** (problem resolution) feeding **SYS.3** (system architectural
design) · ISO 26262 **Part 9** (safety analyses; analysis of dependent failures) · **Part 3**
(functional safety concept, as the origin of `SG-02`). Parts and topics named, no clause numbers
cited.
