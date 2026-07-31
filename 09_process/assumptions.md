# Assumptions (`A-xx`)

Every assumption not backed by a requirement or a stakeholder document is tracked here.
Safety-relevant assumptions are validation targets (ISO 26262-4, validation).

| ID | Assumption | Rationale / source | Safety-relevant | Validation target | Status |
|---|---|---|---|---|---|
| A-01 | The vehicle supply provides 24 V nominal with tolerances per ISO 16750-2. | Standard supply of an N3 vehicle | yes | Evidence in the HW verification plan | open |
| A-02 | The vehicle gateway forwards diagnostic requests (UDS) to the lighting ECU unchanged. | Vehicle-level system architecture, outside the item boundary | no | — | open |
| A-03 | The driver responds to a visual warning in the instrument cluster within the assumed reaction time. | Controllability rating in the HARA | yes | Validation at vehicle level | open |
| A-04 | The type of driver warning is specified by the OEM HMI concept. | Open alignment relating to CR-007 | no | Clarification with the OEM | open |
| A-05 | Object detection for the glare-free high beam is provided by the vehicle via CAN FD and lies outside the item boundary. | System delimitation relating to CR-003 | yes | Interface safeguarding in phase 3, validation at vehicle level | open |
| A-06 | Light switch position and ignition status are provided by the vehicle as bus signals; no direct wiring to the lighting ECU. | System delimitation relating to CR-001, CR-006 | yes | Interface table phase 3 | open |
| A-07 | The usage profile corresponds to N3 long-haul operation with a predominant night share in the winter half-year. | Basis for the exposure rating of the HARA and for CR-022 | yes | Confirmation through OEM usage data | open |
| A-08 | A low-beam channel is driven by a constant-current buck LED driver at a nominal set point of 1.20 A, in two parallel strings of 600 mA. | Basis of the tolerance chain and of the parallel-string blindness (HW-REQ-001) | yes | HW design review, DV measurement | open |
| A-09 | Low-beam PWM dimming runs at 400 Hz with a duty of at least 20 % in normal operation. | Basis of the sampling raster and of the detection-time arithmetic (HW-REQ-003) | yes | HW verification plan, DV | open |
| A-10 | The LED driver provides OVP/OCP/thermal status as a signal readable by the microcontroller. | Precondition for HW-REQ-007 and for the diagnostic coverage of SM-01 | yes | Component selection, datasheet review | open |
| A-11 | The sensing chain is qualified over -40 C to +85 C ambient; the sense amplifier junction temperature does not exceed +105 C. | Basis of the drift terms in the tolerance chain (HW-REQ-001) | yes | ISO 16750-4 environmental test | open |
| A-12 | The thermal derating curve of a low-beam channel never commands below 400 mA. | Precondition for the fixed-threshold approach (HW-REQ-008) | yes | Derating curve review, DV over temperature | open |
| A-13 | The luminous flux of a low-beam channel follows Phi = Phi_ref * (I / I_ref) * (1 - k * (T_j - T_ref)) with Phi_ref = 1200 lm at I_ref = 1.20 A, T_ref = 25 C and k = 0.004 1/K. | Basis of the parametric diagram and of the assessment of the limp-home state against the legal minimum luminous flux | yes | Photometric measurement, LED supplier data | open |

> New assumptions are added with consecutive numbers. An assumption is never deleted, only set to
> `confirmed`, `refuted` or `superseded by A-xx`.
