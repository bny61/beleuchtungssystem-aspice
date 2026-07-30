# Meta-Prompt: MBSE-Beispielprojekt „Beleuchtungssystem Nutzfahrzeug" (ASPICE + ISO 26262)

> **Nutzung:** Block unten komplett kopieren, die `<<PLATZHALTER>>` ersetzen, in ein LLM einfügen.
> Die Phasen-Ausgabe ist bewusst getaktet — so bleibt die Tiefe steuerbar und der Kontext sauber.

---

## VARIABLEN (vor dem Einfügen anpassen)

| Variable | Vorschlag / Default |
|---|---|
| `<<FAHRZEUG>>` | Schwerer LKW, N3-Klasse, 18 t Sattelzugmaschine |
| `<<PRODUKT>>` | Adaptives Front-Beleuchtungssystem inkl. Arbeitsscheinwerfer-Steuerung |
| `<<ZIEL_ASIL>>` | ASIL B (Ausfall Abblendlicht bei Nachtfahrt) |
| `<<SPRACHE>>` | Deutsch, Fachbegriffe und Normbegriffe englisch belassen |
| `<<MBSE_METHODE>>` | MagicGrid (SysML v1.6) |
| `<<NOTATION>>` | PlantUML (alternativ: Mermaid) |
| `<<TOOLCHAIN>>` | Cameo/MagicDraw, Polarion oder Requirements-as-Code, Git/GitHub, Jenkins-frei (nur GitHub Actions) |
| `<<UMFANG>>` | Lehr-/Referenzprojekt, kein Serienstand |

---

## PROMPT (ab hier kopieren)

### Rolle

Du agierst als **Lead Systems Engineer & Functional Safety Manager** in der Nutzfahrzeug-Zulieferindustrie. Du hast Serienerfahrung mit Automotive SPICE (PAM 4.0), ISO 26262:2018 und modellbasierter Systementwicklung. Du schreibst wie in einem echten Projekthandbuch: präzise, mit IDs, Tabellen und Modellen — nicht wie ein Lehrbuchkapitel.

### Auftrag

Erstelle ein **durchgängiges, nachvollziehbares Beispielprojekt** für ein `<<PRODUKT>>` in `<<FAHRZEUG>>`. Das Projekt zeigt den Weg **von Kundenanforderungen → Systemanforderungen → E/E-Systemarchitektur → Hardware & Software → Verifikation → Safety Case**, durchgängig modellbasiert (`<<MBSE_METHODE>>`) und normkonform (ASPICE + ISO 26262). Versionierung, Konfigurationsmanagement und Nachweisführung laufen über **GitHub**.

Sprache: `<<SPRACHE>>`. Umfang/Zweck: `<<UMFANG>>`.

### Die zentrale Tiefenregel — „Golden Thread"

Das Projekt muss **breit, aber nicht überall tief** sein:

- **Breite (Übersichtsniveau):** Jede Phase, jedes Work Product, jeder Prozess wird benannt, eingeordnet und mit 3–8 repräsentativen Einträgen befüllt.
- **Tiefe (Detailniveau):** Genau **ein durchgehender Faden** wird über alle Ebenen bis ins Detail ausgearbeitet:
  `SG-01 „Kein unerkannter Ausfall des Abblendlichts während der Fahrt" (`<<ZIEL_ASIL>>`)`
  → FSR → TSR → Systemarchitektur-Element → HW-Sicherheitsmechanismus → SW-Komponente inkl. Detaildesign → Testfälle → FTA-Pfad → FMEDA-Zeile → Safety-Case-Argument.
- Zusätzlich **ein zweiter, flacherer Faden** zum Kontrast: `SG-02 „Keine unbeabsichtigte Blendung durch Fernlicht/Arbeitsscheinwerfer"`.

Markiere Detail-Abschnitte sichtbar mit `🔍 DEEP DIVE` und Übersichts-Abschnitte mit `📋 ÜBERSICHT`.

### Methodischer Rahmen (verbindlich)

**ASPICE (PAM 4.0) — mindestens abzudecken:**
`SYS.1, SYS.2, SYS.3, SYS.4, SYS.5` · `SWE.1–SWE.6` · `HWE.1–HWE.4` · `SUP.1 (QA), SUP.4 (Reviews), SUP.8 (Konfigurationsmanagement), SUP.9 (Problemlösung), SUP.10 (Änderungsmanagement)` · `MAN.3 (Projektmanagement)`.
Für jeden Prozess: Zweck in 1 Satz, konkrete Work Products im Projekt, Ablageort im Repo.

**ISO 26262:2018 — mindestens abzudecken:**
Part 3 (Item Definition, HARA, Safety Goals, FSC) · Part 4 (TSC, System-Integration, Validierung) · Part 5 (HW-Anforderungen, HW-Metriken) · Part 6 (SW-Anforderungen, -Architektur, -Unit-Design, Verifikation) · Part 8 (Requirements-, Konfigurations-, Änderungsmanagement, Tool-Qualifikation) · Part 9 (ASIL-Dekomposition, DFA, Safety Analyses).

**MBSE:** `<<MBSE_METHODE>>`. Die Modellsichten werden als `<<NOTATION>>`-Code ausgegeben, sodass sie direkt renderbar sind.

### Geforderte Projektstruktur (Phasen)

**Phase 0 — Projektrahmen**
Scope & Abgrenzung, Stakeholder-Liste mit Interessen, Rollenmodell (Safety Manager, Systemarchitekt, HW-/SW-Lead, Test-Lead, unabhängiger Assessor + Unabhängigkeitsgrad nach ISO 26262-2), Tailoring-Entscheidungen mit Begründung, Glossar & Abkürzungsverzeichnis, Annahmenliste (`A-01…`).

**Phase 1 — Kundenanforderungen (SYS.1)**
15–25 Kundenanforderungen `CR-xxx` als Lastenheft-Auszug. Kategorien: funktional, gesetzlich (ECE R48 Anbau, R112/R123 Scheinwerfer, R65 Rundumkennleuchte, R10 EMV), Umwelt/Mechanik (ISO 16750), Elektrik (24 V Bordnetz, ISO 7637 Pulse), Diagnose (UDS ISO 14229), Kommunikation (CAN FD / SAE J1939, LIN), Lebensdauer, Cybersecurity-Schnittstelle (ISO 21434, nur Verweis). Formuliert nach EARS-Schablone. Bewertung der Anforderungsqualität (eindeutig, testbar, atomar) mit kurzem Review-Kommentar bei 3 bewusst schwachen Anforderungen inkl. Verbesserungsvorschlag.

**Phase 2 — Item Definition & HARA (ISO 26262-3)**
Item-Grenze mit Kontextdiagramm, Betriebssituationen (Situation × Betriebsmodus × Umgebung), Gefährdungsanalyse-Tabelle mit S/E/C-Bewertung inkl. **Begründung je Einstufung**, resultierende ASIL, mindestens 6 Hazards. Daraus Safety Goals `SG-xx` mit **Safe State, FTTI, Fault Reaction Time**. Anschließend Functional Safety Concept: `FSR-xxx` je Safety Goal, Zuordnung zu Architekturelementen, ggf. ASIL-Dekomposition mit Nachweis der Unabhängigkeit.

**Phase 3 — Systemanforderungen & E/E-Architektur (SYS.2, SYS.3, ISO 26262-4)**
`SYS-REQ-xxx` abgeleitet aus `CR-xxx` + `FSR-xxx` (Trace zwingend). Technische Sicherheitsanforderungen `TSR-xxx`. E/E-Architektur: Lighting-ECU (µC mit Lockstep oder µC+ASIC-Watchdog), LED-Treiber-Stufen, Stromsensorik, Temperatursensorik, Bordnetz-Interface, Bus-Anbindung, Diagnose-Pfad. Schnittstellen-Tabelle (Signal, Richtung, Typ, Wertebereich, Timing, ASIL). Allokation der `TSR` auf HW / SW / System-Maßnahmen als Matrix.

**Phase 4 — MBSE-Modell (`<<MBSE_METHODE>>`)**
MagicGrid-Matrix (Problem Domain / Solution Domain × Requirements / Behavior / Structure / Parameters) als Tabelle, gefüllt mit den konkreten Artefakten dieses Projekts. Dazu als `<<NOTATION>>`-Code:
1. Use-Case-Diagramm (Akteure: Fahrer, Werkstatt, Fahrzeug-Gateway, Umgebung)
2. Requirements-Diagramm mit `«deriveReqt»` / `«satisfy»` / `«verify»`
3. Activity-Diagramm „Abblendlicht aktivieren inkl. Fehlerfall"
4. Sequence-Diagramm „Erkennung Open Load → Fehlerreaktion → Diagnose-DTC"
5. State Machine „Lichtsystem-Betriebszustände" inkl. Safe State
6. BDD (Systemzerlegung) und IBD (Ports, Flows, Signalpfade)
7. Parametric-Diagramm für eine Constraint (z. B. Lichtstrom vs. Sperrschichttemperatur vs. Strom)
8. Allokationstabelle Funktion → Logisches Element → Physisches Element

**Phase 5 — Sicherheitsanalysen & Nachweisführung**
- **System-FMEA** nach AIAG-VDA 7-Schritt-Methodik: Struktur-, Funktions-, Fehleranalyse, Risikoanalyse mit **B/A/E und Aufgabenpriorität (AP)** — nicht RPZ. Mindestens 8 Zeilen, davon 3 im Golden Thread.
- **DFMEA** für die ECU-Baugruppe, Auszug 5 Zeilen.
- **FTA** je Safety Goal: Top Event = Verletzung des SG, Baumstruktur mit UND/ODER-Gattern als `<<NOTATION>>`-Grafik, Basisereignisse, **Minimal Cut Sets**, Bewertung ob Single Point Faults existieren.
- **FMEDA-Auszug** für den Golden Thread: Bauteil, λ, Fehlermodus-Verteilung, Diagnosedeckungsgrad, klassifiziert als SPF/RF/MPF/SF. Berechnung und Abgleich gegen die `<<ZIEL_ASIL>>`-Zielwerte (SPFM, LFM, PMHF) inkl. Rechenweg.
- **DFA (Dependent Failure Analysis)** für den dekomponierten Pfad: Kopplungsfaktoren (gemeinsame Versorgung, gemeinsamer Takt, thermisch, räumlich) und Gegenmaßnahmen.
- **STPA** als ergänzende Analyse, kurz: unsichere Steueraktionen für „Fernlicht ein".
- **Verifikationsmatrix**: Welches Werkzeug weist welche Anforderung nach (Analyse, Review, Simulation, Test, Feldnachweis).

**Phase 6 — Hardware (HWE.1–HWE.4, ISO 26262-5)**
`HW-REQ-xxx`, HW-Architektur in Blöcken, Sicherheitsmechanismen (Open-Load-/Short-to-Battery-Erkennung, Überstrom, Übertemperatur mit Derating-Kennlinie, Watchdog, Spannungsüberwachung), Sicherheitsanalyse-Rückkopplung, HW-Verifikationsplan (DV/PV, EMV, ISO 16750 Umwelt, HALT/HASS-Ansatz).

**Phase 7 — Software (SWE.1–SWE.6, ISO 26262-6)**
`SW-REQ-xxx` inkl. Timing-Anforderungen. SW-Architektur in Schichten (MCAL / BSW bzw. AUTOSAR Classic / Service Layer / Application) mit Komponentendiagramm und dynamischem Verhalten (Tasks, Zykluszeiten, Prioritäten). Für **eine** Komponente (`SWC_LightManager`) vollständiges Detaildesign: Schnittstellen, Zustandsautomat, Fehlerbehandlungsstrategie, Pseudocode. Coding-Vorgaben (MISRA C:2012 inkl. 2 Beispiel-Deviations mit Begründung), statische Analyse, Unit-Test-Strategie inkl. geforderter Strukturabdeckung für `<<ZIEL_ASIL>>` und Begründung der Metrikwahl. Freiheit-von-Rückwirkung (Speicherpartitionierung, Timing Monitoring) falls gemischte ASIL vorliegen.

**Phase 8 — Verifikation & Validierung (SYS.4, SYS.5, ISO 26262-4)**
Teststrategie je V-Ebene mit Zuordnung Methode → Ebene → Nachweisziel. Beispiel-Testfälle `TC-xxx` in Tabellenform (Vorbedingung, Schritte, erwartetes Ergebnis, abgedeckte Anforderungs-ID, ASIL, Umgebung: MiL/SiL/HiL/Fahrzeug). Fehlerinjektionstests für die Sicherheitsmechanismen. Validierung der Safety Goals auf Fahrzeugebene. Regressionsstrategie.

**Phase 9 — Safety Case & Confirmation Measures**
Work-Product-Liste mit Status. Safety-Case-Argumentationsstruktur (GSN-Skizze: Goal → Strategy → Solution → Evidence) für `SG-01`. Confirmation Reviews, Functional Safety Audit, Functional Safety Assessment inkl. geforderter Unabhängigkeit. Release-for-Production-Kriterien.

**Phase 10 — GitHub: Versionierung, Konfigurationsmanagement, Nachweis**
- **Repo-Struktur** als Verzeichnisbaum (`/01_requirements`, `/02_safety`, `/03_model`, `/04_architecture`, `/05_hardware`, `/06_software`, `/07_verification`, `/08_safety_case`, `/09_process`, `/.github`).
- **Requirements-as-Code**: Anforderungen als Markdown/YAML mit Front-Matter (`id`, `text`, `type`, `asil`, `derived_from`, `allocated_to`, `verified_by`, `status`) — inkl. konkretem Beispiel-File.
- **Branching-Strategie** mit Begründung, Namenskonventionen für Branches und Commits (Conventional Commits mit Anforderungs-ID im Footer).
- **Baselines**: Git Tags + GitHub Releases als Konfigurationsbaselines (SUP.8), Tag-Schema, was zu welchem Gate eingefroren wird.
- **Issues & Projects**: Issue-Templates für Change Request, Problem Report (SUP.9), Safety Anomaly, Requirement Change. Label-Schema (`asil-b`, `safety-relevant`, `sys-req`, `swe`, `hwe`, `impact-analysis-required`). GitHub Projects als MAN.3-Board mit Gates.
- **Pull Requests als Review-Nachweis (SUP.4)**: PR-Template mit Review-Checkliste, `CODEOWNERS` für sicherheitsrelevante Ordner, Branch Protection Rules als technisch erzwungene Freigabe, Aufbewahrung als auditierbarer Nachweis.
- **GitHub Actions**: Workflows für Traceability-Konsistenzprüfung (Skript, das verwaiste oder ungetestete Anforderungen findet), Requirements-Linting, Modell-Export/Render, Unit-Tests + Coverage-Gate, statische Analyse, automatische Erzeugung der Traceability-Matrix und des Safety-Case-Dokuments. Ein Workflow als vollständige YAML ausgeben.
- **Git LFS** für Binärmodelle, Umgang mit Tool-generierten Artefakten, Tool-Qualifikations-Hinweis (ISO 26262-8, Clause 11) für die CI-Skripte.
- **Mapping-Tabelle**: ASPICE-Prozess / ISO-26262-Anforderung ↔ GitHub-Mechanismus ↔ erzeugter Nachweis. Plus ehrliche Grenzen: was GitHub allein **nicht** abdeckt.

**Phase 11 — Durchgängige Traceability & Metriken**
Vollständige bidirektionale Traceability-Matrix `CR → SYS-REQ → FSR/TSR → HW-REQ/SW-REQ → Design → TC → Ergebnis` für den Golden Thread; für den Rest verdichtete Übersicht. Coverage-KPIs (Anforderungsabdeckung, Testabdeckung, Analyseabdeckung) und wie sie in der CI gemessen werden.

### Formatvorgaben

- Durchgängiges **ID-Schema**: `CR-`, `SYS-REQ-`, `SG-`, `FSR-`, `TSR-`, `HW-REQ-`, `SW-REQ-`, `SM-` (Sicherheitsmechanismus), `TC-`, `A-` (Annahme), `RISK-`.
- Anforderungen **immer als Tabelle** mit: ID · Text · Typ · ASIL · Quelle/Trace · Verifikationsmethode · Status.
- Diagramme **immer** als renderbarer `<<NOTATION>>`-Codeblock, jeweils mit 1–2 Sätzen Leseanleitung darunter.
- Jede Phase endet mit: **Work Products** (Dateiname + Repo-Pfad) · **Offene Punkte** · **Verweis auf ASPICE-Prozess und ISO-26262-Clause**.
- Klausel-Verweise nur, wenn du dir sicher bist; ansonsten den Part/Thema nennen statt eine Nummer zu erfinden. **Keine erfundenen Normzitate, keine wörtlichen Normtexte.**
- Annahmen explizit als `A-xx` kennzeichnen statt stillschweigend zu setzen.
- Realistische Zahlenwerte verwenden (Ströme, Temperaturen, Zykluszeiten, Ausfallraten) und als plausible Beispielwerte kennzeichnen — nicht als validierte Daten.

### Ablauf & Interaktion

1. Stelle zuerst **maximal 3 Rückfragen**, falls etwas den Projektzuschnitt wesentlich ändert. Sonst starte direkt.
2. Gib danach ein **Inhaltsverzeichnis mit geschätztem Umfang je Phase** aus.
3. Liefere dann **Phase für Phase**. Halte nach jeder Phase an und warte auf `weiter`.
4. Wenn ich `tiefer: <Thema>` schreibe, arbeite dieses Thema auf Detailniveau aus.
5. Wenn ich `kürzer` schreibe, verdichte die kommende Phase auf Übersichtsniveau.
6. Bleibe über alle Phasen **konsistent**: einmal vergebene IDs, Werte und Architekturelemente ändern sich nicht mehr ohne expliziten Änderungshinweis.

Beginne mit Schritt 1.

## ENDE PROMPT
