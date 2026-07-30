# Safety Goals und Functional Safety Concept (SG, FSR)

<!-- generiert von tools/gen_index.py -- nicht manuell bearbeiten -->

ISO 26262-3. Safety Goals mit Safe State und FTTI, daraus abgeleitete FSR.

**10 Datensaetze.** Klick auf die ID oeffnet den Datensatz.

| ID | Text | Typ | ASIL | Status | Quelle / Trace | Verifiziert durch |
|---|---|---|---|---|---|---|
| [FSR-001](FSR-001.md) | Wenn ein Abblendlicht-Kanal ausfaellt, soll das Beleuchtungssystem den Ausfall innerhalb der Fault Reaction Time erkennen, in den… | sicherheit | B | reviewed | SG-01 | TC-021 |
| [FSR-002](FSR-002.md) | Das Beleuchtungssystem soll eine nicht vom Fahrer angeforderte Deaktivierung des Abblendlichts verhindern. | sicherheit | B | draft | SG-01 | — |
| [FSR-003](FSR-003.md) | Solange nur ein Abblendlicht-Kanal ausgefallen ist, soll das Beleuchtungssystem den verbleibenden Kanal weiterbetreiben. | sicherheit | B | draft | SG-01 | — |
| [FSR-004](FSR-004.md) | Wenn das Beleuchtungssystem einen Ausfall eines Abblendlicht-Kanals erkannt hat, soll es den Fahrer innerhalb von 2 s optisch war… | sicherheit | B | draft | SG-01, CR-007 | — |
| [FSR-005](FSR-005.md) | Wenn Gegenverkehr oder ein vorausfahrendes Fahrzeug gemeldet wird, soll das Beleuchtungssystem den blendenden Fernlichtanteil inn… | sicherheit | A | draft | SG-02 | — |
| [FSR-006](FSR-006.md) | Das Beleuchtungssystem soll aus den gemeldeten Objektdaten den zu deaktivierenden Fernlichtbereich bestimmen und ansteuern. | sicherheit | QM(A) | draft | FSR-005 | — |
| [FSR-007](FSR-007.md) | Wenn der Fernlichtzustand der gemeldeten Verkehrssituation widerspricht, soll ein vom Ansteuerpfad unabhaengiger Monitor das Fern… | sicherheit | A(A) | draft | FSR-005 | — |
| [FSR-008](FSR-008.md) | Solange die Fahrzeuggeschwindigkeit 10 km/h ueberschreitet, soll das Beleuchtungssystem die Aktivierung der Arbeitsscheinwerfer u… | sicherheit | A | draft | SG-02, CR-004 | — |
| [SG-01](SG-01.md) | Kein unerkannter Ausfall des Abblendlichts waehrend der Fahrt. | safety-goal | B | reviewed | HARA H-01 | TC-021 |
| [SG-02](SG-02.md) | Keine unbeabsichtigte Blendung anderer Verkehrsteilnehmer durch Fernlicht oder Arbeitsscheinwerfer. | safety-goal | A | draft | HARA H-02, H-03, H-05, H-07 | — |

**Status:** draft: 8 · reviewed: 2

**ASIL:** A: 3 · A(A): 1 · B: 5 · QM(A): 1

---

Diese Uebersicht wird von `tools/gen_index.py` erzeugt und in der CI auf Aktualitaet
geprueft. Aenderungen bitte am Datensatz vornehmen, nicht an dieser Datei.
