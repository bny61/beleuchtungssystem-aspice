# Item Definition

**Item:** Adaptive front-lighting system incl. work-lamp control
**Vehicle:** Heavy truck, class N3, 18 t tractor unit
**Standard:** ISO 26262-3 (Item Definition)
**Status:** Phase 2, draft
**Owner:** safety-manager

> Teaching/reference project, not a production baseline. Numeric values are plausible example values.

---

## 1 Purpose and functions

The item provides the forward lighting and the work-lamp control:

| Function | Short description |
|---|---|
| Low beam | Basic illumination of the carriageway, implemented across several channels |
| High beam | Long-range illumination, segment-wise maskable for glare-free operation |
| Daytime running lights | Conspicuity in daylight |
| Cornering light | Swivelling as a function of steering angle and speed |
| Headlamp levelling | Load-dependent inclination correction |
| Work lamps | Illumination at standstill and while manoeuvring |
| Diagnostics | Fault detection, DTC management, UDS access |

## 2 Item boundary

### Inside the item boundary

| Element | Role |
|---|---|
| `ECU_LightingCtrl` | Lighting ECU, control and monitoring of all lighting functions |
| `LED_Driver_Stage_1..n` | LED driver stages of the individual channels |
| Current and temperature sensing | Feedback for diagnostics and derating |
| Headlamp modules | Low beam, high beam and cornering light |
| Work-lamp output stages | Control of the work lamps |

### Outside the item boundary (interfaces)

| Element | Relationship | Assumption |
|---|---|---|
| Vehicle supply 24 V | Supply KL30 / KL15, 16–32 V | `A-01` |
| Vehicle gateway (CAN FD / J1939) | Light request, speed, steering angle, status feedback | `A-02` |
| Environment sensing (object detection) | Object list for the glare-free high beam | `A-05` |
| Light switch, ignition | As bus signals, no direct wiring | `A-06` |
| Instrument cluster | Display of the driver warning | `A-04` |
| Diagnostic tester (workshop) | UDS per ISO 14229 | — |

### Explicitly out of scope

Rear lighting · interior lighting · indicators and hazard warning lights · fog lamps ·
body-builder lighting behind the body interface.

> The exclusions are listed explicitly on purpose. A tacit delimitation is a finding in an
> assessment, not a simplification.

## 3 Context diagram

Source: [`../../03_model/plantuml/ctx_item.puml`](../../03_model/plantuml/ctx_item.puml)

The yellow block is the item boundary — only what lies inside it is developed in this project.
Grey blocks are external systems. Every edge crossing the boundary is an interface to be specified
in phase 3 with signal, direction, type, value range, timing and ASIL.

> The diagram has **not** been syntax-checked so far (PlantUML not installed locally, `OP-12`).
> In CI this is done by the `Modell-Syntaxpruefung` job.

## 4 Operating modes

| Mode | Description |
|---|---|
| Init | Self-test after ignition on |
| Normal operation | All lighting functions available |
| Degraded | Partial failure detected, remaining channels active |
| Safe state (limp-home) | Reduced power, driver warning active, DTC stored |
| Sleep | Ignition off, quiescent-current operation after the run-on time |

## 5 Dependencies on other items

| Dependency | Safety impact |
|---|---|
| Object detection (vehicle level) | Part of the effect chain of `SG-02`; requires an interface agreement (DIA) — `OP-10` |
| Vehicle supply | Supply quality affects all lighting functions; a common cause of failure, to be considered in the DFA |
| Instrument cluster | Carries the driver warning from `FSR-004` and thereby the C rating of H-01 |

## 6 Further reading

- Hazard analysis: [`../02_hara/hara.md`](../02_hara/hara.md)
- Safety goals and FSC: [`../03_fsc/`](../03_fsc/)
- Assumptions: [`../../09_process/assumptions.md`](../../09_process/assumptions.md)

**Process reference:** ISO 26262 **Part 3** (Item Definition) · ASPICE **SYS.1** (system context).
