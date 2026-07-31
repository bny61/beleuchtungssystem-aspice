# Traceability matrix (generated)

> Generated automatically by `tools/trace_check.py` - do not edit manually.

| ID | Type | ASIL | Status | derived_from | allocated_to | verified_by | File |
|---|---|---|---|---|---|---|---|
| CR-001 | functional | tbd | draft | - | - | - | `01_requirements/customer/CR-001.md` |
| CR-002 | functional | tbd | draft | - | - | - | `01_requirements/customer/CR-002.md` |
| CR-003 | functional | tbd | draft | - | - | - | `01_requirements/customer/CR-003.md` |
| CR-004 | functional | tbd | draft | - | - | - | `01_requirements/customer/CR-004.md` |
| CR-005 | functional | tbd | draft | - | - | - | `01_requirements/customer/CR-005.md` |
| CR-006 | functional | tbd | draft | - | - | - | `01_requirements/customer/CR-006.md` |
| CR-007 | functional | B | reviewed | - | ECU_LightingCtrl | TC-021 | `01_requirements/customer/CR-007.md` |
| CR-008 | functional | tbd | draft | - | - | - | `01_requirements/customer/CR-008.md` |
| CR-009 | legal | QM | draft | - | - | - | `01_requirements/customer/CR-009.md` |
| CR-010 | legal | QM | draft | - | - | - | `01_requirements/customer/CR-010.md` |
| CR-011 | legal | QM | draft | - | - | - | `01_requirements/customer/CR-011.md` |
| CR-012 | legal | QM | draft | - | - | - | `01_requirements/customer/CR-012.md` |
| CR-013 | environmental-mechanical | QM | draft | - | - | - | `01_requirements/customer/CR-013.md` |
| CR-014 | environmental-mechanical | QM | draft | - | - | - | `01_requirements/customer/CR-014.md` |
| CR-015 | environmental-mechanical | QM | draft | - | - | - | `01_requirements/customer/CR-015.md` |
| CR-016 | electrical | tbd | draft | - | - | - | `01_requirements/customer/CR-016.md` |
| CR-017 | electrical | tbd | draft | - | - | - | `01_requirements/customer/CR-017.md` |
| CR-018 | electrical | QM | draft | - | - | - | `01_requirements/customer/CR-018.md` |
| CR-019 | diagnostics | tbd | draft | - | - | - | `01_requirements/customer/CR-019.md` |
| CR-020 | communication | tbd | draft | - | - | - | `01_requirements/customer/CR-020.md` |
| CR-021 | communication | QM | draft | - | - | - | `01_requirements/customer/CR-021.md` |
| CR-022 | durability | tbd | draft | - | - | - | `01_requirements/customer/CR-022.md` |
| CR-023 | interface | QM | draft | - | - | - | `01_requirements/customer/CR-023.md` |
| FSR-001 | safety | B | reviewed | SG-01 | ECU_LightingCtrl, SM-01 | TC-021 | `02_safety/03_fsc/FSR-001.md` |
| FSR-002 | safety | B | draft | SG-01 | ECU_LightingCtrl, SWC_LightManager | - | `02_safety/03_fsc/FSR-002.md` |
| FSR-003 | safety | B | draft | SG-01 | ECU_LightingCtrl, LED_Driver_Stage_1 | - | `02_safety/03_fsc/FSR-003.md` |
| FSR-004 | safety | B | draft | SG-01, CR-007 | ECU_LightingCtrl, Vehicle_Gateway | - | `02_safety/03_fsc/FSR-004.md` |
| FSR-005 | safety | A | draft | SG-02 | ECU_LightingCtrl | - | `02_safety/03_fsc/FSR-005.md` |
| FSR-006 | safety | QM(A) | draft | FSR-005 | SWC_HighBeamControl | - | `02_safety/03_fsc/FSR-006.md` |
| FSR-007 | safety | A(A) | draft | FSR-005 | ECU_LightingCtrl, SWC_HighBeamMonitor | - | `02_safety/03_fsc/FSR-007.md` |
| FSR-008 | safety | A | draft | SG-02, CR-004 | ECU_LightingCtrl, SWC_WorkLampControl | - | `02_safety/03_fsc/FSR-008.md` |
| H-01 | hazard | B | draft | - | - | - | `02_safety/02_hara/H-01.md` |
| H-02 | hazard | A | draft | - | - | - | `02_safety/02_hara/H-02.md` |
| H-03 | hazard | A | draft | - | - | - | `02_safety/02_hara/H-03.md` |
| H-04 | hazard | B | draft | - | - | - | `02_safety/02_hara/H-04.md` |
| H-05 | hazard | A | draft | - | - | - | `02_safety/02_hara/H-05.md` |
| H-06 | hazard | QM | draft | - | - | - | `02_safety/02_hara/H-06.md` |
| H-07 | hazard | A | draft | - | - | - | `02_safety/02_hara/H-07.md` |
| HW-REQ-001 | electrical | B | draft | SYS-REQ-016, FSR-001 | LED_Driver_Stage_1, Current_Sense_Chain, SM-01 | - | `05_hardware/HW-REQ-001.md` |
| HW-REQ-002 | electrical | B | draft | SYS-REQ-016, HW-REQ-001 | LED_Driver_Stage_1, Current_Sense_Chain, SM-01 | - | `05_hardware/HW-REQ-002.md` |
| HW-REQ-003 | electrical | B | draft | SYS-REQ-014 | ECU_LightingCtrl, LED_Driver_Stage_1, SM-01 | - | `05_hardware/HW-REQ-003.md` |
| HW-REQ-004 | electrical | B | draft | SYS-REQ-017 | LED_Driver_Stage_1, SM-01 | - | `05_hardware/HW-REQ-004.md` |
| HW-REQ-005 | diagnostics | B | draft | FSR-001, SYS-REQ-014 | ECU_LightingCtrl, Current_Sense_Chain, SM-01 | - | `05_hardware/HW-REQ-005.md` |
| HW-REQ-006 | electrical | B | draft | SYS-REQ-019 | LED_Driver_Stage_1, SM-01 | - | `05_hardware/HW-REQ-006.md` |
| HW-REQ-007 | interface | B | draft | SYS-REQ-019 | LED_Driver_Stage_1, ECU_LightingCtrl, SM-01 | - | `05_hardware/HW-REQ-007.md` |
| HW-REQ-008 | electrical | B | draft | SYS-REQ-014, HW-REQ-002 | LED_Driver_Stage_1, SM-01 | - | `05_hardware/HW-REQ-008.md` |
| HW-REQ-009 | safety | B | draft | SYS-REQ-018, FSR-001 | ECU_LightingCtrl, SM-01 | - | `05_hardware/HW-REQ-009.md` |
| HW-REQ-010 | diagnostics | B | draft | FSR-001, HW-REQ-001 | ECU_LightingCtrl, SM-01 | - | `05_hardware/HW-REQ-010.md` |
| RISK-01 | risk | - | draft | - | - | - | `02_safety/05_analyses/RISK-01.md` |
| RISK-02 | risk | - | draft | - | - | - | `02_safety/05_analyses/RISK-02.md` |
| SG-01 | safety-goal | B | reviewed | H-01, H-04 | Item_LightingSystem | TC-021 | `02_safety/03_fsc/SG-01.md` |
| SG-02 | safety-goal | A | draft | H-02, H-03, H-05, H-07 | Item_LightingSystem | - | `02_safety/03_fsc/SG-02.md` |
| SM-01 | safety-mechanism | B | draft | FSR-001 | ECU_LightingCtrl, LED_Driver_Stage_1, Current_Sense_Chain | TC-021 | `05_hardware/SM-01.md` |
| SYS-REQ-014 | functional | B | draft | CR-007, FSR-001 | ECU_LightingCtrl, SWC_LightManager, SM-01 | TC-021 | `01_requirements/system/SYS-REQ-014.md` |
| SYS-REQ-015 | diagnostics | B | draft | SYS-REQ-014 | ECU_LightingCtrl, SWC_LightManager | - | `01_requirements/system/SYS-REQ-015.md` |
| SYS-REQ-016 | electrical | B | draft | SYS-REQ-014, FSR-001 | ECU_LightingCtrl, LED_Driver_Stage_1 | - | `01_requirements/system/SYS-REQ-016.md` |
| SYS-REQ-017 | diagnostics | B | draft | SYS-REQ-014 | ECU_LightingCtrl, SWC_LightManager | - | `01_requirements/system/SYS-REQ-017.md` |
| SYS-REQ-018 | safety | B | draft | SYS-REQ-014, FSR-001 | ECU_LightingCtrl, SM-01 | - | `01_requirements/system/SYS-REQ-018.md` |
| SYS-REQ-019 | diagnostics | B | draft | SYS-REQ-014 | ECU_LightingCtrl, SWC_LightManager | - | `01_requirements/system/SYS-REQ-019.md` |
| TC-021 | fault-injection | B | draft | SYS-REQ-014, SYS-REQ-018, FSR-001, SG-01 | HiL | - | `07_verification/testcases/TC-021.md` |
