# S/E/C-Klassifikation — im Projekt angewendete Auslegung

Ergaenzung zu [`hara.md`](hara.md). Dokumentiert, **wie** die Klassen in diesem Projekt ausgelegt
wurden, damit die Einstufungen im Confirmation Review nachvollziehbar sind.

> **Kein Normauszug.** Die Klassen S0–S3, E0–E4 und C0–C3 sowie die Einstufungstabelle sind in
> ISO 26262-3 definiert. Hier steht ausschliesslich die projektspezifische Auslegung in eigenen
> Worten — kein Normtext, keine reproduzierte Einstufungstabelle.

## 1 Severity — Schwere der Schaedigung

| Klasse | Auslegung im Projekt | Beispiel aus dieser HARA |
|---|---|---|
| S0 | keine Verletzungen zu erwarten | Sachschaden an der Leuchteneinheit ohne Fahrsituation |
| S1 | leichte, in der Regel folgenlos ausheilende Verletzungen | H-06: verminderte Erkennbarkeit bei Tag |
| S2 | schwere Verletzungen, Ueberleben wahrscheinlich | H-05, H-07: Blendung mit verbleibender Reaktionszeit |
| S3 | lebensbedrohliche oder toedliche Verletzungen | H-01, H-02, H-03: unbeleuchtete Fahrbahn bzw. abrupte Blendung bei 80 km/h |

**Projektregel:** Bei Beteiligung eines 18-t-Zugs wird die Schaedigung Dritter mitbetrachtet, nicht
nur die der Fahrzeuginsassen. Das fuehrt bei Kollisionsszenarien systematisch auf S3.

## 2 Exposure — Wahrscheinlichkeit der Betriebssituation

| Klasse | Auslegung im Projekt | Beispiel |
|---|---|---|
| E0 | praktisch auszuschliessen | — |
| E1 | sehr geringe Wahrscheinlichkeit | — |
| E2 | geringe Wahrscheinlichkeit; mehrere Bedingungen muessen zusammentreffen | H-02, H-03, H-07 |
| E3 | mittlere Wahrscheinlichkeit; regelmaessig, aber nicht ueberwiegend | H-01, H-04, H-05, H-06 |
| E4 | hohe Wahrscheinlichkeit; ueberwiegender Teil der Betriebsdauer | — |

**Projektregel:** Bewertet wird die **Betriebssituation**, nicht der Fehler. Massgeblich ist der
Anteil an der Betriebsdauer gemaess Nutzungsprofil `A-07`
(siehe [`betriebssituationen.md`](betriebssituationen.md)).

**Bewusst getroffene Abgrenzung:** "Nachtfahrt" allgemein waere im Fernverkehr E4. Gefaehrdungsrelevant
ist aber die engere Situation *Nacht + unbeleuchtet + Landstrassengeschwindigkeit*, und die ist E3.
Diese Abgrenzung entscheidet zwischen ASIL B und ASIL C und wird als `RISK-01` gefuehrt.

## 3 Controllability — Beherrschbarkeit

| Klasse | Auslegung im Projekt | Beispiel |
|---|---|---|
| C0 | im Allgemeinen beherrschbar | — |
| C1 | einfach beherrschbar; praktisch alle Fahrer beherrschen die Situation | H-06 |
| C2 | normal beherrschbar; der ueberwiegende Teil der Fahrer beherrscht die Situation | H-01, H-02, H-03, H-04, H-05 |
| C3 | schwer oder nicht beherrschbar | H-07 |

**Projektregel:** Bewertet wird die Beherrschbarkeit durch die Person, die tatsaechlich handeln
muss. Bei Blendungsszenarien ist das der **geblendete** Fahrer, nicht der Fahrer des
verursachenden Fahrzeugs.

**Wovon die C-Einstufung abhaengt:** Fuer H-01 setzt C2 voraus, dass der Fahrer den Ausfall bemerkt
und reagiert. Diese Voraussetzung ist Annahme `A-03` und wird durch `FSR-004` (Fahrerwarnung
innerhalb 2 s) technisch gestuetzt. Faellt die Warnung weg, waere C3 zu pruefen — mit
entsprechender ASIL-Erhoehung. **Die Warnung ist damit nicht optional, sondern traegt die
Einstufung.**

## 4 Verwendete Kombinationen und Ergebnis

Nur die in dieser HARA tatsaechlich aufgetretenen Kombinationen, mit dem Ergebnis der
Einstufungstabelle nach ISO 26262-3:

| S | E | C | ASIL | Gefaehrdung |
|---|---|---|---|---|
| S3 | E3 | C2 | **B** | H-01, H-04 |
| S3 | E2 | C2 | **A** | H-02, H-03 |
| S2 | E3 | C2 | **A** | H-05 |
| S2 | E2 | C3 | **A** | H-07 |
| S1 | E3 | C1 | **QM** | H-06 |

Zur Einordnung der Grenzfalldiskussion: die Kombination S3/E4/C2 fuehrt auf **ASIL C**. Genau darum
ist die E-Einstufung von H-01 die kritische Entscheidung dieses Projekts.
