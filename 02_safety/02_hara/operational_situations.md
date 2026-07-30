# Betriebssituationen (Situationskatalog)

Grundlage der Gefaehrdungsanalyse in [`hara.md`](hara.md). Der Katalog entsteht als Kreuzprodukt
**Fahrsituation x Betriebsmodus x Umgebung** und wird anschliessend auf die Kombinationen reduziert,
die fuer die Beleuchtungsfunktionen relevant sind.

> Werte sind plausible Beispielwerte eines Lehrprojekts, keine validierten Nutzungsdaten.
> Grundlage des Nutzungsprofils ist Annahme `A-07`.

## 1 Dimensionen

| Dimension | Auspraegungen |
|---|---|
| **Fahrsituation** | Stillstand · Rangieren (< 10 km/h) · Stadt (50 km/h) · Landstrasse (80 km/h) · Autobahn (85 km/h) |
| **Betriebsmodus** | Tagfahrlicht · Abblendlicht · Fernlicht · Kurvenlicht · Arbeitsscheinwerfer · Notlauf |
| **Umgebung** | Tag / Daemmerung / Nacht · beleuchtet / unbeleuchtet · trocken / Regen / Nebel · Gegenverkehr ja / nein |

Das vollstaendige Kreuzprodukt umfasst mehrere hundert Kombinationen. Reduziert wurde nach zwei
Kriterien: (1) technisch moegliche Kombination, (2) Relevanz fuer mindestens eine Lichtfunktion.
Kombinationen ohne Gefaehrdungspotenzial (z. B. Stillstand mit Tagfahrlicht bei Tag) sind bewusst
nicht gefuehrt.

## 2 Relevante Betriebssituationen

| ID | Fahrsituation | Betriebsmodus | Umgebung | Verwendet in |
|---|---|---|---|---|
| **BS-01** | Landstrasse, 80 km/h | Abblendlicht aktiv | Nacht, unbeleuchtet, trocken | H-01, H-03, H-05 |
| **BS-02** | Landstrasse, 80 km/h | Fernlicht aktiv | Nacht, Gegenverkehr | H-02 |
| **BS-03** | Autobahn, 85 km/h | Abblendlicht aktiv | Nacht, Regen | H-04 |
| **BS-04** | Baustelle / Hof, < 10 km/h | Arbeitsscheinwerfer aktiv | Nacht | — (bestimmungsgemaesse Nutzung) |
| **BS-05** | Stadtverkehr, 50 km/h | Abblendlicht + Kurvenlicht | Nacht, beleuchtet | H-07 |
| **BS-06** | Landstrasse, 80 km/h | Tagfahrlicht aktiv | Tag, gute Sicht | H-06 |
| **BS-07** | Stillstand, Zuendung EIN | Arbeitsscheinwerfer aktiv | Nacht, Ladestelle | — (bestimmungsgemaesse Nutzung) |

**BS-04** und **BS-07** fuehren auf keine Gefaehrdung, weil der Arbeitsscheinwerferbetrieb dort
bestimmungsgemaess ist. Sie bleiben im Katalog, weil sie die Abgrenzung zu H-03 begruenden: erst die
Kombination *Arbeitsscheinwerfer aktiv* mit *Fahrbetrieb* ist gefaehrdend, nicht der Betriebsmodus
an sich. Genau diese Unterscheidung realisiert `FSR-008` ueber die Geschwindigkeitsschwelle.

## 3 Nutzungsprofil (Grundlage der E-Einstufung)

| Situation | Geschaetzter Anteil an der Betriebsdauer | Einstufung |
|---|---|---|
| Nachtfahrt gesamt | ca. 25 % | — |
| davon Nachtfahrt auf unbeleuchteter Landstrasse (BS-01) | wenige Prozent | **E3** |
| Nachtfahrt mit Gegenverkehr und aktivem Fernlicht (BS-02) | gering | **E2** |
| Tagfahrt bei guter Sicht (BS-06) | ueberwiegend | **E3** im Kontext von H-06 |

> Die Zuordnung *unbeleuchtete Landstrasse bei Nacht* zu **E3** statt E4 ist die kritische
> Entscheidung der HARA und wird als `RISK-01` gefuehrt. Eine Bestaetigung durch reale
> Nutzungsdaten des OEM steht aus (`A-07`).
