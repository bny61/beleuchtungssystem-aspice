# Item Definition

**Item:** Adaptives Front-Beleuchtungssystem inkl. Arbeitsscheinwerfer-Steuerung
**Fahrzeug:** Schwerer LKW, Klasse N3, 18 t Sattelzugmaschine
**Norm:** ISO 26262-3 (Item Definition)
**Stand:** Phase 2, Entwurf
**Verantwortlich:** safety-manager

> Lehr-/Referenzprojekt, kein Serienstand. Zahlenwerte sind plausible Beispielwerte.

---

## 1 Zweck und Funktionen

Das Item stellt die Beleuchtung nach vorn sowie die Arbeitsscheinwerfer-Steuerung bereit:

| Funktion | Kurzbeschreibung |
|---|---|
| Abblendlicht | Grundausleuchtung der Fahrbahn, mehrkanalig ausgefuehrt |
| Fernlicht | Reichweitenausleuchtung, blendfrei ausblendbar |
| Tagfahrlicht | Erkennbarkeit bei Tag |
| Kurvenlicht | lenkwinkel- und geschwindigkeitsabhaengige Schwenkung |
| Leuchtweitenregulierung | beladungsabhaengige Neigungskorrektur |
| Arbeitsscheinwerfer | Ausleuchtung im Stand und beim Rangieren |
| Diagnose | Fehlererkennung, DTC-Verwaltung, UDS-Zugriff |

## 2 Item-Grenze

### Innerhalb der Item-Grenze

| Element | Rolle |
|---|---|
| `ECU_LightingCtrl` | Lighting-ECU, Steuerung und Ueberwachung aller Lichtfunktionen |
| `LED_Driver_Stage_1..n` | LED-Treiberstufen der einzelnen Kanaele |
| Strom- und Temperatursensorik | Rueckmeldung fuer Diagnose und Derating |
| Scheinwerfermodule | Abblend-, Fern- und Kurvenlicht |
| Arbeitsscheinwerfer-Endstufen | Ansteuerung der Arbeitsscheinwerfer |

### Ausserhalb der Item-Grenze (Schnittstellen)

| Element | Beziehung | Annahme |
|---|---|---|
| Bordnetz 24 V | Versorgung KL30 / KL15, 16–32 V | `A-01` |
| Fahrzeug-Gateway (CAN FD / J1939) | Lichtanforderung, Geschwindigkeit, Lenkwinkel, Statusrueckmeldung | `A-02` |
| Umfeldsensorik (Objekterkennung) | Objektliste fuer blendfreies Fernlicht | `A-05` |
| Lichtschalter, Zuendung | als Bussignale, keine Direktverdrahtung | `A-06` |
| Kombiinstrument | Anzeige der Fahrerwarnung | `A-04` |
| Diagnosetester (Werkstatt) | UDS nach ISO 14229 | — |

### Ausdruecklich nicht im Scope

Heckbeleuchtung · Innenraumbeleuchtung · Blinker und Warnblinker · Nebelscheinwerfer ·
Beleuchtung des Aufbauherstellers hinter der Aufbau-Schnittstelle.

> Die Ausschluesse sind bewusst explizit gelistet. Eine stillschweigende Abgrenzung ist im
> Assessment ein Befund, keine Vereinfachung.

## 3 Kontextdiagramm

Quelle: [`../../03_model/plantuml/ctx_item.puml`](../../03_model/plantuml/ctx_item.puml)

Der gelbe Block ist die Item-Grenze — nur was darin liegt, wird in diesem Projekt entwickelt.
Graue Bloecke sind Fremdsysteme. Jede Kante ueber die Grenze ist eine Schnittstelle, die in Phase 3
mit Signal, Richtung, Typ, Wertebereich, Timing und ASIL zu spezifizieren ist.

> Das Diagramm ist bisher **nicht** syntaktisch geprueft (PlantUML lokal nicht installiert,
> `OP-12`). In der CI uebernimmt das der Job `Modell-Syntaxpruefung`.

## 4 Betriebsmodi

| Modus | Beschreibung |
|---|---|
| Init | Selbsttest nach Zuendung EIN |
| Betrieb Normal | alle Lichtfunktionen verfuegbar |
| Degraded | Teilausfall erkannt, verbleibende Kanaele aktiv |
| Safe State (Notlauf) | reduzierte Leistung, Fahrerwarnung aktiv, DTC gesetzt |
| Sleep | Zuendung AUS, Ruhestrombetrieb nach Nachlaufzeit |

## 5 Abhaengigkeiten von anderen Items

| Abhaengigkeit | Auswirkung auf die Sicherheit |
|---|---|
| Objekterkennung (Fahrzeugebene) | Teil der Wirkkette von `SG-02`; erfordert eine Schnittstellenvereinbarung (DIA) — `OP-10` |
| Bordnetz | Versorgungsqualitaet beeinflusst alle Lichtfunktionen; gemeinsame Ausfallursache, in der DFA zu betrachten |
| Kombiinstrument | traegt die Fahrerwarnung aus `FSR-004` und damit die C-Einstufung von H-01 |

## 6 Weiterfuehrend

- Gefaehrdungsanalyse: [`../02_hara/hara.md`](../02_hara/hara.md)
- Safety Goals und FSC: [`../03_fsc/`](../03_fsc/)
- Annahmen: [`../../09_process/assumptions.md`](../../09_process/assumptions.md)

**Prozessbezug:** ISO 26262 **Part 3** (Item Definition) · ASPICE **SYS.1** (Systemkontext).
