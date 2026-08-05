# Verification matrix — which means proves which requirement

**Phase 5 · ASPICE SUP.1, SYS.4/SYS.5 (planning) · ISO 26262-4 and -8, verification planning**
**Owner:** safety-analyst, with verification-engineer for the test side · **Status:** draft

> Teaching/reference project. All numeric values are plausible example values, not validated data.

---

## 1 What this matrix is, and what it is not

It says **by which means** each class of requirement is to be proven — analysis, review,
simulation, test or field evidence — and why that means is the appropriate one. It does **not**
assign test cases: `TC-xxx` records are phase 8, owned by `verification-engineer`. A matrix written
before the tests exist is a plan; one written afterwards is a report, and this project does not yet
have the second.

The distinction matters because ISO 26262 expects the *method* to be chosen from the requirement's
nature and ASIL, not from what happened to be convenient once the hardware arrived.

## 2 📋 OVERVIEW — means by requirement class

| Class | Primary means | Supporting means | Why this means |
|---|---|---|---|
| `CR-` customer requirements | Review against the customer specification | Vehicle-level test for the photometric and timing ones | The customer requirement is an agreement; the primary question is whether it was understood, not whether it works |
| `SYS-REQ-` system requirements | Test at system level (HiL) | Analysis for timing budgets, review for interface agreements | They are the first level phrased in terms an integrated system can be measured against |
| `H-` hazards | Review — the HARA itself | — | A hazard is not verified; the *rating* is confirmed (`OP-7`) |
| `SG-` safety goals | Validation at vehicle level | Fault injection at system level | A safety goal is validated, not tested: the question is whether the vehicle is safe, not whether a function returns the right value |
| `FSR-` functional safety req. | Test at system level with fault injection | Analysis for the timing chain | They state a behaviour under fault, so the fault has to be injected |
| `TSR-` technical safety req. | Fault injection at system or HiL level | Analysis (FMEDA, FTA) for the metric claims | The technical safety concept is where analysis and test meet |
| `HW-REQ-` hardware requirements | DV/PV test per `hw_verification_plan.md` (`HV-01` … `HV-14`) | Analysis for the tolerance chain and the thermal design | Component behaviour over the environmental range is not analysable to sufficient confidence |
| `SW-REQ-` software requirements | Unit and integration test with structural coverage per `sw_verification_plan.md` | Static analysis, review of the detailed design | ASIL B asks for statement and branch coverage; the metric choice is argued there |
| `SM-xx` safety mechanisms | Fault injection — the failure the mechanism detects must actually be injected | FMEDA for the coverage claim | A mechanism proven only by analysis has never been seen to fire |
| `A-xx` assumptions | Confirmation with the party the assumption is about | Measurement where the project can measure it | An assumption is closed by agreement or by data, never by argument |

## 3 🔍 DEEP DIVE — the Golden Thread, means by level

The `SG-01` chain end to end, with the means at each level and where it stands today.

| Level | Record | Means | Where it stands |
|---|---|---|---|
| Safety goal | `SG-01` | Vehicle-level validation, plus fault injection at system level | Planned; `TC-021` covers the fault-injection half |
| Functional safety | `FSR-001` | System test with injected open load | `TC-021` |
| Technical safety | `TSR-003` | Fault injection at HiL, timing measured | `TC-021`, timing not yet measured |
| System | `SYS-REQ-014`, `018` | HiL fault injection; `SYS-REQ-016` by analysis plus DV measurement | `TC-021`; the ±20 mA by `analysis_current_sensing.md` and `HV-01` |
| Hardware | `HW-REQ-001` … `009`, `030` | DV/PV per `HV-01` … `HV-14`, over temperature and supply range | Planned only — no hardware exists |
| Safety mechanism | `SM-01` | Fault injection for detection; FMEDA for the 92.2 % coverage | Coverage **confirmed by analysis** (`fmeda_golden_thread.md`); injection owed |
| Software | `SW-REQ-002`, `003`, `013` | Unit test with branch coverage, plus integration test of the reaction chain | Planned only — no code exists |

**Two honest observations.** The whole thread currently rests on **one** test case, `TC-021`, and on
analysis. And the coverage figure that the ASIL B argument depends on is an *analytical* result: the
FMEDA confirms 92.2 %, but no mechanism has been made to fire. That is normal at this stage and
must not be written up as if it were verification evidence.

## 4 Where analysis is the primary means, and why that is legitimate

| Claim | Proven by | Why not by test |
|---|---|---|
| SPFM 91.8 %, LFM 88.8 %, PMHF 1.84 × 10⁻⁸ 1/h | FMEDA | The metrics are properties of a failure-rate distribution; no test enumerates it |
| No order-1 cut set on the SG-01 tree except `MCS-1`/`MCS-2` | FTA with minimal cut sets | Combinatorial — testing every pair is not feasible |
| Freedom from interference between the QM(A) and A(A) partitions | DFA plus the software partitioning argument | Testable only in part; the DFA states what remains argument (`OP-48`) |
| Timing budgets close against the 300 ms FTTI | Analysis, per level | Measurable later, but the budget must hold before the design is built |

**Every one of these becomes weaker if the test never happens.** Analysis says the design should
work; injection says it did. The safety case in phase 9 needs both, and phase 5 supplies only the
first half.

## 5 Coverage today

| | Records | With a `verified_by` link |
|---|---|---|
| All requirement classes | 118 | 3 |

One test case, `TC-021`, verifying four records across four levels. That is not a defect of this
matrix — it is the state of the project before phase 8, and the matrix exists to say what phase 8
has to produce.

## 6 Open points

| ID | Point | Owner |
|---|---|---|
| `OP-19` | Test cases for `HW-REQ-001` … `025`, `SM-02` … `06`, `HV-01` … `HV-14` | verification-engineer |
| `OP-33` | Test cases for `SYS-REQ-022` … `028` | verification-engineer |
| `OP-45` | Test cases for `HW-REQ-026` … `030`; not to be written against `HW-REQ-030` before `OP-42` is decided | verification-engineer |
| `OP-49` | Unit test cases, CI coverage gate, WCET and stack measurement on target | verification-engineer |
| `OP-58` | No fault-injection test exercises the partition boundary from the QM(A) side | software-engineer, verification-engineer |

No new open point is raised here: this matrix collects what the other analyses and phases already
owe, and gives phase 8 a single place to work from.

---

**Work products:** `verification_matrix.md` → `02_safety/05_analyses/`
**Open points:** none new; `OP-19`, `OP-33`, `OP-45`, `OP-49`, `OP-58` collected for phase 8
**Process reference:** ASPICE **SUP.1** (quality assurance), **SYS.4**/**SYS.5** (integration and
qualification test — planning side only) · ISO 26262 **Part 4** (system-level verification and
validation) and **Part 8** (verification planning, and the relation between analysis and test as
means of verification). Parts and topics named, no clause numbers cited.
