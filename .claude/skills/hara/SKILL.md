---
name: hara
description: Method guide for item definition, operational situation analysis, hazard analysis and risk assessment with S/E/C rating and rationale, ASIL determination, safety goal derivation with safe state / FTTI / fault reaction time, and the functional safety concept. Use for ISO 26262 Part 3 work and any ASIL or FTTI question.
---

# HARA & concept phase method

## 1. Item definition

Boundary first: what is **inside** the item, what is an **external interface**, what is
**out of scope** (explicitly listed — an unstated exclusion becomes a finding). Deliver a context
diagram (PlantUML) plus functional description, operating modes and known dependencies on other
items (vehicle supply, gateway, driver assistance).

## 2. Operational situations

Build the situation catalogue as a cross product, then prune to the relevant ones:

`driving situation × operating mode × environment`

e.g. rural road 80 km/h × low beam active × night, rain · construction site 20 km/h ×
work lamps active × night · motorway 85 km/h × high beam active × night, oncoming traffic.

## 3. Hazard analysis

For each function derive malfunctioning behaviours systematically — **loss of function, unintended
activation, incorrect value/intensity, too early / too late, stuck** — and combine with situations.
Minimum 6 hazards.

| ID | Situation | Malfunctioning behaviour | Hazard | S | rationale S | E | rationale E | C | rationale C | ASIL |

**Every rating carries a written rationale.** Scales:
- **S0–S3** severity of harm (S0 no injuries → S3 life-threatening/fatal)
- **E0–E4** exposure/probability of the situation (E1 very low → E4 high)
- **C0–C3** controllability (C0 controllable in general → C3 difficult/uncontrollable)

ASIL follows from the S×E×C combination per the ISO 26262-3 determination table; QM where the
combination yields no ASIL. State the resulting ASIL and, where the combination is near a boundary,
say so and justify the chosen side.

## 4. Safety goals

One safety goal per hazard (merge only hazards with identical goal wording and the same ASIL —
and then use the **highest** ASIL).

| SG-ID | Wording | ASIL | Safe state | FTTI | Fault reaction time |

- **Safe state** must be a reachable, defined system state — for lighting typically *degraded but
  visible* (e.g. low beam via the limp-home path / reduction to the remaining channels plus a
  warning), not simply "off". Justify why the state is safe in the given situation.
- **FTTI** = fault + reaction must complete inside this window. Give the value with rationale
  (marked as plausible example value).
- **Fault Reaction Time** ≤ FTTI − diagnostic test interval − detection time. Show the budget.

## 5. Functional Safety Concept

Per safety goal, derive `FSR-xxx`:

| FSR-ID | Text (EARS) | SG | ASIL | Allocated architecture element | Operating mode | Driver warning? |

Cover: fault detection, fault reaction, transition to safe state, driver warning, degradation
strategy, and the assumptions on driver/other items (as `A-xx`).

## 6. ASIL decomposition (only with independence)

Allowed splits (e.g. B → A(B) + A(B), or B → B(B) + QM(B)). Required deliverables:
1. the two decomposed elements and their allocated requirements,
2. the resulting ASIL notation,
3. the **independence argument**,
4. a **DFA** commissioned to `safety-analyst` covering common supply, common clock, thermal and
   spatial coupling.

Decomposition without a DFA is a blocker finding, not a shortcut.
