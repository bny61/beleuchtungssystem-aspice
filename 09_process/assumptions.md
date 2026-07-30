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

> New assumptions are added with consecutive numbers. An assumption is never deleted, only set to
> `confirmed`, `refuted` or `superseded by A-xx`.
