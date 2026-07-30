# Gefaehrdungsanalyse und Risikobewertung (HARA)

**Item:** Adaptives Front-Beleuchtungssystem inkl. Arbeitsscheinwerfer-Steuerung
**Fahrzeug:** Schwerer LKW, Klasse N3, 18 t Sattelzugmaschine
**Norm:** ISO 26262-3 (Hazard Analysis and Risk Assessment)
**Stand:** Phase 2, Entwurf — nicht durch ein Confirmation Review bestaetigt
**Verantwortlich:** safety-manager

> **Kein Serienstand.** Alle Einstufungen und Zahlenwerte sind plausible Beispielwerte eines
> Lehr-/Referenzprojekts, keine validierten Daten und kein Ersatz fuer eine reale HARA.

---

## 1 Methodik

1. **Item-Grenze festlegen** — siehe [`../01_item_definition/item_definition.md`](../01_item_definition/item_definition.md).
2. **Betriebssituationen bilden** als Kreuzprodukt Fahrsituation x Betriebsmodus x Umgebung,
   anschliessend auf die relevanten Kombinationen reduzieren — siehe
   [`betriebssituationen.md`](betriebssituationen.md).
3. **Fehlverhalten je Funktion systematisch ableiten** ueber die Fehlerklassen
   *loss of function · unintended activation · incorrect value · too early / too late · stuck*.
4. **Gefaehrdung auf Fahrzeugebene** formulieren (nicht die Bauteilstoerung, sondern die Wirkung
   im Verkehr).
5. **S/E/C einstufen** mit schriftlicher Begruendung je Einstufung —
   siehe [`sec_klassifikation.md`](sec_klassifikation.md).
6. **ASIL** aus der Kombination gemaess Einstufungstabelle ISO 26262-3 bestimmen.
7. **Safety Goals ableiten**, Gefaehrdungen mit identischer Zielformulierung zusammenfassen und
   dabei den hoechsten ASIL fuehren.

---

## 2 Gefaehrdungstabelle

| ID | BS | Fehlverhalten | Gefaehrdung auf Fahrzeugebene | S | E | C | **ASIL** | Safety Goal |
|---|---|---|---|---|---|---|---|---|
| **H-01** | BS-01 | Ausfall Abblendlicht (beide Kanaele) | Fahrbahn unbeleuchtet bei 80 km/h, Abkommen von der Fahrbahn oder Auffahren auf unbeleuchtetes Hindernis | 3 | 3 | 2 | **B** | SG-01 |
| **H-02** | BS-02 | Fernlicht bleibt bei Gegenverkehr aktiv | Blendung des entgegenkommenden Fahrers, Frontalkollision | 3 | 2 | 2 | **A** | SG-02 |
| **H-03** | BS-01 | Arbeitsscheinwerfer unbeabsichtigt waehrend der Fahrt aktiv | Blendung von Gegenverkehr und Nachfolgeverkehr | 3 | 2 | 2 | **A** | SG-02 |
| **H-04** | BS-03 | Unbeabsichtigtes Abschalten des Abblendlichts im Betrieb | wie H-01, zusaetzlich ueberraschend fuer den Fahrer | 3 | 3 | 2 | **B** | SG-01 |
| **H-05** | BS-01 | Leuchtweitenregulierung dauerhaft zu hoch | Dauerblendung des Gegenverkehrs | 2 | 3 | 2 | **A** | SG-02 |
| **H-06** | BS-06 | Ausfall Tagfahrlicht bei Tagfahrt | verminderte Erkennbarkeit des Fahrzeugs bei guter Sicht | 1 | 3 | 1 | **QM** | — |
| **H-07** | BS-05 | Kurvenlicht schwenkt in die Gegenfahrbahn | Blendung des Gegenverkehrs, unerwartet und vom Fahrer nicht korrigierbar | 2 | 2 | 3 | **A** | SG-02 |

**Ergebnis:** 7 Gefaehrdungen, davon 6 mit Safety Goal und eine (H-06) mit Ergebnis QM.
Hoechster resultierender ASIL: **B** (H-01, H-04) — damit ist ASIL B das Ziel-ASIL des Projekts.

> **Maschinenlesbare Form:** Jede Zeile dieser Tabelle existiert zusaetzlich als Datensatz
> `H-01.md` … `H-07.md` in diesem Ordner (Uebersicht: [`README.md`](README.md)). Die Safety Goals
> verweisen ueber `derived_from: [H-xx]` darauf; `tools/trace_check.py` meldet jede Gefaehrdung mit
> ASIL ungleich QM, zu der kein Safety Goal existiert (`hazard-uncovered`).
>
> **Bewusste Redundanz:** Die Werte stehen sowohl in dieser Tabelle als auch im Front-Matter der
> Datensaetze. Bei einer Aenderung sind **beide** zu pflegen — die Pruefung erkennt eine Abweichung
> zwischen Tabelle und Datensatz nicht.

---

## 3 Begruendung der Einstufungen

### H-01 — Ausfall Abblendlicht (auslegender Fall)

| | Einstufung | Begruendung |
|---|---|---|
| **S** | **S3** | Vollstaendiger Verlust der Fahrbahnausleuchtung bei 80 km/h auf unbeleuchteter Landstrasse. Ein Abkommen von der Fahrbahn oder ein Auffahren auf ein unbeleuchtetes Hindernis mit 18 t Gesamtmasse fuehrt mit hoher Wahrscheinlichkeit zu lebensbedrohlichen oder toedlichen Verletzungen, auch bei unbeteiligten Dritten. |
| **E** | **E3** | Nachtfahrt auf unbeleuchteter Landstrasse ist im N3-Fernverkehr regelmaessig, aber nicht ueberwiegend. Unter dem Nutzungsprofil `A-07` liegt der Anteil im Bereich weniger Prozent der Betriebsdauer — mittlere Wahrscheinlichkeit. |
| **C** | **C2** | Der Fahrer bemerkt den Ausfall unmittelbar (die Fahrbahn wird dunkel) und kann kontrolliert verzoegern; Restlicht durch Standlicht/Tagfahrlicht und Fremdlicht bleibt erhalten. Ein sicheres Anhalten gelingt dem ueberwiegenden Teil der Fahrer, aber nicht praktisch allen — daher C2 und nicht C1. |

**Grenzfalldiskussion (bewusst offengelegt, gefuehrt als `RISK-01`):**
Mit **E4** statt E3 ergaebe die Einstufungstabelle **ASIL C** statt B. E3 wurde gewaehlt, weil die
Gefaehrdung an die Kombination *Nacht + unbeleuchtet + Landstrassengeschwindigkeit* gebunden ist,
nicht an Nachtfahrt allgemein. Dies ist die sensibelste Einzelentscheidung der gesamten HARA — sie
bestimmt das Ziel-ASIL des Projekts und damit die Zielwerte fuer SPFM, LFM und PMHF, die geforderte
Unabhaengigkeit und die Strukturabdeckung in der Software. Sie ist im Confirmation Review von SG-01
ausdruecklich zu bestaetigen.

### H-02 und H-03 — Blendung durch Fernlicht bzw. Arbeitsscheinwerfer

| | Einstufung | Begruendung |
|---|---|---|
| **S** | S3 | Blendung des Gegenverkehrs kann zur Frontalkollision fuehren; bei Beteiligung eines 18-t-Zugs sind toedliche Verletzungen wahrscheinlich. |
| **E** | E2 | Die Gefaehrdung setzt gleichzeitig Nacht, Gegenverkehr und einen Fehlerfall voraus — geringe Exposition. |
| **C** | C2 | Der geblendete Fahrer kann typischerweise durch Verzoegern und Spurhalten reagieren; die Blendung ist kurzzeitig und wird als solche erkannt. |

### H-04 — Unbeabsichtigtes Abschalten

Wirkung identisch zu H-01, daher gleiche Einstufung **S3/E3/C2**. Unterschied ist die Fehlerklasse:
H-01 ist ein Ausfall, H-04 eine unbeabsichtigte Deaktivierung. Beide fuehren auf **SG-01**, werden
aber durch unterschiedliche Sicherheitsanforderungen adressiert (`FSR-001` gegenueber `FSR-002`).

### H-05 — Leuchtweitenregulierung zu hoch

**S2** — die Blendung baut sich weniger abrupt auf als bei H-02, dem Gegenverkehr bleibt
Reaktionszeit; schwere, aber ueberlebbare Verletzungen sind der wahrscheinlichere Ausgang.
**E3** — betrifft grundsaetzlich jede Nachtfahrt mit Gegenverkehr.
**C2** — beherrschbar durch Verzoegern.

### H-06 — Ausfall Tagfahrlicht (Ergebnis QM)

**S1** — ein 18-t-Fahrzeug bleibt bei Tag und guter Sicht durch seine Silhouette gut erkennbar;
allenfalls leichte Verletzungen sind zu erwarten.
**E3** — Tagfahrt bei guter Sicht ist haeufig, der Ausfall selbst ist jedoch die Voraussetzung.
**C1** — die Situation ist von praktisch allen Verkehrsteilnehmern beherrschbar.

> **Ergebnis QM — es entsteht kein Safety Goal.** Die zugehoerige Anforderung bleibt gesetzlich
> relevant (ECE R48, Schaltvorschrift Tagfahrlicht), aber nicht sicherheitsrelevant im Sinne der
> ISO 26262. Dieser Fall ist bewusst enthalten, um zu zeigen, dass nicht jede Gefaehrdung in ein
> Safety Goal muendet.

### H-07 — Kurvenlicht schwenkt in die Gegenfahrbahn

**S2** — Blendung mit Reaktionszeit, wie H-05.
**E2** — setzt Kurvenfahrt bei Nacht mit Gegenverkehr und Fehlerfall voraus.
**C3** — die Fehlausrichtung tritt unerwartet auf und ist vom betroffenen Fahrer selbst nicht
korrigierbar; er kann lediglich verzoegern. Daher schwer beherrschbar.

---

## 4 Abgeleitete Safety Goals

| ID | Formulierung | ASIL | Safe State | FTTI | Fault Reaction Time | Quelle |
|---|---|---|---|---|---|---|
| **SG-01** | Kein unerkannter Ausfall des Abblendlichts waehrend der Fahrt | **B** | Notlaufbetrieb: verbleibende Kanaele aktiv mit reduzierter Leistung, Fahrerwarnung aktiv, DTC gesetzt | **300 ms** | **150 ms** | H-01, H-04 |
| **SG-02** | Keine unbeabsichtigte Blendung anderer Verkehrsteilnehmer durch Fernlicht oder Arbeitsscheinwerfer | **A** | Fernlicht und Arbeitsscheinwerfer deaktiviert, Abblendlicht bleibt aktiv | 500 ms | 250 ms | H-02, H-03, H-05, H-07 |

Datensaetze: [`../03_fsc/SG-01.md`](../03_fsc/SG-01.md) · [`../03_fsc/SG-02.md`](../03_fsc/SG-02.md)

### Begruendung des Safe State von SG-01

"Licht aus" waere der falsche sichere Zustand — er *ist* die Gefaehrdung. Der Safe State ist
deshalb *degradiert sichtbar*: der intakte Kanal wird weiterbetrieben (`FSR-003`), der Fahrer wird
gewarnt (`FSR-004`) und kann die Fahrt kontrolliert beenden. Genau diese Warnung traegt die
C2-Einstufung von H-01. Damit ist Annahme **`A-03`** (Fahrerreaktion auf die Warnung)
sicherheitsrelevant und Validierungsziel auf Fahrzeugebene, nicht nur eine Randnotiz.

### Zeitbudget SG-01

```
Erkennung        SM-01:  50 ms Schwellwert + 20 ms Entprellung  =  70 ms
Fehlerreaktion   Uebergang in den Notlauf                       = 150 ms   (Fault Reaction Time)
                                                          Summe = 220 ms
FTTI                                                            = 300 ms
Reserve                                                         =  80 ms   (27 %)
```

Das Budget schliesst gegen die in `SG-01` und `SM-01` hinterlegten Werte. Die 2 s Fahrerwarnung aus
`CR-007` / `FSR-004` liegen **ausserhalb** dieses Budgets: sie sind Informationsanforderung, nicht
Fehlerreaktion. Diese Trennung ist bindend — sonst wird gegen die falsche Zeitschranke ausgelegt.

---

## 5 Verwendete Annahmen

| ID | Annahme | Sicherheitsrelevant |
|---|---|---|
| `A-03` | Der Fahrer reagiert auf die optische Warnung innerhalb der angenommenen Reaktionszeit | ja — traegt die C-Einstufung von H-01 |
| `A-05` | Objekterkennung fuer das blendfreie Fernlicht liegt ausserhalb der Item-Grenze | ja — Teil der SG-02-Kette |
| `A-06` | Lichtschalterstellung und Zuendungsstatus kommen als Bussignale | ja |
| `A-07` | Nutzungsprofil N3-Fernverkehr mit ueberwiegendem Nachtanteil im Winterhalbjahr | ja — Grundlage der E-Einstufung |

Vollstaendige Liste: [`../../09_process/assumptions.md`](../../09_process/assumptions.md)

---

## 6 Offene Punkte

| ID | Punkt | Owner |
|---|---|---|
| OP-7 / `RISK-01` | E-Einstufung von H-01 (E3 gegenueber E4) im Confirmation Review bestaetigen | safety-manager |
| OP-9 | `A-03` als Validierungsziel auf Fahrzeugebene einplanen | verification-engineer |
| OP-10 | Schnittstellenvereinbarung (DIA) zur Objekterkennung ausserhalb der Item-Grenze | safety-manager |
| OP-13 | Rollenmodell und Unabhaengigkeitsgrade fehlen (Phase 0 uebersprungen) — Voraussetzung fuer das Confirmation Review dieser HARA | safety-manager |

---

**Work Products:** `hara.md`, `betriebssituationen.md`, `sec_klassifikation.md` → `02_safety/02_hara/`
**Prozessbezug:** ISO 26262 **Part 3** (Hazard Analysis and Risk Assessment, Safety Goals) ·
**Part 2** (Confirmation Review der HARA) · ASPICE **SYS.1/SYS.2** als Anforderungsgrundlage.
