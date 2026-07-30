# Annahmenliste (`A-xx`)

Jede Annahme, die nicht durch eine Anforderung oder ein Stakeholder-Dokument belegt ist, wird hier
gefuehrt. Sicherheitsrelevante Annahmen sind Validierungsziele (ISO 26262-4, Validierung).

| ID | Annahme | Begruendung / Quelle | Sicherheitsrelevant | Validierungsziel | Status |
|---|---|---|---|---|---|
| A-01 | Das Bordnetz stellt 24 V nominal mit Toleranzen nach ISO 16750-2 bereit. | Standard-Bordnetz N3-Fahrzeug | ja | Nachweis im HW-Verifikationsplan | offen |
| A-02 | Das Fahrzeug-Gateway leitet Diagnoseanfragen (UDS) unveraendert an das Lighting-ECU weiter. | Systemarchitektur Fahrzeugebene, ausserhalb Item-Grenze | nein | — | offen |
| A-03 | Der Fahrer reagiert auf eine optische Warnung im Kombiinstrument innerhalb der angenommenen Reaktionszeit. | Controllability-Einstufung in der HARA | ja | Validierung auf Fahrzeugebene | offen |
| A-04 | Die Anzeigeart der Fahrerwarnung wird vom OEM-HMI-Konzept vorgegeben. | offene Abstimmung zu CR-007 | nein | Klaerung mit OEM | offen |
| A-05 | Die Objekterkennung fuer das blendfreie Fernlicht wird vom Fahrzeug ueber CAN FD bereitgestellt und liegt ausserhalb der Item-Grenze. | Systemabgrenzung zu CR-003 | ja | Schnittstellenabsicherung in Phase 3, Validierung Fahrzeugebene | offen |
| A-06 | Lichtschalterstellung und Zuendungsstatus werden vom Fahrzeug als Bussignale bereitgestellt; keine direkte Verdrahtung zum Lighting-ECU. | Systemabgrenzung zu CR-001, CR-006 | ja | Schnittstellentabelle Phase 3 | offen |
| A-07 | Das Nutzungsprofil entspricht N3-Fernverkehr mit ueberwiegendem Nachtanteil im Winterhalbjahr. | Grundlage fuer Exposure-Einstufung der HARA und fuer CR-022 | ja | Bestaetigung durch OEM-Nutzungsdaten | offen |

> Neue Annahmen werden mit fortlaufender Nummer ergaenzt. Eine Annahme wird nie geloescht, sondern
> auf `bestaetigt`, `widerlegt` oder `ersetzt durch A-xx` gesetzt.
