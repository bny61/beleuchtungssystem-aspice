# Traceability-Matrix (generiert)

> Automatisch erzeugt von `tools/trace_check.py` - nicht manuell bearbeiten.

| ID | Typ | ASIL | Status | derived_from | allocated_to | verified_by | Datei |
|---|---|---|---|---|---|---|---|
| CR-007 | funktional | B | reviewed | - | ECU_LightingCtrl | TC-021 | `01_requirements/customer/CR-007.md` |
| FSR-001 | sicherheit | B | reviewed | SG-01 | ECU_LightingCtrl, SM-01 | TC-021 | `02_safety/03_fsc/FSR-001.md` |
| SG-01 | safety-goal | B | reviewed | - | Item_Beleuchtungssystem | TC-021 | `02_safety/03_fsc/SG-01.md` |
| SM-01 | sicherheitsmechanismus | B | reviewed | FSR-001 | ECU_LightingCtrl, LED_Driver_Stage_1 | TC-021 | `05_hardware/SM-01.md` |
| SYS-REQ-014 | funktional | B | reviewed | CR-007, FSR-001 | ECU_LightingCtrl, SWC_LightManager, SM-01 | TC-021 | `01_requirements/system/SYS-REQ-014.md` |
| TC-021 | fehlerinjektion | B | reviewed | SYS-REQ-014, FSR-001, SG-01 | HiL | - | `07_verification/testcases/TC-021.md` |
