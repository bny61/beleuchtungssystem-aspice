#!/usr/bin/env python3
"""Erzeugt je Ordner mit Requirements-as-Code Datensaetzen eine README.md als Uebersicht.

Jeder Ordner, der mindestens eine Markdown-Datei mit YAML-Front-Matter und einem Feld `id`
enthaelt, bekommt eine generierte README.md mit einer klickbaren Tabelle aller Datensaetze.
GitHub zeigt diese Datei beim Oeffnen des Ordners automatisch an.

Nutzt denselben Front-Matter-Parser wie tools/trace_check.py -- keine Drittabhaengigkeit.

Nutzung:
    python3 tools/gen_index.py             # Uebersichten schreiben/aktualisieren
    python3 tools/gen_index.py --check     # nur pruefen, Exit 1 wenn veraltet
    python3 tools/gen_index.py --root DIR  # anderes Repo-Wurzelverzeichnis

Exit 0 = alles aktuell bzw. geschrieben, 1 = veraltet (nur bei --check), 2 = Fehler.

HINWEIS: Erzeugt Uebersichten fuer den Safety Case und ist damit -- wie trace_check.py --
Kandidat fuer eine Tool-Qualifikation (ISO 26262-8, Clause 11).
Siehe 09_process/plans/tool_qualification.md.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from trace_check import parse_front_matter, LIST_FIELDS  # noqa: E402

MARKER = "<!-- generiert von tools/gen_index.py -- nicht manuell bearbeiten -->"

SKIP_DIRS = {".git", ".github", ".claude", "node_modules", "__pycache__", "exports"}

# Ueberschrift und Beschreibung je bekanntem Ordner; unbekannte Ordner bekommen einen Default.
TITLES = {
    "01_requirements/customer": (
        "Kundenanforderungen (CR)",
        "Lastenheft-Auszug, ASPICE SYS.1. ASIL-Einstufung erfolgt ueber die HARA (Phase 2).",
    ),
    "01_requirements/system": (
        "Systemanforderungen (SYS-REQ)",
        "Abgeleitet aus CR und FSR, ASPICE SYS.2.",
    ),
    "02_safety/02_hara": (
        "Gefaehrdungen (H)",
        "Strukturierte Form der HARA-Zeilen, ISO 26262-3. Herleitung und Methodik in hara.md.",
    ),
    "02_safety/03_fsc": (
        "Safety Goals und Functional Safety Concept (SG, FSR)",
        "ISO 26262-3. Safety Goals mit Safe State und FTTI, daraus abgeleitete FSR.",
    ),
    "02_safety/04_tsc": (
        "Technisches Sicherheitskonzept (TSR)",
        "ISO 26262-4. Technische Sicherheitsanforderungen und ihre Allokation.",
    ),
    "02_safety/05_analyses": (
        "Sicherheitsanalysen und Risiken (RISK)",
        "FMEA, FTA, FMEDA, DFA, STPA sowie gefuehrte Risiken.",
    ),
    "05_hardware": (
        "Hardware-Anforderungen und Sicherheitsmechanismen (HW-REQ, SM)",
        "HWE.1-HWE.4, ISO 26262-5.",
    ),
    "06_software": (
        "Software-Anforderungen (SW-REQ)",
        "SWE.1-SWE.6, ISO 26262-6.",
    ),
    "07_verification/testcases": (
        "Testfaelle (TC)",
        "ASPICE SYS.4/SYS.5. Jeder Testfall verweist auf mindestens eine Anforderung.",
    ),
}

ID_SPLIT = re.compile(r"^(.*?)-(\d+)$")


def sort_key(rid: str):
    """Sortiert CR-2 vor CR-10 (numerisch statt lexikografisch)."""
    m = ID_SPLIT.match(rid)
    return (m.group(1), int(m.group(2))) if m else (rid, 0)


def short(text: str, limit: int = 130) -> str:
    """Kuerzt den Anforderungstext fuer die Tabellenspalte und entschaerft Pipes."""
    t = " ".join(str(text).split()).replace("|", "\\|")
    return t if len(t) <= limit else t[: limit - 1].rstrip() + "…"


def collect(root: Path) -> dict[Path, list[dict]]:
    """Sammelt alle Datensaetze, gruppiert nach Ordner."""
    groups: dict[Path, list[dict]] = {}
    for path in sorted(root.rglob("*.md")):
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        if path.name == "README.md":
            continue
        try:
            fm = parse_front_matter(path.read_text(encoding="utf-8"))
        except OSError:
            continue
        if not fm or "id" not in fm:
            continue
        for field in LIST_FIELDS:
            val = fm.get(field)
            if val is None:
                fm[field] = []
            elif isinstance(val, str):
                fm[field] = [val] if val.strip() else []
        fm["_name"] = path.name
        groups.setdefault(path.parent, []).append(fm)
    return groups


def render(folder_rel: str, records: list[dict]) -> str:
    title, desc = TITLES.get(
        folder_rel, (f"Datensaetze in `{folder_rel}`", "Automatisch erzeugte Uebersicht.")
    )
    records = sorted(records, key=lambda r: sort_key(str(r["id"])))

    lines = [
        f"# {title}",
        "",
        MARKER,
        "",
        desc,
        "",
        f"**{len(records)} Datensaetze.** Klick auf die ID oeffnet den Datensatz.",
        "",
        "| ID | Text | Typ | ASIL | Status | Quelle / Trace | Verifiziert durch |",
        "|---|---|---|---|---|---|---|",
    ]

    for r in records:
        rid = str(r["id"])
        trace = ", ".join(r["derived_from"]) or str(r.get("source", "") or "—")
        verified = ", ".join(r["verified_by"]) or "—"
        lines.append(
            "| [{id}]({file}) | {text} | {typ} | {asil} | {status} | {trace} | {ver} |".format(
                id=rid,
                file=r["_name"],
                text=short(r.get("text", "")),
                typ=r.get("type", "—"),
                asil=r.get("asil", "—"),
                status=r.get("status", "—"),
                trace=short(trace, 40),
                ver=verified,
            )
        )

    # Verdichtung nach Status und ASIL
    def tally(field: str) -> str:
        counts: dict[str, int] = {}
        for r in records:
            counts[str(r.get(field, "—"))] = counts.get(str(r.get(field, "—")), 0) + 1
        return " · ".join(f"{k}: {v}" for k, v in sorted(counts.items()))

    lines += [
        "",
        f"**Status:** {tally('status')}",
        "",
        f"**ASIL:** {tally('asil')}",
        "",
        "---",
        "",
        "Diese Uebersicht wird von `tools/gen_index.py` erzeugt und in der CI auf Aktualitaet",
        "geprueft. Aenderungen bitte am Datensatz vornehmen, nicht an dieser Datei.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", default=".", help="Repo-Wurzel (Default: .)")
    ap.add_argument("--check", action="store_true", help="nur pruefen, nichts schreiben")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"error: root not found: {root}", file=sys.stderr)
        return 2

    groups = collect(root)
    if not groups:
        print("Keine Datensaetze gefunden - nichts zu tun.")
        return 0

    stale: list[str] = []
    written: list[str] = []

    for folder, records in sorted(groups.items()):
        rel = folder.relative_to(root).as_posix()
        target = folder / "README.md"
        content = render(rel, records)

        if target.exists():
            existing = target.read_text(encoding="utf-8")
            if MARKER not in existing:
                print(
                    f"WARNUNG: {rel}/README.md ist nicht generiert (kein Marker) "
                    "- wird nicht ueberschrieben.",
                    file=sys.stderr,
                )
                continue
            if existing == content:
                continue

        if args.check:
            stale.append(rel)
        else:
            target.write_text(content, encoding="utf-8")
            written.append(f"{rel}/README.md ({len(records)} Datensaetze)")

    if args.check:
        if stale:
            print("Veraltete Uebersichten:")
            for s in stale:
                print(f"  - {s}/README.md")
            print("\nBitte 'python3 tools/gen_index.py' ausfuehren und Ergebnis committen.")
            return 1
        print(f"Alle Uebersichten aktuell ({len(groups)} Ordner).")
        return 0

    if written:
        print("Aktualisiert:")
        for w in written:
            print(f"  - {w}")
    else:
        print(f"Alle Uebersichten bereits aktuell ({len(groups)} Ordner).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
