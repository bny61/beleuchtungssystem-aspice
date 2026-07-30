#!/usr/bin/env python3
"""Traceability consistency check for the lighting-system ASPICE / ISO 26262 project.

Reads every Requirements-as-Code record (Markdown file with YAML front matter) under
01_requirements/, 02_safety/, 05_hardware/, 06_software/ and 07_verification/ and checks the
trace graph for orphans, dangling links, untested and unallocated requirements.

Standard library only -- no third-party dependency, which keeps the tool-qualification
argument (ISO 26262-8, Clause 11) as small as possible.

Usage:
    python3 tools/trace_check.py [--json] [--matrix OUTFILE] [--root DIR]

Exit code 0 = no findings, 1 = findings, 2 = usage/IO error.

NOTE: This script produces safety-case evidence. It is a tool-qualification candidate --
see 09_process/plans/tool_qualification.md.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SEARCH_DIRS = [
    "01_requirements",
    "02_safety",
    "05_hardware",
    "06_software",
    "07_verification",
]

ID_PATTERN = re.compile(r"^(CR|SYS-REQ|SG|FSR|TSR|HW-REQ|SW-REQ|SM|TC|A|RISK|H)-\d+")

# Datensatzarten, die keine Anforderung sind: Gefaehrdungen, Testfaelle, Annahmen, Risiken.
# Fuer sie gelten die Anforderungspruefungen (untested, unallocated, orphan) nicht.
NON_REQUIREMENT_KINDS = ("TC", "A", "RISK", "H")

ASIL_ORDER = {"QM": 0, "A": 1, "B": 2, "C": 3, "D": 4}

LIST_FIELDS = ("derived_from", "allocated_to", "verified_by", "tags")
STATUS_VALUES = (
    "draft",
    "reviewed",
    "approved",
    "implemented",
    "verified",
    "rejected",
)
# Statuses from which a requirement is expected to be verifiable / traced.
MATURE_STATUS = ("reviewed", "approved", "implemented", "verified")


# --------------------------------------------------------------------------- parsing


def parse_front_matter(text: str) -> dict | None:
    """Parse a minimal YAML subset: scalars, folded blocks (>, |) and lists.

    Returns None when the file has no front matter.
    """
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    block = text[3:end].strip("\n")

    data: dict = {}
    key: str | None = None
    mode: str | None = None  # 'fold' | 'list'
    buf: list[str] = []

    def flush() -> None:
        nonlocal key, mode, buf
        if key is None:
            return
        if mode == "fold":
            data[key] = " ".join(s.strip() for s in buf if s.strip())
        elif mode == "list":
            data[key] = [s for s in buf if s]
        key, mode, buf = None, None, []

    for raw in block.split("\n"):
        line = raw.rstrip()
        if not line.strip() or line.strip().startswith("#"):
            continue
        indented = line[0] in " \t"

        if indented and mode == "fold":
            buf.append(line)
            continue
        if indented and mode == "list" and line.strip().startswith("-"):
            buf.append(line.strip()[1:].strip().strip("'\""))
            continue

        flush()
        if ":" not in line:
            continue
        k, _, v = line.partition(":")
        key = k.strip()
        v = v.strip()

        if v in (">", "|", ">-", "|-"):
            mode, buf = "fold", []
        elif v.startswith("[") and v.endswith("]"):
            items = [s.strip().strip("'\"") for s in v[1:-1].split(",")]
            data[key] = [s for s in items if s]
            key, mode = None, None
        elif v == "":
            mode, buf = "list", []  # may turn out to be an empty value; flush handles it
        else:
            data[key] = v.strip("'\"")
            key, mode = None, None

    flush()
    # A key opened as a list but never filled is an empty value, not an empty list.
    return data


def load_records(root: Path) -> tuple[dict, list]:
    """Return ({id: record}, [findings]) for all records found under root."""
    records: dict[str, dict] = {}
    findings: list[dict] = []

    for sub in SEARCH_DIRS:
        base = root / sub
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*.md")):
            try:
                text = path.read_text(encoding="utf-8")
            except OSError as exc:  # pragma: no cover - IO edge case
                findings.append(
                    finding("io", "major", str(path), f"Datei nicht lesbar: {exc}")
                )
                continue
            fm = parse_front_matter(text)
            if fm is None or "id" not in fm:
                continue  # narrative document, not a requirement record

            rid = str(fm["id"]).strip()
            rel = str(path.relative_to(root))

            if not ID_PATTERN.match(rid):
                findings.append(
                    finding("id-scheme", "major", rel, f"ID '{rid}' folgt nicht dem ID-Schema")
                )
            if rid in records:
                findings.append(
                    finding(
                        "duplicate-id",
                        "blocker",
                        rel,
                        f"ID '{rid}' bereits vergeben in {records[rid]['_file']}",
                    )
                )
                continue

            for field in LIST_FIELDS:
                val = fm.get(field)
                if val is None:
                    fm[field] = []
                elif isinstance(val, str):
                    fm[field] = [val] if val.strip() else []

            fm["_file"] = rel
            records[rid] = fm

    return records, findings


# -------------------------------------------------------------------------- checking


def finding(kind: str, severity: str, where: str, message: str) -> dict:
    return {"check": kind, "severity": severity, "where": where, "message": message}


def asil_rank(value: str | None) -> int | None:
    """Rank an ASIL value; 'B(D)' decomposition notation ranks by its own ASIL (B)."""
    if not value:
        return None
    head = str(value).strip().split("(")[0].strip().upper()
    return ASIL_ORDER.get(head)


def check(records: dict) -> list[dict]:
    findings: list[dict] = []
    known = set(records)

    # Reverse index: which records derive from / verify a given id.
    derived_children: dict[str, list[str]] = {rid: [] for rid in records}
    for rid, rec in records.items():
        for parent in rec["derived_from"]:
            derived_children.setdefault(parent, []).append(rid)

    for rid, rec in sorted(records.items()):
        where = f"{rec['_file']} ({rid})"
        kind = rid.split("-")[0] if not rid.startswith(("SYS-REQ", "HW-REQ", "SW-REQ")) else rid.rsplit("-", 1)[0]
        status = str(rec.get("status", "draft")).strip().lower()
        asil = rec.get("asil")

        if status not in STATUS_VALUES:
            findings.append(
                finding("status", "minor", where, f"Unbekannter Status '{status}'")
            )

        # orphan: everything except CR, SG, A, RISK needs an upstream link
        if kind not in ("CR", "SG", "H", "A", "RISK", "TC") and not rec["derived_from"]:
            findings.append(
                finding("orphan", "major", where, "Kein 'derived_from' - Anforderung ohne Quelle")
            )

        # dangling references
        for field in ("derived_from", "allocated_to", "verified_by"):
            for ref in rec[field]:
                if ID_PATTERN.match(ref) and ref not in known:
                    findings.append(
                        finding(
                            "dangling",
                            "major",
                            where,
                            f"{field} verweist auf unbekannte ID '{ref}'",
                        )
                    )

        # untested
        if kind not in NON_REQUIREMENT_KINDS and status in MATURE_STATUS and not rec["verified_by"]:
            findings.append(
                finding(
                    "untested",
                    "major",
                    where,
                    f"Status '{status}' ohne 'verified_by' - kein Verifikationsnachweis",
                )
            )

        # unallocated safety requirement
        if kind not in ("SG",) + NON_REQUIREMENT_KINDS:
            rank = asil_rank(asil)
            if rank is not None and rank > 0 and not rec["allocated_to"]:
                findings.append(
                    finding(
                        "unallocated",
                        "major",
                        where,
                        f"ASIL {asil} ohne 'allocated_to' - keine Zuordnung zu einem Element",
                    )
                )

            # asil-drop against parents
            child_rank = asil_rank(asil)
            for parent in rec["derived_from"]:
                prec = records.get(parent)
                if not prec:
                    continue
                prank = asil_rank(prec.get("asil"))
                if child_rank is None or prank is None:
                    continue
                decomposed = "(" in str(asil) or str(rec.get("decomposition", "")).strip()
                if child_rank < prank and not decomposed:
                    findings.append(
                        finding(
                            "asil-drop",
                            "blocker",
                            where,
                            f"ASIL {asil} niedriger als Elternanforderung {parent} "
                            f"(ASIL {prec.get('asil')}) ohne Dekompositionsnachweis",
                        )
                    )

        # hazard coverage: jede Gefaehrdung mit ASIL != QM braucht ein Safety Goal
        if kind == "H":
            rank = asil_rank(asil)
            if rank is not None and rank > 0:
                sgs = [c for c in derived_children.get(rid, []) if c.startswith("SG-")]
                if not sgs:
                    findings.append(
                        finding(
                            "hazard-uncovered",
                            "blocker",
                            where,
                            f"Gefaehrdung mit ASIL {asil} ohne abgeleitetes Safety Goal",
                        )
                    )

        # safety goal coverage
        if kind == "SG":
            fsrs = [c for c in derived_children.get(rid, []) if c.startswith("FSR-")]
            if not fsrs:
                findings.append(
                    finding("sg-uncovered", "blocker", where, "Safety Goal ohne abgeleitete FSR")
                )

    return findings


# ---------------------------------------------------------------------------- output


def kpis(records: dict) -> dict:
    reqs = {
        rid: r
        for rid, r in records.items()
        if not rid.startswith(("TC-", "A-", "RISK-", "SM-", "H-"))
    }
    mature = {
        rid: r
        for rid, r in reqs.items()
        if str(r.get("status", "draft")).lower() in MATURE_STATUS
    }
    downstream = {rid for rid, r in reqs.items() if r["verified_by"] or r["allocated_to"]}
    tested = {rid for rid, r in mature.items() if r["verified_by"]}

    def pct(n: int, m: int) -> str:
        return f"{n}/{m} = {(100.0 * n / m):.0f} %" if m else f"{n}/0 = n/a"

    return {
        "Anforderungsabdeckung": pct(len(downstream), len(reqs)),
        "Testabdeckung": pct(len(tested), len(mature)),
        "Datensaetze gesamt": str(len(records)),
    }


def build_matrix(records: dict) -> str:
    rows = ["# Traceability-Matrix (generiert)", "",
            "> Automatisch erzeugt von `tools/trace_check.py` - nicht manuell bearbeiten.", "",
            "| ID | Typ | ASIL | Status | derived_from | allocated_to | verified_by | Datei |",
            "|---|---|---|---|---|---|---|---|"]
    for rid, rec in sorted(records.items()):
        rows.append(
            "| {id} | {typ} | {asil} | {status} | {df} | {al} | {vb} | `{f}` |".format(
                id=rid,
                typ=rec.get("type", "-"),
                asil=rec.get("asil", "-"),
                status=rec.get("status", "-"),
                df=", ".join(rec["derived_from"]) or "-",
                al=", ".join(rec["allocated_to"]) or "-",
                vb=", ".join(rec["verified_by"]) or "-",
                f=rec["_file"],
            )
        )
    return "\n".join(rows) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", default=".", help="repo root (default: .)")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--matrix", metavar="OUTFILE", help="write the traceability matrix")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"error: root not found: {root}", file=sys.stderr)
        return 2

    records, load_findings = load_records(root)
    findings = load_findings + check(records)
    metrics = kpis(records)

    if args.matrix:
        out = Path(args.matrix)
        if not out.is_absolute():
            out = root / out
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(build_matrix(records), encoding="utf-8")

    if args.json:
        print(json.dumps({"findings": findings, "kpis": metrics,
                          "record_count": len(records)}, indent=2, ensure_ascii=False))
        return 1 if findings else 0

    print(f"Traceability-Check - {len(records)} Datensaetze aus {root}")
    print("-" * 72)
    if not records:
        print("Keine Requirements-as-Code Datensaetze gefunden.")
        print("Erwartet: Markdown mit YAML-Front-Matter unter " + ", ".join(SEARCH_DIRS))
    for key, value in metrics.items():
        print(f"  {key:<24} {value}")
    print("-" * 72)

    if not findings:
        print("Keine Findings.")
        return 0

    order = {"blocker": 0, "major": 1, "minor": 2, "observation": 3}
    for f in sorted(findings, key=lambda x: (order.get(x["severity"], 9), x["where"])):
        print(f"[{f['severity'].upper():<8}] {f['check']:<14} {f['where']}")
        print(f"           {f['message']}")
    print("-" * 72)
    counts: dict[str, int] = {}
    for f in findings:
        counts[f["severity"]] = counts.get(f["severity"], 0) + 1
    print("Findings: " + ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    return 1


if __name__ == "__main__":
    sys.exit(main())
