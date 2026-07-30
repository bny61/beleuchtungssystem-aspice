---
id: SYS-REQ-014
text: >
  Wenn der Laststrom eines Abblendlicht-Kanals fuer mehr als 50 ms unter 150 mA faellt,
  soll das Lighting-ECU den Kanal als "Open Load" klassifizieren und den Fehlerzaehler inkrementieren.
type: funktional
asil: B
source: CR-007
derived_from: [CR-007, FSR-001]
allocated_to: [ECU_LightingCtrl, SWC_LightManager, SM-01]
verified_by: [TC-021]
status: reviewed
rationale: >
  Schwellwert und Entprellzeit aus dem FTTI-Budget von SG-01 abgeleitet
  (150 mA / 50 ms: plausible Beispielwerte, nicht validiert).
---

## Kontext

Referenz-Datensatz fuer das Requirements-as-Code-Format. Der Schwellwert muss gegen die
Streuung der Stromsensorik (Toleranzkette) abgesichert werden.

## Offene Punkte

1. Toleranzanalyse Stromsensorik offen — Owner: `hardware-engineer`.
