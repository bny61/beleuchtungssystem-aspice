# Software verification plan — unit verification

**Phase 7 · ASPICE SWE.4 (software unit verification) · ISO 26262-6 (software unit verification,
structural coverage at unit level)**
**Status:** draft · **Owner:** software-engineer, with `verification-engineer` for the test cases
and the CI gate

> Teaching/reference project. **All numeric values, targets and tool names are plausible example
> values, not validated data.**

---

## 1 Scope

This plan covers **software unit verification (SWE.4)** for the units of the five components in
[`sw_architecture.md`](sw_architecture.md). Software integration test (SWE.5) and software
qualification test (SWE.6) are named at the end and are a hand-off to `verification-engineer`; they
are not planned here, because writing someone else's plan is how two plans end up contradicting each
other.

`TC-` records are **not** created here. The test cases for `SW-REQ-001` … `SW-REQ-014` are `OP-49`.

## 2 Methods per unit

| Method | Applied to | Purpose |
|---|---|---|
| Requirements-based test | every unit implementing a `SW-REQ` | one or more test cases per requirement, traced by ID |
| Interface test | every port of `SWC_LightManager` and `SWC_HighBeamMonitor` | range, invalid value, validity flag combinations |
| Fault injection at the test seam | `SM-01` path, E2E path, state variables | forces the branches that normal stimuli cannot reach (see `MD-01`) |
| Boundary and equivalence class analysis | thresholds: 150 mA, 105 °C, 125 °C, 10 km/h, counter limits | the value at the threshold, one below, one above |
| Resource usage | stack, WCET per runnable | against the WCET budgets of `sw_architecture.md` section 4 |
| Static analysis | all C source | MISRA and complexity gate, see [`coding_standard/misra_c_2012.md`](coding_standard/misra_c_2012.md) |

Units are tested **host-compiled** against stubbed RTE and IoHwAb interfaces, with the same compiler
warning set as the target build; WCET and stack are measured on the target, because a host
measurement of either would be meaningless.

## 3 🔍 DEEP DIVE — structural coverage for ASIL B

### 3.1 The metric and the target

| Metric | Target | Applies to |
|---|---|---|
| **Statement coverage** | **100 %** | all units of ASIL A and above |
| **Branch (decision) coverage** | **100 %** | all units of ASIL B — `SWC_LightManager`, `SWC_WorkLampControl` (A), `SWC_HighBeamMonitor` (A(A)) |
| MC/DC | not required; applied voluntarily to the classification decision of `RE_LM_Monitor` | one function |
| Function / call coverage | 100 % | all units |

ISO 26262-6 lists structural coverage metrics at software unit level — statement coverage, branch
coverage and MC/DC — with a recommendation that rises with the ASIL. For **ASIL B the project takes
statement *and* branch coverage as the required metrics**, both at 100 %, and treats MC/DC as
recommended rather than required. (Part and topic named; no clause number cited.)

### 3.2 Why branch coverage, in writing

The target number is the easy part. The justification is the point:

1. **Statement coverage alone would miss exactly the safety-relevant paths.** In
   `RE_LM_Monitor` the fault paths are `if` branches whose *false* arm is the normal case. A test
   suite that only switches the lamp on and off reaches every statement of the healthy path and can
   still leave the classification arm, the short-to-battery arm and the derating arm untaken.
   Statement coverage would report a comfortable number for a suite that never tested a fault.
2. **The unit is decision-dominated, not computation-dominated.** `SWC_LightManager` contains almost
   no arithmetic; it contains guards — validity flags, counters against limits, cause discrimination,
   state transitions. The structure of the code *is* its decisions, so the coverage metric has to be
   a decision metric or it does not measure the unit at all.
3. **Branch coverage is what makes the state machine testable as a state machine.** Every transition
   `T1` … `T13` of the detailed design is a decision. 100 % branch coverage is, for this component,
   equivalent to having exercised every transition — which is the property a reviewer actually wants
   to hear.
4. **MC/DC is not required at ASIL B, and buying it everywhere would be paid for in the wrong
   currency.** MC/DC forces test cases per condition inside compound decisions; on this code base most
   compound decisions are two-condition validity guards where MC/DC adds cases without adding insight.
   It is applied to the one decision where the conditions genuinely interact — the cause
   discrimination, where current, channel voltage, driver status and the derating set point decide
   between three mutually exclusive causes and getting the cause wrong produces the wrong repair.
   Voluntary, targeted, and stated as voluntary so nobody later reads it as an ASIL B obligation.
5. **Coverage is a completeness check on the tests, never a quality claim about the code.** 100 %
   branch coverage with weak assertions is worthless. That is why the gate in section 3.3 is
   *coverage plus requirements traceability*: every `SW-REQ` needs at least one test case, and
   coverage only tells us the suite touched the whole unit while doing it.

### 3.3 How it is measured and what the gate does

| Item | Setting |
|---|---|
| Instrumentation | Host build compiled with coverage instrumentation (plausible example: `gcc --coverage`, report via `gcov`/`lcov`) |
| Where | GitHub Actions job `sw-unit-tests` on every pull request touching `06_software/` or the source tree |
| Report | HTML and Cobertura XML as build artefacts; summary posted to the pull request |
| **Gate — pass** | statement 100 % **and** branch 100 % over the ASIL A/B units, **and** every `SW-REQ` in the change traced to at least one executed test case |
| **Gate — fail** | the pull request is blocked. Not a warning, not a comment: a required check |
| **Below target** | The only way past the gate is a **justified-unreached record** per uncovered branch: the branch, why it cannot be reached by test, and what compensates (review, fault injection at a higher level, or removal). Approved by `verification-engineer` and, for ASIL B units, `safety-manager`. Recorded in the same place as the MISRA deviations, and counted as a metric |
| **Not allowed** | Lowering the target, excluding a file from measurement, or "temporarily" disabling the check. Excluding a file is a change to the ASIL allocation, not a CI convenience |
| Defensive branches | The defensive `default` arms of deviation `MD-01` are **covered by fault-injection tests**, not written off as unreachable — that is the compensating measure of `MD-01` and it is enforced here |

**What happens when the target is not met** is the question this table exists to answer: the merge
does not happen. The escape hatch is a written, approved, counted justification per branch — never a
threshold turned down. A coverage target that can be edited by whoever is blocked by it measures
nothing.

## 4 📋 OVERVIEW — traceability of the verification

| Requirement group | Units | Verification emphasis |
|---|---|---|
| `SW-REQ-001` … `003`, `013` | `SWC_LightManager` monitoring and arbitration | fault injection, boundary values, timing on target |
| `SW-REQ-004`, `005` | reception and validity handling | E2E fault injection: counter, CRC, data identifier, timeout |
| `SW-REQ-006`, `012` | transmit and DTC path | event plus cycle, DEM interaction |
| `SW-REQ-007` … `009` | high-beam and work-lamp components | plausibility boundaries, invalid-signal case |
| `SW-REQ-010`, `011`, `014` | watchdog service, derating, activation share | window compliance, curve and floor, latency measurement |

## 5 Hand-offs and what is deliberately not planned here

- **Test cases (`TC-xxx`) for `SW-REQ-001` … `SW-REQ-014`** → `verification-engineer` (`OP-49`).
- **The CI gate implementation** (workflow file, required-check configuration) → `verification-engineer`
  with `config-manager`.
- **SWE.5 software integration test and SWE.6 qualification test** → `verification-engineer`. Both
  need the integration of the partitions and the bus, which this plan does not describe.
- **Tool confidence** for the coverage tool and the static analyser → `OP-50`.
- **No back-to-back test against a model**, because no executable model of the software exists; the
  SysML views are specification views, not a simulation.

---

**Work products:** `06_software/sw_verification_plan.md`
**Open points:** `OP-49` (unit test cases and the CI coverage gate), `OP-50` (tool confidence)
**Process reference:** ASPICE **SWE.4** (software unit verification), handing over to **SWE.5** and
**SWE.6** · ISO 26262 **Part 6** (software unit verification, including structural coverage metrics
at unit level and the verification of the software detailed design) · **Part 8** (software tool
confidence). Parts and topics named, no clause numbers cited.
