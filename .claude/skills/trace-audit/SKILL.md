---
name: trace-audit
description: Runs and interprets the traceability consistency check - finds orphan requirements, untested requirements, broken links, unallocated safety requirements and status violations - and generates the bidirectional traceability matrix and coverage KPIs. Use before closing a phase, before a baseline/tag, or when asked about traceability, coverage or the CI gate.
---

# Traceability audit

## Run it

```bash
python3 tools/trace_check.py            # human-readable report, exit 1 on findings
python3 tools/trace_check.py --json     # machine-readable
python3 tools/trace_check.py --matrix 07_verification/reports/traceability_matrix.md
```

Report the **actual output**, including failures. Never claim a clean trace without having run it.

## What it checks

| Check | Rule |
|---|---|
| `orphan` | Requirement other than `CR-` without `derived_from` |
| `dangling` | `derived_from` / `allocated_to` / `verified_by` points to a non-existent ID |
| `untested` | Requirement in status ≥ `reviewed` without `verified_by` |
| `unallocated` | Requirement with `asil != QM` and empty `allocated_to` |
| `asil-drop` | Derived requirement with a lower ASIL than its parent without a decomposition note |
| `duplicate-id` | Same ID in two files |
| `sg-uncovered` | `SG-xx` without at least one `FSR-` deriving from it |
| `hazard-uncovered` | `H-xx` with an ASIL other than QM and no `SG-` deriving from it |

## Coverage KPIs

```
Anforderungsabdeckung = Anforderungen mit ≥1 downstream-Trace / alle Anforderungen
Testabdeckung         = Anforderungen mit ≥1 verified_by / alle Anforderungen (Status ≥ reviewed)
Analyseabdeckung      = Sicherheitsanforderungen, die in FMEA/FTA/FMEDA referenziert sind / alle Sicherheitsanforderungen
```

Report each as `n/m = xx %`, and state the CI gate threshold that applies. For the Golden Thread the
target is 100 % — anything less is a finding, not a rounding issue.

## Golden Thread matrix

Full bidirectional chain, one row per link level:

`CR → SYS-REQ → FSR/TSR → HW-REQ/SW-REQ → Design-Element → TC → Ergebnis`

For everything outside the Golden Thread produce a condensed summary (counts per level plus the list
of findings), not the full matrix.

## Fixing findings

Findings are fixed **at the source record**, never by editing the generated matrix. If a requirement
genuinely has no downstream artefact yet, set its status to `draft` and record it as an open point —
do not fabricate a `verified_by` entry to silence the check.
