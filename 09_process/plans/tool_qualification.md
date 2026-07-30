# Tool-Qualifikation — Hinweis fuer die CI-Skripte (ISO 26262-8, Clause 11)

**Status:** Vorbetrachtung, kein Qualifikationsnachweis. Lehr-/Referenzprojekt.

## Betrachtete Werkzeuge

| Werkzeug | Zweck im Projekt | Erzeugt Nachweis? | Betrachtung |
|---|---|---|---|
| `tools/trace_check.py` | Prueft Traceability-Konsistenz, erzeugt Traceability-Matrix und Coverage-KPIs | **ja** | Qualifikationskandidat — siehe unten |
| GitHub Actions Runner | Fuehrt die Pruefungen aus, archiviert Artefakte | mittelbar | Infrastruktur; Nachweis liegt in den archivierten Artefakten |
| PlantUML | Rendert Modellsichten aus Textquellen | nein (Darstellung) | Quelle ist der Text, nicht das Bild — Fehlrendering ist im Review erkennbar |
| Compiler / statische Analyse / Coverage-Tool | SW-Verifikation | ja | Eigene Betrachtung im SW-Plan (Phase 7) erforderlich |

## Argumentationslinie fuer `trace_check.py`

**Anwendungsfall:** Das Skript kann einen Fehler *einfuehren* (falsche Matrix) oder einen
vorhandenen Fehler *nicht erkennen* (fehlende Trace bleibt unentdeckt). Der zweite Fall ist der
relevantere: das Skript wirkt als Verifikationsmassnahme.

**Fehlermoeglichkeiten:**
1. Front-Matter wird falsch geparst → Datensatz wird stillschweigend ignoriert.
2. Prueflogik enthaelt einen Fehler → Finding wird nicht gemeldet.
3. Ein Verzeichnis liegt ausserhalb von `SEARCH_DIRS` → Datensaetze werden nicht erfasst.

**Massnahmen zur Reduktion des Vertrauensbedarfs:**
- Ausschliesslich Standardbibliothek — keine unqualifizierte Drittabhaengigkeit.
- Das Skript gibt die Anzahl gefundener Datensaetze aus; ein unerwartet niedriger Wert ist im
  Review erkennbar (Fehlermoeglichkeit 1 und 3 werden dadurch beobachtbar).
- Zusaetzliche menschliche Reviewpflicht (CODEOWNERS, PR-Checkliste) — der CI-Check ersetzt das
  Review nicht, er ergaenzt es.
- Negativtests: bewusst fehlerhafte Datensaetze muessen die erwarteten Findings ausloesen.

**Offener Punkt:** Ein tatsaechlicher Qualifikationsnachweis (Tool Classification mit TI/TD,
resultierendes TCL und die daraus folgende Qualifikationsmethode) ist **nicht** erbracht. Fuer einen
Serienstand waere er zu fuehren. Diese Datei benennt die Luecke, sie schliesst sie nicht.

## Ehrliche Grenze

Solange die Toolqualifikation offen ist, darf ein gruener CI-Lauf im Safety Case nur als
*unterstuetzender* Nachweis (Sn-07) argumentiert werden, nicht als alleiniger Nachweis der
Anforderungsvollstaendigkeit.
